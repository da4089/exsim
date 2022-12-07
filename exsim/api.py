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
import typing


logging.basicConfig(level=logging.DEBUG)


class API:
    """Exchange Simulator Client API."""

    def __init__(self):
        """Constructor."""
        self._buffer = b''
        self._servers = {}
        self._connected = False
        return

    def delete(self):
        """Clean up this API instance."""
        for server_proxy in self._servers:
            server_proxy.delete()
        self._servers = {}
        self._buffer = b''
        return

    def create_server(self, name: str = 'default'):
        """Create an Exchange Simulator server instance.

        :param name: String name to identify this server

        Normally, only one server instance is required, but when that's
        not the case, the name is used to distinguish them."""

        # Create pipe to receive TCP port number from child.
        from_api_fd, to_api_fd = os.pipe()

        # Fork server process off API.
        pid = os.fork()
        if pid == 0:
            # Child (server)

            # Make child process more daemon-like.
            from_devnull = open("/dev/null", "r")
            to_devnull = open("/dev/null", "w")

            sys.stderr.close()
            sys.stdout.close()
            sys.stdin.close()

            sys.stdin = from_devnull
            sys.stdout = to_devnull
            sys.stderr = to_devnull

            # Create main Server instance (not the API wrapper).
            sim_server = exsim.Server()

            # Return control port number to parent process.
            port = sim_server.get_port()
            os.close(from_api_fd)
            to_api = os.fdopen(to_api_fd, 'w')
            to_api.write(str(port))
            to_api.flush()
            to_api.close()

            # Enter server mainloop.
            sim_server.run()

            # Exit server process.
            sys.exit(0)

        # Wait to receive server's control port number.
        os.close(to_api_fd)
        from_api = os.fdopen(from_api_fd)
        s = from_api.read(10)
        port = int(s)
        from_api.close()

        # Connect to server.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', port))
        self._connected = True
        logging.info("Connected")

        # Create server proxy class in API.
        server_proxy = Server(self, name, sock, pid)
        self._servers[name] = server_proxy
        return server_proxy

    def delete_server(self, name):
        server_proxy = self._servers.get(name, None)
        if not server_proxy:
            raise KeyError("No such server: %s" % name)
        server_proxy.delete()
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


class Server:
    """Proxy for external exchange simulator server process."""
    def __init__(self, api: API, name: str, sock: socket.socket, pid: int):
        """Constructor.

        :param api: Reference to owning API.
        :param name: String name to identify this server
        :param sock: Management socket connected to server
        :param pid: Process identifier for simulator process."""
        self._api = api
        self._name = name
        self._socket = sock
        self._child_pid = pid

        self._buffer = b''
        return

    def delete(self):
        """Destroy this proxy wrapper, and its managed server process."""
        os.kill(self._child_pid, signal.SIGINT)
        pid, status = os.waitpid(self._child_pid, 0)
        # FIXME: need to have a SIGKILL after a bit here?
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

    def create_engine(self, name: str):
        """Request server to create a new simulated matching engine.

        :param name: String name to identify the matching engine."""
        request = {'type': 'create_engine', 'name': name}
        reply = {}
        self._send(request, reply)

        result = reply["result"]
        if not result:
            raise Exception(reply["message"])

        return Engine(self, name)

    def delete_engine(self, name):
        """Request server to delete a simulated matching engine.

        :param name: String name to identify the matching engine."""
        request = {"type": "delete_engine", "name": name}
        reply = {}
        self._send(request, reply)

        result = reply["result"]
        if not result:
            raise Exception(reply["message"])
        return

    def _send(self, request, reply):
        """(Internal) Make RPC to server process.

        :param request: Request dictionary.
        :param reply: Empty dictionary to be populated with reply message."""

        # Send request.
        body = pickle.dumps(request)
        header = struct.pack("<L", len(body))
        self._socket.sendall(header + body)
        logging.debug(f"Sent request to server {self._name}")

        # Wait for reply.
        while True:
            data = self._socket.recv(8192)
            logging.debug(f"Received {len(data)} bytes "
                          f"from server '{self._name}'")
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


class Engine:
    def __init__(self, server: Server, name: str):
        """Constructor.

        :param server: Reference to owning server
        :param name: String name to identify this engine"""
        self.server = server
        self.name = name

        self.endpoints: typing.Dict[str, Endpoint] = {}
        return

    def create_endpoint(self, name: str):
        """Create an endpoint on this engine.

        :param name: String name to identify this endpoint"""
        ep = Endpoint(name)
        self.endpoints[name] = ep
        return ep


class Endpoint:
    def __init__(self, name):
        self.name = name
        return


class Session:
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

