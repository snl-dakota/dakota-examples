# Summary

Import a Python module into Dakota to use a decorated function it contains as a driver

# Description

This example combines use of the Dakota direct python callback interface
together with use of the `dakota.interfacing` Python module provided by
Dakota to transparently convert from the incoming Python dictionary to
Parameters and Response objects native to `dakota.interfacing`.  This is
done using an idiom supported in Python known as a decorator factory.
More specific details for both the direct python callback in Dakota and
the `dakota.interfacing` module can be found in the Python `linked` and `di`
examples.

# Driver

The main function of the direct Python callback driver `driver.py` is:

```python
@di.python_interface
def decorated_driver(params, results):

    textbook_input = pack_textbook_parameters(params, results)
    fns, grads, hessians = textbook_list(textbook_input)
    results = pack_dakota_results(fns, grads, hessians, results)

    return results
```

Prior to this snippet, the driver imports the `dakota.interfacing` module
as `di`, and the actual funxtion, gradient and hessian calculations are
brought in from the `textbook` module.

The Python decorator is invoked by using the Python convention of the
`@` followed by the name of the decorator function which in this case is
`di.python_interface()`.  This has the effect of passing the incoming
python dictionary of parameters and expected responses to the decorator
which internally converts this to `Parameters` and `Responses` objects
native to `dakota.interfacing`.  Two helper functions also in `driver.py`
extract parameter information suitable to the call to `textbook_list`
and subsequently pack the function, gradient and hessian values calculated
in that call into the `Responses` object.  The decorator then internally
extracts and returns to Dakota the needed python dictionary of results
required by the python direct interface.


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
* `driver.py`: Module containing the decorated callback function used by
   the Python direct interface together with helper functions for extracting
   and populating data with the `dakota.interfacing` `Parameters` and
  `Responses` objects, respectively.
* `textbook.py`: simulator for computing functions, gradients and hessians for
   parameter values

# Further reading

* The Textbook function is described in more detail in the 
  [Reference Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/textbook.html).
* More details of the Python linked interface can be found in the [Reference
  Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/interface-analysis_drivers-python.html)
  and in Section 16.3.2 of the [User's Manual](https://dakota.sandia.gov/content/manuals).
* Chapter 10 of the User's Manual provides a full description of interfacing in Dakota, including documentation 
  of the `dakota.interfacing` module.
