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
