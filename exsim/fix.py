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

import datetime
import logging
import select
import socket
import time

from fix_protocol import FixParser, FixMessage, print_fix

logging.basicConfig(level=logging.DEBUG)



class Session(object):

    def __init__(self, sock, addr):
        self._socket = sock
        self._address = addr
        self._parser = FixParser()
        self._gateway = None

        # Next expected sequence number.
        self._in_seq = 1

        # Sequence number to be used for next sent message.
        self._out_seq = 1

        # Interval before sending TestRequest or Heartbeat messages.
        self._heartbeat_interval = 30 * 1000

        # Outstanding test request identifiers.
        self._test_requests = {}
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

            elif t == '1':
                self.handle_test_request(fix_msg)

            elif t == 'A':
                self.handle_logon(fix_msg)

            elif t == '5':
                self.handle_logout(fix_msg)

            else:
                logging.warning("Unhandled message: %s" % str(fix_msg))

        return


    def handle_new_order(self, fix_msg):
        return

    def handle_test_request(self, fix_msg):
        test_request_id = fix_msg.get(112)
        logging.debug("Received TestRequest, id = %s" % str(test_request_id))

        self.send_heartbeat(test_request_id)
        return

    def handle_heartbeat(self, fix_msg):
        return

    def handle_logon(self, fix_msg):
        # Check Sender and TargetCompID
        # Check username/password

        # Send response
        resp = FixMessage()
        resp.set_message_type('A')  # Logon
        resp.append_pair(34, self.next_seq())
        resp.append_pair(49, fix_msg.get(56))  # Sender
        resp.append_pair(56, fix_msg.get(49))  # Target
        resp.append_pair(52, self.get_fix_time())
        resp.append_pair(98, 0)  # No encryption
        resp.append_pair(108, fix_msg.get(108))  # Heartbeat interval
        s = resp.encode()

        print "Sending ",
        print_fix(s)

        self._socket.send(s)

        # Save CompIDs
        self._peer_compid = fix_msg.get(49)
        self._my_compid = fix_msg.get(56)

        # Save the heartbeat interval.
        try:
            self._heartbeat_interval = int(fix_msg.get(108)) * 1000
        except ValueError:
            pass

        # Register timeout for heartbeat.
        self._gateway.add_timeout(time.time() + self._heartbeat_interval, self.send_heartbeat)
        return

    def handle_logout(self, fix_msg):
        return

    def send_message(self, message):
        self._socket.send(message)
        return

    def send_heartbeat(self, test_request_id=None):
        msg = FixMessage()
        msg.set_message_type('0')  # Heartbeat
        msg.append_pair(34, self.next_seq())
        msg.append_pair(49, self._my_compid)
        msg.append_pair(56, self._peer_compid)
        msg.append_pair(52, self.get_fix_time())

        if test_request_id:
            msg.append_pair(112, test_request_id)

        self.send_message(msg.encode())

        logging.debug("Sent heartbeat")
        return

    def next_seq(self):
        seq = self._out_seq
        self._out_seq += 1
        return seq

    def get_fix_time(self):
        return datetime.datetime.utcnow().isoformat('-')[:-3]



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
        self._timeouts = []
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
            now = time.time()
            while True:
                if len(self._timeouts) == 0:
                    break

                expiry, callback = self._timeouts[0]
                if expiry > now:
                    break

                callback()
                self._timeouts.pop(0)

            if len(self._timeouts) > 0:
                wait = self._timeouts[0][0] - time.time()
                if wait < 0:
                    wait = 0
            else:
                wait = 1.0

            sessions = self.get_sessions()
            endpoints = self.get_endpoints()

            r, w, x = select.select(sessions + endpoints, [], [], wait)

            for s in r:
                if s in self._endpoints:
                    self.create_session(s)
                else:
                    msg = self._sessions[s].readable()
        return

    def add_timeout(self, expiry_time, callback):
        t = (expiry_time, callback)
        self._timeouts.append(t)
        self._timeouts.sort()
        return

    def delete_timeout(self, expiry_time, callback):
        t = (expiry_time, callback)
        self._timeouts.remove(t)
        return
