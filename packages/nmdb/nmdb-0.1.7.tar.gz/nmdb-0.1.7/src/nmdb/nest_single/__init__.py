import datetime as dt
import pandas as pd

# local library that generates the html strings to download NEST data
from nmdb import nest


def main():
    """read data for a single station with NEST into a dataframe"""
    print("NMDB: NEST download tool for a single station")

    start = dt.datetime(2022, 2, 1, 0, 0, 0)
    end = dt.datetime(2022, 2, 28, 23, 59, 59)
    table = "revori"  # virtual table with merge original and revised data

    station = "oulu"  # station short name as used in NMDB
    data = ["p", "u", "c", "e"]  # download pressure, uncorrected, corrected (for pressure) and efficiency corrected data

    download = nest.single(station, table, data, start, end)
    # the download string for the data we selected
    print(download)

    names = data.copy()  # keep the original columns, work only with a copy
    names.insert(0, "start_date_time")
    print(names)
    df = pd.read_table(download, sep=";", comment="#", header=0, names=names)
    print(df)

    # Select only data with very high pressure
    print(df[df['p'] > 1025])

    # Select only data with very low pressure
    print(df[df['p'] < 965])

    df.plot(y=["p"])
    df.plot(y=["u", "e"])

    # Row numbers as x-axis looks ugly, lets use the date instead
    df.index = pd.to_datetime(df['start_date_time'])
    df.plot(y=["u", "c"])


if __name__ == '__main__':
    print("To use this file as starting point for your own script, copy __init.py__ to a new place and edit it to your liking:")
    print("cp ~/.local/lib/python3.9/site-packages/nmdb_nest_single/__init__.py /tmp/single.py")
    print("\n")

    main()
