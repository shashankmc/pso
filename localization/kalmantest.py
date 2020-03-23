import math

import numpy as np

from pso.localization.Beacon import Beacon
from pso.localization.Robot import Robot

def nCr(n,k):
    f = math.factorial
    return f(n) / (f(k) * f(n-k))

def poseCalculationReal(beaconList: [Beacon], robot: Robot, miuT):
    # in range?
    counter = 0
    for beacon in beaconList:
        distance = np.sqrt((beacon.x - robot.xCoord) ** 2 + (beacon.y - robot.yCoord) ** 2)
        if distance < 150:
            counter += 1

    if counter > 2:
        possibleTriangulations = int(nCr(counter, 3))
        noise = [np.mean(np.random.normal(0, 1, possibleTriangulations)), np.mean(np.random.normal(0, 1, possibleTriangulations)), np.mean(np.random.normal(0, 0.1, possibleTriangulations))]
        result = np.array([robot.xCoord, robot.yCoord, robot.forwardAngle]) + noise
        return result, counter
    else:
        return np.array([0,0,0]), counter
        #return miuT, counter


def poseTracking(deltaTime, uT, zT, miuTminusOne, epsilonTminusOne):
    # uT is change / action / v, w
    # miu is position at time t

    # z calculated pose with sensor noise from beacons

    A = np.identity(3)
    C = np.identity(3)

    B = np.array(
        [[deltaTime * np.cos(miuTminusOne[2]), 0], [deltaTime * np.sin(miuTminusOne[2]), 0], [0, deltaTime]])

    # R = Covariance, noise of motion model epsilon
    # Init with small values
    sigmaRx2 = 1
    sigmaRy2 = 1
    sigmaRTheta2 = 0.1
    R = np.array([[sigmaRx2, 0, 0], [0, sigmaRy2, 0], [0, 0, sigmaRTheta2]])

    # Q = Covriance, noise of sensor model delta?!
    # init with small values
    sigmaQx2 = 1
    sigmaQy2 = 1
    sigmaQTheta2 = 0.1
    Q = np.array([[sigmaQx2, 0, 0], [0, sigmaQy2, 0], [0, 0, sigmaQTheta2]])

    #print("KalmanFilter")
    #print("Prediction")

    muiTBar = np.matmul(A, miuTminusOne) + np.matmul(B, uT)
    #print("Prediction2,  muiTBar: " + str(muiTBar))

    epsilonTBar = np.matmul(A, np.matmul(epsilonTminusOne, np.transpose(A))) + R
    #print("prediction3 epsilonTHat: " + str(epsilonTBar))

    #print("Correction")

    ect = np.matmul(epsilonTBar, np.transpose(C))
    cecplusq = np.matmul(C, np.matmul(epsilonTBar, np.transpose(C))) + Q
    inverse = np.linalg.inv(cecplusq)
    Kt = np.matmul(ect, inverse)
    #print("Correction4 Kt: " + str(Kt))

    zCMui = zT - np.matmul(C, muiTBar)
    miuT = muiTBar + np.matmul(Kt, zCMui)
    #print("Correction5 miuT: " + str(miuT))

    ikc = np.identity(3) - np.matmul(Kt, C)
    epsilonT = np.matmul(ikc, epsilonTBar)
    #print("Correction6 epsilonHat: " + str(epsilonT))
    #print("Return")

    return miuT, epsilonT

"""
robot: Robot

uT = np.array([(robot.vLeft + robot.vRight) / 2, (robot.vRight - robot.vLeft) / robot.length])

beaconList: []
zt = poseCalculationReal(beaconList, robot) + np.random.normal(0, 0.1, 3)

# position of robot with beacons in range
# triangulate,
# add noise
# multi feature take mean


muiT = np.array([robot.xCoord, robot.yCoord, robot.forwardAngle])

sigmax2 = 1
sigmay2 = 1
sigmaTheta2 = 1
epsilonT = np.array([[sigmax2, 0, 0], [0, sigmay2, 0], [0, 0, sigmaTheta2]])

print(poseTracking(0.2, uT, zt, muiT, epsilonT))
"""