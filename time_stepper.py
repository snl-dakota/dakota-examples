import numpy as np
import matplotlib.pyplot as plt


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

    pos = np.empty(nt+1)
    vel = np.empty(nt+1)

    # Assign initial conditions
    pos[0] = x0
    vel[0] = v0
    xexact[0] = x0
    vexact[0] = v0

    # Do time integration
    for step in range(nt):
        acc = accel(pos[step])
        vel[step+1] = vel[step] + dt*acc
        pos[step+1] = pos[step] + dt*vel[step]

        # Compute exact values
        time += dt
        xexact[step+1] =  np.cos(omega*time)
        vexact[step+1] = -np.sin(omega*time)

    return pos, vel, xexact, vexact




if __name__ == "__main__":

    # Start by trying to call the various functions
    #   ... use some nominal time stepping values ...
    dt = 0.1
    nt = 25
    v0 = 0.0 
    x0 = 1.0

    x, v, xe, ve = scenario_ForwardEuler(dt, nt)
    for i in range(nt+1):
        print(i, v[i], x[i], ve[i], xe[i])

    assert(True),'expected to make it this far wthout error.'
