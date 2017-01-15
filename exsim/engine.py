#! /usr/bin/env python

from exsim.message import *

class Engine(object):
    """A matching engine."""

    def __init__(self, name):
        self.name = name
        self.markets = {}  # symbol: book
        return

    def delete(self):
        # Clean up.
        return

    def handle_trade_flow(self, message):

        if not hasattr(message, 'type'):
            self.log("Bad message:", str(message))
            return

        t = message.type
        if t == NEW_ORDER_MESSAGE:
            pass

        elif t == MODIFY_ORDER_MESSAGE:
            pass

        elif t == CANCEL_ORDER_MESSAGE:
            pass

        elif t == CANCEL_ALL_MESSAGE:
            pass

        else:
            self.log("Bad message type:", t)
            return


    def handle_login(self, message):
        return

    def handle_logout(self, message):
        return

    def handle_new_order(self, message):
        """Process new order."""
        return

    def handle_cancel_order(self, message):
        """Process attempt to cancel an open oerder."""
        return

    def handle_subscribe(self, message):
        """Process request for streaming prices."""
        return

    def handle_unsubscribe(self, message):
        """Process request to cancel streaming prices."""
        return

    def handle_quote(self, message):
        """Process new submitted quote."""
        return

    def handle_quote_delete(self, message):
        """Process withdrawal of a quote."""
        return



    def publish_message(self, message):
        return


    def send_login_ack(self, message):
        """Acknowledge successful login."""
        return

    def send_login_reject(self, message):
        """Acknowledge unsuccessful login."""
        return

    def send_quote_ack(self, message):
        """Acknowledge submitted quote."""
        return

    def send_quote_delete_ack(self, message):
        """Acknowledge deletion of quote."""
        return

    def send_subscribe_ack(self, message):
        """Acknowledge successful subscription."""
        return

    def send_subscribe_reject(self, message):
        """Acknowledge unsuccessful subscription."""
        return

    def send_market_data_update(self, message):
        """Publish new quote to subscribers."""
        return

    def send_order_ack(self, message):
        """Acknowledge new order."""
        return

    def send_order_cancelled(self, message):
        """Report cancellation of remaining order quantity."""
        return

    def send_order_execution(self, message):
        """Report execution of some order quantity."""
        return
