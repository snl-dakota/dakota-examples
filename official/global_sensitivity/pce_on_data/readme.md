# PCE on data

In other sections, we demonstrate building a surrogate and then creating a PCE on the surrogate.

In this section, we instead attempt to approximate a PCE directly from existing data. This differs from other PCE methods since Dakota does *not* get to choose the location of the samples and instead relies entirely on existing data

## Methods

There are **many** methods to build a PCE. In this example, we simply present three methods:

1. Undersample (regression). In this case, we choose an expansion order such that the number of terms is approximately half of the number of data samples. This is chosen by guess-and-check
2. Oversample (compressed sensing). In this example, we apply guess-and-check to determine a basis of about double the number of sample and then choose to adapt the basis and let Dakota decide the optimal basis
3. Exact Sampling(Orthogonal Least Interpolation, OIL) We use `orthogonal_least_interpolation` to build the PCE directly.

The data is the same as from `official/global_sensitivity/surrogate/existing_data/existing_data.dat`

## Results

- [ ] Come back and document results
