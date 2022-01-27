import math
import os
import pandas as pd
import json
import networkx as nx
from network import Network
from network import Sectors
from network import Edges
from shocks import Shock
from shocks import ShockManager
from utility import createShockLog
# from appLogic import getSectorsForCountry

SHK_LOG_PATH = './Assets/shockLog.CSV'
TEST_FILE = './Assets/test.json'

info = json.load(open(TEST_FILE))


# infoDict = {}

def readData(inFile):
    inDataframe = pd.read_csv(inFile, header=None, sep=',', engine='python')
    return inDataframe


def getFirstColumn(dataframe):
    return dataframe[0]


def getFirstRow(dataframe):
    col = dataframe.iloc[:1, :]
    col = col.transpose()
    return col[0]


def getRowNumOfFirstTax(dataframe):
    r = getFirstColumn(dataframe)
    i = -1
    for row in r:
        i += 1
        if i == 0:
            continue
        if row == "0":
            return i
        if row.split('_')[1] == "TAXSUB":
            return i
    return i


def getColNumOfFinalDemand(dataframe):
    c = getFirstRow(dataframe)
    j = -1
    for column in c:
        j += 1
        if j == 0:
            continue
        if column.split('_')[1] == 'HFCE':
            return j
    return j + 1


def getZ(dataframe):
    row = getRowNumOfFirstTax(dataframe)
    col = getColNumOfFinalDemand(dataframe)
    z = dataframe.iloc[1:row, 1:col]
    z = z.astype(float)
    # z.index = range(z.shape[0])
    return z


def getX(dataframe):
    col = getColNumOfFinalDemand(dataframe)
    x = dataframe.iloc[len(getFirstColumn(dataframe)) - 1:, 1:col]
    x = x.astype(float)
    # x.index = range(x.shape[0])
    return x


def getAddedValue(dataframe):
    col = getColNumOfFinalDemand(dataframe)
    addedValue = dataframe.iloc[len(getFirstColumn(dataframe)) - 2:len(getFirstColumn(dataframe)) - 1, 1:col]
    addedValue = addedValue.astype(float)
    return addedValue


def prepareName(country, sector):
    return country + "_" + sector


def makeShockObject(origin, destination, amount, sign, iteration):
    shock = Shock(origin, destination, amount, sign, iteration)
    return shock


def main(data, window, sectorsForCountry):
    origins = []
    targets = []
    itr = math.inf
    thr = -1
    infoDict = data
    print("IN BACK")
    print(infoDict["inputFile"])
    df = readData(infoDict["inputFile"])
    Z = getZ(df)
    print(Z)
    X = getX(df)
    print(X)
    header = list(getFirstRow(df))[1:Z.shape[0] + 1]
    network = Network(Z, X, header)
    # print(network.Z)
    # for i, name in enumerate(network.Header, start=1):
    #     for j, _ in enumerate(network.Header, start=1):
    #         print(i, "-", name, "-", j, "-", network.Z.loc[i][j])
    # print(network.Z.loc[0][3])
    # print(getColNumOfFinalDemand(df))
    # network.updateEdgeWeight("K_0", "K_0", 100)
    # network.showNetwork()
    print(network.A)
    # for s in Sectors.sectorsList:
    #     print(s)
    # for e in Edges.edgesList:
    #     print(e)

    if infoDict["shockSrc"] == "importer":
        if infoDict["imSector"] == "ALL":
            for sector in sectorsForCountry[infoDict["imCountry"]]:
                origins.append(prepareName(infoDict["imCountry"], sector))
        else:
            origins.append(prepareName(infoDict["imCountry"], infoDict["imSector"]))
        if infoDict["exSector"] == "ALL":
            for sector in sectorsForCountry[infoDict["exCountry"]]:
                targets.append(prepareName(infoDict["exCountry"], sector))
        else:
            targets.append(prepareName(infoDict["exCountry"], infoDict["exSector"]))
    elif infoDict["shockSrc"] == "exporter":
        if infoDict["exSector"] == "ALL":
            for sector in sectorsForCountry[infoDict["exCountry"]]:
                origins.append(prepareName(infoDict["exCountry"], sector))
        else:
            origins.append(prepareName(infoDict["exCountry"], infoDict["exSector"]))
        if infoDict["imSector"] == "ALL":
            for sector in sectorsForCountry[infoDict["imCountry"]]:
                targets.append(prepareName(infoDict["imCountry"], sector))
        else:
            targets.append(prepareName(infoDict["imCountry"], infoDict["imSector"]))
    if infoDict["shockItr"] == "NOT CHOSEN":
        thr = float(infoDict["shockThr"])
    elif infoDict["shockThr"] == "NOT CHOSEN":
        itr = int(infoDict["shockItr"])
    else:
        thr = float(infoDict["shockThr"])
        itr = int(infoDict["shockItr"])
    # secondShock = Shock("L_0", "M_0", "1000", "+", 1)
    resultName = infoDict["outputName"] + '.CSV'
    shockLogPath = os.path.join(infoDict["outputPath"], resultName)
    shockManager = ShockManager(network, thr, itr, shockLogPath)
    createShockLog(shockLogPath, ['Origin', 'Target', 'Origin_Shock', 'Coefficient', 'Target-Shock', 'Iteration'])
    print("LOG CREATED!!!!!")
    for origin in origins:
        for target in targets:
            srcIndex = network.getIndex(origin)
            dstIndex = network.getIndex(target)
            firstShock = Shock(origin, target, 0.01 * float(infoDict["shockAmount"]) * network.Z[dstIndex][srcIndex],
                               infoDict["shockSign"], 0)
            shockManager.addShock(firstShock)
    # shockManager.addShock(secondShock)
    shockManager.applyShocks()
    shockManager.processShocks(window)
    shockManager.print()


# main(info)
