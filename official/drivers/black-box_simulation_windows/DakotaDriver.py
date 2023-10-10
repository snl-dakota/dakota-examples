#!/usr/bin/env python3

#############
#  Imports  #
#############

# Common imports
import subprocess, csv
import dakota.interfacing as di

###################
#  Preprocessing  #
###################

# Get the Dakota Parameters and Response objects.
params, results = di.read_parameters_file()

# Substitute the parameter values into the templatized
# input file, outputting a valid input file for the 
# black-box code.
di.dprepro(template='cantilever.template', 
           parameters=params, 
           output='cantilever.in')

##################################
#  Running black-box simulation  #
##################################

subprocess.run('python cantilever cantilever.in'.split())

####################
#  Postprocessing  #
####################

# Importing results from output CSV file

# Uses Python's built-in csv DictReader capability, which returns
# an iterable with each row of the CSV saved as a dictionary with 
# keys being the column names of the CSV and values being the data 
# in each row. The __next__() command returns the next row in the 
# CSV file. Since we have only one row of data, it returns a dictionary
# of the response values from the model.
blackbox_outputs = csv.DictReader( open('black-box_results.csv') ).__next__() 

# Writing results to Dakota-formatted results file using the Response object.
results['mass'].function = blackbox_outputs['mass [lb]']
results['stress'].function = blackbox_outputs['stress [lb/in^2]']
results['displacement'].function = blackbox_outputs['displacement [in]']
results.write()