#! /usr/bin/python

import logging
import select
import socket

from fix_protocol import FixParser, FixMessage

logging.basicConfig(level=logging.DEBUG)


class Session(object):

    def __init__(self, sock, addr):
        self._socket = sock
        self._address = addr
        self._parser = FixParser()
        self._gateway = None
        return

    def set_gateway(self, gateway):
        self._gateway = gateway
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
            self._gateway.session_closed(self)
            return

        self._parser.append_buffer(data)

        while True:
            fix_msg = self._parser.get_message()
            if not fix_msg:
                logging.debug("buf = [%s], length = %d" % (self._parser.buf, len(self._parser.buf)))
                break

            logging.debug("FIX pairs = %s" % str(fix_msg.pairs))

            t = fix_msg.message_type
            if t == "D":
                msg = self.handle_new_order(fix_msg)

            elif t == '0':
                self.handle_heartbeat(fix_msg)

            elif t == 'A':
                self.handle_logon(fix_msg)

            elif t == '5':
                self.handle_logout(fix_msg)

            else:
                logging.warning("Unhandled message: %s" % str(fix_msg))

        return


    def handle_new_order(self, fix_msg):
        return

    def handle_heartbeat(self, fix_msg):
        return

    def handle_logon(self, fix_msg):
        logging.info("Logon")
        return

    def handle_logout(self, fix_msg):
        return

    def send_message(self, message):
        self._socket.send(message)
        return


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


class Gateway(object):

    def __init__(self):
        self._engine = None
        self._comp_id = ''
        self._sessions = {}  #  socket: session
        self._endpoints = {}  # socket: endpoint
        self._is_running = True
        return

    def set_engine(self, engine):
        self._engine = engine
        return

    def listen(self, port):
        e = Endpoint()
        sock = e.listen(port)
        self._endpoints[sock] = e
        return

    def authenticate(self, username, password, source_addreess):
        return

    def create_session(self, sock):
        client_sock, client_addr = sock.accept()
        session = Session(client_sock, client_addr)
        self._sessions[client_sock] = session
        session.set_gateway(self)

        logging.info("New session %d from %s" % (session.socket().fileno(), str(client_addr)))
        return

    def session_closed(self, session):
        del self._sessions[session.socket()]
        logging.info("Closed %d" % session.socket().fileno())
        session.close()
        return

    def get_sessions(self):
        return reduce(lambda l, x: l.append(x.socket()) or l, self._sessions.values(), [])

    def get_endpoints(self):
        return reduce(lambda l, e: l.append(e.socket()) or l, self._endpoints.values(), [])

    def run(self):

        while self._is_running:
            # Wait 200ms for something to happen on a socket.
            sessions = self.get_sessions()
            endpoints = self.get_endpoints()

            r, w, x = select.select(sessions + endpoints, [], [], 0.2)

            for s in r:
                if s in self._endpoints:
                    self.create_session(s)
                else:
                    msg = self._sessions[s].readable()


        return
