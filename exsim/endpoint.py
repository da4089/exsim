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
import socket

from .session import Session


logging.basicConfig(level=logging.DEBUG)


class Endpoint(object):

    def __init__(self, name: str, port: int):
        """Constructor.

        :param name: Name of listening endpoint.
        :param port: TCP port number on which to accept connections."""
        self._name = name
        self._engine = None
        self._protocol = None

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(('0.0.0.0', port))
        self._socket.listen(5)
        return

    def socket(self):
        """Return listening socket."""
        return self._socket

    def set_engine(self, engine):
        """Set matching engine for this endpoint.

        :param engine: Matching engine."""
        self._engine = engine
        return

    def set_protocol(self, protocol):
        """Set protocol for this endpoint.

        :param protocol: FIXME"""
        self._protocol = protocol
        return

    def close(self):
        """Stop listening for connections on this endpoint."""
        self._socket.close()
        self._socket = None
        return

    def accept(self) -> Session:
        """Accept an inbound connection to this endpoint."""
        client_sock, client_addr = self._socket.accept()
        session = Session(client_sock, client_addr)
        session.set_engine(self._engine)
        session.set_protocol(self._protocol)
        return session
