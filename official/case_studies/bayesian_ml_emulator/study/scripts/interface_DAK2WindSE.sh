#!/bin/bash

#bash script connecting to Python script
#$1: params.in.i
#$2: results.out.i
#i: current run/case number
python python_DAK2WindSE.py -p $1 -r $2
