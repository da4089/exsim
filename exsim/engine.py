#! /usr/bin/env python

from exsim.message import *

class Engine(object):

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


    def handle_new_order(self, message):
        return

    def handle_modify_order(self, message):
        return

    def handle_cancel_order(self, message):
        return


    def publish_message(self, message):
        return
