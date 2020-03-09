import numpy as np
from numpy.random.mtrand import random

from pso.robotSimulator.Network import Network
from pso.robotSimulator.Stat import Stat


class Controller:
    # layersSizes: []
    # bias = 1
    populationSize = 1
    population: [Network]
    fitnessScores: []

    highestScore = -10000
    highestMeansScore = -10000
    highestCurrentScore = -10000
    currentMeanScore = []

    hammingDistance= []

    bestCurrentNetwork: Network

    highestPopulation: [Network]
    layers: []

    def __init__(self, layers: [], populationSize):
        print("init: layers: " + str(layers))
        self.population = []
        self.fitnessScores = []
        self.layers = layers
        # we need a population of networks

        for ps in range(0, populationSize):
            self.population.append(Network(layers))
            self.fitnessScores.append(0)

    def calcHammingDistance(self):
        hamm = 0
        bestWList = self.bestCurrentNetwork.getWeightsAsList()
        for nw in self.population:
            conc = nw.getWeightsAsList()
            for i in range(len(bestWList)):
                if np.abs(bestWList[i] - conc[i]) > 0.01:
                    hamm += 1
        self.hammingDistance.append(hamm)

    def setFitnessScores(self, statsInOrder: []):
        self.fitnessScores = []
        for pop in range(len(self.population)):
            self.fitnessScores.append(self.fit(statsInOrder[pop]))

        self.currentMeanScore.append(np.mean(self.fitnessScores))
        self.highestMeansScore = np.max([self.currentMeanScore[-1], self.highestMeansScore])
        self.highestCurrentScore = np.max([self.fitnessScores])
        self.bestCurrentNetwork = self.population[np.argmax(self.fitnessScores)]
        self.highestScore = np.max([self.highestCurrentScore, self.highestScore])

        self.calcHammingDistance()

        # print(self.fitnessScores)

    # updates the weight matrix of connecting layerLevel and layerLevel -1
    def train(self):

        # position is index of the network, and value is fitness score
        # evaluated = []
        # for network in self.population:
        #    resultFromInput = network.calc(inputValues)
        #    fitnessScore = self.fit(resultFromInput)
        #    evaluated.append(fitnessScore)

        ########################
        # fitnessScores is set in the fitness score setter
        ########################
        # create a selection with the evaluated list and self.population
        # results in a list of selected indexes
        selection = self.tournamentSelection(self.fitnessScores)
        # print("Selection: " + str(selection))
        # reproduces a new population with the selected indexes
        # returns flatten weight list
        reproduction = self.reproduction2(selection)
        # print("Reproduction: " + str(reproduction))

        # reproduces the children with mixing from parents
        crossover = self.crossover(reproduction)
        # print("Crossover: " + str(crossover))

        # cross mutation because maybe we create spiderman
        # crossMutation = self.mutation(crossover)
        # print("Cross Mutation: " + str(crossMutation))
        # update the weights
        for i in range(len(self.population)):
            self.population[i].setWeightsAsList(crossover[i])

        crossMutation = self.mutation(crossover)
        return self.currentMeanScore

    def crossover(self, reproducedNW):
        resultArray = []
        # Not sure if this works correctly
        np.random.shuffle(reproducedNW)

        # this needs to be randomized, as it is always the same

        for i in range(len(reproducedNW)):
            crossoverType = random()
            # crossoverType = 0.9
            # print("Crossover: " + str(crossoverType))
            crossedNWs = []
            # if multiple weights
            mum: np.array = reproducedNW[i]
            dad: np.array = reproducedNW[0]
            if i < len(reproducedNW) - 1:
                dad = reproducedNW[i + 1]

            if crossoverType < 0.4:
                # onepoint mutation
                # print("ONEPOINT")
                cutIndex = np.random.randint(0, len(mum))
                crossedNWs.extend(mum[0:cutIndex])
                crossedNWs.extend(dad[cutIndex:])
            elif crossoverType < 0.6:
                # print("other")
                for j in range(len(mum)):
                    if random() < 0.5:
                        crossedNWs.append(mum[j])
                    else:
                        crossedNWs.append(dad[j])

            else:
                # print("ari")
                blaa = (mum + dad) / 2
                crossedNWs.extend(blaa.tolist())

            resultArray.append(crossedNWs)
        return resultArray

    def mutation(self, reproducedNW):
        ctm = 0.05  # chance to mutate
        for nw in self.population:
            if random() > ctm:

                wml = []
                for layerLevel in range(1, len(self.layers)):
                    wml.append(np.random.rand(self.layers[layerLevel - 1] + 1, self.layers[layerLevel]) * 2 - 1)
                wml = np.array(wml)
                nw.weightMatrixList = wml
                return

            # for repNW in reproducedNW:
            #    if random() > ctm:
            #    continue
            # if len(repNW) <= 1:
            #    print("Shoudln t happen, len: " + str(len(repNW)))
            #    continue
            # index = np.random.randint(0, len(repNW))

            # if random() < 0.5:
            #    repNW[index] = -repNW[index]
            # else:
            #    repNW[index] = 2*repNW[index]

        return reproducedNW

    def reproduction2(self, reproductionIndex):
        reproduced = []
        for i in range(len(self.population)):
            reproduced.append(self.population[reproductionIndex[i]].getWeightsAsList())
        return reproduced

    def tournamentSelection(self, fitScores: []):
        k = 20
        selection = []
        for i in range(len(self.population)):
            # returns k random elements of fitscores
            tSel = np.random.choice(fitScores, size=k, replace=False)
            # finds the index of the highest fit of tSel in fitScores
            tSelIndex = np.where(fitScores == np.amax(tSel))
            selection.append(tSelIndex[0][0])
        return np.array(selection)

    def fit(self, stat: Stat):

        wallscore = 1 - 1 / (1 + stat.bumpedIntoWall[0])
        areascore = stat.areaCovered / stat.maxArea

        dvC = np.mean(stat.dvCount)

        result = areascore - wallscore + dvC

        #print("Stat: " + str(stat))
        #print("biw: " + str(stat.bumpedIntoWall) + ", area: " + str(stat.areaCovered))
        #print("fit score: " + str(result))

        return result

    def calc(self, ind, inputs):
        return self.population[ind].calc(inputs, ind)

    def savePopulation(self, path):
        count = 0
        for nw in self.population:
            nw.savenetwork(path + str(count))
            count += 1

    def loadPopulation(self, path):
        count = 0
        for nw in self.population:
            nw.loadnetwork(path + str(count))
            count += 1
