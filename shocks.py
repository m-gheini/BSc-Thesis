import json
from utility import writeShockLog
SHK_LOG_PATH = './Assets/shockLog.CSV'

class Shock:
    shocksList = list()

    def __init__(self, origin, target, amount, sign, iteration):
        self.origin = origin
        self.target = target
        self.amount = amount
        self.sign = sign
        self.iteration = iteration
        Shock.shocksList.append(self)

    def __str__(self):
        return json.dumps({'origin': self.origin, 'target': self.target,
                           'amount': self.amount, 'sign': self.sign, 'iteration': self.iteration})


class ShockManager:
    def __init__(self, network, threshold, maxIteration):
        self.network = network
        self.threshold = threshold
        self.maxIteration = maxIteration
        self.currentIteration = 1
        self.shockQueue = []
        self.processQueue = dict()

    def addShock(self, shock):
        # print("addShock...")
        self.shockQueue.append(shock)
        # print(shock)

    def applyShock(self, shock):
        # print("applyShock...")
        if not self.processQueue.get(shock.iteration):
            self.processQueue[shock.iteration] = dict()
        if shock.amount != 0:
            targetIndex = self.network.getIndex(shock.target)
            originIndex = self.network.getIndex(shock.origin)
            shockNewAmount = float(shock.amount) * self.network.A[originIndex][targetIndex]
            # print("shock Amount::",float(shock.amount),"/A::",self.network.A[targetIndex][originIndex])
            if (abs(shockNewAmount) >= self.threshold) or (self.threshold == -1):
                writeShockLog(SHK_LOG_PATH, [shock.origin, shock.target, shock.amount, shockNewAmount, shock.iteration])
                if not shock.target in self.processQueue[shock.iteration]:
                    self.processQueue[shock.iteration][shock.target] = shockNewAmount
                else:
                    self.processQueue[shock.iteration][shock.target] += shockNewAmount
        # print(self.processQueue)

    def applyShocks(self):
        # print("applyShocks...")
        while len(self.shockQueue) > 0:
            shock = self.shockQueue.pop()
            self.applyShock(shock)

    def processShocks(self):
        # print("processShocks...")
        while self.currentIteration < self.maxIteration:
            # logger.
            # self.print()
            for lastTarget in self.processQueue[self.currentIteration]:
                origin = lastTarget
                # print("LAST::",lastTarget, "IS::" ,self.network.getDemandsFrom(lastTarget))
                targets = self.network.getDemandsFrom(lastTarget)
                val = self.processQueue[self.currentIteration][lastTarget]
                sign = "+"
                iteration = self.currentIteration + 1
                for target in targets:
                    newShock = Shock(origin, target, val, sign, iteration)
                    self.addShock(newShock)
            self.applyShocks()
            self.currentIteration += 1

    def print(self):
        print(self.shockQueue)
        print(self.processQueue)
