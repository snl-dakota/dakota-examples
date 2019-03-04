# Summary
Perform statistical model calibration using Bayesian inference with noisy
observations relating to two model outputs (responses).
 
### Run Dakota
    $ dakota -i dakota_bayes_calib_multi_qoi.in -o dakota_bayes_calib_multi_qoi.out
 
# What problem does this solve?
This example demonstrates how to calibrate a model using Bayesian inference
to noisy experimental data.
 
## Math Equation

In Bayesian calibration, uncertain input parameters, $` \boldsymbol{\theta} `$
are initially characterized
by a prior distribution, $` f_{\boldsymbol{\Theta}}\left( \boldsymbol{\theta}
\right) `$. A Bayesian calibration approach uses noisy data,
$` \boldsymbol{d} `$, together with a likelihood function,
$` \mathcal{L}\left(\boldsymbol{{\theta ;d}} \right) `$, which describes how
well a realization of the parameters is supported by the data, to update this
prior knowledge. The process yields a posterior distribution,
$` f_{\boldsymbol{{\Theta |D}}}\left( \boldsymbol{{\theta |d}} \right) `$ of
the parameters most consistent with the data, such that running the model
at samples from the posterior yields results consistent with the
observational data and the associated noise model:

$` {f_{\boldsymbol{\Theta |D}}}\left( \boldsymbol{\theta |d} \right) = \frac{{{f_{\boldsymbol{\Theta}}}\left( \boldsymbol{\theta}  \right)\mathcal{L}\left( \boldsymbol{\theta;d} \right)}}{{{f_{\boldsymbol{D}}}\left( \boldsymbol{d} \right)}} `$.

The specific likelihood function used in
Dakota is based on Gaussian probability density functions. This means
that we assume the difference between the model-predicted quantity
(e.g. quantity of interest returned from a computer simulation) and
the experimental observation is Gaussian.

# What method will we use?

We utilize Markov Chain Monte Carlo (MCMC) sampling technique to
generate samples from the posterior parameter distribution. We utilize the
QUESO library (Quantification of Uncertainty for Estimation,
Simulation, and Optimization) developed at The University of Texas at
Austin. Its implementation of the Delayed Rejection and Adaptive
Metropolis (DRAM) algorithm is used.

# Additional Input to Dakota

Dakota expects to find all the data required for calibration in one file with a
predefined name of **dakota_cantilever_queso.withsigma.dat**. The calibration
data file has the observational data: in this case, it is a freeform file (e.g.
no header or annotation) with ten experiments. For each experiment, there are
two experiment values, one for stress and one for displacement, followed by two
variance values for the error associated with that experiment for each quantity
of interest.

## Analysis Driver

The model to be calibrated is that of a simple
uniform cantilever beam for which the cross-sectional width, $` w `$, and 
Young's modulus, $` E `$, are unknowns to be inferred from multiple (10)
independent noisy observations of the maximum stress and tip deflection, relative
to some nominal stress and displacement values, being $` R=40000 `$ and
$` D_{0} = 2.2535 `$, respectively. The maximum stress and tip displacement
have the following relationships:

$` \mathtt{stress}=\frac{600}{w t^2}Y+\frac{600}{w^2t}X `$

and

$` \mathtt{displacement}=\frac{4L^3}{E w t}
  \sqrt{\bigg(\frac{Y}{t^2}\bigg)^2+\bigg(\frac{X}{w^2}\bigg)^2} `$ .

We assume that the horizontal and vertical loads, $`X`$ and $`Y`$, as well as the
cross-sectional thickness, $` t `$, are known, as provided in the Dakota input
file, with values being 500, 1000, and 3, respectively.

### Inputs

The mod\_cantilever driver expects values for:

- $`E`$: Young's modulus
- $`w`$: width
- $`t`$: thickness
- $`R`$: yield strength
- $`X`$: horizontal load
- $`Y`$: vertical load

### Outputs

The driver provides either two or three outputs, depending on the number 
specified in the responses section of the Dakota input file. When three are 
requested, they are:

- area
- stress constraint
- displacement constraint

When two are requested, as in this example, the latter two are returend.
 
# Interpret the results
 
## Screen Output

Dakota produces the following output to the screen (redirected to
`dakota_bayes_calib_multi_qoi.out`):

~~~~
<<<<< Best parameters          =
                      2.8691852474e+07 E
                      2.4998843409e+00 w
<<<<< Best misfit              =
                      9.7137281272e+00
<<<<< Best log prior           =
                     -2.0703165165e+01
<<<<< Best log posterior       =
                     -6.9874315821e+01
Sample moment statistics for each posterior variable:
                            Mean           Std Dev          Skewness          Kurtosis
             E  2.8609959149e+07  1.4417714265e+05  8.0289072767e-01  7.8655956161e-02
             w  2.5016445558e+00  3.8306697138e-03 -1.2217188066e-01  3.8866929785e-02
Sample moment statistics for each response function:
                            Mean           Std Dev          Skewness          Kurtosis
        stress  2.6282814617e+03  8.9765361327e+01  1.3400226598e-01  4.9239052295e-02
  displacement  2.9604502307e-01  1.0636886950e-02 -3.5080744510e-01 -1.2381836901e-01
                  Response Level    Probability Level
                  ----------------- -----------------
                  2.4532691039e+03  5.0000000000e-02
                  2.8135291937e+03  9.5000000000e-01
                  2.4826692535e+03  1.0000000000e-01
                  2.7721260449e+03  9.0000000000e-01
                  Response Level    Probability Level
                  ----------------- -----------------
                  2.7441078882e-01  5.0000000000e-02
                  3.1315737297e-01  9.5000000000e-01
                  2.7697240600e-01  1.0000000000e-01
                  3.1131408378e-01  9.0000000000e-01
                  Response Level    Probability Level
                  ----------------- -----------------
                  2.0843894793e+03  5.0000000000e-02
                  3.1738032617e+03  9.5000000000e-01
                  2.1663019534e+03  1.0000000000e-01
                  3.0881754948e+03  9.0000000000e-01
                  Response Level    Probability Level
                  ----------------- -----------------
                  2.3243987081e-01  5.0000000000e-02
                  3.5984952189e-01  9.5000000000e-01
                  2.4309506889e-01  1.0000000000e-01
                  3.4867791685e-01  9.0000000000e-01
~~~~

The final results include:

* The best parameters, being the maximum a-posteriori (MAP) parameter estimates (those that maximize the posterior probability density)
* Statistical moments of inferred parameters, being the cross-sectional width, $` w `$, and 
Young's modulus, $` E `$
* Statistical moments of pushed-forward response functions, being maximum stress and tip displacement
* Credible and prediction intervals for each model output

## Chain Samples

The chain samples are written to the file `chain_samples.dat` in Dakota tabular format.