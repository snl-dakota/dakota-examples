#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import os

import PIC

def update_hist_plot(data):
    plt.ion()
    plt.clf()
    n, bins, patches = plt.hist(data, 50, range=(-0.001,0.001), density=True)
    plt.xlabel('pos')
    plt.ylabel('Probability')
    plt.title('Histogram')
    plt.draw()
    plt.pause(0.001)


def update_line_plot(time, x, y1, y2):
    plt.ion()
    plt.clf()
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(4*slab_xmin, 4*slab_xmax)
    plt.ylim(top=1.25*n0_max)
    plt.title('Time ='+str(time))
    plt.draw()
    plt.pause(0.001)



if __name__ == "__main__":

    params = PIC.read_parameters("tsi.json")

    # Acquire simulation specs
    dt         = params['simulation']['dt']
    time_steps = params['simulation']['time_steps']
    xmin       = params['simulation']['xmin']
    xmax       = params['simulation']['xmax']
    N          = params['simulation']['num_elems']
    verbose    = params['simulation']['verbose']

    # Determine outputs
    show_plots       = params['output']['show_plots']
    output_densities = params['output']['densities']

    if output_densities:
        if not os.path.exists("tsi_output"):
            os.makedirs("tsi_output")

    if verbose:
        print("dt:\t\t",         dt         )
        print("time_steps:\t", time_steps )
        print("xmin:\t\t",       xmin       )
        print("xmax:\t\t",       xmax       )
        print("N:\t\t",          N          )

    # Create the equally spaced 1D mesh
    mesh = np.linspace(xmin, xmax, N+1)
    dx = mesh[1]-mesh[0]

    # Compute node volumes by scattering element volumes (= dx) to nodes
    node_vols = PIC.compute_node_volumes(mesh)

    # Parse particle types
    particles = PIC.parse_particle_types(params)
    
    # This needs to be moved into PIC and unit tested...
    n0_max = -1.0
    for ptype in params['initial_conditions']:
        slab_xmin = params['initial_conditions'][ptype]['xmin']
        slab_xmax = params['initial_conditions'][ptype]['xmax']
        n0   = params['initial_conditions'][ptype]['n0']
        vx0  = params['initial_conditions'][ptype]['vx0']
        T    = params['initial_conditions'][ptype]['T']
        particle = [_ for _ in particles if _.type == ptype][0]
        n0_max = max(n0_max, n0*particle.weight*dx)
        PIC.particle_loader(slab_xmin, slab_xmax, n0, particle, T, K_B = 1.380649e-23)

    if verbose:
        for p in particles:
            print("particle type: ", p.type)
            print("computational particles: ",p.pos.shape)
            print("Pos  (min, mean, max): "  ,np.min(p.pos),  np.mean(p.pos),  np.max(p.pos))
            print("Velx (min, mean, max): "  ,np.min(p.velx), np.mean(p.velx), np.max(p.velx))
            print("Vely (min, mean, max): "  ,np.min(p.vely), np.mean(p.vely), np.max(p.vely))
            print("Velz (min, mean, max): "  ,np.min(p.velz), np.mean(p.velz), np.max(p.velz))

    # Compute initial potential field by:
    #   1) Scattering charge to nodes to 
    rho = -0.0*np.ones_like(mesh)
    for p in particles:
        rho -= PIC.charge_scatter(mesh, p.pos, p.weight, p.charge*np.ones_like(p.pos))
    rho /= node_vols

    #   2) Solving the linear system
    V = PIC.solveBanded(dx, rho)
    #print(V)
    with open("python_V.dat", 'w') as F:
        for i in range(len(V)):
            F.write("{0:25.14e}{1:25.14}\n".format(mesh[i], V[i]))

    # Compute the electric field from the potential
    E = PIC.computeGrad(dx, V, second_order=True)

    # Gather the electric field from the mesh to the particles
    for p in particles:
        p.field = PIC.field_gather(mesh, p.pos, E)

    # Rewind initial particle velocities by 0.5 dt based on electric field
    for p in particles:
        p.velx += -0.5 * p.charge*p.field/p.mass*dt


    # Do time integration
    time = 0.0
    #update_hist_plot(p.pos)
    #plt.show()
    #plt.pause(0.001)
    if show_plots:
        p1 = [_ for _ in particles if _.charge < 0][0]
        p2 = [_ for _ in particles if _.charge > 0][0]
        fig, ax = plt.subplots()
        update_line_plot(time, mesh,
                         PIC.charge_scatter(mesh, p1.pos, p1.weight, p1.weight*np.ones_like(p1.pos)),
                         PIC.charge_scatter(mesh, p2.pos, p2.weight, p2.weight*np.ones_like(p2.pos)))
        plt.ylim(top=1.25*n0_max)
        plt.show()
        plt.pause(0.001)


    for t in range(time_steps):
        rho = np.zeros_like(mesh)
        for p in particles:
            rho -= PIC.charge_scatter(mesh, p.pos, p.weight, p.charge*np.ones_like(p.pos))
        rho /= node_vols

        # Allow real-time plotting
        if show_plots:
            p1 = [_ for _ in particles if _.charge < 0][0]
            p2 = [_ for _ in particles if _.charge > 0][0]
            update_line_plot(time, mesh,
                             PIC.charge_scatter(mesh, p1.pos, p1.weight, p1.weight*np.ones_like(p1.pos)),
                             PIC.charge_scatter(mesh, p2.pos, p2.weight, p2.weight*np.ones_like(p2.pos)))

        # Write densities
        if output_densities:
            for p in particles:
                filename = "tsi_output/"+p.type+"_density_"+str(t)+".csv"
                density = PIC.charge_scatter(mesh, p.pos, p.weight, np.ones_like(p.pos))/node_vols
                with open(filename, 'w') as F:
                    for i in range(len(V)):
                        F.write("{0:25.14e}, {1:25.14}\n".format(mesh[i], density[i]))

        # Solve the linear system
        V = PIC.solveBanded(dx, rho)

        # Compute the electric field from the potential
        E = PIC.computeGrad(dx, V, second_order=True)

        # Gather the electric field from the mesh to the particles
        for p in particles:
            p.field = PIC.field_gather(mesh, p.pos, E)

        # Update position and velocity
        for p in particles:
            acc = p.charge*p.field/p.mass    
            p.pos, p.velx = PIC.update_pos_and_vel(p.pos, p.velx, dt, acc)

            #if t%5 == 0 and p.charge < 0:
            #    n, bins, patches = plt.hist(p.pos, 50, range=(-0.001,0.001), density=True)
            #    plt.xlabel('pos')
            #    plt.ylabel('Probability')
            #    plt.title('Histogram')
            #    update_hist_plot(p.pos)

        print("Finished step: ",t)

        time += dt
