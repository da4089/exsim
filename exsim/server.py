#! /usr/bin/python

import datetime
import logging
import select
import socket
import time

from fix_protocol import FixParser, FixMessage, print_fix
from engine import Engine
from manager import Manager
from endpoint import Endpoint


logging.basicConfig(level=logging.DEBUG)


class Server(object):

    def __init__(self):
        self._engines = {}
        self._sessions = {}  #  socket: session
        self._endpoints = {}  # socket: endpoint
        self._managers = {}  #  socket: manager
        self._is_running = True
        self._timeouts = []

        # Management interface.
        self._mgmt_ep = Endpoint()
        self._mgmt_sock = self._mgmt_ep.listen(10101)
        return

    def set_engine(self, engine):
        self._engine = engine
        return

    def listen(self, port):
        e = Endpoint()
        sock = e.listen(port)
        self._endpoints[sock] = e
        return

    def authenticate(self, username, password, source_addreess):
        return

    def create_manager(self, sock):
        mgmt_sock, mgmt_addr = sock.accept()
        manager = Manager(mgmt_sock, mgmt_addr)
        self._managers[mgmt_sock] = manager
        manager.set_server(self)

        logging.info("New manager %d from %s" % (manager.socket().fileno(), str(mgmt_addr)))
        return

    def manager_closed(self, manager):
        del self._managers[manager.socket()]
        logging.info("Closed manager %d" % manager.socket().fileno())
        manager.close()
        return

    def create_session(self, sock):
        client_sock, client_addr = sock.accept()
        session = Session(client_sock, client_addr)
        self._sessions[client_sock] = session
        session.set_gateway(self)

        logging.info("New session %d from %s" % (session.socket().fileno(), str(client_addr)))
        return

    def session_closed(self, session):
        del self._sessions[session.socket()]
        logging.info("Closed %d" % session.socket().fileno())
        session.close()
        return

    def get_sessions(self):
        return reduce(lambda l, x: l.append(x.socket()) or l, self._sessions.values(), [])

    def get_endpoints(self):
        return reduce(lambda l, e: l.append(e.socket()) or l, self._endpoints.values(), [])

    def get_managers(self):
        return reduce(lambda l, m: l.append(m.socket()) or l, self._managers.values(), [])

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

            sessions = self.get_sessions()
            endpoints = self.get_endpoints()
            managers = self.get_managers()

            r, w, x = select.select(sessions +
                                    endpoints +
                                    managers +
                                    [self._mgmt_sock],
                                    [], [], wait)

            for s in r:
                if s in sessions:
                    msg = self._sessions[s].readable()
                elif s in endpoints:
                    self.create_session(s)
                elif s in managers:
                    self._managers[s].readable()
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
            raise KeyError()

        engine = self._engines[name]
        del self._engines[name]
        engine.delete()
        return

    def set_engine_property(self, name, value):
        return

    def start_engine(self, name):
        if name not in self._engines:
            raise KeyError()

        self._engines[name].start()
        return

    def stop_engine(self, name):
        if name not in self._engines:
            raise KeyError()

        self._engines[name].stop()
        return


    def create_endpoint(self, name):
        if name in self._endpoints:
            return KeyError()

        endpoint = Endpoint(name)
        self._endpoints[name] = endpoint

        return
