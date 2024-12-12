#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:22:09 2024

@author: steigies
"""

import sys
import pytest

from nmdb.station import kiel3

# --------------------------------------------------------------------------
#def setup_module(module: Any) -> None:
#    print(f"setting up MODULE {module.__name__}")
    #realtime = {"kiel3": kiel3.read_rt}
    #revised = {"kiel3": kiel3.read_rev}
    #pressure = {"kiel3": kiel3.pressure}
    #countrate = {"kiel3": kiel3.countrate}


# --------------------------------------------------------------------------
#def teardown_module(module: Any) -> None:
#    print(f"tearing down MODULE {module.__name__}")



# --------------------------------------------------------------------------
def test_pressure():
    # Given
    # test double index as in upload
    pressure = {"kiel3": kiel3.pressure}
    #pressure = kiel3.pressure
    # Each test case is a tuple of (input, expected_result)
    test_cases = [
        (["kiel3"], [900., 1100.]),
    ]
    for my_station, expected in test_cases:
        # When
        my_station = "kiel3"
        p_min = pressure[my_station][my_station][0]
        p_max = pressure[my_station][my_station][1]
        #p_min = pressure[my_station][0]
        #p_max = pressure[my_station][1]
        # Then
        expected_p_min = expected[0]
        expected_p_max = expected[1]
        assert p_min == expected_p_min
        assert p_max == expected_p_max


# --------------------------------------------------------------------------
def test_countrate():
    # Given
    countrate = {"kiel3": kiel3.countrate}
    # Each test case is a tuple of (input, expected_result)
    test_cases = [
        (["kiel3"], [60., 6000.]),
    ]
    for my_station, expected in test_cases:
        # When
        my_station = "kiel3"
        c_min = countrate[my_station][my_station][0]
        c_max = countrate[my_station][my_station][1]
        # Then
        expected_c_min = expected[0]
        expected_c_max = expected[1]
        assert c_min == expected_c_min
        assert c_max == expected_c_max
