#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""mysql helper functions

Copyright (C) 2012-2019 Christian T. Steigies <steigies@physik.uni-kiel.de>

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
"""

__author__ = "Christian T. Steigies <steigies@physik.uni-kiel.de>"
__license__ = "GPL License"

from datetime import datetime
#from nmdb3.nmdb.mysql_query import query, query_1h
from nmdb.mysql.nmdb_format import hour_format, ori_format, rev_format, meta_format, env_format
from nmdb.station.station_name import station_name

## --------------------------------------------------------------------------
def query(name, version, mode):
    if mode in ["ori", "1m"]:
        value = query_1m(name, version)
    elif mode in ["1h"]:
        value = query_1h(name, version)
    else:
        raise ValueError  # illegal mode

    return value
## --------------------------------------------------------------------------

def query_1h(name, version):
    """
    create write query for 1h data
    use REPLACE only when version == 1
    TODO rename to insert_1h?
    """

    station = station_name(name)  # kiel3 is stored as kiel2
    # print("writing to table: "+ station)

    if version == 0:  # initial write
        value = ("INSERT INTO %s_1h (%s)") % (station.upper(), hour_format)

    elif version == 1:  # overwrite
        value = ("REPLACE INTO %s_1h (%s)") % (station.upper(), hour_format)

    else:
        print(station, version)
        raise ValueError  # illegal version number

    return value


## --------------------------------------------------------------------------
def query_1m(name, version):
    """
    create write query for ori, rev, based on version number
    TODO rename to insert_revori?
    """

    station = station_name(name)  # kiel3 is stored as kiel2
    # print("writing to table: "+ station)

    if version == 0:  # version = "ori"
        value = ("INSERT INTO %s_ori (%s)") % (station.upper(), ori_format)

    elif  version == 1:  # rev version 1
        value = ("INSERT INTO %s_rev (%s)") % (station.upper(), rev_format)

    elif version > 1:  # rev version 2 or higher
        value = ("REPLACE INTO %s_rev (%s)") % (station.upper(), rev_format)

    else:
        raise ValueError  # illegal version number

    return value



## --------------------------------------------------------------------------
def write_nmdb(options, cursor, write):
    """write to NMDB"""

    value = 1

    if options.dryrun:  # dryrun counts as if data was written
        print(write)
    else:  # write data
        if options.verbose > 0:
            print(write)
        cursor.execute(write)
        answer = cursor.fetchone()
        if answer is not None:
            print(answer)

    return value


## --------------------------------------------------------------------------
def BUG_flush_nmdb(options, cursor, name, data_type, data, version):
    """INSERT or REPLACE 1h values"""

    # BUG mixup query and query_1h?
    if data_type in ["1m", "ori", "rev"]:
        write = query_1h(name, version)  # INSERT or REPLACE
    elif data_type in ["1h"]:
        write = query(name, version)  # INSERT or REPLACE, ori or rev
    else:
        raise ValueError  # wrong data_type

    if len(data) == 0:
        value = 0
    else:
        write += " VALUES " + mysql_values(data)
        value = write_nmdb(options, cursor, write)

    return value


## --------------------------------------------------------------------------
def mysql_values(data):
    """
    executemany uses many INSERTS with only one VALUE,
    instead of one INSERT with many VALUES
    see https://answers.launchpad.net/myconnpy/+question/120598
    until this is fixed, use execute instead of executemany
    and prepare the VALUES with this helper function
    """

    ret = ""
    delimiter = ""
    for row in data:
        ret += delimiter + mysql_row(row)
        if delimiter == "":
            delimiter = ", "

    return ret

## --------------------------------------------------------------------------
def mysql_row(row):
    """for one dataset, convert all values to strings and None to NULL"""

    ret = "("
    delimiter = ""
    for val in row:
        if val is None:
            val = "NULL"
        elif isinstance(val, str):
            val = "\"" + str(val) + "\""
        elif isinstance(val, datetime):
            val = "\"" + str(val) + "\""
        else:
            val = str(val)
        ret += delimiter + val
        if not delimiter:
            delimiter = ", "
    ret += ")"

    return ret

## --------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is the mysql module.")

    data = [('2013-07-18 21:15:00', 60, 92.51, None, 90.68, 1010.519, 2), ('2013-07-18 21:17:00', 60, 93.37, None, 91.5, 1010.506, 2), ('2013-07-18 21:19:00', 60, 94.91, None, 93.02, 1010.519, 2), ('2013-07-18 21:22:00', 60, 91.99, None, 90.16, 1010.519, 2), ('2013-07-18 21:24:00', 60, 92.16, None, 90.3, 1010.479, 2), ('2013-07-18 21:25:00', 60, 92.47, None, 90.57, 1010.426, 2), ('2013-07-18 21:26:00', 60, 93.54, None, 91.61, 1010.413, 2), ('2013-07-18 21:27:00', 60, 92.38, None, 90.46, 1010.399, 2), ('2013-07-18 21:36:00', 60, 92.14, None, 90.22, 1010.386, 2), ('2013-07-18 21:38:00', 60, 97.11, None, 95.07, 1010.359, 2), ('2013-07-18 21:39:00', 60, 92.75, None, 90.79, 1010.346, 2), ('2013-07-18 21:40:00', 60, 95.68, None, 93.66, 1010.346, 2)]

    print(mysql_values(data))
