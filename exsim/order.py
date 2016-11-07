#! /usr/bin/env python

class Order(object):

    def __init__(self):
        self.symbol = ''
        self.order_type = 0  # market, limit, etc
        self.time_in_force = 0  # IOC, Day, GTD, GTC, FOK, FAK, OCO, etc, etc
        self.quantity = 0
        return


class LimitOrder(Order):

    def __init__(self):
        super(LimitOrder, self).__init__()
        self.limit_price = 0
        return


class MarketOrder(Order):

    def __init__(self):
        super(MarketOrder, self).__init__()
        return
