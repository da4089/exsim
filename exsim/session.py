#! /usr/bin/python

import logging

from manager import Manager


logging.basicConfig(level=logging.DEBUG)



class Session(object):

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
        self._protocol = protocol
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