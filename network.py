import json
from utility import getTechnicalCoefficients
import networkx as nx
import matplotlib.pyplot as plt


class Sectors:
    sectorsList = list()

    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.providesTo = list()
        self.demandsFrom = list()
        Sectors.sectorsList.append(self)

    def __str__(self):
        return json.dumps({'index': self.index, 'name': self.name,
                           'provides_to': self.providesTo, 'demands_from': self.demandsFrom})


class Edges:
    edgesList = list()

    def __init__(self, edge, weight):
        self.demander = edge[0]
        self.provider = edge[1]
        self.weight = weight
        Edges.edgesList.append(self)

    def __str__(self):
        return json.dumps({'demander': self.demander, 'provider': self.provider, 'weight': self.weight})

    def updateWeight(self, newWeight):
        self.weight = newWeight


class Network:
    def __init__(self, Z, X, Header):

        self.Z = Z
        self.X = X
        self.Header = Header
        self.A = getTechnicalCoefficients(self.Z, self.X)
        self.network = self.generateStructure()
        # self.A_Inverse = getLeontiefInverseMatrix(self.A0)
        # self.graph = {}
        # self.internalQueue = dict()
        # self.shockQueue = dict()
        #
        # logger.info(f"A:\n{self.A}")
        # logger.info(f"X:\n{self.X}")
        # logger.info(f"Header:\n{self.Header}")
        # logger.info(f"\nTechnical Coeff:\n{self.A0}")
        # logger.info(f"\nA0 Inverse:\n{self.A_Inverse}")

        # self.generateStructue()

    def generateStructure(self):
        net = nx.DiGraph()
        for i, demander in enumerate(self.Header, start=1):
            print(i, demander)
            newSector = Sectors(i, demander)
            # providesTo = []
            # demandsFrom = []
            for j, provider in enumerate(self.Header, start=1):
                print(j)
                print(demander, "-", provider, "-", self.Z[i][j])
                if float(self.Z[i][j]) != 0.0:
                    print("Y", self.Z[i][j])
                    net.add_edge(demander, provider, weight=float(self.Z[i][j]))
        for sector in Sectors.sectorsList:
            sector.demandsFrom = list(net.successors(sector.name))
            sector.providesTo = list(net.predecessors(sector.name))

        for edge in net.edges:
            newEdge = Edges(edge, net[edge[0]][edge[1]]["weight"])

        return net

    def showNetwork(self):
        nx.draw(self.network, with_labels=True)
        plt.show()

    def updateEdgeWeight(self, demander, provider, newWeight):
        available = self.network.has_edge(demander, provider)
        if available:
            self.network[demander][provider]["weight"] = newWeight
            for edge in Edges.edgesList:
                if edge.demander == demander and edge.provider == provider:
                    edge.updateWeight(newWeight)
        else:
            self.network.add_edge(demander, provider, weight=newWeight)
            newEdge = Edges((demander, provider), newWeight)
            for sector in Sectors.sectorsList:
                print("IN FOR")
                i = 0
                if sector.name == demander:
                    i+=1
                    sector.demandsFrom.append(provider)
                if sector.name == provider:
                    i+=1
                    sector.providesTo.append(demander)
                if i == 2:
                    break
