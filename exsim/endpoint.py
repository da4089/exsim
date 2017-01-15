#! /usr/bin/python

import logging
import socket

logging.basicConfig(level=logging.DEBUG)



class Endpoint(object):

    def __init__(self, name, port):
        self._name = name
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(('0.0.0.0', port))
        self._socket.listen(5)
        return

    def close(self):
        return

    def socket(self):
        return self._socket

    # FIXME: add accept()

    # FIXME: move to session
    def send(self, buffer):
        return self._socket.send(buffer)


    def set_protocol(self, name):
        return


    def connect_engine(self, name):
        return
