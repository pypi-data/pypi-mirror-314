########################
# STORAGE Module
# Reading / Writing files and directories
########################

import os, json, sys, shutil, pickle
from csv import writer as csvWriter

# WRITE files
def writeText(filePath, content):
    with open(filePath, "w") as file:
        file.write(content)

def writeJson(filePath, data, indent=4):
    if not filePath.endswith(".json"): filePath += ".json"
    if type(data)==str: data = json.loads(data)
    jsonString = json.dumps(data, indent=indent, sort_keys=False)
    with open(filePath,"w") as file:
        file.write(jsonString)

def renameFile(filePath, newName):
    os.rename(filePath, newName)

def moveFile(fileStart, fileEnd):
    shutil.move(fileStart, fileEnd)

def writeCSV(filePath, data, delimiter=","):
    with open(filePath, "w") as file:
        write = csvWriter(file)
        write.writerows(data)

def writePickle(filePath, data):
    with open(filePath, 'wb') as f:
        pickle.dump(data, f)

# generates a numbered/unique file name
def generateFileName(prefix, folder="."):
    if not os.path.isdir(folder): os.mkdir(folder)
    allFiles = os.listdir(folder)
    maxNumber = -1
    for file in allFiles:
        if file.startswith(prefix):
            if "." in file:
                number = int(file.split(".")[0].split("_")[-1])
            elif "_" in file:
                number = int(file.split("_")[-1])
            if number > maxNumber:
                maxNumber = number
    maxNumber += 1
    return os.path.join(folder, f"{prefix}_{maxNumber}")



# READ files
def readPickle(filePath, fallback=None):
    if not isFile(filePath): return fallback
    with open(filePath, 'rb') as f:
        return pickle.load(f)
def readJson(filePath):
    with open(filePath, "r") as file:
        return json.load(file)
def parseJson(jsonString):
    return json.loads(jsonString)
def readText(filePath):
    with open(filePath, "r") as file:
        return file.read()
def readData(fileName, outputType=str):
    data=[]
    with open(fileName) as f:
        for line in f:
            if outputType==int:
                data.append(int(line))
            elif outputType==float:
                data.append(float(line))
            else:
                data.append(line)
    return data
def readCSV(filePath, delimiter=",", header=False):
    with open(filePath, "r") as file:
        data = file.read()
        lineList = data.split("\n")
    if header==True:
        headerList = lineList.pop(0).split(delimiter)
        headerList = [h.strip() for h in headerList]
        goodData = []
        for line in lineList:
            entry = {}
            row = line.split(delimiter)
            row = [cell.strip() for cell in row]
            if len(row)!=len(headerList): continue
            for i,key in enumerate(headerList):
                entry[key] = row[i]
            goodData.append(entry)
        return goodData
    else:
        return [line.split(delimiter) for line in lineList]





########################
# FILESYSTEM IO
########################
def isFile(filePath):
    return os.path.isfile(filePath)
def isDirectory(dirPath):
    return os.path.isdir(dirPath)


# DELETE files/folders
def deleteFile(filePath):
    os.remove(filePath)
def deleteDirectory(*dirPath):
    dirPath = joinPath(*dirPath)
    if isDirectory(dirPath):
        shutil.rmtree(dirPath)
def makeDirectory(*dirPath):
    dirPath = joinPath(*dirPath)
    if not isDirectory(dirPath):
        os.mkdir(dirPath)


# LIST folders in directory
def listFolders(*dirPath):
    dirPath = joinPath(*dirPath)
    for file in listDirectory(dirPath):
        path = joinPath(dirPath, file)
        if not isFile(path):
            yield path

# LIST files in directory
def listFiles(*dirPath):
    dirPath = joinPath(*dirPath)
    for file in listDirectory(dirPath):
        path = joinPath(dirPath, file)
        if isFile(path):
            yield path
# LIST files in directory + files in child sub-directories
def listFilesDeep(*dirPath):
    dirPath = joinPath(*dirPath)
    return [os.path.join(root, name)
            for root, dirs, files in os.walk(dirPath)
            for name in files]

# LIST files+folders in directory
def listDirectory(*dirPath):
    dirPath = joinPath(*dirPath)
    return os.listdir(dirPath)

# get number of subfolders in folder
def countFolders(*dirPath):
    dirPath = joinPath(*dirPath)
    folders = listFolders(path) 
    return len(list(folders))
# get number of files in folder
def countFiles(dirPath):
    dirPath = joinPath(*dirPath)
    files = listFiles(path) 
    return len(list(files))


# join list of folder into path string
def joinPath(*args):
    if len(args)==0:
        return ""
    elif args[0]==None:
        return os.path.join(*args[1:])
    else:
        return os.path.join(*args)
# clean up string
def sanatizePhrase(phrase):
    for char in list("“”.,\'\"/()[]"):
        phrase = phrase.replace(char," ")
    phrase = " ".join(phrase.split())
    phrase = phrase.title()
    return phrase
