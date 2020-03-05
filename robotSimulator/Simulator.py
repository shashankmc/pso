from pygame.locals import *
import pygame
import math
from Obstacle import Obstacle
from Robot import Robot
import numpy as np

keepRunning = True
timeTick = 0.1
tickRate = 13.0
robot: Robot
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

visitedGrid = []


def init():
    global robot
    global clock
    global circleSurf
    global circleObj
    global screen
    global font_obj
    global visitedGrid

    print("init Objects")
    robot = Robot(circleRadius, [150, 300, 0], [0, 0])
    initMap()

    print("init display")
    # initiates pygame for the simulation of an object
    pygame.init()
    # set the screen size as per requirement
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(white)
    font_obj = pygame.font.Font('freesansbold.ttf', 11)

    # setup a surface for the circle to displayed on
    circleSurf = pygame.Surface(((2 * circleRadius), (2 * circleRadius)))
    # make the background white in color
    circleSurf.fill(white)
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

    thickness = 5
    obstacleList.append(Obstacle([0, 0], [0, screenHeight], thickness))
    obstacleList.append(Obstacle([0, screenHeight], [screenWidth, screenHeight], thickness))
    obstacleList.append(Obstacle([screenWidth, screenHeight], [screenWidth, 0], thickness))
    obstacleList.append(Obstacle([screenWidth, 0], [0, 0], thickness))

    obstacleList.append(Obstacle([100, 40], [130, 100], thickness))
    obstacleList.append(Obstacle([240, 450], [200, 240], thickness))


def update():
    global clock
    global tickRate
    global robot
    global obstacleList
    global FPS

    clock.tick(FPS)
    # print(clock)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            handleInput()

    move()


def handleInput():
    global keepRunning
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        keepRunning = False
        return
    if keys[pygame.K_w] and robot.xCoord > changePos:
        #print("positive increment of left wheel motor speed")
        robot.leftWheelInc()
        return
    if keys[pygame.K_s] and robot.yCoord < screenHeight - (2 * circleRadius):
        #print("negative increment of left wheel motor speed")
        robot.leftWheelDec()
        return

    if keys[pygame.K_d] and robot.xCoord < screenWidth - (2 * circleRadius):
        #print('You just pressed d')
        return
    if keys[pygame.K_a] and robot.xCoord > changePos:
        #print('You just pressed a')
        return
    if keys[pygame.K_o]:
        #print("positive increment of right wheel motor speed")
        # robot.xCoord += changePos
        robot.rightWheelInc()
        return
    if keys[pygame.K_l]:
        #print("negative increment of right wheel motor speed")
        # robot.xCoord -= changePos
        robot.rightWheelDec()
        return
    if keys[pygame.K_x]:
        #print("both motor speeds are zero")
        robot.bothWheelZero()
    if keys[pygame.K_t]:
        #print("positive increment of both wheels’ motor speed")
        robot.bothWheelInc()
    if keys[pygame.K_g]:
        #print("negative increment of both wheels’ motor speed")
        robot.bothWheelDec()


def move():
    global robotw
    global circleSurf
    global circleObj
    global timeTick
    screen.fill(white)
    drawGrid()
    # background.clamp_ip(screen)
    robot.updateLocation(timeTick, obstacleList)
    updateGrid(robot.xCoord, robot.yCoord)
    addObstacle()
    screen.blit(circleSurf, (robot.xCoord - circleRadius, robot.yCoord - circleRadius))
    displayRobotSensor()
    displayVelocityOnScreen()
    pygame.display.update()


def updateGrid(xCoord, yCoord):
    global circleSurf
    global visitedGrid
    xind = int(xCoord/10)
    yind = int(yCoord/10)
    visitedGrid[xind][yind] = True

    numDust = np.sum(visitedGrid)
    dustLoc = np.nonzero(visitedGrid)
    for i in range(numDust):
        pygame.draw.circle(screen, red, (dustLoc[0][i]*10, dustLoc[1][i]*10), 10)

    print(numDust)


def displayRobotSensor():
    global circelSurf
    addAngle = 0
    for i in range(0, 12):
        start_location = [robot.xCoord + np.cos(robot.forwardAngle + addAngle) * circleRadius,
                          robot.yCoord + np.sin(robot.forwardAngle + addAngle) * circleRadius]
        text_location = [robot.xCoord + np.cos(robot.forwardAngle + addAngle) * 4 * circleRadius,
                         robot.yCoord + np.sin(robot.forwardAngle + addAngle) * 4 * circleRadius]
        end_location = [robot.xCoord + np.cos(robot.forwardAngle + addAngle) * 3 * circleRadius,
                        robot.yCoord + np.sin(robot.forwardAngle + addAngle) * 3 * circleRadius]
        pygame.draw.line(screen, blue, start_location, end_location, 2)

        distToObj = distanceToClosestObj(start_location[0] - robot.xCoord,
                                         start_location[1] - robot.yCoord, robot.xCoord,
                                         robot.yCoord) - circleRadius
        text_surface_obj = font_obj.render("%.2f" % round(distToObj, 2), True, black)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (text_location)
        screen.blit(text_surface_obj, text_rect_obj)
        addAngle += np.pi / 6


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


def displayVelocityOnScreen():
    font = pygame.font.Font('freesansbold.ttf', 12)
    textLeft = ('Left wheel: ' + str(robot.vLeft))
    textLeft = font.render(textLeft, True, black)
    text_rect_obj = textLeft.get_rect()
    text_rect_obj.center = ((robot.xCoord, robot.yCoord))
    screen.blit(textLeft, (550, 10))
    textRight = ('Right wheel: ' + str(robot.vRight))
    textRight = font.render(textRight, True, black)
    text_rect_obj = textRight.get_rect()
    text_rect_obj.center = ((robot.xCoord, robot.yCoord))
    screen.blit(textRight, (550, 25))


init()
while keepRunning:
    update()

pygame.quit()
