from pygame.locals import *
import pygame

from robotSimulator.Obstacle import Obstacle
from robotSimulator.Robot import Robot

keepRunning = True
timeTick = 0
tickRate = 13.0
robot: Robot
obstacleList = []
# initiates pygame for the simulation of an object
pygame.init()
# set the screen size as per requirement
screen = pygame.display.set_mode((640, 480))

background : any


def init():
    global robot
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
    x = 25
    y = 25
    # the circle created will represent the object or robot which will move based on key inputs
    # the parameters for drawing a circle are these - (Surface, color, pos, radius, width=0)
    pygame.draw.circle(background, (0, 200, 0), (x, y), 25)
    # the function blit creates the initially drawing based on the settings
    screen.blit(background, (0, 0))
    FPS = 30

    print("init end")


def update():
    global timeTick
    global tickRate
    global robot
    global obstacleList

    timeTick = timeTick + 1
    #print("Update: " + str(timeTick))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waitForInput = False
        if event.type == pygame.KEYDOWN:
            handleInput(event.key)

    move()

def handleInput(key):
    global keepRunning
    if key == K_ESCAPE:
        keepRunning = False
        return
    if key == K_d:
        print('You just pressed d')
        x_change = 25
        # x_change = calcBounds(x, x_change, 'x')
        robot.location[0] += x_change
        return
    if key == K_w:
        print('You just pressed w')
        print("positive increment of left wheel motor speed")
        y_change = -25
        # y_change = calcBounds(y, y_change, 'y')
        robot.location[1] += y_change
        return
    if key == K_a:
        print('You just pressed a')
        x_change = -25
        # x_change = calcBounds(x, x_change, 'x')
        robot.location[0] += x_change
        return
    if key == K_s:
        print('You have pressed s')
        print("negative increment of left wheel motor speed")
        y_change = 25
        # y_change = calcBounds(y, y_change, 'y')
        robot.location[1] += y_change
        return
    if key == K_o:
        print("positive increment of right wheel motor speed")
    if key == K_l:
        print("negative increment of right wheel motor speed")
    if key == K_x:
        print("both motor speeds are zero")
    if key == K_t:
        print("positive increment of both wheels’ motor speed")
    if key == K_g:
        print("negative increment of both wheels’ motor speed")



def move():
    global robot
    global background
    screen.fill((255, 255, 255))
    # background.clamp_ip(screen)
    screen.blit(background, (robot.location[0], robot.location[1]))


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
