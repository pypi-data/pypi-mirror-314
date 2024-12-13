#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIEL2 data format

Copyright (c) 2011-2019 Christian T. Steigies <steigies@physik.uni-kiel.de>

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

This module offers functions to read NM data from the Alcala database as used in KIEL
and return data in the format as used by NMDB.

KIEL2 (Alcala) data availability:
2011-01-12 -- 2017-07-18
"""

__author__ = "Christian T. Steigies <steigies@physik.uni-kiel.de>"
__license__ = "GPL License"

# http://wiki.python.org/moin/ConfigParserExamples
import configparser  # python-configparser
import numpy as np
import pandas as pd
import os
#import MySQLdb  # python-mysqldb abstracted by sqlalchemy
from sqlalchemy import create_engine
import sqlite3

#import sys
#print(sys.path)

from nmdb.tools.query import dt_start_stopp
from nmdb.tools.configtool import config_section_map

my_station = ["kiel2"]
my_names = {"kiel2": "KIEL2"}
my_station_longnames = {"kiel2": "Kiel (alcala)"}
pressure = {"kiel2": [900., 1100.]} # (961.8 - 1041.05) mbar
countrate = {"kiel2": [60., 6000.]} # typical counts per tube (450-600) / min

TUBES = 18 # Kiel is an 18NM64

# one hour long-term averages
# taken from original IZMIRAN software
n0 = [#0, # first tube is ch_01 not 0
      30220, 35780, 36960, 37362, 37020, 31690,
      32550, 36785, 38000, 37284, 36826, 32270,
      32200, 37003, 37685, 37910, 37125, 31030]

# -------------------------------------------------------------------
def read_nmdadb(year, month=None, day=None):
    """
    read data from Alcala nmdadb and store it in sqlite files
    nmdadb table can be deleted, local mysql server not needed anymore
    """

    return None  # sqlitefiles have been created, do NOT overwrite them

    my_station = "kiel2_nmdadb"
    my_rcfile = "~/.nmdbrc"

    config = configparser.ConfigParser()
    try:
        rcfile = os.path.expanduser(my_rcfile)
        config.read(rcfile)
    except:
        print("parse_config: rcfile not found:", my_rcfile)
        raise ValueError

    username = config_section_map(my_station, config)['username']
    password = config_section_map(my_station, config)['password']
    hostname = config_section_map(my_station, config)['hostname']
    dbname = config_section_map(my_station, config)['dbname']
    #portnumber = config_section_map(my_station, config)['port']

    db_connection_str = 'mysql+pymysql://%s:%s@%s/%s' \
        % (username, password, hostname, dbname)
    db_connection = create_engine(db_connection_str)

    table = "binTable"
    (start, stopp) = dt_start_stopp(year, month, day)
    print(year, month, day, start, stopp)
    query = "SELECT * FROM %s WHERE start_date_time BETWEEN '%s' AND '%s'" \
        %(table, start, stopp)
    print(query)

    try:
        df = pd.read_sql(query, con=db_connection)
    except Exception as error:
        print(error)
        return None

    filename = "/data/nm64/kiel2/kiel2_%i.raw.sqlite" % (year)
    try:
        con = sqlite3.connect(filename)
    except:
        return None
    df.to_sql(name='data', if_exists='replace', con=con)

    return df

# --------------------------------------------------------------------------
# TODO nearly identical to kiel3 function
def read_lvl(station, lvl, year, month, day=None):
    """
    read data for lvl from sqlite
    """
    # TODO DRY! put this in a function, lvl as parameter
    if station in my_station:
        pass
    else:
        raise ValueError  # wrong station

    # sqlite file
    if lvl < 0:  # raw data, monthly files
        filename = "/data/nm64/kiel2/%s_%04i.raw.sqlite" \
            % (station, year)
        table = 'data'
    else:  # all levels of revised data, yearly files
        filename = "/data/nm64/kiel2/%s_%04i.rev.sqlite" \
            % (station, year)
        table = 'lvl%i' %(lvl)
    try:
        con = sqlite3.connect(filename)
    except:
        return None

    (start, stopp) = dt_start_stopp(year, month, day)
    if lvl < 0:
        query = "SELECT * FROM '%s' WHERE start_date_time BETWEEN '%s' AND '%s'" %(table, start, stopp)
    else:
        query = "SELECT * FROM '%s' WHERE datetime BETWEEN '%s' AND '%s'" %(table, start, stopp)
    print(query)
    try:
        df = pd.read_sql_query(query, con)
    except Exception as error:
        print(error)
        return(None)

    if lvl < 0:
        df['datetime'] = df['start_date_time']
        df.drop(['start_date_time', 'index'], axis=1, inplace=True) # drop obsolete columns
    df.index = pd.to_datetime(df['datetime'])
    df.index = df.index.tz_localize(None)  # remove TZ
    df.drop(['datetime'], axis=1, inplace=True) # drop obsolete columns

    return(df, con)

# -------------------------------------------------------------------
def lvl0(station, year, month=None, day=None):
    """
    create sqlite database with lvl0 data
    """
    if station in my_station:
        pass
    else:
        raise ValueError  # wrong station

    (df, con) = read_lvl(station, -1, year, month, day)
    con.close()

    df['press'] = df['atmPressure']/100.
    df.drop(['atmPressure', 'hv1', 'hv2', 'hv3', 'temp_1', 'temp_2'], axis=1, inplace=True) # drop obsolete columns

    # write to sqlite
    filename = "/data/nm64/kiel2/%s_%04i.rev.sqlite" % (station, year)
    try:
        con = sqlite3.connect(filename)
    except:
        return None
    #df.to_sql(name='lvl0', if_exists='append', con=con)
    df.to_sql(name='lvl0', if_exists='replace', con=con)
    con.close()

    return(df)

# --------------------------------------------------------------------------
def interpolate_pressure(df, ts):
    minutes = 2  # +- 2 minutes
    t_min = ts - pd.Timedelta(minutes=minutes)
    t_max = ts + pd.Timedelta(minutes=minutes)
    df2 = df[t_min:t_max][['press']]
    pressure = df2['press'].median()
    #print(pressure)

    return(pressure)

# --------------------------------------------------------------------------
def lvl1(station, year, month=None, day=None):
    """
    create lvl1 data
    find tubes with countrate out of range and set to NA
    find pressure out of range and set to NA
    """

    p_min = pressure["kiel2"][0]
    p_max = pressure["kiel2"][1]
    cr_min = countrate["kiel2"][0]
    cr_max = countrate["kiel2"][1]

    (df, con) = read_lvl(station, 0, year, month, day)

    # Verify that result of SQL query is stored in the dataframe
    print(df.head())

    # BM35 barometer
    df.loc[df['press'] < p_min,'press'] = np.nan  # pressure too low
    df.loc[df['press'] > p_max,'press'] = np.nan  # pressure too high

    # this should be done in lvl2:
    # dataframe containing BM35 pressure measurements with errors:
    df_p = df.loc[pd.isna(df['press'])]
    print(df_p)
    for idx, row in df_p.iterrows():
        press = interpolate_pressure(df, idx)
        df.at[idx, 'press'] = press  # replace missing value
        print("replacing press at", idx, "from", row.press, "with", press)

    # eliminate counts that are clearly out of range for this station
    for i in range(1, TUBES+1):
        ch = "ch%02i" % (i)
        df.loc[df[ch] < cr_min,ch] = np.nan  # countrate too low
        df.loc[df[ch] > cr_max,ch] = np.nan  # countrate too high

    # TODO change dtypes of ch to INT instead of float64
    #df.to_sql(name='lvl1', if_exists='append', con=con)
    df.to_sql(name='lvl1', if_exists='replace', con=con)
    con.close()

    return(df)

# --------------------------------------------------------------------------
if __name__ == '__main__':
    DO_read = False
    DO_lvl0 = False
    DO_lvl1 = False
    DO_lvl2 = False

    YEAR = 2011
    #DO_read = True
    #DO_lvl0 = True
    DO_lvl1 = True
    #DO_lvl2 = True

    station = "kiel2"
    data_type = "1m"

    if DO_read:
        df = read_nmdadb(year=2011, month=1, day=15)
        print(df)

    if DO_lvl0:
        for year in range(2011, 2017+1):
            df = lvl0(station, year)
            print(df)

    if DO_lvl1:
        #df = lvl1(station, 2011,1,15)
        #print(df)
        for year in range(2011, 2017+1):
            df = lvl1(station, year)
            print(df)
