#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:55:54 2023

@author: steigies

https://stackoverflow.com/questions/14745022/how-to-split-a-dataframe-string-column-into-two-columns
"""

import pandas as pd

def main():
    df = pd.DataFrame({'AB': [':BM35:989.46:BM35b:989.28:', ':BM35:989.43:BM35b:989.25:',
                          ':BM35:1004.7:', ':BM35:1028.32:GB1:0.0:']})

    for index, row in df.iterrows():
        #print(row[0])
        #p_bm35 = pressure(row[0])
        p_bm35 = press_parse(row[0], "BM35")
        #p_bm = p_bm35(row['p_bm35'])
        print(p_bm35)
        print()

#df['AB_split'] = df['AB'].str.split('BM35')
#print(df)

def pressure(bm35):
    """find :BM35: in string. Numbers until next : are p_bm35"""
    p_bm35 = None
    head = bm35.find(":BM35:")
    if head >= 0:
        tail = bm35[head+6:].find(":")
        p_bm35 = float(bm35[head+6:tail+6])

    return p_bm35

    
def press_parse(press, key):
    print(press, key)

    value = 0.  # no pressure, store as 0
    if isinstance(press, float):  # until 2022 a single BM35 value was used
        value = float(press)
    else:
        pressure = {}
        if press[0] == ":":  # several key:value pairs are stored
            data = press.split(":")
            keyword = data.pop(0)  # pop off first ":"
            while len(data) > 1:  # need two values: keyword and value
                keyword = data.pop(0)
                value = data.pop(0)
                pressure[keyword] = value

        #print(pressure, key, pressure[key])
        try:
            value = pressure[key]  # return pressure for the given key
        except KeyError:  # return 0 if key not found
            value = 0.

    return value


# --------------------------------------------------------------------------
if __name__ == '__main__':
    main()