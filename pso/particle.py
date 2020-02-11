import numpy as np
import random
from pso_final import rosenBrockFunc
class Particle:
    def __init__(self):
        random.seed()
        self.position = np.array([random.randrange(-5, 5), random.randrange(-5, 5)])
        self.velocity = np.array([random.randrange(0, 1), random.randrange(0, 1)])
        self.bestPosition = self.position
        self.bestValue = rosenBrockFunc(self.position[0], self.position[1]) 
        # self.bestVal = rastriginFunc(self.position[0], self.position[1])
