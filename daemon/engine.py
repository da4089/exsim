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


class Side:

    # FIXME: Need to deal with non-uniform books here: volume tiers, etc.

    def __init__(self):
        self.orders = []



class Engine:
    def handle_new_order(self):
        """Handle a received new order."""
        pass

    def handle_modify_order(self):
        """Handle a received order modify."""
        pass

    def handle_cancel_order(self):
        """Handle a received order cancel."""
        pass

    def handle_end_of_day(self):
        """Hnadle the end-of-day event."""
        pass

    def handle_shutdown(self):
        """Handle request to shut down the engine."""
        pass

    def handle_reset(self):
        """Reset the engine."""
        pass



class DefaultEngine(Engine):
    """Standard CLOB matching engine."""

    def handle_new_order(self):
        """Handle a received new order."""
        pass

    def handle_modify_order(self):
        """Handle a received order modify."""
        pass

    def handle_cancel_order(self):
        """Handle a received order cancel."""
        pass

    def handle_end_of_day(self):
        """Hnadle the end-of-day event."""
        pass

    def handle_shutdown(self):
        """Handle request to shut down the engine."""
        pass

    def handle_reset(self):
        """Reset the engine."""
        pass


class RejectEngine(Engine):
    """Engine that will automatically reject all received orders immediately."""
    pass


class CancelEngine(Engine):
    """Engine that will automatically cancel orders after a short time."""
    pass


class PartialThenCancelEngine(Engine):
    """Send a partial fill, and then cancel the remainder."""
    pass
