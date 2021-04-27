# Summary

Collect training data from a simulation to construct a surrogate model, and
then run a study on it

# Description

In a single Dakota run, Dakota can collect training data from a simulation to
construct a surrogate model and then execute a method on that model. Dakota
uses a *DACE method* to collect training data. DACE is an acronym that stands 
for *design and analysis of computer experiments*, and is a term that refers 
to methodologies for constructing surrogate models of computational simulations.
In addition to specifying the method that will be run on the surrogate, the user
must include a DACE method block the the Dakota input file.

In this example, a Gaussian process surrogate of the built-in `text_book`
function (2 variables, 1 response) is built from 10 latin hypercube samples.
Then, a larger LHS study (100 samples) is executed on the surrogate. The
example explains the structure of the Dakota input file and the specific 
keywords needed to construct and use a surrogate model.

# Dakota Input File

There are several things to note about the input file, `dakota_sampling_surrogate.in`.

* In many simple Dakota studies, only one `method` block is present. In this
  one, there are two. The `EvalSurrogate` method block specifies the sampling
  study (100 samples) that is run on the surrogate. The `DesignMethod` block specifies the
  DACE method (10 samples), which Dakota uses to collect training data to build the surrogate.
* There are also two model blocks. `SurrogateModel` specifies the surrogate model details,
  including the type, `gaussian_process surfpack`. (The
  [model->surrogate->global](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/model-surrogate-global.html)
  section of the Reference Manual documents the other types of global surrogates that Dakota provides.)
  The second model, `SimulationModel`, is
  used by the `DesignMethod` to interrogate the simulation via the `SimulationInterface`. In this study,
  the two models share variables and responses specifications.
* The DACE method is linked to the surrogate model by the `dace_method_pointer` keyword.
* The `environment` block points to the top-level method using a `method_pointer`. When
  more than one method is present in an input file, the `environment` block and `method_pointer`
  must be included to make the structure of the study unambiguous.

# Dakota Output

Reviewing Dakota's console output helps to clarify what's happening in the study. A few snippets of the
output are shown here. After echoing out the input file, Dakota reports:

```
>>>>> Executing environment.

>>>>> Running random_sampling iterator.

NonD lhs Samples = 100 Seed (user-specified) = 5

>>>>> Building global_kriging approximations.

NonD lhs Samples = 10 Seed (user-specified) = 50

------------------------------
Begin SimulationInterface Evaluation    1
------------------------------
Parameters for evaluation 1:
                      1.0404287246e+00 x1
                      9.4816394391e-01 x2

Direct interface: invoking text_book

Active response data for SimulationInterface evaluation 1:
Active set vector = { 1 }
                      9.8913745147e-06 f
```

The `random_sampling` iterator is the `EvalSurrogate` method. Before this method can be run, Dakota
must construct the surrogate, the `global_kriging approxmation`. (A "kriging model" is another name
for a Gaussian process.) Dakota runs the 10 samples specified in the `DesignMethod` study; only the
first is shown here. On your system, the values of the variables, which are random, and the response f
may be a bit different.

After collecting the 10 samples, Dakota constructs the surrogate and prints some diagnostics:

```
>>>>> Appending 10 points to global_kriging approximations.

<<<<< global_kriging approximation updates completed.
Constructing global approximations with no anchor, 10 DACE samples, and 0 reused points.
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

After the model is constructed, Dakota evaluates it 100 times for the `EvalSurrogate` method.
The individual evaluations are not reported to the console at this level of verbosity, but may be seen by
adding `output verbose` to the `EvalSurrogate` specification.

Dakota prints a function evaluation summary:

```
<<<<< Function evaluation summary (APPROX_INTERFACE_1): 100 total (100 new, 0 duplicate)
<<<<< Function evaluation summary (SimulationInterface): 10 total (10 new, 0 duplicate)
```
In the summary, `SimulationInterface` of course refers to the user-specified interface to
the `text_book` driver. `APPROX_INTERFACE_1` is the name of the interface to the surrogate
model, which Dakota automatically generates.

# How to run the example

`dakota -i dakota_sampling_surrogate.in`

# Further reading

* Section 8.4 (Surrogates) of the User's Manual
* [model->surrogate->global](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/model-surrogate-global.html)
  keyword entry in the Reference Manual.
* Dakota [surrogates training](https://dakota.sandia.gov/training/dakota-training-materials)
