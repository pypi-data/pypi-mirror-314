import datetime as dt
import pandas as pd

# local library that generates the html strings to download NEST data
from nmdb import nest


def main():
    """read data for multiple stations with NEST into a dataframe"""
    print("NMDB: NEST download tool for multiple stations")

    start = dt.datetime(2022, 1, 1, 0, 0, 0)
    end = dt.datetime(2022, 1, 2, 23, 59, 59)
    # NEST returns stations sorted alphabetically!
    station = sorted(["oulu", "kiel2", "jung"])
    # only one data type for multiple stations
    data = "e"
    table = "revori"
    download = nest.multi(station, table, data, start, end)
    print(download)
    header = nest.header(download)
    print(header)

    names = station.copy()
    names.insert(0, "start_date_time")
    df = pd.read_table(download, sep=";", comment="#", header=0, names=names)
    print(df)
    df.plot()

    df.index = pd.to_datetime(df['start_date_time'])
    df.plot()

    df[df['start_date_time'] > "2022-01-02"].plot()

    df[(df['start_date_time'] > "2022-01-02") & (df['start_date_time'] < "2022-01-02 12:00:00") ].plot()

    df[(df['start_date_time'] > "2022-01-02") & (df['kiel2'] < 181) ].plot()

    df[(df['start_date_time'] > "2022-01-02") & (df['kiel2'] < 181) ]



if __name__ == '__main__':
    print("To use this file as starting point for your own script, copy __init.py__ to a new place and edit it to your liking:")
    print("cp ~/.local/lib/python3.9/site-packages/nmdb_nest_multi/__init__.py /tmp/multi.py")
    print("\n")

    main()
