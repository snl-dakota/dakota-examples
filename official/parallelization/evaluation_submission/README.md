# Summary

Submit individual evaluations to an HPC queue

# Description

In the evaluation submission approach, each Dakota evaluation is
submitted to an HPC queue as a separate job. It makes the most
sense to use this approach when the simulation under study is
computationally expensive. This example shows how to set up
an evaluation submission workflow using Slurm. If your HPC uses
a different resource manager, it should be straightforward to adapt.

Compared to tiling and batch tiling, evaluation submission is simple.
There are a few things to note about evaluation submission.

* Dakota typically is run on the login node of the HPC.
* In the Dakota input file, `dakota_sampling.in`, the
  [asynchronous](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/reference/interface-asynchronous.html)
  keyword is used to cause Dakota to run multiple driver instances
  concurrently. The [evaluation_concurrency](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/reference/interface-asynchronous-evaluation_concurrency.html)
  keyword can be used
  as a throttle if your HPC limits the number of active job submissions.
* As with any `asynchronous` study, because Dakota runs multiple driver
  instances simultaneously, filesystem conflicts between the evaluations
  must be avoided. This study uses tagged
  [work directories](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/reference/interface-analysis_drivers-fork-work_directory.html).
* The driver script is responsible for submitting the
  job and waiting for it to complete. In this example, `run_textbook.sh`
  uses the [srun](https://slurm.schedmd.com/srun.html) command to
  submit perform the submission. Equivalently,
  [sbatch --wait](https://slurm.schedmd.com/sbatch.html#OPT_wait)
  could be used. On HPCs that do not have a queue submission
  command that can be configured to block, the driver must determine when
  the job has completed some other way, such as by polling the resource
  manager.

# How to run the example

Edit the driver `run_textbook.sh` to change the account and partition
information in the `srun` command to values approrpriate for your system.

Next, if you have not already done so, build `text_book_par` from source
using an MPI-aware C++ compiler.

Finally, set up the environment to run Dakota and run:

```
dakota dakota_sampling.in
```

Five random samples will be run as part of the study. As Dakota executes,
it will launch evaluations for the samples concurrently. Each driver
instance will submit a job to Slurm, wait for it to complete, and exit.
Once all five samples are complete, Dakota will compute and report summary statistics and exit.
