# -*- coding: utf-8 -*-
########################################################################
# exsim - Exchange Simulator
# Copyright (C) 2016-2018, ZeroXOne.
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

import datetime
import simplefix
import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 10102))

    p = simplefix.FixParser()

    # Logon
    m = simplefix.FixMessage()
    m.append_pair(8, "FIX.4.2")
    m.append_pair(35, "A")
    m.append_pair(49, "CLIENT")
    m.append_pair(56, "SERVER")
    m.append_pair(52, datetime.datetime.utcnow().isoformat('-')[:-3])
    m.append_pair(98, 0) # No encrytion
    m.append_pair(108, 30)

    s.sendall(m.encode())

    while True:
        data = s.recv(8192)
        p.append_buffer(data)
        r = p.get_message()
        if r:
            break

    print m.encode().replace(simplefix.SOH, "|")


if __name__ == "__main__":
    main()
