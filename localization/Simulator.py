from pygame.locals import *
import pygame
import math
from Obstacle import Obstacle
from Robot import Robot
from kalmantest import poseTracking
import numpy as np

# from pso.localization.Beacon import Beacon
from Beacon import Beacon
# from pso.localization.kalmantest import poseCalculationReal
from kalmantest import poseCalculationReal

keepRunning = True
timeTick = 0.6
tickRate = 13.0
tick = 0

circle: any
obstacleList = []
beaconList: [Beacon] = []
# setting screen width and height
screenWidth = 640
screenHeight = 480
# setting object radius
circleRadius = 20
changePos = 25
# setting grid margin, and blocks size
marginSize = 30
blockSize = 25
ellipseSize = (0, 0, 100, 50)

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (200, 200, 200)

screen: any

circleSurf: any
obstacleList: any
obstacleSurf: any
clock: any
font_obj: any
FPS = 40

startingLocation = [[250, 300], [450, 300], [150, 150], [450, 400], [250, 50]]
visitedGrids = []
ellipseHist = []
predictLine = []
robots: [Robot]

epsilonT: np.array
miuT: np.array


def init():
    global clock
    global circleSurf
    global circleObj
    global screen
    global font_obj
    global visitedGrid
    global robot
    global epsilonT
    global miuT

    robot = Robot(circleRadius, [startingLocation[0][0], startingLocation[0][1], 0], [0, 0], 0)
    print("init Objects")

    sigmax2 = 1
    sigmay2 = 1
    sigmaTheta2 = 0.1
    epsilonT = np.array([[sigmax2, 0, 0], [0, sigmay2, 0], [0, 0, sigmaTheta2]])

    miuT = np.array([robot.xCoord, robot.yCoord, robot.angle])

    initMap2()

    print("init display")
    # initiates pygame for the simulation of an object
    pygame.init()
    # set the screen size as per requirement
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(white)
    font_obj = pygame.font.Font('freesansbold.ttf', 11)

    # setup a surface for the circle to displayed on
    circleSurf = pygame.Surface(((2 * circleRadius), (2 * circleRadius)), pygame.SRCALPHA)
    # make the background white in color
    circleSurf.fill((255, 255, 255, 0))
    # setting the initial position
    x = circleRadius
    y = circleRadius
    # the circle created will represent the object or robot which will move based on key inputs
    # the parameters for drawing a circle are these - (Surface, color, pos, radius, width=0)
    circleObj = pygame.draw.circle(circleSurf, red, (x, y), circleRadius)
    screen.blit(screen, circleObj)
    # addObstacle()
    # for obstacle in obstacleList:
    #   print(obstacle)
    pygame.display.update()
    # circleSurf.blit(screen, (100,100))
    # the function blit creates the initially drawing based on the settings
    FPS = 30
    clock = pygame.time.Clock()
    visitedGrid = np.full((64, 48), False)

    print("init end")


def initMap():
    global obstacleList
    global beaconList

    thickness = 5
    obstacleList.append(Obstacle([0, 0], [0, screenHeight], thickness))
    obstacleList.append(Obstacle([0, screenHeight], [screenWidth, screenHeight], thickness))
    obstacleList.append(Obstacle([screenWidth, screenHeight], [screenWidth, 0], thickness))
    obstacleList.append(Obstacle([screenWidth, 0], [0, 0], thickness))

    obstacleList.append(Obstacle([100, 40], [100, 100], thickness))
    obstacleList.append(Obstacle([300, 450], [300, 240], thickness))

    beaconList.append(Beacon(0, 0, 0))
    beaconList.append(Beacon(0, screenHeight, 1))
    beaconList.append(Beacon(screenWidth, 0, 2))
    beaconList.append(Beacon(screenWidth, screenHeight, 3))


