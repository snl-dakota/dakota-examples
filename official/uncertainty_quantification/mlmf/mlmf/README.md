# Summary

Understand how Multilevel-Multifidelity Monte Carlo (MLMF) can compute statistics with greater precision and lower cost than orindary Monte Carlo and learn how to configure a Dakota study to use this approach

# Description

This example is part of a longer tutorial that covers Dakota's multilevel and multifidelity sampling approaches. The top-level page, which provides an outline and describes the test problem used throughout the tutorial, is [here](../README.md). In this section, multilevel Monte Carlo (MLMC) sampling is used to estimate the expectation (mean) of a model QoI. Comparison is made to results obtained using plain [Monte Carlo](../mc).

At the end of this section, the user should understand the basic theory that underlies MLMF, and undestand how to configure a Dakota study to use this approach.

# Theory Highlights

The multilevel-multifidelity (MLMF) estimator combines the two
approaches presented in the previous sections, MLMC and CVMC, in a
single variance reduction strategy. This method is particularly
well-suited when there are two model forms, and each of them has several
discretization levels associated to it. This is exactly the case of the
model problem presented in this tutorial.

The main idea is to use the MLMC to create a first expansion, based only
on the first model form, with a smaller variance than a single fidelity
estimator. The levels of the second model forms are paired with the one
of the first model form to obtain a control variate, level-by-level.

The estimator form is
```math
{\mathbb{E}\left[Q\right]} = \hat{Q}^{MLMF} = \sum_{\ell=0}^L \frac{1}{N_\ell} \sum_{i=1}^{N_\ell} Y_\ell^{HF,(i)} 
                         + \alpha_\ell \left( \sum_{i=1}^{N_\ell} Y_\ell^{LF,(i)} - \frac{1}{r_\ell} \sum_{i=1}^{r_\ell N_\ell} Y_\ell^{LF,(i)} \right).
```
Level-by-level the control variate is applied, as explained in the
previous sections, with the only difference that this is used between
the discrepancies of the high- and low-fidelity model, *i.e.*
$`Y_\ell^{HF}`$ and $`Y_\ell^{LF}`$.

The variance of this estimator is
```math
{\mathbb{V}ar\left[ \hat{Q}^{MLMF} \right]} = \sum_{l=0}^{L} \left( \dfrac{1}{N_\ell} {\mathbb{V}ar\left[Y_\ell^{HF}\right]} \left( 1 - \frac{r_\ell-1}{r_\ell} \rho_\ell^2  \right) \right),
```
which, due to the independent sampling on each level, corresponds to the
sum of variances of control variate estimators.

The sample allocation problem is a combination of the MLMC allocation
and control variate allocation:
```math
N_{\ell}^{HF} = \frac{1}{\varepsilon^2} \!\! \left[ \, \sum_{k=0}^{L} \left( \frac{{\mathbb{V}ar\left[Y^{HF}_k\right]} \mathcal{C}_{k}^{HF}}{ 1-\rho_k^2}  \right)^{1/2}
 \left(1 - \frac{r_k-1}{r_k} \rho_k^2  \right) \right] \sqrt{ \left( 1 - \rho_\ell^2 \right) \frac{ {\mathbb{V}ar\left[Y^{HF}_\ell\right]} }{\mathcal{C}_{\ell}^{HF} } },
 ```

