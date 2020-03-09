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
    vLeftOld = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    vRightOld = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    length = 0

    areaCovered = 0
    wallBumps: []

    inputSensors: []

    dvCount = []

    id = 0

    def __init__(self, radius, startLoc: [], startVelo: [], id):
        self.length = radius
        self.xCoord = startLoc[0]
        self.yCoord = startLoc[1]
        if len(startLoc) > 2:
            self.forwardAngle = startLoc[2]
        else:
            self.forwardAngle = 0

        self.vLeft = startVelo[0]
        self.vRight = startVelo[1]
        self.id = id

        # stats for fitness, [1 collicion, 2 collisions, 3 collisions]
        self.wallBumps = [0, 0, 0]

    def __str__(self):
        msg = " Robot:\n"
        msg += "Robot location: x= " + str(self.xCoord) + ", y= " + str(self.yCoord) + "\n"
        msg += "Robot velocity: left= " + str(self.vLeft) + ", right= " + str(self.vRight) + "\n"
        msg += "Robot Facing: " + str(self.forwardAngle) + "\n"
        return msg

    def setWheelSpeed(self, left, right):
        self.vLeft = left
        if (-self.speedMax) > left > self.speedMax:
            self.vLeft = self.speedMax
            if left < 0:
                self.vLeft *= -1

        self.vRight = right
        if (-self.speedMax) > right > self.speedMax:
            self.vRight = self.speedMax
            if right < 0:
                self.vRight *= -1

        self.vRightOld.pop(0)
        self.vLeftOld.pop(0)
        self.vRightOld.append(self.vRight / self.speedMax)
        self.vLeftOld.append(self.vLeft / self.speedMax)
        dvc = 1 - np.sqrt(np.abs(self.vRight - self.vLeft) / (np.abs(self.vLeft) + np.abs(self.vRight)))
        self.dvCount.append(dvc)

    def leftWheelInc(self):
        self.vLeft += 1

    def rightWheelInc(self):
        self.vRight += 1

    def leftWheelDec(self):
        self.vLeft -= 1

    def rightWheelDec(self):
        self.vRight -= 1

    def bothWheelZero(self):
        self.vRight = 0
        self.vLeft = 0

    def bothWheelInc(self):
        self.vRight += 1
        self.vLeft += 1

    def bothWheelDec(self):
        self.vRight -= 1
        self.vLeft -= 1

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
                        self.wallBumps[2] += 1
                        print("Stuck between 3 walls")
        if (collision > -1):
            self.wallBumps[0] += 1
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
            self.wallBumps[1] += 1
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
        # In case vL and vR are equal the calc of R would throw and error /0
        # but in that case the direction is forward facing
        if self.vLeft == self.vRight:
            self.nextX = self.xCoord + self.vRight * np.cos(self.forwardAngle) * timeStep
            self.nextY = self.yCoord + self.vRight * np.sin(self.forwardAngle) * timeStep
            self.collisionstuff(obstacleList)
            return

        # In case vL and vR are opposite, this would work with normal calc, but a lot of stuff is unnesseary
        if self.vLeft == -self.vRight:
            self.forwardAngle += 2 * self.vRight * timeStep / self.length
            return

        omega = (self.vRight - self.vLeft) / self.length

        R = 0.5 * self.length * (self.vLeft + self.vRight) / (self.vRight - self.vLeft)
        ICC = [self.xCoord - R * np.sin(self.forwardAngle), self.yCoord + R * np.cos(self.forwardAngle)]
        rotMat = [[np.cos(omega * timeStep), - np.sin(omega * timeStep), 0],
                  [np.sin(omega * timeStep), np.cos(omega * timeStep), 0],
                  [0, 0, 1]]
        difMat = [self.xCoord - ICC[0], self.yCoord - ICC[1], self.forwardAngle]
        addMat = [ICC[0], ICC[1], omega * timeStep]
        result = np.matmul(rotMat, difMat) + addMat

        self.nextX = result[0]
        self.nextY = result[1]
        self.forwardAngle = result[2]

        self.collisionstuff(obstacleList)
