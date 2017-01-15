#! /usr/bin/env python

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
