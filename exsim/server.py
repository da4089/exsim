# -*- coding: utf-8 -*-
########################################################################
# exsim - Exchange Simulator
# Copyright (C) 2016-2022, zeroXone.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/
#
########################################################################

import logging
import select
import socket
import time
import typing

from .endpoint import Endpoint
from .engine import Engine
from .manager import Manager
from .protocol import Protocol
from .session import Session

# FIXME: this should be loaded as a plugin
from .default_engine import DefaultEngine


logging.basicConfig(filename="xs.log", level=logging.DEBUG)


class Server:

    def __init__(self):
        """Constructor."""

        self._engine_types: typing.Dict[str, type(Engine)] = {}

        self._engines: typing.Dict[str, Engine] = {}
        self._endpoints: typing.Dict[str, Endpoint] = {}
        self._protocols: typing.Dict[str, Protocol] = {}

        self._session_socks: typing.Dict[socket, Session] = {}
        self._manager_socks: typing.Dict[socket, Manager] = {}
        self._endpoint_socks: typing.Dict[socket, Endpoint] = {}

        self._is_running: bool = True
        self._timeouts: typing.List = []

        # Management interface.
        self._mgmt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._mgmt_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._mgmt_sock.bind(('0.0.0.0', 0))
        self._mgmt_sock.listen(5)
        return

    def get_port(self) -> int:
        """Return integer port number for management socket."""
        _, port = self._mgmt_sock.getsockname()
        return port

    def authenticate(self, username, password, source_address):
        return

    def create_manager(self, sock):
        mgmt_sock, mgmt_addr = sock.accept()
        manager = Manager(mgmt_sock, mgmt_addr)
        self._manager_socks[mgmt_sock] = manager
        manager.set_server(self)

        logging.info("New manager %d from %s"
                     % (manager.socket().fileno(), str(mgmt_addr)))
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

        logging.info("New session %d from %s"
                     % (session.socket().fileno(), str(session.address())))
        return

    def session_closed(self, session):
        del self._session_socks[session.socket()]
        logging.info("Closed %d" % session.socket().fileno())
        session.close()
        return

    def get_session_socks(self):
        return [x.socket() for x in self._session_socks.values()]

    def get_endpoints(self):
        return [e.socket() for e in self._endpoints.values()]

    def get_manager_socks(self):
        return [m.socket() for m in self._manager_socks.values()]

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

    def load_engine(self, name, module_name, class_name):
        """Load a protocol plugin.

        :param name: String name for this engine.
        :param module_name: String name for the module file.
        :param class_name: String name for the engine class."""

        if name in self._engine_types:
            return KeyError(f"Engine type '{name}' already loaded")

        # FIXME: sanitize!
        d = {}
        exec(f"from exsim import {module_name}", globals(), d)
        exec(f"engine = {module_name}.{class_name}", globals(), d)
        self._engine_types[name] = d["engine"]
        logging.info(f"Loaded engine type '{name}'")
        return

    def create_engine(self, name: str, engine_type: str):
        if name in self._engines:
            raise KeyError(f"Engine '{name}' already exists")

        if engine_type not in self._engine_types:
            raise KeyError(f"Engine type '{engine_type}' not leaded")

        # FIXME: need to lookup the engine type name here
        engine = self._engine_types[engine_type](name)
        self._engines[name] = engine
        return engine

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

    def load_protocol(self, name, module_name, class_name):
        """Load a protocol plugin.

        :param name: String name for this protocol.
        :param module_name: String name for the module file.
        :param class_name: String name for the protocol class."""

        if name in self._protocols:
            return KeyError(f"Protocol '{name}' already loaded")

        # FIXME: sanitise!
        d = {}
        exec(f"from exsim import {module_name}", globals(), d)
        exec(f"protocol = {module_name}.{class_name}", globals(), d)
        self._protocols[name] = d["protocol"]
        logging.info(f"Loaded protocol {name}")
        return

    def create_endpoint(self,
                        name: str,
                        port: int,
                        protocol_name: str,
                        engine_name: str):
        """Create a new Endpoint, listening for client connections."""
        if name in self._endpoints:
            return KeyError(f"Endpoint '{name}' already exists")

        protocol = self._protocols.get(protocol_name)
        if not protocol:
            return KeyError(f"Protocol '{protocol_name}' not found")

        engine = self._engines.get(engine_name)
        if not engine:
            return KeyError(f"Engine '{engine_name}' not found")

        endpoint = Endpoint(name, port, protocol, engine)
        self._endpoints[name] = endpoint
        self._endpoint_socks[endpoint.socket()] = endpoint
        return

    def set_endpoint_property(self, name, value):
        if name not in self._endpoints:
            return KeyError("No such endpoint: '%s'" % name)

        endpoint = self._endpoints[name]
        endpoint.set_property(name, value)
        return
