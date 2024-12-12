#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find table name for station:
    kiel3 is stored in kiel2 table (merge all to kiel later...)
"""

__author__ = "Christian T. Steigies <steigies@physik.uni-kiel.de>"
__license__ = "GPL License"


def station_name(station):
    if station == "kiel3":
        value = "kiel2"
    else:
# TODO check is staion is a valid station?
        value = station

    return value

