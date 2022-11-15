# Dakota Examples Library

A collection of official and user-contributed [Dakota](https://dakota.sandia.gov)
examples. The examples help bridge the gap between our
[other documentation](https://dakota.sandia.gov/content/manuals) and practical use.
Types of examples include runnable Dakota studies, drivers to simulation tools 
such as MATLAB and Python, case studies, tutorials, and more.

Tour a few examples:

* Construct a [driver](./official/drivers/) for Dakota to run your simulation;
* Learn about Dakota's new [multilevel and multifidelity](./official/uncertainty_quantification/mlmf/) 
  sampling methods;
* Develop a driver or plot results using the [Dakota GUI](./official/gui);
* Access results and evaluation data in Dakota's [HDF5](./official/hdf5) format output file;
* Calibrate model parameters to [experimental data](./official/deterministic_calibration/)


## How to use the Library

Examples are organized topically in a hierarchy of folders. Each example (and in some
cases collection of examples) has a README, which is in markdown format.
This document includes a description of the example and other details, such as how to
run or use the example yourself.

Examples in the [official](./official) folder were created or reviewd by Dakota project
team members and are tested. [contributed](./contributed) examples are those we believe
may be useful but have received a lower level of vetting.

(Some of the other folders you may encounter, such as `cmake`, handle testing
and packaging and can be disregarded if you aren't a Dakota developer.)

The Dakota GUI also is a convenient and powerful way to view and find examples. It
includes a text-based search interface to quickly search for examples.

## Contributing Dakota Examples

If you've created an example that you feel may be of value to others, we invite you
to submit it for inclusion in the Library. Let us know in the
[Show and Tell](https://github.com/orgs/snl-dakota/discussions/categories/show-and-tell)
discussion. 
