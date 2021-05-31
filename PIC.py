#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

#EPS_0 = 8.85418782e-12   # C/V/m, vac. permittivity
EPS_0 = 1.0


# solves potential using Gauss-Seidel iterations with successive overrelaxation (SOR)
def solvePotentialGS(dx, rho, max_it) :

    dx2 = dx*dx       # precompute dx*dx
    SOR_W = 1.4;
    V = 0.0*rho
    ni = V.shape[0] # number of mesh nodes
    #print("The size of the numpy array is: "+str(ni))

    # solve potential
    for solver_it in range(max_it) :
        V[0] = 0.0      # dirichlet boundary on left,  V = 0
        V[ni-1] = 0.0   # dirichlet boundary on right, V = 0
		
        # Gauss Seidel method, V[i-1]-2*V[i]+V[i+1] = -dx^2*rho[i]/eps_0*/
        for i in range(1,ni-1) :
            g = 0.5*(V[i-1] + V[i+1] + dx2*rho[i]/EPS_0)
            V[i] = V[i] + SOR_W*(g-V[i]) # SOR

    return V;	


# computes electric field by differentiating potential
def computeGrad(dx, V, second_order) :

    ni = V.shape[0] # number of mesh nodes
    grad = 0.0*V

    # central difference on internal nodes
    for i in range(1,ni-1) :
        grad[i] = (V[i+1]-V[i-1])/(2*dx);

    # boundaries
    if second_order :
        grad[0] = -(3*V[0]-4*V[1]+V[2])/(2*dx)
        grad[ni-1] = -(-V[ni-3]+4*V[ni-2]-3*V[ni-1])/(2*dx)
    else : # first order
        grad[0] = -(V[0]-V[1])/dx
        grad[ni-1] = -(V[ni-2]-V[ni-1])/dx
    
    return grad


def update_pos_and_vel(pos, vel, dt, acc):

    new_vel = vel + dt*acc
    new_pos = pos + dt*new_vel

    return new_pos, new_vel

