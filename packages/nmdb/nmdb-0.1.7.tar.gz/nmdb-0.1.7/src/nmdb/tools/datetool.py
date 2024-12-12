#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 10:33:02 2023

@author: steigies
"""
from datetime import datetime, date, time
import pandas as pd
import numpy as np
from nmdb.station.station_name import station_name

# --------------------------------------------------------------------------
def idate(year, month, day):
    timestamp = date(int(year), int(month), int(day))
    return timestamp

# --------------------------------------------------------------------------
def itime(hour, minute, sec):
    timestamp = time(int(hour), int(minute), int(sec))
    return timestamp


# --------------------------------------------------------------------------
def last_datapoint(cursor, table, station):
    """return timestamp of last value for station in real-time table"""

    if table in ["1m"]:  # 1m real-time data is in ori table
        table = "ori"
    elif table in ["ori", "1h", "env", "meta"]:
        pass
    elif table in ["rev"]:
        raise ValueError  # rev is not a real-time table
    else:
        raise ValueError  # illegal table

    station = station_name(station)  # kiel3 is stored as kiel2
    #print("last_datapoint for %s" %(station))
    select = "SELECT start_date_time FROM"
    order = "ORDER BY start_date_time DESC LIMIT 1"
    querystring = "%s %s_%s %s;" % (select, station.upper(), table, order)
    cursor.execute(querystring)
    answer = cursor.fetchone()
    if answer is None:
        print("%s_%s is empty, you should select a --startdate. "
        "Using default date." % (station.upper(), table))
        lastdatapoint = datetime(2000, 1, 1, 0, 0, 0)
    else:
        lastdatapoint = answer[0]

    #return(lastdatapoint)
    return(pd.to_datetime(lastdatapoint))


# --------------------------------------------------------------------------
def nmdb_timestamp(cursor):
    """get current timestamp from database server"""

    qstring = "SELECT CURRENT_TIMESTAMP()"
    cursor.execute(qstring)
    value = cursor.fetchone()

    return value[0]


# --------------------------------------------------------------------------
def str2datetime(string, zero=False):
    """convert string into datetime timestamp"""

    if string:
        # datetime.strptime is not available on CentOS
        # dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

        if "T" in string:
            (mydate, mytime) = string.split("T")
            # print(mydate)
            if "Z" in mytime:
                mytime = mytime[:-1]
                # print(mytime)
        else:
            (mydate, mytime) = string.split()
        (year, month, day) = mydate.split("-")
        (hour, minute, sec) = mytime.split(":")
        if zero:  # set seconds to zero
            sec = 0
        # timestamp = datetime(int(year), int(month), int(day), int(hour), int(minute), int(sec))
        timestamp = datetime.combine(idate(year, month, day),
                                     itime(hour, minute, sec))
        #return timestamp
        return np.datetime64(timestamp)
    else:
        raise ValueError


# --------------------------------------------------------------------------
def sys_timestamp(format="dt"):
    """get system time in UTC"""
    from time import gmtime, strftime
    now = gmtime()
    if format in ["dt", "datetime"]:
        value = datetime(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    elif format in ["str", "string"]:
        value = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    else:
        raise ValueError  # unknown format
    return value


