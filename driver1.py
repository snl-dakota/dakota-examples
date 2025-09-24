#!/usr/bin/env python

import numpy as np

import PIC



if __name__ == "__main__":

    params = PIC.read_parameters("driver1.json")

    # Acquire simulation specs
    dt         = params['simulation']['dt']
    time_steps = params['simulation']['time_steps']
    xmin       = params['simulation']['xmin']
    xmax       = params['simulation']['xmax']
    N          = params['simulation']['num_elems']
    GS_iters   = params['simulation']['GS_iters']

    print(dt         )
    print(time_steps )
    print(xmin       )
    print(xmax       )
    print(N          )
    print(GS_iters   )

    # Create the equally spaced 1D mesh
    mesh = np.linspace(xmin, xmax, N+1)
    dx = mesh[1]-mesh[0]

    # Compute node volumes by scattering element volumes (= dx) to nodes
    node_vols = PIC.compute_node_volumes(mesh)

    # Parse particle types
    particles = PIC.parse_particle_types(params)
    

    # Create computational particles (i.e. populate pos and vel arrays)
    # ... use temporary lists to later create the numpy arrays
    pos_list = {}
    vel_list = {}
    for p in particles:
        pos_list[p.type] = []
        vel_list[p.type] = []

    for cond in params['initial_conditions']:
        if "particle" in cond:
            ptype = params['initial_conditions'][cond]['type']
            pos_list[ptype].append(params['initial_conditions'][cond]['x0'])
            vel_list[ptype].append(params['initial_conditions'][cond]['v0'])

    for p in pos_list:
        particle = [_ for _ in particles if _.type == p][0]
        particle.pos = np.array(pos_list[p])
        particle.vel = np.array(vel_list[p])
        particle.field = np.zeros(len(pos_list[p]))


    print("\n\n")
    for p in particles:
        print(p.type, p.pos, p.vel, p.field, p.mass, p.charge)
        print(p.pos.shape)

    # Compute initial potential field by:
    #   1) Scattering charge to nodes to 
    rho = np.zeros_like(mesh)
    for p in particles:
        rho -= PIC.charge_scatter(mesh, p.pos, p.weight, p.charge*np.ones_like(p.pos))
    rho /= node_vols
    print(rho)
    #   2) Solving the linear system
    V = PIC.solvePotentialGS(dx, rho, GS_iters)
    print(V)

    # Compute the electric field from the potential
    E = PIC.computeGrad(dx, V, second_order=True)
    print(E)

    # Gather the electric field from the mesh to the particles
    for p in particles:
        p.field = PIC.field_gather(mesh, p.pos, E)
        print(p.field)

    # Rewind initial particle velocities by 0.5 dt based on electric field
    for p in particles:
        p.vel += -0.5 * p.charge*p.field/p.mass*dt
        print(p.vel)

    # Do time integration
    # Loop over previous steps

    for t in range(time_steps):
        rho = np.zeros_like(mesh)
        for p in particles:
            rho -= PIC.charge_scatter(mesh, p.pos, p.weight, p.charge*np.ones_like(p.pos))
        rho /= node_vols
        #print("rho = ", rho)

        # Solve the linear system
        V = PIC.solvePotentialGS(dx, rho, GS_iters)
        #print("V = ", V)

        # Compute the electric field from the potential
        E = PIC.computeGrad(dx, V, second_order=True)
        #print("E = ", E)

        # Gather the electric field from the mesh to the particles
        for p in particles:
            p.field = PIC.field_gather(mesh, p.pos, E)
           # print("Field = ", p.field)

        # Update position and velocity
        for p in particles:
            # acc = 1                        # --- Temporary acceleration value
            acc = p.charge*p.field/p.mass    
            p.pos, p.vel = PIC.update_pos_and_vel(p.pos, p.vel, dt, acc)
            if p.charge < 0:
                print(t*dt, p.pos[0], p.vel[0])



