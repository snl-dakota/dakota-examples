# Summary

Global Sensitivity can be assessed via direct Monte-Carlo sampling however, this is *very expensive* to do. For example, using `N` samples in `ndim` dimensions actually require `N*(2*ndim-1)` (though for 2D, this may be reduced). For this example with 1000 samples in 3 dimensions, the actual function is called 5000 times.

See other examples for ways to use surrogates or PCEs to drastically improve performance.
 
### Run Dakota

run:

    $ dakota -i direct_sample.in -o direct_sample.out
    
 
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

We use the `sampling` method but with the `variance_based_decomp` flag. **WARNING**: Unlike some other methods such as Polynomial Chaos, this greatly increases the number of sample
 
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
 
The output is as follows:

                                  Main             Total
                      3.6442176674e-01  6.4970249569e-01 x
                      4.4188053874e-01  4.5552696765e-01 y
                      3.2470524558e-02  2.4838191925e-01 z
                      
Note that this is both less correct and noisier than that from a polynomial chaos expansion.
