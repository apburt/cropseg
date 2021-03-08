#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import numpy

def rgbcomposite(image,bands):
    red = next(item for item in bands if item["band"] == "red")["idx"]    
    green = next(item for item in bands if item["band"] == "green")["idx"]    
    blue = next(item for item in bands if item["band"] == "blue")["idx"]    
    rgb = numpy.dstack((image[red],image[green],image[blue]))    
    return rgb
