from random import random

import numpy as np

population: np.array
fitnessMean= 0


def init(popSize):
    global population
    population = []
    for i in range(popSize):
        population.append((random() * 4 - 2, random() * 4 - 2))
    population = np.array(population)


def rosenBrockFunc(x, y):
    a = 0
    b = 100
    return ((a - x) ** 2 + b * (y - x ** 2) ** 2)


def fit(point: tuple):
    return 100 - rosenBrockFunc(point[0], point[1])


def tournamentSelection(fitScores: []):
    global population
    k = 4
    selection = []
    for i in range(len(population)):
        tSel = np.random.choice(fitScores, size=k, replace=False)
        tSelIndex = np.where(fitScores == np.amax(tSel))
        selection.append(tSelIndex[0][0])
    return np.array(selection)


def reproduction(reproductionIndex):
    global population
    reproduced = []
    for i in range(len(population)):
        reproduced.append(population[reproductionIndex[i]])
    return reproduced


def crossover(reproducedNW):
    resultArray = []
    # Not sure if this works correctly
    np.random.shuffle(reproducedNW)

    # this needs to be randomized, as it is always the same
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
            cutIndex = np.random.randint(0, len(mum))
            crossedNWs.extend(mum[0:cutIndex])
            crossedNWs.extend(dad[cutIndex:])
        elif crossoverType < 0.6:
            for j in range(len(mum)):
                if random() < 0.5:
                    crossedNWs.append(mum[j])
                else:
                    crossedNWs.append(dad[j])

        else:
            crossedNWs.extend((0.5 * mum[0] + 0.5 * dad[0], 0.5 * mum[1] + 0.5 * dad[1]))
            # crossedNWs.append(np.add(mum, dad) / 2)

        resultArray.append(crossedNWs)
    return resultArray


def mutation(reproducedNW):
    ctm = 0.1  # chance to mutate
    for repNW in reproducedNW:
        if random() > ctm:
            continue

        rndVal = random() * 2 - 1

        if rndVal < 0:
            repNW[0] += rndVal
        else:
            repNW[1] += rndVal

    return reproducedNW


def train():
    global fitnessMean
    global population
    # position is index of the network, and value is fitness score
    evaluated = []
    for tup in population:
        evaluated.append(fit(tup))


    fitnessMean = np.mean(evaluated)
    print("FitnessMean: " + str(fitnessMean))

    print("\tFitnessScores: " + str(evaluated))

    # create a selection with the evaluated list and self.population
    # results in a list of selected indexes
    selection = tournamentSelection(evaluated)
    print("\tSelection: " + str(selection))
    # reproduces a new population with the selected indexes
    # returns flatten weight list

    repro = reproduction(selection)
    print("\tReproduction: " + str(repro))

    # reproduces the children with mixing from parents
    crosso = crossover(repro)
    print("\tCrossover: " + str(crosso))

    # cross mutation because maybe we create spiderman
    crossMutation = mutation(crosso)
    print("\tCross Mutation: " + str(crossMutation))

    # update the weights
    for i in range(len(population)):
        population[i] = (crossMutation[i][0],crossMutation[i][1])


init(10)
while fitnessMean < 99:
    train()
