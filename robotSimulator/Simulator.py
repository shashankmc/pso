from pygame.locals import *
import pygame
import math
from Obstacle import Obstacle
from Robot import Robot
import numpy as np
import random
from matplotlib import pyplot as plt
import pandas as pd
#from pso.robotSimulator.Controller import Controller
from Controller import Controller
#from pso.robotSimulator.Stat import Stat
from Stat import Stat

keepRunning = True
timeTick = 0.6
tickRate = 13.0
tick = 0

circle: any
obstacleList = []
# setting screen width and height
screenWidth = 640
screenHeight = 480
# setting object radius
circleRadius = 20
changePos = 25
# setting grid margin, and blocks size
marginSize = 30
blockSize = 25

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


#startingLocation = [[250, 300], [450, 300], [150, 150], [450, 400], [250, 50]]

#startingLocation = [[250, 300], [450, 300] ,[150, 150] ,[450, 400] ,[250, 50]]
startingLocation = [random.randrange(275, 475), random.randrange(200, 325)]
#startingLocation = [random.randrange(245, 355), random.randrange(125, 275)]
visitedGrids = []
robots: [Robot]


def init(popSize, mapNumber=1):
    global clock
    global circleSurf
    global circleObj
    global screen
    global font_obj
    global visitedGrids
    global robots
    robots = []
    print("init Objects")
    if mapNumber == 1:
        initMap()
    if mapNumber == 2:
        initMap2()
    if mapNumber == 3:
        initMap3()
    if mapNumber == 4:
        initMap4()


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
    visitedGrids = []
    for i in range(popSize):
        #rob = Robot(circleRadius, [startingLocation[0][0], startingLocation[0][1], 0], [0, 0], i)
        rob = Robot(circleRadius, (startingLocation[0], startingLocation[1]), [0, 0], i)
        robots.append(rob)
        visitedGrids.append(np.full((64, 48), False))
        displayRobotSensor(rob)

    print("init end")


def initMap():
    global obstacleList

    thickness = 5
    obstacleList.append(Obstacle([0, 0], [0, screenHeight], thickness))
    obstacleList.append(Obstacle([0, screenHeight], [screenWidth, screenHeight], thickness))
    obstacleList.append(Obstacle([screenWidth, screenHeight], [screenWidth, 0], thickness))
    obstacleList.append(Obstacle([screenWidth, 0], [0, 0], thickness))

    #obstacleList.append(Obstacle([100, 40], [100, 100], thickness))
    #obstacleList.append(Obstacle([300, 450], [300, 240], thickness))
    obstacleXPos = [250, 500]
    obstacleYPos = [175, 350]
    obstacleList.append(Obstacle([obstacleXPos[0], obstacleYPos[0]], [obstacleXPos[1], obstacleYPos[0]], thickness))
    obstacleList.append(Obstacle([obstacleXPos[1], obstacleYPos[0]], [obstacleXPos[1], obstacleYPos[1]], thickness))
    obstacleList.append(Obstacle([obstacleXPos[1], obstacleYPos[1]], [obstacleXPos[0], obstacleYPos[1]], thickness))
    obstacleList.append(Obstacle([obstacleXPos[0], obstacleYPos[1]], [obstacleXPos[0], obstacleYPos[0]], thickness))


def initMap2():
    global obstacleList

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


def initMap3():
    global obstacleList

    thickness = 5
    obstacleList.append(Obstacle([0, 0], [0, screenHeight], thickness))
    obstacleList.append(Obstacle([0, screenHeight], [screenWidth, screenHeight], thickness))
    obstacleList.append(Obstacle([screenWidth, screenHeight], [screenWidth, 0], thickness))
    obstacleList.append(Obstacle([screenWidth, 0], [0, 0], thickness))

    #obstacleList.append(Obstacle([100, 40], [100, 100], thickness))
    #obstacleList.append(Obstacle([300, 450], [300, 240], thickness))
    obstacleList.append(Obstacle([100, 100],[400, 200], thickness))
    obstacleList.append(Obstacle([400, 200],[400, 325], thickness))
    obstacleList.append(Obstacle([400, 325],[100, 400], thickness))
    obstacleList.append(Obstacle([100, 400],[100, 100], thickness))


