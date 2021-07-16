#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
import numpy as np

from particle import Particle

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


def get_elem_id(mesh, pos):

    # Assumes equal mesh spacing
    # ... will need to generalize to support unequal mesh spacing
    dx = abs(mesh[1] - mesh[0])
    return np.floor((pos-mesh[0])/dx).astype(int)


def charge_scatter(mesh, pos, part_wt, charge):

    #Distributes charge in 1d

    '''
    sp_wt = pos/dx
    right = 1-sp_wt
    left  = sp_wt

    charge_den[get_elem_id(mesh,pos)] = right*charge
    charge_den[get_elem_id(mesh,pos)+1] = left*charge
    return sp_wt_right, sp_wt_left
    '''

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


def charge_density(mesh, pos, part_wt, charge):

    return charge_scatter(mesh, pos, part_wt, charge)/compute_node_volumes(mesh)


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


if __name__=='__main__':
    driver()
