#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 12:11:01 2023

@author: steigies
"""

my_station = ["kiel"]
pressure = [900., 1200.]
countrate = [10., 1000.]

def read_rt(args):
    if args.station in my_station:
        print(args.station)
    else:
        raise ValueError  # wrong station

    print("read_rt KIEL")


    return None
