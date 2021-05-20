# Summary

Understand how Multilevel Monte Carlo (MLMC) can compute statistics with greater precision and lower cost than orindary Monte Carlo and learn how to configure a Dakota study to use this approach

# Description

This example is part of a longer tutorial that covers Dakota's multilevel and multifidelity sampling approaches. The top-level page, which provides an outline and describes the test problem used throughout the tutorial, is [here](../README.md). In this section, Multilevel Monte Carlo (MLMC) sampling is used to estimate the expectation (mean) of a model QoI. Comparison is made to results obtained using plain [Monte Carlo](../mc).

At the end of this section, the user should understand the basic theory that underlies MLMC, and undestand how to configure a Dakota study to use this approach.

# Theory Highlights

Multilevel MC (MLMC) is an estimator that is built by expanding the
expected value operator, applied to the QoI, over a set of levels:

```math
{\mathbb{E}\left[Q\right]} = {\mathbb{E}\left[Q_0\right]} + \sum_{\ell=1}^L {\mathbb{E}\left[ Q_\ell - Q_{\ell-1} \right]}.
```

If we define
$`Y_\ell = Q_{\ell} - Q_{\ell-1}`$, for $`\ell=1,\dots,L`$ and
$`Y_0 = Q_0`$, we can write the expected value of the quantity of interest
as a sum of discrepancy $`Y_\ell`$ contributions. Each of this discrepancy
contribution terms can then be evaluated with an independent number of
samples to obtain the MLMC estimator:
```math
{\mathbb{E}\left[Q\right]} \approx \hat{Q}^{MLMC} = \sum_{\ell=0}^L \frac{1}{N_\ell} \sum_{i=1}^{N_\ell} Y_\ell^{(i)}.
```

Each level is handled independently with $`N_\ell`$ samples, which means
that for $`Y_\ell \rightarrow 0`$,
$`{\mathbb{V}ar\left[Y_\ell\right]} \rightarrow 0`$ and, therefore, the
amount of work needed at higher levels, *i.e.* number of samples
$`N_\ell`$, decreases with $`\ell`$.

