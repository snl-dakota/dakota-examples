# Summary

Perform a polynomial chaos expansion (PCE) by fitting to data (as opposed to spectral projection)

 
### Run Dakota

There are three example files:
- `pce_oversampling.in`
- `pce_undersampling.in`
- `pce_oli.in`

Run as follows

    $ dakota -i <dakota-file>.in 
 
 
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

There are **many** methods to build a PCE. In this example, we simply present three methods:

1. Oversample (regression). In this case, we choose an expansion order such that the number of terms is approximately half of the number of data samples. This is chosen by guess-and-check
2. Undersample (compressed sensing). In this example, we apply guess-and-check to determine a basis of about double the number of sample and then choose to adapt the basis and let Dakota decide the optimal basis
3. Exact Sampling(Orthogonal Least Interpolation, OIL) We use `orthogonal_least_interpolation` to build the PCE directly.

The data is the same as from `official/global_sensitivity/surrogate/existing_data/existing_data.dat`

# Additional Input to Dakota

For all three input files, Dakota imports data from the file 
`existing_data.dat`. This file contains evaluations (variables + response) of
the Ishigami test function.

## Analysis Driver

We do not need one except to be syntactically correct since we are using existing 
data. The data were generated using the Ishigami function.

### Inputs

The Ishigami takes three variables, which for this example were
uniformly distributed in $[-\pi,\pi]^3$

```dakota
	uniform_uncertain =  3
	lower_bounds    =    -3.14159 -3.14159 -3.14159    
	upper_bounds    =    +3.14159 +3.14159 +3.14159    
	descriptors     =    'x'      'y'      'z'
```

### Outputs

The Ishigami driver has one output.

# Interpret the results

## Screen Output

### Oversampling
```
Local sensitivities for each response function evaluated at uncertain variable means:
Ishigami:
 [  2.8007066059e+00  7.7901828436e-01 -1.2006125890e+00 ] 

Global sensitivity indices for each response function:
Ishigami Sobol' indices:
                                  Main             Total
                      4.6252824047e-01  6.3538389818e-01 x
                      3.4017883952e-02  4.5187966064e-01 y
                      7.8132817774e-02  4.4863050116e-01 z
                           Interaction
                      5.4823374420e-02 x y 
                      7.4592811125e-03 x z 
                      2.5246540009e-01 y z 
                      1.1057300218e-01 x y z 
```
### Undersampling
```
Local sensitivities for each response function evaluated at uncertain variable means:
Ishigami:
 [  8.9355346991e-01  6.3716434730e-02 -3.7933005039e-01 ] 

Global sensitivity indices for each response function:
Ishigami Sobol' indices:
                                  Main             Total
                      3.4340798604e-01  5.4661462270e-01 x
                      4.4581083487e-01  4.5514273448e-01 y
                      8.3213851759e-04  2.1050280112e-01 z
                           Interaction
                      2.7837796122e-04 x y 
                      2.0061714096e-01 x z 
                      6.7424039128e-03 y z 
                      2.3111177353e-03 x y z 
```
### Exact Sampling
```
Local sensitivities for each response function evaluated at uncertain variable means:
Ishigami:
 [  1.2814475690e+00  4.3287767938e+00  3.2555616069e-01 ] 

Global sensitivity indices for each response function:
Ishigami Sobol' indices:
                                  Main             Total
                      6.2174913365e-02  5.5462644727e-01 x
                      1.1285856005e-01  6.5708956509e-01 y
                      1.7010857056e-01  7.4310005461e-01 z
                           Interaction
                      8.1866471977e-02 x y 
                      1.1062695099e-01 x z 
                      1.6240642212e-01 y z 
                      2.9995811094e-01 x y z 
```


