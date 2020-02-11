from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import random

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

from particle_yannick import Particle

a = 0.9
b = 2
c = 2

vMax = 1

tick = 0
globalBest = 2000
globalBestLocation = np.array([1, 1])
particleList = []

displayShow = 10

# not yet done, needs to be tuples
resultMemoryList = []


def rosenbrock(x, y):
    ar = 2
    br = 100
    result = (ar - x) ** 2 + br * (y - x ** 2) ** 2
    return result


def initSwarm(numPart: int, xMin: float, xMax: float, yMin: float, yMax: float):
    global particleList
    global globalBestLocation
    global globalBest
    # create particles and append them to global list
    for la in range(1, numPart):
        localBestLoc = [random.randrange(xMin, xMax), random.randrange(yMin, yMax)]
        localBestVal = rosenbrock(localBestLoc[0], localBestLoc[1])
        particleList.append(Particle([random.randrange(xMin, xMax), random.randrange(yMin, yMax)],
                                     [random.uniform(0, 1), random.uniform(0, 1)],
                                     localBestLoc, localBestVal))
    # Setting globalBest
    globalBestLocation = np.asarray([random.randrange(xMin, xMax), random.randrange(yMin, yMax)])
    globalBest = rosenbrock(globalBestLocation[0], globalBestLocation[1])


def updateParticle(particle: Particle, saveParticalHistory: bool = False):
    global globalBest
    global globalBestLocation
    # print("update particle location: " + str(particle))

    # create random arrays for randomness
    R1 = random.uniform(0, 1)  # np.asarray([random.uniform(0, 1), random.uniform(0, 1)])
    R2 = random.uniform(0, 1)  # np.asarray([random.uniform(0, 1), random.uniform(0, 1)])

    # speed function from the script
    unlimitedV = a * particle.velocity \
                 + b * R1 * (particle.bestLocation - particle.location) \
                 + c * R2 * (globalBestLocation - particle.location)

    particle.velocity = limitVMax(unlimitedV)
    # print("Unlimited V: " + str(unlimitedV) + ", limitedV: " + str(particle.velocity))
    # location function from the script
    particle.setLocation(particle.location + particle.velocity * 1, saveParticalHistory)

    # if new local best => update local best
    if rosenbrock(particle.location[0], particle.location[1]) < particle.bestValue:
        particle.bestValue = rosenbrock(particle.location[0], particle.location[1])
        particle.bestLocation = particle.location

        # if new globalb best => update global best
        if particle.bestValue < globalBest:
            globalBest = particle.bestValue
            globalBestLocation = particle.bestLocation

    error = np.sqrt((particle.location[0] - globalBestLocation[0]) ** 2
                    + (particle.location[1] - globalBestLocation[1]) ** 2)

    return error


def limitVMax(velocity: np.array):
    global vMax
    vectorSum = 0
    for val in velocity:
        vectorSum = vectorSum + val ** 2

    if vectorSum > vMax:
        velocity = velocity * (vMax / np.math.sqrt(vectorSum))

    return velocity


def update():
    global a
    global displayShow
    # global counter
    global tick
    tick = tick + 1
    distToBestSum = 0

    print("tick value: " + str(tick) + ", a = " + str(a))
    print("Global best position: " + str(globalBestLocation) + ", globalBest: " + str(globalBest))
    # update every particle
    for particle in particleList:
        distToBestSum = distToBestSum + updateParticle(particle)

    print("Distances to gBest: " + str(distToBestSum))
    # every tenth iteration a display
    if tick % displayShow == 0:
        a = a / 1.1
        display()

    return distToBestSum


def display():
    global resultMemoryList
    # creates an array from -2 to 2 with 100 steps
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-1, 3, 100)

    # this meshgrid transform needed for plot
    xx, yy = np.meshgrid(x, y)

    # evaluating every z value for the variable grid
    zz = rosenbrock(xx, yy)

    # plot stuff
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(xx, yy, zz, cmap='viridis', edgecolor='none', alpha=0.8)
    ax.set_title('Surface plot after ' + str(tick) + " iteration(s)")

    # Iterates over particle and adds a dot to ax for each current location location
    for particle in particleList:
        #ax.scatter(particle.location[0], particle.location[1], 2000, c='r', marker='x')
        ax.scatter(particle.location[0], particle.location[1],
                   rosenbrock(particle.location[0], particle.location[1]),
                   c='r', marker='x')
    plt.show()


initSwarm(10, -2, 2, -1, 3)

for i in range(displayShow*10):
    if update() < 0.002:
        print("Stopped pso because a good solution has been found!")
        print("Global best position: " + str(globalBestLocation) + ", globalBest: " + str(globalBest))
        display()
        break

