#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import datetime

def datepositions(dates):
    positions = []
    yearstart = datetime.date(min(dates).year,1,1)
    yearend = datetime.date(min(dates).year,12,31)
    duration = (yearend-yearstart).days
    for i in range(len(dates)):
        position = (dates[i]-yearstart).days / duration
        positions.append(position)
    return positions
