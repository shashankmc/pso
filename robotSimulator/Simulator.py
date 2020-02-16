from pygame.locals import *
import pygame
import math
# from robotSimulator.Obstacle import Obstacle
# from robotSimulator.Robot import Robot
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
# for every key stroke, the object moves as per the value of the radius.
changePos = circleRadius
# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

screen: any

circleSurf: any
obstacleList: any
obstacleSurf: any
clock: any
font_obj: any
FPS = 20


def init():
    global robot
    global clock
    global circleSurf
    global circleObj
    global screen
    global font_obj

    print("init Objects")
    robot = Robot([200, 200, 0], [0, 0])
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

    print("init end")


def initMap():
    global obstacleList

    thickness = 10
    # obstacleList.append(Obstacle([0, 0], [0, screenHeight]))
    # obstacleList.append(Obstacle([0, screenHeight], [screenWidth, screenHeight]))
    # obstacleList.append(Obstacle([screenWidth, screenHeight], [screenWidth, 0]))
    # obstacleList.append(Obstacle([screenWidth, 0], [0, 0]))

    obstacleList.append(Obstacle([100, 40], [100, 100]))
    obstacleList.append(Obstacle([240, 450], [240, 240]))


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
        return
    if keys[pygame.K_a] and robot.xCoord > changePos:
        print('You just pressed a')
        return
    if keys[pygame.K_o]:
        print("positive increment of right wheel motor speed")
        # robot.xCoord += changePos
        robot.rightWheelInc()
        return
    if keys[pygame.K_l]:
        print("negative increment of right wheel motor speed")
        # robot.xCoord -= changePos
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
    global robot
    global circleSurf
    global circleObj
    global timeTick
    screen.fill(white)
    # background.clamp_ip(screen)
    robot.updateLocation(timeTick)
    addObstacle()
    screen.blit(circleSurf, (robot.xCoord, robot.yCoord))
    robotSensor2()
    pygame.display.update()


def calculateNextPosition():
    checkCollision()
    print("calc next position")


def checkCollision():
    print("check collisions")
    print("update direction according to collision")


def robotSensor():
    global circleSurf

    start_location = [robot.xCoord + np.cos(robot.forwardAngle) * circleRadius + circleRadius,
                      robot.yCoord + np.sin(robot.forwardAngle) * circleRadius + circleRadius]
    text_location = [robot.xCoord + np.cos(robot.forwardAngle) * 2 * circleRadius + circleRadius,
                     robot.yCoord + np.sin(robot.forwardAngle) * 2 * circleRadius + circleRadius]
    end_location = [robot.xCoord + np.cos(robot.forwardAngle) * 3 * circleRadius + circleRadius,
                    robot.yCoord + np.sin(robot.forwardAngle) * 3 * circleRadius + circleRadius]
    # start_location2 = [robot.xCoord + np.cos(robot.forwardAngle + 30) * circleRadius + circleRadius,
    #                  robot.yCoord + np.sin(robot.forwardAngle + 30) * circleRadius + circleRadius]
    # end_location2 = [robot.xCoord + np.cos(robot.forwardAngle + 30) * 3 * circleRadius + circleRadius,
    #                robot.yCoord + np.sin(robot.forwardAngle + 30) * 3 * circleRadius + circleRadius]
    # draw the line
    pygame.draw.line(screen, blue, start_location, end_location, 2)
    # pygame.draw.line(screen, blue, start_location2, end_location2, 2)
    # display the distance between the robot and the object.
    # calculate the distance -- this is a dummy calculation and needs to modified
    dist = math.hypot(start_location[0] - end_location[0], start_location[1] - end_location[1])
    distToObj = distanceToClosestObj(start_location[0] - robot.xCoord - circleRadius,
                                     start_location[1] - robot.yCoord - circleRadius, robot.xCoord ,
                                     robot.yCoord)

    text_surface_obj = font_obj.render("%.2f" % round(distToObj, 2), True, black)
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (text_location)
    screen.blit(text_surface_obj, text_rect_obj)

def robotSensor2():
    global circelSurf
    addAngle = 0
    for i in range(0, 12):
        start_location = [robot.xCoord + np.cos(robot.forwardAngle + addAngle) * circleRadius + circleRadius,
                          robot.yCoord + np.sin(robot.forwardAngle + addAngle) * circleRadius + circleRadius]
        text_location = [robot.xCoord + np.cos(robot.forwardAngle + addAngle) * 4 * circleRadius + circleRadius,
                     robot.yCoord + np.sin(robot.forwardAngle + addAngle) * 4 * circleRadius + circleRadius]
        end_location = [robot.xCoord + np.cos(robot.forwardAngle + addAngle) * 3 * circleRadius + circleRadius,
                    robot.yCoord + np.sin(robot.forwardAngle + addAngle) * 3 * circleRadius + circleRadius]
        pygame.draw.line(screen, blue, start_location, end_location, 2)
        dist = math.hypot(start_location[0] - end_location[0], start_location[1] - end_location[1])
        distToObj = distanceToClosestObj(start_location[0] - robot.xCoord - circleRadius,
                                     start_location[1] - robot.yCoord - circleRadius, robot.xCoord ,
                                     robot.yCoord)
        text_surface_obj = font_obj.render("%.2f" % round(distToObj, 2), True, black)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (text_location)
        screen.blit(text_surface_obj, text_rect_obj)
        addAngle += 60


def distanceToClosestObj(robotSensorDirX, robotSensorDirY, robotMiddleX, robotMiddleY):
    global obstacleList
    closestDist = 100

    for obstacle in obstacleList:
        # gets distance to obstacle
        dist = distanceToObj(robotSensorDirX, robotSensorDirY, robotMiddleX, robotMiddleY, obstacle.directionvector[0],
                             obstacle.directionvector[1], obstacle.startLoc[0], obstacle.startLoc[1],
                             )
        dist = dist * circleRadius
        print("DISTANCE: " + str(dist))
        # only needs closest distance
        if dist < closestDist:
            print("DISTANCE UPDATE: " + str(dist))
            closestDist = dist

    return closestDist


def distanceToObj(robotDirX, robotDirY, robotMiddleX, robotMiddleY, wallDirX, wallDirY, wallStartX, wallStartY):
    if wallDirX == 0:
        s = (wallStartX - robotMiddleX) / robotDirX
        g = (s * robotDirY + robotMiddleY - wallStartY) / wallDirY

    elif wallDirY == 0:
        s = (wallStartY - robotMiddleY) / robotDirY
        g = (s * robotDirX + robotMiddleX - wallStartX) / wallDirX
    # if true than parallel

    elif wallDirX * (robotDirY / wallDirY) == robotDirX:
        return 100
    else:
        s = ((wallStartY - robotMiddleY) / robotDirY) / (1 - ((robotDirX + robotMiddleX - wallStartX) / wallDirX))
        # s = x of sensor line
        g = (s * robotDirX + robotMiddleX - wallStartX) / wallDirX
        print("s: = " + str(s) + ", g: " + str(g))
    print("S: " + str(s))
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
                                       (obstacle.endLoc[0], obstacle.endLoc[1]), 5)
        # screen.blit(screen, obstacleObj)


init()
while keepRunning:
    update()

pygame.quit()
