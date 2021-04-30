# Summary

Perform an optimization study using the C-API python linked interface
for the problem driver

# Description

A simple optimization of the Rosenbrock scalar function is performed
using a linked Python interface compiled into Dakota.  The optimization
is performed to obtain the best values for two continuous variables,
each constrained by lower and upper bounds.  The python interface script
supports callbacks to evaluate functions, gradients and hessians requested
by Dakota.  The script has two candidate callback functions with the
first using native Python lists, and the second using numpy arrays.
Only the former is currently used and is specified in the `interface`
block in the Dakota input file using the `python` keyword together with
specification of a string value in the form ``module:function'' for the
arguemnet to the `analysis_drivers` input.

# Optimization Problem

The Rosenbrock optimization problem seeks to minimize the function
$`f(x_1,x_2)`$ with lower and upper bounds applied to both $`x_1`$
and $`x_2`$, eg
```math
f_0 = x_2-x_1^2
f_1 = 1-x_1

f(x_1,x_2)=100 f_0^2+f_1^2
-2.0 < x_1 < 2.0
-2.0 < x_2 < 2.0
```

# Analysis Driver

The analysis driver for this study is the script
`rosenbrock.py` which is described in more detail in the [Reference
Manual](https://dakota.sandia.gov//sites/default/files/docs/6.13/html-ref/rosenbrock.html).
Dakota calls the function specified in the Daktoa interface specification
and passes a python dictionary containing variable values and an ``active
set'' value indicating which values Dakota expects to be computed and
returned by the python script.  There are several more entries in the
python dictionary which are not used in the example.

More details of the Python linked interface can be found in the [Reference
Manual](https://dakota.sandia.gov//sites/default/files/docs/6.13/html-ref/interface-analysis_drivers-python.html)
and in Section 16.3.2 of the [User
Manual](https://dakota.sandia.gov/sites/default/files/docs/6.13/Users-6.13.0.pdf).

# How to run the example
 
 Make sure the Python used to build Dakota is in the environment PATH and
 that the PYTHONPATH includes the directory containing the rosenbrock.py
 driver script.

Run Dakota

    $ dakota -i dakota_rosenbrock_python.in -o dakota_rosenbrock_python.out
 
# Requirements

Python 2 or 3

# Contents

* `dakota_rosenbrock_python.in`: Dakota input file
* `rosenbrock.py`: Combined simulator and analysis driver

# Study Results 
## Screen Output

Dakota produces output similar to the following to the screen (redirected to 
`dakota_rosenbrock_python.out`).

~~~~
<<<<< Best parameters          =
                      9.9972719897e-01 x1
                      9.9941343413e-01 x2
<<<<< Best objective function  =
                      2.4283400701e-07
<<<<< Best data captured at function evaluation 73
~~~~

Dakota reports several pieces of information, including

* The best parameters (those that minimize the objective function and respect the bounds constraints)
* The best objective function value
* The evaluation ID of the best parameters/function
 
