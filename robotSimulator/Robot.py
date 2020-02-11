import numpy as np

class Robot:
    location = []
    velocity = []

    def __init__(self, startLoc: [], startVelo: []):
        self.location = np.asarray(startLoc)
        self.velocity = np.asarray(startVelo)

    def __str__(self):
        msg = " Robot:\n"
        msg += "Robot location: " + str(self.location) + "\n"
        msg += "Robot velocity: " + str(self.velocity) + "\n"
        return msg
