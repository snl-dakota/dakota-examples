import numpy as np
import matplotlib.pyplot as plt

def time_step(dt, nt, v0, x0):
    '''
    Input variables:
        dt = time step size
        nt = number of time steps
        v0 = initial velocity
        x0 = initial position

    '''

    vel = np.empty(nt)
    pos = np.empty(nt)

    E   = 1.0                  # placeholder for later Electric Field Function
    vel[0] = v0-0.5*q/m*E*dt   # move vel back by 1/2*dt
    pos[0] = x0                # initialize position

    for ii in range(nt):
        vel[ii] = vel[ii] + q/m*E*dt
        pos[ii] = pos[ii] + vel[ii]*dt

    return

def accel():
    

    pass


def set_v():
    dtdx = dt/dx
    t    = -dt/2

    vx = np.empty(len())
    vy = np.empty(len())

    if (t!=0):
        c = 1.0/np.sqrt(1.0+t**2)
        s = c*t

        for ii in range():
            vxx = vx[ii]
            vx[ii] =  c*vxx + s*vy[ii]
            vy[ii] = -s*vxx + c*vy[ii]
            vy[ii] = vy[ii]*dtdx

     # normalize vx
     for ii in range():
         vx[ii] = vx[ii]*dtdx

     # electric impulse to go back 1/2 time step
     dum = 0.0
     accel()

     return



