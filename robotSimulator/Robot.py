import numpy as np


class Robot:
    xCoord = 0
    yCoord = 0

    # angle with the X-Axis and the direction the robot is facing
    forwardAngle = 0

    vLeft = 0
    vRight = 0

    length = 0

    def __init__(self, startLoc: [], startVelo: []):
        self.xCoord = startLoc[0]
        self.yCoord = startLoc[1]
        if len(startLoc) > 2:
            self.forwardAngle = startLoc[2]
        else:
            self.forwardAngle = 0

        self.vLeft = startVelo[0]
        self.vRight = startVelo[1]
        self.length = 5

    def __str__(self):
        msg = " Robot:\n"
        msg += "Robot location: x= " + str(self.xCoord) + ", y= " + str(self.yCoord) + "\n"
        msg += "Robot velocity: left= " + str(self.vLeft) + ", right= " + str(self.vRight) + "\n"
        msg += "Robot Facing: " + str(self.forwardAngle) + "\n"
        return msg

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

    def updateLocation(self, timeStep):

        # In case vL and vR are equal the calc of R would throw and error /0
        # but in that case the direction is forward facing
        if self.vLeft == self.vRight:
            self.xCoord += self.vRight * np.cos(self.forwardAngle) * timeStep
            self.yCoord += self.vRight * np.sin(self.forwardAngle) * timeStep
            return

        # In case vL and vR are opposite, this would work with normal calc, but a lot of stuff is unnesseary
        if self.vLeft == -self.vRight:
            self.forwardAngle += 2 * self.vRight * timeStep / self.length
            return

        omega = (self.vRight - self.vLeft) / self.length

        R = 0.5 * self.length * (self.vLeft + self.vRight) / (self.vRight - self.vLeft)
        ICC = [self.xCoord - R * np.sin(self.forwardAngle), self.yCoord + R * np.cos(self.forwardAngle)]
        rotMat = [[np.cos(omega * timeStep), - np.sin(omega * timeStep), 0],
                  [np.sin(omega * timeStep),   np.cos(omega * timeStep), 0],
                  [0, 0, 1]]
        difMat = [self.xCoord - ICC[0], self.yCoord - ICC[1], self.forwardAngle]
        addMat = [ICC[0], ICC[1], omega * timeStep]
        result = np.matmul(rotMat, difMat) + addMat

        self.xCoord = result[0]
        self.yCoord = result[1]
        self.forwardAngle = result[2]
