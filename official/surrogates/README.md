# Summary

Build and use data-fit surrogates

# Description

In Dakota, a *surrogate model* is a computationally inexpensive approximation
that is used in place of a computational simulation. Most commonly,
surrogates are used because of the high computational cost of a simulation.
Surrogates may also be used to smooth or fill in poorly behaved responses.

Dakota includes several types of surrogate models, such as polynomials, neural
networks, gaussian processes, and others. In all cases, Dakota constructs 
surrogates by fitting to training data. The data may be imported, or Dakota may 
collect it via an interface to the user's simulation. Any of Dakota's suite
of methods can by applied to a surrogate model.

This example demonstrates a few basic ways of constructing and using surrogate
models. It has four parts.

The first two parts feature Dakota studies that use surrogate models. One
demonstrates how to set up Dakota to collect training data from a simulation,
and the other shows Dakota importing training data.

The third part shows how to use the `surfpack` command line application in 
concert with Dakota. Dakota can build and export `surfpack` surrogates, which 
the application can evaluate.

In the fourth part, we demonstrate Dakota's new surrogate library. Work is 
ongoing to re-implement Dakota's surrogate models in a stand-online library 
that can be conveniently used by Dakota or outside of Dakota via a Python API.

## Table of Contents
* [Construct a surrogate from collected data](dace/)
* [Construct a surrogate from imported data](imported/)
* [Use the `surfpack` command line application](surfpack/)
* [Use Dakota's surrogate library](library/)

