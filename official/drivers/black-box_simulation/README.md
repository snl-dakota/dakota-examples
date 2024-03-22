# Summary

This is an example that demonstrates how to connect a black-box code to Dakota using a driver script. It demonstrates the use of Dakota's built-in preprocessing tool `dprepro` to insert parameter values into a template input file for use with the black-box code.

# Description

By black-box code, we mean a code that takes an input file that specifies the simulation to be run. Black box codes are typically run from the command line with an input file passed as an argument to an executable, e.g., `blackboxsimulation inputfile.in`. In this case, a driver script must substitute parameter values into a template input file, execute the black-box code, and postprocess the black-box code's output files to extract response values.

The black-box simulation model used in this example is a *cantilever beam*, which can be thought of as a rigid structural element that extends horizontally and is supported at only one end.

The simulation model accepts seven input parameters:

 - the length of the beam, **L**
 - the width of the beam, **w**
 - the thickness of the beam, **t**
 - Young's modulus, **E**
 - the density of the beam, **p**
 - the horizontal load on the beam, **X**
 - the vertical load on the beam, **Y**

The simulation model produces three output responses:

 - the **mass** of the beam
 - the **stress** on the beam
 - the **displacement** of the beam

This problem demonstrates a very common use-case for Dakota studies, in that we have a black-box code where parameter samples must be substituted into an input file that is used to run the simulation. We also have to postprocess the black-box code's output files to extract responses to return to Dakota.

# Description of analysis driver

Dakota does not know how to set up, run, or get output from a user's simulation.  That responsibility belongs to the *analysis driver,* which carries out those tasks on Dakota's behalf. In a typical study, Dakota runs the analysis driver one time for each evaluation, which is a mapping from a single point in input/parameter space to a corresponding point in response/output space.  The driver has three main responsibilities.

1. **Preprocessing:** Dakota provides parameter values to the driver by writing them to a parameters file.  It communicates the name of the parameters file as the first command line argument of the driver. In the preprocessing phase, the driver uses values it reads from the parameters file to construct valid input for the simulation.

2. **Execution:** The driver runs the user's simulation.

3. **Postprocessing:** In this phase, the driver extracts response information from simulation output and writes it to a correctly formatted Dakota results file. Dakota provides the name of the results file as the second command line argument to the driver.

Because Dakota does not directly interpret the driver and relies on the operating system and other tools on the user's system to execute it, the driver can be written in any programming language.  This example demonstrates Python- and Bash-based driver scripts.

# Contents

- `cantilever` - the black-box simulation model representing the cantilever beam.  In reality, this is a Python script with the extension removed and made executable so that it can be invoked from the command-line as `./cantilever <input file>`, where `<input file>` is the input data file for the simulation.
- `cantilever.template` - the template input file for the cantilever beam.  Note the presence of curly braces in the text of this file.  This file is primarily used in the **pre-processing** step of analysis driver logic.
- `dakota_cantilever_center.in` - the Dakota study, which uses the `centered_parameter_study` method to study the cantilever beam model.
- `DakotaDriver.py` - the Python analysis driver for the Dakota study.  This Python script is responsible for transferring information between Dakota and the cantilever beam model. *Note that the driver script must be made executable for it to function as a Driver script for Dakota*

# How to run the example

## Prerequisites (IMPORTANT!)

- This example is written for Linux/Mac OS. There is a separate Windows version of the example in `official/drivers/black-box_simulation_windows`.
- This analysis driver will *only* work if Dakota's Python interfacing libraries are available on the **PYTHONPATH** environment variable. OS-specific instructions for setting this variable are provided [here](https://snl-dakota.github.io/docs/latest_release/users/setupdakota.html#setting-your-environment).
- The driver and cantilever scripts require Python 3.


## Run on command line

    $ dakota dakota_cantilever_center.in
