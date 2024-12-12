#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read Kiel3 data into a pandas dataframe in NMDB format
"""

__author__ = "Christian T. Steigies <steigies@physik.uni-kiel.de>"
__license__ = "GPL License"

import numpy as np
import pandas as pd
from datetime import datetime
#from statistics import median
import sqlite3
#from nmdb3.tools.datetool import str2datetime, valid_date

#from nmdb.tools.query import dt_start_stopp

# realtime: read nm_raw files
# revised: read from sqlite

my_station = ["kiel3"]
my_names = {"kiel3": "KIEL3"}
my_station_longnames = {"kiel3": "Kiel (nmrena)"}
# module may support reading data for multiple station, with different pressures
pressure = {"kiel0": [600., 1100.],  # (961.8 - 1041.05) mbar
            "kiel1": [700., 1100.],  # (961.8 - 1041.05) mbar
            "kiel2": [800., 1100.],  # (961.8 - 1041.05) mbar
            "kiel3": [900., 1100.],  # (961.8 - 1041.05) mbar
            }
countrate = {"kiel3": [60, 6000]}  # typical counts per tube (450-600) / min

TUBES = 18 # Kiel is an 18NM64

# one hour long-term averages
# taken from original IZMIRAN software
n0 = [#0, # first tube is ch_01 not 0
      30220, 35780, 36960, 37362, 37020, 31690,
      32550, 36785, 38000, 37284, 36826, 32270,
      32200, 37003, 37685, 37910, 37125, 31030]

# pressure sensors mapping to sqlite column names
#sensor= {"BM35": "p_bm35",
#         "BM35b": "p_bm35",
#         "int": "p_int",
#         "GB1": "p_gb1"}

# --------------------------------------------------------------------------
def min_value(station, measure, checked=False):
    """
    minimum value (countrate, pressure) the station will ever measure.
    if checked is True, accept 10 times lower values (for use in revise)
    """

    print(measure)
    if station in my_station:
        value = measure[station][0]
        if checked:
            value = value/10.
    else:
        raise ValueError # station not defined

    return (value)


# --------------------------------------------------------------------------
def max_value(station, measure, checked=False):
    """
    maximum value (countrate, pressure) the station will ever measure.
    if checked is True, accept 10 times higher values (for use in revise)
    """

    print(measure)
    if station in my_station:
        value = measure[station][1]
        if checked:
            value = value*10.
    else:
        raise ValueError # station not defined

    return (value)

# --------------------------------------------------------------------------
def corrected_for_pressure(uncorrected, pressure_mbar):
    """correct countrates to standard pressure"""
    from math import exp
    
    press_0 = 1006.7

    corrected = uncorrected * exp(0.00721*(pressure_mbar-press_0))

    return corrected

# --------------------------------------------------------------------------
def corrected_for_efficiency(corrected):
    """no efficiency correction for kiel (yet)"""

    return corrected

# --------------------------------------------------------------------------
def efficiencies(data):
    """efficiency: compare with (long term?) hour average of each channel"""
    eff = []
    for ch in range(0, TUBES):
        eff.append(data[ch]*60./n0[ch])
    
    return eff

# --------------------------------------------------------------------------
def tube2ch(station, num):
    """
    map tube number to data channel
    3 sections with 8 counters each
    the outer tubes of each section (0 and 7) are not connected
    """
    # TODO lists start at 0, median calculation is wrong if 0 is element 0
    # do not shift ch numbers by 1...
    # TODO map tubes to section Green, Yellow, Red?
    if station in "kiel":
        if num <= 0:
            raise ValueError  # tube number too small
        elif num <= TUBES/3:  # first section
            return num + 1
        elif num <= TUBES/3*2:  # second section
            return num + 3
        elif num <= TUBES:  # third section
            return num + 5
        else:
            raise ValueError  # tube number too big
    else:
        print("tube2ch not defined for station", station)
        raise ValueError

# --------------------------------------------------------------------------
def p_parser(press, key="BM35"):
#def p_parser(row, key="BM35"):
    """
    input: pressure as float or string as provided by NMRENA

    BM35 column may contain two values: BM35 (Mittlerer Luftdruck)
    and BM35b.(Momentaner Luftdruck). We use only BM35.
    find :BM35: in string. Numbers until next : are p_bm35
    since 2024-01-08: GB1 data is included in BM35 column, GB1 is empty!?!
    """

    #press = row[sensor[key]]
    #print("parser:", press, key)
    value = 0.  # no pressure, store as 0
    if isinstance(press, float):  # until 2022 a single BM35 value was used
        value = float(press)
    else:
        my_dict = {}
        if press[0] == ":":  # several key:value pairs are stored
            data = press.split(":")
            keyword = data.pop(0)  # pop off first ":"
            while len(data) > 1:  # need two values: keyword and value
                keyword = data.pop(0)
                value = data.pop(0)
                my_dict[keyword] = value

        try:
            value = my_dict[key]  # return pressure for the given key
        except KeyError:  # return 0 if key not found
            value = 0.

    return float(value)

# --------------------------------------------------------------------------
def median_editor(index, row):
    """
    Kiel median editor
    replace channels that deviate by more than 20% with median scaled values
    sum all (edited) channels for the total countrate
    perform pressure and efficiency corrections on sum
    ignore known bad channels
    ignore nan for median calculation: this changes the median!
    """
    p_min = pressure["kiel3"][0]
    p_max = pressure["kiel3"][1]
    cr_min = countrate["kiel3"][0]
    cr_max = countrate["kiel3"][1]

    ts = index.replace(second=0)  # set seconds to zero
    #print(row)
    length = float(row['integration'])
    # TODO check for length off by more than 1 sec?
    # TODO flag bad values, write to separate table for manual processing?
    press = p_parser(row['p_bm35'], 'BM35')  # BM35 averaged value
    # crude check for invalid data
    if (press < p_min) or (press > p_max):
        return None

    # TODO check for missing values, use other sensors. in read_rev?

    # first ch is ch01
    counts = np.zeros(TUBES)
    edited = np.zeros(TUBES)
    for i in range(0, TUBES):
        ch = "ch%02i" % (tube2ch('kiel', i+1))
        #if mode == "rt":
        #    ch = "ch%02i" % (tube2ch('kiel', i))
        #elif mode == "rev":
        #    ch = "ch_%02i" % (tube2ch('kiel', i))
        #else:
        #    raise ValueError  # wrong mode in median_editor
        counts[i] = int(row[ch])

    # eliminate bad channels: typical countrate per tube is 600
    # channels off by a factor of 10 are considered to be bad
    nobad = np.ma.masked_outside(counts, cr_min, cr_max)
    # convert mask to nan to prevent User Warning: converting a masked element to nan
    counts_nan = np.ma.filled(nobad.astype(float), np.nan)
    eff = efficiencies(counts_nan)  # eff without known bad channels
    m = np.nanmedian(eff)  # ignore NaN for median calculation

    edit_ch = 0
    for i in range(0, TUBES):
        # known bad channels or more than 20% deviation from median
        if nobad.mask[i] or (eff[i] < (m-0.2)) or (eff[i] > (m+0.2)):
            # take length of measurement (60s +- delta t) into account!?
            edited[i] = m*n0[i]/length  # replace by median scaled value
            edit_ch += 1
        else:
            edited[i] = counts[i]

    if False:
        print("counts", counts)
        print("nobad ", nobad)
        print("w. NaN", counts_nan)
        print("eff   ", eff)
        print("median", m)
        print("mask  ", nobad.mask)
        print("edited", edited)
        print()

    # TODO divide by length a second time?
    uncorr = sum(edited)/length
    corr = corrected_for_pressure(uncorr, press)
    ceff = corrected_for_efficiency(corr)

    df = pd.DataFrame({'start_date_time': [ts],
        'interval': [60],
        'uncorr': [uncorr],
        'ceff': [ceff],
        'corr': [corr],
        'press': [press],
        'edit_ch': [edit_ch],
        'bad_ch': [sum(nobad.mask)]})

    df.index = pd.to_datetime(df['start_date_time'])
    df.drop(["start_date_time"], axis=1, inplace=True)

    return(df)

# --------------------------------------------------------------------------
def read_rt(station, data_type, year, month, day):
    """
    read realtime data for one day at a time
    return dataframe in nmdb format
    """

    #print("read_rt: reading for", year, month, day)
    if data_type in  ["env", "meta"]:  # not yet implemented
        return None

    df_day = []  # list with dataframes for all hours of the day
    for hour in range(0, 24):
        #df_raw = []  # list with dataframes of raw data for one hour
        df = read_raw(year, month, day, hour)
        if df is not None:
            #df = pd.concat(df_raw)  # dataframe with Kiel3 raw data
            df_hour = []  # list of dataframes for one hour
            for index, row in df.iterrows():  # better: list comprehension...
                df_hour.append(median_editor(index, row))
            df_nmdb = pd.concat(df_hour)  # dataframe with Kiel3 data in NMDB format
            #print("df_nmdb", df_nmdb)
            if data_type in  ["1m"]:
                df_day.append(df_nmdb)
                #print(len(df_day))
            elif data_type in  ["1h"]:  # calculate one hour averages
                df_1h = pd.DataFrame({
                    'start_date_time': [pd.to_datetime(datetime(year, month, day, hour))],
                    'interval': [3600],
                    'uncorr': [df_nmdb.mean()["uncorr"]],
                    'ceff': [df_nmdb.mean()["ceff"]],
                    'corr': [df_nmdb.mean()["corr"]],
                    'press': [df_nmdb.mean()["press"]]})
                df_1h.index = pd.to_datetime(df_1h['start_date_time'])
                df_1h.drop(["start_date_time"], axis=1, inplace=True)
                df_day.append(df_1h)
        else:  # not yet defined, exit early
            return None
    #print(df_hour)  # check/warn number of bad channels
    return(pd.concat(df_day))  # dataframe with Kiel3 data in NMDB format

# --------------------------------------------------------------------------
def read_rev(station, data_type, year, month, day=None):
    """read revised data

    station     station short name, must be valid station
    data_type   "1m", "1h", "env", "meta"
    year        integer (1950-9999), may not be None

    month       integer (1-12), may not be None
    day         integer (1-31), if None, read day 1-31

    return dataframe in nmdb format

    read sqlitefile produced by lvl0, lvl1, lvl2, ... functions?
    """
    return None

# --------------------------------------------------------------------------
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
        filename = "/data/nm64/kiel/%s_%04i-%02i.raw.sqlite" \
            % (station, year, month)
        table = 'data'
    else:  # all levels of revised data, yearly files
        filename = "/data/nm64/kiel3/%s_%04i.rev.sqlite" \
            % (station, year)
        table = 'lvl%i' %(lvl)
    try:
        con = sqlite3.connect(filename)
    except:
        return None

    (start, stopp) = dt_start_stopp(year, month, day)
    query = "SELECT * FROM '%s' WHERE datetime BETWEEN '%s' AND '%s'" %(table, start, stopp)
    #print(query)
    try:
        df = pd.read_sql_query(query, con)
    except Exception as error:  # OperationalError
        print(error)
        return(None)
    df.index = pd.to_datetime(df['datetime'])
    df.index = df.index.tz_localize(None)  # remove TZ
    df.drop(['datetime'], axis=1, inplace=True) # drop obsolete columns

    return(df, con)

# --------------------------------------------------------------------------
def lvl0(station, year, month, day=None):
    """
    create sqlite database with lvl0 data

    test case:
        "2023-10-17 17:13:00" (missing 17:12:00, double length?)
        "2022-07-20 09:30:00" BM35 contains only ":"
    """

    (df, con) = read_lvl(station, -1, year, month, day)
    con.close()
    #if station in my_station:
    #    pass
    #else:
    #    raise ValueError  # wrong station

    ## read from sqlite
    #filename = "/data/nm64/kiel/%s_%04i-%02i.raw.sqlite" \
    #        % (station, year, month)
    #try:
    #    con = sqlite3.connect(filename)
    #except:
    #    return None

    #(start, stopp) = dt_start_stopp(year, month, day)
    #query = "SELECT * FROM data WHERE datetime BETWEEN \"%s\" AND \"%s\"" % (start, stopp)
    #try:
    #    df = pd.read_sql_query(query, con)
    #    con.close()
    #except:  # OperationalError:  # raw.sqlite file does not exist
    #    return

    # use datetime as index
    #df.index = pd.to_datetime(df['datetime'])
    #df.drop(["datetime"], axis=1, inplace=True)  # drop unused columns

    # write to sqlite
    # TODO put everything in dataframe, df.to_sql
    filename = "/data/nm64/kiel3/%s_%04i.rev.sqlite" \
            % (station, year)
    try:
        con = sqlite3.connect(filename)
    except:
        return None

    cols = "datetime DATE PRIMARY KEY ASC, integration FLOAT, t_int FLOAT, p_int FLOAT, p_bm35 FLOAT, p_gb1 FLOAT"
    for i in range(1, TUBES+1):
        cols += ", ch%02i INT" % (i)
    query= "CREATE TABLE IF NOT EXISTS lvl0 (%s);" % (cols)
    con.execute(query)

    for index, row in df.iterrows():  # better: list comprehension...
        ts = index.replace(second=0)  # set seconds to zero
        length = float(row['integration'])
        t_int = row["t_int"]
        p_int = p_parser(row["p_int"], 'int')  # internal sensor
        p_bm35 = p_parser(row["p_bm35"], 'BM35')  # BM35 averaged value
        p_gb1 = p_parser(row["p_gb1"], 'GB1')  # GB1 not connected
        counts = np.zeros(TUBES+1)
        # copied from median_editor
        for i in range(1, TUBES+1):  # TODO channel 1-18 not 0-17!
            # TODO ch_01 or ch01?
            ch = "ch_%02i" % (tube2ch('kiel', i))
            #ch = "ch%02i" % (tube2ch('kiel', i))
            counts[i] = int(row[ch])

        data = "\"%s\", %f, %f, %f, %f, %f" % (ts, length, t_int, p_int, p_bm35, p_gb1)
        for i in range(1, TUBES+1):
            data += ", %i" % counts[i]
        query= "INSERT OR IGNORE INTO lvl0 VALUES (%s);" % (data)
        #print(query)
        con.execute(query)
    con.commit()
    con.close()

    return()

# --------------------------------------------------------------------------
def lvl1(station, year, month, day=None):
    """
    create lvl1 data
    find tubes with countrate out of range and set to NA
    find pressure out of range and set to NA
    """

    p_min = pressure["kiel3"][0]
    p_max = pressure["kiel3"][1]
    cr_min = countrate["kiel3"][0]
    cr_max = countrate["kiel3"][1]

    (df, con) = read_lvl(station, 0, year, month, day)
    # TODO rename column from interval to integration?

    # Verify that result of SQL query is stored in the dataframe
    #print(df.head())

    # BM35 barometer
    df.loc[df['p_bm35'] < p_min,'p_bm35'] = np.nan  # pressure too low
    df.loc[df['p_bm35'] > p_max,'p_bm35'] = np.nan  # pressure too high

    # internal barometer (less precision)
    df.loc[df['p_int'] < p_min,'p_int'] = np.nan  # pressure too low
    df.loc[df['p_int'] > p_max,'p_int'] = np.nan  # pressure too high

    # GB1 barometer (not connected)
    df.loc[df['p_gb1'] < p_min,'p_gb1'] = np.nan  # pressure too low
    df.loc[df['p_gb1'] > p_max,'p_gb1'] = np.nan  # pressure too high

    # this should be done in lvl2:
    # dataframe containing BM35 pressure measurements with errors:
    df_p = df.loc[pd.isna(df['p_bm35'])]
    #print(df_p)
    for idx, row in df_p.iterrows():
        press = interpolate_pressure(df, idx)
        df.at[idx, 'p_bm35'] = press  # replace missing value
        print("replacing p_bm35 at", idx, "from", row.p_bm35, "with", press)

    # eliminate counts that are clearly out of range for this station
    for i in range(1, TUBES+1):
        ch = "ch%02i" % (i)
        df.loc[df[ch] < cr_min,ch] = np.nan  # countrate too low
        df.loc[df[ch] > cr_max,ch] = np.nan  # countrate too high

    # TODO change dtypes of ch to INT instead of float64
    #df.to_sql(name='lvl1', if_exists='append', con=con)
    #df.to_sql(name='lvl1', if_exists='replace', con=con)
    con.close()

    return(df)

# --------------------------------------------------------------------------
def interpolate_pressure(df, ts):
    minutes = 2  # +- 2 minutes
    t_min = ts - pd.Timedelta(minutes=minutes)
    t_max = ts + pd.Timedelta(minutes=minutes)
    df2 = df[t_min:t_max][['p_int', 'p_bm35']]
    pressure = df2['p_bm35'].median()
    #print(pressure)

    return(pressure)

# --------------------------------------------------------------------------
def lvl2(station, year, month, day=None):
    """
    create lvl2 data
    replace tubes with countrate 0 by median scaled values
    select one pressure: p_bm35 preferred, if invalid: scale p_int
    data is invalid if interval deviates more than 1.2s from 60s
    """
    (df, con) = read_lvl(station, 1, year, month, day)

    return(df)
# --------------------------------------------------------------------------
def lvl3(station, year, month, day=None):
    """
    create lvl3 data
    sum all channels, pressure and efficiency correction
    """

# --------------------------------------------------------------------------
def read_raw(year, month, day, hour):
    """
    read raw NMIRENA data from file
    return all data in a pandas dataframe
    1       Uhrzeit UTC (des letzten HK pakets in der Minute)
    2       Uhrzeit in Sekunden
    3       Integrationszeit in Sekunden
    4       Temperatur des internen Drucksensors
    5       Luftdruck des internen Drucksensors
    6       Luftdruck des BM35 (seit 2024-01-08: auch GB1 statt BM35b?)
    7       Luftdruck des GB1 (seit 2024-01-08: ":" auf nm64data)
    8 - 15  ADC readout (future use: bias Voltages and Currents)
    16 - 39 Röhrenzählrate [min¯¹] (i.e., NICHT MEHR korrigiert nach Spalte 2)
    40 - 55 delta t-Spektrum [min¯¹] (i.e., NICHT MEHR korrigiert nach Spalte 2)
    """

    names = ["timestamp", "unixtime", "integration", "t_int",
             "p_int", "p_bm35", "p_gb1"]
    for i in range(8, 15+1):
        names.append("adc%02i" %(i-8))
    for i in range(16, 39+1):
        # BUG ?
        #names.append("ch%02i" %(i-16))  # ch00-17?
        names.append("ch%02i" %(i-15))  # ch01-18
    for i in range(40, 55+1):
        names.append("dt%02i" %(i-40))

    if year < 2023:
        filename = "~/data/kiel/%04i/%02i/kiel_%04i-%02i-%02iT%02iZ.nm_raw" \
            % (year, month, year, month, day, hour)
    else:
        #filename = "~/data/kiel/kiel_%04i-%02i-%02iT%02iZ.nm_raw" \
        filename = "/data/falbala/nm64/data/kiel/nm64_kiel_%04i-%02i-%02iT%02i:02:00Z.nm_raw" \
            % (year, month, day, hour)

    try:
        df = pd.read_csv(
            filename,
            delim_whitespace=True,
            header=None,
            names=names,
            )
    except FileNotFoundError:
        print("file not found: %s" %(filename))
        return None
    # TODO: test that 60 rows are read (when hour is complete)
    df.index = pd.to_datetime(df['timestamp'])
    df.index = df.index.tz_localize(None)  # remove TZ

    # do NOT modify BM35 column, this is taken care of in median_editor

    # drop unused columns
    df.drop(["timestamp"], axis=1, inplace=True)

    return(df)


# --------------------------------------------------------------------------
def main():
    """test kiel3 functions"""
    import argparse

    parser = argparse.ArgumentParser(description='NMDB kiel3 data.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity level')
    group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument('station', metavar='STATION', nargs='?', default='test', help='NMDB station short name')
    parser.add_argument('data_type', choices=['1m', '1h', 'env', 'meta'], nargs='?', default='1m')
    parser.add_argument('-Y', '--year', type=int, dest='year', help='year')
    parser.add_argument('-M', '--month', type=int, dest='month', help='month')
    parser.add_argument('-D', '--day', type=int, dest='day', help='day')
    parser.add_argument('-n', '--dry-run', dest='dryrun', action="store_true", help='print but do not execute commands')

    #test = 'kiel3 1m -Y 2024 -M 1 -D 1 -n'
    test = 'kiel3 1m -Y 2024 -M 11 -D 12 -n' # data on falabala
    #test = 'kiel3 1m -Y 2023 -M 9 -D 29 -n'
    #test = 'kiel3 1h -Y 2022 -M 7 -D 29 -n'
    #test = 'kiel3 1m -Y 2023 -M 8 -D 29 -n'

    # countrate goes to zero!
    #File "/home/steigies/src/python/site-packages/nmdb/upload.py", line 226, in upload
    #write += " VALUES " + mysql_row(pandas2nmdb(args, row, my_data_type, p_min, p_max,c_min, c_max))
    #                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #File "/home/steigies/src/python/site-packages/nmdb/mysql/mysql.py", line 92, in mysql_row
    #for val in row:
    #TypeError: 'NoneType' object is not iterable
    #test = 'kiel3 1h -Y 2023 -M 6 -D 12 -n'
    #test = 'kiel3 1m -Y 2023 -M 6 -D 12 -n'

    args = parser.parse_args(args=test.split())

    #mode = "raw"
    mode = "rt"
    #mode = "rev"

    print("This is the kiel3 module.")
    print(vars(args))

    year = args.year
    month = args.month
    day = args.day
    station = args.station
    data_type = args.data_type

    if mode in "raw":
        hour = 0
        data = read_raw(year, month, day, hour)

    if mode in "rt":
        data = read_rt(station, data_type, year, month, day)
        if data is not None:
            data.plot(y=["corr", "uncorr"])

    if mode in "rev":
        #data = read_rev(options, station, data_type, year, month, day)
        data = read_rev(station, data_type, year, month, day)

    return data

# --------------------------------------------------------------------------
if __name__ == '__main__':

    DO_main = False
    DO_lvl0 = False
    DO_lvl1 = False
    DO_lvl2 = False

    YEAR = 2019
    DO_main = True
    #DO_lvl0 = True
    #DO_lvl1 = True
    #DO_lvl2 = True

    if DO_main:
        print('main()')
        #data = main()
        ##for line in data:
        ##    print(line)
        ##print(data)
        station = "kiel3"
        print(min_value(station, pressure[station]))
        print(max_value(station, pressure[station]))


    if DO_lvl0:
        for i in range(1, 12+1):
            lvl0("kiel3", YEAR, i)
        #    #lvl0("kiel3", 2024, i)
    if DO_lvl1:
        #for i in range(1, 6+1):
        #    (df) = lvl1("kiel3", 2024, i)
        #    df.p_bm35.plot()
        #    df.p_int.plot()
        for i in range(1, 12+1):
            lvl1("kiel3", YEAR, i)
        #(df) = lvl1("kiel3", 2024, 1, 8)
        #df.p_bm35.plot()
        #df.p_int.plot()
        #df[['p_bm35', 'p_int']].plot()
        # TODO fail to insert rev data on duplicate keys
        # TODO fail to read for missing raw data
    if DO_lvl2:
        (df) = lvl2("kiel3", 2024, 1, 8)
