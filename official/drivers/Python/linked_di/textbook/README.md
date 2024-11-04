# Summary

Use Parameters and Results objects from dakota.interfacing with Dakota's direct Python interface

# Description

This example combines use of the Dakota direct `python` callback interface
with use of the `dakota.interfacing` Python module to transparently convert
the incoming Python dictionary to Parameters and Results objects defined in
`dakota.interfacing`.  This is accomplished using a decorator.
More specific details for both the direct Python callback in Dakota and
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
as `di`, and the actual function, gradient and hessian calculations are
brought in from the `textbook` module.

The Python decorator is invoked by using the Python convention of the
`@` followed by the name of the decorator function, which in this case is
`di.python_interface`.  This has the effect of passing the incoming
Python dictionary of parameters and expected responses to the decorator
which internally converts this to `Parameters` and `Results` objects
native to `dakota.interfacing`.  Two helper functions also in `driver.py`
extract parameter information suitable to the call to `textbook_list`
and subsequently pack the function, gradient and hessian values calculated
in that call into the `Results` object.  The decorator then internally
extracts and returns to Dakota the needed python dictionary of results
required by the Python direct interface.


# How to run the example
 
 Make sure the `PYTHONPATH` environment variable includes the directories
 containing the textbook.py driver script and the `dakota` Python package.

Run Dakota

    $ dakota -i dakota_textbook_python.in
 
# Requirements

Dakota built with the Python direct interface enabled. The downloads available on the Dakota website meet this
requirement, as do builds from source, by default.

# Contents

* `dakota_textbook_python.in`: Dakota input file
* `driver.py`: Module containing the decorated callback function used by
   the Python direct interface together with helper functions for extracting
   and populating data with the `dakota.interfacing` `Parameters` and
  `Results` objects, respectively.
* `textbook.py`: simulator for computing functions, gradients and hessians for
   parameter values

# Further reading

* The Textbook function is described in more detail in the 
  [User Manaul](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/examples/additionalexamples.html#textbook).
* More details of the Python linked interface can be found in the 
  [User Manual](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/advanced/advancedsimulationcodeinterfaces.html#python).
