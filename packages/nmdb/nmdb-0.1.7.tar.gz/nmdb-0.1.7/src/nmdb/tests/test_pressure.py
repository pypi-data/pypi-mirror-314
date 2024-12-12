#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:22:09 2024

@author: steigies
"""

import sys
import pytest

from nmdb.station import aata
from nmdb.station import drhm
from nmdb.station import kiel3

#pressure = {"aata": aata.pressure,
##            "drhm": drhm.pressure,
#            "kiel0": kiel3.pressure,
#            "kiel1": kiel3.pressure,
#            "kiel2": kiel3.pressure,
#            "kiel3": kiel3.pressure,}

pressure = kiel3.pressure
#yaata.pressure
#pressure.update(kiel3.pressure)
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
    #pressure = {"kiel3": kiel3.pressure}
    #pressure = kiel3.pressure
    # Each test case is a tuple of (input, expected_result)
    test_cases = [
        (["aata", "aata"], [900., 1100.]),
        (["kiel3", "kiel3"], [900., 1100.]),
    ]
    for my_station, expected in test_cases:
        # When
        institute = my_station[0]
        station = my_station[1]
        p_min = pressure[institute][station][0]
        p_max = pressure[institute][station][1]
        # Then
        expected_p_min = expected[0]
        expected_p_max = expected[1]
        assert p_min == expected_p_min
        assert p_max == expected_p_max

# --------------------------------------------------------------------------
if __name__ == '__main__':
    print(pressure)
    for station in ["kiel1", "kiel2", "kiel3"]:
        print(pressure[station])