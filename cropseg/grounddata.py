#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import numpy
from osgeo import gdal
import scipy.ndimage

from mlhubdata import loadjson

def groundCropCountByTile(datasetinfo):
    groundlabels = loadjson(f'{datasetinfo["metadatadir"]}{datasetinfo["groundcollection"]}_id.json')
    groundmetadata = loadjson(f'{datasetinfo["metadatadir"]}{datasetinfo["groundcollection"]}.json')
    cropcount = numpy.zeros([len(groundmetadata),len(groundlabels)+1],dtype='int')
    for i in range(len(groundmetadata)):        
        tile = gdal.Open(f'{datasetinfo["datadir"]}{datasetinfo["groundcollection"]}/{groundmetadata[i]["id"]}/labels.{datasetinfo["extension"]}')
        tiledata = numpy.array(tile.GetRasterBand(1).ReadAsArray(),dtype="int")
        cropcount[i][len(groundlabels)] = int(groundmetadata[i]["id"].split("_")[len(groundmetadata[i]["id"].split("_"))-1])
        for j in range(len(groundlabels)):
            cropcount[i][j] = numpy.count_nonzero(tiledata == j)
    return cropcount

def getFieldMasks(tiledata,erosioniterations=0):
    crops = numpy.unique(tiledata[tiledata != 0])
    fieldmasks = [[]] * len(crops)
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
