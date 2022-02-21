from json import load, dump
from os import path as osPath
from glob import glob

## Searches a directory for png images and returns it as a list
def searchFiles(directory, fileExtension):
    fileList = []

    for filename in glob(f'{directory}*.{fileExtension}'):
        fileList.append(filename)
    
    return fileList

## loads a dictonary from a json file
def loadData(directory):
    with open(directory, 'r') as jsonFile:
        return load(jsonFile)

## Save's a dictonary in a json file
def saveData(directory, data, indent = 3):
    with open(directory, 'w') as jsonFile:
        dump(data, jsonFile, indent=indent)


## Return filename from path
def getFilename(path):
    return osPath.basename(path).split(".", 1)[0]