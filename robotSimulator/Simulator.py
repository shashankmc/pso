####################################################################
# Assignment: Robot Simulator                                        #
# Group: Group 18                                                    #
# Members: Yannick Ruppenthal, Arthur Willems, Shashank Chakravarthy #
# Who did what: Everybody was involved in almost all functions       #
####################################################################
from pygame.locals import *
import pygame
import math
from Obstacle import Obstacle
from Robot import Robot
import numpy as np
# from pso.robotSimulator.Controller import Controller
from Controller import Controller

keepRunning = True
timeTick = 0.1
robot: Robot
circle: any
obstacleList = []
# setting screen width and height
screenWidth = 640
screenHeight = 480
# setting object radius
circleRadius = 20
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

inputLayerN = 2
hiddenLayerN = 3
outputLayerN = 5


def init():
    global robot
    global clock
    global circleSurf
    global circleObj
    global screen
    global font_obj

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
    circleSurf = pygame.Surface(((2 * circleRadius), (2 * circleRadius)), pygame.SRCALPHA)
    # make the background white in color
    circleSurf.fill((255, 255, 255, 0))
    # setting the initial position
    x = circleRadius
    y = circleRadius
    # the circle created will represent the object or robot which will move based on key inputs
    # the parameters for drawing a circle are these - (Surface, color, pos, radius, width=0)
    circleObj = pygame.draw.circle(circleSurf, red, (x, y), circleRadius)
    # font_obj.render(str(robot.vWheels[0]), False, black)
    # screen.blit(circleSurf, (robot.middleCoords[0] + 100, robot.middleCoords[1] + 100))
    screen.blit(screen, circleObj)
    # addObstacle()
    # for obstacle in obstacleList:
    #   print(obstacle)
    pygame.display.update()
    # circleSurf.blit(screen, (100,100))
    # the function blit creates the initially drawing based on the settings
    FPS = 30
    clock = pygame.time.Clock()

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
    global robot
    global obstacleList
    global FPS

    clock.tick(FPS)
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
    if keys[pygame.K_w]:
        print("positive increment of left wheel motor speed")
        robot.leftWheelInc()
        return
    if keys[pygame.K_s]:
        print("negative increment of left wheel motor speed")
        robot.leftWheelDec()
        return
    if keys[pygame.K_d]:
        print('You just pressed d')
        return
    if keys[pygame.K_a]:
        print('You just pressed a')
        return
    if keys[pygame.K_o]:
        print("positive increment of right wheel motor speed")
        robot.rightWheelInc()
        return
    if keys[pygame.K_l]:
        print("negative increment of right wheel motor speed")
        robot.rightWheelDec()
        return
    if keys[pygame.K_x]:
        print("both motor speeds are zero")
        robot.bothWheelZero()
    if keys[pygame.K_t]:
        print("positive increment of both wheels’ motor speed")
        robot.bothWheelInc()
    if keys[pygame.K_g]:
        print("negative increment of both wheels’ motor speed")
        robot.bothWheelDec()


def move():
    global circleSurf
    global timeTick
    print(timeTick)
    screen.fill(white)
    drawGrid()
    robot.updateLocation(timeTick, obstacleList)
    screen.blit(circleSurf, (robot.middleCoords[0] - circleRadius, robot.middleCoords[1] - circleRadius))
    displayObstacles()
    displayRobotSensor()
    displayVelocityOnScreen()
    pygame.display.update()


def displayRobotSensor():
    for sensor in robot.sensorList:
        pygame.draw.line(screen, sensor.color, sensor.start_location, sensor.end_location, 2)
        text_surface_obj = font_obj.render("%d" % int(sensor.distance), True, black)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = sensor.text_location
        screen.blit(text_surface_obj, text_rect_obj)


def displayObstacles():
    for obstacle in obstacleList:
        obstacleObj = pygame.draw.line(screen, black,
                                       (obstacle.startLoc[0], obstacle.startLoc[1]),
                                       (obstacle.endLoc[0], obstacle.endLoc[1]), obstacle.thickness)


def displayVelocityOnScreen():
    font = pygame.font.Font('freesansbold.ttf', 12)
    textLeft = ('Left wheel: ' + str(robot.vWheels[0]))
    textLeft = font.render(textLeft, True, black)
    text_rect_obj = textLeft.get_rect()
    text_rect_obj.center = ((robot.middleCoords[0], robot.middleCoords[1]))
    screen.blit(textLeft, (550, 10))
    textRight = ('Right wheel: ' + str(robot.vWheels[1]))
    textRight = font.render(textRight, True, black)
    text_rect_obj = textRight.get_rect()
    text_rect_obj.center = ((robot.middleCoords[0], robot.middleCoords[1]))
    screen.blit(textRight, (550, 25))


def drawGrid():
    global screen
    # draw the grid
    for i in range(0, screenWidth, blockSize):
        i = i + 10
        pygame.draw.line(screen, grey, (i, 0), (i, screenHeight), 1)
    for j in range(0, screenHeight, blockSize):
        j = j + 10
        pygame.draw.line(screen, grey, (0, j), (screenWidth, j), 1)


c = Controller([inputLayerN, hiddenLayerN, outputLayerN], 10)
print(c.calc([12, 20]))
init()
while keepRunning:
    update()

pygame.quit()
