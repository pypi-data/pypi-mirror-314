#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""usage: python status.py -h

NMDB realtime

Copyright (C) 2008-2023 Christian T. Steigies <steigies@physik.uni-kiel.de>

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

__cmd__ = 'realtime'

# --------------------------------------------------------------------------

def parser(subparsers):
    # create the parser for the "realtime" command
    sub_p = subparsers.add_parser(__cmd__, help='get NMDB realtime data')
    group = sub_p.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity level')
    group.add_argument("-q", "--quiet", action="store_true")
    sub_p.set_defaults(cmd=__cmd__)

    return(sub_p)


# --------------------------------------------------------------------------
def realtime(args):
    """read NMDB realtime data into a pandas dataframe"""
    print(vars(args))
    if args.verbose:
        print(vars(args))
    if not args.quiet:
        print("NMDB: realtime data")

    realtime = "http://rt.nmdb.eu/realtime.txt"  # NMDB realtime data is available here    
    columns = ['timestamp', 'station', 'countrate']  # list with column names
    df = pd.read_table(realtime, comment="#", sep=";", header=0, names=columns)

    df['timestamp'] = pd.to_datetime(df['timestamp'])  # convert str to datetime
    df = df.astype({'station':'string'})
    df['countrate'] = pd.to_numeric(df['countrate'], errors='coerce')  # None -> NaN
    df.dropna(inplace=True)  # drop rows that contain NaN/None values
    if args.verbose:
        print(df)

    # create a pivot table with station names as column name
    data = df.pivot(index='timestamp', columns='station', values='countrate')
    # pivot table with max, mean, min for each station
    d3 = df.pivot_table(index='station', values='countrate', aggfunc=('mean', 'max', 'min'))
    print(d3)
    if args.verbose:
        print(data)

    return(data)


# --------------------------------------------------------------------------
def main():
    from matplotlib import pyplot as plt
    import argparse
    p = argparse.ArgumentParser(description='NMDB realtime interface.')
    # add subparsers!
    subparsers = p.add_subparsers()
    parser_realtime = parser(subparsers)

    args = p.parse_args(args=[__cmd__])
    data = realtime(args)
    print(data)
    # run this file in spyder to see the plots
    #data.plot()  # plot all the data
    #data.ATHN.plot()  # plot a single station
    #data[['ATHN', 'OULU']].plot()  # plot multiple stations

    # plt.plot(data)
    # #plt.figtext(0.15, 0.72, f"NMDB realtime data")
    # #plt.xlabel(f"$\omega$ in 1/s")
    # #plt.ylabel(f"Auslenkung in $\mu$m")
    # plt.title("NMDB realtime data")
    # #plt.legend()
    # plt.show()
    # #plt.savefig(f"Realtime.png", dpi=600)
    # plt.close()

    # calculate the mean countrate for one or several stations
    #print("mean countrate for ATHN: ", data.ATHN.mean())
    #print(data[['ATHN', 'OULU']].mean())
    #print("mean countrate:\n", data.mean())
    #print("max countrate:\n", data.max(), data.min())
    #print("min countrate:\n", data.min())
    #d2  = data.mean()
    #df2  = d2.merge(data.max())
    #d2.a = data.max()
    #d2.i = data.min()
    #print(df2)
    #print("countrate:\n", data.mean() + data.max() + data.min())
    # data = data.join(
    # data.groupby('station')['ATHN'].aggregate(['mean', 'min', 'max']),
    # on='station')
    # data["mean"]= data.groupby('statistics')['s_values'].transform('mean')
    #print(data)


# --------------------------------------------------------------------------
if __name__ == '__main__':
    main()