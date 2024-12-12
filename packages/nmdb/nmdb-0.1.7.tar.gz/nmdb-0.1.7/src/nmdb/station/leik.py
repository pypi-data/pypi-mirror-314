#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""read leik (LEIK) data into a pandas dataframe -- testing station

Copyright (c) 2023 Christian T. Steigies <steigies@physik.uni-kiel.de>

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

import pandas as pd

from datetime import datetime
from time import gmtime, strftime

# TODO use your station names here
stations = ["leik"]
#names = {"leik": "LEIK"}
station_longnames = {"leik": "Test Station"}




# --------------------------------------------------------------------------
def read_rt(options, station, data_type, year, month, day):
    """read realtime data for one day at a time

    options     verbose, dryrun, ...
    station     station short name, must be valid station
    data_type   "ori", "1h", "env", "meta"
    year        integer (1950-9999), may not be None
    month       integer (1-12), if None, read month 1-12
    day         integer (1-31), if None, read day 1-31

    return list of values in nmdb format, all countrates are counts/s
    [str2datetime(str(start_date_time)), # start of the measurement
     60,      # length of the measurement in seconds: 60 for 1min data
     uncorr,  # countrate of the whole monitor, uncorrected
     ceff,    # countrate corrected for pressure and efficiency (often == corr)
     corr,    # countrate corrected for pressure
     press]   # atmospheric pressure in mbar
    """
    data = []
    for hour in range(0, 24):
        data += read_1m(options, station, year, month, day, hour)

    return data


# --------------------------------------------------------------------------
def read_rev(options, station, data_type, year, month=None, day=None):
    """read revised data

    options     verbose, dryrun, ...
    station     station short name, must be valid station
    data_type   "ori", "1h", "env", "meta"
    year        integer (1950-9999), may not be None
    month       integer (1-12), if None, read month 1-12
    day         integer (1-31), if None, read day 1-31

    return list of values in nmdb format, all countrates are counts/s
    [str2datetime(str(start_date_time)),
     60,      # length of the measurement in seconds: 60 for 1min data
     uncorr,  # countrate of the whole monitor, uncorrected
     ceff,    # countrate corrected for pressure and efficiency (often == corr)
     corr,    # countrate corrected for pressure
     press]   # atmospheric pressure in mbar
    """

    if station in stations:
        pass
    else:
        raise ValueError  # wrong station

    data = []
    if year is None:
        raise ValueError  # year has to be specified
    elif month is None:  # read one year
        for m in range(1, 13):
            data += read_rev(options, station, data_type, year, month=m)
    elif day is None:  # read one month
        for d in range(1, 32):
            if valid_date(year, month, d):
                data += read_rev(options, station, data_type, year, month, day=d)
    else:  # read one day
        for hour in range(0, 24):
            if data_type in "1h":
                data += read_1h(options, station, year, month, day, hour)
            elif data_type in "ori":
                data += read_1m(options, station, year, month, day, hour)
            elif data_type in ["env", "meta"]:
                print("data_type '{}' not implemented yet".format(data_type))
                raise ValueError 
            else:
                print("unknown data_type: '{dt}'".format(dt=data_type))
                raise ValueError 
    return data


# --------------------------------------------------------------------------
def read_1h(options, station, year, month, day, hour):
    """"read one hour of data with 1-hour resolution
    just returning some dummy data
    """
    data = []
    start_date_time = datetime(year, month, day, hour)
    data.append([start_date_time, 3600, 99.1, 102.0, 100.0, 1013.1])

    return data


# --------------------------------------------------------------------------
def read_1m(options, station, year, month, day, hour):
    """"read one hour of data with 1-minute resolution
    just returning some dummy data
    """
    data = []
    for minute in range(0, 60):
        start_date_time = datetime(year, month, day, hour, minute)
        data.append([start_date_time, 60, 99.1, 102.0, 100.0, 1013.1])

    return data


# --------------------------------------------------------------------------
if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("-v", dest="verbose", default=0, action="count",
            help="increment output verbosity; may be specified multiple times")
    (options, args) = parser.parse_args()

    print("This is the sample module.")

    station = "smpl"
    data_type="ori"
    #data_type="1h"
    #data_type="meta"
    year = 2023
    month = 1
    day = 1
    hour = 12

    df = read_pandas(options, station, data_type, year, month, day, online=False)
    print(df)
    #exit(0)
    
    ##data = read_1m(options, station, year, month, day, hour)
    ##data = read_1h(options, station, year, month, day)
    #data = read_rev(options, station, data_type, year, month, day)
    data = read_rt(options, station, data_type, year, month, day)

    for line in data:
        print(line)
