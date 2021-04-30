# Summary

Interface Dakota to a MATLAB simulation on Windows

# Description

Many valuable computational simulations are written in MATLAB. Although interfacing Dakota to a
MATLAB simulation on Windows often is straightforward, the precise details depend on how
the simulation must be run and other specifics. The driver's responsibilities for preprocessing,
execution, and postprocessing may be shared between custom MATLAB and higher-level
scripting in other languages as dictated by need and convenience. In addition, the Windows version of
MATLAB features the [MATLAB Automation Server]( `https://www.mathworks.com/help/matlab/matlab_external/creating-the-server-manually.html),
which can greatly reduce the overall time taken by a
Dakota study by largely eliminiating the overheard of repeatedly starting up MATLAB.

This example contains a Dakota study and driver that executes a MATLAB function. The top-level driver
(`matlab_rosen_bb_simulator.vbs`) is a Visual Basic script. It communicates with the MATLAB Automation Server,
which the user has launched on her own system, to execute a purpose-written MATLAB wrapper function. The
wrapper (`matlab_rosen_wrapper.m`) reads variable values from the Dakota parameters file, passes them
into the simulation (`rosenbrock.m`), and writes the results to the Dakota results file.

It is assumed that the user has a good understanding of Dakota input
interface keywords and of the way Dakota runs and communicates with drivers. A more detailed
introduction to the interfacing task may be found in the [bash](../../bash/) and
[windows_bat](../../windows_bat/) peer examples.
Chapter 10 of the User's Manual describes interfacing in depth.


# Things to notice

* Use of the MATLAB Automation Server adds a layer of complexity to the driver but avoids the overhead
  of starting a new MATLAB process for each evaluation. As a result, Dakota studies complete much more rapidly.
* The wrapper function `matlab_rosen_wrapper.m` parses the Dakota parameters file. An
  alternative approach that avoids MATLAB's somewhat unwieldy file I/O and string processing functions
  might be to use `dprepro` to configure a templated Matlab wrapper.
* The Dakota input file does not use `asynchronous` evaluation. In our experience, MATLAB does not support
  multiple, concurrent executions.
* In the Dakota input file, the `analysis_driver` string shows that the Windows built-in `cscript` utility is used
  to execute the driver script. In some corporate environments, use of `cscript` is restricted. If cybersecurity won't
  budge, you can forego use of the MATLAB Automation Server and adopt an approach similar to the one illustrated
  in the `linux` peer example.

# How to run the example

1. Start the MATLAB Automation Server in a CMD terminal: `matlab -automation`
2. Run Dakota: `dakota -i dakota_matlab_rosenbrock.in`
	
# Requirements

MATLAB; Windows

# Contents

* `dakota_matlab_rosenbrock.in`: Dakota input file
* `matlab_rosen_bb_simulator.vbs`: Top-level driver script run by Dakota
* `matlab_rosen_wrapper.m`: Purpose-written wrapper function that handles preprocessing, execution, and postprocessing
* `rosenbrock.m`: Simuator

# Futher Reading

MATLAB's documentation for interacting with a [MATLAB COM server](https://www.mathworks.com/help/matlab/call-matlab-com-automation-server.html).
