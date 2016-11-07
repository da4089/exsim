#! /usr/bin/env python

class Side:
    """A single-side of a book for a market for a tradable thing."""

    BUY = 1
    SELL = 2

    def __init__(self):
        self.symbol = ''
        self.side = None
        self.orders = []
        return

    def add_order(self, order):
        return

    def modify_order(self, order):
        return

    def cancel_order(self, order):
        return

    def cancel_all_orders(self):
        return
