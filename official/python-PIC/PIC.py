#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_banded

from particle import Particle

# solves potential using scipy's banded linear solver
def solveBanded(dx, rho, bc = "dirichlet", left_side = 0.0, right_side = 0.0, eps0=8.854187817e-12) : # C/V/m, vac. permittivity
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
    if (bc == "dirichlet"):
        ab[1][0]    = 1.0
        ab[1][ni-1] = 1.0
        b[0]        = left_side
        b[ni-1]     = right_side

    # For Neumann BCs
    elif (bc == "neumann"):
        ab[1][0]    = 1.0
        ab[1][ni-1] = 1.0
        b[0]        = (left_side*dx - 2*b[1] + b[2]/2.0) / (-3.0/2.0)
        b[ni-1]     = (right_side*dx + 3.0/2.0*b[ni-3] - 2*b[ni-2]) / (-1.0/2.0)

    # Do the solve
    V = solve_banded((1, 1), ab, b)

    return V;	

# solves potential using Gauss-Seidel iterations with successive overrelaxation (SOR)
def solvePotentialGS(dx, rho, max_it, bc = "Dirichlet", left_side = 0.0, right_side = 0.0, eps0=8.854187817e-12) :

    dx2 = dx*dx       # precompute dx*dx
    SOR_W = 1.4;
    V = 0.0*rho
    ni = V.shape[0] # number of mesh nodes
    #print("The size of the numpy array is: "+str(ni))

    # solve potential
    if (bc == "Dirichlet" or bc == "dirichlet"):
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


def apply_outflux_bc(particles, left, right):

    new_part = Particle(particles.type, { 'charge': particles.charge, 'mass': particles.mass, 'weight': particles.weight })

    mask1 = particles.pos >= left
    mask2 = particles.pos <= right
    mask = np.logical_and(mask1, mask2)

    new_part.pos   = particles.pos  [mask]
    new_part.velx  = particles.velx [mask]
    new_part.vely  = particles.vely [mask]
    new_part.velz  = particles.velz [mask]
    new_part.field = particles.field[mask]

    return new_part


def apply_periodic_bc(particles, left, right):

    mask1 = particles.pos > right
    mask2 = particles.pos < left

    particles.pos[mask1] = left  + np.mod((particles.pos[mask1]-left),(right-left))
    particles.pos[mask2] = right + np.mod((particles.pos[mask2]-right),(left-right))

    return particles


def get_elem_id(mesh, pos):

    # Assumes equal mesh spacing
    # ... will need to generalize to support unequal mesh spacing
    dx = abs(mesh[1] - mesh[0])
    elem_id = np.floor((pos-mesh[0])/dx).astype(int)
    # Handle pos on outer domain boundary
    if elem_id.size > 1:
        elem_id[elem_id<0] = 0
        elem_id[elem_id>len(mesh)-2] = 0
    return elem_id


def charge_scatter(mesh, pos, part_wt, charge, verbose=False):

    # Distributes charge in 1d
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


def particle_loader(xleft, xright, num_den, particle, Temp, K_B = 1.380649e-23):
    
    box_vol  = float((xright - xleft))
    num_real = num_den * box_vol
    num_sim  = round(num_real/particle.weight)
    sigma = np.sqrt(K_B*Temp / particle.mass)

    # sample position (uniform) and velocity (Maxwellian)
    particle.pos = np.random.uniform(xleft, xright, num_sim)
    particle.velx = sigma*np.random.standard_normal(num_sim)
    particle.vely = sigma*np.random.standard_normal(num_sim)
    particle.velz = sigma*np.random.standard_normal(num_sim)

    return


if __name__=='__main__':
    driver()
