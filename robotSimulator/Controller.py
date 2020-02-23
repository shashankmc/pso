import numpy as np


class Controller:

    layersSizes: []
    bias = 1
    populationSize = 1
    population : np.array

    def __init__(self, layers: [], populationSize):
        print("init: layers: " + str(layers))
        self.population = []
        #we need a population of networks
        for ps in range(0, populationSize):
            weights = []
            #networklayers
            for layerLevel in range(1, len(layers)):
                weights.append(np.random.rand(layers[layerLevel - 1] + self.bias, layers[layerLevel]))
            self.population.append(weights)



    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def calc(self, inputValues: []):
        resultAll = []
        for weights in self.population:
            #too lazy to look up how to throw an exception ^^
            if len(inputValues) != len(weights[0]) - self.bias:
                return -1

            #adds a bias to the input array
            res = np.append(np.array(inputValues), self.bias)

            #iterates through the the wheigt matrices connecting layer n and n-1
            for layerWeight in weights:
                res = np.matmul(res, layerWeight)
                res = self.sigmoid(res)
                res = np.append(res, self.bias)

            #adds the result vector of n-th network to resultAll
            #removes the last entry as it is only the bias
            resultAll.append(res[0:-1])

        #resultVector of every network
        return resultAll

    #updates the weight matrix of connecting layerLevel and layerLevel -1
    def train(self, layerLevel):

        #position is index of the network, and value is fitness score
        evaluated = []
        for nwWeights in self.population:
            evaluated.append(self.fit(nwWeights))

        #create a selection with the evaluated list and self.population
        selection = self.selection(evaluated)

        #reproduces a new population with the selected population
        reproduction = self.reproduction(selection)

        #cross mutation because maybe we create spiderman
        crossMutation = self.crossMutation(reproduction)

        #update the weights
        self.population = crossMutation

    def crossMutation(self, reproducedNW):
        print("wait and weight sounds similar")
        return reproducedNW

    def reproducation(self, selectedNW):
        print("f!#$ you")
        return selectedNW

    def selection(self, evalNW):
        print("neither do it")
        return evalNW

    def fit(self, network):
        print("I don t work")
        return network