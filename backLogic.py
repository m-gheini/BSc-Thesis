import os
import pandas as pd
import networkx as nx
from shocks import Shock
from network import Network
from shockManager import ShockManager

info = {'inputFile': './Assets/data.CSV', 'outputName': 'res', 'outputPath': 'C:/', 'imCountry': 'CAN',
            'imSector': '07T08', 'exCountry': 'BEL', 'exSector': '09', 'shockSrc': 'importer', 'shockSign': '-',
            'shockAmount': '4', 'shockTo': 'intermediate goods', 'shockItr': '11', 'shockThr': 'NOT CHOSEN',
            'imScenario': 'option 1', 'exScenario': 'option 4', 'imAlter': 'NONE', 'exAlter': 'EST_19 : 100'}


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
        if row.split('_')[1] == "TAXSUB":
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


def getZ(dataframe):
    row = getRowNumOfFirstTax(dataframe)
    col = getColNumOfFinalDemand(dataframe)
    z = dataframe.iloc[1:row, 1:col]
    z = z.astype(float)
    return z


def getX(dataframe):
    col = getColNumOfFinalDemand(dataframe)
    x = dataframe.iloc[len(getFirstColumn(dataframe)) - 1:, 1:col]
    x = x.astype(float)
    return x


def getAddedValue(dataframe):
    col = getColNumOfFinalDemand(dataframe)
    addedValue = dataframe.iloc[len(getFirstColumn(dataframe)) - 2:len(getFirstColumn(dataframe)) - 1, 1:col]
    addedValue = addedValue.astype(float)
    return addedValue


# def getImExAdjacency(dataframe):
#     row = getRowNumOfFirstTax(dataframe)
#     col = getColNumOfFinalDemand(dataframe)
#     adjacencyDF = dataframe.iloc[:row, :col]
#     twoLastRow = dataframe.iloc[len(getFirstColumn(dataframe)) - 2:, :col]
#     adjacencyDF = adjacencyDF.append(twoLastRow)
#     adjacencyDF.index = range(adjacencyDF.shape[0])
#     return adjacencyDF


# def prepareNetworkUsingLibrary(dataframe):
#     network = nx.DiGraph()
#     for i in range(1, len(getFirstRow(dataframe))):
#         for j in range(1, len(getFirstColumn(dataframe)) - 2):
#             if float(dataframe[i][j]) != 0:
#                 network.add_edge(dataframe[i][0], dataframe[0][j], weight=float(dataframe[i][j]))
#     return network
#
#
# def getProvidersForSector(graph, node):
#     return list(graph.successors(node))
#
#
# def getDemandersFromSector(graph, node):
#     return list(graph.predecessors(node))
#
#
# def updateEdgeWeight(graph, edge, newWeight):
#     demander, provider = edge
#     graph[demander][provider]["weight"] = newWeight
#     return graph
#
#
# def prepareName(country, sector):
#     return country + "_" + sector
#
#
# def makeShockObject(origin, destination, amount, sign, iteration):
#     shock = Shock(origin, destination, amount, sign, iteration)
#     return shock


def main(data):
    origin = destination = ""
    itr = thr = -1
    infoDict = data
    print("IN BACK")
    df = readData(infoDict["inputFile"])
    Z = getZ(df)
    print(Z)
    X = getX(df)
    header = list(getFirstRow(df))[1:Z.shape[0]+1]
    network = Network(Z, X, header)
    print(network.A)

    # adjacencyDF = getImExAdjacency(df)
    # network = prepareNetworkUsingLibrary(adjacencyDF)
    # print(len(list(network.edges)))
    # if infoDict["shockSrc"] == "importer":
    #     origin = prepareName(infoDict["imCountry"], infoDict["imSector"])
    #     destination = prepareName(infoDict["exCountry"], infoDict["exSector"])
    # elif infoDict["shockSrc"] == "exporter":
    #     origin = prepareName(infoDict["exCountry"], infoDict["exSector"])
    #     destination = prepareName(infoDict["imCountry"], infoDict["imSector"])
    # makeShockObject(origin, destination, infoDict["shockAmount"], infoDict["shockSign"], 1)
    # if infoDict["shockItr"] == "NOT CHOSEN":
    #     thr = int(infoDict["shockThr"])
    # elif infoDict["shockThr"] == "NOT CHOSEN":
    #     itr = int(infoDict["shockItr"])
    # ShockManager(network, thr, itr)


main(info)
