# Summary

Dakota studies applied to mechanical analysis of a cylindrical tank

# Description

Version 1; 06 January, 2013

Dakota examples illustrating studies that might be useful in an
engineering analysis. The examples run a model of a cylindrical tank,
which simulates displacement, strain, and stress responses to load.

The cylindrical tank model `tank_model/` used in these studies
corresponds to that in the 2014 V&V Challenge Workshop at the ASME V&V
Symposium.

This content migrated from top-level Dakota Git repo at
`fd500c77fc94fe3dceab864e1f7235820386a321`

# Requirements

This was originally intended to run in a Linux environment and python
2 or 3.  It has been tested w/ Dakota 5.4 and python 2.6.6 and 3.3.2,
on RHEL 6.  Some of the driver scripts are written in bash, and no
Windows equivalent is provided.  However, the python driver scripts
have also been tested on Windows 7, Dakota 5.4, and Python 3.3.3.
Although this was not tested on Mac systems, it is assumed that the
tank model will run with default installations of python, and the
Dakota examples will run under Dakota 5.4.

# Contents 

Usage information for each Dakota example is included in the Dakota
input file.

`DakotaList/`: Two list parameter studies

A list parameter study is good for manual exploration of parameter
space.  This illustrates the most basic method, plus: use of Dakota
with a driver script that calls a setup script (`EvalTank.py`) which
then runs the physics code (`FEMTank.py`) selecting which variables
are active concurrent function evaluations, with file_tag Different
results from the simulation (controlled by the input variable
resultStyle) and the necessary changes in the Dakota responses block

`DakotaLHS/`: An LHS study

Latin Hypercube Sampling can be used for sensitivity analysis,
uncertainty quantification, or surrogate building.  This illustrates:
use of Dakota where the driver script runs the physics code an
uncertainty quantification method use of uncertain variables

`DakotaCalibration/`: Least-squares calibration to minimize residuals

Parameter calibration is used to match model responses to observed
data.  This illustrates: A calibration method How Dakota uses
datafiles A complicated driver script that makes multiple calls to the
setup script (`EvalTank.py`) in order calibrate to data from multiple
experiments How to use Dakota to optimize some inputs, while others
are constant (state variables), and another is modified within the
driver script (Pressure)

`tank_model`: Python mechanical analysis of the loaded cylindrical
tank (see its README)

`VVTankProblem.zip`: Full package of this example, including the data
from the V&V challenge workshop.