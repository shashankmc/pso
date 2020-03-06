from pygame.locals import *
import pygame
import math
from Obstacle import Obstacle
from Robot import Robot
import numpy as np

from pso.robotSimulator.Controller import Controller
from pso.robotSimulator.Stat import Stat

keepRunning = True
timeTick = 0.1
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

visitedGrids = []
robots: [Robot]


def init(popSize):
    global clock
    global circleSurf
    global circleObj
    global screen
    global font_obj
    global visitedGrids
    global robots
    robots = []
    print("init Objects")


    initMap()

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
        rob = Robot(circleRadius, [150, 300, 0], [0, 0], i)
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

    obstacleList.append(Obstacle([100, 40], [130, 100], thickness))
    obstacleList.append(Obstacle([340, 450], [300, 240], thickness))


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

        vs = controller.calc(robot.id, robot.inputSensors)
        faktor = 25
        robot.setWheelSpeed(faktor * vs[0], faktor * vs[1])
        if robot.id == 1:
            print("robotss" + str(robot.vRight))
        #robot.vRight = vs[0] * faktor
        #robot.vLeft = vs[1] * faktor
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
    if keys[pygame.K_s] and robots[1].yCoord < screenHeight - (2 * circleRadius):
        # print("negative increment of left wheel motor speed")
        robots[1].leftWheelDec()
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
        robots[1].rightWheelDec()
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
    updateGrid(robot.xCoord, robot.yCoord, robot)
    if robot.id == 1:
        screen.fill(white)
        drawGrid()
        addObstacle()
        screen.blit(circleSurf, (robot.xCoord - circleRadius, robot.yCoord - circleRadius))


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
    visitedGrids[robot.id][xind][yind] = True

    numDust = np.sum(visitedGrid)
    dustLoc = np.nonzero(visitedGrid)
    for i in range(numDust):
        if robot.id == 1:  # we draw only one robot
            pygame.draw.circle(screen, red, (dustLoc[0][i] * 10, dustLoc[1][i] * 10), 13)
    robot.areaCovered = numDust


def displayRobotSensor(robot):
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
        sensorValues.append(distToObj)
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
    if(closestDist > 150):
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
    if s < 0:
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
    global  robots
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
    for robo in robots:
        stats.append(Stat(robo.areaCovered, robo.wallBumps))
    return stats

def reset():
    global robots
    global visitedGrids
    visitedGrids = []
    print("Reset")
    for robot in robots:
        robot.yCoord = 300
        robot.xCoord = 150
        robot.forwardAngle = 1
        visitedGrids.append(np.full((64, 48), False))


# while working
# simulate driving robot
# driven by ann
# multiple robots
# same map just multiple robots -> for loop
# different paths width or colros
# instead of key strokes ann calc

# feedback sensorinfos to continue steering
# save fitness stats at the end

# fitevaluate
# area covered, collision?
# reproduce
# reproduction -> weights

populationSize = 10
init(populationSize)
controller = Controller([12, 1, 2], populationSize)

roundCount = 1
while keepRunning:
    print("round number started: " + str(roundCount))
    for i in range(1500):  # time for a simulation
        update()
    print("done emulating round: " + str(roundCount))

    controller.setFitnessScores(getEvaluation())  # get stats for fitness function
    controller.train()  # updates the weights
    roundCount += 1
    reset()

pygame.quit()
