# Scalar Terms and Replicate Experiments

If you have not already done so, you may wish to read the introduction to this collection of examples that is one directory level up. It describes the calibration problem that is being solved.

This example demonstrates several Dakota features, including:
* *Computing residuals from user-provided experimental data.* Instead of the analysis driver returning residuals to Dakota, as demonstrated in the `scalar_residual` example, it returns predictions that Dakota differences with the experimental data.
* *Calibrating to replicate experimental data.* Data from multiple, identical experiments can be provided to Dakota. The analysis driver predicts the outcome of a single experiment, and Dakota handles differencing those predictions with the data from all of the experiments.
* *Treatment of uncertainty information.* Measurement uncertainty can be expressed to Dakota as variance on each measurement.

For this example, two experiments were conducted under identical conditions. (In particular, the vertical load was the same in both experiments.) Twenty measurements of displacement as a function of temperature were made in each. Uncertainty in the displacement measurements are available for both. All the measurements in the first experiment have a standard deviation of 0.1 in (variance = 0.01). For the second, the uncertainty was 0.15 in (variance = 0.0225).

The measured displacements and uncertainties are provided to Dakota in the file `displacements.dat`. This file is in the default ‘`annotated`’ format and has three lines. The first line is a header row that typically contains column labels but can contain anything. Although the header must be present in an annotated file, its contents are ignored by Dakota. Following the header are two lines of data, one for each experiment. These lines contain 41 items. The first item is the experiment number (1 or 2). The experiment number is followed by the 20 measurements. These are followed by the uncertainty (in terms of variance) of each of the 20 measurements.

In addition to the annotated format, Dakota supports ‘`freeform`’ and ‘`custom_annotated`’ formats. The reader is referred to the Reference Manual entries for these keywords for more information.

The name of the data file is provided to Dakota using the `calibration_data_file` keyword. The number of experiments and type of uncertainty are also specified in the response block.

To run the example, first make sure Dakota is on your `PATH` and that the share/dakota/Python folder in your Dakota installation is on your `PYTHONPATH`. Then run,

`dakota -i dakota_cal.in`

