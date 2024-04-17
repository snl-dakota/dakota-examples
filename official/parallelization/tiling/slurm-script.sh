#!/bin/bash
#SBATCH --nodes=3
#SBATCH --job-name=dakota_tiling_example
#SBATCH --time=00:05:00
#SBATCH --partition=short,batch


export FLUX_QMANAGER_OPTIONS="queue-policy=easy"
export PSM2_DEVICES="self,shm,hfi"

# Start one Flux daemon per node, interactive session on first compute node

srun -N 3 -n 3 --mpi=none flux start ./run_dakota.sh

