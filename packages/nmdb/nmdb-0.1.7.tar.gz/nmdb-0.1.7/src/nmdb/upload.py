#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""usage: python upload3.py -v -f nmdbrc newk ori|1h

NMDB upload3: upload real-time data for all stations, python3/pandas version

Copyright (C) 2008-2024 Christian T. Steigies <steigies@physik.uni-kiel.de>

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

# --------------------------------------------------------------------------
# on centos: yum install
#   MySQL-python
#   numpy???
#   python-sqlite

#import sys
# http://wiki.python.org/moin/ConfigParserExamples
import configparser  # python-configparser
from datetime import datetime
from datetime import timedelta
import MySQLdb  # python-mysqldb
import os
import pandas as pd
import numpy as np
##import sqlite3

from nmdb.tools.configtool import config_section_map
from nmdb.tools.datetool import last_datapoint
from nmdb.tools.datetool import nmdb_timestamp
from nmdb.tools.datetool import sys_timestamp
#from nmdb.tools.datetool import str2datetime

##from nmdb3.nmdb.sqlite import SqlData
from nmdb.mysql.mysql import query #, nmdb_timestamp
from nmdb.mysql.mysql import mysql_row
from nmdb.mysql.mysql import write_nmdb

from nmdb.station import aata
from nmdb.station import drhm
from nmdb.station import kiel3

realtime = {"aata": aata.read_rt,
            "drhm": drhm.read_rt,
            "mtws": drhm.read_rt,
            "ldvl": drhm.read_rt,
            "hlea": drhm.read_rt,
            "clmx": drhm.read_rt,
            "huan": drhm.read_rt,
            "kiel3": kiel3.read_rt,}

#revised = {"aata": aata.read_rev,
#           "drhm": drhm.read_rev,
#           "kiel": kiel.read_rev,}

#pressure = {"aata": aata.pressure,
#            "drhm": drhm.pressure,
#            "kiel3": kiel3.pressure,}

#countrate = {"aata": aata.countrate,
#             "drhm": drhm.countrate,
#             "kiel3": kiel3.countrate,}


# --------------------------------------------------------------------------
def parser_upload(subparsers):
    # create the parser for the "upload" command
    sub_p = subparsers.add_parser('upload', help='upload to NMDB')
    sub_p.add_argument('station', metavar='STATION', nargs='?', default='test', help='NMDB station short name')
    sub_p.add_argument('data_type', choices=['1m', '1h', 'env', 'meta'], nargs='?', default='1m')
    sub_p.add_argument('-n', '--dry-run', dest='dryrun', action="store_true", help='print but do not execute commands')
    sub_p.add_argument('--file', dest='rcfile', default='~/.nmdbrc', help='config file for NMDB')
    sub_p.add_argument('-H', '--host', dest='hostname', default='write.nmdb.eu', help='NMDB hostname to connect to')
    sub_p.add_argument('-P', '--port', type=int, dest='port', default='3306', help='NMDB port number to connect to')
    sub_p.add_argument('-Y', '--year', type=int, dest='year', help='year')
    sub_p.add_argument('-M', '--month', type=int, dest='month', help='month')
    sub_p.add_argument('-D', '--day', type=int, dest='day', help='day')
    sub_p.add_argument('-T', '--timeout', type=int, dest='timeout', default=30, help='timeout')
    sub_p.add_argument('--maxcount', type=int, dest='maxcount', default=120, help='send max values')
    sub_p.add_argument('--start', dest='tstart', default='2020-01-01 00:00:00', help='use this start date if there is no data for this station in NMDB')
    group = sub_p.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity level')
    group.add_argument("-q", "--quiet", action="store_true")
    sub_p.set_defaults(cmd="upload")

    return(sub_p)


