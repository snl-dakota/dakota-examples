#!/bin/bash
export OMP_NUM_THREADS=1
#Runs windse using single_turbine.yaml
cd ./run_$1
windse run single_turbine.yaml
cd ..
