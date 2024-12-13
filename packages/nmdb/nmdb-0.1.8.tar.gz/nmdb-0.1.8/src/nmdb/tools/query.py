# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
def dt_start_stopp(year, month, day, hour=None):
    if month is None:
        month_min = 1
        month_max = 12
        day_min = 1
        day_max = 31
    else:
        month_min = month
        month_max = month
        if day is None:
            day_min = 1
            day_max = 31
        else:
            day_min = day
            day_max = day
            if hour is None:
                hour_min = 0
                hour_max = 23
            else:
                hour_min = hour
                hour_max = hour

    # read into dataframe
    start = "%04i-%02i-%02i %02i:00:00" % (year, month_min, day_min, hour_min)
    stopp = "%04i-%02i-%02i %02i:59:59" % (year, month_max, day_max, hour_max)

    return(start, stopp)


