# Summary

Import data from a tabular file to construct a surrogate model, and
then run a study on it

# Description

Dakota can construct a surrogate model from imported data and then execute a 
method on that model. In studies like these, Dakota need not run an external
simulation at all, and data can be used from any source, including prior Dakota
studies and physical experiments.

In this example, a Gaussian process surrogate is built from 10 data points,
which are imported from a tabular data file. Then, a larger LHS study (100 samples)
is executed on the surrogate. The example explains the Dakota input
file, the format of imported data file, and warns of a few "gotchas" when importing
data.

# Surrogate Model Specification

Compared to the [dace](../dace) example, this one is relatively straightforward.
We focus our attention on the surrogate model specification in `dakota_sampling_surrogate.in`.
```
model
  surrogate global
    gaussian_process surfpack	
    import_build_points_file 'training_data.dat'
      annotated
        use_variable_labels
```
The `surrogate global` keywords identify the type of model. This is in contrast to, say,
a `single` model type, which is used when running an external simulation. The specific
kind of surrogate that Dakota will build and evaluate is `gaussian_process surfpack`.
Surfpack is the surrogate modeling library that currently provides much of Dakota's
surrogate capabilities.

The `import_build_points_file` keyword specifies the pathname of the tabular file that
contains the build points; its format is `annotated`.

## The annotated file format

The first few lines of `training_data.dat` are:
```
%eval_id interface             x1             x2              f 
1        NO_ID    1.040428725   0.9481639439 9.891374515e-06 
2        NO_ID    1.067546302   0.9390941226 3.457701524e-05 
3        NO_ID    1.012198763     0.99543788 2.257753865e-08 
...
```
A total of ten data points appear in the actual file. The features of the
file that make it "annotated" are 1) the initial header row, 2) the evaluation
ID column, and 3) the interface column. In a [`freeform`](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/model-surrogate-global-import_build_points_file-freeform.html) file, only the data
would appear, and any combination of the three annotations can be present in a 
[`custom_annotated`](https://dakota.sandia.gov//sites/default/files/docs/6.13/html-ref/model-surrogate-global-import_build_points_file-custom_annotated.html) file.

The `use_variable_labels` keyword in the Dakota input causes Dakota to validate
the variable labels (`x1` and `x2` here) that appear in the header row against those that 
appear in the model's `variables` specification. In addition, when this keyword is used,
the variable columns can appear in any order. The responses always must come after the
variables, and they must appear in the correct order. It is recommended to use the 
`annotated` (or `custom_annotated header`) format and `use_variable_labels` keywords
whenever possible to reduce the risk of mistakes.

One final note concerning the interface column in the tabular file. The interplay between
it and the `id_interface` of any interfaces in the study can be confusing. Broadly speaking,
the column contents must match the ID of an interface that is associated with the surrogate
model via a `dace_method_pointer`or `truth_model_pointer`. Otherwise, it should be `NO_ID`.
In this example, there are no interface blocks, so the column is `NO_ID`. A tell-tale
sign of a problem with interface naming is that the console output indicates that
data was imported, but surrogate construction fails because no data is available to it. This often
occurs when the tabular data file that is being imported was exported from a previous Dakota study
that had a differently named interface.

Tabular files that lack an interface column altogether (e.g. `freeform` files) are less restrictive
and will "just work".

# Dakota Output

Reviewing Dakota's console output helps to clarify what's happening in the study. A few snippets of the
output are shown here. After echoing out the input file, Dakota reports:

```
Surrogate model retrieving points with 2 variables and 1 response
functions from file 'training_data.dat'
Surrogate model retrieved 10 total points.
```

Having read in the training data, Dakota begins to execute the study. 

```
>>>>> Executing environment.

>>>>> Running random_sampling iterator.

NonD lhs Samples = 100 Seed (user-specified) = 5

>>>>> Building global_kriging approximations.
Constructing global approximations with no anchor, 0 DACE samples, and 10 reused points.
--- Surfpack Kriging Diagnostics ---
KM: #real inputs=2; #pts=10; used 10/10 pts;
using the Gaussian correlation function with (unscaled)
Correlation lengths=[0.50592, 0.029874]^T
found by the "global" optimization_method;
unadjusted variance=3.51715e-10; "per equation" log(likelihood)=3.68003;
rcond(R)=0.000810124; rcond(G_Rinv_Gtran)=0.0788191; [if either rcond is less
than 2^-40 (approx 9.095*10^-13) then the matrix is ill-conditioned and
that "voids the warranty" of the Kriging Model]; nugget=0.  A reduced_polynomial
of order 2 (with 5 terms) was requested for the trend function; the build
data was sufficient to use the requested trend function; the highest total
polynomial order of any term in the utlized trend function is 2;
for SCALED inputs and outputs the utilized trend function is
betaHat^T*g(x)=-0.661231 + 0.0605352*x0 + 0.159936*x1 + ...
               1.46994*x0^2 + 4.3462*x1^2
------------------------------------

<<<<< global_kriging approximation builds completed.
```
The `random_sampling iterator` is the sampling method. Before it can be executed, the
surrogate must be constructed. Diagnostics from the surrogate build process are
reported to the console. (A "Kriging" model is another name for a Gaussian process.)

After building the surrogate, Dakota runs the sampling study on it. Evaluations on the
surrogate model are not reported at this level of verbosity; to see them, add `output verbose`
to the method block. Dakota reports the function evaluation summary:

```
<<<<< Function evaluation summary (APPROX_INTERFACE_1): 100 total (100 new, 0 duplicate)
```

Then the final statistics from the 100 samples on the surrogate are reported.

# How to run the example

`dakota -i dakota_sampling_surrogate.in`

# Further reading

* Section 8.4 (Surrogates) of the User's Manual
* [model->surrogate->global](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/model-surrogate-global.html)
  keyword entry in the Reference Manual.
* Dakota [surrogates training](https://dakota.sandia.gov/training/dakota-training-materials)

