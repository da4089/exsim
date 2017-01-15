#! /usr/bin/env python

import logging
import pickle
import struct

logging.basicConfig(level=logging.DEBUG)


class Manager(object):
    """Server manager."""

    def __init__(self, sock, addr):
        self._socket = sock
        self._address = addr
        self._server = None
        self._buffer = ""
        return

    def set_server(self, server):
        self._server = server
        return

    def socket(self):
        return self._socket

    def close(self):
        self._socket.close()
        self._address = None
        return

    def readable(self):
        data = self._socket.recv(8192)
        if len(data) == 0:
            self._server.manager_closed(self)
            return

        self._buffer += data

        msg = self.parse_message()
        if not msg:
            return

        self.dispatch(msg)
        return

    def send(self, msg):
        data = pickle.dumps(msg)
        header = struct.pack("<L", len(data))
        self._socket.sendall(header + data)
        return

    def parse_message(self):

        # Check we have a header.
        if len(self._buffer) < 4:
            logging.debug("Manager buffer < 4")
            return None

        # Unpack header, and sanity check.
        l = struct.unpack("<L", self._buffer[:4])[0]
        if l > 65535:
            logging.debug("Manager buffer > 64KB (%d)" % l)
            return None

        # Check we have the full packet.
        if len(self._buffer) < l + 4:
            logging.debug("Manager received message fragment")
            return None

        msg = pickle.loads(self._buffer[4:l+4])
        self._buffer = self._buffer[l+4:]

        return msg


    def dispatch(self, message):
        """Handle a decoded management session message."""

        if not hasattr(self, "handle_" + message["type"]):
            logging.warning("No handler for '%s' request" % message["type"])
            # FIXME: create error reply.
            return

        reply = {}
        handler = getattr(self, 'handle_' + message["type"])
        handler(message, reply)
        self.send(reply)
        return


    def set_error(self, reply, request_name, error):
        logging.info("Request '%s' failed: %s" % (request_name, error))

        reply["result"] = False
        reply["message"] = error
        return

    def set_success(self, reply, request_name):
        logging.info("Request '%s': succeeded" % request_name)
        reply["result"] = True
        return

    def check_parameters(self, request, reply, names):
        for name in names:
            if name not in request:
                self.set_error(reply,
                               request["type"],
                               "Missing '%s' parameter" % name)
                return False
        return True

    def handle_create_engine(self, request, reply):
        if not self.check_parameters(request, reply, ['name']):
            return
        try:
            self._server.create_engine(request["name"])
            self.set_success(reply, "create_engine")
        except Exception as e:
            self.set_error(reply, "create_engine", e.message)
        return

    def handle_delete_engine(self, request, reply):
        if not self.check_parameters(request, reply, ['name']):
            return
        try:
            self._server.delete_engine(request["name"])
            self.set_success(reply, "delete_engine")
        except Exception as e:
            self.set_error(reply, "delete_engine", e.message)
        return

    def handle_create_endpoint(self, request, reply):
        if not self.check_parameters(request, reply, ['name', 'port']):
            return
        try:
            self._server.create_endpoint(request["name"], request["port"])
            self.set_success(reply, "create_endpoint")
        except Exception as e:
            self.set_error(reply, "create_endpoint", e.message)
        return

    def handle_set_endpoint_engine(self, request, reply):
        if not self.check_parameters(request, reply, []):
            return
        try:
            self._server.set_endpoint_engine(request["endpoint"], request["engine"])
            self.set_success(reply, "set_endpoint_engine")
        except Exception as e:
            self.set_error(reply, "set_endpoint_engine", e.message)
        return
