# Global Sensitivity Analysis

Global Sensitivity Analysis is activated via the keyword `variance_based_decomp` in the respective method. The two main methods in Dakota to assess global sensitivity analysis via the variance are with sampling or with PCEs. Sampling requires *many* more samples to assess the sensitivity so it is almost always best done with a surrogate. PCEs can be built in numerous ways either from existing data or by directly choosing the evaluation points.

## Test Function 

For all of these examples, we will use the so-called Ishigami Function:

```
f(x,y,z) = sin(x) + a*sin^2(y) + b*z**4*sin(x)
```

with `a = 7` and `b = 0.1` on `[-pi,pi]^3`

The Sobol Index can be solved analytically in terms of `a`, and `b` as presented below:


| Index | Analytical Form                                                                      | `a = 7` & `b = 0.1` |
|-------|--------------------------------------------------------------------------------------|---------------------|
| Sx    | `(pi^8*b^2/50 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2)`              | 0.313905191147811   |
| Sy    | `a^2/(8*(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2))`                                     | 0.442411144790041   |
| Sz    | `0`                                                                                  | 0                   |
|       |                                                                                      |                     |
| Tx    | `-a^2/(8*(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2)) + 1`                                | 0.557588855209959   |
| Ty    | `-(pi^8*b^2/18 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2) + 1`         | 0.442411144790041   |
| Tz    | `-(a^2/8 + pi^8*b^2/50 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2) + 1` | 0.243683664062148   |

Or, in terms of contribution to the variance:


| Index | Analytical Form                                                                 | `a = 7` & `b = 0.1` |
|-------|---------------------------------------------------------------------------------|---------------------|
| x     | `(pi**8*b**2/50 + pi**4*b/5 + 1/2)/(a**2/8 + pi**8*b**2/18 + pi**4*b/5 + 1/2))` | 0.313905191147811   |
| y     | `a**2/(8*(a**2/8 + pi**8*b**2/18 + pi**4*b/5 + 1/2)))                         ` | 0.442411144790041   |
| z     | `0                                                                            ` | 0                   |
| xy    | `0                                                                            ` | 0                   |
| yz    | `0                                                                            ` | 0                   |
| zx    | `8*pi**8*b**2/(225*(a**2/8 + pi**8*b**2/18 + pi**4*b/5 + 1/2)))               ` | 0.243683664062148   |
| xyz   | `0                                                                            ` | 0                   |

Or, as Dakota would format it (if calculated analytically):


```
                                  Main             Total
                      3.1390519115e-01  5.5758885521e-01 x
                      4.4241114480e-01  4.4241114480e-01 y
                      0.0000000000e-00  2.4368366406e-01 z
                           Interaction
                      0.0000000000e-00 x y
                      2.4377949556e-01 x z
                      0.0000000000e-00 y z
                      0.0000000000e-00 x y z
```

### Run Dakota
   
See each sub example

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

Each sub example uses a different method. See each example separately
 
## Analysis Driver

### Inputs

### Outputs
 
# Interpret the results
 







