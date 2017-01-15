#! /usr/bin/env python

class Protocol(object):
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
