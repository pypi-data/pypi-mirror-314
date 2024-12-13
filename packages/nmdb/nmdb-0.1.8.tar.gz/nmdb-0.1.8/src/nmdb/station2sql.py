#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""convert station data (revised Minute and Hour) to SQlite file

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


## --------------------------------------------------------------------------
import os
import sys
# http://wiki.python.org/moin/ConfigParserExamples
import configparser  # python-configparser

# SpaceWx uses CentOS5 with Python2.4 and pysqlite2
try:
    from pysqlite2 import dbapi2 as sqlite3
except ImportError:
    try:
        from sqlite3 import dbapi2 as sqlite3
    except ImportError:
        print("SQLite module not found")
        sys.exit(1)

#from nmdb.tools.configtool import parse_options, parse_args
#from nmdb.sqlite import sqlfilename
#from nmdb.sqlite_format import sql_create, sql_insert

from nmdb.station import aata
from nmdb.station import drhm
from nmdb.station import kiel3
from nmdb.station import thailand

revised = {"aata": aata.read_rt,
            "drhm": drhm.read_rt,
            "mtws": drhm.read_rt,
            "ldvl": drhm.read_rt,
            "hlea": drhm.read_rt,
            "clmx": drhm.read_rt,
            "huan": drhm.read_rt,
            "kiel3": kiel3.read_rev,
            "psnm": thailand.read_rt,
            }

# --------------------------------------------------------------------------
def parser(subparsers):
    # create the parser for the "station2sql" command
    sub_p = subparsers.add_parser('station2sql', help='stored revised data in sqlite file')
    sub_p.add_argument('station', metavar='STATION', nargs='?', default='test', help='NMDB station short name')
    sub_p.add_argument('data_type', choices=['1m', '1h', 'env', 'meta'], nargs='?', default='1m')
    sub_p.add_argument('-n', '--dry-run', dest='dryrun', action="store_true", help='print but do not execute commands')
    sub_p.add_argument('--file', dest='rcfile', default='~/.nmdbrc', help='config file for NMDB')
    sub_p.add_argument('-Y', '--year', type=int, dest='year', help='year')
    sub_p.add_argument('-M', '--month', type=int, dest='month', help='month')
    sub_p.add_argument('-D', '--day', type=int, dest='day', help='day')
    sub_p.add_argument('--datadir', type=str, dest='datadir', default='/tmp', help='data directory')
    group = sub_p.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity level')
    group.add_argument("-q", "--quiet", action="store_true")
    sub_p.set_defaults(cmd="station2sql")

    return(sub_p)

# --------------------------------------------------------------------------
def oldmain():
    (options, args) = parse_options(mode="sqlite")
    if not os.path.exists(options.datadir):
        print("datadir not found:", options.datadir)
        print("please specify a writable directory for sqlite files with -D or --datadir")
        sys.exit(1)

    if options.verbose > 1:
        print("options:", options)
        print("args:", args)
        if options.dryrun:
            print("dryrun: not writing any data.")

    if options.year is None:
        print("WARNING: you should specify a year to revise with, ie --year 2015")

    try:
        (station, data_type) = parse_args(options, args, mode="sql")
    except ValueError:
        print("usage: station2sql [station] [1m|1h]\n")
        sys.exit(1)

    if not options.dryrun:
        sqlfile = sqlfilename(options.datadir, station, mode="write", data=data_type)

        sql_conn = sqlite3.connect(sqlfile)
        sql_c = sql_conn.cursor()
        # Create table
        sql_c.execute(sql_create)
        sql_conn.commit()

    data = read_rev(station, data_type, options)
    # TODO store column order in sqlite file?

    if data is None:
        return

    for mydata in data:
        if options.verbose > 1:
            print("DATA", mydata)

        ucorr = mydata[2]
        corr_e = mydata[3]
        corr_p = mydata[4]
        press = mydata[5]
        # test if at least one measured value is available
        if (ucorr or corr_e or corr_p or press) is None:
            if options.nullok:  # write all NULL values as requested by user
                if options.verbose:
                    print("writing empty data", mydata)
            else:  # do not write all NULL values
                if options.verbose:
                    print("not writing empty data", mydata)
                continue  # skip to next value

        # test for valid timestamps
        if data_type in ["1m"]:
            if mydata[0].second > 0:
                if options.verbose:
                    print("skipping invalid time for 1m data:",  mydata[0])
                continue
            else:
                pass
        elif data_type in ["1h"]:  # no length for 1h data
            if options.verbose:
                print(mydata)
            if mydata[0].minute > 0 or mydata[0].second > 0:
                if options.verbose:
                    print("skipping invalid time for 1h data:",  mydata[0])
                continue
            else:
                pass
        else:
            raise ValueError  # invalid mode

        if not options.dryrun:
            sql_c.execute(sql_insert, mydata)
        else:
            print (sql_insert, mydata)

    ## clean up
    if not options.dryrun:
        sql_conn.commit()
        sql_c.close()


