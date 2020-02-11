import numpy as np
import random
import matplotlib.pyplot as plt
import math
#from particle import Particle

numOfIterations = 100
numOfParticles = 30
xMin = -5
xMax = 5
yMin = -5
yMax = 5
vMax = 1
numOfDim = 2
a = 0.9
b = 2
c = 2
targetError = 1e-6
target = 1
global globalBestPosition
global globalBest

#class Particle:
#    def __init__(self):
#        random.seed()
#        self.position = np.array([random.randrange(xMin, xMax), random.randrange(yMin, yMax)])
#        self.velocity = np.array([random.randrange(0, vMax), random.randrange(0, vMax)])
#        self.bestPosition = self.position
#        self.bestValue = rosenBrockFunc(self.position[0], self.position[1]) 
        # self.bestVal = rastriginFunc(self.position[0], self.position[1])


def rosenBrockFunc(x, y):
    a = 0
    b = 100
    return ((a-x) ** 2 + b * (y - x ** 2) ** 2)


def rastriginFunc(x, y):
    return (10 * numOfDim + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x)))


def initSwarm():
    global particleList
    global particleBestPosition
    global globalBest
    particleList = [0] * numOfParticles
    for i in range(numOfParticles):
        particleList.append(Particle())

    globalBestPosition = np.asarray([random.randrange(xMin, xMax), random.randrange(yMin, yMax)])
    globalBest = rosenBrockFunc(globalBestPosition[0], globalBestPosition[1])
    # globalBest = rastrigiinFunc(globalBestPosition[0], globalBestPosition[1])


def updateParticle(particle: Particle):
    global globalBest
    global globalBestPosition

    random.seed()
    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)

    newVelocity = a * particle.velocity \
            + b * r1 * (particle.bestPosition - particle.position) \
            + c * r2 * (globalBestPosition - particle.position)

    newVelocity = limitVelocity(newVelocity)
    currentLocalBest = rosenBrockFunc(particle.position[0], particle.position[1])
    # currentLocalBest = rastriginFunc(particle.position[0], particle.position[1])

    if (currentLocalBest < globalBest):
        particle.bestVal = currentLocalBest
        globalBest = currentLocalBest
        globalBestPosition = particle.position
    
    error = np.sqrt((particle.position[0] - globalBestPosition[0]) ** 2 + (particle.position[1] - globalBestPoistion[1]) ** 2)

    return error

    
def limitVelocity(velocity):
    vectorSum = 0
    for i in velocity:
        vectorSum = vectorSum + i ** 2
        
    if(vectorSum > vMax):
        velocity = velocity * (vMax/np.math.sqrt(vectorSum))
        return velocity
    return velocity


def display(iteration):
    global resMemList
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)

    X, Y = np.meshgrid(x, y)
    Z = rosenBrockFunc(X, Y)
    # Z = rastriginFunx(X, Y)

    fig = plt.figure(0)
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    ax.set_title('Surface plot after ', iteration, ' iterations')

    for particle in particleList:
        ax.scatter(particle.position[0], particle.position[1], 2000, c='r', marker='x')

    plt.show()

def update(iteration):
    global globalBestPosition
    global globalBest
    distTobeSum = 0
    print('Iteration number: ', iteration + 1)
    for particle in particleList:
        distTobeSum = distTobeSum + updateParticle(particle)
    print('Global Best Position:', globalBestPosition, ' ,Global Best Value: ', globalBest)
    print('Distance to best: ', distTobeSum)
    if(iteration % 10 == 0):
        a = a / 1.1
        display(iteration)


initSwarm()
for i in range(numOfIterations):
    update(i)
display()
