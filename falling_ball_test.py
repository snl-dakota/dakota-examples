import numpy as np
import matplotlib.pyplot as plt

from gallery import FallingBall
import PIC

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
    
    # Use a FallingBall object to test the Leap Frog time integator in the PIC module
    ball = FallingBall(x0, v0, E=-10.0, q=1.0, m=1.0)

    test_pos = np.empty(time.size)
    test_vel = 0.0*test_pos
    test_pos[0] = x0
    test_vel[0] = v0 - 0.5*ball.exact_a(0)*dt

    for i in range(1, time.size):
        xval = test_pos[i-1]
        vval = test_vel[i-1]
        test_pos[i], test_vel[i] = PIC.update_pos_and_vel(xval, vval, dt, ball.forcing_term(xval))

    assert( np.allclose(pos, test_pos, rtol=0, atol=1.e-20)),'positions should exactly agree.'
    assert( np.allclose(vel, test_vel, rtol=0, atol=1.e-20)),'velocities should exactly agree.'
