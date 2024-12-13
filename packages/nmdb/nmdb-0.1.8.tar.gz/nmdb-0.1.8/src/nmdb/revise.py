#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""NMDB revise: upload revised 1min and 1h data

Copyright (C) 2008-2019 Christian T. Steigies <steigies@physik.uni-kiel.de>

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

import MySQLdb  # apt-get install python-mysqldb # yum install MySQL-python
import datetime
import sys
import os

#http://docs.python.org/library/sqlite3.html
# SpaceWx uses CentOS5 with Python2.4 and pysqlite2
try:
    from pysqlite2 import dbapi2 as sqlite3
except ImportError:
    try:
        from sqlite3 import dbapi2 as sqlite3
    except ImportError:
        print("SQLite module not found")
        sys.exit(1)

# database table definitions:
from nmdb3.nmdb.nmdb_format import ori_format, rev_format, hour_format
from nmdb3.nmdb.nmdb_class import NMDBdata
from nmdb3.nmdb.sqlite import SqlData
from nmdb3.tools.datetool import read_datapoint, str2datetime
# last_datapoint
from nmdb3.tools.configtool import parse_options, parse_config, parse_args
from nmdb3.tools.configtool import date_range
from nmdb3.tools.almost_equal import almost_equal
from nmdb3.station.station_data import check_data, check_pressure
from nmdb3.nmdb.mysql import mysql_values
from nmdb3.nmdb.mysql import write_nmdb
from nmdb3.nmdb.mysql_query import query, insert_meta, read_meta_id
#from nmdb.tools.mysql_write import BufferData


## --------------------------------------------------------------------------
def revise_data(options, cursor, name, new, old, mode):
    """
    compare new and old
    if data is different, increase version number
    use version = 0 as initial version (ie ori data)
    write only when they are different
    return number of written datasets
    """

    # TODO: allow user to specify ranges for checks
    new.u = check_data(new.u, cr_min=0.1, cr_max=10000.)
    new.p = check_pressure(new.p, p_min=500., p_max=1200.)
    new.c = check_data(new.c, cr_min=0.1, cr_max=10000.)
    new.e = check_data(new.e, cr_min=0.1, cr_max=10000.)

    value = 0
    # data is usually written with two or three digits precision
    # compare up to two to find out if data has changed
    if (almost_equal(new.u, old.u, 2) and
        almost_equal(new.e, old.e, 2) and
        almost_equal(new.c, old.c, 2) and
        almost_equal(new.p, old.p, 2) and
        almost_equal(new.len, old.len, 2)
        ):
        if options.verbose > 1:
            print("data is equal")
    else:
        if options.verbose > 0:
            print("data is not equal, UPDATE!")
            old.show()
            new.show()
        if old.version is None:
            version = 0
        else:
            version = old.version + 1

        if mode == "rev":
            value = write_revori(options, cursor, name, new, version)
        elif mode == "1h":
            value = write_1h(options, cursor, name, new, version)
        else:
            raise ValueError  # illegal mode

    return value


## --------------------------------------------------------------------------
def write_revori(options, cursor, name, revori, version=0):
    """
    v = 0: ori
    v = 1: rev, initial
    v = 2: rev, revised
    columns in the same order as in NMDB and tools/nmdb_format!
    return number or written datasets
    """

    global data_ori_i, data_rev_i, data_rev_r

    value = 1
    if version == 0:
        data_ori_i.append((str(revori.datetime), revori.len,
                           revori.u, revori.e, revori.c, revori.p))
        if len(data_ori_i) >= buffer_len:
            value = flush(options, cursor, name, "1m", data_ori_i, version)
            data_ori_i = []
    elif version == 1:
        data_rev_i.append((str(revori.datetime), revori.len,
                           revori.u, revori.e, revori.c, revori.p, version))
        if len(data_rev_i) >= buffer_len:
            value = flush(options, cursor, name, "1m", data_rev_i, version)
            data_rev_i = []

    else:
        data_rev_r.append((str(revori.datetime), revori.len,
                           revori.u, revori.e, revori.c, revori.p, version))
        if len(data_rev_r) >= buffer_len:
            value = flush(options, cursor, name, "1m", data_rev_r, version)
            data_rev_r = []

    return value


