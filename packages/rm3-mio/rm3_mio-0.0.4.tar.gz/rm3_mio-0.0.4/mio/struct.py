#######################
# STRUCT MODULE
# utlities for working with data structures
#######################


# flatten any list -> 1D array
def flatten(inList):
    outList = []
    for item in inList:
        if type(item)==list:
            outList += flatten(item)
        else:
            outList.append(item)
    return outList


# unpack a dictionary into global variable space
def unpack(dictionary):
    if vSpace==None: vSpace = globals
    for key,value in dictionary.items():
        vSpace()[key] = value
