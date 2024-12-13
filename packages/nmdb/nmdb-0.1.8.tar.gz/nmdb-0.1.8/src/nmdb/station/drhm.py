#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""University of New Hampshire data format

Copyright (C) 2014-2023 Christian T. Steigies <steigies@physik.uni-kiel.de>

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

This module offers functions to read NM data in ASCII from an FTP server
as used in New Hampshire and return data in the format as used by NMDB."""

__author__ = ["Malcolm Colson <malcolm.colson@unh.edu>",
              "Andrew Kuhlman <andrew.kuhlman@unh.edu>",
              "Christian T. Steigies <steigies@physik.uni-kiel.de>"]
__license__ = "GPL License"

import pandas as pd
import sqlalchemy
import sys

TABLE_NAMES = { "drhm": "Durham",
                "mtws": "MWO",
                "ldvl": "Leadville",
                "hela": "HLEA",
                "clmx": "Climax",
                "huan": "Huancayo"
              }

# --------------------------------------------------------------------------
def get_sql_info(info_file):
    file = open(info_file, 'r')
    lines = file.readlines()

    user = lines[0].rstrip()
    password = lines[1].rstrip()
    
    return user, password
# --------------------------------------------------------------------------
def read_rt(station, data_type, year, month, day):
    """read in data from UNH/Durham"""
    try:
        sql_user, sql_pass = get_sql_info('/Users/Malcolm/Desktop/NMDB/.psqlinfo')
        conn_string = f'postgresql://{sql_user}:{sql_pass}@localhost/Neutron Monitor'
        db = sqlalchemy.create_engine(conn_string)

        start_date = f'{year}-{month}-{day}'
        query = (f"""SELECT * 
                     FROM public."{TABLE_NAMES[station]}"
                     WHERE DATE("Timestamp") = '{start_date}';""")

        df = pd.read_sql(query, con=db)
        if df.empty is True:
            print("no DATA")
            return None

        df.rename(columns={'Timestamp': 'start_date_time',
                           'Total': 'uncorr',
                           'Corr_Total': 'corr',
                           'HP_Barometer': 'press'}, inplace=True)

        if data_type in ["1m", "ori"]:
            df['interval'] = 60.
        elif data_type in ["1h"]:
            data = data.resample('1hr', on='Timestamp').mean()
            df['interval'] = 3600.
        else:
            raise ValueError  # unknown data_type in read_pandas

        df['ceff'] = df['corr']

        return df
    except ValueError:
        return None


# --------------------------------------------------------------------------
def read_rev(station, data_type, year, month, day):
    return read_rt(station, data_type, year, month, day)

# --------------------------------------------------------------------------
if __name__ == '__main__':
    station = "drhm"
    data_type="1m"
    year = sys.argv[1]
    month = sys.argv[2]
    day = sys.argv[3]

    df = read_rev(station, data_type, year, month, day)
    df.sort_values(by = 'start_date_time', inplace = True)
    print(df.head())
