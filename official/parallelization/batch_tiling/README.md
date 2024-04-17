# Summary

Use batch tiling to run a study on an HPC

# Description

If you aren't familiar with ordinary tiling, it may be helpful
to first read the tiling example, which is peer to this one. Batch
tiling is similar to tiling, in that evaluations are tiled across
available resources within an HPC job. The main difference between
the two is that in batch tiling, Dakota runs outside of the HPC job,
typically on the login node, and a specially designed driver submits
batches of evaluations to the queue. To simplify the submission of
batches, Dakota's [batch](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/reference/interface-batch.html)
interface is used.

The main benefit of the batch interface and of the batch tiling
approach is that it grants the user finer grained control over
how evaluations are run. For instance, in a multilevel sampling
study, the same Dakota interface may be used to run evaluations with
greatly different computational demands. The batch interface simplifies
packaging up the least expensive evaluations to be run in one job using
a batch tiling approach while running more costly ones using an
evaluation submission approach.

As in the ordinary tiling example, batch tiling uses Flux to schedule
evaluations to run within the HPC job. Flux manages computational tasks
and the CPU cores (and GPUs) available in the job to ensure that efficient
use is made of computational resources.

# Approach

We will step through the moving parts of the workflow, explaining them
as we go.

## Run Dakota

The `run_dakota.sh` script is simple. It sets up the environment for
Dakota by loading the dakota module and also exports a pair of environment
variables that may be needed by Flux on your system. It then runs Dakota 
using the `dakota_sampling.in` input file.

A couple of things are noteworthy about `dakota_sampling.in`. The first
is the `batch` keyword in the interface section, which turns on Dakota's
batch interface.

The second is the analysis driver string, which is more complex
than in most Dakota input files.

```
srun --account=XXXXX --time=00:03:00 --partition=short,batch -N2 -n 2 --pty flux start python3 ../batch_driver.py
```

In plain language, this command uses `srun` to launch a Flux instance on 2 nodes,
and provides Flux with an initial command, the batch-aware driver, which is written
in Python. As usual, Dakota will append the names of the parameters and results files
when it runs the command.

When `srun` is used outside of a job, it behaves similarly to `sbatch --wait`. It
submits a job request to Slurm. When the job runs, the supplied command (`python3 ...`)
is run. `srun` blocks until the job completes.

As we will see in the following section, the batch driver uses Flux's Python
API to run all of the individual evaluations in the batch.

## The Batch Driver

The batch driver in this example is more complicated than a typical driver, both
because it is responsible for completing a batch of evaluations instead of a single
one and because it uses Flux's asynchronous API, which uses concepts that
may be unfamiliar to some. We'll step through and discuss some of the more noteworthy
parts of the script.

### Splitting the batch

The simulation that will be run, `text_book_par`, expects a single Dakota parameters file and
writes a single Dakota results file. Dakota, in batch mode, concatenates parameter sets for
all evaluations in the batch in a batch parameters file, and expects all results for the batch
in a concatenated batch results file. 

Roughly the first half of the `main()` function is responsible for splitting the batch parameters
file into individual parameters sets and writing them into work directories. A class
in the `dakota.interfacing` Python module (imported as `di`) called `BatchSplitter` assists
with this task.

A `BatchSplitter` instance is constructed using the name of the batch parameters file.

``` python
splitter = di.BatchSplitter(batch_params_file)
 ```

 `splitter` is iterated to obtain parameter sets, which are yielded as lists of strings,
 so that they can be written to parameters files in work directories:

 ``` python
eval_workdir_map = {}
for i, params in enumerate(splitter):
    eval_num = splitter.eval_nums[i]
    eval_workdir_map[eval_num] = create_workdir(workdir_base, eval_num)
    write_parameters_file(eval_workdir_map[eval_num] / parameters_file, params)
 ```

 A map (`eval_workdir_map`) from the evaluation number to the name of that evaluation's work directory
 is built up for later use.

### Submitting evaluations to Flux

