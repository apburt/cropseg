#!/usr/bin/env python

import numpy
import scipy.optimize
import scipy.fftpack

def _dbllogifunc_initialguess(x,y,x01=0.2,k1=10.0,x02=0.8,k2=-15.0):
    A1 = numpy.min(y)
    A2 = numpy.max(y)-numpy.min(y)
    return A1,A2,x01,k1,x02,k2

def dbllogifunc(x,A1,A2,x01,k1,x02,k2):
    return A1+A2*(1./(1+numpy.exp(-k1*(x-x01)))-1./(1+numpy.exp(k2*(x-x02))))

def doublelogistic(x,y,weights=None,bound=True,epsilon=0.1):    
    A1,A2,x01,k1,x02,k2 = _dbllogifunc_initialguess(x,y)
    if bound == False:
        popt,pcov = scipy.optimize.curve_fit(dbllogifunc,x,y,p0=[A1,A2,x01,k1,x02,k2],sigma=weights,method='lm',maxfev=1000000)
        return popt
    if bound == True:
        popt,pcov = scipy.optimize.curve_fit(dbllogifunc,x,y,p0=[A1,A2,x01,k1,x02,k2],sigma=weights,method='trf',maxfev=1000000,bounds=((A1-epsilon,A2-epsilon,0,0,0,-numpy.inf),(A1+epsilon,A2+epsilon,1,numpy.inf,1,0)))
        return popt

def doublelogistic_fittingconditions(x,y,durationmin=0.9,gapmax=0.3,amplitudemin=0.25):
    if numpy.max(x)-numpy.min(x) <= durationmin:
        return False
    if numpy.max(numpy.diff(x)) >= gapmax:
        return False
    if numpy.max(y)-numpy.min(y) <= amplitudemin:
        return False
    return True

def doublelogistic_parameterconditions(parameters,A1min=0.05,A1max=0.25,A2min=0.30,A2max=0.80,x01min=0.50,x01max=0.70,k1min=5.0,k1max=50.0,x02min=0.80,x02max=0.95,k2min=-50.0,k2max=-10.0):
    A1,A2,x01,k1,x02,k2 = parameters
    if A1 >= A1min and A1 <= A1max:
        if A2 >= A2min and A2 <= A2max:
            if x01 >= x01min and x01 <= x01max:
                if k1 >= k1min and k1 <= k1max:
                    if x02 >= x02min and x02 <= x02max:
                        if k2 >= k2min and k2 <= k2max:
                            return True
    return False

def dct(y,ncoeff):
    dctcoeff = scipy.fftpack.dct(y,norm="ortho",type=2)
    return dctcoeff[:ncoeff]

def idct(coeff,ncoeff):
    threshold = numpy.zeros(len(coeff))
    threshold[:ncoeff] = 1
    coeff = coeff * threshold
    return scipy.fftpack.idct(coeff,norm="ortho",type=2)

def dct_fittingconditions(x,y,minduration=0.9,maxgap=0.3):
    if numpy.max(x)-numpy.min(x) <= minduration:
        return False
    if numpy.max(numpy.diff(x)) >= maxgap:
        return False
    return True
