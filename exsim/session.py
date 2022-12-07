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


logging.basicConfig(level=logging.DEBUG)


class Session:

    def __init__(self, sock, addr):
        self._socket = sock
        self._address = addr

        self._gateway = None
        self._protocol = None
        self._engine = None
        return

    def socket(self):
        return self._socket

    def address(self):
        return self._address

    def set_gateway(self, gateway):
        self._gateway = gateway
        return

    def set_engine(self, engine):
        self._engine = engine
        return

    def set_protocol(self, protocol):
        self._protocol = protocol(self)
        return

    def close(self):
        self._socket.close()
        self._address = None
        return

    def readable(self):
        data = self._socket.recv(8192)
        if len(data) == 0:
            self._gateway.session_closed(self)
            return

        self._protocol.receive(data)
        return

    def send(self, data):
        return self._socket.sendall(data)
