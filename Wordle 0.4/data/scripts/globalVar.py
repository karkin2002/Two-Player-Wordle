from data.scripts.UI.printInfo import printInfo

## Global Var
def init():
    global winScale, imageDict

    ## Stores the value that items in
    ## the window should be scaled by.
    ## ----
    ## Value is set in UI.py
    winScale = 1

    ## Stores all images
    ## ----
    ## Use this dict when using images
    ## to save memory
    ## ----
    ## Add new images using UI.addImage()
    imageDict = {}


## Checks whether image is in dict
def isImage(imageName):
    if imageName in imageDict:
        return True
    else:
        printInfo("Error", f"__isImage - Image doesn't exist [{imageName}]")
        return False

## Returns image
def getImage(imageName):
    if isImage(imageName):
        return imageDict[imageName]