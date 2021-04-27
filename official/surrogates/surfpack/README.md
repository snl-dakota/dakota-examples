# Summary

Create and evaluate surrogate models with Dakota and Surfpack

# Description

Many of Dakota's surrogate capabilities are provided by Surfpack,
a software library and application for building and evaluating
a variety of surrogate types. Other examples demonstrate how to
use Dakota to construct and use surfpack surrogates as part of a
study. In this example, Dakota will export a surrogate to a file,
and the `surfpack` application will be used to evaluate it. The
example also demonstrates how to use the `surfpack` application
to build and evaluate a surrogate outside of Dakota.

An important Dakota limitation is that although it can export 
Surfpack surrogates, it cannot import them. Users who need
support for exporting and importing surrogates should consider
using Dakota's new surrogate library, instead. It is demonstrated
[here](../library/).

The discussion and examples here apply not only to Gaussian process 
models, but to the following Dakota global surrogate types, all 
provided by the Surfpack sub-package:

* `gaussian_process surfpack`,  `kriging surfpack`
* `mars`
* `moving_least_squares`
* `neural_network`
* `radial_basis`
* `polynomial`

The Dakota-only approaches described will also work for other Dakota
surrogate models, but the Surfpack-specific approaches will not.  All
examples here use a two variable form of the textbook example function
provided with Dakota, so are creating a surrogate model for the
textbook function $`f(x1, x2)`$.

# Contents

The example contains the following input files:

* `build_points.dat`: Training data used by Dakota and Surfpack to build the surrogate model
* `dakota_sampling_surrogate.in`: Dakota study that constructs, uses, and exports a surrogate
* `eval_points.dat`: Points at which Dakota and Surfpack will evaluate the surrogate
* `sp_build_surrogate.spk`: `surfpack` input file to build a surrogate
* `sp_eval_surrogate.spk`: `surfpack` input file to evaluate a surrogate


And the following example output files:

* `dak_gp_model.f.sps`: Surrogate exported by Dakota
* `sp_gp_model.f.sps`: Surrogate exported by `surfpack`
* `sp_surrogate_evals.dat`: Record of `surfpack` surrogate evaluations

# Building a Surrogate Model

## Using Dakota

The [dace](../dace/) and [imported](../imported/) surrogate examples 
demonstrate and explain how to use Dakota to build and use a surrogate.
The present example adds one further detail: surrogate export.

The `model` section of the Dakota input file `dakota_surrogate.in`
includes the keywords,

```
    export_model
      filename_prefix = 'dak_gp_model'
      formats
        text_archive
```
After constructing a surrogate for a response, these keywords direct Dakota to write
it to a file named `dak_gp_model.DESCRIPTOR.sps`. The `DESCRIPTOR` in this case is
`f` (see the `responses` section of the file). Valid formats for writing a 
`surfpack`-readable file are `text_archive` and `binary_archive`. The difference 
between the two is usually unimportant.

The exported file is included with the example. To regenerate it, simply run Dakota:

`dakota dakota_sampling_surrogate.in`

## Using the Surfpack Executable

To build the same surrogate model using the standalone Surfpack
executable `surfpack`, use the Surfpack instruction file `sp_build_surrogate.spk`:
```
Load[name = textbook_build, file = 'build_points.dat',
     n_predictors= 2, n_responses = 1]

CreateSurface[name = textbook_gp, data = textbook_build, type = kriging]

Save[surface = textbook_gp, file = 'sp_gp_model.f.sps']
```
To build, run `surfpack sp_build_surrogate.spk`, which will
write the file `sp_gp_model.f.sps`.  In this example the
Surfpack-generated GP model will differ slightly from that generated
by Dakota.  This is being investigated.

# Evaluating a Surrogate Model

This section discusses evaluating a surrogate model either in Dakota
directly or in Surfpack after previously saving in Dakota or Surfpack.

## Using Dakota

The Dakota input `dakota_surrogate.in` performs a list parameter
study. In a list parameter study, Dakota runs a simulation (or evaluates
a surrogate) at a list of user-specified points. The points can be listed
directly in the input file or read from a tabular file. This example reads
the points from `eval_points.dat`:
```
0.90 1.00
0.95 1.00
1.00 1.00
1.00 0.93
1.00 0.98
1.00 1.01
```
As mentioned previously, Dakota cannot import a previously exported
Surfpack surrogate. To use the same surrogate in multiple studies,
the best approach is to reuse training data, which causes Dakota to
build the same surrogate.

For studies that construct surrogates using imported tabular data,
simply use the same tabular data file. This is the approach used
in this example.

When Dakota obtains surrogate training data using a [dace](../dace)
method, Dakota writes the data to the restart file. Subsequent studies
can load the data from that source.

To load data from the restart file, run Dakota with the `-read_restart` option:

`dakota -input dakota_study.in -read_restart dakota.rst`.

For the restart file method to work, the DACE method specification (including
any `seed` specification), variables, and responses must be the same in all studies.

The `dakota_restart_utility` also can be used to write evaluations
from the restart file to tabular format, which can be imported.

## Using the Surfpack Executable

This example uses Surfpack to evaluate a saved surrogate at user
provided points.  (Surfpack can also generate simple designs at which
to evaluate the surrogate using the CreateSample command.)  The
commands for evaluation are in `sp_eval_surrogate.spk`:
```
Load[name = eval_points, file = 'eval_points.dat', 
     n_predictors = 2, n_responses = 0 ]

Load[name = textbook_gp, file = 'sp_gp_model.f.sps']

Evaluate[surface = textbook_gp, data = eval_points]
Save[data = eval_points, file = 'sp_surrogate_evals.dat']
```

Running `surfpack sp_eval_surrogate.spk` loads the surface from
the file `sp_gp_model.f.sps`, loads a
set of evaluation points from `eval_points.dat` and evaluates the model 
at them, writing `sp_surrogate_evals.dat`:
```
   9.000000e-01   1.000000e+00   4.052870e-05
   9.500000e-01   1.000000e+00   7.658733e-06
   1.000000e+00   1.000000e+00  -2.051040e-06
   1.000000e+00   9.300000e-01   2.751099e-05
   1.000000e+00   9.800000e-01   1.538432e-07
   1.000000e+00   1.010000e+00  -4.029054e-06
```
The Surfpack phases for building and evaluating a surrogate model may
be combined into a single Surfpack command file if desired.

# Further Reading

* Section 8.4 (Surrogates) of the User's Manual
* [model->surrogate->global](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/model-surrogate-global.html)
  keyword entry in the Reference Manual.
* [Surpack User's Manual](https://dakota.sandia.gov//sites/default/files/documents/surfpack_users_manual.pdf)
