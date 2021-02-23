#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import datetime

def datepositions(dates):
    positions = []
    startdate = min(dates)
    for i in range(len(dates)):
        positions.append((dates[i]-startdate).days)
    return positions
