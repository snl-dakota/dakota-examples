# Scalar Calibration Terms - Residual Responses

If you have not already done so, you may wish to read the introduction to this collection of examples that is one directory level up. It describes the calibration problem that is being solved.

In this example, no experimental data is provided to Dakota (the `calibration_data` and `calibration_data_file` keywords are absent from the Dakota input file, `dakota_cal.in`). Instead, the user’s analysis driver returns residuals (prediction minus experiment) to Dakota. This differencing is readily observed by editing the driver `cantilever_residuals.py`.

Displacement was experimentally measured at 20 temperatures, and `cantilever_residuals.py` predicts displacement at the same 20 temperatures. It returns the resulting residuals to Dakota, which is configured to expect 20 scalar “`calibration_terms`.”
To run the example, first make sure Dakota is on your `PATH` and that the `share/dakota/Python` folder in your Dakota installation is on your `PYTHONPATH`. Then run,

`dakota -i dakota_cal.in`

