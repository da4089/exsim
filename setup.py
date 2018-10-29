#! /usr/bin/env python
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

from setuptools import setup


with open("README.rst") as readme:
    long_description = readme.read()

setup(name="exsim",
      version="0.0.1",
      description="Simple exchange simulator",
      long_description=long_description,
      url="https://github.com/da4089/exsim",
      author="David Arnold",
      author_email="d+exsim@0x1.org",
      license="GPLv3",
      packages=["exsim"],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Environment :: No Input/Output (Daemon)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
      )


########################################################################
