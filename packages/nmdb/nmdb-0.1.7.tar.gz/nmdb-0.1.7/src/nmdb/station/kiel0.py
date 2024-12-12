#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIEL0 (IGY and NM64 before IZMIRAN) data format

Copyright (c) 2009-2024 Christian T. Steigies <steigies@physik.uni-kiel.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

This module offers functions to read NM data in ASCII format as used in KIEL.

KIEL data availability
1h data since:
1957-07-01 C and O data only, no U or P data
1964-09-01 C, O, U and P data

1min data since:
TODO (early data is actually in 5min resolution?)
1971-02-01 C, O and P data
"""

__author__ = "Christian T. Steigies <steigies@physik.uni-kiel.de>"
__license__ = "GPL License"

import pandas as pd

my_station = ["kiel0"]
my_names = {"kiel0": "KIEL0"}
my_station_longnames = {"kiel0": "Kiel (IGY and NM64)"}
pressure = {"kiel0": [900., 1200.]}
countrate = {"kiel0": [10., 1000.]}
