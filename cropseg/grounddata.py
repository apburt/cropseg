#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import numpy
from osgeo import gdal
import scipy.ndimage

def tilecropcount(datasetinfo,groundlabels,groundmetadata):
    cropcount = numpy.zeros([len(groundmetadata),len(groundlabels)+1],dtype=numpy.int32)
    for i in range(len(groundmetadata)):
        tilehandle = gdal.Open(f'{datasetinfo["datadir"]}{datasetinfo["groundcollection"]}/{groundmetadata[i]["id"]}/{datasetinfo["groundname"]}')
        tiledata = numpy.array(tilehandle.GetRasterBand(1).ReadAsArray(),dtype=numpy.int32)
        cropcount[i][len(groundlabels)] = int(groundmetadata[i]["id"].split("_")[len(groundmetadata[i]["id"].split("_"))-1])
        for j in range(len(groundlabels)):
            cropcount[i][j] = numpy.count_nonzero(tiledata == j)
    return cropcount

def erodedfieldmasks(tiledata,erosioniterations=0):
    crops = numpy.unique(tiledata[tiledata != 0])
    fieldmasks = [[] for _ in range(len(crops))]
    cstructure = [[1,1,1],
                  [1,1,1],
                  [1,1,1]]
    for i in range(len(crops)):
        data = numpy.copy(tiledata)
        data[data != crops[i]] = 0
        if erosioniterations > 0:
            erosionmask = scipy.ndimage.binary_erosion(data,iterations=erosioniterations)
            data[erosionmask == False] = 0
        fields = scipy.ndimage.label(data,structure=cstructure)
        fieldmasks[i] = fields
    return fieldmasks
