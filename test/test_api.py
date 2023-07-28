# -*- coding: utf-8 -*-
########################################################################
# exsim - Exchange Simulator
# Copyright (C) 2022-2023, zeroXone.
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

import pytest

import exsim
import exsim.api


def test_api_construct_destruct():
    api = exsim.api.API()
    api.delete()


def test_api_server():
    api = exsim.api.API()
    api.create_server('s1')
    api.delete_server('s1')
