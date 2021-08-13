#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
import numpy as np
import random as rnd
from scipy.linalg import solve_banded

from particle import Particle

# solves potential using scipy's banded linear solver
def solveBanded(dx, rho, eps0=8.854187817e-12) : # C/V/m, vac. permittivity
    # This is based on:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_banded.html#scipy.linalg.solve_banded

    # precompute dx*dx
    dx2 = dx*dx

    # number of mesh nodes
    ni = rho.shape[0]

    # Form the matrix - does not change so that we might want to do it once and reuse
    ab = np.zeros((3,len(rho)))
    # ... and the right-hand-side - does change over time
    b  = np.zeros(len(rho))
    for i in range(1,ni-1) :
        ab[2][i-1] = 1.0
        ab[1][i  ] = -2.0
        ab[0][i+1] = 1.0
        b[i]      = -dx2*rho[i]/eps0

    # For Dirichlet BCs
    ab[1][0]    = 1.0
    ab[1][ni-1] = 1.0
    b[0]        = 0.0
    b[ni-1]     = 0.0

    # Do the solve
    V = solve_banded((1, 1), ab, b)

    return V;	

# solves potential using Gauss-Seidel iterations with successive overrelaxation (SOR)
def solvePotentialGS(dx, rho, max_it, eps0=8.854187817e-12) :

    dx2 = dx*dx       # precompute dx*dx
    SOR_W = 1.4;
    V = 0.0*rho
    ni = V.shape[0] # number of mesh nodes
    #print("The size of the numpy array is: "+str(ni))

    # solve potential
    for solver_it in range(max_it) :
        V[0] = 0.0      # dirichlet boundary on left,  V = 0
        V[ni-1] = 0.0   # dirichlet boundary on right, V = 0
		
        # Gauss Seidel method, V[i-1]-2*V[i]+V[i+1] = -dx^2*rho[i]/eps0*/
        for i in range(1,ni-1) :
            g = 0.5*(V[i-1] + V[i+1] + dx2*rho[i]/eps0)
            deltaV = SOR_W*(g-V[i]) # SOR
            V[i] = V[i] + deltaV

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


def get_elem_id(mesh, pos):

    # Assumes equal mesh spacing
    # ... will need to generalize to support unequal mesh spacing
    dx = abs(mesh[1] - mesh[0])
    return np.floor((pos-mesh[0])/dx).astype(int)


def charge_scatter(mesh, pos, part_wt, charge, verbose=False):

    #Distributes charge in 1d

    n   = mesh.shape[0]
    rho = np.zeros(n)

    for i in range(len(pos)):
        elem_id = get_elem_id(mesh, pos[i])
        left_x  = mesh[elem_id]
        right_x = mesh[elem_id+1]
        dx  = abs(right_x-left_x)

        wt_right = (pos[i]-left_x)/dx
        wt_left  = 1-wt_right
            
        rho[elem_id]   += charge[i]*part_wt*wt_left 
        rho[elem_id+1] += charge[i]*part_wt*wt_right 
        if verbose:
            print(pos, charge)
    if verbose:
        print(rho)
    return rho



def field_gather(mesh, pos, field):

    gathered_vals = np.empty(pos.shape[0])
    for i,x in enumerate(pos):
        elem_id = get_elem_id(mesh, x)
        left_x = mesh[elem_id]
        right_x = mesh[elem_id+1]
        weight_right = (x-left_x)/(right_x-left_x)
        weight_left = 1.0 - weight_right
        gathered_vals[i] = field[elem_id]*weight_left + field[elem_id+1]*weight_right

    return gathered_vals


def compute_node_volumes(mesh):

    node_vols = 0.0*mesh

    elem_centers = np.zeros(mesh.shape[0]-1)
    for elem in range(len(mesh)-1):
        elem_centers[elem] = 0.5*(mesh[elem] + mesh[elem+1])

    dx = abs(mesh[1] - mesh[0])
    return charge_scatter(mesh, elem_centers, 1.0, dx*np.ones_like(elem_centers))


def charge_density(mesh, pos, part_wt, charge, node_vols):

    return charge_scatter(mesh, pos, part_wt, charge)/node_vols


def read_parameters(filename):

    with open(filename) as F:
        params = json.load(F)
    return params


def parse_particle_types(params):
    
    particles = []

    for part_type in params['particle_types'] :
        particles.append( Particle(part_type, params['particle_types'][part_type]) )

    return particles


def driver():
    params = read_parameters("test_params.json")
    return

def calc_energy(mesh, V, particle): #pos, vel, mass_e, charge_e):   #, charge_ion):
    
    field = field_gather(mesh, particle.pos, V)
    potentialEnergy = field * particle.charge
    kineticEnergy   =  particle.mass * particle.vel**2 / 2.0

    totalEnergy = potentialEnergy + kineticEnergy

    return potentialEnergy, kineticEnergy, totalEnergy

def particle_loader(xleft, xright, num_den, num_sim, mass, Temp, K_B = 1.380649e-23):
    
    box_vol  = float((xright - xleft))
    num_real = num_den * box_vol
    mpw      = num_real/num_sim
    vel_seed = np.sqrt(2*K_B*Temp / mass)

    particles = np.zeros((num_sim, 3))

    # sample position and velocity
    for i in range(num_sim):
        pos = rnd.uniform(xleft, xright)
        vel = rnd.normal(vel_seed) 

        particles[i][0] = pos
        particles[i][1] = vel
        particles[i][2] = mpw
    
    return particles


if __name__=='__main__':
    driver()
