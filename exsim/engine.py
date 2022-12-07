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

from exsim.message import *


class Engine(object):
    """A matching engine."""

    def __init__(self, name: str):
        """Constructor.

        :param name: Matching engine name."""
        self.name = name
        self.markets = {}  # symbol: book

        self._clients = {}
        self._drops = {}
        self._prices = {}
        self._trades = {}


        return

    def delete(self):
        # Clean up.
        return

    def attach(self, name):
        """Connect a client session to this engine.

        This identifies a source of orders, and is used to select
        order flow for drop copy subscribers."""
        pass

    def subscribe_drops(self, names):
        """Request delivery of drop copies for named client sessions."""
        pass

    def subscribe_prices(self):
        """Request delivery of pricing.

        Depending on the engine type, this can be either quotes or
        limit order prices."""
        pass

    def subscribe_trades(self):
        """Request delivery of trade reports.

        This is not a drop copy, but rather the unattributed time and
        sales stream from the matching engine."""
        pass

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
