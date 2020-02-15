import numpy as np


class Obstacle:
    startLoc = []
    endLoc = []

    directionvector = []


    def __init__(self, startLoc: [], endLoc: []):
        self.startLoc = np.asarray(startLoc)
        self.endLoc = np.asarray(endLoc)
        self.directionvector = self.endLoc - self.startLoc

    def __str__(self):
        msg = " Obstacle:\n"
        msg += "Obstacle Start: " + str(self.startLoc) + "\n"
        msg += "Obstacle End: " + str(self.endLoc) + "\n"
        return msg



