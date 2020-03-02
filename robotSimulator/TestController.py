from random import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
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

def rastrigin(x, y):
    n = 2
    sum = 10 * n
    sum += (x ** 2 - 10 * np.cos(2 * np.pi * x))
    sum += (y ** 2 - 10 * np.cos(2 * np.pi * y))
    return sum


def rastriginFunc(x,y):
    n = 2
    sum = 10 * n
    sum += (x ** 2 - 10 * np.cos(2 * np.pi * x))
    sum += (y ** 2 - 10 * np.cos(2 * np.pi * y))
    return sum


def fit(point: tuple):
    #return 100 - rosenBrockFunc(point[0], point[1])
    return 100 - rastriginFunc(point[0], point[1])

def fit2(point: tuple):
    return 100 - rastrigin(point[0], point[1])


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
<<<<<<< HEAD
        evaluated.append(fit(tup))
        display()
=======
        evaluated.append(fit2(tup))

>>>>>>> e8b37183e9f420bf8442817cd751b63ad8498206

    fitnessMean = np.mean(evaluated)
    #print("FitnessMean: " + str(fitnessMean))

    #print("\tFitnessScores: " + str(evaluated))

    # create a selection with the evaluated list and self.population
    # results in a list of selected indexes
    selection = tournamentSelection(evaluated)
    #print("\tSelection: " + str(selection))
    # reproduces a new population with the selected indexes
    # returns flatten weight list

    repro = reproduction(selection)
    #print("\tReproduction: " + str(repro))

    # reproduces the children with mixing from parents
    crosso = crossover(repro)
    #print("\tCrossover: " + str(crosso))

    # cross mutation because maybe we create spiderman
    crossMutation = mutation(crosso)
    ##print("\tCross Mutation: " + str(crossMutation))

    # update the weights
    for i in range(len(population)):
        population[i] = (crossMutation[i][0],crossMutation[i][1])

def average():
    global population
    sumx = 0
    sumy = 0
    for i in range(len(population)):
        sumx += population[i][0]
        sumy += population[i][1]
    sumx /= len(population)
    sumy /= len(population)
    print("avg. X: " + str(sumx))
    print("avg. Y: " + str(sumy))

def display(loop):
    # creates an array from -2 to 2 with 100 steps
    x = np.linspace(-15, 15, 100)
    y = np.linspace(-3, 3, 100)

    # this meshgrid transform needed for plot
    xx, yy = np.meshgrid(x, y)

    # evaluating every z value for the variable grid
    zz = rastrigin(xx, yy)

    # plot stuff
    fig = plt.figure(0)
    ax = plt.axes(projection='3d')
    ax.plot_surface(xx, yy, zz, cmap='viridis', alpha=0.5)
    # ax.contour3D(xx, yy, zz, 50, cmap='binary')
    ax.set_title('Surface plot after ' + str(loop) + " iteration(s)")
    # Iterates over particle and adds a dot to ax for each current location location
    for particle in population:
        #ax.scatter(particle.location[0], particle.location[1], 2000, c='r', marker='x')
        ax.scatter(particle[0], particle[1],
                   rastrigin(particle[0], particle[1]),
                   c='r', marker='>', alpha=0.5)
    ax.view_init(60,35)
    if(loop % 100 == 0):
        plt.savefig('fig%d.png' %loop)
    plt.pause(0.001)

def display():
    global population
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)

    xx, yy = np.meshgrid(x, y)
    # zz = rosenBrockFunc(xx, yy)
    zz = rastriginFunc(xx, yy)

    fig = plt.figure(0)
    ax = plt.axes(projection='3d')
    ax.plot_surface(xx, yy, zz, cmap='viridis', alpha=0.5)
    #ax.set_title('Surface plot after ', iteration, ' generations')

    for tup in population:
        ax.scatter(tup[0], tup[1],
                   #rosenBrockFunc(tup[0], tup[1]),
                   rastriginFunc(tup[0], tup[1]),
                   c='r', marker='o', alpha=0.5)
    ax.view_init(60,35)
    plt.pause(0.001)
    

init(10)
loops = 0
while (fitnessMean < 99 and loops < 1000):
    train()
<<<<<<< HEAD
# plt.show()
=======
    loops += 1
    display(loops)
    print(loops)
print("Fitness Mean: " + str(fitnessMean))
average()
>>>>>>> e8b37183e9f420bf8442817cd751b63ad8498206
