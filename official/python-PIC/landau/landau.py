#!/usr/bin/env python

import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
from math import sin

import PIC

def plot_vals(x, vals, filename, ylabel=None):

    #plt.figure()
    #plt.yscale('log')
    plt.xlabel('x (m)')
    if ylabel:
        plt.ylabel(ylabel)
    plt.plot(x, vals)
    plt.savefig(filename)
    plt.clf()


def dump_vals(x, vals, dumpfile):

    with open(dumpfile, 'w') as F:
        for i in range(len(vals)):
            F.write("{0:25.14e}{1:25.14}\n".format(x[i], vals[i]))


def read_hdf5_particles(filename):
    data = h5py.File(filename, 'r')
    for att in data.attrs :
        print("\t",att,": ",data.attrs[att])
        if "particle_type" in att:
            print(data.attrs[att])
    #list(data.keys())
    step0=data['Step#0']
    #step1=data['Step#1']
    print(step0.keys())
    #print(type(step0['type'][0]))
    type_mask = step0['type'][:] == 1
    e_pos = step0['x'][type_mask]#.copy()
    print("# type 1: ",len(e_pos))
    return e_pos


if __name__ == "__main__":


    # A hack to read initial particles from and Aleph h5part dump file
    #e_pos = read_hdf5_particles("tmp.dump.h5")
    #print("Got ",len(e_pos), " e-")
    #print(e_pos.shape)
    #print(e_pos[:])

    params = PIC.read_parameters("landau.json")

    # Acquire simulation specs
    dt         = params['simulation']['dt']
    time_steps = params['simulation']['time_steps']
    xmin       = params['simulation']['xmin']
    xmax       = params['simulation']['xmax']
    N          = params['simulation']['num_elems']
    verbose    = params['simulation']['verbose']

    # Determine outputs
    output_phasespace = params['output']['phasespace']

    out_dir = "landout"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    out_dir = ''.join([out_dir, "/"])
    for d in ["V", "E", "rho"]:
        if not os.path.exists(''.join([out_dir, d])):
            os.makedirs(''.join([out_dir, d]))

    # Create the equally spaced 1D mesh
    mesh = np.linspace(xmin, xmax, N+1)
    dx = mesh[1]-mesh[0]

    if verbose:
        print("dt:\t\t",       dt         )
        print("time_steps:\t", time_steps )
        print("xmin:\t\t",     xmin       )
        print("xmax:\t\t",     xmax       )
        print("N:\t\t",        N          )
        print("dx:\t\t",       dx         )


    # Compute node volumes by scattering element volumes (= dx) to nodes
    node_vols = PIC.compute_node_volumes(mesh)
    dump_vals(mesh, node_vols, dumpfile=''.join([out_dir, "node_vols.dat"]))

    # Parse particle types
    particles = PIC.parse_particle_types(params)
    
    # This needs to be moved into PIC and unit tested...
    n0_max = -1.0
    for ptype in params['initial_conditions']:
        #num_p = params['initial_conditions'][ptype]['num']
        n0    = params['initial_conditions'][ptype]['n0']
        vx0   = params['initial_conditions'][ptype]['vx0']
        T     = params['initial_conditions'][ptype]['T']
        particle = [_ for _ in particles if _.type == ptype][0]
        #n0_max = max(n0_max, n0*particle.weight*dx)
        #PIC.particle_loader(mesh, n0, particle, T, K_B = 1.380649e-23)
        #particle.pos = np.linspace(xmin, xmax, num_p)
        #particle.pos = mesh[0:-1] +dx/2.0
        #particle.pos = e_pos
        #particle.velx = vx0*np.ones_like(particle.pos)
        #particle.vely = np.zeros_like(particle.pos)
        #particle.velz = np.zeros_like(particle.pos)
        if 'perturb_x' in params['initial_conditions'][ptype].keys():
            pert_x_expr = params['initial_conditions'][ptype]['perturb_x']
            pert_x = lambda x: eval(pert_x_expr)
            #pert_pos = np.array([pert_x(_) for _ in mesh])
            #particle.pos += np.array([pert_x(xi) for xi in particle.pos])
            PIC.particle_loader(mesh, n0, particle, T, K_B = 1.380649e-23, pert=pert_x)
            #dump_vals(mesh, pert_pos, dumpfile=''.join([out_dir, ptype, "_node_perts.dat"]))
            #plot_vals(mesh, pert_pos, filename=''.join([out_dir, "x_pert_", ptype, ".png"]))
        particle.velx = vx0*np.ones_like(particle.pos)
        particle.vely = np.zeros_like(particle.pos)
        particle.velz = np.zeros_like(particle.pos)

    if verbose:
        for p in particles:
            print("particle type: ", p.type)
            print("computational particles: ",p.pos.shape)
            print("Pos  (min, mean, max): "  ,np.min(p.pos),  np.mean(p.pos),  np.max(p.pos))
            print("Velx (min, mean, max): "  ,np.min(p.velx), np.mean(p.velx), np.max(p.velx))
            print("Vely (min, mean, max): "  ,np.min(p.vely), np.mean(p.vely), np.max(p.vely))
            print("Velz (min, mean, max): "  ,np.min(p.velz), np.mean(p.velz), np.max(p.velz))

    # Compute initial densities for sanity checking...
    p1 = [_ for _ in particles if _.charge < 0][0]
    p2 = [_ for _ in particles if _.charge > 0][0]
    e_dens = PIC.particle_scatter(mesh, p1.pos, p1.weight, np.ones_like(p1.pos))/node_vols
    i_dens = PIC.particle_scatter(mesh, p2.pos, p2.weight, np.ones_like(p2.pos))/node_vols
    dump_vals(mesh, e_dens, dumpfile=''.join([out_dir, "e-_density_0.dat"]))
    dump_vals(mesh, i_dens, dumpfile=''.join([out_dir, "ion_density_0.dat"]))
    elem_dens = np.zeros(N)
    for px in p1.pos:
        elem = PIC.get_elem_id(mesh, px)
        elem_dens[elem] += p1.weight
    elem_dens /= dx
    dump_vals(mesh, elem_dens, dumpfile=''.join([out_dir, "el_e-_density_0.dat"]))
    elem_dens *= 0
    for px in p2.pos:
        elem = PIC.get_elem_id(mesh, px)
        elem_dens[elem] += p2.weight
    elem_dens /= dx
    dump_vals(mesh, elem_dens, dumpfile=''.join([out_dir, "el_ion_density_0.dat"]))
    #raise "Stopping ..."


    # Compute initial potential field by:
    #   1) Scattering charge to nodes to 
    rho = np.zeros_like(mesh)
    for p in particles:
        rho -= PIC.particle_scatter(mesh, p.pos, p.weight, p.charge*np.ones_like(p.pos))
    rho /= node_vols

    #   2) Solving the linear system
    V = PIC.solveBanded(dx, rho)
    dump_vals(mesh, V, dumpfile=''.join([out_dir, "V_0.dat"]))

    # Compute the electric field from the potential
    E = PIC.computeGrad(dx, V, second_order=True)
    dump_vals(mesh, E, dumpfile=''.join([out_dir, "E_0.dat"]))

    # Gather the electric field from the mesh to the particles
    for p in particles:
        p.field = PIC.field_gather(mesh, p.pos, E)

    # Rewind initial particle velocities by 0.5 dt based on electric field
    for p in particles:
        p.velx += -0.5 * p.charge*p.field/p.mass*dt

    metricsF = open("landau_globals.dat", 'w')

    # Do time integration
    time = 0.0

    for t in range(time_steps):

        print(t, np.max(np.abs(E)), np.dot(E,E), len(particles[0].pos), len(particles[1].pos))
        metricsF.write("{} {} {} {} {}\n".format(
            time, np.max(np.abs(E)), np.dot(E,E), len(particles[0].pos), len(particles[1].pos)))

        rho = np.zeros_like(mesh)
        for p in particles:
            rho -= PIC.particle_scatter(mesh, p.pos, p.weight, p.charge*np.ones_like(p.pos))
        rho /= node_vols
        dump_vals(mesh, rho, dumpfile=''.join([out_dir, "rho/rho_", str(t).zfill(6), ".dat"]))

        # Write densities
        if output_phasespace:
            for p in particles:
                filename = ''.join([out_dir, p.type, "_phasespace_", str(t), ".csv"])
                with open(filename, 'w') as F:
                    for i in range(len(p.pos)):
                        F.write("{0:25.14e}, {1:25.14}\n".format(p.pos[i], p.velx[i]))

        # Solve the linear system
        V = PIC.solveBanded(dx, rho)
        dump_vals(mesh, V, dumpfile=''.join([out_dir, "V/V_", str(t).zfill(6), ".dat"]))

        # Compute the electric field from the potential
        E = PIC.computeGrad(dx, V, second_order=True)
        dump_vals(mesh, E, dumpfile=''.join([out_dir, "E/E_", str(t).zfill(6), ".dat"]))

        # Gather the electric field from the mesh to the particles
        for p in particles:
            p.field = PIC.field_gather(mesh, p.pos, E)

        # Update position and velocity
        for p in particles:
            acc = p.charge*p.field/p.mass    
            p.pos, p.velx = PIC.update_pos_and_vel(p.pos, p.velx, dt, acc)
            PIC.apply_periodic_bc(p, xmin, xmax)

        print("Finished step: ",t)
        metricsF.flush()

        time += dt

    metricsF.close()
