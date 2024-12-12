# Access the Neutron Monitor database with python

![NMDB Logo](https://www.nmdb.eu/img/nmdb-6.png "NMDB")

This package provides python functions to access data from the
[Neutron Monitor database][nmdb].

# Installation

You can install directly from PyPI using
```
pip install nmdb
```

# Spyder
To run scripts and modules directly from the spyder IDE, use the PYTHONPATH manager
- disable system PYTHONPATH
- add user path with <PROJECT>/src

# Usage

- `nmdb_realtime` is an example to access realtime data,
as presented in a [tutorial][realtime] at the [NMDB hybrid conference in 2022][conf2022].

- `nmdb_nest_single` and `nmdb_nest_multi` are examples to get data from the
[NEST][nest] interface into a pandas dataframe.
These examples use the nest module from the nmdb package to generate html strings to query NEST.

- `nmdb_conf2022` is the script that creates the coverpage plot for the 2022 NMDB conference.
The plot shows GLE70 data as downloaded from NMDB
(with the data header manually edited so that the data can be read easily with pandas).
The plots are created using seaborn.

- `nmdb` is the commandline tool that allows stations to upload real-time and revised data to NMDB.
It uses several subcommands for the different operations.
nmdb as well as the subcommands provide a help function (-h) for complete usage information.
  -   status (not yet implemented):
  get station status from NMDB
  -   realtime (not yet implemented):
  get real-time data from NMDB
  -   `nmdb upload [STATION] [1m|1h|env|meta]` : upload real-time data for STATION
   This subcommand finds the last value of the STATION that is stored in NMDB
   and reads in up to two full days of data that is to be uploaded:
   data for the date of the last value in NMDB,
   and data for the following day that data is available for
   (in case of data gaps, this is not necessarily the next day).
   The data can be stored in files locally, in a database, or at an FTP or webserver.
   The subcommand does not read in data from the future (which must not exist).
   Data is read by the function `read_rt` that is provided by the module station/STATION.py
   which takes the station name (a module may provide a read_rt function for several stations),
   data_type (1m, 1h, optionally also env and meta) and the date (year, month, day) as argument.
   Since the upload script is supposed to be run typically every minute by a cron job,
   by default a maximum of 120 values are sent.
   Also the script is terminated after 30 seconds.
   Both values can by modified by options,
   but the user has to ensure that only one upload script at a time runs for any station.
   A further option allows to define a start date
   (needed if no data for a station is present in NMDB yet).
   Large amounts of data should be sent with `revise` using sqlitefiles
   (which can also be sent from Kiel to reduce latency).

  -   `nmdb station2sql [STATION] [1m|1h|env|meta]` (not yet converted):
   creates a sqlite file for STATION which can be used by revise.
   Time period (month, year) needs to be given as option.
   Data is read by the function `read_rev` that is provided by station/STATION.py
   which takes the data_type and the date (year, month, day) as argument.
   This function can use the same function as `read_rt` if no separate revised data is available.

  -   `nmdb revise [STATION] [1m|1h|env|meta]` (not yet converted):
   revises data in NMDB by comparing revised data in sqlite file with data present in NMDB.
   Data that is new or different is replaced in NMDB,
   with the version number increased appropriately.
   Data is buffered and sent in bunches of 12 (default value) to speed up ingestion into NMDB (updating indexes).

   All subcommands/modules can be executed stand-alone with the help of the special name `__main__`.
   When a module is executed stand-alone
   it should perform some tests
   and/or provide examples on how the module is used.
   This code is not executed when the module is imported by the main program.

All station modules must provide the `read_rt` and `read_rev` functions and they only use the arguments
 `station` (station short name),
 `data_type` (1m, 1h [, env, meta]),
 `year`, `month`, `day`.
Any further arguments must be optional (ie predefined, used for testing only)
 and are not used when called from a subcommand.
The module returns a dataframe of the data for the given date in NMDB format
 or `None` if no data is available or the date is invalid.
In addition they must provide a list called `my_station` with the official NMDB short names of the stations
 that this module can be used for.
The dictionary `my_names` maps those stations to the NMDB table names (uppercase of the station name).
The dictionary `my_station_longnames` maps the station short name to the full name of the station.
The two lists `pressure` and `countrate` have the minimum and maximum acceptable values
 for pressure and countrate of the stations
 (TODO: how to handle different ranges for multiple stations??? pressure[STATION]? ifthen based on station?).
Any further functions and variables in STATION.py are only to be used internally by the module
 (ie reading raw data, editing for missing tubes, pressure and efficiency correction,
 if the data is not already provided with all corrections).

--- 

[nmdb]: https://nmdb.eu
[realtime]: https://conf2022.nmdb.eu/abstract/s6/steigies/
[conf2022]: https://conf2022.nmdb.eu
[nest]: https://www.nmdb.eu/nest/