## --------------------------------------------------------------------------
def write_1h(options, cursor, name, new, version=0):
    """
    overwrite with new 1h data
    store data in global variable, separate for insert and replace
    write many values in one command when 12 values are stored
    remember to flush the remaining data in the end
    """

    global data_1h_i, data_1h_r
    value = 0

    if version == 0:
        data_1h_i.append((str(new.datetime), new.u, new.e, new.c, new.p))
        if len(data_1h_i) >= buffer_len:
            value = flush(options, cursor, name, "1h", data_1h_i, version)
            data_1h_i = []
    else:
        data_1h_r.append((str(new.datetime), new.u, new.e, new.c, new.p))
        if len(data_1h_r) >= buffer_len:
            value = flush(options, cursor, name, "1h", data_1h_r, version)
            data_1h_r = []

    return value


## --------------------------------------------------------------------------
def flush(options, cursor, name, data_type, data, version):
    """INSERT or REPLACE values"""

    if len(data) == 0:
        value = 0
    else:
        write = query(name, version, data_type)  # INSERT or REPLACE
        write += " VALUES " + mysql_values(data)
        value = write_nmdb(options, cursor, write)

    return value


## --------------------------------------------------------------------------
def parse_answer(answer, mode):
    """store return values from NMDB in nmdb_data object
    columns have to be in the same order as in NMDB

    sqlite3 /var/tmp/nmdb/NEWK_1m.sqlite
    SQLite version 3.7.13 2012-06-11 02:05:22
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> .schema data
    CREATE TABLE data
    (datetime timestamp, interval int, ucorr real, corr_e real, corr_p real, pressure real);
    sqlite> select * from data limit 1;
    2013-07-18 21:15:00|60|92.51|90.68|90.68|1010.519
    sqlite> select datetime, interval, ucorr, pressure, corr_p, corr_e from data limit 1;
    2013-07-18 21:15:00|60|92.51|1010.519|90.68|90.68
    """

    if answer is None:
        return None

    if mode == "nmdb-1h":
        (dt, ucorr, corr_e, corr_p, press) = answer
        length = 3600
        version = 0
    elif mode == "1h":
        (dt, length, ucorr, corr_e, corr_p, press) = answer
        version = 0
    elif mode == "rev":
        try:
            (dt, length, ucorr, corr_e, corr_p, press, version) = answer
        except ValueError:
            (dt, length, ucorr, corr_e, corr_p, press) = answer
            version = 0
    else:
        print("parse_answer: unknown mode")
        sys.exit(1)

    try:
        data = NMDBdata(dt=dt,
                    length=length,
                    uncorr=ucorr,
                    p_mbar=press,
                    corr_p=corr_p,
                    corr_e=corr_e,
                    version=version)
    except TypeError:
        print(answer)
        sys.exit(1)

    return data


