#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import os
from math import sin
from mpi4py import MPI  # Added for parallelization

import PIC

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def update_hist_plot(data):
    plt.ion()
    plt.clf()
    n, bins, patches = plt.hist(data, 50, range=(-0.001,0.001), density=True)
    plt.xlabel('pos')
    plt.ylabel('Probability')
    plt.title('Histogram')
    plt.draw()
    plt.pause(0.001)


def update_line_plot(time, x, y1, y2, n0_max):
    plt.ion()
    plt.clf()
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(xmin, xmax)
    plt.ylim(top=1.25*n0_max if n0_max > 0 else 1.0)
    plt.title('Time ='+str(time))
    plt.draw()
    plt.pause(0.001)


if __name__ == "__main__":

    # Only rank 0 reads parameters and broadcasts them, or everyone reads (simpler)
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

    if output_densities and rank == 0:
        if not os.path.exists("tsi_output"):
            os.makedirs("tsi_output")

    if verbose and rank == 0:
        print(f"Running on {size} MPI ranks")
        print("dt:\t\t",         dt         )
        print("time_steps:\t", time_steps )
        print("xmin:\t\t",       xmin       )
        print("xmax:\t\t",       xmax       )
        print("N:\t\t",          N          )

    # Create the equally spaced 1D mesh (Replicated on all ranks)
    mesh = np.linspace(xmin, xmax, N+1)
    dx = mesh[1]-mesh[0]

    # Compute node volumes (Replicated on all ranks)
    node_vols = PIC.compute_node_volumes(mesh)

    # Parse particle types
    particles = PIC.parse_particle_types(params)

    # Distribute particles across ranks
    for ptype in params['initial_conditions']:
        spec = params['initial_conditions'][ptype]
        num_p = spec['num']
        vx0   = spec['vx0']
        T     = spec['T']
        particle = [_ for _ in particles if _.type == ptype][0]

        # Calculate local slice of particles for this rank
        # This replaces the global np.linspace with a rank-specific slice
        local_num_p = num_p // size
        remainder = num_p % size

        start_idx = rank * local_num_p + min(rank, remainder)
        end_idx = start_idx + local_num_p + (1 if rank < remainder else 0)

        # Generate the specific slice of positions to maintain identical results to serial
        # x_i = xmin + i * (xmax - xmin) / (num_p - 1)
        indices = np.arange(start_idx, end_idx)
        particle.pos = xmin + indices * (xmax - xmin) / (num_p - 1)

        particle.velx = vx0 * np.ones_like(particle.pos)
        particle.vely = np.zeros_like(particle.pos)
        particle.velz = np.zeros_like(particle.pos)

        if 'perturb_x' in spec.keys():
            pert_x_expr = spec['perturb_x']
            # Use a vectorized eval if possible, but keeping the original logic:
            pert_x = lambda x: eval(pert_x_expr)
            particle.pos += np.array([pert_x(xi) for xi in particle.pos])

    if verbose and rank == 0:
        for p in particles:
            print(f"particle type: {p.type}")
            # Note: This now prints the local count per rank
            print(f"local computational particles: {p.pos.shape}")
            print("Pos  (min, mean, max): "  ,np.min(p.pos),  np.mean(p.pos),  np.max(p.pos))

    # Compute initial potential field
    # 1) Local scatter
    rho_local = 0.0 * np.ones_like(mesh)
    for p in particles:
        rho_local -= PIC.charge_scatter(mesh, p.pos, p.weight, p.charge * np.ones_like(p.pos))

    # 2) Global Sync (AllReduce)
    rho_global = np.zeros_like(mesh)
    comm.Allreduce(rho_local, rho_global, op=MPI.SUM)
    rho_global /= node_vols

    # 3) Local Solve
    V = PIC.solveBanded(dx, rho_global)

    if rank == 0:
        with open("python_V.dat", 'w') as F:
            for i in range(len(V)):
                F.write("{0:25.14e}{1:25.14}\n".format(mesh[i], V[i]))

    # Compute the electric field from the potential (Local)
    E = PIC.computeGrad(dx, V, second_order=True)

    # Gather the electric field from the mesh to the particles (Local)
    for p in particles:
        p.field = PIC.field_gather(mesh, p.pos, E)

    # Rewind initial particle velocities (Local)
    for p in particles:
        p.velx += -0.5 * p.charge * p.field / p.mass * dt

    # Time integration
    time = 0.0
    # Default n0_max for plotting if not explicitly calculated
    n0_max = 1.0

    if show_plots and rank == 0:
        p1 = [_ for _ in particles if _.charge < 0][0]
        p2 = [_ for _ in particles if _.charge > 0][0]
        fig, ax = plt.subplots()
        # Initial plot uses rank 0's local charge scatter as a proxy for visualization
        update_line_plot(time, mesh,
                         PIC.charge_scatter(mesh, p1.pos, p1.weight, p1.weight*np.ones_like(p1.pos)),
                         PIC.charge_scatter(mesh, p2.pos, p2.weight, p2.weight*np.ones_like(p2.pos)),
                         n0_max)
        plt.show()
        plt.pause(0.001)

    for t in range(time_steps):
        # Local charge scatter
        rho_local = np.zeros_like(mesh)
        for p in particles:
            rho_local -= PIC.charge_scatter(mesh, p.pos, p.weight, p.charge * np.ones_like(p.pos))

        # Global Sync
        rho_global = np.zeros_like(mesh)
        comm.Allreduce(rho_local, rho_global, op=MPI.SUM)
        rho_global /= node_vols

        # Real-time plotting on rank 0 only
        if show_plots and rank == 0:
            p1 = [_ for _ in particles if _.charge < 0][0]
            p2 = [_ for _ in particles if _.charge > 0][0]
            update_line_plot(time, mesh,
                             PIC.charge_scatter(mesh, p1.pos, p1.weight, p1.weight*np.ones_like(p1.pos)),
                             PIC.charge_scatter(mesh, p2.pos, p2.weight, p2.weight*np.ones_like(p2.pos)),
                             n0_max)

        # Write densities (Each rank writes its own subset to avoid file locking)
        if output_densities:
            for p in particles:
                filename = f"tsi_output/{p.type}_phasespace_{t}_rank{rank}.csv"
                with open(filename, 'w') as F:
                    for i in range(len(p.pos)):
                        F.write("{0:25.14e}, {1:25.14}\n".format(p.pos[i], p.velx[i]))

        # Solve the linear system (Local)
        V = PIC.solveBanded(dx, rho_global)

        # Compute the electric field (Local)
        E = PIC.computeGrad(dx, V, second_order=True)

        # Gather the electric field (Local)
        for p in particles:
            p.field = PIC.field_gather(mesh, p.pos, E)

        # Update position and velocity (Local)
        for p in particles:
            acc = p.charge * p.field / p.mass
            p.pos, p.velx = PIC.update_pos_and_vel(p.pos, p.velx, dt, acc)
            PIC.apply_periodic_bc(p, xmin, xmax)

        if rank == 0:
            print("Finished step: ", t)

        time += dt
