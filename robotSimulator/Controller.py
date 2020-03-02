import numpy as np
from numpy.random.mtrand import random

from pso.robotSimulator.Network import Network


class Controller:
    # layersSizes: []
    # bias = 1
    populationSize = 1
    population: [Network]

    def __init__(self, layers: [], populationSize):
        print("init: layers: " + str(layers))
        self.population = []
        # we need a population of networks
        for ps in range(0, populationSize):
            self.population.append(Network(layers))

    # updates the weight matrix of connecting layerLevel and layerLevel -1
    def train(self, inputValues):

        # position is index of the network, and value is fitness score
        evaluated = []
        for network in self.population:
            resultFromInput = network.calc(inputValues)
            fitnessScore = self.fit(resultFromInput)
            evaluated.append(fitnessScore)

        # create a selection with the evaluated list and self.population
        # results in a list of selected indexes
        selection = self.tournamentSelection(evaluated)
        print("Selection: " + str(selection))
        # reproduces a new population with the selected indexes
        # returns flatten weight list
        reproduction = self.reproduction2(selection)
        print("Reproduction: " + str(reproduction))

        #reproduces the children with mixing from parents
        crossover = self.crossover(reproduction)
        print("Crossover: " + str(crossover))

        # cross mutation because maybe we create spiderman
        crossMutation = self.mutation(crossover)
        print("Cross Mutation: " + str(crossMutation))
        # update the weights
        for i in range(len(self.population)):
            self.population[i].setWeightsAsList(crossMutation[i])

    def crossover(self, reproducedNW):
        resultArray = []
        # Not sure if this works correctly
        np.random.shuffle(reproducedNW)

        #this needs to be randomized, as it is always the same
        crossoverType = random()

        for i in range(len(reproducedNW)):
            crossedNWs = []
            # if multiple weights
            mum: np.array = reproducedNW[i]
            dad: np.array = reproducedNW[0]
            if i < len(reproducedNW) - 1:
                dad = reproducedNW[i + 1]

            if crossoverType < 0.3:
                # onepoint mutation
                print("ONEPOINT")
                cutIndex = np.random.randint(0, len(mum))
                crossedNWs.extend(mum[0:cutIndex])
                crossedNWs.extend(dad[cutIndex:])
            elif crossoverType < 0.6:
                print("other")
                for j in range(len(mum)):
                    if random() < 0.5:
                        crossedNWs.append(mum[j])
                    else:
                        crossedNWs.append(dad[j])

            else:
                print("ari")
                crossedNWs.extend(mum[:])
                #crossedNWs.append(np.add(mum, dad) / 2)

            resultArray.append(crossedNWs)
        return resultArray

    def mutation(self, reproducedNW):
        ctm = 0.1  # chance to mutate
        for repNW in reproducedNW:
            if random() > ctm:
                continue
            if len(repNW) <= 1:
                print("Shoudln t happen, len: " + str(len(repNW)))
                continue
            index = np.random.randint(0, len(repNW))

            if random() < 0.5:
                repNW[index] = repNW[index] + 1
            else:
                repNW[index] = repNW[index] - 1

        return reproducedNW

    def reproduction2(self, reproductionIndex):
        reproduced = []
        for i in range(len(self.population)):
            reproduced.append(self.population[reproductionIndex[i]].getWeightsAsList())
        return reproduced

    def reproduction(self, selectedNW):
        newpopulation = selectedNW
        while (newpopulation.count < self.newpopulationSize):
            # don't have to check for end of array since it will increase with each loop
            newpopulation.append(newpopulation[i])
            i += 1
        return newpopulation

    def crossMutation(self, reproducedNW):
        ctm = 0.1  # chance to mutate
        for i in range(reproducedNW.count):
            if (random() > ctm):
                continue
            mutation = random()
            mw = randomrange(0, reproducedNW.count, 1)  # random mutation partner
            if (mutation < 0.3):
                # onepoint mutation

                continue
            if (mutation < 0.6):
                # uniform mutation
                continue
            else:
                continue
                # arithmetic mutation
        return reproducedNW

    def tournamentSelection(self, fitScores: []):
        k = 4
        selection = []
        for i in range(len(self.population)):
            #returns k random elements of fitscores
            tSel = np.random.choice(fitScores, size=k, replace=False)
            #finds the index of the highest fit of tSel in fitScores
            tSelIndex = np.where(fitScores == np.amax(tSel))
            selection.append(tSelIndex[0][0])
        return np.array(selection)

    def selection(self, evalNW):
        groupsize = 3
        reproduce = 2
        newpopulation = []
        for i in range(0, self.populationSize / groupsize + 1, groupsize):
            group = []
            for j in range(groupsize):
                if (i * groupsize + j < self.populationSize):
                    group.append(self.population[groupsize * i + j])
            # SelectionSort
            for j in range(min(reproduce, group.count)):
                for k in range(j, group.count):
                    if (group[j] < group[k]):
                        temp = group[j]
                        group[j] = group[k]
                        group[k] = temp
            for j in range(min(reproduce, group.count)):
                newpopulation.append(group[j])
        return newpopulation

    def fit(self, network):
        print("I don t work")
        return random()*10


c = Controller([2, 4, 3], 10)
for i in range(100):
    c.train([1,2])
