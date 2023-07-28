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

from .engine import Engine
from .protocol import Protocol
from .session import Session


class Endpoint:
    """
    An Endpoint represents the combination of a listening socket,
    a Protocol, and an Engine.  The endpoint accepts connections from
    clients, and creates a Session for each connection.
    """

    def __init__(self, name: str, port: int, protocol: Protocol, engine: Engine):
        """Constructor.

        :param name: Name of listening endpoint.
        :param port: TCP port number on which to accept connections.
        :param protocol: Protocol instance for this Endpoint.
        :param engine: Engine instance to receive inbound messages."""

        self._name = name
        self._port = port
        self._protocol = protocol
        self._engine = engine

        # Open socket and listen for connections.
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(('0.0.0.0', self._port))
        self._socket.listen(5)
        return

    def socket(self):
        """Return listening socket."""
        return self._socket

    def engine(self):
        """Return reference to Endpoint's configured Engine."""
        return self._engine

    def protocol(self):
        """Return reference to Endpoint's configured Protocol."""
        return self._protocol

    def close(self):
        """Stop listening for connections on this endpoint."""
        self._socket.close()
        self._socket = None
        return

    def accept(self) -> Session:
        """Accept an inbound connection to this endpoint."""
        client_sock, client_addr = self._socket.accept()
        session = Session(client_sock, client_addr, self)
        return session
