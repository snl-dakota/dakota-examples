# Summary

Perform batch evaluations using dakota.interfacing and Dakota's direct Python interface

# Description

This example combines use of the Dakota direct `python` callback interface
with use of the `dakota.interfacing` Python module to perform batch evaluations.
When used alone to perform evaluations in batch, Dakota's `python` interface passes 
a list of parameter dictionaries (one dictionary per evaluation in the batch)
to the user-provided Python function, and expects the function to return a corresponding
list of results dictionaries. The `dakota.interfacing` module provides a decorator
that transparently converts the parameters list to `BatchParameters` and `BatchResults`
objects. The decorator is named `python_interface`, and its use is illustrated below.

# Driver

The name of user-provided function in the `driver` module is `decorated_driver`. It
is listed here, along with the `python_interface` decorator.

```python
@di.python_interface
def decorated_driver(batch_params, batch_results):
    assert(isinstance(batch_params, di.BatchParameters))
    assert(isinstance(batch_results, di.BatchResults))
    for params, results in zip(batch_params, batch_results):
        textbook_input = pack_textbook_parameters(params, results)
        fns, grads, hessians = textbook_list(textbook_input)
        results = pack_dakota_results(fns, grads, hessians, results)
    return batch_results
```

Prior to this snippet, the driver imports the `dakota.interfacing` module
as `di`, and the actual funxtion, gradient and hessian calculations are
brought in from the `textbook` module.

The Python decorator is invoked by using the Python convention of the
`@` followed by the name of the decorator function.  This has the effect
of passing the incoming Python list of dictionaries of parameters and expected 
responses to the decorator, which internally converts this information to `BatchParameters`
and `BatchResults` objects, defined in `dakota.interfacing`.  Helper
functions in `driver.py` extract parameter information from these objects, 
compute the responses, and pack the resulting function, gradient and hessian values
into `Results` object.  The decorator then internally
extracts and returns to Dakota the expected list of dictionaries of results.

# How to run the example
 
 Make sure the `PYTHONPATH` environment variable includes the directories
 containing the textbook.py driver script and the `dakota` Python package.

Run Dakota

    $ dakota -i dakota_textbook_python_batch.in
 
# Requirements

Dakota built with the Python direct interface enabled. The downloads available on the Dakota website meet this
requirement, as do builds from source, by default.

# Contents

* `dakota_textbook_python_batch.in`: Dakota input file
* `driver.py`: Module containing the decorated callback function used by
   the Python direct interface together with helper functions for extracting
   and populating data with the `dakota.interfacing` `BatchParameters` and
  `BatchResults` objects, respectively.
* `textbook.py`: simulator for computing functions, gradients and hessians for
   parameter values

# Further reading

* The Textbook function is described in more detail in the 
  [User Manaul](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/examples/additionalexamples.html#textbook).
* More details of the Python linked interface can be found in the 
  [User Manual](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/advanced/advancedsimulationcodeinterfaces.html#python).

