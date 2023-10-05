# Summary

Use the python interface to run a driver that uses a tensorflow/keras surrogate model
for predictions

# Description

This example demonstrates use of a pre-built tensorflow/keras model in a Python driver.
Dakota executes the driver using its direct `python` callback interface. One noteworthy
feature of the example is that the model, which is a surrogate of Dakota's built-in 
`sobol_ishigami` function, is loaded at module scope rather than in the driver function.
Because Dakota imports the module only once, this approach elminates the overheard that
would occur if the model were loaded every time Dakota called the driver function.

# Driver
The main function of the direct Python callback driver 'TF-Ishigami.py' is: 

``` python
tfk_model = tf.keras.models.load_model("./exported_tfk_model.keras")

@di.python_interface
def prediction_driver(params, results):
    params_list = []
    #add current iteration dakota parameters with sample values into python list
    for i, label in enumerate(params):
        params_list.append(params[label])

    #add function output to dakota response object 
    for i, label in enumerate(results):
        results[label].function = tfk_model.predict([params_list])[0][0]

#return function output as dakota response object
    return results

```

Prior to this snippet, the driver imports the `dakota.interfacing` module
as `di`. 
The Python decorator is invoked by using the Python convention of
`@` followed by the name of the decorator function which in this case is
`di.python_interface()`. This has the effect of passing the incoming
python dictionary of parameters and expected responses to the decorator
which internally converts this to `Parameters` and `Responses` objects
native to `dakota.interfacing`.

The `prediction_driver()` function receives direct parameters from Dakota and a results variable to package the responses into.
The received parameters are then sent to a Tensorflow/Keras surrogate model. Its prediction is placed in the results object
and returned to Dakota.

# Dakota input

Dakota input file for direct global sensitivity analysis on the Ishigami function or on the Tensorflow/Keras surrogate model of it.

```
method
	polynomial_chaos
	    quadrature_order = 5
     	variance_based_decomp

variables
	uniform_uncertain =  3
	descriptors     =    'x1'      'x2'    'x3'
	lower_bounds    =     0         0       0
	upper_bounds    =     1         1       1

interface
    python
    analysis_driver = 'TF-Ishigami:prediction_driver'
#     direct
#     analysis_driver = 'sobol_ishigami'



responses
    response_functions = 1
    descriptors = 'Ishigami'
	no_gradients
	no_hessians

```

# How to run the example

The tensorflow/keras model first must be trained using data from the `sobol_ishigami` function.

To create sample data from the Ishigami function

    $ dakota -i dakota_training_data.in

To build Tensorflow/Keras surrogate model from Dakota sample data

    $ python tfk_model_build.py

To perform sensitivity analysis on the previously trained and exported surrogate model or Dakota's `sobol_ishigami` function:

    $ dakota -i dakota-TF_pce_quadrature.in -o dakota_pce_quadrature.out

(to modify what interface to use, uncomment or comment the driver to be tested in the dakota-TF_pce_quadrature.in input file's interface block)

# Requirements

Dakota built with Python support. The downloads available on the Dakota website come with Python enabled.
The major.minor version of Python (e.g. 2.7, 3.8) in your environment must match the one included with Dakota.
The version that comes with Dakota can be checked by examining the contents of the bin folder, which contains a
versioned Python library. We recommend setting up a conda or virtual environment to use with Dakota in order to
satisfy the version requirements.

Python with the following libraries: numpy, pandas, tensorflow

# Contents

* `dakota-TF_pce_quadrature.in`: Dakota input file that performs variance based decomposition based on polynomial chaos expansion samples on an external/tensorflow surrogate model.  

* `TF-Ishigami.py`: Module with decorated callback function used by Dakota's "direct" interface, for Dakota IO.

* `dakota_training_data.in`: Dakota input file that creates samples from Dakota's built-in implementation of the sobol_ishigami function and outputs a tabular file "ishigami_training_data.txt"

* `tfk_model_build.py`: Python script with Tensorflow/Keras libraries to train a surrogate neural network model from Dakota's sampled data.


# Further Reading

More information can be found in Chapter 5.4 of the Dakota User's Manual.  Theoretical foundations can be found in Chapter 3 of the Dakota Theory Manual.  Both can be found at https://dakota.sandia.gov/content/manuals.

* More details of the Python linked interface can be found in the [Reference
  Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/interface-analysis_drivers-python.html)
  and in Section 16.3.2 of the [User's Manual](https://dakota.sandia.gov/content/manuals).
* Chapter 10 of the User's Manual provides a full description of interfacing in Dakota, including documentation 
  of the `dakota.interfacing` module.
