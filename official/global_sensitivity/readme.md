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


## Comparisons


