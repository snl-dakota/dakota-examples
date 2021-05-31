import numpy as np
import matplotlib.pyplot as plt


def scenario_oscillator(dt, nt, leap_frog=False):
    '''
    Time integration using example from
         https://www.particleincell.com/2011/velocity-integration/

    Input variables:
        dt = time step size
        nt = number of time steps
        leap_frog = Boolean flag using either:
           True: Leap Frog time stepping OR
           False: Explicit (Forward) Euler time stepping
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

    vel_index_shift = 0

    if leap_frog:
        vel[0] = vel[0] -0.5*accel(pos[0])*dt
        vel_index_shift = 1
    
    # Do time integration
    for step in range(nt):
        acc = accel(pos[step])
        vel[step+1] = vel[step] + dt*acc
        pos[step+1] = pos[step] + dt*vel[step+vel_index_shift]

        # Compute exact values
        time += dt
        xexact[step+1] =  np.cos(omega*time)
        vexact[step+1] = -np.sin(omega*time)*omega

    return pos, vel, xexact, vexact




if __name__ == "__main__":

    # Start by trying to call the various functions
    #   ... use some nominal time stepping values ...
    dt = 0.1
    nt = 42
    x0 = 1.0
    v0 = 0.0 

    # Use Forward Euler
    pos, vel, exact_x, exact_v = scenario_oscillator(dt, nt)
    for i in range(nt+1):
        print(i, i*dt, vel[i], pos[i], exact_v[i], exact_x[i])


    # Now use Leap Frog
    pos, vel, exact_x, exact_v = scenario_oscillator(dt, nt, True)
    for i in range(nt+1):
        print(i, i*dt, vel[i], pos[i], exact_v[i], exact_x[i])


    assert(True),'expected to make it this far wthout error.'
