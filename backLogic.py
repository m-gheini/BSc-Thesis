import os
import pandas as pd
infoDict = {'inputFile': './Assets/ICIO2018_2015.CSV', 'outputName': 'res', 'outputPath': 'C:/', 'imCountry': 'CAN', 'imSector': '07T08', 'exCountry': 'BEL', 'exSector': '09', 'shockSrc': 'importer', 'shockSign': '-', 'shockAmount': '4', 'shockTo': 'intermediate goods', 'shockItr': '11', 'shockThr': 'NOT CHOSEN', 'imScenario': 'option 1', 'exScenario': 'option 4', 'imAlter': 'NONE', 'exAlter': 'EST_19 : 100'}

# infoDict = {}

def readData(inFile):
    inDataframe = pd.read_csv(inFile)
    return inDataframe

# def getImExAdjacency(inDataframe):


# def prepareImExAdjacency():


def main(data):
    infoDict = data
    print("IN BACK")
    print(readData(infoDict["inputFile"]))

main(infoDict)