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
            #networklayers111
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
        ctm = 0.1 #chance to mutate
        for i in range (reproducedNW.count):
            if (random()>ctm):
                continue
            mutation = random()
            mw = randomrange(0,reproducedNW.count,1) # random mutation partner
            if (mutation<0.3):
                #onepoint mutation

                continue
            if (mutation<0.6):
                #uniform mutation
                continue
            else:
                continue
                #arithmetic mutation
        return reproducedNW

    def reproduction(self, selectedNW):
        newpopulation = selectedNW
        while(newpopulation.count < newpopulationSize):
            # don't have to check for end of array since it will increase with each loop
            newpopulation.append(newpopulation[i])
            i += 1
        return newpopulation

    def selection(self, evalNW):
        groupsize = 3
        reproduce = 2
        newpopulation = []
        for i in range(0,self.populationSize / groupsize + 1,groupsize):
            group = []
            for j in range(groupsize):
                if (i*groupsize + j < populationSize):
                    group.append(population[groupsize*i + j])
            #SelectionSort
            for j in range(min(reproduce,group.count)):
                for k in range(j,group.count):
                    if (group[j]<group[k]):
                        temp = group[j]
                        group[j] = group[k]
                        group[k] = temp
            for j in range(min(reproduce, group.count)):
                newpopulation.append(group[j])
        return newpopulation

    def fit(self, network):
        print("I don t work")
        return network