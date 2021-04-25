#!/usr/bin/env python

import numpy

def rgbcomposite(image,bands):
    red = next(item for item in bands if item["band"] == "red")["idx"]    
    green = next(item for item in bands if item["band"] == "green")["idx"]    
    blue = next(item for item in bands if item["band"] == "blue")["idx"]    
    rgb = numpy.dstack((image[red],image[green],image[blue]))    
    return rgb

def fieldmask_colrowcount(fieldmasks):
    ncol = nrow = 0
    for i in range(len(fieldmasks)):
        if fieldmasks[i][1] > 0:
            ncol = ncol + 1
        if fieldmasks[i][1] > nrow:
            nrow = fieldmasks[i][1]
    return ncol,nrow