def initMap4():
    global obstacleList

    thickness = 5
    obstacleList.append(Obstacle([0, 0], [0, screenHeight], thickness))
    obstacleList.append(Obstacle([0, screenHeight], [screenWidth, screenHeight], thickness))
    obstacleList.append(Obstacle([screenWidth, screenHeight], [screenWidth, 0], thickness))
    obstacleList.append(Obstacle([screenWidth, 0], [0, 0], thickness))

    #obstacleList.append(Obstacle([100, 40], [100, 100], thickness))
    #obstacleList.append(Obstacle([300, 450], [300, 240], thickness))
    obstacleList.append(Obstacle([320, 0],[370, 100], thickness))
    obstacleList.append(Obstacle([370, 100],[440, 100], thickness))
    obstacleList.append(Obstacle([440, 100],[370, 200], thickness))
    obstacleList.append(Obstacle([370, 200],[420, 370], thickness))
    obstacleList.append(Obstacle([420, 370],[320, 320], thickness))
    obstacleList.append(Obstacle([320, 320],[220, 370], thickness))
    obstacleList.append(Obstacle([220, 370],[220, 100], thickness))
    obstacleList.append(Obstacle([220, 100],[120, 100], thickness))
    obstacleList.append(Obstacle([120, 100],[320, 0], thickness)) 
    

def update():
    global clock
    global tickRate
    global tick
    global obstacleList
    global FPS
    global robots

    clock.tick(FPS)
    # print(clock)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            handleInput()

    for robot in robots:
        inputs = np.append(robot.inputSensors,
                          [robot.vRightOld[0], robot.vLeftOld[0], (robot.vRightOld[0] - robot.vLeftOld[0])])
        vs = controller.calc(robot.id, inputs)
        vs = vs * robot.speedMax / sum(vs)

        robot.setWheelSpeed(vs[0], vs[1])
        move(robot)

    tick += 1


def handleInput():
    global keepRunning
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        keepRunning = False
        return
    if keys[pygame.K_w] and robots[1].xCoord > changePos:
        # print("positive increment of left wheel motor speed")
        robots[1].leftWheelInc()
        return
    if keys[pygame.K_s]:
        # print("negative increment of left wheel motor speed")
        # robots[1].leftWheelDec()
        print("SAVING")
        controller.savePopulation("networkWeights/robotSave")
        return

    if keys[pygame.K_d] and robots[1].xCoord < screenWidth - (2 * circleRadius):
        # print('You just pressed d')
        return
    if keys[pygame.K_a] and robots[1].xCoord > changePos:
        # print('You just pressed a')
        return
    if keys[pygame.K_o]:
        # print("positive increment of right wheel motor speed")
        # robot.xCoord += changePos
        robots[1].rightWheelInc()
        return
    if keys[pygame.K_l]:
        # print("negative increment of right wheel motor speed")
        # robot.xCoord -= changePos
        # robots[1].rightWheelDec()
        print("Loading")
        controller.loadPopulation("networkWeights/robotSave")
        reset()
        return
    if keys[pygame.K_x]:
        # print("both motor speeds are zero")
        robots[1].bothWheelZero()
    if keys[pygame.K_t]:
        # print("positive increment of both wheels’ motor speed")
        robots[1].bothWheelInc()
    if keys[pygame.K_g]:
        # print("negative increment of both wheels’ motor speed")
        robots[1].bothWheelDec()


def move(robot: Robot):
    global circleSurf
    global circleObj
    global timeTick

    # background.clamp_ip(screen)
    robot.updateLocation(timeTick, obstacleList)

    if robot.id == 1:
        screen.fill(white)
        drawGrid()
        addObstacle()
        screen.blit(circleSurf, (robot.xCoord - circleRadius, robot.yCoord - circleRadius))

    updateGrid(robot.xCoord, robot.yCoord, robot)

    displayRobotSensor(robot)  # didn t want to try to  mix up the sequence
    if robot.id == 1:
        displayVelocityOnScreen(1)
        pygame.display.update()


