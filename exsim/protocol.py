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
        return
