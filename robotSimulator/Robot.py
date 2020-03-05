import numpy as np


class Sensor:
    distance = 0
    angle = 0
    start_location = []
    text_location = []
    end_location = []
    circleRadius = 0
    color = (0, 0, 255)

    def __init__(self, angle, robotMiddle, forwardAngle, circleRadius):
        self.distance = 100
        self.angle = angle
        self.circleRadius = circleRadius

        self.start_location = self.lineDir(robotMiddle, forwardAngle, 1)
        self.end_location = self.lineDir(robotMiddle, forwardAngle, 3)
        self.text_location = self.lineDir(robotMiddle, forwardAngle, 4)

        if self.angle == 0:
            self.color = (0, 0, 0)  # Black
        else:
            self.color = (0, 0, 255)  # Blue

    def lineDir(self, robotMiddle, robotAngle, n):
        return np.array(robotMiddle + np.array((np.cos(robotAngle + self.angle) * self.circleRadius * n,
                                                np.sin(robotAngle + self.angle) * self.circleRadius * n)))

    def updateSensors(self, obstacles: [], robotMiddle, forwardAngle):
        self.start_location = self.lineDir(robotMiddle, forwardAngle, 1)
        self.end_location = self.lineDir(robotMiddle, forwardAngle, 3)
        self.text_location = self.lineDir(robotMiddle, forwardAngle, 4)

        self.distance = self.distanceToClosestObj(self.start_location - robotMiddle, robotMiddle,
                                                  obstacles) - self.circleRadius

    def distanceToClosestObj(self, robotSensorDir, robotMiddle, obstacleList):

        closestDist = 100000

        for obstacle in obstacleList:
            # gets distance to obstacle
            dist = self.distanceToObj(robotSensorDir, robotMiddle, obstacle.directionvector, obstacle.startLoc)
            dist = dist * self.circleRadius
            # only needs closest distance
            if dist < closestDist:
                closestDist = dist

        return closestDist

    def distanceToObj(self, robotDir, robotMiddle, wallDir, wallStart):
        if wallDir[0] == 0:
            s = (wallStart[0] - robotMiddle[0]) / robotDir[0]
            g = (s * robotDir[1] + robotMiddle[1] - wallStart[1]) / wallDir[1]

        elif wallDir[1] == 0:
            s = (wallStart[1] - robotMiddle[1]) / robotDir[1]
            g = (s * robotDir[0] + robotMiddle[0] - wallStart[0]) / wallDir[0]

        elif robotDir[0] == 0:
            g = (robotMiddle[0] - wallStart[0]) / wallDir[0]
            s = (g * wallDir[1] + wallStart[1] - robotMiddle[1]) / robotDir[1]

        elif robotDir[1] == 0:
            g = (robotMiddle[1] - wallStart[1]) / wallDir[1]
            s = (g * wallDir[0] + wallStart[0] - robotMiddle[0]) / robotDir[0]


        # if true than parallel
        elif wallDir[0] * (robotDir[1] / wallDir[1]) == robotDir[0]:
            return 100
        else:
            g = (((wallStart[1] - robotMiddle[1]) / robotDir[1]) * (robotDir[0] / wallDir[0]) + (
                    (robotMiddle[0] - wallStart[0]) / wallDir[0])) / (
                        1 - ((robotDir[0] * wallDir[1]) / (wallDir[0] * robotDir[1])))
            # s = ((wallStart[1] - robotMiddle[1]) / robotDir[1]) / (1 - ((robotDir[0] + robotMiddle[0] - wallStart[0]) / wallDir[0]))
            # s = x of sensor line
            s = (g * wallDir[1] + wallStart[1] - robotMiddle[1]) / robotDir[1]
            # g = (s * robotDir[0] + robotMiddle[0] - wallStart[0]) / wallDir[0]
            # print("s: = " + str(s) + ", g: " + str(g))
        # print("S: " + str(s))
        if g < 0 or g > 1:
            return 100

        # s is distance
        if s < 0:
            return 100
        return s


