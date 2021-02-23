#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import numpy
from osgeo import gdal

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
