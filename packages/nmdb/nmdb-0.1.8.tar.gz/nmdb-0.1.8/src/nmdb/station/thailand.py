#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thailand data format

Copyright (c) 2011-2024 Christian T. Steigies <steigies@physik.uni-kiel.de>

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

# online = False  # read data from local disk
online = True  # read data from webserver

# --------------------------------------------------------------------------
# import MySQLdb # python-mysqldb

import os
from datetime import date #, datetime, time
#import numpy as np
import pandas as pd

#from nmdb3.station.station_data import check_data, check_pressure
from nmdb.tools.datetool import date2doy, valid_date #parse_date, doy2date, idate
#from nmdb3.tools.pressure import mbar

# __all__ = ["", ""]

# --------------------------------------------------------------------------

thailand_station = ["psnm"]
thailand_longnames = {"psnm": "Thailand"}
DATA_PATH = '~/data/thailand'


# --------------------------------------------------------------------------
def read_rt(options, station, data_type, year, month, day):
    """read realtime data

    options     verbose, dryrun, ...
    station     station short name, must be valid station
    data_type   "1m", "1h", "env", "meta"
    year        integer (1950-9999), may not be None
    month       integer (1-12), if None, read month 1-12
    day         integer (1-31), if None, read day 1-31
    
    return dataframe (was: list of values in nmdb format)
    """

    if station in thailand_station:
        pass
    else:
        raise ValueError  # wrong station

    if data_type in ["1h"]:  # PSNM provides only 1h data
        if month is None:
            raise ValueError  # read full year from Archive instead!
            #df = [ read_rt(options, station, data_type, year, m, None) for m in range(1, 12+1) ]
            #try:
            #    data = pd.concat(df)
            #except ValueError:  # All objects passed were None
            #    data = None
        elif day is None:  # read all days recursively
            df = [ read_rt(options, station, data_type, year, month, d) for d in range(1, 31+1) ]
            try:
                data = pd.concat(df)
            except ValueError:  # All objects passed were None
                data = None
        else:
            data = read_pandas(options, data_type, year, month, day)

    elif data_type in ["1m", "env", "meta"]:
        raise ValueError  # reading this data_type is not yet implemented
    else:
        raise ValueError  # illegal data_type

    return(data)


# --------------------------------------------------------------------------
def read_rev(options, station, data_type, year, month, day):
    """read revised data

    options     verbose, dryrun, ...
    station     station short name, must be valid station
    data_type   "1m", "1h", "env", "meta"
    year        integer (1950-9999), may not be None
    month       integer (1-12), if None, read month 1-12
    day         integer (1-31), if None, read day 1-31

    return list of values in nmdb format
    """

    if station in thailand_station:
        pass
    else:
        raise ValueError  # wrong station

    if options.verbose:
        print(year, type(year), month, type(month), day, type(day))
    if data_type in ["1h"]:
        data = read_pandas_arc(options, data_type, year)
    elif data_type in ["1m", "env", "meta"]:
        raise ValueError  # reading this data_type is not yet implemented
    else:
        raise ValueError  # illegal data_type

    return data

# --------------------------------------------------------------------------
def read_pandas_arc(options, data_type, year):
    """A line containing 42 asterisks occurs immediately preceding
       and following the data, and nowhere else in this file.
       Software can use this line to seek past this header material.
       YYYY DOY HHMM    Corr  Uncorr  Press
       ******************************************
       2015   1 0030 2152069 2128672 564.28

    return dataframe (was: list of values in nmdb format)
    """
    import urllib.request, urllib.error, urllib.parse

    pattern = "*"*42

    if online:  # read directly from WWW server
        wwwserver = "http://astro.phys.sc.chula.ac.th/NMdata_files/Archival"
    else:  # read from local copy
        wwwserver = os.path.expanduser(DATA_PATH)
    filename = "%s/Archive_%04i_latest.txt" % (wwwserver, year)
    if options.verbose:
        print("reading", filename)

    if online:
        myfile = urllib.request.urlopen(filename)
    else:
        myfile = open(filename, "r")

    found = []  # find start and stopp lines of data
    for i, line in enumerate(myfile):
        if online:  # urllib returns 'str', not a bytes-like object
            line = line.decode('utf-8')
        #print(i, line)
        if pattern in line:
            found.append(i)
    if len(found) != 2:
        raise ValueError  # pattern must be found exactly twice
    [start, stopp] = found  # we only use start. stopp should be the last line
    if options.verbose > 1:
        print(start, stopp)

    try:
        df = pd.read_csv(filename, sep=" ", engine="python",
                     #error_bad_lines = False,
                     names=["year", "doy", "time", "cor", "uncor", "p"],
                     skipinitialspace=True, # extra space for DOY?
                     skiprows=start-1, skipfooter=1
                     )
    except:
        return(None)

    # create index and data columns in NMDB format
    df.index = pd.to_datetime(df['year'] * 10000000 + df['doy'] * 10000
                    + df['time'] , format='%Y%j%H%M')
    df['u'] = df['uncor'].astype(float)/3600.
    df['c'] = df['cor'].astype(float)/3600.

    # drop unused columns
    df.drop(["year", "doy", "time", "cor", "uncor"], axis=1, inplace=True)

    return(df)


# --------------------------------------------------------------------------
def read_pandas(options, data_type, year, month, day):
    """
    realtime / 1h
    """

    if not(valid_date(year, month, day)):
        return(None)
    doy = date2doy(date(year, month, day))

    if online:  # read directly from WWW server
        wwwserver = "http://cosmic.sc.mahidol.ac.th/~psnm/nmdb"
    else:  # read from local copy
        wwwserver = os.path.expanduser(DATA_PATH)
    filename = "%s/%i/PSNM-%04i.%i.txt" % (wwwserver, year, year, doy)
    if options.verbose:
        print("reading", filename)
    try:
        df = pd.read_csv(filename, sep=" ")
    except: # HTTPError is undefined?
        return(None)

    df.index = pd.to_datetime(df['YYYY-MM-DD'] + " " + df['HH:MM:SS'])
    df['interval'] = 3600.
    df['p'] = df['Press'].astype(float)
    df['u'] = df['NMUncor'].astype(float)/3600.
    df['c'] = df['NMPCor'].astype(float)/3600.
    df['e'] = df['NMEffCor'].astype(float)/3600.

    # drop unnamed column
    df = df.drop(df.columns[[6]], axis=1)
    # drop remaining columns by name
    df.drop(['YYYY-MM-DD', 'HH:MM:SS', 'Press', 'NMUncor', 'NMPCor', 'NMEffCor'],
            axis=1, inplace=True)

    return(df)

# --------------------------------------------------------------------------
def main():

    import optparse
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("-v", dest="verbose", default=0, action="count",
            help="increment output verbosity; may be specified multiple times")

    (options, args) = parser.parse_args()

    print("This is the thailand module.")

    station = "psnm"
    data_type = "1h"  # 1h data only for PSNM
    #year = 2022
    year = 2019
    month = 4
    #day = 7
    day = None

    # real-time data is no longer available?
    #data = read_rt(options, station, data_type, year, month, day)
    data = read_rev(options, station, data_type, year, month, day)  # reads whole year
    #data = read_pandas_arc(options, data_type, year)

    # need to convert dataframe data to list for use with upload/revise?
    return(data)


# --------------------------------------------------------------------------
if __name__ == '__main__':
    data = main()
    print(data)
    #data.plot(y=["p", "c", "u"])
