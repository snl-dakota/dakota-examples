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

    time = np.linspace(0,nt*dt,nt+1)

    return pos, vel, time


def plot_pos_vel(time, pos, vel, exact_pos, exact_vel, leap_frog=False):

    plt.plot(time, pos, marker='o', label='Position (x)')
    plt.plot(time, exact_pos(time), label='Exact (x)')
    if leap_frog:
        dt = time[1]-time[0]
        plt.plot(time-0.5*dt, vel, marker='o', label='Velocity (v)')
    else:
        plt.plot(time, exact_vel(time), marker='o', label='Velocity (v)')
    plt.plot(time, exact_vel(time), label='Exact (v)')
    plt.legend()
    plt.show()


def plot_phase(time, pos, vel, exact_pos, exact_vel, leap_frog=False):

    if leap_frog:
        plt.plot(exact_vel(time-0.5*dt), exact_pos(time), label='Theory')
    else:
        plt.plot(exact_vel(time), exact_pos(time), label='Theory')
    plt.plot(vel, pos, '--', label='Numerical')
    plt.legend()
    plt.show()



if __name__ == "__main__":

    # Start by trying to call the various functions
    #   ... use some nominal time stepping values ...
    dt = 0.1
    nt = 232
    x0 = 1.0
    v0 = 0.0 

    # Exact velocity and position functions
    omega = 2*np.pi/(50.0*dt)
    exact_x = lambda t :  np.cos(omega*t)
    exact_v = lambda t : -np.sin(omega*t)*omega

    # Use Forward Euler
    pos, vel, time = scenario_oscillator(dt, nt)
    for i in range(nt+1):
        print(i, time[i], vel[i], pos[i], exact_v(time[i]), exact_x(time[i]))

    #plot_pos_vel(time, pos, vel, exact_x, exact_v)
    #plot_phase(time, pos, vel, exact_x, exact_v)


    # Now use Leap Frog
    pos, vel, time = scenario_oscillator(dt, nt, True)
    for i in range(nt+1):
        print(i, time[i], vel[i], pos[i], exact_v(time[i]), exact_x(time[i]))

    #plot_pos_vel(time, pos, vel, exact_x, exact_v, leap_frog=True)
    #plot_phase(time, pos, vel, exact_x, exact_v, leap_frog=True)


    assert(True),'expected to make it this far wthout error.'
