#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import datetime

def datepositions(dates,yearstart=False):
    positions = []
    if yearstart == False:
        startdate = min(dates)
    else:
        startdate = datetime.date(min(dates).year,1,1)
    for i in range(len(dates)):
        positions.append((dates[i]-startdate).days+1)
    return positions
