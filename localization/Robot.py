import numpy as np


class Robot:
    speedMax = 40
    xCoord = 0
    yCoord = 0
    nextX = 0
    nextY = 0

    # angle with the X-Axis and the direction the robot is facing
    forwardAngle = 0

    vLeft = 0
    vRight = 0

    speed = 0
    angle = 0

    length = 0

    areaCovered = 0
    wallBumps: []

    inputSensors: []

    dvCount = []

    id = 0

    def __init__(self, radius, startLoc: [], startVal: [], id):
        self.length = radius
        self.xCoord = startLoc[0]
        self.yCoord = startLoc[1]
        if len(startLoc) > 2:
            self.forwardAngle = startLoc[2]
        else:
            self.forwardAngle = 0

        self.speed = startVal[0]
        self.angle = startVal[1]
        self.id = id

    def __str__(self):
        msg = " Robot:\n"
        msg += "Robot location: x= " + str(self.xCoord) + ", y= " + str(self.yCoord) + "\n"
        msg += "Robot velocity: left= " + str(self.vLeft) + ", right= " + str(self.vRight) + "\n"
        msg += "Robot Facing: " + str(self.forwardAngle) + "\n"
        return msg

    def setWheelSpeed(self, speed):
        self.speed = speed
        if (-self.speedMax) > speed > self.speedMax:
            self.speed = self.speedMax
            if speed < 0:
                self.speed *= -1

    def speedInc(self):
        self.speed += 1
    
    def speedDec(self):
        self.speed -= 1

    def angleInc(self):
        self.angle += .02
    
    def angleDec(self):
        self.angle -= .02

    def stop(self):
        self.speed = 0
        self.angle = 0

    def collisionstuff(self, obstacleList):
        collision = -1
        collision2 = -1

        for i in range(len(obstacleList)):
            p1 = np.array(obstacleList[i].startLoc)
            p2 = np.array(obstacleList[i].endLoc)
            p3 = np.array([self.nextX, self.nextY])
            distance = np.linalg.norm(np.cross(p2 - p1, p3 - p1)) / np.linalg.norm(p2 - p1)
            # print(self.length)
            # print("wall " + str(i) + "distance: " + str(distance))
            if (self.length > distance):
                if (self.inbetween(p1, p2)):
                    if (collision < 0):
                        collision = i
                    elif (collision2 < 0):
                        collision2 = i
                    else:
                        print("Stuck between 3 walls")
        if (collision > -1):
            # print("colliding wall " + str(collision))
            v1 = obstacleList[collision].endLoc - obstacleList[collision].startLoc
            v2 = [self.nextX - self.xCoord, self.nextY - self.yCoord]
            angle = np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
            # print("angle: " + str(angle))

            newV = v1 / np.linalg.norm(v1)
            newV *= np.cos(np.radians(angle))
            self.nextX = self.xCoord + newV[0]
            self.nextY = self.yCoord + newV[1]

        if (collision2 > -1):
            # print("colliding wall2 " + str(collision2))
            v1 = obstacleList[collision2].endLoc - obstacleList[collision2].startLoc
            v2 = [self.nextX - self.xCoord, self.nextY - self.yCoord]
            angle = np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
            # print("angle: " + str(angle))

            newV = v1 / np.linalg.norm(v1)
            newV *= np.cos(np.radians(angle))
            self.nextX = self.xCoord + newV[0]
            self.nextY = self.yCoord + newV[1]

            p1 = np.array(obstacleList[collision].startLoc)
            p2 = np.array(obstacleList[collision].endLoc)
            p3 = np.array([self.nextX, self.nextY])
            distance = np.linalg.norm(np.cross(p2 - p1, p3 - p1)) / np.linalg.norm(p2 - p1)

            if (self.length > distance):
                self.nextX = self.xCoord
                self.nextY = self.yCoord

        self.xCoord = self.nextX
        self.yCoord = self.nextY

    def inbetween(self, p1, p2):
        if (p1[0] < p2[0]):
            x1 = p1[0]
            x2 = p2[0]
        else:
            x1 = p2[0]
            x2 = p1[0]

        if (p1[1] < p2[1]):
            y1 = p1[1]
            y2 = p2[1]
        else:
            y1 = p2[1]
            y2 = p1[1]
        if (x1 == x2):
            return (self.yCoord + self.length >= y1 and self.yCoord - self.length <= y2)
        if (y1 == y2):
            return (self.xCoord + self.length >= x1 and self.xCoord - self.length <= x2)
        return (
                self.xCoord + self.length >= x1 and self.xCoord - self.length <= x2 and self.yCoord + self.length >= y1 and self.yCoord - self.length <= y2)

    def updateLocation(self, timeStep, obstacleList):
        self.nextX = self.xCoord + self.speed * np.cos(self.forwardAngle) * timeStep
        self.nextY = self.yCoord + self.speed * np.sin(self.forwardAngle) * timeStep
        self.forwardAngle += self.angle 
        self.collisionstuff(obstacleList)
