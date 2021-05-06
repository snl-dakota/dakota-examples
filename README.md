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

### Access

If you are internal to Sandia, we recommend accessing the Library directly on
gitlab-ex. (https://gitlab-ex.sandia.gov/dakota/dakota-examples). Library content has
been tailored to render correctly there, and any additions or changes we make to examples
will be available immediately. On Gitlab, we recommend browsing the folder
structure or using search to find what you are looking for.

Outside of Sandia, the Library currently is available only in Dakota source and binary
packages [on our website](https://dakota.sandia.gov/download.html). In source
packages, it is located in the `dakota-examples` folder. In binary packages, it is
locatedin `share/dakota/examples/official`. We plan to mirror the repository externally
in the very near future; to be notified, email dakota-announce@software.sandia.gov
and ask to be subscribed.

The Dakota GUI also is a convenient and powerful way to view and find examples. It
includes a text-based search interface to quickly search for examples.

### Organization

Examples are organized topically in a hierarchy of folders. Each example (and in some
cases collection of examples) has a README, which is in markdown format.
This document includes a description of the example and other details, such as how to
run or use the example yourself.

Examples in the [official](./official) folder were created or reviewd by Dakota project
team members and are tested. [contributed](./contributed) examples are those we believe
may be useful but have received a lower level of vetting.

(Some of the other folders you may encounter, such as `cmake`, handle testing
and packaging and can be disregarded if you aren't a Dakota developer.)

## Contributing Dakota Examples

If you've created an example that you feel may be of value to others, we invite you
to submit it for inclusion in the Library. Please contact the user support mailing
list, dakota-users@software.sandia.gov.

