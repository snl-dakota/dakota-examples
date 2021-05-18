#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

#EPS_0 = 8.85418782e-12   # C/V/m, vac. permittivity
EPS_0 = 1.0


# solves potential using Gauss-Seidel iterations with successive overrelaxation (SOR)
def solvePotentialGS(dx, rho, max_it) :

    dx2 = dx*dx       # precompute dx*dx
    SOR_W = 1.4;
    phi = 0.0*rho
    ni = phi.shape[0] # number of mesh nodes
    #print("The size of the numpy array is: "+str(ni))

    # solve potential
    for solver_it in range(max_it) :
        phi[0] = 0.0      # dirichlet boundary on left,  V = 0
        phi[ni-1] = 0.0   # dirichlet boundary on right, V = 0
		
        # Gauss Seidel method, phi[i-1]-2*phi[i]+phi[i+1] = -dx^2*rho[i]/eps_0*/
        for i in range(1,ni-1) :
            g = 0.5*(phi[i-1] + phi[i+1] + dx2*rho[i]/EPS_0)
            phi[i] = phi[i] + SOR_W*(g-phi[i]) # SOR

    return phi;	

