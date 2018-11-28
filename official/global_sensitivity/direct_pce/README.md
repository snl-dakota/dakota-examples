# Summary

Apply quadrature-based Polynomial Chaos expansions for global sensitivity and (some) general UQ
 
### Run Dakota

    $ dakota -i direc_pce.in -o direct_pce.out
 
### More about running this example

Python is required to run this example.
 
# What problem does this solve?

Variance-based decomposition (VBD) attributes fractions of response variance to variables so that
the most important variables can be identified. Polynomial chaos produces the *main effect*,
*interaction effects*, and *total effect* of each variable. These are also called the Sobol' indices.
The main effect is the fraction of the response variance that can be attributed to a variable acting
on its own. The interaction effects include the influence of the variable in combination with other
variables. The total effect is the variable's main effect, plus the summed effects of all its 
interactions.
 
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

and the interation between $`x_i`$ and $`x_j`$ are defined as

$`S_{i,j} = \frac {
        \mathbb{V} \left( \mathbb{E} ( f|x_i, x_j ) \right) - S_i - S_j
    }{
        \mathbb{V}(f)
    }
`$

where $`x_{\sim i}`$ is all variables *but* $`x_i`$

# What method will we use?

Polynomial Chaos Expansion (PCE) methods are ideally suited for smooth responses. A direct quadrature-based method (as opposed to sparse grids) are ideal for low-dimension and/or low-order approximations.

PCEs are particularly well suited for global sensitivity analysis since they do not require resampling and also provide immediate access to *explicit* interactions
 
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

The output (redirected to the file `direct_pce.out` is as follows:

```
Local sensitivities for each response function evaluated at uncertain variable means:
Ishigami:
 [  9.9999724630e-01  1.8104711070e-16 -5.5065304221e-16 ]

Global sensitivity indices for each response function:
Ishigami Sobol' indices:
                                  Main             Total
                      3.1402935786e-01  5.5780885341e-01 x
                      4.4219114659e-01  4.4219114659e-01 y
                      2.7230302032e-30  2.4377949556e-01 z
                           Interaction
                      1.8693507016e-30 x y
                      2.4377949556e-01 x z
                      9.8240433823e-31 y z
                      6.3759218235e-31 x y z
```
From these results, we may make the following observations:

- All three variables have significant total effects on the response.
- About 31% of the response variance can be attributed to x alone (x's main effect).
  The interaction between x and z also makes a significant contribution, about 24%.
- The main and total effects of y are identical, indicating that it does not have 
   any interactions with other variables. It can be seen that its interaction effects
   with the other variables are negligible.
- The main effect of z is neglible; it influences the response only via its interactions 
  with x.

In addition to the console output, samples on the PCE are written to the file 
`pce_samples.dat`.
