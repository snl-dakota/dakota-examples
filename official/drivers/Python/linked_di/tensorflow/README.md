# Summary

Perform uncertainty quantification and global sensitivity analysis using polynomial chaos expansions constructed from quadrature points applied to external tensorflow/keras surrogate model of the Ishigami function. 

# Description
To analyze the sensitivity of the function approximation of an exported surrogate model trained on random uniform samples of the Ishigami function.

# Driver
The main function of the direct Python callback driver 'TF-Ishigami.py' is: 
```
@di.python_interface
def prediction_driver(params, results):
    params_list = []
    #add current iteration dakota parameters with sample values into python list
    for i, label in enumerate(params):
        params_list.append(params[label])

    '''
    FOR TENSORFLOW (load an exported model)
    tfk_model = tf.keras.models.load_model("./exported_tfk_model.keras")
    '''
    #add function output to dakota response object 
    for i, label in enumerate(results):
        results[label].function = Ishigami(params_list)

        '''
        FOR TENSORFLOW (send parameter values to model and get a prediction)
        results[label].function = tfk_model.predict([params_list])[0][0]
        '''
    #return function output as dakota response object
    return results

```
Prior to this snippet, the driver imports the `dakota.interfacing` module
as `di`. 
The Python decorator is invoked by using the Python convention of the
`@` followed by the name of the decorator function which in this case is
`di.python_interface()`.  This has the effect of passing the incoming
python dictionary of parameters and expected responses to the decorator
which internally converts this to `Parameters` and `Responses` objects
native to `dakota.interfacing`. 
A helper function or tensorflow model (in the works) also in `TF-Ishigami.py`
extract the parameters gotten from dakota and call the functions to get a 
suitable `Response` object for dakota.
The function to calculate the Ishigami function output can 
either be a tensorflow model (in the works),  or a simple Ishigami function
in mathematical form "sin(x) + a*sin(y)**2 + b*z**4*sin(x)" where a = 7.0
and b = 0.1. 

# Dakota input
Dakota input file for global sensitivity analysis for the Ishigami function

```

method
	polynomial_chaos
	    quadrature_order = 5
     	variance_based_decomp #interaction_order = 1
	distribution cumulative

variables
	uniform_uncertain =  3
	descriptors     =    'x'      'y'      'z'
	lower_bounds    =    -3.141592 -3.141592 -3.141592
	upper_bounds    =    +3.141592 +3.141592 +3.141592

interface
    python
    analysis_driver = 'TF-Ishigami:prediction_driver'

responses
    response_functions = 1
    descriptors = 'Ishigami'
	no_gradients
	no_hessians

```
Dakota interfaces with python through the type `python`, Dakota passes keyword arguments
from the directory `kwargs`. These include PCE examples with the bounds set in the input file.


# How to run the example
	 
Make sure the Python used to build Dakota is in the environment PATH and
that the PYTHONPATH includes the directory containing the textbook.py
driver script.

To perform sensitivity analysis on the previously trained and exported surrogate model or dedicated function:
     $ dakota -i dakota-TF_pce_quadrature.in -o dakota_pce_quadrature.out
	

# Requirements

Dakota built with Python support. The downloads available on the Dakota website come with Python enabled.
The major.minor version of Python (e.g. 2.7, 3.8) in your environment must match the one included with Dakota.
The version that comes with Dakota can be checked by examining the contents of the bin folder, which contains a
versioned Python library. We recommend setting up a conda or virtual environment to use with Dakota in order to
satisfy the version requirements.

Python with the following libraries: numpy, pandas, tensorflow

# Contents

* `dakota-TF_pce_quadrature.in`: Dakota input file that performs variance based decomposition based on polynomial chaos expansion samples on an external surrogate model.  
* `TF-Ishigami.py`: Python scripts to read Dakota outputs and return predictions as responses for Dakota.
* `exported_tfk_model.keras`: Exported tensorflow/keras feed forward neural network for regression

# Further Reading

More information can be found in Chapter 5.4 of the Dakota User's Manual.  Theoretical foundations can be found in Chapter 3 of the Dakota Theory Manual.  Both can be found at https://dakota.sandia.gov/content/manuals.

* More details of the Python linked interface can be found in the [Reference
  Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/interface-analysis_drivers-python.html)
  and in Section 16.3.2 of the [User's Manual](https://dakota.sandia.gov/content/manuals).
* Chapter 10 of the User's Manual provides a full description of interfacing in Dakota, including documentation 
  of the `dakota.interfacing` module.
