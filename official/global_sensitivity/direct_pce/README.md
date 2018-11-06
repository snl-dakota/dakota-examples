# Summary

Apply quadrature-based Polynomial Chaos expansions for global sensitivity and (some) general UQ
 
### Run Dakota

    $ dakota -i direc_pce.in -o direct_pce.out
 
### More about running this example

This also puts out `pce_samples.dat`. This is optional but useful later
 
# What problem does this solve?

Use global sensitivity analysis to return the Sobol indices of the function
 
## Math Equation

Without going into too much detail, the "Main" sensitivity of a direction $d$ is

$$ 
S_{\{d}\} = \frac{
        \mathbb{V} \left ( \mathbb{E} (f|x_{\\{d\\}}) \right )
    }{
        \mathbb{V}(f)
    } 
$$

And the "Total" sensitivity is

$$ 
T_{\{d}\} = 1- \frac{
        \mathbb{V} \left ( \mathbb{E} (f|x_{\\{\sim d\\}}) \right )
    }{
        \mathbb{V}(f)
    } 
$$

where $x_{\{\sim d\}}$ is all direction *but* $\\{d\\}$

# What method will we use?

Polynomial Chaos Expansion (PCE) methods are ideally suited for smooth responses. A direct quadrature-based method (as opposed to sparse grids) are ideal for low-dimension and/or low-order approximations.

PCEs are particularly well suited for global sensitivity analysis since they do not require resampling and also provide immediate access to *explicit* interactions
 
## Analysis Driver

In this example, we do a `fork` with the included Python `Ishigami.py` function

The analytical answers are:

| Index | Analytical Form                                                                      | `a = 7` & `b = 0.1` |
|-------|--------------------------------------------------------------------------------------|---------------------|
| Sx    | `(pi^8*b^2/50 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2)`              | 0.313905191147811   |
| Sy    | `a^2/(8*(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2))`                                     | 0.442411144790041   |
| Sz    | `0`                                                                                  | 0                   |
|       |                                                                                      |                     |
| Tx    | `-a^2/(8*(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2)) + 1`                                | 0.557588855209959   |
| Ty    | `-(pi^8*b^2/18 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2) + 1`         | 0.442411144790041   |
| Tz    | `-(a^2/8 + pi^8*b^2/50 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2) + 1` | 0.243683664062148   |


### Inputs

The Ishigami takes three uniform variables in $[-\pi,\pi]^3$

```dakota
	uniform_uncertain =  3
	lower_bounds    =    -3.14159 -3.14159 -3.14159    
	upper_bounds    =    +3.14159 +3.14159 +3.14159    
	descriptors     =    'x'      'y'      'z'
```

### Outputs
 
We are primarily interested in the sensitivity measures. They are presented in the dakota output as follows. Note that this also includes local sensitivity:

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
Please note that values such as `2.7230302032e-30` should be interpreted as zero.