def updateGrid(xCoord, yCoord, robot):
    global circleSurf
    global visitedGrids
    visitedGrid = visitedGrids[robot.id]
    xind = int(xCoord / 10)
    yind = int(yCoord / 10)
    if 0 <= xind < 64 and 0 <= yind < 48:
        visitedGrids[robot.id][xind][yind] = True

    numDust = np.sum(visitedGrid)
    dustLoc = np.nonzero(visitedGrid)
    for i in range(numDust):
        if robot.id == 1:  # we draw only one robot
            pygame.draw.circle(screen, red, (dustLoc[0][i] * 10, dustLoc[1][i] * 10), 13)
    robot.areaCovered = numDust


def displayRobotSensor(robot: Robot):
    global circelSurf
    global robots

    addAngle = 0
    sensorValues = []
    for i in range(0, 12):
        start_location = [robot.xCoord + np.cos(robot.forwardAngle + addAngle) * circleRadius,
                          robot.yCoord + np.sin(robot.forwardAngle + addAngle) * circleRadius]
        text_location = [robot.xCoord + np.cos(robot.forwardAngle + addAngle) * 4 * circleRadius,
                         robot.yCoord + np.sin(robot.forwardAngle + addAngle) * 4 * circleRadius]
        end_location = [robot.xCoord + np.cos(robot.forwardAngle + addAngle) * 3 * circleRadius,
                        robot.yCoord + np.sin(robot.forwardAngle + addAngle) * 3 * circleRadius]

        distToObj = distanceToClosestObj(start_location[0] - robot.xCoord,
                                         start_location[1] - robot.yCoord, robot.xCoord,
                                         robot.yCoord) - circleRadius
        # if i == 0 or i == 1 or i == 11:
        sensorValues.append(1 - distToObj / (150 - circleRadius))
        if robot.id == 1:
            pygame.draw.line(screen, blue, start_location, end_location, 2)
            text_surface_obj = font_obj.render("%.2f" % round(distToObj, 2), True, black)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (text_location)
            screen.blit(text_surface_obj, text_rect_obj)
        addAngle += np.pi / 6
    robot.inputSensors = sensorValues


def distanceToClosestObj(robotSensorDirX, robotSensorDirY, robotMiddleX, robotMiddleY):
    global obstacleList
    closestDist = 100000

    for obstacle in obstacleList:
        # gets distance to obstacle
        dist = distanceToObj(robotSensorDirX, robotSensorDirY, robotMiddleX, robotMiddleY, obstacle.directionvector[0],
                             obstacle.directionvector[1], obstacle.startLoc[0], obstacle.startLoc[1],
                             )
        dist = dist * circleRadius
        # print("DISTANCE: " + str(dist))
        # only needs closest distance
        if dist < closestDist:
            # print("DISTANCE UPDATE: " + str(dist))
            closestDist = dist
    if (closestDist > 150):
        return 150
    return closestDist


def distanceToObj(robotDirX, robotDirY, robotMiddleX, robotMiddleY, wallDirX, wallDirY, wallStartX, wallStartY):
    if wallDirX == 0:
        s = (wallStartX - robotMiddleX) / robotDirX
        g = (s * robotDirY + robotMiddleY - wallStartY) / wallDirY

    elif wallDirY == 0:
        s = (wallStartY - robotMiddleY) / robotDirY
        g = (s * robotDirX + robotMiddleX - wallStartX) / wallDirX

    elif robotDirX == 0:
        g = (robotMiddleX - wallStartX) / wallDirX
        s = (g * wallDirY + wallStartY - robotMiddleY) / robotDirY

    elif robotDirY == 0:
        g = (robotMiddleY - wallStartY) / wallDirY
        s = (g * wallDirX + wallStartX - robotMiddleX) / robotDirX


    # if true than parallel
    elif wallDirX * (robotDirY / wallDirY) == robotDirX:
        return 100
    else:
        g = (((wallStartY - robotMiddleY) / robotDirY) * (robotDirX / wallDirX) + (
                (robotMiddleX - wallStartX) / wallDirX)) / (1 - ((robotDirX * wallDirY) / (wallDirX * robotDirY)))
        # s = ((wallStartY - robotMiddleY) / robotDirY) / (1 - ((robotDirX + robotMiddleX - wallStartX) / wallDirX))
        # s = x of sensor line
        s = (g * wallDirY + wallStartY - robotMiddleY) / robotDirY
        # g = (s * robotDirX + robotMiddleX - wallStartX) / wallDirX
        # print("s: = " + str(s) + ", g: " + str(g))
    # print("S: " + str(s))
    if g < 0 or g > 1:
        return 100

    # s is distance
    if s < -0.5:
        return 100
    return s


