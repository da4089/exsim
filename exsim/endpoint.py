#! /usr/bin/python

import datetime
import logging
import select
import socket
import time

from fix_protocol import FixParser, FixMessage, print_fix

logging.basicConfig(level=logging.DEBUG)



class Endpoint(object):

    def __init__(self):
        return

    def listen(self, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(('0.0.0.0', port))
        self._socket.listen(5)
        return self._socket

    def close(self):
        return

    def socket(self):
        return self._socket



    def set_protocol(self, name):
        return


    def connect_engine(self, name):
        return

