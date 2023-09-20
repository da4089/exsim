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

# Model classes for most of the system entities
# Model state updates send requests to daemon
# Daemon responses update model state
# - Maybe with a dummy loopback for initial testing?


class BaseModel:
    def __init__(self):
        pass


class VenueModel(BaseModel):
    def __init__(self):
        self.name = ""
        self.endpoints = {}


class EndpointModel(BaseModel):
    def __init__(self):
        self.name = ""
        self.sessions = {}


class SessionModel(BaseModel):
    def __init__(self):
        self.active: bool = False


class FixSessionModel(SessionModel):
    def __init__(self):
        super().__init__()
        self.begin_string = ""
        self.sender_comp_id = ""
        self.target_comp_id = ""

    def get_description(self):
        return f"FIX: {self.begin_string}={self.sender_comp_id}-{self.target_comp_id}"


class InstrumentModel(BaseModel):
    def __init__(self):
        self.symbol = ""
        self.book = None


class BookModel(BaseModel):
    def __init__(self):
        self.bids = None
        self.offers = None
