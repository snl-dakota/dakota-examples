# Basic Field Calibration Terms

If you have not already done so, you may wish to read the introduction to this collection of examples that is one directory level up. It describes the calibration problem that is being solved.

This example demonstrates basic usage of Dakota’s field calibration term feature. Any Dakota study that has been created using scalar calibration terms can be converted into a study that uses field terms instead. Field calibration terms offer a couple of additional capabilities compared to scalar terms.

The first is that richer uncertainty information can be specified for field terms. Instead of point-wise variance, an entire covariance matrix that expresses the relationship between points in the field may be provided to Dakota.

Second, when field calibration terms are used, Dakota can interpolate between experimental data and simulation predictions. Currently, this feature is limited to linear interpolation on a single coordinate.

In addition, some users may find the way that experimental data is provided to Dakota for field calibration terms more convenient than for scalar terms.

In this example, two experiments were performed at different load configurations. The loads are provided as configuration variables, and uncertainty is provided to Dakota as well. Users may wish to compare this example to the `scalar_multiexperiment_config` example, in which exactly the same calibration problem is posed using scalar calibration terms. That example also contains discussion of calibration variables.

Note the presence of several files in addition to the Dakota input file (`dakota_cal.in`):
* *`displacement.1.dat` and `displacement.2.dat`.* These files contain the experimentally measured displacements. The indexes 1 and 2 are for the experiment number, and the name of the file matches the descriptor of the field calibration term in the Dakota input file.
* *`displacement.1.sigma` and `displacement.2.sigma`.* This pair of files contains the uncertainty information for this field response for the two experiments.
* *`experiment.1.config` and `experiment.2.config`.* These contain the values of the configuration variables. Unlike the measurement and uncertainty files, these files are not named for specific field calibration term descriptors. This is because multiple field responses may be measured in a single experiment.

Next, examine the responses section of the Dakota input file (`dakota_cal.in`).

There is a single field calibration term, so the `calibration_terms` keyword has an argument of 1. Because it’s a field term, the `field_calibration_terms` keyword is also present and has an argument of 1. (Dakota permits a combination of scalar and field terms in a single study. To maintain backward compatibility, all the calibration terms are assumed to be scalar in the absence of the `field_calibration_terms` keyword.) The length of the terms (the number of predictions that the analysis driver will return) is specified using the `lengths` keyword.

The `calibration_data` keyword group tells Dakota to expect the group of files described above. We have two experiments, one configuration variable, and scalar uncertainty information.

To run the example, first make sure Dakota is on your `PATH` and that the `share/dakota/Python` folder in your Dakota installation is on your `PYTHONPATH`. Then run,

`dakota -i dakota_cal.in`