Multilevel MC (MLMC) is a particular multifidelity estimator that has a
main distinctive feature compared to a multifidelity MC: it does not
require the estimation of the coefficient $`\alpha`$, which is assumed to
be always equal to $`-1`$ (see [\[1\]](#references) for more details regarding
the comparison of MLMC and control variate based approaches). This
assumption also simplify the optimization problem that allocates
resources on each level to reach a prescribed accuracy target
$`\varepsilon^2`$. The number of realizations $`N_\ell`$ is obtained as
```math
N_\ell = \frac{ \sum\limits_{k=0}^L \sqrt{ \left( {\mathbb{V}ar\left[Y_k\right]} \mathcal{C}_k \right)^{1/2} }  }{\varepsilon^2} \frac{ {\mathbb{V}ar\left[Y_\ell\right]} }{ \mathcal{C}_\ell },
```
which requires an estimation of $`{\mathbb{V}ar\left[Y_\ell\right]}`$
on each level.

More information about MLMC can be found in the comprehensive review [\[2\]](#references)
from Mike Giles, who introduced the MLMC estimator in the
seminal paper [\[3\]](#references).

# Input Configuration

In this case, we want to configure a MLMC study that uses all the
available levels of the HF model, which is all the models that use $`21`$
modes and a spatial resolution
$`N_x = \left\{ 30, 60, 100, 200 \right\}`$ (see also the Table at the end of the [problem description](../README.md#test-problem-description)). The total cost is, as for the
previous case, defined as $`N_x \times N_{mod}`$.

For the configuration of a MLMC study, we only need minimal
modifications with respect to the control variate case. The input file
is located under `dakota_MLMC.in` and the
important modifications, with respect to the [control variate](../cv) case, are
the following:

First, consider the `method` block:
```
method,
	model_pointer = 'HIERARCH'
        multilevel_sampling				
	  pilot_samples = 10 seed_sequence = 1237
	  max_iterations = 5
	  convergence_tolerance = 0.001
	output silent
```

The `method` is configured to use $`10`$ pilot samples per level, which means that each discrepancy
level ($`Y_\ell = Q_\ell - Q_{\ell-1}`$, for $`\ell`$) is evaluated 10
times. In our case we have 4 levels and therefore the total number
of model evaluations corresponding to the pilot phase is
$`10 + 20 + 20 + 20 = 70`$. Also, we are using a smaller `convergence_tolerance`, $`\tau_{target}`$,
in order to demonstrate a sample allocation over multiple levels. In the MLMC, the target tolerance
is evaluated with respect to the variance of the multilevel estimator with only the pilot samples,
*i.e.*
```math
      \varepsilon_{target}^2 = {\mathbb{V}ar\left[\hat{Q}^{MLMC}_{pilot}\right]} \times \tau_{target} = \left( \sum_{\ell=0}^L \frac{{\mathbb{V}ar\left[Y_\ell\right]}}{N_\ell^{pilot}} \right) \times \tau_{target} \\
        =  \left( \sum_{\ell=0}^L \frac{{\mathbb{V}ar\left[Y_\ell\right]}}{10} \right) \times 0.001.
```
Unlike the CVMC case, where we defined low- and high-fidelity models, we only need
to use a single fidelity model (HF) because we will change the
spatial resolution only. The cost for the four levels is added using the `solution_level_cost`
keyword.
```
model,
	id_model = 'HIERARCH'
	variables_pointer = 'HF_VARS'
	surrogate hierarchical
	  ordered_model_fidelities = 'HF'	
	  
model,
	id_model = 'HF'
	variables_pointer = 'HF_VARS'
	simulation
	  solution_level_control = 'N_x'
          solution_level_cost = 630. 1260. 2100. 4200.
```
The `solution_level_control` sets the name of the Dakota variable, `N_x`, that
is used to control the model level. `N_x` is one of the
state variables specified in the `variables` block:
```
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
The first four `set_values` for the `discrete_state_set` variables
define the four levels of `N_x`, beginning with the coarsest.

# PostProcessing Phase

The MLMC study can be executed with:\
`dakota -i dakota_MLMC.in -o dakota_MLMC.out`.

Dakota execution starts with scheduling the pilot runs:
```
Multilevel pilot sample:
                                    10
                                    10
                                    10
                                    10
```

Afterwards, the relative tolerance is computed:
```math
\left( \frac{{\mathbb{V}ar\left[Y_0\right]}}{10} + \frac{{\mathbb{V}ar\left[Y_1\right]}}{10} + \frac{{\mathbb{V}ar\left[Y_2\right]}}{10} + \frac{{\mathbb{V}ar\left[Y_3\right]}}{10} \right) \times \tau_{target} = 639.25 \times 0.001 = 0.63925 
      = \varepsilon^2_{target}
```
The optimal sample profile is now evaluated as
```math
N_\ell = \frac{ \sum_{k=0}^3 \sqrt{ {\mathbb{V}ar\left[Y_k\right]} \mathcal{C}_k } }{ \varepsilon^2_{target} } \sqrt{ \frac{{\mathbb{V}ar\left[Y_\ell\right]}}{\mathcal{C}_\ell} },
```
which in this case leads to $`N_\ell = \left[ 10181, 27, 11, 4 \right]`$.
The increment of additional samples is evaluated by subtracting, from
the optimal allocation, the samples already included in the pilot
samples:
```math
\Delta N_\ell = \left[ 10171, 17, 1, 0 \right],
```

Dakota starts with scheduling the pilot runs:
```
MLMC iteration 1 sample increments:
                                 10171
                                    17
                                     1
                                     0
```

The interested reader can verify this step by manually post-processing
the data included in `dakota_model_eval_it0.dat`. This dataset includes all the model
evaluations written by Dakota in `dakota_MLMC.dat` and
re-ordered here for convenience.

This process is repeated until either the increment is zero (no
additional simulations are required) or the max number of iterations
`max_iterations` is reached.

In this case, the process converges after two samples increments and the
final samples profile is reported with an estimation of the total
number of equivalent HF runs: 
```
<<<<< Function evaluation summary: 18461 total (18461 new, 0 duplicate)
<<<<< Final samples per level:
                                 18295
                                    59
                                    14
                                    10
<<<<< Equivalent number of high fidelity evaluations: 2.7970000000e+03
```
It is important to note here that the total number of simulations is
expressed as the total computational cost, divided the cost of a single
execution at the highest level:
```math
\left( 18295 \times 630 + 59 \times ( 1260+430 ) + 14 \times ( 2100+1260 ) + 10 \times ( 4200 + 2100 ) \right) / 4200 = 2797.
```

# Further Reading

* Reference Manual entry for the 
  [multilevel_sampling](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/method-multilevel_sampling.html)
  method and [hierarchical](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/model-surrogate-hierarchical.html)
  surrogate model.
* [User's Manual](https://dakota.sandia.gov/content/manuals) discussion of active variable view in section 9.5.

# References

1. A.A. Gorodetsky, G. Geraci, M.S. Eldred & J.D. Jakeman, A generalized approximate 
   control variate framework for multifidelity uncertainty quantification. *Journal of Comp Phys*, 408, 2020.
2. M.B. Giles, Multilevel Monte Carlo methods. *Acta Numerica*, 24:259-328, 2015.
3. M.B. Giles, Multi-level Monte Carlo path simulation. *Operations Research*, 56(3):607-617, 2008.


---
* Return to the [Outline](../README.md#outline)
* Continue to the [next section](../mlmf) of the tutorial
* Go back to the [previous section](../cv) of the tutorial
