#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import numpy
import scipy.optimize

def _dbllogifunc_initialguess(x,y,x01=0.2,k1=10,x02=0.8,k2=10,delta=0.2):
    A1 = numpy.min(y)
    A2 = numpy.max(y)-numpy.min(y)
    return A1,A2,x01,k1,x02,k2

def dbllogifunc(x,A1,A2,x01,k1,x02,k2):
    return A1+A2*(1./(1+numpy.exp(-k1*(x-x01)))-1./(1+numpy.exp(-k2*(x-x02))))

def fitdoublelogistic(x,y,bound=True,epsilon=0.1):
    A1,A2,x01,k1,x02,k2 = _dbllogifunc_initialguess(x,y)
    if bound == False:
        popt,pcov = scipy.optimize.curve_fit(dbllogifunc,x,y,p0=[A1,A2,x01,k1,x02,k2],method='lm',maxfev=1000000)
        return popt
    if bound == True:
        popt,pcov = scipy.optimize.curve_fit(dbllogifunc,x,y,p0=[A1,A2,x01,k1,x02,k2],method='trf',maxfev=1000000,bounds=((A1-epsilon,A2-epsilon,0,0,0,0),(A1+epsilon,A2+epsilon,1,numpy.inf,1,numpy.inf)))
        return popt

def doublelogistic_conditions(x,y,minduration=0.9,maxgap=0.3,minamplitude=0.25):
    if numpy.max(x)-numpy.min(x) <= minduration:
        return False
    if numpy.max(numpy.diff(x)) >= maxgap:
        return False
    if numpy.max(y)-numpy.min(y) <= minamplitude:
        return False
    return True
