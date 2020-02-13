from pygame.locals import *
import pygame

from robotSimulator.Obstacle import Obstacle
from robotSimulator.Robot import Robot

keepRunning = True
timeTick = 0.1
tickRate = 13.0
robot: Robot
circle: any
obstacleList = []
screenWidth = 640
screenHeight = 480
circleRadius = 20
changePos = circleRadius
# initiates pygame for the simulation of an object
pygame.init()
# set the screen size as per requirement
screen = pygame.display.set_mode((screenWidth, screenHeight))

background: any
clock: any
FPS = 10


def init():
    global robot
    global clock
    global background
    global circle

    print("init")
    robot = Robot([200, 200, 0], [0, 0])
    obstacleList.append(Obstacle([0, 0], [30, 0]))
    obstacleList.append(Obstacle([30, 0], [30, 30]))
    obstacleList.append(Obstacle([30, 30], [0, 30]))
    obstacleList.append(Obstacle([0, 30], [0, 0]))

    # empty the background -- this needs to be set only initially. This is here for current run
    background = pygame.Surface(screen.get_size())
    # make the background white in color
    background.fill((255, 255, 255))
    # convert the background with the provided settings and display with the necessary objects
    background.convert()
    # setting the initial position
    x = circleRadius
    y = circleRadius
    # the circle created will represent the object or robot which will move based on key inputs
    # the parameters for drawing a circle are these - (Surface, color, pos, radius, width=0)

    circle = pygame.draw.circle(background, (200, 0, 0), (x, y), 25)

    for obstacle in obstacleList:
        pygame.draw.line(background, (0, 200, 0), (obstacle.startLoc[0], obstacle.startLoc[1]),
                         (obstacle.endLoc[0], obstacle.endLoc[0]), 5)

    # the function blit creates the initially drawing based on the settings
    screen.blit(background, (0, 0))
    FPS = 30
    clock = pygame.time.Clock()

    print("init end")


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
        print("positive increment of left wheel motor speed")
        robot.leftWheelInc()
        return
    if keys[pygame.K_s] and robot.yCoord < screenHeight - (2 * circleRadius):
        print("negative increment of left wheel motor speed")
        robot.leftWheelDec()
        return

    if keys[pygame.K_d] and robot.xCoord < screenWidth - (2 * circleRadius):
        print('You just pressed d')
        # x_change = calcBounds(x, x_change, 'x')
        robot.xCoord += changePos
        return
    if keys[pygame.K_a] and robot.xCoord > changePos:
        print('You just pressed a')
        # x_change = -25
        # x_change = calcBounds(x, x_change, 'x')
        robot.xCoord -= changePos
        return

    if keys[pygame.K_o]:
        print("positive increment of right wheel motor speed")
        robot.rightWheelInc()
    if keys[pygame.K_l]:
        print("negative increment of right wheel motor speed")
        robot.rightWheelDec()
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
    global robot
    global background
    global circle
    global timeTick
    screen.fill((255, 255, 255))
    # background.clamp_ip(screen)
    robot.updateLocation(timeTick)
    screen.blit(background, (robot.xCoord, robot.yCoord))
    pygame.display.update()


# def calcBounds(pos, pos_change, axes):
#    if (axes == 'x'):
#        if(pos - pos_change < 0 or pos + pos_change > 600):
#            pos_change = 0
#        else:
#           pos_change
#   elif (axes == 'y'):
#       if(pos_change - pos < 0 or pos + pos_change > 480):
#           pos_change = 0
#       else:
#            pos_change
#    return (pos_change)


def calculateNextPosition():
    checkCollision()
    print("calc next position")


def checkCollision():
    print("check collisions")
    print("update direction according to collision")


init()
while keepRunning:
    update()

pygame.quit()
