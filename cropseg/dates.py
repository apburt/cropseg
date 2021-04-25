#!/usr/bin/env python

import datetime

def datepositions(dates):
    positions = []
    yearstart = datetime.date(min(dates).year,1,1)
    yearend = datetime.date(min(dates).year+1,1,1)
    duration = (yearend-yearstart).days
    for i in range(len(dates)):
        position = (dates[i]-yearstart).days / duration
        positions.append(position)
    return positions
