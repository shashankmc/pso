#  Assignment 1 - Particle Swarm Optmisation - Group 4      #
#  Group Member: Yannick, Arthur, Shashank                  #
#  Code:                                                    #
#  1.Yannick - particle update, rosenbrock cost function    #
#  2.Arthur - rastrigin, gradient descent cost function     #
#  3.Shashank - plotting, rosenbrock cost function          #
#############################################################
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import random
from particle_group4 import Particle

a = 0.9
b = 2
c = 2
vMax = 0.25 
tick = 0
globalBest = 0
globalBestLocation = np.array([1, 1])
particleList = []

def rosenbrock(x, y):
    ar = 0
    br = 100
    result = (ar - x) ** 2 + br * (y - x ** 2) ** 2
    return result

def rastrigin_easy(x,y):
    n = 2
    sum = 10 * n
    sum += (x ** 2 - 10 * np.cos(2 * np.pi * x))
    sum += (y ** 2 - 10 * np.cos(2 * np.pi * y))
    return sum 

def rastrigin(x):
    # n = len(x) 
    n = 2
    sum = 10 * n
    for i in range(0,n):
        sum += (x ** 2 - 10 * np.cos(2 * np.pi * x))
    return sum 


def gradient_descent(decendrate, tolerance, xMin, xMax, yMin, yMax):     
    currentx = random.randrange(xMin, xMax)
    currenty = random.randrange(yMin, yMax)
    currentvalue = usedfunction(currentx, currenty)

    while True: 
        if (decendrate<=tolerance):
            break

        direction = 1
        bestnext = usedfunction(currentx + decendrate, currenty)
        if (usedfunction(currentx - decendrate, currenty) < bestnext):
            direction = 2
            bestnext = usedfunction(currentx - decendrate, currenty)
        if (usedfunction(currentx, currenty + decendrate) < bestnext):
            direction = 3
            bestnext = usedfunction(currentx, currenty + decendrate)
        if (usedfunction(currentx, currenty - decendrate) < bestnext):
            direction = 4
            bestnext = usedfunction(currentx, currenty - decendrate)
        if (bestnext > currentvalue):
            decendrate /= 2
        else: 
            if (direction==1):
                currentx += decendrate
                currentvalue = usedfunction(currentx,currenty)
            elif (direction==2):
                currentx -= decendrate
                currentvalue = usedfunction(currentx, currenty)
            elif (direction==3):
                currenty += decendrate
                currentvalue = usedfunction(currentx,currenty)
            elif (direction==4):
                currenty -= decendrate
                currentvalue = usedfunction(currentx,currenty)
    print("Position: [" + str(currentx) + "," + str(currenty) + "]")
    print("Value: " + str(currentvalue))


# function will be called to initialise the swarm with local and global values
def initSwarm(numPart: int, xMin: float, xMax: float, yMin: float, yMax: float):
    global particleList
    global globalBestLocation
    global globalBest
    # create particles and append them to global list
    for la in range(1, numPart):
        localBestLoc = [random.randrange(xMin, xMax), random.randrange(yMin, yMax)]
        localBestVal = usedfunction(localBestLoc[0], localBestLoc[1])
        particleList.append(Particle([random.randrange(xMin, xMax), random.randrange(yMin, yMax)],
                                     [random.uniform(0, 1), random.uniform(0, 1)],
                                     localBestLoc, localBestVal))
    # Setting globalBest
    globalBestLocation = np.asarray([random.randrange(xMin, xMax), random.randrange(yMin, yMax)])
    globalBest = usedfunction(globalBestLocation[0], globalBestLocation[1])


def updateParticle(particle: Particle):
    global globalBest
    global globalBestLocation
    # create random arrays for randomness
    R1 = random.uniform(0, 1)  # np.asarray([random.uniform(0, 1), random.uniform(0, 1)])
    R2 = random.uniform(0, 1)  # np.asarray([random.uniform(0, 1), random.uniform(0, 1)])
    # velocity equation
    unlimitedV = a * particle.velocity \
                 + b * R1 * (particle.bestLocation - particle.location) \
                 + c * R2 * (globalBestLocation - particle.location)
    particle.velocity = limitVMax(unlimitedV)
    # location function from the script
    particle.location = particle.location + particle.velocity * 1
    # if new local best => update local best
    if usedfunction(particle.location[0], particle.location[1]) < particle.bestValue:
        particle.bestValue = usedfunction(particle.location[0], particle.location[1])
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

    if (vectorSum > vMax):
        return velocity * (vMax / np.math.sqrt(vectorSum))
    else:
        return velocity


def update():
    global a
    # global counter
    global tick
    tick = tick + 1
    global distToBestSum
    distToBestSum = 0
    # update every particle
    for particle in particleList:
        distToBestSum = distToBestSum + updateParticle(particle)
    # every iteration to be plotted 
    if tick % 1000 == 0:
        a = 0.4
    display()

def display():
    global tick
    global globalBestLocation
    global globalBest
    # creates an array from -2 to 2 with 100 steps
    x = np.linspace(-4, 4, 100)
    y = np.linspace(-1, 3, 100)

    # this meshgrid transform needed for plot
    xx, yy = np.meshgrid(x, y)

    # evaluating every z value for the variable grid
    zz = usedfunction(xx, yy)

    # plot stuff
    fig = plt.figure(0)
    ax = plt.axes(projection='3d')
    ax.plot_surface(xx, yy, zz, cmap='viridis', alpha=0.5)
    # ax.contour3D(xx, yy, zz, 50, cmap='binary')
    ax.set_title('Surface plot after ' + str(tick) + " iteration(s)")
    # Iterates over particle and adds a dot to ax for each current location location
    for particle in particleList:
        #ax.scatter(particle.location[0], particle.location[1], 2000, c='r', marker='x')
        ax.scatter(particle.location[0], particle.location[1],
                   usedfunction(particle.location[0], particle.location[1]),
                   c='r', marker='>', alpha=0.5)
    ax.scatter(globalBestLocation[0], globalBestLocation[1], globalBest, c='k', marker='x')
    ax.view_init(60,35)
    if(tick % 100 == 0):
        plt.savefig('fig%d.png' %tick)
    plt.pause(0.001)


usedfunction = rosenbrock
# usedfunction = rastrigin_easy
initSwarm(100, -4, 4, -1, 3)
for i in range(1000):
    update()
    #print("iteration: " + str(i)) 
print("Global Best: " + str(globalBestLocation))
print("Average Error: " + str(distToBestSum/100.))
# display()
plt.show()
#gradient_descent(10,0.0001,-2,2,-1,3)