# --------------------------------------------------------------------------
def upload(args):
    print("This is NMDB upload.")

    if args.verbose > 1:
        #print("args:", args)
        print(vars(args))
    if args.dryrun:
        print("dryrun: not sending any data to NMDB")
    my_rcfile = args.rcfile
    my_station = args.station
    my_data_type = args.data_type

    if my_data_type in ["1m", "1h"]:
        pass
    elif my_data_type in ["env", "meta"]:
        raise ValueError  # not yet implemented
    else:
        raise ValueError  # illegal data_type

    config = configparser.ConfigParser()
    try:
        rcfile = os.path.expanduser(my_rcfile)
        config.read(rcfile)
    except:
        print("parse_config: rcfile not found:", my_rcfile)
        raise ValueError

    username = config_section_map(args.station, config)['username']
    password = config_section_map(args.station, config)['password']

    #print("upload for %s" % (my_station))
    #print("Sending real-time %s data for %s (%s)" % (data_type, username, longname))
    #print("Sending real-time %s data for %s using %s"
    #      % (my_data_type, my_station, my_rcfile))

    try:
        read_rt = realtime[my_station]
        # TODO def pressure and countrate function with station as argument
        #p_min = pressure[my_station][my_station][0]
        #p_max = pressure[my_station][my_station][1]
        #c_min = countrate[my_station][my_station][0]
        #c_max = countrate[my_station][my_station][1]
        p_min = 100.
        p_max = 1500.
        c_min = 1.
        c_max = 1000000.

    except KeyError:
        print("No import filter for %s available" % (my_station))
        raise ValueError  # station undefined
    except:
        raise ValueError  # unknown error

    # upload is executed every minute, so we need to timeout after ~30 seconds
    start = pd.to_datetime(datetime.now())
    timeout = start + timedelta(seconds=args.timeout)

    # open connection to NMDB
    con = MySQLdb.connect(host=args.hostname, port=args.port, 
                          db="nmdb", user=username, passwd=password)
    nmdb = con.cursor()

    # sys_time should be identical to nmdb_time
    # TODO warning/error if not
    sys_time = pd.to_datetime(sys_timestamp())
    nmdb_time = pd.to_datetime(nmdb_timestamp(nmdb))
    # find timestamp of last real-time value
    last_data = last_datapoint(nmdb, my_data_type, my_station)
    # TODO for debugging only go back one year
    #last_data = last_data - timedelta(days=365)
    if args.verbose > 0:
        print("system time\t", sys_time, "\t",)
        print("NMDB time\t", nmdb_time, "\t",)
        print("diff:\t", sys_time - nmdb_time)
        print("last data in NMDB", last_data)
    # only write data newer than last available data
    # for (revising) older data, use revise and station2sql
    #tstart = str2datetime(args.tstart)
    tstart = pd.to_datetime(args.tstart)
    if tstart > last_data:
        last_data = tstart
    print("start writing at:", last_data)
    # TODO if last data is one minute old, wait a bit before trying to read new RT data

    # read data starting with day of last_data
    next_data = last_data.date()
    count = 0  # counting the number of values written
    version = 0  # real-time data is always version 0
    #done = False
    data = []
    # read new day until maxvalues, timeout or two days or no data?
    while True:  # read in two days of data
        if len(data) >= 2:
            break  # two days of data read in, we are done reading in data
        if next_data > nmdb_time.date():
            break  # do not try to read data from the future, we are done
        #print("reading for ", next_data, "days read:", len(data)) 
        try:
            df = read_rt(my_station, my_data_type, next_data.year, next_data.month, next_data.day)
            if df is None:
               if args.verbose:
                    print("no data for ", next_data)
            else:
                #print(df)
                data.append(df)
            continue  # no data, try next day

            #df = df[df.index > last_data-timedelta(hours=1)]  # only data not yet in NMDB
            #df = df.replace({np.nan: None})  # store None in MySQL, not NaN
            #print(my_station, my_data_type, next_data.year, next_data.month, next_data.day)
        except:  # file not found
            if args.verbose:
                print("no data for ", next_data)
            continue  # file may be missing, try next day
        finally:
            next_data = next_data + timedelta(days=1)

    #print("done reading", next_data, "days read:", len(data))
    #print("last_data", last_data, type(last_data))
    #print("nmdb_time", nmdb_time, type(nmdb_time))

    if len(data) > 0:  # no-op when no data
        #print("df_index ", df.index[0], type(df.index[0]))
        df = pd.concat(data)  # dataframe with Kiel3 data in NMDB format
        df = df[df.index > last_data]  # only data not yet in NMDB
        df = df[df.index < nmdb_time]  # no data from the future
        df = df.replace({np.nan: None})  # store None in MySQL, not NaN

        ## TODO BUG in dryrun mode nmdb_date is not set for MXCO only?
        ## write data to NMDB
        for row in df.itertuples():
            # TODO check for valid datetime
            #print(my_station, row)
            write = query(my_station, version, my_data_type)
            write += " VALUES " + mysql_row(pandas2nmdb(args, row, my_data_type, p_min, p_max,c_min, c_max))
            count += write_nmdb(args, nmdb, write)
            if count >= args.maxcount:
                if not args.quiet:
                    print("sent %i values, pausing..." % (args.maxcount))
                break
            if datetime.now() > timeout:
                if not args.quiet:
                    print("timeout of %i seconds reached." % (args.timeout))
                    break
    con.commit()
    print("last data in NMDB", last_datapoint(nmdb, my_data_type, my_station))
    con.close()

    return


