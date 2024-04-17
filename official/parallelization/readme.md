# Summary

Approaches for using Dakota on HPCs

# Description

This family of examples presents approaches to using
HPC resources in Dakota studies. To understand the examples, its
first necessary to briefly describe two mechanisms for parallelization
used by Dakota, message-passing and local. A comprehensive description
of parallelization in Dakota is available in the [Parallel Computing](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/advanced/parallelcomputing.html) section of the Dakota manual.

## Local Parallelism

In local parallelism, Dakota asynchronously runs multiple driver instances.
The [asynchronous](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/reference/interface-asynchronous.html)
interface keyword group is used to enable and control local parallelism.

Local parallelism is an easy way to take advantage of available computing
resources such as multiple CPU cores on a shared memory system such as a desktop,
laptop, or single node of an HPC.

Local parallelism has two important limitations compared to message-passing
parallelism. First, as the name suggests, Dakota can launch drivers only locally
using this mechanism, not across the network. Second, local parallelism takes advantage
of available concurrency only at the interface level. It cannot exploit additional
sources of concurrency in Dakota, such as concurrently running two optimizers in a
multi-start optimization.

## Message-Passing Parallelism

Message-passing parallelism is enabled by running Dakota with an MPI launcher such
as mpirun or srun. When Dakota is run in parallel, additional concurrency internal
to Dakota is exposed. For example, in an optimization-under-uncertainty (OUU) study, 
Dakota may be able to run multiple UQ studies at the same time. As with local
parallelism, parallel Dakota can run multiple driver instances concurrently.
Parallel Dakota can also be launched across multiple nodes of an HPC job.

Message-passing parallelism and local parallelism can be used together. For example, Dakota
can be MPI run with one task per node of an HPC job allocation, and local parallelism
then used to launch multiple driver instances on each node.

However, message-passing parallelism has a critical weakness. When Dakota is run
in parallel, the driver that Dakota runs cannot also use MPI to perform any work.
In other words, parallel Dakota cannot be used together with MPI parallelized simulations,
only serial ones.


## Dakota and HPCs

Because of the limitation just mentioned, often we are limited to using local parallelism
on HPCs. And because Dakota can use local parallelism to launch drivers only locally,
we need strategies to take advantage of mutiple nodes in an HPC job. This family of 
examples describes a few such approaches.

### Evaluation Submission

Outside of running Dakota in parallel with a serial simulation (so-called 'massively serial' operation), Evaluation submission is
perhaps the simplest way to use Dakota on an HPC. It makes the most
sense when the simulation under study is computationally expensive. In
evaluation submission, each evaluation is submitted as a separated job
to the HPC queue.

Dakota does not interact directly with the HPC queuing system. It is
the responsibility of the user to write a driver that manages job
submission and waiting for job completion.

### Tiling

Tiling means that multiple parallelized evaluations run concurrently within an HPC job. Suppose for example
that each evaluation requires running a simulation on 2 nodes. If the HPC job includes 20 total nodes, then
up to ten concurrent evaluations may be "tiled" across the available nodes.

Dakota is run serially as part of the job, and local parallelism is used to launch the concurrent driver
instances. All of the driver instances run on the same node, and it is up to the driver instances to 
manage the rest of the job's resources (other nodes, GPUs, etc).

Dakota's [batch interface](https://snl-dakota.github.io/docs/6.19.0/users/usingdakota/reference/interface-batch.html) 
can simplify management of resources in tiling. Unlike Dakota's ordinary interface,
which runs a separate instance of the driver for each evaluation, the batch interface writes all available
parameter sets (up to size) to a single parameters file and executes one driver instance. That driver
is responsible for performing all the evaluations in the file and returning a single results file.

### Batch Tiling

Batch tiling is similar to tiling in that multiple evaluations are tiled across the nodes of a larger
HPC job. The difference is, in batch tiling, Dakota runs outside of the HPC job. It uses its batch 
interface to run a single driver instance for multiple evaluations, and, just as with ordinary tiling,
the driver is responsible for tiling the evaluations within an HPC job.

Batch tiling can be useful in more complex studies such as MF/ML sampling that involve running a hierarchy
of simulations. With Dakota running on the login node, a single driver instance can "batch up" the least expensive simulations in a single submitted job and run the more expensive ones in their onwn jobs using the evaluation submission approach.

## Tools used in these Examples

[Slurm](https://slurm.schedmd.com/), a widely used workflow manager for HPCs, is used in the examples. They should
be easy to adapt to others such as PBS and SGE.

The underlying simulation that is run by Dakota is a modified version of the `text_book_par` test problem that
is built alongside parallel Dakota. The modified version reports diagnostic information to the console including
the hostname where each MPI task ran. Its cost has been artificially increased so that execution takes
additional time, and sleep of random duration up to 10 seconds has been added to simulate heterogenous computational
cost. The driver should be built from the source file in this folder
(`text_book_par.cpp`) with an MPI appropriate to your computing environment. On many systems, this is likely as simple as:

```
mpicxx text_book_par.cpp -o text_book_par
```

The examples also will work
with the `text_book_par` in Dakota's `share/dakota/test` folder.

The final and most important tool to mention is [Flux](http://flux-framework.org/). Flux, like Slurm, is a resource
manager for HPCs. Flux can be used alongside Slurm and has many features missing from Slurm that are helpful
for Dakota use. The interested reader is referred to the Flux documentation for a full details. A minimal
description is given here to clarify how it is used in the examples.


### Bare-bones Flux

The main reason for our interest in Flux is its ability to "subschedule" tasks within a Slurm job. In the 
Tiling section, we mentioned that it was the driver's responsibility to manage allocation of
computational resources. In the past, this may have required static scheduling and somewhat esoteric
features of specific MPI implementations such as machine files or relative node lists. Consistency between
the size of the HPC job, the resources needed by each driver instance, and Dakota's evaluation concurrency 
was demanded.

Flux simplifies and improves on these approaches. A Flux instance is launched on the nodes within a Slum job allocation,
and the Dakota driver submits work to it in a fashion similar to submitting a Slurm job. The Flux instance is aware of
the resources available in the job (number of CPU cores and GPUs), and it dynamically schedules work submitted to it
based on the resources demanded by each task.

## The Examples

Three examples are provided to demonstrate evaluation submission,
tiling, and batch tiling. Consult their respective READMEs for
a detailed explanation of how they work.