def initMap2():
    global obstacleList
    global beaconList

    thickness = 5
    obstacleList.append(Obstacle([0, 0], [0, screenHeight], thickness))
    obstacleList.append(Obstacle([0, screenHeight], [screenWidth, screenHeight], thickness))
    obstacleList.append(Obstacle([screenWidth, screenHeight], [screenWidth, 0], thickness))
    obstacleList.append(Obstacle([screenWidth, 0], [0, 0], thickness))

    # obstacleList.append(Obstacle([150, 150], [450, 150], thickness))
    obstacleList.append(Obstacle([100, 250], [100, 350], thickness))
    obstacleList.append(Obstacle([400, 150], [400, 300], thickness))
    obstacleList.append(Obstacle([220, 150], [400, 150], thickness))
    obstacleList.append(Obstacle([150, 350], [400, 480], thickness))
    obstacleList.append(Obstacle([100, 350], [150, 350], thickness))

    # obstacleList.append(Obstacle([300, 450], [300, 240], thickness))

    beaconList.append(Beacon(0, 0, 0))
    beaconList.append(Beacon(0, screenHeight, 1))
    beaconList.append(Beacon(screenWidth, 0, 2))
    beaconList.append(Beacon(screenWidth, screenHeight, 3))
    beaconList.append(Beacon(220, 150, 4))
    beaconList.append(Beacon(100, 350, 4))
    beaconList.append(Beacon(400, 300, 4))
    beaconList.append(Beacon(150, 350, 4))
    beaconList.append(Beacon(100, 250, 4))
    beaconList.append(Beacon(400, 150, 4))


def update():
    global clock
    global tickRate
    global tick
    global obstacleList
    global FPS
    global robot

    clock.tick(FPS)
    # print(clock)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            handleInput()

    tick += 1
    move(robot, tick)


def handleInput():
    global keepRunning
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        keepRunning = False
        return
    if keys[pygame.K_w]:
        # print("positive increment of left wheel motor speed")
        robot.speedInc()
        return
    if keys[pygame.K_s]:
        # print("negative increment of left wheel motor speed")
        robot.speedDec()
        # print("SAVING")
        # controller.savePopulation("networkWeights/robotSave")
        return

    if keys[pygame.K_d]:
        # print('You just pressed d')
        robot.angleInc()
        return
    if keys[pygame.K_a]:
        # print('You just pressed a')
        robot.angleDec()
        return
    if keys[pygame.K_o]:
        # print("positive increment of right wheel motor speed")
        # robot.xCoord += changePos
        # robots[1].rightWheelInc()
        return
    if keys[pygame.K_l]:
        # print("negative increment of right wheel motor speed")
        # robot.xCoord -= changePos
        # robots[1].rightWheelDec()
        print("Loading")
        # controller.loadPopulation("networkWeights/robotSave")
        # reset()
        return
    if keys[pygame.K_x]:
        # print("both motor speeds are zero")
        robot.stop()


def move(robot: Robot, tick):
    global circleSurf
    global circleObj
    global timeTick

    # background.clamp_ip(screen)
    robot.updateLocation(timeTick, obstacleList)
    screen.fill(white)
    drawGrid()
    doLocalization(robot)
    drawEllipse(tick, robot)
    updateGrid(robot.xCoord, robot.yCoord, robot)
    addObstacle()
    screen.blit(circleSurf, (robot.xCoord - circleRadius, robot.yCoord - circleRadius))
    startLoc = [robot.xCoord, robot.yCoord]
    endLoc = [robot.xCoord + np.cos(robot.forwardAngle) * circleRadius,
              robot.yCoord + np.sin(robot.forwardAngle) * circleRadius]
    pygame.draw.line(screen, black, startLoc, endLoc, 2)
    # displayRobotSensor(robot)  # didn t want to try to  mix up the sequence
    displayVelocityOnScreen(1)
    pygame.display.update()


def updateGrid(xCoord, yCoord, robot):
    global circleSurf
    global visitedGrid
    global visitedGrids

    xind = int(xCoord / 10)
    yind = int(yCoord / 10)
    visitedGrids.append([xind, yind])
    # print(xind, yind)
    if 0 <= xind < 64 and 0 <= yind < 48:
        visitedGrid[xind][yind] = True

    numDust = np.sum(visitedGrid)
    dustLoc = np.nonzero(visitedGrid)
    # print(len(visitedGrids))
    for i in range(1, len(visitedGrids)):
        # for i in range(numDust):
        # if robot.id == 1:
        # pygame.draw.circle(screen, red, (dustLoc[0][i] * 10, dustLoc[1][i] * 10), 13)
        pygame.draw.line(screen, black, (visitedGrids[i - 1][0] * 10, visitedGrids[i - 1][1] * 10),
                         (visitedGrids[i][0] * 10, visitedGrids[i][1] * 10), 1)
    robot.areaCovered = numDust


