# Direct Sampling

Global Sensitivity can be assessed via direct Monte-Carlo sampling however, this is *very expensive* to do. For example, using `N` samples in `ndim` dimensions actually require `N*(2*ndim-1)` (though for 2D, this may be reduced). For this example with 1000 samples in 3 dimensions, the actual function is called 5000 times.

See other examples for ways to use surrogates or PCEs to drastically improve performance.

The results of the global sensitivity with 1000 (really 5000) samples are:

```
Global sensitivity indices for each response function:
Ishigami Sobol' indices:
                                  Main             Total
                      3.6442176674e-01  6.4970249569e-01 x
                      4.4188053874e-01  4.5552696765e-01 y
                      3.2470524558e-02  2.4838191925e-01 z
```

