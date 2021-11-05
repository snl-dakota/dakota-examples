# Summary

Perform uncertainty quantification and global sensitivity analysis using polynomial chaos expansions constructed from sparse grids.

# Description

In this example, Dakota is used to

1. compute Sobol indices, a measure of global sensitivity,
2. compute statistical moments,
3. compute the probability density function (PDF), and
4. compute the complementary cumulative distribution function (CCDF)

for the Ishigami problem using polynomial chaos.  A polynomial chaos expansion (PCE) is used to approximate the Ishigami function and is constructed from sparse grids (specified by `sparse_grid_level = 3`).  Sparse grids can require fewer function evaluations than quadrature to construct the PCE and are particularly attractive for problems with larger numbers of parameters.  Sobol indices (specified by `variance_based_decomp`) and statistical moments are computed analytically from the PCE.  Sampling on the PCE (specified by `samples_on_emulator = 10000`) is used to compute the PDF and the CCDF.

# How to run the example

This example can be run using Dakota's command-line interface.  More specifically,

     $ dakota -i dakota_pce_sparse_grid.in -o dakota_pce_sparse_grid.out

All output can be found in `dakota_pce_sparse_grid.out`.

# Requirements

python3 is needed to run this example.

# Contents

* `dakota_pce_sparse_grid.in`: Dakota input file for performing uncertainty quantification using polynomial chaos expansions constructed using sparse grids
* `Ishigami.py`: Python implementation of the Ishigami function, a common test problem for uuncertainty quantification methods

# Further Reading

More information can be found in Chapter 5.4 of the Dakota User's Manual.  Theoretical foundations can be found in Chapter 3 of the Dakota Theory Manual.  Both can be found at https://dakota.sandia.gov/content/manuals.
