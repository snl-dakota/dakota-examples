# Summary

Use random sampling to perform variance-based decomposition for sensitivity analysis

### Run Dakota

run:

    $ dakota -i direct_sample.in -o direct_sample.out
    
### More about running this example

Python is required to run this example.

# What problem does this solve?

Variance-based decomposition (VBD) attributes fractions of response variance to variables so that
the most important variables can be identified. Sampling-baesd VBD results in the *main effect* and
*total effect* of each variable. These are also called the Sobol' indices. The main effect is the
the fraction of the response variance that can be attributed to a variable acting on its own. A
variable's total effect is its main effect, plus the summed effects of all its interactions with
other variables. The interation effects are not computed by sampling-based VBD, but they can 
be obtained using polynomial choas.
 
## Math Equation

The "main" sensitivity of a variable $`x_i`$ is

$`S_i = \frac {
        \mathbb{V} \left( \mathbb{E} ( f|x_i ) \right)
    }{
        \mathbb{V}(f)
    }
`$

The "total" sensitivity is

$`T_i = \frac { \mathbb{E} \left( \mathbb{V}(Y|x_{\sim i})  \right)
              } {
                  \mathbb{V}(Y)
              }
`$

where $`x_{\sim i}`$ is all variables *but* $`x_i`$

# What method will we use?

We use the `sampling` method with the `variance_based_decomp` flag. 

**WARNING**: Unlike some other methods such as Polynomial Chaos, sampling-based VBD 
requires a very large number of samples; typically hundreds per variable.

Dakota automatically multiples the number of `samples` requested by the user by $`(M+2)`$, where $`M`$
is the number of variables. In this example, which has three variables and 1000 samples, the driver 
will be called 5000 times.
 
## Analysis Driver

In this example, we do a `fork` with the included Python `Ishigami.py` function

The analytical answers are:

| Index | Analytical Form                                                                        | $`a = 7`$ & $`b = 0.1`$ |
|-------|----------------------------------------------------------------------------------------|-------------------------|
| Sx    | $`(pi^8*b^2/50 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2)`$              | 0.313905191147811       |
| Sy    | $`a^2/(8*(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2))`$                                     | 0.442411144790041       |
| Sz    | $`0`$                                                                                  | 0                       |
|       |                                                                                        |                         |
| Tx    | $`-a^2/(8*(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2)) + 1`$                                | 0.557588855209959       |
| Ty    | $`-(pi^8*b^2/18 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2) + 1`$         | 0.442411144790041       |
| Tz    | $`-(a^2/8 + pi^8*b^2/50 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2) + 1`$ | 0.243683664062148       |


### Inputs

The Ishigami takes three variables, which in this example are uniformly
distributed in $[-\pi,\pi]^3$

```dakota
	uniform_uncertain =  3
	lower_bounds    =    -3.14159 -3.14159 -3.14159    
	upper_bounds    =    +3.14159 +3.14159 +3.14159    
	descriptors     =    'x'      'y'      'z'
```

### Outputs
 The Ishigami driver has one output.

# Interpret the results
## Screen Outputs

The output (redirected to the file `direct_sample.out` is as follows:

```

                                  Main             Total
                      3.6442176674e-01  6.4970249569e-01 x
                      4.4188053874e-01  4.5552696765e-01 y
                      3.2470524558e-02  2.4838191925e-01 z
```                      
Note that this is both less correct and noisier than that from a polynomial chaos 
expansion (see the `direct_pce` and `pce_on_data` examples).
