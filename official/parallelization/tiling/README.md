# Summary

Use a tiling approach to run a study on an HPC

# Description

As discussed in the README one level up, tiling means that Dakota
runs multiple concurrent instances of a driver within an HPC job.
The parallel computational work that each driver instance is responsible for
is run on availble resources (cpus, gpus, memory) within in the job.

The tiling approach uses local parallelism (the 
[asynchronous](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/reference/interface-asynchronous.html) keyword), and Dakota is run serially.

The primary challenge of tiling arises from the fact that Dakota is run
on a single node is not "aware of" the other nodes in the job. It is
the responsibility of the driver instances, which are all launched
locally on the same node where Dakota is running, to take advantage of available computational resources within the job. The best way to do
so can depend on the resource manager in use on the HPC (e.g. Slurm, SGE) and also the MPI implementation.

This example demonstrates use of a tool called [Flux](http://flux-framework.org/)
in concert with Slurm. See the README one level up for a brief explanation of Flux.

# Approach

We will step through the moving parts of workflow, explaining them
as we go.

## Job submission

A Slurm job (`slurm-script.sh`) is submitted using the `sbatch` command
that requests 3 nodes. It launches a flux instance on the three nodes.
The flux instance will manage the nodes in the job. The [start](https://flux-framework.readthedocs.io/projects/flux-core/en/latest/man1/flux-start.html)
subcommand is used to run a top-level script that runs the Dakota study. The command looks like:

```
srun -N 3 -n 3 --mpi=none flux start ./run_dakota.sh
```

The exports you see above this line in the script (`FLUX_QMANAGER_OPTIONS`
and `PSM2_DEVICES`) may not be needed on your system.

It may be necessary for you to specify an account either in `slurm-script.sh`
or on the command line when using the `sbatch` command.

## Launching Dakota

Dakota is run by the script `run_dakota.sh`, which is launched by `slurm-script.sh`. It handles any environment set up needed by Dakota, such as loading appropriate modules. The [flux run](https://flux-framework.readthedocs.io/projects/flux-core/en/latest/man1/flux-run.html)
command communicates with the flux instance that was started in `slurm-script.sh`
to request that the Dakota executable be run using one node (`-N 1`). The
instruction in `run_dakota.sh` is

```
flux run -N 1 -x dakota -input dakota_sampling.in
```

Allocating a dedicated node to Dakota itself by using the `-x` switch ensures
that no driver instances compete with Dakota for memory or processors. Because
Dakota is usually not very computationally demanding, this may not be necessary, and
you may wish to forgo using the `-x` swith or using `flux` at all to
schedule the Dakota process.

## Launch Drivers

In the Dakota input file, the `analsyis_driver` is the script `run_textbook.sh`. Note
the use of the `asynchronous` keyword to direct Dakota to launch multiple concurrent
driver instances. Usually, to avoid oversubscriping available resources, it's necessary
to limit the number of concurrent  evaluations by using the `evaluation_concurrency` keyword.
In this case, flux will handle scheduling of work performed by the driver, so it's okay
to launch all of them at the same time. If your study has very high available
concurrency (a sampling study with a very large number of samples, for examle), it may still be
necessary to throttle the number of concurrent driver instances.

## Run Simulations

The `run_textbook.sh` script uses `flux run` to request 14 cores for each simulation.

```
flux run -n 14 --label-io --output=eval-${eval_id}.out --error=eval-${eval_id}.err ./text_book_par $params $results 
```

Flux can manage GPUs as well as CPUs and permits specification of additional constraints.
See the [flux run](https://flux-framework.readthedocs.io/projects/flux-core/en/latest/man1/flux-run.html)
documentation for more details.

The job has 3 total nodes, and Dakota itself has exclusive use of one of them, so flux will manage
cores on the remaining 2 nodes to run each instance of the `text_book_par` simulation, ensuring
that cores are not oversubscribed. The `text_book_par` simulator can run on any number of cores,
and 14 is a somewhat arbitrary number. A real simulation will have its own memory, GPU, and CPU
requirements and parallel efficiency tradeoff. It's best to consult the documentation for your HPC to
learn the resources it provides and determine the optimal resources to rqurest to minimize the overall
time required to run the Dakota study.

# How to run the example

Build `text_book_par.cpp` (source in the folder above) using an MPI compiler and place the
executable alonside the Dakota input and scripts.

Then, run:

```
sbatch slurm-script.sh
```

It may be necessary to provide an account number or to modify the requested partition for your HPC.

Running the example will produce output from the study in the slurm console output. In addition,
output from each simulation will be written to files named `eval-N.out` and `eval-N.err`, where `N` is the Dakota
evaluation number.`The console output includes information about where each MPI task ran. By comparing
these, you can see how Flux allocated cores to each instance.
