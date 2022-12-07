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
import simplefix

from .protocol import Protocol


class FixProtocol(Protocol):
    """A basic FIX protocol module."""

    def __init__(self, session):
        super().__init__(session)

        # Reset protocol state.
        self.reset()
        return

    def reset(self):
        """Reset the parser state.

        Discards any received by unprocessed data."""

        # Parser.
        self._parser = simplefix.FixParser()

        # My CompID.
        self._my_comp_id = ""

        # Peer's CompID.
        self._peer_comp_id = ""

        # Next expected sequence number.
        self._in_seq = 1

        # Sequence number to be used for next sent message.
        self._out_seq = 1

        # Interval before sending TestRequest or Heartbeat messages.
        self._heartbeat_interval = 30 * 1000

        # Outstanding test request identifiers.
        self._test_requests = {}
        return

    def receive(self, buf):
        """Process a byte buffer received from the session."""
        return self._parser.append_buffer(buf)

    def get_message(self):
        fix_message =  self._parser.get_message()
        if not fix_message:
            #FIXME
            return

        t = fix_message.get(35)
        if not t:
            #FIXME
            return

        if t == "D":
            msg = self.receive_fix_new_order_single(fix_message)

        elif t == '0':
            self.receive_fix_heartbeat(fix_message)

        elif t == '1':
            self.receive_fix_test_request(fix_message)

        elif t == 'A':
             self.receive_fix_logon(fix_message)

        elif t == '5':
             self.receive_fix_logout(fix_message)

        else:
             logging.warning("Unhandled message: %s" % str(fix_message))

        return

    def receive_fix_logon(self, fix_message):
        # Save CompIDs
        # Set heartbeat interval
        return

    def receive_fix_logout(self, fix_message):
        return

    def receive_fix_heartbeat(self, fix_message):
        return

    def receive_fix_test_request(self, fix_message):
        test_request_id = fix_message.get(112)
        logging.info("Received FIX TestRequest, id = [%s]" % str(test_request_id))
        self.send_heartbeat(test_request_id)
        return

    def receive_fix_new_order_single(self, fix_message):
        return

    def receive_fix_cancel_request(self, fix_message):
        return

    def send_login_ack(self, message):

        # In FIX, login acknowledgement is sent with a Logon()
        # message.  In addtion to confirming authentication, it also
        # returns the agree heartbeat timeout period.

        fix = simplefix.FixMessage()
        fix.append_pair(35, "A")
        fix.append_pair(34, self.next_seq())
        fix.append_pair(49, self._my_comp_id)  # Sender
        fix.append_pair(56, self._peer_comp_id)  # Target
        fix.append_pair(52, self.get_fix_time())
        fix.append_pair(98, 0)  # No encryption
        fix.append_pair(108, self._heartbeat_interval)
        self._session.send(fix.encode())

        # FIXME: set timer for heartbeats.
        #self._gateway.add_timeout(time.time() + self._heartbeat_interval, self.send_heartbeat)

        logging.info("Sent FIX logon (login_ack)")
        return

    def send_order_ack(self, message):
        return

    def send_order_reject(self, message):
        return

    def send_order_cancelled(self, message):
        return

    def send_order_executed(self, message):
        return

    def send_cancel_ack(self, message):
        return

    def send_replace_ack(self, message):
        return

    def send_heartbeat(self, test_request_id = None):

        fix = simplefix.FixMessage()
        fix.set_message_type('0')  # Heartbeat
        fix.append_pair(34, self.next_seq())
        fix.append_pair(49, self._my_compid)
        fix.append_pair(56, self._peer_compid)
        fix.append_pair(52, self.get_fix_time())
        if test_request_id:
            fix.append_pair(112, test_request_id)

        self._session.send(fix.encode())
        logging.info("Sent FIX heartbeat" + " id = [%s]" % test_request_id if test_request_id else "")
        return

    def get_fix_time(self):
        return datetime.datetime.utcnow().isoformat('-')[:-3]

    def next_seq(self):
        seq = self._out_seq
        self._out_seq += 1
        return seq
