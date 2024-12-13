#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""usage: python upload3.py -v -f nmdbrc newk ori|1h

NMDB upload3: upload real-time data for all stations, python3/pandas version

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


def parser_download(subparsers):
    # create the parser for the "down" command
    sub_p = subparsers.add_parser('download', help='download from NMDB')
    sub_p.add_argument('station', metavar='STATION', nargs='?', default='test', help='NMDB station short name')
    sub_p.add_argument('data_type', choices=['1m', '1h', 'env', 'meta'], nargs='?', default='1m')
    sub_p.add_argument('--dry-run', dest='dryrun', action="store_true", help='print but do not execute commands')
    sub_p.add_argument('--file', dest='rcfile', help='config file for NMDB')
    sub_p.add_argument('-H', '--host', dest='hostname', help='NMDB hostname to connect to')
    sub_p.add_argument('-P', '--port', type=int, dest='port', default='3306', help='NMDB port number to connect to')
    sub_p.add_argument('-Y', '--year', type=int, dest='year', help='year')
    sub_p.add_argument('-M', '--month', type=int, dest='month', help='month')
    sub_p.add_argument('-D', '--day', type=int, dest='day', help='day')
    group = sub_p.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity level')
    group.add_argument("-q", "--quiet", action="store_true")
    sub_p.set_defaults(cmd="download")

    return(sub_p)


# --------------------------------------------------------------------------
def download(args):
    pass


# --------------------------------------------------------------------------
if __name__ == '__main__':
    from nmdb.parser import nmdb_parser
    parser = nmdb_parser()

    test = 'download kiel 1m --dry -Y 2023 -M 1'
    test = 'download oulu 1h --dry -Y 1999 -M 12'

    args = parser.parse_args(args=test.split())
    print(vars(args))
    download(args)
