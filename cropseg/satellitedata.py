#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import numpy
from osgeo import gdal

from mlhubdata import loadjson

def cloudFreeS2Items(items,cloudcovermax,datasetinfo):
    cfitems = []
    for i in range(len(items)):
        tile = gdal.Open(f'{datasetinfo["datadir"]}{datasetinfo["s2collection"]}/{items[i]["id"]}/cloudmask.{datasetinfo["extension"]}')
        tiledata = tile.GetRasterBand(1).ReadAsArray()
        if numpy.count_nonzero(tiledata != 0) / numpy.size(tiledata) <= cloudcovermax:
            cfitems.append(items[i])
    return cfitems

def rgbComposite(item,datasetinfo):
    tile = gdal.Open(f'{datasetinfo["datadir"]}{datasetinfo["s2collection"]}/{item["id"]}/source.{datasetinfo["extension"]}')
    r = numpy.array(tile.GetRasterBand(3).ReadAsArray()) / 4096.
    g = numpy.array(tile.GetRasterBand(2).ReadAsArray()) / 4096.
    b = numpy.array(tile.GetRasterBand(1).ReadAsArray()) / 4096.
    rgb = numpy.dstack((r,g,b))
    return rgb
