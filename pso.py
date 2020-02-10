from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import random

numOfParticles = 30
numOfIterations = 100
a = 0.9
b = 2
c = 2
vMax = 8
tick = 0
particleList = []
numOfDim = 2
xMin = -20
xMax = 20
yMin = -20
yMax = 20

#not yet done, needs to be tuples
resultMemoryList =[]


class Particle:
    def __init__(self):
        self.position = np.array([random.randrange(xMin, xMax), random.randrange(yMin, yMax)]) 
        self.velocity = np.array([random.uniform(-1, vMax), random.uniform(-1, vMax)]) 
        self.bestPosition = self.position 
        # self.bestPosVal = rastriginFunc(self.position[0], self.position[1]) 
        self.bestPosVal = rosenBrockFunc(self.position[0], self.position[1]) 


def rosenBrockFunc(x, y):
    ar = 0
    br = 100
    return ((ar - x) ** 2 + br * (y - x ** 2) ** 2)


def rastriginFunc(x, y):
    return (10 * numOfDim + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x)))


def initSwarm():
    global particleList
    global globalBestPosition
    global globalBest
    # create particles and append them to global list
    for la in range(1, numOfParticles):
        particleList.append(Particle())
    # Setting globalBest
    globalBestPosition = np.asarray([random.randrange(xMin, xMax), random.randrange(yMin, yMax)])
    
    globalBest = rosenBrockFunc(globalBestPosition[0], globalBestPosition[1])
    # globalBest = rastriginFunc(globalBestPosition[0], globalBestPosition[1])


def updateParticle(particle: Particle):
    global globalBest
    global globalBestPosition

    # create random arrays for randomness
    r1 = random.uniform(0, 1)  # np.asarray([random.uniform(0, 1), random.uniform(0, 1)])
    r2 = random.uniform(0, 1)  # np.asarray([random.uniform(0, 1), random.uniform(0, 1)])

    # speed function from the script
    newVelocity = a * particle.velocity \
                 + b * r1 * (particle.bestPosition - particle.position) \
                 + c * r2 * (globalBestPosition - particle.position)

    particle.velocity = limitVMax(newVelocity)
    # location function from the script
    particle.position = particle.position + particle.velocity * 1

    # if new local best => update local best
    newLocalVal = rosenBrockFunc(particle.position[0], particle.position[1])
    # newLocalVal = rastriginFunc(particle.position[0], particle.position[1])
    if  newLocalVal < particle.bestPosVal:
         particle.bestValue = newLocalVal 
         particle.bestPosition = particle.position
         #if new global best => update global best
         if particle.bestValue < globalBest:
             globalBest = particle.bestValue
             globalBestPosition = particle.bestPosition

    error = np.sqrt((particle.position[0] - globalBestPosition[0]) ** 2
                    + (particle.position[1] - globalBestPosition[1]) ** 2)

    print("single error: " + str(error))
    return error


def limitVMax(velocity: np.array):
    vectorSum = 0
    for val in velocity:
        vectorSum = vectorSum + val ** 2

    if vectorSum > vMax:
        velocity = velocity * (vMax / np.math.sqrt(vectorSum))

    return velocity


def update(iteration):
    global a
    iteration = iteration + 1
    distToBestSum = 0
    if (iteration > 1000):
        a = 0.4
    print("Iteration: " + str(iteration) + ", a = " + str(a))
    print("Global best position: " + str(globalBestPosition) + ", globalBest: " + str(globalBest))
    # update every particle
    # Shashank doesn't understand this, please help
    for particle in particleList:
        distToBestSum = distToBestSum + updateParticle(particle)
    
    print("Distance to Best: " + str(distToBestSum))
    # every tenth iteration a display
    if iteration % 10 == 0:
        a = a / 1.1
        display(iteration)


def display(iteration):
    global resultMemoryList
    # figure 0 is fixed as animation is dependent on it.
    fig = plt.figure(0)
    ax = fig.add_subplot(111, projection='3d')
    # creates an array from -20 to 20 with 100 steps
    x = y = np.linspace(-20, 20, 100)

    # meshgrid transform for plot
    X, Y = np.meshgrid(x, y)
    # evaluating every z value for the variable grid
    Z = (rosenBrockFunc(X, Y)).reshape(X.shape) 
    # Z = rastriginFunc(X, Y)
    light = LightSource(90, 45)
    illuminates_surface = light.shade(Z, cmap=cm.cool)
    # plot stuff
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, linewidth=0, antialiased=False, facecolors=illuminates_surface, alpha=0.4)
    # Iterates over particle and adds a marker to ax for each current location location
    for particle in particleList:
        ax.scatter(particle.position[0], particle.position[1], 2000, color='r', s=100, alpha=0.5, marker='>', zorder=1)
    # plotting the global best to indicate the movement of the swarm
    ax.scatter(globalBestPosition[0], globalBestPosition[1], globalBest, color='k', s=100, alpha=1)
    ax.set_title('Particle movement after ' + str(iteration) + " iteration(s)")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('f(X,Y)')
    # for angle in range(0, 360):
    #     ax.view_init(45, angle)
    #     plt.draw()
    plt.pause(0.05)


initSwarm()

for i in range(100):
    update(i)
plt.show()
