# Scalar Terms with Configuration Variables

If you have not already done so, you may wish to read the introduction to this collection of examples that is one directory level up. It describes the calibration problem that is being solved.

This example demonstrates the use of configuration variables. A configuration is the set of controlled conditions under which an experiment is performed. For this example, two experiments were conducted. In the first, displacement of the cantilever tip was measured as a function of temperature under the load configuration Y = 400 lb. In the second, the load configuration was changed to Y = 600 lb. These loads are provided to Dakota as configuration variables alongside their associated displacement measurements.

Because the load values are provided to Dakota, Dakota is able to manage running the simulation cantilever.py at the two configurations and differencing with the correct experimental data. Without this feature, the user would need to provide data for both experiments as a single fictitious composite experiment, and then modify cantilever.py to calculate the full set of displacement-vs-temperature predictions at both configurations every evaluation.

To perform an evaluation at a particular configuration, Dakota inserts the value of the configuration variable into the state variable Y. The console output will show Dakota performing an evaluation at a point in parameter space at the first configuration, and then another evaluation at the same point for the second configuration. For example,

```
---------------------
Begin Evaluation    1
---------------------
Parameters for evaluation 1:
                      2.8000000000e+07 E0
                      0.0000000000e+00 Es
                      4.0000000000e+02 Y

blocking fork: python cantilever.py params.in.1 results.out.1

<snip>

---------------------
Begin Evaluation    2
---------------------
Parameters for evaluation 2:
                      2.8000000000e+07 E0
                      0.0000000000e+00 Es
                      6.0000000000e+02 Y

blocking fork: python cantilever.py params.in.2 results.out.2
```

The response block of the input file specifies the number of experiments (`num_experiments`) and the number of configuration variables (`num_config_variables`). The value of the configuration variable is placed in the calibration data file displacements.dat alongside the measurements and uncertainty information. The format of an '`annotated`' calibration data file is explained in the `scalar_multiexperiment_noconfig` example and in the Reference Manual entry for `calibration_data_file`. Briefly, there is one experiment per line, and configuration variable values must be placed before the measurements and variances for each experiment. 

To run the example, first make sure Dakota is on your `PATH` and that the share/dakota/Python folder in your Dakota installation is on your `PYTHONPATH`. Then run,

`dakota -i dakota_cal.in`

On the system where this example was generated, the best values of E0 and Es discovered were:
```
<<<<< Best parameters (experiment config variables omitted) =
                      2.9891556145e+07 E0
                     -5.3290509492e+03 Es
```
Using these values, the predicted displacements are:
![Predicted displacements](configresult.png)

