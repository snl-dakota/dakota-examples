#!/bin/bash

module purge
module load dakota

flux run -N 1 -x dakota -input dakota_sampling.in


