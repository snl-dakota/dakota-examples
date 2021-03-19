#!/bin/bash

#just remove some unnecessary data here to save disk space
cd ./run_$1
rm -r ./output/single_turbine/functions
rm -r ./output/single_turbine/log.txt
rm -r ./output/single_turbine/mesh
rm -r ./output/single_turbine/plots
#rm ./output/single_turbine/solutions/*.vtu
cd ..
