#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 10:38:41 2023

@author: steigies
"""

# http://wiki.python.org/moin/ConfigParserExamples
#import configparser  # python-configparser

# --------------------------------------------------------------------------
def config_section_map(section, config):
    """return configuration as dict"""

    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                # DebugPrint("skip: %s" % option)
                pass
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


