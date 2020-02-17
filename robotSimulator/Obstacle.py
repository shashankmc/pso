import numpy as np


class Obstacle:
    startLoc = []
    endLoc = []
    thickness = 0

    directionvector = []


    def __init__(self, startLoc: [], endLoc: [], thickness):
        self.startLoc = np.asarray(startLoc)
        self.endLoc = np.asarray(endLoc)
        self.thickness = thickness
        self.directionvector = self.endLoc - self.startLoc

    def __str__(self):
        msg = " Obstacle:\n"
        msg += "Obstacle Start: " + str(self.startLoc) + "\n"
        msg += "Obstacle End: " + str(self.endLoc) + "\n"
        return msg



