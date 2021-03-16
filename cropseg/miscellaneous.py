#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import numpy

def fusedataandweight(x1,y1,x2,y2,weight=[0.1,1]):
    x = numpy.zeros(len(x1)+len(x2))
    y = numpy.zeros(len(y1)+len(y2))
    idx = numpy.zeros(len(x1),dtype=numpy.int32)
    count1 = 0
    count2 = 0
    for i in range(len(x)):
        if count1 < len(x1) and x1[count1] <= x2[count2]:
            x[i] = x1[count1]
            y[i] = y1[count1]
            idx[count1] = i
            count1 = count1 + 1
        else:
            x[i] = x2[count2]
            y[i] = y2[count2]
            count2 = count2 + 1
    weights = numpy.zeros(len(y))+weight[1]
    numpy.put(weights,idx,weight[0])
    return x,y,weights
