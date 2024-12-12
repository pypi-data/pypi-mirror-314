#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:22:09 2024

@author: steigies
"""

from __future__ import annotations
from typing import Any, Callable

#import pytest
import pandas as pd
#import sys

#from nmdb.tools.query import dt_start_stopp
from query import dt_start_stopp

# --------------------------------------------------------------------------
def setup_module(module: Any) -> None:
    print(f"setting up MODULE {module.__name__}")


# --------------------------------------------------------------------------
def teardown_module(module: Any) -> None:
    print(f"tearing down MODULE {module.__name__}")


# --------------------------------------------------------------------------
#def test_simple_skip() -> None:
#    if sys.platform != "ios":
#        pytest.skip("Test works only on ios")


# --------------------------------------------------------------------------
def test_dt_start_stopp():
    # Given
    #station = "kiel2"
    # Each test case is a tuple of (input, expected_result)
    test_cases = [
        ([2011, 1, 1], ["2011-01-01 00:00:00", "2011-01-01 23:59:59"]),
        ([2011, 1, None], ["2011-01-01 00:00:00", "2011-01-31 23:59:59"]),
        ([2011, None, None], ["2011-01-01 00:00:00", "2011-12-31 23:59:59"]),
    ]
    for date, expected in test_cases:
        # When
        year = date[0]
        month = date[1]
        day = date[2]
        (start, stopp) = dt_start_stopp(year, month, day)
        # Then
        expected_start = expected[0]
        expected_stopp = expected[1]
        assert start == expected_start
        assert stopp == expected_stopp



