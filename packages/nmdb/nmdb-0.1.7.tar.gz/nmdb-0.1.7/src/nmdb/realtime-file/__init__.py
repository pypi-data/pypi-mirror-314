import pandas as pd


def main():
    """read NMDB realtime data into a pandas dataframe"""
    print("NMDB: realtime data")

    realtime = "http://rt.nmdb.eu/realtime.txt"  # NMDB realtime data is available here    
    columns = ['timestamp', 'station', 'countrate']  # list with column names
    df = pd.read_table(realtime, comment="#", sep=";", header=0, names=columns)

    df['timestamp'] = pd.to_datetime(df['timestamp'])  # convert str to datetime
    df = df.astype({'station':'string'})
    df['countrate'] = pd.to_numeric(df['countrate'], errors='coerce')  # None -> NaN
    df.dropna(inplace=True)  # drop rows that contain NaN/None values
    print(df)

    # create a pivot table with station names as column name
    data = df.pivot(index='timestamp', columns='station', values='countrate')

    # run this file in spyder to see the plots
    data.plot()  # plot all the data
    data.ATHN.plot()  # plot a single station
    data[['ATHN', 'OULU']].plot()  # plot multiple stations

    # calculate the mean countrate for one or several stations
    print("mean countrate for ATHN: ", data.ATHN.mean())
    print(data[['ATHN', 'OULU']].mean())
    print("mean countrate:\n", data.mean())


if __name__ == '__main__':
    print("To use this file as starting point for your own script, copy __init.py__ to a new place and edit it to your liking:")
    print("cp ~/.local/lib/python3.9/site-packages/nmdb_realtime/__init__.py /tmp/realtime.py")
    print("\n")

    main()
