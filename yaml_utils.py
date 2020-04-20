#! /usr/bin/env python3

# This library requires pyyaml to be installed,
# "pip3 install pyyaml"
# 
# I have not bothered to do any validation of paths being valid
# 
# Magne Sirnes, 18th April 2020

import yaml

# ------ HIGH LEVEL FUNCTIONS ------

# apply updates to an existing yaml file,
# resulting file is saved in newFilePath,
# if not provided, old file is overwritten
# updateDict should look like:
# d = {
#   "Camera": {
#     "fps": 30
#   }
# } etc..
def updateExistingFile(updateDict, oldFilePath:str, newFilePath:str=""):
    oldDict = readDictFromFile(oldFilePath)
    newDict = mergeIntoDict(oldDict, updateDict)
    if newFilePath == "":
        newFilePath = oldFilePath
    dumpToFile(newDict, newFilePath)

# Creates a default YAML file, using params found in make*SubDict functions
def createDefaultYamlFile(filePath:str="config.yaml"):
    dumpToFile(makeBaseDict(),filePath)

# ------ LOW LEVEL FUNCTIONS ------

def makeCamSubDict():
    return {
        "Camera": {
            "fx": 646,
            "fy": 486,
            "cx": 960,
            "cy": 540,
            "k1": 0,
            "k2": 0,
            "k3": 0,
            "p1": 0,
            "p2": 0,
            "fps": 30,
            "RGB": 1
        }
    }

def makeORBextractorSubDict():
    return {
        "ORBextractor": {
            "nFeatures": 1000,
            "scaleFactor": 1.2,
            "nLevels": 8,
            "iniThFAST": 20,
            "minThFAST": 7
        }
    }

def makeViewerSubDict():
    return {
        "Viewer": {
            "KeyFrameSize": 0.05,
            "KeyFrameLineWidth": 1,
            "GraphLineWidth": 0.9,
            "PointSize": 2,
            "CameraSize": 0.08,
            "CameraLineWidth": 3,
            "ViewpointX": 0,
            "ViewpointY": -0.7,
            "ViewpointZ": -1.8,
            "ViewpointF": 500
        }
    }

def makeBaseDict():
    baseobj = { **flattenDict(makeCamSubDict()),
        **flattenDict(makeORBextractorSubDict()),
        **flattenDict(makeViewerSubDict())
    }
    return baseobj

def readDictFromFile(filePath:str):
    f = open(filePath,"r")
    if f.readline() == "%YAML:1.0\n":
        myDict = yaml.load(f)
    else:
        myDict = {}
    f.close()
    return myDict

def dumpToFile(myDict, filePath:str):
    f = open(filePath,"w")
    f.write("%YAML:1.0\n\n")
    yaml.dump(myDict, f)
    f.close()

# returns a new dict, with all elements of newDict added to oldDict
# where elements in oldDict already exist, 
# these are overwritten by values in newDict
def mergeIntoDict(oldDict, newDict):
    return {**oldDict, **flattenDict(newDict)}

def flattenDict(deepDict):
    d = {}
    for k1 in deepDict:
        for k2 in deepDict[k1]:
            d[k1 + "." + k2] = deepDict[k1][k2]
    return d

if __name__ == "__main__":
    #createDefaultYamlFile("test.yaml")
    updateExistingFile({"Camera":{"fps":60}}, "test.yaml")