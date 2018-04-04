# Wait for Slurm

This is a simple tool that can be used in a driver script to wait for a slurm submission to run.

For example, inside a of a bash script that submits a job to slurm, 

```bash
# Set up all of the runs
# ...

# Submit run to queue
sbatch submit_script.sh | python wait_for_job.py

```

And it will block until the job finishes.


## Command Line Help

```
usage: wait_for_slurm.py [-h] [--init-time T] [-p T] [job_id]

Tool to wait for a SLURM job to finish by polling the queue.

Usage:

    $ python wait_for_job.py 447787
    $ sbatch submit_script.sh | python wait_for_job.py

positional arguments:
  job_id          ["-"] The SLURM id of the job. Will also remove any non-
                  numeric characters. Useful for piping input. "-" means stdin

optional arguments:
  -h, --help      show this help message and exit
  --init-time T   [5.0] seconds *before* starting to look for the job in the
                  queue
  -p T, --poll T  [3.5] seconds between polling the queue for the job
```
