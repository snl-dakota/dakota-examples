# Field Calibration Terms with Interpolation

If you have not already done so, you may wish to read the introduction to this collection of examples that is one directory level up. It describes the calibration problem that is being solved.

This example demonstrates interpolation of field calibration terms. Please first read and understand the `field_no_interp` example. In that example, the analysis driver `cantilever.py` returns predictions of the displacement at the same temperatures where the experiments were performed (20 evenly spaced temperatures between -20 F and 500 F).  In this example, `cantilever.py` returns predictions at temperatures that differ from the experimental data (12, instead of 20, evenly spaced temperatures over the same domain), requiring interpolation from the predictions to the experiments.

Interpolation is enabled by adding the `interpolate` keyword to the response block of the Dakota input file. Currently, Dakota supports only linear interpolation over a single coordinate. When using interpolation, the user must provide the coordinate values (i.e. the temperatures in this case) at which measurements were taken. These are located in the files `displacement.1.coords` (for the first experiment) and `displacement.2.coords` (for the second). 

Likewise, the user must provide the coordinates of the simulation predictions for each field calibration term. An important current limitation of Dakota is that these coordinates must be the same for all evaluations; they are not permitted to change during the Dakota study. The simulation coordinates are specified in the file `displacement.coords`. (Note the lack of experiment number.) Although only a single coordinate is supported presently for interpolation, the user must also tell Dakota the number of coordinates using the `num_coordinates_per_field` keyword, and the user must add the `read_field_coordinates` keyword.

To run the example, first make sure Dakota is on your `PATH` and that the `share/dakota/Python` folder in yoru Dakota installation is on your `PYTHONPATH`. Then run,

`dakota -i dakota_cal.in`

On the system where this example was generated, the best values of E0 and Es discovered were:
```
<<<<< Best parameters (experiment config variables omitted) =
                      2.9891897415e+07 E0
                     -5.3290120824e+03 Es
```
Using these values, the predicted displacements are:
![Predicted displacements](configresult.png)

