#! /usr/bin/env python
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

# This program can run either as a standalone daemon, or as a local child
# process for a GUI or API manager.
#
# In the standalone case, it should run as a Unix daemon, with either
# traditional or systemd-style behaviour (ie. optional daemonisation),
# or as a Windows Service.
#
# I will need to investigate how a Windows Service works with
# PyInstaller -- it *should* be ok, given that distinct executable?
#
# So, some flags:
# -h for help
# -v for version info
# -d for debug (log to console, don't detach)
# -s for systemd behaviour?
# -p for management port number
# -i for IP of interface to listen on (can be multiple)



def main():
    pass


if __name__ == "__main__":
    main()
