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


class Session:
    """
    A Session represents an:
    - An active client connection, eg. a TCP session
    - A Protocol instance, and
    """

    def __init__(self, sock: socket.socket, addr, endpoint: 'Endpoint'):
        self._socket = sock
        self._address = addr
        self._endpoint = endpoint

        self._protocol = self._endpoint.protocol()
        self._engine = self._endpoint.engine()
        return

    def socket(self):
        """Return reference to the Session's socket."""
        return self._socket

    def address(self):
        """Return reference to the Session's address."""
        return self._address

    def engine(self):
        """Return reference to Session's Engine."""
        return self._engine

    def protocol(self):
        """Return reference to Session's Protocol."""
        return self._protocol

    def close(self):
        """Close this session."""
        self._socket.close()
        self._address = None
        return

    def readable(self):
        data = self._socket.recv(8192)
        if len(data) == 0:
            self._gateway.session_closed(self)
            return

        message = self._protocol.receive(data)
        if message:
            self._engine.deliver(message)
        return

    def send(self, data: bytes):
        """Send the supplied data to the session's peer."""
        return self._socket.sendall(data)
