from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import random

from particle import Particle

a = 0.4
b = 2
c = 2

vMax = 1

tick = 0
globalBest = 2000
globalBestLocation = np.array([1, 1])
particleList = []


def rosenbrock(x, y):
    ar = 0
    br = 100
    result = (ar - x) ** 2 + br * (y - x ** 2) ** 2
    return result


def initSwarm(numPart: int, xMin: float, xMax: float, yMin: float, yMax: float):
    global particleList
    # create particles and append them to global list
    for la in range(1, numPart):
        particleList.append(Particle([random.randrange(xMin, xMax), random.randrange(yMin, yMax)],
                                     [random.uniform(0, 1), random.uniform(0, 1)]))


def updateParticle(particle: Particle):
    global globalBest
    global globalBestLocation
    print("update particle location: " + str(particle))

    # create random arrays for randomness
    R1 = np.asarray([random.uniform(0, 1), random.uniform(0, 1)])
    R2 = np.asarray([random.uniform(0, 1), random.uniform(0, 1)])

    # speed function from the script
    unlimitedV = a * particle.velocity \
                        + b * R1 * (particle.bestLocation - particle.location) \
                        + c * R2 * (globalBestLocation - particle.location)

    particle.velocity = limitVMax(unlimitedV)

    # location function from the script
    particle.location = particle.location + particle.velocity * 1

    # if new local best => update local best
    if rosenbrock(particle.location[0], particle.location[1]) < particle.bestValue:
        particle.bestValue = rosenbrock(particle.location[0], particle.location[1])
        # if new globalb best => update global best
        if particle.bestValue < globalBest:
            globalBest = particle.bestValue

    return particle


def limitVMax(velocity: np.array):
    global vMax
    vectorSum = 0
    for val in velocity:
        vectorSum = vectorSum + val ** 2

    velocity = velocity * (vMax / np.math.sqrt(vectorSum))
    return velocity


def update():
    # global counter
    global tick
    tick = tick + 1
    print("tick value: " + str(tick))

    # update every particle
    for particle in particleList:
        updateParticle(particle)

    # every tenth iteration a display
    if tick % 1000 == 0:
        display()


def display():
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
    ax.plot_surface(xx, yy, zz, cmap='viridis', edgecolor='none')
    ax.set_title('Surface plot after ' + str(tick) + " iteration(s)")

    # Iterates over particle and adds a dot to ax for each current location location
    for particle in particleList:
        ax.scatter(particle.location[0], particle.location[1], 2000, c='r', marker='x')

    plt.show()


initSwarm(15, -1, 1, -1, 1)

for i in range(10000):
    update()

display()
