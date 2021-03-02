#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import numpy
from osgeo import gdal

from mlhubdata import loadjson

def getEOIndicies(data,bands,idxs):
    indicies = numpy.zeros([len(data),len(idxs),numpy.shape(data[0][0])[0],numpy.shape(data[0][0])[1]])
    for i in range(len(idxs)):
        if idxs[i] == "vhvv":
            vv = next(item for item in bands if item["band"] == "vv")["idx"]
            vh = next(item for item in bands if item["band"] == "vh")["idx"]
            indicies[:,i] = data[:,vh] - data[:,vv]
        if idxs[i] == "ndvi":
            red = next(item for item in bands if item["band"] == "red")["idx"]
            nir = next(item for item in bands if item["band"] == "nir")["idx"]
            indicies[:,i] = (data[:,nir] - data[:,red]) / (data[:,nir] + data[:,red])
        if idxs[i] == "gndvi":
            green = next(item for item in bands if item["band"] == "green")["idx"]
            nir = next(item for item in bands if item["band"] == "nir")["idx"]
            indicies[:,i] = (data[:,nir] - data[:,green]) / (data[:,nir] + data[:,green])
        if idxs[i] == "gci":
            green = next(item for item in bands if item["band"] == "green")["idx"]
            nir = next(item for item in bands if item["band"] == "nir")["idx"]
            indicies[:,i] = (data[:,nir] / data[:,green]) - 1
        if idxs[i] == "rdedci":
            reded1 = next(item for item in bands if item["band"] == "rded1")["idx"]
            nir = next(item for item in bands if item["band"] == "nir")["idx"]
            indicies[:,i] = (data[:,nir] / data[:,reded1]) - 1
        if idxs[i] == "ndmi":
            swir1 = next(item for item in bands if item["band"] == "swir1")["idx"]
            nir = next(item for item in bands if item["band"] == "nir")["idx"]
            indicies[:,i] = (data[:,nir] - data[:,swir1]) / (data[:,nir] + data[:,swir1])
    return indicies

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
