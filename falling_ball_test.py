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
    
    time = np.linspace(0,nt*dt,nt)

    E   = -10.0                 # placeholder for later Electric Field Function
    q   = 1.0                  # Dummy charge value - TODO: replace with meaningful value
    m   = 1.0                  # Dummy mass value - TODO: replace with meaningful value
    vel[0] = v0-0.5*q/m*E*dt   # move vel back by 1/2*dt
    pos[0] = x0                # initialize position

    for i in range(1,nt):
        vel[i] = vel[i-1] + q/m*E*dt
        pos[i] = pos[i-1] + vel[i]*dt      # + 1/2*q/m*E*dt**2

    return (pos,vel,time)

if __name__ == "__main__":

    # Start by trying to call the various functions
    #   ... use some nominal time stepping values ...
    dt = 0.1
    nt = 46
    v0 = 0.0 
    x0 = 100.0

    pos,vel,time = time_step(dt, nt, v0, x0) 

    plt.plot(time, pos, label='Position (x)')
    plt.plot(time, vel, label='Velocity (v)')
    plt.legend()
    plt.savefig("vel_pos_graph.png");
    
    assert(True),'expected to make it this far wthout error.'