# --------------------------------------------------------------------------
def sqlfilename(datadir, name, mode="write", data="1m", year=None):
    """
    name of sqlfile to store data in.
    all files are to be considered temporary
    """

    if data == "1m":
        sqlfile = datadir + "/" + name.upper() + "_1m" + ".sqlite"
    elif data == "1h":
        sqlfile = datadir + "/" + name.upper() + "_1h" + ".sqlite"
    elif data == "bin":  # NM64 bin data
        if year is not None:
            sqlfile = datadir + "/" + name.upper() + "_" + str(year) + "_bin" + ".sqlite"
        else:
            print("sqlitefilename: year not defined")
            sys.exit(1)
    else:
        print("unknown data: %s" % (data))
        sys.exit(1)

    if mode == "write":  # append?
        if os.path.isfile(sqlfile):
            print("sqlite file already exists: %s" % (sqlfile))
            print("please remove this file before running this script")
            sys.exit(1)

    if mode == "read":
        if not os.path.isfile(sqlfile):
            print("\nsqlite file does not exist: %s" % (sqlfile))
            print("please create this file with bartol2sql/cvs2sql first.")
            sys.exit(1)

    return sqlfile

# --------------------------------------------------------------------------
def station2sql(args):
    """convert station data to sqlite"""
    print("This is NMDB station2sql "
          "(converting revised Minute and Hour data).\n")

    if args.verbose > 1:
        #print("args:", args)
        print(vars(args))
    if args.dryrun:
        print("dryrun: not sending any data to NMDB")
    my_rcfile = args.rcfile
    my_station = args.station
    #my_station = "kiel3"
    my_data_type = args.data_type
    #my_data_type = "1m"
    my_year = int(args.year)
    my_month = int(args.month)
    try:
        my_day = int(args.day)
    except:
        my_day = None

    if my_data_type in ["1m", "1h"]:
        pass
    elif my_data_type in ["env", "meta"]:
        raise ValueError  # not yet implemented
    else:
        raise ValueError  # illegal data_type

    #config = configparser.ConfigParser()
    #try:
    #    rcfile = os.path.expanduser(my_rcfile)
    #    config.read(rcfile)
    #except:
    #    print("parse_config: rcfile not found:", my_rcfile)
    #    raise ValueError

    try:
        read_rev = revised[my_station]
    except KeyError:
        print("No import filter for %s available" % (my_station))
        raise ValueError  # station undefined
    except:
        raise ValueError  # unknown error

    if not args.dryrun:
        sqlfile = sqlfilename(args.datadir, my_station, mode="write", data=my_data_type)
        sql_conn = sqlite3.connect(sqlfile)

    try:
        #df = read_rev(my_station, my_data_type, next_data.year, next_data.month, next_data.day)
        df = read_rev(my_station, my_data_type, my_year, my_month, my_day)
        if df is None:
            if args.verbose:
                print("no data for %4i-%2i%2i" %(my_year, my_month, my_day))
        else:
            #print(df.to_string())
            #data.append(df)
            pass
    except:
        raise ValueError

    if not args.dryrun:
        df.to_sql(name='df', con=sql_conn)

# --------------------------------------------------------------------------
if __name__ == "__main__":

    from nmdb.parser import nmdb_parser
    parser = nmdb_parser()

    #test = 'station2sql kiel3 1m --dry -v -Y 2024 -M 11'
    test = 'station2sql kiel3 1m -v -Y 2024 -M 11'

    args = parser.parse_args(args=test.split())
    #args = ""
    print(vars(args))
    station2sql(args)
