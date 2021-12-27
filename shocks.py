import json


class Shock:
    shocksList = list()

    def __init__(self, origin, destination, amount, sign, iteration):
        self.origin = origin
        self.destination = destination
        self.amount = amount
        self.sign = sign
        self.iteration = iteration
        Shock.shocksList.append(self)

    def __str__(self):
        return json.dumps({'origin': self.origin, 'destination': self.destination,
                           'amount': self.amount, 'sign': self.sign, 'iteration': self.iteration})



class ShockManager:
    def __init__(self, network, threshold, maxIteration):
        self.network = network
        self.threshold = threshold
        self.maxIteration = maxIteration
        self.currentIteration = 0
        self.shockQueue = []


# class Shock(object):
#     G: Graph
#
#     def __init__(self, provider, amount, iteration) -> None:
#         super().__init__()
#         self.provider = provider
#         self.amount = amount
#         self.iteration = iteration
#
#     def __str__(self):
#         return f"Shock Info: \n\tProvider: {self.provider},\n\tAmount: {self.amount},\n\tIteration:{self.iteration}"
#
#
# class ShockManager(object):
#     def __init__(self, graph: Graph, threshold: float = 0.01, maxCount=5) -> None:
#         super().__init__()
#         self.shockHistory = []
#         self.currentIteration = 0
#         self.shockQueue = []
#         self.G = graph
#         self.internalQueue = dict()
#         self.internalQueue[0] = dict()
#         self.threshold = threshold
#         self.iterationHistory = dict()
#         self.maxCount = maxCount
#
#     def initializeShocks(self, FD_ChangeVector):
#         pass
#
#     def addShock(self, shock):
#         self.shockQueue.append(shock)
#         logger.info(f"Shock Added To Current Iteration({self.currentIteration}) Queue \n{shock}")
#         logger.info("-=-" * 10)
#         logger.info(f"Queue Len : {len(self.shockQueue)}")
#         logger.info("-=-" * 10)
#
#     def processShocks(self):
#         logger.info("=-=-=- Processing Shocks Started  -=-=-=-=")
#         logger.info(f"Graph : {pformat(self.G.graph)}")
#         logger.info("-=-" * 10)
#         while self.currentIteration < self.maxCount:
#             logger.info("-=-" * 10)
#             logger.info(f"-=--=--=--=--=- Iteraion {self.currentIteration + 1} Started -=--=--=--=--=-")
#
#             iterationShockFinalValues = self.__processInternalQueue__(self.currentIteration)
#             # logger.
#             for node, v in iterationShockFinalValues.items():
#                 newShock = Shock(node, v, self.currentIteration + 1)
#                 self.addShock(newShock)
#             self.applyShocks()
#             logger.info(f"-=--=--=--=--=- Iteraion {self.currentIteration + 1} Ended   -=--=--=--=--=-")
#             self.currentIteration += 1
#         logger.info("-_-" * 20)
#         logger.info(f"\n{pformat(self.iterationHistory)}")
#
#     def applyShocks(self):
#         while len(self.shockQueue) > 0:
#             shock = self.shockQueue.pop()
#             self.applyShock(shock)
#             self.shockHistory.append(shock)
#
#         # self.aggregateShocks()
#         # self.currentIteration += self.currentIteration
#
#     def applyShock(self, shock: Shock) -> None:
#         logger.info(f"Applying Shock :\n {shock}")
#         logger.info("-=-" * 10)
#         if not self.internalQueue.get(shock.iteration, None):
#             self.internalQueue[shock.iteration] = dict()
#         if shock.amount != 0:
#             for shockTarget in self.G.graph[shock.provider].demands_from:
#                 target_index = self.G.getIndex(shockTarget)
#                 source_index = self.G.getIndex(shock.provider)
#                 logger.info(f"Diffusion from {self.G.graph[shock.provider].key} to {self.G.graph[shockTarget].key}")
#                 # print(f"Diffusion from {self.graph.Header[source_index]} to {self.graph.Header[target_index]}")
#                 logger.info(f"Shock Amount : {shock.amount}")
#                 logger.info(f"Coefficient Applied : {self.G.A0[target_index][source_index]}")
#                 shockNewAmount = shock.amount * self.G.A0[target_index][source_index]
#                 if abs(shockNewAmount) >= self.threshold:
#
#                     if self.internalQueue[shock.iteration].get(shockTarget, None) == None:
#                         self.internalQueue[shock.iteration][shockTarget] = {
#                             shock.provider: shockNewAmount
#                         }
#                     else:
#                         self.internalQueue[shock.iteration][shockTarget] = {
#                             **self.internalQueue[shock.iteration][shockTarget],
#                             **{shock.provider: shockNewAmount}
#                         }
#             logger.info(
#                 f"Internal Queue - Iteration: {shock.iteration}\n{pformat(self.internalQueue[shock.iteration])}")
#             logger.info("-=-" * 10)
#
#         # self.__processInternalQueue__(0)
#
#     def __processInternalQueue__(self, iteration):
#         logger.info(f"Processing Internal Queue - Iteration : {iteration}")
#         logger.info(f"Internal Queue : \n{pformat(self.internalQueue[iteration])}")
#         logger.info("-=-" * 10)
#         # key = f'{iteration}'
#         finalShockValues = dict()
#         for target, shocks in self.internalQueue[iteration].items():
#             s = 0
#             for shock in shocks.values():
#                 s += shock
#             finalShockValues[target] = s
#         self.iterationHistory[iteration] = finalShockValues
#         return finalShockValues