where the control variate term contributes to reduce the variance, and,
therefore, the number of HF evaluations on each level.
Dakota currently implement the version of this scheme
described in [\[1\]](#references).

# Input Configuration

For the MLMF estimator, we need to combine the two model forms that we
used for the [control variate](../cv) estimator, with the levels definition of
the [MLMC](../mlmc) estimator. The resulting input file is `dakota_MLMF.in`.

If we start from the input file of the control variate estimator,
`dakota_CV.dat`, the differences are in the method specification, in which the keyword `multilevel_multifidelity_sampling` is used, 
and the definition of the model forms, which will need the
levels/discretizations specification:
```
method,
	model_pointer = 'HIERARCH'
    multilevel_multifidelity_sampling
	(...)

model,
	id_model = 'LF'
	variables_pointer = 'LF_VARS'
	simulation
	  solution_level_control = 'N_x'		 
	  solution_level_cost = 15. 45. 90. 180.
	  
model,
	id_model = 'HF'
	variables_pointer = 'HF_VARS'
	simulation
	  solution_level_control = 'N_x'
          solution_level_cost = 630. 1260. 2100. 4200.	  
```

The `LF` and `HF` blocks include specifications of the low- and high-fidelity,
respectively. Here, the levels are defined in term of spatial cells and the associated costs are specified.

Additionally, there are separate variables blocks for the low- and high-fidelity models. Even in this case, each
block is equivalent to the corresponding one in MLMC.

```
variables,
	id_variables = 'LF_VARS'
	uniform_uncertain = 7
	  lower_bounds    = 7*-1.
	  upper_bounds    = 7* 1.
	discrete_state_set
	  integer = 2
	    num_set_values = 4 1
	    set_values = 5 15 30 60 # number of spatial coords
	    	       	 3 	    # number of Fourier solution modes
	    initial_state = 5 3
	    descriptors 'N_x' 'N_mod'
	    
variables,
	id_variables = 'HF_VARS'
	uniform_uncertain = 7
	  lower_bounds    = 7*-1.
	  upper_bounds    = 7* 1.
	discrete_state_set
	  integer = 2
	    num_set_values = 4 1
	    set_values = 30 60 100 200 # number of spatial coords
	    	       	 21  # number of Fourier solution modes
	    initial_state = 30 21
	    descriptors 'N_x' 'N_mod'	
```

In the case of the MLMF estimator, Dakota uses the
relative `convergence_tolerance` as in the case of MLMC, which corresponds 
to a relative variance reduction computed from the corresponding MLMC variance after the pilot
sampling. It is important to note that the presence of the low-fidelity
evaluations is not accounted in the evaluation of the convergence
criterion for the estimator, which only based on the MLMC for the
high-fidelity model form.

In order to make the sample allocation problem more interesting, we
select 20 samples per level and, to maintain the same accuracy level of
the previous MLMC case, we use 0.002 for `convergence_tolerance`.

# PostProcessing Phase

The MLMF study can be executed with:\
`dakota -i dakota_MLMF.in -o dakota_MLMF.out`.

The method starts with the pilot samples for both model fidelities and
for all levels:

```
Multilevel-multifidelity pilot sample:
                                    20
                                    20
```
In this case, by using 20 samples per levels, this first step requires a
total of 20+40+40+40 model evaluations for each model form, for a total
of 280 evaluations.

After this step, Dakota considers a control variate on
each level and evaluates the optimal oversampling ratio for the
low-fidelity model:

```
VMC LF sample increment = 613

NonD random Samples = 613 Seed not reset from previous LHS execution

No CVMC LF sample increment

CVMC LF sample increment = 7

NonD random Samples = 7 Seed not reset from previous LHS execution

CVMC LF sample increment = 7

NonD random Samples = 7 Seed not reset from previous LHS execution
```


In this case, the algorithm allocates a total of 613 samples at the
coarsest level $`\ell=0`$, 7 for $`\ell=2`$ and 7 for $`\ell=3`$. No samples
are allocated for the low-fidelity, at this step, on the level $`\ell=1`$
due to a low estimated correlation.

Once all the additional low-fidelity evaluations are computed, the MLMC
step is performed. This case only requires a single level sample
iteration:
```
MLCVMC iteration 1 sample increments:
                                   723
                                     0
                                     0
                                     0
```

However, a final control variate step is needed to finalize this
iteration, which requires low-fidelity evaluations only, for a total of 34699
evaluations:
```
CVMC LF sample increment = 34699
```

Finally, before reporting the final statistics,
Dakota reports the correlation and the control variate
data for each level (and for the first four moments). For instance, for
the first level we observe a correlation of 0.991:

```
rho_LH (Pearson correlation) for QoI 1 = 9.9119944477e-01
Moment 1:
   QoI 1: control variate beta = 1.0478033791e+00
Moment 2:
   QoI 1: control variate beta = 1.1411411782e+00
Moment 3:
   QoI 1: control variate beta = 1.2180765560e+00
Moment 4:
   QoI 1: control variate beta = 1.3026938129e+00
```

The final sample allocation is reported with the total computational
cost, normalized with respect to the cost of a single high-fidelity
simulation:

```
<<<<< Final samples per model form:
      Model Form 1:
                                 36055
                                    20
                                    27
                                    27
      Model Form 2:
                                   743
                                    20
                                    20
                                    20
<<<<< Equivalent number of high fidelity evaluations: 2.9810714286e+02
```

The total cost, of approximately 298 high-fidelity simulation, is
approximately one order of magnitude less than the MLMC cost (see the
result of the previous section) for the same accuracy requirement. The
total cost of this estimator is obtained by summing the cost of all the simulations, per
model fidelity and model form.

# Further Reading

* Reference Manual entry for the 
  [multilevel_sampling](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/method-multilevel_sampling.html)
  method and [hierarchical](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/model-surrogate-hierarchical.html)
  surrogate model.
* [User's Manual](https://dakota.sandia.gov/content/manuals) discussion of active variable view in section 9.5.

# References

1. G. Geraci, M.S. Eldred & G. Iaccarino, A multifidelity multilevel Monte Carlo method 
   for uncertainty propagation in aerospace applications. *19th AIAA Non-Deterministic
   Approaches Conference*, 2017.


---

* Return to the [Outline](../README.md#outline)
* Go back to the [previous section](../mlmc) of the tutorial
