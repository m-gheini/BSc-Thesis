import os
import pandas as pd
import networkx as nx

infoDict = {'inputFile': './Assets/ICIO2018_2015.CSV', 'outputName': 'res', 'outputPath': 'C:/', 'imCountry': 'CAN',
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


def getImExAdjacency(dataframe):
    row = getRowNumOfFirstTax(dataframe)
    col = getColNumOfFinalDemand(dataframe)
    adjacencyDF = dataframe.iloc[:row, :col]
    twoLastRow = dataframe.iloc[len(getFirstColumn(dataframe)) - 2:, :col]
    adjacencyDF = adjacencyDF.append(twoLastRow)
    adjacencyDF.index = range(adjacencyDF.shape[0])
    return adjacencyDF


def prepareNetworkUsingLibrary(dataframe):
    network = nx.DiGraph()
    for i in range(1, len(getFirstRow(dataframe))):
        for j in range(1, len(getFirstColumn(dataframe))-2):
            if float(dataframe[i][j]) != 0:
                network.add_edge(dataframe[i][0], dataframe[0][j], weight=float(dataframe[i][j]))
    return network


def getProvidersForSector(graph, node):
    return list(graph.successors(node))


def getDemandersFromSector(graph, node):
    return list(graph.predecessors(node))


def main(data):
    infoDict = data
    print("IN BACK")
    df = readData(infoDict["inputFile"])
    adjacencyDF = getImExAdjacency(df)
    network = prepareNetworkUsingLibrary(adjacencyDF)
    print(len(list(network.edges)))


main(infoDict)