class Robot:
    middleCoords: np.array
    nextX = 0
    nextY = 0

    # angle with the X-Axis and the direction the robot is facing
    forwardAngle = 0

    vWheels: np.array

    length = 0

    sensorList = []

    def __init__(self, radius, startLoc: [], startVelo: [], numberOfSensors=12):
        self.length = radius
        self.middleCoords = np.array([startLoc[0], startLoc[1]])
        if len(startLoc) > 2:
            self.forwardAngle = startLoc[2]
        else:
            self.forwardAngle = 0

        self.vWheels = np.array(startVelo)

        for i in range(0, numberOfSensors):
            self.sensorList.append(Sensor(i * 2 * np.pi / numberOfSensors, self.middleCoords, self.forwardAngle, self.length))

    def __str__(self):
        msg = " Robot:\n"
        msg += "Robot location: x= " + str(self.middleCoords[0]) + ", y= " + str(self.middleCoords[1]) + "\n"
        msg += "Robot velocity: left= " + str(self.vWheels[0]) + ", right= " + str(self.vWheels[1]) + "\n"
        msg += "Robot Facing: " + str(self.forwardAngle) + "\n"
        return msg

    def leftWheelInc(self):
        self.vWheels[0] += 1

    def rightWheelInc(self):
        self.vWheels[1] += 1

    def leftWheelDec(self):
        self.vWheels[0] -= 1

    def rightWheelDec(self):
        self.vWheels[1] -= 1

    def bothWheelZero(self):
        self.vWheels[1] = 0
        self.vWheels[0] = 0

    def bothWheelInc(self):
        self.vWheels[1] += 1
        self.vWheels[0] += 1

    def bothWheelDec(self):
        self.vWheels[1] -= 1
        self.vWheels[0] -= 1

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
            v2 = [self.nextX - self.middleCoords[0], self.nextY - self.middleCoords[1]]
            angle = np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
            # print("angle: " + str(angle))

            newV = v1 / np.linalg.norm(v1)
            newV *= np.cos(np.radians(angle))
            self.nextX = self.middleCoords[0] + newV[0]
            self.nextY = self.middleCoords[1] + newV[1]

        if (collision2 > -1):
            print("colliding wall2 " + str(collision2))
            v1 = obstacleList[collision2].endLoc - obstacleList[collision2].startLoc
            v2 = [self.nextX - self.middleCoords[0], self.nextY - self.middleCoords[1]]
            angle = np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
            # print("angle: " + str(angle))

            newV = v1 / np.linalg.norm(v1)
            newV *= np.cos(np.radians(angle))
            self.nextX = self.middleCoords[0] + newV[0]
            self.nextY = self.middleCoords[1] + newV[1]

            p1 = np.array(obstacleList[collision].startLoc)
            p2 = np.array(obstacleList[collision].endLoc)
            p3 = np.array([self.nextX, self.nextY])
            distance = np.linalg.norm(np.cross(p2 - p1, p3 - p1)) / np.linalg.norm(p2 - p1)
            if (self.length > distance):
                self.nextX = 0
                self.nextY = 0

        self.middleCoords[0] = self.nextX
        self.middleCoords[1] = self.nextY

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
            return (self.middleCoords[1] + self.length >= y1 and self.middleCoords[1] - self.length <= y2)
        if (y1 == y2):
            return (self.middleCoords[0] + self.length >= x1 and self.middleCoords[0] - self.length <= x2)
        return (
                self.middleCoords[0] + self.length >= x1 and self.middleCoords[0] - self.length <= x2 and self.middleCoords[1] + self.length >= y1 and self.middleCoords[1] - self.length <= y2)

    def updateLocation(self, timeStep, obstacleList):

        # In case vL and vR are equal the calc of R would throw and error /0
        # but in that case the direction is forward facing
        if self.vWheels[0] == self.vWheels[1]:
            self.nextX = self.middleCoords[0] + self.vWheels[1] * np.cos(self.forwardAngle) * timeStep
            self.nextY = self.middleCoords[1] + self.vWheels[1] * np.sin(self.forwardAngle) * timeStep
            self.collisionstuff(obstacleList)
            return

        # In case vL and vR are opposite, this would work with normal calc, but a lot of stuff is unnesseary
        if self.vWheels[0] == -self.vWheels[1]:
            self.forwardAngle += 2 * self.vWheels[1] * timeStep / self.length
            return

        omega = (self.vWheels[1] - self.vWheels[0]) / self.length

        R = 0.5 * self.length * (self.vWheels[0] + self.vWheels[1]) / (self.vWheels[1] - self.vWheels[0])
        ICC = [self.middleCoords[0] - R * np.sin(self.forwardAngle), self.middleCoords[1] + R * np.cos(self.forwardAngle)]
        rotMat = [[np.cos(omega * timeStep), - np.sin(omega * timeStep), 0],
                  [np.sin(omega * timeStep), np.cos(omega * timeStep), 0],
                  [0, 0, 1]]
        difMat = [self.middleCoords[0] - ICC[0], self.middleCoords[1] - ICC[1], self.forwardAngle]
        addMat = [ICC[0], ICC[1], omega * timeStep]
        result = np.matmul(rotMat, difMat) + addMat

        self.nextX = result[0]
        self.nextY = result[1]
        self.forwardAngle = result[2]

        self.collisionstuff(obstacleList)
        self.updateSensors(obstacleList)

    def updateSensors(self, obstacleList: []):
        for sensor in self.sensorList:
            sensor.updateSensors(obstacleList, (self.middleCoords[0], self.middleCoords[1]), self.forwardAngle)
