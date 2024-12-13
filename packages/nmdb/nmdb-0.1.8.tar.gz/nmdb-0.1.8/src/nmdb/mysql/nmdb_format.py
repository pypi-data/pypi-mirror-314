#! /usr/bin/env python3
"""NMDB database table formats

Copyright (c) 2011-2019 Christian T. Steigies <steigies@physik.uni-kiel.de>

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


__all__ = ["ori_format", "rev_format", "hour_format", "meta_format"]

## --------------------------------------------------------------------------

ori_format = (
    "start_date_time, "
    "length_time_interval_s, "
    "measured_uncorrected, "
    "measured_corr_for_efficiency, "
    "measured_corr_for_pressure, "
    "measured_pressure_mbar"
    )

rev_format = (
    "start_date_time, "
    "length_time_interval_s, "
    "revised_uncorrected, "
    "revised_corr_for_efficiency, "
    "revised_corr_for_pressure, "
    "revised_pressure_mbar, "
    "version"
    )

hour_format = (
    "start_date_time, "
    "uncorrected, "
    "corr_for_efficiency, "
    "corr_for_pressure, "
    "pressure_mbar"
    )

meta_format = (
    "start_date_time, "
    "end_date_time, "
    "quality_flag, "
    "comment, "
    "ID_RECORD"
    )

def env_format():    
    """format of the NMDB env tables"""
    return None

## --------------------------------------------------------------------------

if __name__ == "__main__":
    print("This is the nmdb format helper module.")
