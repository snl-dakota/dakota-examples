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
    q   = 1.0                  # Dummy charge value - TODO: replace with meaningful value
    m   = 1.0                  # Dummy mass value - TODO: replace with meaningful value
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
    for ii in range(len(vx)):
        vx[ii] = vx[ii]*dtdx

     # electric impulse to go back 1/2 time step
    dum = 0.0
    accel()

    return


def scenario_ForwardEuler(dt, nt):
    '''
    "Explicit" or "Forward" Euler time integration using example from
         https://www.particleincell.com/2011/velocity-integration/

    Input variables:
        dt = time step size
        nt = number of time steps
    '''

    # Model params
    omega = 2*np.pi/(50.0*dt)

    # Initial conditions
    x0 = 1.0
    v0 = 0.0

    # Initialize time
    time = 0.0

    # This is the exact expression for the forcing term (acceleration)
    accel = lambda x : -omega*omega*x

    # Compute the exact solutions as well for later comparison
    xexact = np.empty(nt+1)
    vexact = np.empty(nt+1)

    xsol = np.empty(nt+1)
    vsol = np.empty(nt+1)

    # Assign initial conditions
    xsol[0] = x0
    vsol[0] = v0
    xexact[0] = x0
    vexact[0] = v0

    # Do time integration
    for step in range(nt):
        acc = accel(xsol[step])
        vsol[step+1] = vsol[step] + dt*acc
        xsol[step+1] = xsol[step] + dt*vsol[step]

        # Compute exact values
        time += dt
        xexact[step+1] =  np.cos(omega*time)
        vexact[step+1] = -np.sin(omega*time)

    return xsol, vsol, xexact, vexact




if __name__ == "__main__":

    # Start by trying to call the various functions
    #   ... use some nominal time stepping values ...
    dt = 0.1
    nt = 25
    v0 = 0.0 
    x0 = 1.0

    #time_step(dt, nt, v0, x0) 
    x, v, xe, ve = scenario_ForwardEuler(dt, nt)
    for i in range(nt+1):
        print(i, v[i], x[i], ve[i], xe[i])

    assert(True),'expected to make it this far wthout error.'
