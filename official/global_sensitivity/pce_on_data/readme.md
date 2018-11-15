# Summary

Perform a polynomial chaos expansion (PCE) directly on data via fitting to the data (as opposed to quadrature

 
### Run Dakota

There are numerous example files. Run as follows

    $ dakota -i <dakota-file>.in 
 
 
# What problem does this solve?

Use global sensitivity analysis to return the Sobol indices of the function. This assumes there is already existing data
 
 
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

There are **many** methods to build a PCE. In this example, we simply present three methods:

1. Undersample (regression). In this case, we choose an expansion order such that the number of terms is approximately half of the number of data samples. This is chosen by guess-and-check
2. Oversample (compressed sensing). In this example, we apply guess-and-check to determine a basis of about double the number of sample and then choose to adapt the basis and let Dakota decide the optimal basis
3. Exact Sampling(Orthogonal Least Interpolation, OIL) We use `orthogonal_least_interpolation` to build the PCE directly.

The data is the same as from `official/global_sensitivity/surrogate/existing_data/existing_data.dat`


## Analysis Driver

We do not need one except to be syntactically correct since we are using existing data

### Inputs

The Ishigami takes three uniform variables in $[-\pi,\pi]^3$

```dakota
	uniform_uncertain =  3
	lower_bounds    =    -3.14159 -3.14159 -3.14159    
	upper_bounds    =    +3.14159 +3.14159 +3.14159    
	descriptors     =    'x'      'y'      'z'
```

### Outputs
 
# Interpret the results
 
## Screen Output
_Insert image of screen output:_

---

![Screen Output](DAKOTA_Arrow_Name_horiz.jpg)
 
_Explain the relevance of the image._
 
---

_Insert image of other images (plots, etc.):_

![Other images](DAKOTA_Arrow_Name_horiz.jpg)
 
_Explain the relevance of the image._

---
