# Summary

Interface Dakota to a MATLAB simulation on Linux/OS X

# Description

Many valuable computational simulations are written in MATLAB. Although interfacing Dakota to a
MATLAB simulation on Linux or OS X often is straightforward, the precise details depend on how
the simulation must be run and other specifics. The driver's responsibilities for preprocessing,
execution, and postprocessing may be shared between custom MATLAB and higher-level
scripting in other languages as dictated by need and convenience.

This example contains a Dakota study and driver that executes a MATLAB function. The top-level driver
(`matlab_rosen_bb_simulator.sh`) is a Bash script. Its only task is launching MATLAB in
"batch" mode (no GUI, no user interaction) to execute a purpose-written MATLAB wrapper function. The
wrapper (`matlab_rosen_wrapper.m`) reads variable values from the Dakota parameters file, passes them
into the simulation (`rosenbrock.m`), and writes the results to the Dakota results file.

It is assumed that the user has a good understanding of Dakota input
interface keywords and of the way Dakota runs and communicates with drivers. A more detailed
introduction to the interfacing task may be found in the [bash](../../bash/) and 
[windows_bat](../../windows_bat/) examples. Chapter 10 of the User's  Manual describes
interfacing in depth.


# Things to notice

* The `-batch` command line option to MATLAB in `matlab_rosen_bb_simulator.sh`. This option causes
   MATLAB to execute the command that follows without opening the GUI or entering interactive mode.
* The wrapper function `matlab_rosen_wrapper.m` parses the Dakota parameters file. An
  alternative approach that avoids MATLAB's somewhat unwieldy file I/O and string processing functions
  might be to use `dprepro` to configure a templated Matlab wrapper.
* The Dakota input file does not use `asynchronous` evaluation. In our experience, MATLAB does not support
  multiple, concurrent executions.
* Due to the overheard of restarting MATLAB for each evaluation, even studies on simulations that run quite quickly
  will be slow. On Windows, studies can take advantage of the MATLAB Automation Server to speed things up considerably.
  Users may also want to consider performing Dakota evaluations in batch (Section 10.6 of the User's Manual).

# How to run the example

Make sure that MATLAB is on your PATH, then:

`dakota -i dakota_matlab_rosenbrock.in`
	
# Requirements

MATLAB; Linux or OS X.

# Contents

* `dakota_matlab_rosenbrock.in`: Dakota input file
* `matlab_rosen_bb_simulator.sh`: Top-level driver script run by Dakota
* `matlab_rosen_wrapper.m`: Purpose-written wrapper function that handles preprocessing, execution, and postprocessing
* `rosenbrock.m`: Simuator