# --------------------------------------------------------------------------
def pandas2nmdb(args, row, data_type, p_min, p_max,c_min, c_max):
    """convert one row from dataframe to NMDB format
    """

    if data_type in ["ori"]:
        raise ValueError  # must be called as "1m"
    elif data_type in ["1m", "1h"]:
        #dt = row.Index  # Mariadb does not like TZ in datetime
        # https://stackoverflow.com/questions/10944047/how-can-i-remove-a-pytz-timezone-from-a-datetime-object
        dt = row.Index.replace(tzinfo=None)
        interval = row.interval
        ucorr = row.uncorr
        corr_e = row.ceff
        corr_p = row.corr
        press = row.press

        # test if at least one measured value is available
        if (ucorr or corr_e or corr_p or press) is None:
            if args.verbose:
                print("not writing empty data", row)
            return None

        if (press < p_min) or (press > p_max):
            if args.verbose:
                print("not writing unrealistic pressure", press)
            return None
        if (ucorr < c_min) or (ucorr > c_max):
            if args.verbose:
                print("not writing unrealistic ucorr", ucorr)
            return None
        if (corr_e < c_min) or (corr_e > c_max):
            if args.verbose:
                print("not writing unrealistic corr_e", corr_e)
            return None
        if (corr_p < c_min) or (corr_p > c_max):
            if args.verbose:
                print("not writing unrealistic corr_p", corr_p)
            return None

        if data_type in ["1m"]:
            if dt.second == 0:
                return [str(dt), interval, ucorr, corr_e, corr_p, press]
            else:
                if args.verbose:
                    print("skipping invalid time for 1m data:", dt)
            return None
        elif data_type in ["1h"]:  # no interval for 1h data
            if (dt.minute == 0) and (dt.second == 0):
                return [str(dt), ucorr, corr_e, corr_p, press]
            else:
                if args.verbose:
                    print("skipping invalid time for 1h data:", dt)
            return None
        else:
            raise ValueError  # invalid mode
    elif data_type in ["env", "meta"]:
        raise ValueError  # not yet implemented
    else:
        raise ValueError  # invalid mode while writing


# --------------------------------------------------------------------------
if __name__ == '__main__':
    from nmdb.parser import nmdb_parser
    parser = nmdb_parser()

    #test = 'upload kiel3 1m --dry -v -Y 2023 -M 1'
    #test = 'upload kiel3 1m --dry -v -Y 2024 -M 11'
    #test = 'upload kiel3 1h --dry -v'
    test = 'upload drhm 1m --dry -v'
    #test = 'upload hlea 1m --dry -v -Y 2024 -M 11'

    args = parser.parse_args(args=test.split())
    print(vars(args))
    upload(args)
