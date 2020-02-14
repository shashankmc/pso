from pygame.locals import *
import pygame
import math
from Obstacle import Obstacle
from Robot import Robot

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
# initiates pygame for the simulation of an object
pygame.init()
# set the screen size as per requirement
screen = pygame.display.set_mode((screenWidth, screenHeight))
screen.fill(white)
font_obj = pygame.font.Font('freesansbold.ttf', 12)

circleSurf: any
obstacleList: any
obstacleSurf: any
clock: any
FPS = 10


def init():
    global robot
    global clock
    global circleSurf
    global circleObj

    print("init")
    robot = Robot([200, 200, 0], [0, 0])
    obstacleList.append(Obstacle([10, 10], [10, 30]))
    obstacleList.append(Obstacle([100, 40], [100, 100]))
    obstacleList.append(Obstacle([240, 450], [240, 240]))
    # obstacleList.append(Obstacle([0, 0], [0, 0]))

    # setup a surface for the circle to displayed on
    circleSurf = pygame.Surface(((2 * circleRadius),(2 * circleRadius)))
    # make the background white in color
    circleSurf.fill(white)
    # setting the initial position
    x = circleRadius
    y = circleRadius
    # the circle created will represent the object or robot which will move based on key inputs
    # the parameters for drawing a circle are these - (Surface, color, pos, radius, width=0)
    circleObj = pygame.draw.circle(circleSurf, red, (x, y), circleRadius)
    screen.blit(screen, circleObj)
    #addObstacle()
    # for obstacle in obstacleList:
    #   print(obstacle)
    pygame.display.update()
    # circleSurf.blit(screen, (100,100))
    # the function blit creates the initially drawing based on the settings
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
        robot.xCoord += changePos
        return
    if keys[pygame.K_a] and robot.xCoord > changePos:
        print('You just pressed a')
        robot.xCoord -= changePos
        return
    if keys[pygame.K_o]:
        print("positive increment of right wheel motor speed")
        robot.xCoord += changePos
        robot.rightWheelInc()
        return
    if keys[pygame.K_l]:
        print("negative increment of right wheel motor speed")
        robot.xCoord -= changePos
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
    robotSensor()
    pygame.display.update()
    

def calculateNextPosition():
    checkCollision()
    print("calc next position")


def checkCollision():
    print("check collisions")
    print("update direction according to collision")
    

def robotSensor():
    global circleSurf
    start_location = [robot.xCoord + circleRadius, robot.yCoord + circleRadius]
    text_location = [robot.xCoord + 2 * circleRadius, robot.yCoord + 2 * circleRadius]
    end_location = [robot.xCoord + 3 * circleRadius, robot.yCoord + 3 * circleRadius]   
    # draw the line
    pygame.draw.line(screen, blue, start_location, end_location, 2 )
    # display the distance between the robot and the object.
    # calculate the distance -- this is a dummy calculation and needs to modified
    dist = math.hypot(start_location[0]-end_location[0], start_location[1] - end_location[1])
    # text_surface_obj = font_obj.render((str(robot.location[0]) + ',' +str(robot.location[1])), 
    #                                   True, (150, 150, 0))
    text_surface_obj = font_obj.render("%.2f" % round(dist, 2), True, black)
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (text_location)
    screen.blit(text_surface_obj, text_rect_obj)
    

def addObstacle():
    screen.fill(white)
    for obstacle in obstacleList:    
        obstacleObj = pygame.draw.line(screen, black,
                                       (obstacle.startLoc[0], obstacle.startLoc[1]),
                                       (obstacle.endLoc[0], obstacle.endLoc[0]), 5)
        screen.blit(screen, obstacleObj)


init()
while keepRunning:
    update()

pygame.quit()
