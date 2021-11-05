# Summary

Perform uncertainty quantification and global sensitivity analysis using polynomial chaos expansions constructed using orthogonal matching pursuit (OMP), a regression-based approach for under-determined systems.

# Description

In this example, Dakota is used to

1. compute Sobol indices, a measure of global sensitivity,
2. compute statistical moments,
3. compute the probability density function (PDF), and
4. compute the cumulative distribution function (CDF)

for the Ishigami problem using polynomial chaos.  A fourth-order polynomial chaos expansion (PCE) is used to approximate the Ishigami function using a regression-based approach (specified by `expansion_order = 4`).  In this case, the regression is under determined (specified by `collocation_ratio = 0.7`), so orthogonal matching pursuit (specified by `omp`) is used to construct the PCE.  Sobol indices (specified by `variance_based_decomp`) and statistical moments are computed analytically from the PCE.  Sampling on the PCE (specified by `samples_on_emulator = 10000`) is used to compute the PDF and the CDF.

# How to run the example

This example can be run using Dakota's command-line interface.  More specifically,

     $ dakota -i dakota_pce_omp.in -o dakota_pce_omp.out

All output can be found in `dakota_pce_omp.out`.

# Requirements

python3 is needed to run this example.

# Contents

* `dakota_pce_omp.in`: Dakota input file for performing uncertainty quantification using polynomial chaos expansions constructed using orthogonal matching pursuit (under-determined regression)
* `Ishigami.py`: Python implementation of the Ishigami function, a common test problem for uuncertainty quantification methods

# Further Reading

Theoretical foundations can be found in Chapter 3 of the Dakota Theory Manual, which can be found at https://dakota.sandia.gov/content/manuals.