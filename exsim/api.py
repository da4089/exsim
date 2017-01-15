#! /usr/bin/env python

import logging
import pickle
import socket
import struct

logging.basicConfig(level=logging.DEBUG)


class API:
    """Client API."""

    def __init__(self):
        self._socket = None
        self._buffer = ''
        self._connected = False
        return

    def connect(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, int(port)))
        self._connected = True
        logging.info("Connected: %s:%u" % (host, int(port)))
        return

    def send(self, request, reply):

        # Send request.
        body = pickle.dumps(request)
        header = struct.pack("<L", len(body))
        self._socket.sendall(header + body)
        logging.debug("Sent")

        # Wait for reply.
        while True:
            data = self._socket.recv(8192)
            logging.debug("Received")
            if len(data) == 0:
                self._connected = False
                # FIXME: set error in reply
                return False

            self._buffer += data
            if len(self._buffer) < 4:
                continue

            length = struct.unpack("<L", self._buffer[:4])[0]
            if len(self._buffer) < length + 4:
                continue

            tmp = pickle.loads(self._buffer[4:4+length])
            reply.update(tmp)
            self._buffer = self._buffer[4+length:]
            if len(self._buffer) > 0:
                # FIXME: report error
                pass

            return True


if __name__ == "__main__":
    api = API()
    api.connect("localhost", 10101)

    request = {'type': 'create_engine', 'name': 'e1'}
    reply = {}
    api.send(request, reply)
