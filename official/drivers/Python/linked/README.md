# Summary

Import a Python module into Dakota to use a function it contains as a driver

# Description

When configured to use a `fork` or `system` interface, Dakota launches a driver
as a separate process (similar to a user launching an application at the command
line) and communicates with it using file I/O. Dakota also offers *linked* interfaces
to a few simulation tools, which allows direct communication through shared memory
with a driver.

Python is one such case. Dakota's `python` interface allows it to import Python
modules directly in order to use functions they contain as drivers. Dakota calls
the user-specified function and provides evaluation information as keyword arguments.
After computing the requested results, the function is required to return them in
a dictionary to Dakota.

One potential advantage to using Dakota's `python` interface is speed. Because
communication between Dakota and the driver occurs in-memory, file I/O is avoided.
Further, Dakota imports the module just once at the beginning of the study. Any
set up that can be shared or reused by all the evaluations can be performed at the module
level, where it will be executed one time upon import. This approach can be a powerful
way to avoid needless and costly rework.

The main downside of the `python` interface is that when using it Dakota cannot perform
evaluations asynchronously. That is, evaluations can be performed only one at a time.

Hence, the case for using the `python` interface may be strongest when the unqiue
computational work done by a driver for each evaluation is very small but depends on
significant set up that can be shared by all evaluations, such as building or reading
in a surrogate model or large lookup table for interpolation.

In this example, a simple optimization of the Textbook scalar function is performed
using the `python` interface. The optimization is performed to obtain the best values
for three continuous variables, each constrained by lower and upper bounds. After reading
the example, the user should understand how to configure Dakota to use the `python` interface,
and the basics of how to write a Python module for use with the interface.

A companion example that shows how to use the `dakota.interfacing` module that comes with
Dakota to write a forked Python driver is [also available](../di).

# Python driver module

The Python driver module featured in this example, `textbook.py`, includes callbacks to
evaluate function values, two nonlinear inequality values and gradients and hessians for each of these as requested
by Dakota.  The script has two candidate callback functions with the
first(`textbook_numpy`) using numpy arrays, and the second (`textbook_list`)
using native Python lists. The Dakota study in this example currently is configured to use the
latter.

Both Python functions receive keyword
arguments passed to it by Dakota in a dictionary named `kwargs`. These arguments include variable
values and other information needed to perform the evaluation. A complete list of arguments is available
in Table 16.1 of the Dakota User's Manual. In this example, two items in the dictionary are used.
The first, `cv`, is a Python list of the continuous variable values. The second, `asv`, is the
active set vector, which encodes the information (function value, gradient, hessian) that Dakota
requests for each response (objective and two nonlinear inequalities). See
Section 9.7 of the User's Manual for further description of the ASV.

After extracting variable values from `params`, the driver computes the requested
portions (function, gradient, hessian) of the responses based on the ASV. It packs the
results into a dictionary called `retval`. The function values are placed in a list and
associated with the key `fns`, and similarly for the  gradients (key `fnGrads`) and
hessians (key `fnHessians`). Figure 16.2 in the User's Manual shows the required and
permitted keys in this dictionary.

Finally, the function returns `retval` to Dakota.

# Dakota input

Our primary focus here is on the interface block.
```
interface,
        python
# the current analysis driver format is module:function
# use this for the list method of passing the data		
          analysis_driver = 'textbook:textbook_list'
# use this for the numpy array method of passing the data
#         analysis_drivers = 'textbook:textbook_numpy'
#           numpy
```

The primary things to note are:
* The interface type is `python`.
* The `analysis_drivers` specifies the name of the module (`textbook`) and function (`textbook_list`)
  that Dakota is to execute. They are delimited by a colon.


# How to run the example
 
 Make sure the Python used to build Dakota is in the environment PATH and
 that the PYTHONPATH includes the directory containing the textbook.py
 driver script.

Run Dakota

    $ dakota -i dakota_textbook_python.in
 
# Requirements

Dakota built with Python support. The downloads available on the Dakota website come with Python enabled.
The major.minor version of Python (e.g. 2.7, 3.8) in your environment must match the one included with Dakota.
The version that comes with Dakota can be checked by examining the contents of the bin folder, which contains a
versioned Python library. We recommend setting up a conda or virtual environment to use with Dakota in order to
satisfy the version requirements.

# Contents

* `dakota_textbook_python.in`: Dakota input file
* `textbook.py`: Combined simulator and analysis driver

# Further reading

* The Textbook function is described in more detail in the 
  [Reference Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/textbook.html).
* More details of the Python linked interface can be found in the [Reference
  Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/interface-analysis_drivers-python.html)
  and in Section 16.3.2 of the [User's Manual](https://dakota.sandia.gov/content/manuals).
 
