#!/bin/bash

module purge
module load dakota

rm -rf workdir

export FLUX_QMANAGER_OPTIONS="queue-policy=easy"
export PSM2_DEVICES="self,shm,hfi"

dakota -input dakota_sampling.in 2>&1 | tee dakota_sampling.log

