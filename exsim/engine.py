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

from .session import Session


class Engine:
    """Base class for engine implementation."""

    def __init__(self, name: str):
        """Constructor.

        :param name: String name for this engine."""
        self._name = name

        self._sessions = []
        return

    def attach_session(self, session: Session):
        """Attach a Session to this Engine."""

        self._sessions.append(session)
        return

    def detach_session(self, session: Session):
        """Detach a Session from this Engine."""
        self._sessions.remove(session)
        return
