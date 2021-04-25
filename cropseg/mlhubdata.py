#!/usr/bin/env python

import os
import json
import urllib
import datetime

def _checkfileexists(filename):
    return os.path.isfile(filename)

def _checkdirexists(dirname):
    return os.path.exists(dirname)

def _createdir(dirname):
    os.makedirs(dirname)

def _ccdir(dirname):
    if _checkdirexists(dirname) == False:
         _createdir(dirname)

def loadjson(jsonfile):
    data = []
    with open(jsonfile,'r') as fp:
        data = json.load(fp)
    return data

def get_tileitems_from_collection(tileid,metadata,datasetinfo,verbose=0):
    items = []
    dates = []
    for i in range(len(metadata)):
        if tileid in metadata[i]["id"]:
            items.append(metadata[i])
            _ccdir(f'{datasetinfo["datadir"]}{metadata[i]["collection"]}')
            _ccdir(f'{datasetinfo["datadir"]}{metadata[i]["collection"]}/{metadata[i]["id"]}')
            for j in metadata[i]["assets"]:
                if j != "documentation":
                    filename = f'{datasetinfo["datadir"]}{metadata[i]["collection"]}/{metadata[i]["id"]}/{j}.{datasetinfo["extension"]}'
                    if _checkfileexists(filename) == False:
                        urllib.request.urlretrieve(f'{metadata[i]["assets"][j]["href"]}',filename)
                        if verbose > 0:
                            print(f'Downloading: {filename}     ',end='\r')
    items = sorted(items,key=lambda k:k["properties"]["datetime"])
    for i in range(len(items)):
        dates.append(datetime.datetime.strptime(items[i]["properties"]["datetime"],"%Y-%m-%dT%H:%M:%S+0000").date())  
    if verbose > 0:
        print(f'Items for {tileid} are available                                                                                                    ')
    return items,dates
