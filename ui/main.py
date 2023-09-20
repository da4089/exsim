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

import exsim
import logging


# PyQt5 GUI
# - connect to or start daemon
# - CRUD instruments, endpoints, bots, venues, etc
# - look at books

# Start with venues (and one of them)
# Configure the engine and endpoints for the venue
# Add instruments to the venue
# Configure instruments with bots, etc
# View order books
# Manually fill orders


# Model classes for most of the system entities
# Model state updates send requests to daemon
# Daemon responses update model state
# - Maybe with a dummy loopback for initial testing?