## --------------------------------------------------------------------------
def main():
    """revise"""
    print("This is NMDB revise.")

    (options, args) = parse_options(mode="revise")

    if options.verbose > 1:
        print("options:", options)
        print("args:", args)
    if options.dryrun:
        print("dryrun: not sending any data to NMDB")
    rcfile = options.rcfile

    try:
        (station, mode) = parse_args(options, args)
    except ValueError:
        print("usage: revise <station> [ori|1h]\n")
        sys.exit(1)

    try:
        (username, password, longname) = parse_config(rcfile, station)
    except:
        print("station %s is not defined in %s." % (station, rcfile))
        sys.exit(1)

    print("Sending revised %s data for %s (%s)" % (mode, username, longname))

    #data_buffer = BufferData(len=12)

    ## select appropriate mode to load data to be sent to NMDB
    if mode in ["1m", "ori"]:
        if options.verbose > 0:
            print("switching to rev mode")
        mode = "rev"
        #delta_t = 1
    elif mode == "rev":
        if options.verbose > 0:
            print("using rev mode")
        #delta_t = 1
    elif mode == "1h":
        if options.verbose > 0:
            print("rev mode for 1h data")
        #delta_t = 60
    else:
        print("main(1): invalid mode")
        sys.exit(1)

    if mode == "rev":
        filename = options.datadir + "/" + station.upper() + "_1m.sqlite"
        meta_comment = "revised ori data"
    elif mode == "1h":
        filename = options.datadir + "/" + station.upper() + "_1h.sqlite"
        meta_comment = "revised 1h data"
    else:
        print("main(2): invalid mode")
        sys.exit(1)

    if os.path.exists(filename):
        print("Reading from SQLite file:", filename)
        data = SqlData(filename)
    else:
        print("SQLite file does not exist:", filename)
        sys.exit(1)

    revised = data.generator()

    (start_date, stopp_date) = date_range(data, options)
    if options.verbose > 0:
        print("start", start_date)
        print("stopp", stopp_date)

    ## open connection to NMDB
    con = MySQLdb.connect(host=options.hostname,
                          port=options.portnum,
                          db="nmdb",
                          user=username,
                          passwd=password,
                          )
    nmdb = con.cursor()
    meta_id = read_meta_id(nmdb, station) + 1
    next_day = start_date + datetime.timedelta(days=1)
    count = 0

    while True:
        try:
            answer = next(revised)
            #answer = revised.__next__()
            #print(answer)
            new = parse_answer(answer, mode)

            if options.verbose > 2:
                print("NEW",)
                new.show()

            this_date = new.datetime
            this_datetime = str2datetime(this_date)
            if this_datetime >= next_day:  # show progress for every day read
                print("read up to", this_date, "written", count, "values")
                next_day = this_datetime + datetime.timedelta(days=1)
                # in case of crash not all data has been written yet
                # this_date is too new then, where to get last_written_date?
                # do NOT write meta data every day: causes Deadlockon cluster
                #if not options.dryrun:
                #    nmdb.execute(insert_meta(station, start_date, this_date, 0, meta_comment, meta_id))

            if mode == "1h":
                answer = read_datapoint(nmdb, "1h", station, this_date, values=hour_format)
                ori = parse_answer(answer, mode="nmdb-1h")
                if ori is None:
                    if options.verbose > 2:
                        print("1h  None")
                else:
                    if options.verbose > 2:
                        print("1h ",)
                        ori.show()

                if ori is None:  # data is new, INSERT it
                    if options.verbose > 1:
                        print("no data in NMDB for", this_date, "write as initial value")
                        # None can not be shown ori.show()
                    count += write_1h(options, nmdb, station, new, 0)
                    continue
                else:  # check if data is equal, only write changed data
                    if options.verbose > 1:
                        print("data is in NMDB 1h TABLE for", this_date, "need to revise")
                    count += revise_data(options, nmdb, station, new, ori, mode)

            elif mode == "rev":
                answer = read_datapoint(nmdb, "ori", station, this_date, values=ori_format)
                ori = parse_answer(answer, mode)

                if options.verbose > 2:
                    if ori is None:
                        print("ORI None")
                    else:
                        print("ORI",)
                        ori.show()

                answer = read_datapoint(nmdb, "rev", station, this_date, values=rev_format)
                rev = parse_answer(answer, mode)
                if options.verbose > 2:
                    if rev is None:
                        print("REV None")
                    else:
                        print("REV",)
                        rev.show()

                if ori is None:
                    if options.verbose > 2:
                        print("no data in NMDB for", this_date, "write as initial value")
                        new.show()
                    count += write_revori(options, nmdb, station, new, 0)
                    continue
                else:
                    if options.verbose > 1:
                        print("data is in NMDB ORI TABLE for", this_date, "need to revise")
                    if rev is None:  # no data in rev
                        # if revise is needed, write to rev as version 1
                        count += revise_data(options, nmdb, station, new, ori, mode)
                    else:  # data is in rev
                        count += revise_data(options, nmdb, station, new, rev, mode)

                if count >= options.maxcount:
                    print("sent %i values, pausing...\n" % (options.maxcount))
                    break

            else:
                print("invalid mode")
                sys.exit(1)

        except StopIteration:
            break

    # write the remaining data
    print("flushing data buffers...",)
    value = 0
    if mode == "1h":
        value += flush(options, nmdb, station, "1h", data_1h_i, 0)
        value += flush(options, nmdb, station, "1h", data_1h_r, 1)
    elif mode == "rev":
        value += flush(options, nmdb, station, "1m", data_ori_i, 0)
        value += flush(options, nmdb, station, "1m", data_rev_i, 1)
        value += flush(options, nmdb, station, "1m", data_rev_r, 2)
    print(value, "buffers flushed.")

    # update the information in the meta table, all data was revised
    nmdb.execute(insert_meta(station, start_date, stopp_date, 0, meta_comment, meta_id))

    return

## --------------------------------------------------------------------------
if __name__ == '__main__':
    # setup global variables for executemany commits
    # keep separate lists for INSERT and REPLACE
    # ori data is never replaced

    # TODO: use lock files
    # TODO: check timestamps in rev, ori table,
    # if no data exists for timerange, data can be sent
    # without a query for every single timestamp
    # TODO: do not use global variables, store data in a buffer object

    data_ori_i = []
    data_rev_i = []
    data_rev_r = []
    data_1h_i = []
    data_1h_r = []
    buffer_len = 12

    main()
