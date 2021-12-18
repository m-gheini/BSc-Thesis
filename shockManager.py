class ShockManager:
    def __init__(self, network, threshold, maxIteration):
        self.network = network
        self.threshold = threshold
        self.maxIteration = maxIteration
        self.currentIteration = 0
        self.shockQueue = []
        # self.internalQueue = dict()
        # self.internalQueue[0] = dict()
        # self.iterationHistory = dict()
