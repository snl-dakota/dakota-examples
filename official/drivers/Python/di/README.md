# Summary

Use the dakota.interfacing Python module to write an analysis driver

# Description

The Python programming language offers several advantages for developing analysis drivers,
such as its portability and widespread use. The motivation for using Python may be greatest
when the simulation that the driver will run is itself written in Python or has a Python API.

Dakota includes a Python module, `dakota.interfacing`, to aid developement of black-box drivers
in Python. It hides many of the details of reading Dakota parameters files and writing Dakota results
files and provides convenient key- and index-based access to variables and responses.

This example demonstrates basic use of `dakota.interfacing` in a driver that runs a simulation which
also is written in Python. It is assumed that the user has a good understanding of Dakota input
`interface` keywords and of the way Dakota runs and communicates with drivers. A more detailed 
introduction to the interfacing task may be found in the [bash](../bash/) and
[windows_bat](../windows_bat/) examples. Chapter 10 of the User's  Manual describes
interfacing in depth. It also contains detailed documentation of the `dakota.interfacing` module.

A [companion example](../linked) is available that demonstrates how to directly import a Python module
into Dakota.

# Driver

The main function of the driver `rosenbrock_bb.py` is:

```python
params, results = di.read_parameters_file()
rosen_input = pack_rosen_parameters(params, results)

rosen_output = rosenbrock_list(**rosen_input)
    
results = pack_dakota_results(rosen_output, results)
results.write()
```

Prior to this snippet, the driver imports the `dakota.interfacing` module as `di`.

The `read_parameters_file()` function takes the names of the Dakota parameters and results files
from the command line arguments, reads and parses the parameters file, and constructs `Parameters`
and `Results` objects. These objects contain information such as variable values and the active set
vector for the responses.

The `pack_rosen_parameters()` function is a helper that uses information from the `Parameters` and
`Results` objects to construct the input data structure for the `rosenbrock_list()` simulator. Examine
this function to learn one way of accessing variable values stored in the `Parameters` object. Chapter
10 of the Dakota User's manual describes other functionality.

After calling `rosenbrock_list()` on the packaged input, the dictionary it returns is passed to
`pack_dakota_results()`. This function extracts output and inserts it into the Dakota `Results` object.

Finally, `results.write()` is called to write the Dakota results file.


# How to run the example

On Linux or OS X, run Dakota in the `Python` folder:

`dakota dakota_rosenbrock_python.in`

On Windows, it is necessary first to modify the `analysis_driver` string in `dakota_rosenbrock_python.in as
directed by the comments there.

# Requirements

Python

# Contents

* `dakota_rosenbrock_python.in`: Dakota input file
* `rosenbrock_bb.py`: Driver
* `rosenbrock.py`:  Python module that implements the Rosenbrock test problem (Section 20.2 of the User's Manual)

# Further Reading

* Chapter 10 of the User's Manual provides a full description of interfacing in Dakota, including documentation 
  of the `dakota.interfacing` module.
* The `interface` keyword documentation in the [Reference Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/interface.html)
  contains detailed descriptions and more examples.

