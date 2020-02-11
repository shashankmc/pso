import numpy as np

class Particle:
    location = []
    velocity = []
    bestLocation = []
    bestValue = 2000
    locationHistory = []

    def __init__(self, startLoc:[], startVelo:[], bestLoc:[], bestVal):
        self.location = np.asarray(startLoc)
        self.velocity = np.asarray(startVelo)
        self.bestLocation = np.asarray(bestLoc)
        self.bestValue = bestVal
        self.locationHistory.append(startLoc)

    def __str__(self):
        msg = " Particle:\n"
        msg += "Particle location: " + str(self.location) + "\n"
        msg += "Particle velocity: " + str(self.velocity) + "\n"
        msg += "Particle bestLocation: " + str(self.bestLocation) + "\n"
        msg += "Particle bestValue: " + str(self.bestValue) + "\n"
        return msg

    def setLocation(self, location:np.array, save:bool):
        self.location = location
        if save:
            self.locationHistory.append(location)