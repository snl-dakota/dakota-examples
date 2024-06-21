#!/bin/bash

module purge
module load dakota

rm -rf workdir

export FLUX_QMANAGER_OPTIONS="queue-policy=easy"
export PSM2_DEVICES="self,shm,hfi"

dakota -input dakota_sampling.in 2>&1 | tee dakota_sampling.log

## On some systems, the study leaves the terminal in a bad state after
## exiting (commands aren't echoed, prompt is preceded by lots of space, etc).
## Uncomment the reset command to fix it.

# reset
