#!/bin/bash

#sed script to write values into single_turbine.yaml
#$1 = case_nb
#$2 = max_vel
#$3 = power
#$4 = wind_angle
#$5 = lmax
#$6 = grid_refine
#$7 = grid_x
#$8 = grid_y
#$9 = grid_z

cd ./run_$1
#echo $1 $2 $3 $4 $5 $6
sed "s/#HH_vel_sed/$2/1" single_turbine.yaml > single_turbine_output.yaml
mv single_turbine_output.yaml single_turbine.yaml 
sed "s/#power_sed/$3/1" single_turbine.yaml > single_turbine_output.yaml
mv single_turbine_output.yaml single_turbine.yaml 
sed "s/#init_wind_angle_sed/$4/1" single_turbine.yaml > single_turbine_output.yaml
mv single_turbine_output.yaml single_turbine.yaml 
sed "s/#final_wind_angle_sed/$4/1" single_turbine.yaml > single_turbine_output.yaml
mv single_turbine_output.yaml single_turbine.yaml
sed "s/#lmax_sed/$5/1" single_turbine.yaml > single_turbine_output.yaml
mv single_turbine_output.yaml single_turbine.yaml
sed "s/#grid_refine_sed/$6/1" single_turbine.yaml > single_turbine_output.yaml
mv single_turbine_output.yaml single_turbine.yaml
sed "s/#grid_x_sed/$7/1" single_turbine.yaml > single_turbine_output.yaml
mv single_turbine_output.yaml single_turbine.yaml
sed "s/#grid_y_sed/$8/1" single_turbine.yaml > single_turbine_output.yaml
mv single_turbine_output.yaml single_turbine.yaml
sed "s/#grid_z_sed/$9/1" single_turbine.yaml > single_turbine_output.yaml
mv single_turbine_output.yaml single_turbine.yaml
cd ..
