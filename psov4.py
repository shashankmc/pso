import numpy as np
import random

def benchMarkFunc(position):
    ## Rosenbrock function
    a = 0
    ## No idea if b value should be set to 100
    b = 100
    return (position[0]**2 + (b *(position[1] - position[0]**2)**2))

## initialising variables for particle action
weightAHigh = 0.9
weightALow = 0.4
b = 2
c = 2
## haven't understood the use of target or targetError
target = 1
targetError = 1e-6
numOfParticles = 30
numOfIterations = 100

## initialising particle position and velocity
particlePos = np.array([np.array([(-1)**(bool(random.getrandbits(1))) * random.random()*20,(-1)**(bool(random.getrandbits(1))) * random.random()*20]) for _ in range(numOfParticles)])
particleBestPos = particlePos
## initiating particleBestPosValue with float inf
## as the minimal value is required
particleBestPosValue = np.array([float('inf') for _ in range(numOfParticles)])
globalBestPosValue = float('inf')
globalBestPos = np.array([float('inf'),float('inf')])
particleVel = np.array([np.array([0,0]) for _ in range(numOfParticles)])

## the algorithm for particle swarm optimisation
for iterations in range(numOfIterations):
    for i in range(numOfParticles):
        currentFitness = benchMarkFunc(particlePos[i])
        print(currentFitness, ' ', particlePos[i])

        if(particleBestPosValue[i] > currentFitness):
            particleBestPosValue[i] = currentFitness
            particleBestPos[i] = particlePos[i]

        if(globalBestPosValue > currentFitness):
            globalBestPosValue = currentFitness
            globalBestPos = particlePos[i]

    if(abs(globalBestPosValue - target) < targetError):
        break
    if(iterations > 1000):
        a = weightALow
    else:
        a = weightAHigh

    for i in range(numOfParticles):
        newVelocity = (a*particleVel[i] + (b * random.random()) * (particleBestPos[i] - particlePos[i]) + (c * random.random()) * (globalBestPos - particlePos[i]))
        newPosition = newVelocity + particlePos [i]
        particlePos[i] = newPosition

print("Global Best Position: ", globalBestPos, " with iteration number ", iterations)
