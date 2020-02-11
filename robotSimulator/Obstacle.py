import numpy as np


class Obstacle:
    startLoc = []
    endLoc = []


    def __init__(self, startLoc: [], endLoc: []):
        self.location = np.asarray(startLoc)
        self.endLoc = np.asarray(endLoc)

    def __str__(self):
        msg = " Obstacle:\n"
        msg += "Obstacle Start: " + str(self.startLoc) + "\n"
        msg += "Obstacle End: " + str(self.endLoc) + "\n"
        return msg
