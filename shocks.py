import json
from utility import writeShockLog
import updatedDesign as design

# SHK_LOG_PATH = './Assets/shockLog.CSV'


class Shock:
    shocksList = list()

    def __init__(self, origin, target, amount, sign, iteration):
        self.origin = origin
        self.target = target
        self.sign = sign
        self.amount = +1 * float(amount) if self.sign == '+' else -1 * float(amount)
        self.iteration = iteration
        Shock.shocksList.append(self)

    def __str__(self):
        return json.dumps({'origin': self.origin, 'target': self.target,
                           'amount': self.amount, 'sign': self.sign, 'iteration': self.iteration})


class ShockManager:
    def __init__(self, network, threshold, maxIteration, logPath):
        self.network = network
        self.threshold = threshold
        self.maxIteration = maxIteration
        self.currentIteration = 0
        self.shockQueue = []
        self.processQueue = dict()
        self.logPath = logPath

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
                writeShockLog(self.logPath,
                              [shock.origin, shock.target, round(shock.amount, 4), self.network.A[originIndex][targetIndex],
                               round(shockNewAmount, 4), shock.iteration])
                if shock.target not in self.processQueue[shock.iteration]:
                    self.processQueue[shock.iteration][shock.target] = [shockNewAmount, [shock.origin]]
                else:
                    self.processQueue[shock.iteration][shock.target][0] += shockNewAmount
                    self.processQueue[shock.iteration][shock.target][1].append(shock.origin)
        # print(self.processQueue)

    def applyShocks(self):
        # print("applyShocks...")
        while len(self.shockQueue) > 0:
            shock = self.shockQueue.pop()
            self.applyShock(shock)

    def processShocks(self, window):
        # print("processShocks...")
        while (self.currentIteration < self.maxIteration) and (self.currentIteration in self.processQueue):
            print("CURRENT_ITR :: ", self.currentIteration)
            design.updateGif(window, self.currentIteration)
            # logger.
            # self.print()
            for lastTarget in self.processQueue[self.currentIteration]:
                origin = lastTarget
                # print("LAST::",lastTarget, "IS::" ,self.network.getDemandsFrom(lastTarget))
                targets = self.network.getDemandsFrom(lastTarget)
                val = self.processQueue[self.currentIteration][lastTarget][0]
                sign = "+"
                iteration = self.currentIteration + 1
                for target in targets:
                    if target not in self.processQueue[self.currentIteration][lastTarget][1]:
                        newShock = Shock(origin, target, val, sign, iteration)
                        self.addShock(newShock)
            self.applyShocks()
            self.currentIteration += 1

    def print(self):
        print(self.shockQueue)
        print(self.processQueue)
