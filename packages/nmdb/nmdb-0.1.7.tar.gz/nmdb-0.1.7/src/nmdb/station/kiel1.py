#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIEL1 (IZMIRAN) data format

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

This module offers functions to read NM data in BIN format as used in KIEL.

KIEL BIN data availability:
1994-08-01 -- 2017-05-16
"""

__author__ = "Christian T. Steigies <steigies@physik.uni-kiel.de>"
__license__ = "GPL License"

#from datetime import datetime, date, time
#from calendar import monthrange
# http://wiki.python.org/moin/ConfigParserExamples
import configparser  # python-configparser
import pandas as pd
import os
#import MySQLdb  # python-mysqldb abstracted by sqlalchemy
from sqlalchemy import create_engine
import sqlite3

#from nmdb.tools.configtool import config_section_map
#from tools.query import dt_start_stopp

my_station = ["kiel1"]
my_names = {"kiel1": "KIEL1"}
my_station_longnames = {"kiel1": "Kiel (IZMIRAN)"}
pressure = {"kiel1": [900., 1200.]}
countrate = {"kiel1": [10., 1000.]}
