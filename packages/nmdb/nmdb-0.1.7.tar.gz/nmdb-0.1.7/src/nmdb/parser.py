#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 14:10:20 2023

@author: steigies
"""

import argparse  # https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3/howto/argparse.html#argparse-tutorial

# __version__ = VERSION
__version__ = "0.1.7"
# BUG  nmdb --version prints 0.1.3

# --------------------------------------------------------------------------
def nmdb_parser():
    parser = argparse.ArgumentParser(description='NMDB commandline interface, public version.')
    parser.add_argument('--version', action='version', version='This is nmdb '+ __version__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity level')
    group.add_argument("-q", "--quiet", action="store_true")
    parser.set_defaults(cmd=None)
    
    # add subparsers!
    subparsers = parser.add_subparsers() #help='nmdb sub-commands')

    from nmdb.status import parser as parser_status
    parser_status = parser_status(subparsers)
    from nmdb.realtime import parser as parser_realtime
    parser_realtime = parser_realtime(subparsers)

    # create the parser for the "revise" command
    parser_rev = subparsers.add_parser('revise', help='revise NMDB data')
    parser_rev.add_argument('station', metavar='STATION', nargs='?', default='test', help='NMDB station short name')
    parser_rev.add_argument('data_type', choices=['1m', '1h', 'env', 'meta'], nargs='?', default='1m')
    parser_rev.add_argument('--dry-run', dest='dryrun', action="store_true", help='print but do not execute commands')
    parser_rev.add_argument('--file', dest='rcfile', help='config file for NMDB')
    parser_rev.add_argument('-H', '--host', dest='hostname', help='NMDB hostname to connect to')
    parser_rev.add_argument('-P', '--port', type=int, dest='port', default='3306', help='NMDB port number to connect to')
    parser_rev.add_argument('-Y', '--year', type=int, dest='year', help='year')
    parser_rev.add_argument('-M', '--month', type=int, dest='month', help='month')
    parser_rev.add_argument('-D', '--day', type=int, dest='day', help='day')
    group = parser_rev.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity level')
    group.add_argument("-q", "--quiet", action="store_true")
    parser_rev.set_defaults(cmd="revise")

    from nmdb.upload import parser_upload
    parser_upload = parser_upload(subparsers)
    from nmdb.download import parser_download
    parser_download = parser_download(subparsers)

    return(parser)
