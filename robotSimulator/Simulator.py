import time
from pynput.keyboard import Key, Listener
from pygame.locals import *
import pygame
import random

from Obstacle import Obstacle
from Robot import Robot

keepRunning = True
timeTick = 0
tickRate = 13.0
robot: Robot
obstacleList = []
# initiates pygame for the simulation of an object
pygame.init()
# set the screen size as per requirement
screen = pygame.display.set_mode((640, 480))

def init():
    global robot
    print("init")
    Listener(on_release=on_release).start()
    robot = Robot([1, 1], [0, 0])
    obstacleList.append(Obstacle([0,0],[3,0]))
    obstacleList.append(Obstacle([3,0],[3,3]))
    obstacleList.append(Obstacle([3,3],[0,3]))
    obstacleList.append(Obstacle([0,3],[0,0]))
    print("init end")


def update():
    global timeTick
    global tickRate
    global robot
    global obstacleList

    timeTick = timeTick + 1
    print("Update: " + str(timeTick))
    calculateNextPosition()
    display()
    time.sleep(tickRate)


def display():
    print("display")



# this function is to display the frame for the simulation
def initDisplay():
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
    pygame.draw.circle(background, (0, 200, 0), (x,y), 25)
    # the function blit creates the initially drawing based on the settings
    screen.blit(background, (0, 0))
    waitForInput = True
    FPS = 30
    # once the display is put up in front of the user
    # pygame module waits for key strokes from the user
    x_change = 0
    y_change = 0
    while waitForInput:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waitForInput = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    waitForInput = False
                elif event.key == K_d:
                    print('You just pressed d')
                    x_change = 25
                    #x_change = calcBounds(x, x_change, 'x')
                    x += x_change
                elif event.key == K_w:
                    print('You just pressed w')
                    y_change = -25
                    # y_change = calcBounds(y, y_change, 'y')
                    y += y_change
                elif event.key == K_a:
                    print('You just pressed a')
                    x_change = -25
                    #x_change = calcBounds(x, x_change, 'x')
                    x += x_change
                elif event.key == K_s:
                    print('You have pressed s')
                    y_change = 25
                    # y_change = calcBounds(y, y_change, 'y')
                    y += y_change
                print(x, y)
                move(x, y, background)

def move(x, y, background):
    screen.fill((255, 255, 255))
    # background.clamp_ip(screen)
    screen.blit(background, (x,y))

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


def on_release(key):
    global keepRunning
    print('{0} release'.format(
        key))

    if str(key)[1:2] == 'w':
        print("positive increment of left wheel motor speed")

    if str(key)[1:2] == 's':
        print("negative increment of left wheel motor speed")

    if str(key)[1:2] == 'o':
        print("positive increment of right wheel motor speed")

    if str(key)[1:2] == 'l':
        print("negative increment of right wsolxtgwheel motor speed")

    if str(key)[1:2] == 'x':
        print("both motor speeds are zero")

    if str(key)[1:2] == 't':
        print("positive increment of both wheels’ motor speed")

    if str(key)[1:2] == 'g':
        print("negative increment of both wheels’ motor speed")

    if key == Key.esc:
        keepRunning = False
        return False



initDisplay()
#init()
# while keepRunning:
#    update()
pygame.quit()