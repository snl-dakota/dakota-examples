# Summary

Use Dakota's new surrogate library to build and evaluate surrogates within and outside of a Dakota study

# Description

Dakota's surrogate modeling capabilities are being re-implemented in a new library. A Python binding to
the library is also available in the `dakota.surrogates` module. The module enables building,
evaluating, saving, and loading surrogates models outside of Dakota. Dakota itself can save surrogate
models that it constructs during a study, which can be loaded and evaluated later in a Python script.

This example demonstrates use of `dakota.surrogates` to build and evaluate a polynomial and a Gaussian
process model. Model saving and loading in Python are also demonstrated. Second, a Dakota study that
builds and saves a Gaussian process model is explained, and a script is provided that loads and
interrogates the model.

# Python Binding

The Jupyter notebook `dakota_surrogates_demo.ipynb` demonstrates using the `dakota.surrogates` module
to build, evaluate, save, and load polynomial and Gaussian process surrogate models. Open the notebook
to view the example.

# Dakota Study

The Dakota input file `dakota_morris_gp_study.in` constructs an `experimental_gaussian_process` surrogate
model using the new surrogate modeling library. It obtains training data using a DACE method. See the
[dace](../dace) example for further explanation. The surrogate model block is:
```
model
  id_model = 'SurrogateModel'
  surrogate global
    dace_method_pointer = 'DesignMethod'
  experimental_gaussian_process
    export_model
      filename_prefix 'morris'
      formats binary_archive
    export_approx_variance = 'dak_gp_variances.dat'
```

After training the surrogate, Dakota exports it to a file named `morris.gp.bin`. In addition, evaluations of
the GP variance are written to the file `dakota_gp_variances.dat`.

# Load exported model

The `load_gp.py` script loads `morris.gp.bin` and prints out some of information it retains about the
fitting process. The model could also be evaluated, if desired.

```python
import numpy as np
import sys

def print_gp_history(gp):
    obj_fun_values = gp.objective_function_history()
    print("GP MLE objective function value history:\n{0}\n".format(obj_fun_values))
    
    obj_grad_values = gp.objective_gradient_history()
    print("GP MLE objective gradient history:\n{0}\n".format(obj_grad_values))
    
    theta_values = gp.theta_history()
    print("GP MLE hyperparameter (theta) history:\n{0}\n".format(theta_values))

if __name__ == '__main__':
    import dakota.surrogates as daksurr
    morris_gp = daksurr.load("morris.gp.bin", True)
    print_gp_history(morris_gp)
```

# How to run the example

* Use Jupyter Notebook or Jupyterlab to open `dakota_surrogates_demo.ipynb`.  On gitlab, the notebook can be viewed read-only. 
Another way to view the notebook read-only is by opening `dakota_surrogates_demo.html` in a web browser.
* Run the dakota study using the command `dakota dakota_morris_gp_study.in`. This regenerates `morris.gp.bin`.
* Import `morris_gp.bin` and print out its build history using the command `python3 load_gp.py`.

# Requirements

* Dakota built with Python support
* Python. The major.minor version must match the one that Dakota was built with. One quick way to learn the version is by locating the Python library in Dakota's bin folder. On POSIX systems, the library will be named libpythonM.Nm.so.X.Y, where M.N is the major.minor version, e.g. 3.6.
* [Jupyter notebook or JupyterLab](https://jupyter.org/) is needed to run the notebook interactively. The Python packages `seaborn`, `numpy`, and `matplotlib` are also required. All these dependencies can be satisfied by installing the [Anaconda](https://www.anaconda.com/) Python distribution. It may be convenient to set up a conda environment with the correct version of Python and the required packages.

