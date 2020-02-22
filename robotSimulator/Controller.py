import numpy as np


class Controller:

    weights: []
    layersSizes: []
    bias = 1

    def __init__(self, layers: []):

        print("init: layers: " + str(layers))
        self.weights = []
        for layerLevel in range(1, len(layers)):
            self.weights.append(np.random.rand(layers[layerLevel - 1] + self.bias, layers[layerLevel]))

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def calc(self, inputValues: []):

        if len(inputValues) != len(self.weights[0]) - self.bias:
            print("inpL: " + str(len(inputValues)) + "")
            return -1

        res = np.append(np.array(inputValues), self.bias)

        for layerWeight in self.weights:
            res = np.matmul(res, layerWeight)
            res = self.sigmoid(res)
            res = np.append(res, self.bias)

        return res[0:-1]
