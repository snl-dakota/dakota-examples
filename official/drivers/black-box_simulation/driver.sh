#!/bin/bash

# $1 and $2 are special variables in bash that contain the 1st and 2nd 
# command line arguments to the script, which are the names of the
# Dakota parameters and results files, respectively.

params=$1
results=$2

############################################################################### 
##
## Pre-processing Phase -- Generate/configure an input file for your simulation 
##  by substiting in parameter values from the Dakota paramters file.
##
###############################################################################

dprepro $params cantilever.template cantilever.in

############################################################################### 
##
## Execution Phase -- Run your simulation
##
###############################################################################


./cantilever cantilever.in > cantilever.log

############################################################################### 
##
## Post-processing Phase -- Extract (or calculate) quantities of interest
##  from your simulation's output and write them to a properly-formatted
##  Dakota results file.
##
###############################################################################

mass=$(tail -1 black-box_results.csv | cut -f 1 -d ,)
stress=$(tail -1 black-box_results.csv | cut -f 2 -d ,)
displacement=$(tail -1 black-box_results.csv | cut -f 3 -d ,)

echo "$mass mass" > $results
echo "$stress stress" >> $results
echo "$displacement displacement" >> $results