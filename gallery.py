
import numpy as np

class Oscillator:

    def __init__(self, x0, v0, freq):
        self.x0 = x0
        self.v0 = v0
        self.freq = freq

    def exact_x(self, t):
        return self.x0*np.cos(self.freq*t)

    def exact_v(self, t):
        return -self.x0*np.sin(self.freq*t)*self.freq

    def exact_a(self, t):
        return -1.0*np.square(self.freq)*self.exact_x(t)

    def forcing_term(self, x):
        return -1.0*np.square(self.freq)*x



class FallingBall:

    def __init__(self, x0, v0, E, q, m):
        self.x0 = x0
        self.v0 = v0
        self.E = E
        self.q = q
        self.m = m

        self.acc = q/m*E

    def exact_x(self, t):
        return self.x0 + self.v0*t + 0.5*self.acc*t*t

    def exact_v(self, t):
        return self.v0 + self.acc*t

    def exact_a(self, t):
        return self.acc

    def forcing_term(self, x):
        return self.acc



