import numpy as np

class Particle:

    def __init__(self, ptype, specs):

        self.type = ptype
        self.charge = specs['charge']
        self.mass = specs['mass']
        self.weight = 1.0
        self.pos = np.empty(0)
        self.vel = np.empty(0)
        self.field = np.empty(0)
