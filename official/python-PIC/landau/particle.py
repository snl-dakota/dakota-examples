import numpy as np

class Particle:

    def __init__(self, ptype, specs):

        self.type = ptype
        self.charge = specs['charge']
        self.mass = specs['mass']
        self.weight = specs['weight']
        self.pos = np.empty(0)
        self.velx = np.empty(0)
        self.vely = np.empty(0)
        self.velz = np.empty(0)
        self.field = np.empty(0)
