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

LOGIN_REQUEST_MESSAGE = "login_req"
LOGIN_ACCEPTED_MESSAGE = "login_ack"
LOGIN_REJECTED_MESSAGE = "login_rej"
LOGOUT_REQUEST_MESSAGE = "logout_req"
LOGGED_OUT_MESSAGE = "logged_out"

NEW_ORDER_MESSAGE = "new"
MODIFY_ORDER_MESSAGE = "mod"
CANCEL_ORDER_MESSAGE = "cxl"
ORDER_ACCEPTED_MESSAGE = "ack"
ORDER_REJECTED_MESSAGE = "rej"
MODIFY_ACCEPTED_MESSAGE = "mod_ack"
MODIFY_REJECTED_MESSAGE = "mod_rej"
CANCEL_ACCEPTED_MESSAGE = "cxl_ack"
CANCEL_REJECTED_MESSAGE = "cxl_rej"
CANCEL_ALL_MESSAGE = "cxl_all"
EXECUTION_MESSAGE = "exec"

SYMBOL_STATUS_MESSAGE = "symbol"
MARKET_STATUS_MESSAGE = "market"

ORDER_ADDED_MESSAGE = "added"
ORDER_MODIFIED_MESSAGE = "modified"
ORDER_CANCELED_MESSAGE = "canceled"
ORDER_EXECUTED_MESSAGE = "executed"
TRADE_EXECUTED_MESSAGE = "traded"

CREATE_ENGINE_MESSAGE = "create_engine"
DELETE_ENGINE_MESSAGE = "delete_engine"
SET_ENGINE_PROPERTY_MESSAGE = "set_engine_property"
START_ENGINE_MESSAGE = "start_engine"
STOP_ENGINE_MESSAGE = "stop_engine"

CREATE_ENDPOINT_MESSAGE = "create_endpoint"
DELETE_ENDPOINT_MESSAGE = "delete_endpoint"
SET_ENDPOINT_PROPERTY_MESSAGE = "set_endpoint_property"


class Message:
    def __init__(self, msg_type: str=None):
        self.type = msg_type
        return


class LoginRequestMessage(Message):
    def __init__(self):
        super().__init__(LOGIN_REQUEST_MESSAGE)
        self.username = ''
        self.password = ''
        return


class LoginAcceptedMessage(Message):
    def __init__(self):
        super().__init__(LOGIN_ACCEPTED_MESSAGE)
        return


class NewOrderMessage(Message):
    def __init__(self):
        super().__init__(NEW_ORDER_MESSAGE)
        self.symbol = ''
        self.order_type = ''
        self.quantity = 0
        self.price = 0
        return


class CreateEngineMessage(Message):
    def __init__(self):
        super().__init__(CREATE_ENGINE_MESSAGE)
        self.name = ''
        return


class DeleteEngineMessage(Message):
    def __init__(self):
        super().__init__(DELETE_ENGINE_MESSAGE)
        self.name = ''
        return


class SetEnginePropertyMessage(Message):
    def __init__(self):
        super().__init__(SET_ENGINE_PROPERTY_MESSAGE)
        self.engine = ''
        self.name = ''
        self.value = None
        return


class StartEngineMessage(Message):
    def __init__(self):
        super().__init__(START_ENGINE_MESSAGE)
        self.engine = ''
        return


class StopEngineMessage(Message):
    def __init__(self):
        super().__init__(STOP_ENGINE_MESSAGE)
        self.engine = ''
        return
