#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import os
import json
import urllib

def _checkfileexists(filename):
    return os.path.isfile(filename)

def _checkdirexists(dirname):
    return os.path.exists(dirname)

def _createdir(dirname):
    os.makedirs(dirname)

def _sortdir(dirname):
    if _checkdirexists(dirname) == False:
        _createdir(dirname)

def loadjson(jsonfile):
    data = []
    with open(jsonfile,'r') as fp:
        data = json.load(fp)
    return data

def getItemFromCollection(item,collection,datasetinfo):
    metadata = loadjson(f'{datasetinfo["metadatadir"]}{collection}.json')
    labelmetadata = []
    for i in range(len(metadata)):
        if item in metadata[i]["id"]:
            labelmetadata.append(metadata[i])
            _sortdir(f'{datasetinfo["datadir"]}{metadata[i]["collection"]}')
            _sortdir(f'{datasetinfo["datadir"]}{metadata[i]["collection"]}/{metadata[i]["id"]}')
            for key in metadata[i]["assets"]:
                if key != "documentation":
                    filename = f'{datasetinfo["datadir"]}{metadata[i]["collection"]}/{metadata[i]["id"]}/{key}.{datasetinfo["extension"]}'
                    if _checkfileexists(filename) == False:
                        urllib.request.urlretrieve(f'{metadata[i]["assets"][key]["href"]}',filename)
                        print(f'Downloading: {filename}     ',end='\r')
    print(f'Items for {metadata[i]["collection"]}_{item} are available                                                          ')
    return labelmetadata