def addObstacle():
    global beaconList
    # screen.fill(white)
    for obstacle in obstacleList:
        obstacleObj = pygame.draw.line(screen, black,
                                       (obstacle.startLoc[0], obstacle.startLoc[1]),
                                       (obstacle.endLoc[0], obstacle.endLoc[1]), obstacle.thickness)
        # screen.blit(screen, obstacleObj)
    for beacon in beaconList:
        beaconObj = pygame.draw.circle(screen, blue, [beacon.x, beacon.y], 15)


def drawGrid():
    global screen
    # draw the grid
    for i in range(0, screenWidth, blockSize):
        i = i + 10
        pygame.draw.line(screen, grey, (i, 0), (i, screenHeight), 2)
    for j in range(0, screenHeight, blockSize):
        j = j + 10
        pygame.draw.line(screen, grey, (0, j), (screenWidth, j), 2)


def displayVelocityOnScreen(ind):
    global robots
    font = pygame.font.Font('freesansbold.ttf', 12)
    textLeft = ('Speed: ' + str(robot.speed))
    textLeft = font.render(textLeft, True, black)
    text_rect_obj = textLeft.get_rect()
    text_rect_obj.center = ((robot.xCoord, robot.yCoord))
    screen.blit(textLeft, (550, 10))
    textRight = ('Angle: ' + str(robot.angle))
    textRight = font.render(textRight, True, black)
    text_rect_obj = textRight.get_rect()
    text_rect_obj.center = (robot.xCoord, robot.yCoord)
    screen.blit(textRight, (550, 25))


def doLocalization(robot: Robot):
    global beaconList
    global epsilonT
    global miuT
    global tick
    global epsilonTP1
    global miuTP1

    uT = np.array([robot.speed, robot.angle])
    # addend motion modle error
    uT = uT + np.array([np.random.normal(0, 0.1), np.random.normal(0, 0.01)])

    # mock, not sure how this is supposed to behave when less than 3 beacons
    zt, inRangeBeacon = poseCalculationReal(beaconList, robot, miuT)

    miuTP1, epsilonTP1 = poseTracking(timeTick, uT, zt, miuT, epsilonT)
    epsilonT = epsilonTP1
    miuT = miuTP1
    if tick % 100 == 0:
        print("Beacons in range: " + str(inRangeBeacon))
        print("Estimated epsilonTP1: \n" + str(epsilonTP1))
        print("Estimated muiT+1: \n" + str(miuTP1))
        print("Real muiT+1: \n" + str([robot.xCoord, robot.yCoord, robot.forwardAngle]))


def drawEllipse(tick, robot: Robot):
    global epsilonTP1
    global ellipseHist
    global miuT

    predictLine.append([miuT[0], miuT[1]])
    #if tick % 100 == 0:
    ellipseSize = [miuT[0] - 0.5 * epsilonTP1[0, 0], miuT[1] - 0.5 * epsilonTP1[1, 1], epsilonTP1[0, 0], epsilonTP1[1, 1]]
    # ellipseSize = [miuTP1[0] - 25, miuTP1[0] - 25, 50, 50]
    if (ellipseSize[2] + ellipseSize[3] > 5 ):
        ellipseHist.append(ellipseSize)
    else:
        ellipseHist = []

    for i in range(1, len(ellipseHist)):
        #print("drawing elli: " + str(ellipseHist[i - 1]))
        #print("drawing robot xchoord: " + str(robot.xCoord) + ", y: " + str(robot.yCoord))
        pygame.draw.ellipse(screen, green, ellipseHist[i - 1], 1)
        #pygame.gfxdraw.ellipse(screen, ellipseHist[i - 1], epsilonTP1[0,1], epsilonTP1[1,1], Color("Pink"))
        
    if (len(predictLine) > 1):
        for i in range(1, len(predictLine)):
            pygame.draw.line(screen, red, predictLine[i-1], predictLine[i], 1)
    #print("#######################")


init()

while keepRunning:
    update()

pygame.quit()
