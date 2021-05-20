# Summary

Describe use of Monte Carlo sampling to estimate the expectation (mean) of a model QoI and discuss the uncertainty in that estimate

# Description

This example is part of a longer tutorial that covers Dakota's multilevel and multifidelity sampling approaches. The top-level page, which provides an outline and describes the test problem used throughout the tutorial, is [here](../README.md). In this section, Monte Carlo sampling is used to estimate the expectation (mean) of a model QoI. The variance or uncertainty of the estimate is discussed. Understanding these concepts is key before reading the following sections.

# Theory Highlights

A Monte Carlo estimator for evaluating the expected value of a generic
QoI $`Q`$ can be written as

```math
\hat{Q}^{MC} = \frac{1}{N} \sum_{i=1}^N Q^{(i)},
```

where $`Q^{(i)}`$ corresponds to the $`i`$th realization of the QoI (for us
the average temperature in the rod) and $`N`$ indicates the number of
random realizations. The MC estimator has a variability associated to
the set of $`N`$ realizations that can be obtained, *i.e.* we would get a
different results each time we run a set of $`N`$ evaluations. The
variance of the MC estimator can be quantified as

```math
{\mathbb{V}ar\left[ \hat{Q}^{MC} \right]} = \frac{ {\mathbb{V}ar\left[Q\right]} }{ N },
```

where the variance of the QoI is indicated with
$`{\mathbb{V}ar\left[Q\right]}`$. It is common to report the result of a
MC simulation in term of their confidence of interval, which is based on
the normal distribution followed by a MC estimator. A confidence of
interval is built by considering a multiple of the estimator standard
deviation around the mean value. For instance, a 95% confidence interval
can be obtained by using an interval of
$`\pm 1.96 {\mathbb{V}ar^{1/2}\left[\hat{Q}^{MC}\right]}`$. This is the
default in Dakota.

# Input Configuration

We start with a MC study that uses only the highest fidelity model:
$`N_{mod} = 21`$ and $`N_x=200`$ (see Table at the bottom of the [problem description](../README.md#test-problem-description)). In the following the main features of the
input file (`dakota_MC.in`) are discussed:

The `environment` section of the input configures the tabular file that will be written at the end of the
execution to collect input coordinates and output values;
```
environment,
   tabular_data
   tabular_data_file = 'dakota_MC_HF.dat' 
   freeform
```
The `method` section selects a MC (`random`) sampling with 1000 samples. Latin hypercube sampling is also available `lhs`;
```
method,
   sampling
      sample_type random # lhs
      samples = 1000
      seed = 1234 
```
The `model` section defines the model (`HF`) and the variable pointer (`HF_VARS`);
```
model,
	id_model = 'HF'
	variables_pointer = 'HF_VARS'
	simulation   
```

In the `variables` section, the seven uniform uncertainties $`~\mathcal{U}(-1,1)`$ are first defined, and then a pair of `discrete_state_set` variables are used to define the model fidelity and level. In this case the `initial_state=200 21` is the only combination of states which defines the HF model;
```
variables,
	id_variables = 'HF_VARS'
	uniform_uncertain = 7
	  lower_bounds    = 7*-1.
	  upper_bounds    = 7* 1.
	discrete_state_set
	  integer = 2
	    num_set_values = 1 1
	    set_values = 200 # number of spatial coords
	    	       	 21  # number of Fourier solution modes
	    initial_state = 200 21
	    descriptors 'N_x' 'N_mod'
```

The `transient_diffusion_1d` driver is built into Dakota and so uses the `direct` interface type.
```
interface,
	 direct
	  analysis_driver = 'transient_diffusion_1d'
	  deactivate restart_file
```
Finally, the `responses` section specifies that we expect a single output for the QoI and we do not expect gradients
    or Hessian information.
```
responses,
	response_functions = 1
	no_gradients
	no_hessians	 
```

# PostProcessing Phase

The MC configuration can be executed with:\
`dakota -i dakota_MC.in -o dakota_MC.out`

and this produces a number of outputs. The relevant ones are:

-   `dakota_MC_HF.dat` which is the tabular file we configured for the
    input/output matrix;

-   `dakota_MC.out` which contains the results of the analysis (and
    output relative to the job execution).

For this tutorial the important information is reported at the end of
`dakota_MC.out`

Dakota computes moments (mean, standard deviation, skewness and
kurtosis) near the end of the output, and for
the mean and standard deviation the confidence interval is also
provided.



```
<<<<< Function evaluation summary: 1000 total (1000 new, 0 duplicate)
-----------------------------------------------------------------------------
Statistics based on 1000 samples:

Sample moment statistics for each response function:
                            Mean           Std Dev          Skewness          Kurtosis
 response_fn_1  4.0550855939e+01  1.0778033484e+02  2.4185521044e+00  8.4391131873e+00

95% confidence intervals for each response function:
                    LowerCI_Mean      UpperCI_Mean    LowerCI_StdDev    UpperCI_StdDev
 response_fn_1  3.3862581142e+01  4.7239130736e+01  1.0325489177e+02  1.1272371842e+02
```
(Note: on your system, the results may differ somewhat.)

The user can easily generate a different confidence interval by using
the provided output. For instance, the confidence interval for the mean
corresponding to a 99.7% probability can be obtained by using $`\pm 3`$
times the estimator standard deviation. This confidence interval could
be obtained directly from the Dakota output. The variance
of the quantity of interest, $`{\mathbb{V}ar\left[Q\right]}`$, can be
obtained from `Std Dev` (*i.e.* $`1.0778033484e+02`$) and therefore the
estimator standard deviation can be computed as
$`107.78033484/\sqrt{1000} = 3.4083`$. It follows that the 99.7%
confidence interval for the mean is $`\left[ 30.326, 50.776 \right]`$. The
exact solution for this problem is 41.98.

# Further Reading

* Reference Manual entry for the 
  [sampling](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/method-sampling.html)
  method.
* [User's Manual](https://dakota.sandia.gov/content/manuals) discussion of active variable view in section 9.5.

---

* Return to the [Outline](../README.md#outline)
* Continue to the [next section](../cv) of the tutorial.
