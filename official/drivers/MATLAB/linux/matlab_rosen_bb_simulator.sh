#!/bin/bash

# Parameters and results filenames
params=$1
results=$2

# Assuming Matlab .m files and any necessary data are in ./
# from which Dakota is run.

matlab -batch "matlab_rosen_wrapper('${params}', '${results}'); exit"