The next section of `main()` is responsible for submitting the individual evaluations
 to Flux using Flux's asynchrous API and awaiting their completion using Python's 
 built-in `concurrent.futures` module. While a full discussion of asynchronous execution
 is beyond the scope of this example, it may be worthwhile for the reader to consult the
  [Python docs](https://docs.python.org/3/library/concurrent.futures.html#module-concurrent.futures)
 for this package or some other tutorial or examples to obtain a deeper understanding of the concepts.

 At a high level, `FluxExecutor()` provides a context manager that is responsible for scheduling and
 performing work asynchronously using Flux. Work is scheduled using the `submit()` method on the
 `executor` object. The call to `submit()` is nonblocking and returns an object of class
 [Future](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future). A
 `Future` can be queried for completion of the task, and the result of the task can also be obtained
 from the `Future` when it is complete. the code below builds up a dictionary that maps `Future`s to
 evaluation numbers.

``` python
    failed = set()
    with FluxExecutor() as executor:
        futures = {
                executor.submit(create_job_spec(workdir, parameters_file, results_file)): eval_num 
                for eval_num, workdir in eval_workdir_map.items()
                }
```

 The `submit()` method accepts a Flux [Jobspec](https://flux-framework.readthedocs.io/projects/flux-core/en/latest/python/autogenerated/flux.job.Jobspec.html#flux.job.Jobspec.Jobspec) object, which is returned by the `create_job_spec()` function:

 ``` python
 def create_job_spec(workdir: pathlib.Path, parameters_file: str , results_file: str) -> JobspecV1:
    """Create a Flux jobspec that can be used by Flux's asynch API"""
    # from_command creates a job spec from a command and set of resource requirements
    jobspec = JobspecV1.from_command(
            command=["text_book_par", parameters_file, results_file],
            num_tasks=8
        )
    # A few other attributes must be set explicitly (they aren't constructor arguments)
    jobspec.cwd = str(workdir)
    jobspec.environment = dict(os.environ)
    jobspec.stdout = "stdout.txt"
    jobspec.stderr = "stderr.txt"
    return jobspec
 ```

This function just uses the Flux function `JobspecV1.from_command()` to create a jobspec from
the command that we wish to run. You can see that in addition to constructing the jobspec
object, the function configures it by modifying a few of its attributes. Most importantly, its current working directory must be set to the work directory where `text_book_par` should be run.


After all the evaluations have been submitted to Flux, the driver must await their completion. The driver passes the dictionary of futures to the built-in Python function [concurrent.futures.as_completed()](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.as_completed), which yields
futures as they complete.

The driver checks whether any exception occured while the task represented by the future ran. If so, the associated evaluation number is stored to the `failed` set.

``` python
    for future in concurrent.futures.as_completed(futures):
        if future.exception():
            eval_num = futures[future]
            print(f"Eval {eval_num} raised exception {future.exception()}", file=sys.stderr)
            failed.add(eval_num)
```

### Colllecting the results

The individual results files written by `text_book_par` for each evaluation must be concatenated
into a Dakota-format batch results file. The individual results sets are separated by a `#` sign.

This occurs in the final portion of `main()`.

``` python
    with open(batch_results_file, "w") as f:
        for eval_num, workdir in eval_workdir_map.items():
            if eval_num in failed:
                f.write("FAIL\n")
            else:
                eval_result = read_eval_result(workdir / results_file)
                f.write(eval_result)
            f.write("#\n")
```

Note that for failed evaluations, the driver writes the string "FAIL" for the results, which triggers
Dakota's failure capturing mechanism.

# How to run the example

Build `text_book_par.cpp` (source in the folder above) using an MPI compiler and place the
executable alonside the Dakota input and scripts.

Then, run:

```
dakota dakota_sampling.in
```

It may be necessary to provide an account number or to modify the requested partition for your HPC
in the analysis driver string in dakota_sampling.in.

Running the example will produce output from the study in the slurm console output. In addition,
output from each simulation will be written to files named `stdout.txt` and `stderr.txt` in the
work directory for each evaluation.
