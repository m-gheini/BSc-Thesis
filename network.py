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
        return net

    def showNetwork(self):
        nx.draw(self.network, with_labels=True)
        plt.show()
    #
    # def generateStructue(self):
    #     logger.info("-=-" * 10)
    #     logger.info("Generating Graph Structure ...")
    #     logger.info("-=-" * 10)
    #     for i, node in enumerate(self.Header):
    #         newNode = Node(node)
    #         provides_to = []
    #         demands_from = []
    #         provides_to_edges = []
    #         demands_from_edges = []
    #         for j, _ in enumerate(self.Header):
    #             if i != j and self.A[i][j] != 0:
    #                 provides_to.append(self.Header[j])
    #                 provides_to_edges.append(Edge(self.Header[i], self.Header[j], self.A[i][j], "Provider"))
    #             if i != j and self.A[j][i] != 0:
    #                 demands_from.append(self.Header[j])
    #                 demands_from_edges.append(Edge(self.Header[i], self.Header[j], self.A[j][i], "Demander"))
    #         newNode.demands_from = demands_from
    #         newNode.provides_to = provides_to
    #         newNode.demands_from_edges = demands_from_edges
    #         newNode.provides_to_edges = provides_to_edges
    #
    #         self.graph[node] = newNode
    #
    #         logger.info("New Node Added ...")
    #         logger.info(pformat(newNode))
    #
    #     logger.info("-=-" * 10)
    #     logger.info(f"Final Graph Structure : \n{pformat(self.graph)}")
    #     logger.info("-=-" * 10)
    #     self.applyShock()
    #
    # def getIndex(self, node_name):
    #     index = -1
    #     for i, name in enumerate(self.Header):
    #         if name == node_name:
    #             index = i
    #             break
    #     if index >= 0:
    #         return index
    #     raise Exception("Index Not Found in Header Names")
    #
    # def test_shock(self):
    #     import random
    #     for node, node_data in self.graph.items():
    #         for edge in node_data.provides_to_edges_info:
    #             edge.update_weight(random.randint(1, 30))
    #
    #     for node, node_data in self.graph.items():
    #         for edge in node_data.provides_to_edges_info:
    #             logger.info("=-" * 25)
    #             logger.info(pformat(edge))
    #             logger.info("=-" * 25)
    #             logger.info(
    #                 f"Edge  History:\n <{edge.nodes[0]},{edge.nodes[1]}> - Changes Over Time:\n{pformat(edge.get_history())}")
    #
    # def applyShock(self, deltaF=None):
    #     deltaF = [0, 20, 0]
    #     logger.info("-=-" * 10)
    #     logger.info(f"Delta F : {deltaF}")
    #     logger.info("-=-" * 10)
    #     iteration = 0
    #     flag = True
    #
    #     self.internalQueue[iteration] = dict()
    #     for i, shock in enumerate(deltaF):
    #         if shock != 0:
    #             logger.info(f"Shock Originated From : {self.Header[i]} ")
    #             for target in self.graph[self.Header[i]].demands_from:
    #                 target_index = self.getIndex(target)
    #                 logger.info(f"  Target of Shock : {target}")
    #                 logger.info(f"    Received Shock : {shock}")
    #                 logger.info(f"    Coefficient Applied : {self.A0[target_index][i]}")
    #                 self.internalQueue[iteration][target] = {
    #                     self.Header[i]: shock * self.A0[target_index][i]
    #                 }
    #             logger.info("-=-" * 10)
    #     self.__processInternalQueue__(0)
    #     iteration += 1
    #     while iteration < 10 and flag:
    #         self.internalQueue[iteration] = dict()
    #         deltaF = [0, 0, 0]
    #         for target_node, delta_f in self.shockQueue[iteration - 1].items():
    #             deltaF[self.getIndex(target_node)] = delta_f
    #         logger.info("-=-" * 10)
    #         logger.info(f"Delta F : {deltaF}")
    #         logger.info("-=-" * 10)
    #         for i, shock in enumerate(deltaF):
    #             if shock != 0:
    #                 logger.info(f"Shock Originated From : {self.Header[i]} ")
    #                 for target in self.graph[self.Header[i]].demands_from:
    #                     target_index = self.getIndex(target)
    #                     logger.info(f"  Target of Shock : {target}")
    #                     logger.info(f"    Received Shock : {shock}")
    #                     logger.info(f"    Coefficient Applied : {self.A0[target_index][i]}")
    #                     self.internalQueue[iteration][target] = {
    #                         self.Header[i]: shock * self.A0[target_index][i]
    #                     }
    #                 logger.info("-=-" * 10)
    #         self.__processInternalQueue__(iteration)
    #         iteration += 1
    #
    # def __processInternalQueue__(self, iteration):
    #     logger.info(f"Processing Queue - Iteration : {iteration}")
    #     logger.info(f"Internal Queue : \n{pformat(self.internalQueue)}")
    #     logger.info("-=-" * 10)
    #     # key = f'{iteration}'
    #     self.shockQueue[iteration] = dict()
    #     for target, shocks in self.internalQueue[iteration].items():
    #         s = 0
    #         for shock in shocks.values():
    #             s += shock
    #         self.shockQueue[iteration][target] = s
    #     logger.info(f"Shock Queue :\n{self.shockQueue}")
    #     logger.info("-=-" * 10)
