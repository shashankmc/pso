import time
from pynput.keyboard import Key, Listener

from Obstacle import Obstacle
from Robot import Robot

keepRunning = True
timeTick = 0
tickRate = 13.0
robot: Robot
obstacleList = []


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


init()
while keepRunning:
    update()
