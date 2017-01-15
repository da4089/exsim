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

    def create_engine(self, name):
        request = {'type': 'create_engine', 'name': name}
        reply = {}
        api._send(request, reply)

        result = reply["result"]
        if not result:
            raise Exception(reply["message"])
        return

    def create_endpoint(self, name, port):
        request = {"type": "create_endpoint", "name": name, "port": port}
        reply = {}
        api._send(request, reply)

        result = reply["result"]
        if not result:
            raise Exception(reply["message"])
        return

    def set_endpoint_engine(self, engine, endpoint):
        request = {"type": "set_endpoint_engine",
                   "engine": engine,
                   "endpoint": endpoint}
        reply = {}
        api._send(request, reply)

        result = reply["result"]
        if not result:
            raise Exception(reply["message"])
        return

    def load_protocol(self, name, module, klass):
        request = {"type": "load_protocol",
                   "name": name,
                   "module": module,
                   "class": klass}
        reply = {}
        api._send(request, reply)

        result = reply["result"]
        if not result:
            raise Exception(reply["message"])
        return


    def set_endpoint_protocol(self, endpoint, protocol):
        request = {"type": "set_endpoint_protocol",
                   "endpoint": endpoint,
                   "protocol": protocol}
        reply = {}
        api._send(request, reply)

        result = reply["result"]
        if not result:
            raise Exception(reply["message"])
        return


    def delete_engine(self, name):
        request = {"type": "delete_engine", "name": name}
        reply = {}
        api._send(request, reply)

        result = reply["result"]
        if not result:
            raise Exception(reply["message"])
        return


    def _send(self, request, reply):

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


########################################################################

class Server(object):
    def __init__(self, name):
        self.name = name
        return

    def load_protocol(self, name, module):
        return

class Engine(object):
    def __init__(self, name):
        self.name = name
        return

    def create_endpoint(self, name):
        ep = Endpoint(name)
        self._endpoints[name] = ep
        return ep

    def create_message(self, name):
        msg = Message(name)
        self._messages[name] = msg
        return msg

class Endpoint(object):
    def __init__(self, name):
        self.name = name
        return

class Session(object):
    pass

class Message(object):
    pass



########################################################################

if __name__ == "__main__":
    api = API()
    api.connect("localhost", 10101)
    api.create_engine("e1")
    api.create_endpoint("ep1", 10102)
    api.set_endpoint_engine("ep1", "e1")
    api.load_protocol("fix", "fix_protocol", "FixProtocol")
    api.set_endpoint_protocol("ep1", "fix")

    # api.accept_session("ep1", "s1")
    # api.get_session_message("s1", "m1")
    # api.process_message("e1", "m1", "m2")
    # api.send_session_message("s1", "m2")

    # api.set_endpoint_property("ep1", "auto_accept", "true")

    # api.set_engine_property("e1", "auto_receive", "true")
    # api.set_endpoint_property("ep1", "auto_receive", "true")
    # api.set_session_property("s1", "auto_receive", "true")



    api.delete_engine("e1")
