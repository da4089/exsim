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

import exsim
import logging
import os
import pickle
import signal
import socket
import struct
import sys

logging.basicConfig(level=logging.DEBUG)


class API:
    """Client API."""

    def __init__(self):
        self._buffer = ''
        self._servers = {}
        self._connected = False
        return

    def delete(self):
        for server in self._servers:
            server.delete()
        self._servers = {}
        self._buffer = ''
        return

    def create_server(self, name):
        # Create pipe to receive port from child.
        pr, pw = os.pipe()

        # Fork server process off API.
        pid = os.fork()
        if pid == 0:
            # Child (server)

            # Daemonise.
            r = open("/dev/null", "r")
            w = open("/dev/null", "w")

            sys.stderr.close()
            sys.stdout.close()
            sys.stdin.close()

            sys.stdin = r
            sys.stdout = w
            sys.stderr = w

            # Create main Server class.
            server = exsim.Server()

            # Return control port number to parent process.
            port = server.get_port()
            os.close(pr)
            pw = os.fdopen(pw, 'w')
            pw.write(str(port))
            pw.flush()
            pw.close()

            # Enter server mainloop.
            server.run()

            # Exit server process.
            sys.exit(0)

        # Wait to receive server's control port number.
        os.close(pw)
        pr = os.fdopen(pr)
        s = pr.read(10)
        port = int(s)
        pr.close()

        # Connect to server.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', port))
        self._connected = True
        logging.info("Connected")

        # Create server proxy class in API.
        s = Server(self, name, sock, pid)
        self._servers[name] = s
        return s

    def delete_server(self, name):
        server = self._servers.get(name, None)
        if not server:
            raise KeyError("No such server: %s" % name)
        server.delete()
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


class Server(object):
    def __init__(self, api, name, sock, pid):
        self._api = api
        self._name = name

        self._socket = sock
        self._child_pid = pid
        self._buffer = ''
        return

    def delete(self):
        os.kill(self._child_pid, signal.SIGINT)
        pid, status = os.waitpid(self._child_pid, 0)
        return

    def load_protocol(self, name, module, klass):
        request = {"type": "load_protocol",
                   "name": name,
                   "module": module,
                   "class": klass}
        reply = {}
        self._send(request, reply)

        result = reply["result"]
        if not result:
            raise Exception(reply["message"])
        return

    def create_engine(self, name):
        request = {'type': 'create_engine', 'name': name}
        reply = {}
        self._send(request, reply)

        result = reply["result"]
        if not result:
            raise Exception(reply["message"])
        return

    def delete_engine(self, name):
        request = {"type": "delete_engine", "name": name}
        reply = {}
        self._send(request, reply)

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

    server = api.create_server("s1")
    server.load_protocol("fix", "fix_protocol", "FixProtocol")

    engine = server.create_engine("e1")
    #ep1 = engine.create_endpoint("ep1", 10102)
    #ep1.set_endpoint_protocol("fix")

    # api.accept_session("ep1", "s1")
    # api.get_session_message("s1", "m1")
    # api.process_message("e1", "m1", "m2")
    # api.send_session_message("s1", "m2")

    # api.set_endpoint_property("ep1", "auto_accept", "true")

    # api.set_engine_property("e1", "auto_receive", "true")
    # api.set_endpoint_property("ep1", "auto_receive", "true")
    # api.set_session_property("s1", "auto_receive", "true")



    server.delete_engine("e1")
    api.delete_server("s1")