def addObstacle():
    # screen.fill(white)
    for obstacle in obstacleList:
        obstacleObj = pygame.draw.line(screen, black,
                                       (obstacle.startLoc[0], obstacle.startLoc[1]),
                                       (obstacle.endLoc[0], obstacle.endLoc[1]), obstacle.thickness)
        # screen.blit(screen, obstacleObj)


def drawGrid():
    global screen
    # draw the grid
    for i in range(0, screenWidth, blockSize):
        i = i + 10
        pygame.draw.line(screen, grey, (i, 0), (i, screenHeight), 1)
    for j in range(0, screenHeight, blockSize):
        j = j + 10
        pygame.draw.line(screen, grey, (0, j), (screenWidth, j), 1)


def displayVelocityOnScreen(ind):
    global robots
    font = pygame.font.Font('freesansbold.ttf', 12)
    textLeft = ('Left wheel: ' + str(robots[ind].vLeft))
    textLeft = font.render(textLeft, True, black)
    text_rect_obj = textLeft.get_rect()
    text_rect_obj.center = ((robots[ind].xCoord, robots[ind].yCoord))
    screen.blit(textLeft, (550, 10))
    textRight = ('Right wheel: ' + str(robots[ind].vRight))
    textRight = font.render(textRight, True, black)
    text_rect_obj = textRight.get_rect()
    text_rect_obj.center = (robots[ind].xCoord, robots[ind].yCoord)
    screen.blit(textRight, (550, 25))


def getEvaluation():
    global robots

    stats = []
    for robot in robots:
        maxArea = 64 * 48
        stats.append(Stat(robot.areaCovered, maxArea, robot.wallBumps, robot.dvCount))
    return stats


def reset():
    global robots
    global visitedGrids
    global startingLocation
    visitedGrids = []
    print("Reset")
    startInd = np.random.randint(0, len(startingLocation))

    for robot in robots:
        #robot.xCoord = startingLocation[startInd][0]
        robot.xCoord = startingLocation[0]
        #robot.yCoord = startingLocation[startInd][1]
        robot.yCoord = startingLocation[1]
        robot.forwardAngle = 1
        robot.wallBumps[0] = 0
        robot.areaCovered = 0
        visitedGrids.append(np.full((64, 48), False))

def runTrainingSimulation(mapNumber):
    global controller
    populationSize = 40
    simulationDuration = 50
    init(populationSize, mapNumber)
    controller = Controller([12 + 3, 4, 2], populationSize)

    roundCount = 1
    while keepRunning:
        print("round number started: " + str(roundCount))
        for i in range(simulationDuration):  # time for a simulation
            update()
        print("done emulating round: " + str(roundCount))

        controller.setFitnessScores(getEvaluation())  # get stats for fitness function
        print("Current mean fitness score: " + str(
            controller.currentMeanScore[-4:-1]) + ", highest mean fitness score: " + str(
            controller.highestMeansScore))

        print("Highest currentScore: " + str(controller.highestCurrentScore))
        print("Hamming Distance: " + str(controller.hammingDistance))

        controller.train()  # updates the weights
        roundCount += 1
        if roundCount % 10 == 0:
            simulationDuration += 50
        reset()
    controller.bestCurrentNetwork.savenetwork("bestWeights")


def runRobot(mapNumber):
    global controller
    global robots
    simulationDuration = 50
    init(2, mapNumber)
    controller = Controller([12 + 3, 4, 2], 2)
    controller.population[1].loadnetwork("bestWeights")
    keepRunning = True
    while keepRunning:
        update()

#Map numbers:
#1 = rect
#2 = yannick world
#3 = trapzoid
#4 = wierd star

runTrainingSimulation(4)
#runRobot(2)

pygame.quit()
