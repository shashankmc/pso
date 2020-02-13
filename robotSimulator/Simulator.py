from pygame.locals import *
import pygame

from Obstacle import Obstacle
from Robot import Robot

keepRunning = True
timeTick = 0
tickRate = 13.0
robot: Robot
obstacleList = []
screenWidth = 640
screenHeight = 480
circleRadius = 20
changePos = circleRadius
# initiates pygame for the simulation of an object
pygame.init()
# set the screen size as per requirement
screen = pygame.display.set_mode((screenWidth, screenHeight))

background : any
clock: any
FPS = 30


def init():
    global robot
    global clock
    global background

    print("init")
    robot = Robot([1, 1], [0, 0])
    obstacleList.append(Obstacle([0, 0], [3, 0]))
    obstacleList.append(Obstacle([3, 0], [3, 3]))
    obstacleList.append(Obstacle([3, 3], [0, 3]))
    obstacleList.append(Obstacle([0, 3], [0, 0]))


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
    pygame.draw.circle(background, (0, 200, 0), (x, y), circleRadius)
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
    print(clock)
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
    if keys[pygame.K_d] and robot.location[0] < screenWidth - (2 * circleRadius):
        print('You just pressed d')
        # x_change = calcBounds(x, x_change, 'x')
        robot.location[0] += changePos
        return
    if keys[pygame.K_w] and robot.location[1] > changePos:
        print('You just pressed w')
        print("positive increment of left wheel motor speed")
        # y_change = -25
        # y_change = calcBounds(y, y_change, 'y')
        robot.location[1] -= changePos
        return
    if keys[pygame.K_a] and robot.location[0] > changePos:
        print('You just pressed a')
        # x_change = -25
        # x_change = calcBounds(x, x_change, 'x')
        robot.location[0] -= changePos
        return
    if keys[pygame.K_s] and robot.location[1] < screenHeight - (2 * circleRadius):
        print('You have pressed s')
        print("negative increment of left wheel motor speed")
        # y_change = 25
        # y_change = calcBounds(y, y_change, 'y')
        robot.location[1] += changePos
        return
    if keys[pygame.K_o]:
        print("positive increment of right wheel motor speed")
    if keys[pygame.K_l]:
        print("negative increment of right wheel motor speed")
    if keys[pygame.K_x]:
        print("both motor speeds are zero")
    if keys[pygame.K_t]:
        print("positive increment of both wheels’ motor speed")
    if keys[pygame.K_g]:
        print("negative increment of both wheels’ motor speed")



def move():
    global robot
    global background
    screen.fill((255, 255, 255))
    # background.clamp_ip(screen)
    screen.blit(background, (robot.location[0], robot.location[1]))
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
