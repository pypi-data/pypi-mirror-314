# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
def dt_start_stopp(year, month, day):
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
    # read into dataframe
    start = "%04i-%02i-%02i 00:00:00" % (year, month_min, day_min)
    stopp = "%04i-%02i-%02i 23:59:59" % (year, month_max, day_max)

    return(start, stopp)


