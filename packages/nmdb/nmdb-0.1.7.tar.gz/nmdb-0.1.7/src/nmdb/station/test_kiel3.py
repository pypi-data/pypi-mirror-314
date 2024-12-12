#!/usr/bin/pytest-3 -v
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 14:20:57 2021

@author: steigies

upgrade to python3-tz_2023.3.post1-2_all.deb to get rid of annoying warning
"""

from __future__ import annotations
from typing import Any, Callable

import pytest
#import numpy as np
import pandas as pd
from kiel3 import p_parser, median_editor, tube2ch


# --------------------------------------------------------------------------
def setup_module(module: Any) -> None:
    print(f"setting up MODULE {module.__name__}")


# --------------------------------------------------------------------------
def teardown_module(module: Any) -> None:
    print(f"tearing down MODULE {module.__name__}")


# --------------------------------------------------------------------------
def test_tube2ch() -> None:
    # Given
    station = "kiel"
    # Each test case is a tuple of (input, expected_result)
    test_cases = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 10),
        (8, 11),
        (9, 12),
        (10, 13),
        (11, 14),
        (12, 15),
        (13, 18),
        (14, 19),
        (15, 20),
        (16, 21),
        (17, 22),
        (18, 23),
    ]
    for tube, expected in test_cases:
        # When
        output = tube2ch(station, tube)
        # Then
        assert output == expected


# --------------------------------------------------------------------------
def test_tube2_out_of_bounds():
    # Given
    station = "kiel"
    # Each test case is a tuple of (input, expected_result)
    test_cases = [
        (-1, ValueError),
        (0, ValueError),
        (19, ValueError),
        (24, ValueError),
    ]
    for tube, expected in test_cases:
        with pytest.raises(expected):
            print(tube, expected)
            tube2ch(station, tube)


# --------------------------------------------------------------------------
def test_tube2_not_kiel():
    # Given
    station = "oulu"
    # Each test case is a tuple of (input, expected_result)
    test_cases = [
        (-1, ValueError),
        (0, ValueError),
        (1, ValueError),
        (2, ValueError),
        (17, ValueError),
        (18, ValueError),
        (19, ValueError),
        (24, ValueError),
    ]
    for tube, expected in test_cases:
        with pytest.raises(expected):
            tube2ch(station, tube)


# --------------------------------------------------------------------------
def test_p_parser() -> None:
    # Given
    # Each test case is a tuple of (input, expected_result)
    test_cases = [
        (1013.1, 1013.1),                        # very old format: float
        (":BM35:991.55:", 991.55),               # old format
        (":BM35:991.58:BM35b:991.40:", 991.58),  # format since 2023-10
        (":BM35:1017.61:GB1:0.0:", 1017.61),     # format since 2024-01-08
        (":BM35:977.37:BM35b:977.19:", 977.37),  #
    ]
    for pressure, expected in test_cases:
        # When
        output = p_parser(pressure)
        #print("test:", pressure, expected, output)
        # Then
        assert output == expected


# --------------------------------------------------------------------------
def test_median():
    # Given
    ts = pd.to_datetime("2023-06-12 23:56:05")

    channel = []
    for i in range(0, 24):
        channel.append("ch%02i" % (i))
    channel.append("p_bm35")

    data1 = [0, 10, 20, 30, 40, 50, 60, 70,
            600, 601, 602, 603, 604, 605, 606, 607,
            2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 1013.1]

    # RuntimeWarning: All-NaN slice encountered
    data2 = [0, 1, 2, 3, 4, 5, 6, 7,
             0, 1, 2, 3, 4, 5, 6, 7,
             2, 3, 4, 5, 6, 7, 8, 9, 1013.1]

    row = pd.Series(data=data2, index=channel)
    print("row:", row)
    print(median_editor(ts, row))


# --------------------------------------------------------------------------
def notest_median() -> None:
    ts = pd.to_datetime("2023-06-12 23:56:05")

    channel = []
    for i in range(1, 18+1):
        channel.append("ch%02i" % (i))
    channel.append("p_bm35")
    # append integration?
    print(channel)

    # Each test case is a tuple of (input, expected_result)
    test_cases = [([600, 600, 600, 600, 600, 600,
                    600, 600, 600, 600, 600, 600,
                    600, 600, 600, 600, 600, 600,
                    ":BM35:1017.61:GB1:0.0:"], 600.),
                  ]

    for data_in, expected in test_cases:
        data = pd.Series(data=data_in, index=channel)
        print(data)
        # When
        output = median_editor(ts, data_in)
        # Then
        assert output == expected


