#! /usr/bin/python

import datetime
import logging
import select
import socket
import time

from engine import Engine
from manager import Manager
from endpoint import Endpoint


logging.basicConfig(level=logging.DEBUG)


class Server(object):

    def __init__(self):
        self._engines = {}  # name: engine
        self._endpoints = {}  # name: endpoint

        self._session_socks = {}  #  socket: session
        self._manager_socks = {}  #  socket: manager
        self._endpoint_socks = {}  # socket: endpoint

        self._is_running = True
        self._timeouts = []

        # Management interface.
        self._mgmt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._mgmt_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._mgmt_sock.bind(('0.0.0.0', 10101))
        self._mgmt_sock.listen(5)
        return

    def authenticate(self, username, password, source_addreess):
        return

    def create_manager(self, sock):
        mgmt_sock, mgmt_addr = sock.accept()
        manager = Manager(mgmt_sock, mgmt_addr)
        self._manager_socks[mgmt_sock] = manager
        manager.set_server(self)

        logging.info("New manager %d from %s" % (manager.socket().fileno(), str(mgmt_addr)))
        return

    def manager_closed(self, manager):
        del self._manager_socks[manager.socket()]
        logging.info("Closed manager %d" % manager.socket().fileno())
        manager.close()
        return


    def create_session(self, sock):
        """Accept a connection to an endpoint, and create a session."""

        endpoint = self._endpoint_socks[sock]
        session = endpoint.accept()
        self._session_socks[session.socket()] = session
        session.set_gateway(self)

        logging.info("New session %d from %s" % (session.socket().fileno(), str(session.address())))
        return

    def session_closed(self, session):
        del self._session_socks[session.socket()]
        logging.info("Closed %d" % session.socket().fileno())
        session.close()
        return

    def get_session_socks(self):
        return reduce(lambda l, x: l.append(x.socket()) or l, self._session_socks.values(), [])

    def get_endpoints(self):
        return reduce(lambda l, e: l.append(e.socket()) or l, self._endpoints.values(), [])

    def get_manager_socks(self):
        return reduce(lambda l, m: l.append(m.socket()) or l, self._manager_socks.values(), [])

    def run(self):
        while self._is_running:
            now = time.time()
            while True:
                if len(self._timeouts) == 0:
                    break

                expiry, callback = self._timeouts[0]
                if expiry > now:
                    break

                callback()
                self._timeouts.pop(0)

            if len(self._timeouts) > 0:
                wait = self._timeouts[0][0] - time.time()
                if wait < 0:
                    wait = 0
            else:
                wait = 1.0

            sessions = self.get_session_socks()
            endpoints = self.get_endpoints()
            managers = self.get_manager_socks()

            r, w, x = select.select(sessions +
                                    endpoints +
                                    managers +
                                    [self._mgmt_sock],
                                    [], [], wait)

            for s in r:
                if s in sessions:
                    msg = self._session_socks[s].readable()
                elif s in endpoints:
                    self.create_session(s)
                elif s in managers:
                    self._manager_socks[s].readable()
                else:
                    self.create_manager(s)
        return


    def add_timeout(self, expiry_time, callback):
        t = (expiry_time, callback)
        self._timeouts.append(t)
        self._timeouts.sort()
        return


    def delete_timeout(self, expiry_time, callback):
        t = (expiry_time, callback)
        self._timeouts.remove(t)
        return


    def create_engine(self, name):
        if name in self._engines:
            raise KeyError("Engine '%s' already exists" % name)

        engine = Engine(name)
        self._engines[name] = engine
        return


    def delete_engine(self, name):
        if name not in self._engines:
            raise KeyError("No such engine: '%s'" % name)

        engine = self._engines[name]
        del self._engines[name]
        engine.delete()
        return


    def set_engine_property(self, name, value):
        if name not in self._engines:
            raise KeyError("No such engine: '%s'" % name)

        engine = self._engines[name]
        engine.set_property(name, value)
        return


    def start_engine(self, name):
        if name not in self._engines:
            raise KeyError("No such engine: '%s'" % name)

        self._engines[name].start()
        return


    def stop_engine(self, name):
        if name not in self._engines:
            raise KeyError("No such engine: '%s'" % name)

        self._engines[name].stop()
        return


    def create_endpoint(self, name, port):
        if name in self._endpoints:
            return KeyError("Endpoint '%s' already exists" % name)

        endpoint = Endpoint(name, port)
        self._endpoints[name] = endpoint
        self._endpoint_socks[endpoint.socket()] = endpoint
        return


    def set_endpoint_engine(self, endpoint_name, engine_name):
        if endpoint_name not in self._endpoints:
            return KeyError("No such endpoint: '%s'" % endpoint_name)

        if engine_name not in self._engines:
            raise KeyError("No such engine: '%s'" % engine_name)

        endpoint = self._endpoints[endpoint_name]
        engine = self._engines[engine_name]
        endpoint.set_engine(engine)
        return


    def set_endpoint_property(self, name, value):
        if name not in self._endpoints:
            return KeyError("No such endpoint: '%s'" % name)

        endpoint = self._endpoints[name]
        endpoint.set_property(name, value)
        return
