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

# One or more Protocol modules are associated with a Session.  Incoming
# bytes are passed to the protocol modules for decoding, resulting in
# calls to the matching engine.  Events on the matching engine will
# trigger a callback to the protocol, which can in turn send a message
# via the associated Session.
#
# The standard matching engine supports three protocol types: market
# data, order entry, and drop copy.  A given protocol implementation
# can support one or more of these roles.


class Protocol:
    """A protocol module."""

    def __init__(self, session):
        self.session = session
        return

    def receive(self, buf):
        """Process a byte buffer received from the session."""
        return

    def send(self, message):
        """Encode this message, and send it via the session."""

        # The message is represented as a Python dictionary.  The type
        # of message is in the 'type' field; the remainder of the
        # fields depend of what type it is.
        #
        # Protocols might ignore some fields when encoding: the
        # information from the matching should be a superset of what
        # any protocol might require.
        #
        # So: switch on type to message-specific encoding functions.
        # If there's no translation, ignore the message.  Otherwise
        # pass it to the Session to be sent.

        message_type = message.get("type", None)
        if not message_type:
            return

        if message_type == "login_ack":
            self.send_login_ack(message)

        elif message_type == "order_ack":
            self.send_order_ack(message)

        elif message_type == "order_reject":
            self.send_order_reject(message)

        elif message_type == "order_cancelled":
            self.send_order_cancelled(message)

        elif message_type == "order_executed":
            self.send_order_executed(message)

        elif message_type == "cancel_ack":
            self.send_cancel_ack(message)

        elif message_type == "replace_ack":
            self.send_replace_ack(message)

        else:
            logging.warning("Unhandled message type: '%s'" % message_type)

        return
