#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import numpy
from osgeo import gdal
import datetime

def _geteoindex(data,bands,index):
    if index == "vhvv":
        vv = next(item for item in bands if item["band"] == "vv")["idx"]
        vh = next(item for item in bands if item["band"] == "vh")["idx"]
        return data[vh] - data[vv]
    if index == "ndvi":
        red = next(item for item in bands if item["band"] == "red")["idx"]
        nir = next(item for item in bands if item["band"] == "nir")["idx"]
        return (data[nir] - data[red]) / (data[nir] + data[red])
    if index == "gndvi":
        green = next(item for item in bands if item["band"] == "green")["idx"]
        nir = next(item for item in bands if item["band"] == "nir")["idx"]
        return (data[nir] - data[green]) / (data[nir] + data[green])
    if index == "gci":
        green = next(item for item in bands if item["band"] == "green")["idx"]
        nir = next(item for item in bands if item["band"] == "nir")["idx"]
        return (data[nir] / data[green]) - 1
    if index == "rdedci":
        reded1 = next(item for item in bands if item["band"] == "rded1")["idx"]
        nir = next(item for item in bands if item["band"] == "nir")["idx"]
        return (data[nir] / data[reded1]) - 1
    if index == "ndmi":
        swir1 = next(item for item in bands if item["band"] == "swir1")["idx"]
        nir = next(item for item in bands if item["band"] == "nir")["idx"]
        return (data[nir] - data[swir1]) / (data[nir] + data[swir1])

def load_satellite_data_as_array(items,bands,indices,datasetinfo,shape,rr=1):
    data = numpy.zeros([len(items),len(bands)+len(indices),shape[0],shape[1]],dtype=numpy.float32)
    for i in range(len(items)):
        imagehandle = gdal.Open(f'{datasetinfo["datadir"]}{items[i]["collection"]}/{items[i]["id"]}/source.tif')
        for j in range(len(bands)):
            data[i][j] = imagehandle.GetRasterBand(j+1).ReadAsArray() / rr
        j = j + 1
        for k in range(len(indices)):
            data[i][j+k] = _geteoindex(data[i],bands,indices[k])
    return data

def load_satellite_cloudmasks_as_array(items,datasetinfo,shape):
    data = numpy.zeros([len(items),shape[0],shape[1]],dtype=numpy.int32)
    for i in range(len(items)):
        imagehandle = gdal.Open(f'{datasetinfo["datadir"]}{items[i]["collection"]}/{items[i]["id"]}/cloudmask.tif')
        data[i] = imagehandle.GetRasterBand(1).ReadAsArray()
    return data

def cloudfreeitems(items,cloudmasks,cloudcover_max):
    cfitems = []
    cfdates = []
    for i in range(len(items)):
        if numpy.count_nonzero(cloudmasks[i] != 0) / numpy.size(cloudmasks[i]) <= cloudcover_max:
            cfitems.append(items[i])
    for i in range(len(cfitems)):
        cfdates.append(datetime.datetime.strptime(cfitems[i]["properties"]["datetime"],"%Y-%m-%dT%H:%M:%S+0000").date())
    return cfitems,cfdates
