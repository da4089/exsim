# -*- coding: utf-8 -*-
########################################################################
# exsim - Exchange Simulator
# Copyright (C) 2023, zeroXone.
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


class Order:
    def __init__(self):

        self.symbol = ''
        self.suffix = ''
        self.maturity_year = 0
        self.maturity_month = 0
        self.maturity_day = 0
        self.put_or_call = None
        self.asset_class = None
        self.series = 0

        self.order_type = ''
        self.tif = ''
        self.side = ''

        self.order_quantity = 0
        self.min_quantity = 0  # FIXME: ???
        self.remaining_quantity = 0

        self.price = 0
        self.stop_price = 0
