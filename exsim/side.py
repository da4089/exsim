# -*- coding: utf-8 -*-
########################################################################
# exsim - Exchange Simulator
# Copyright (C) 2016-2023, zeroXone.
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
