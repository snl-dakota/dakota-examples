# Summary

Adjust the parameters of a model to make its predictions more closely
match data, when simulation predictions must be interpolated onto the
data.
 
### Run Dakota
    $ dakota -i dakota_cal.in -o dakota_cal.out
 
### More about running this example

This example uses the driver `cantilever.py`, which requires Python.
 
# What problem does this solve?

This example demonstrates how to calibrate a model to experimental data when
the user desires that Dakota interpolate the simulation predictions onto the 
data.

## Math Equation

minimize: $` \qquad \qquad f(\theta) = \sum_{j=1}^{N_{configs}} {\sum_{i=1}^{N_{data}} { ( y_i^{interp}(\theta; \chi_j) - y_{i,j}^{data} )^2  }} `$

Where:
* $`N_{configs}`$ is the number of experimental configurations (`num_experiments` in the Dakota input file)
* $`N_{data}`$ is the number of data points (this must be the same for all configurations; `calibration_terms` in the Dakota input file)
* $`y_i^{interp}(\theta; \chi_j)`$ is the interpolated model prediction for the $`i`$th datapoint and configuration $`j`$.
* $`\theta`$ are the parameters to be calibrated.
* $`\chi_j`$ are the configuration variables for configuration $`j`$.
* $`y_{i,j}^{data}`$ is the $`i`$th datapoint for configuration $`j`$.

# What method will we use?

The method used in this example, `nl2sol`, is a gradient-based local optimizer
that is tailored to calibration problems. It is often a good method to use when
discovering a local minimum will achieve the goal of the calibration, and the 
residuals have smooth gradients.

# Additional Input to Dakota

Because the driver predicts the displacement at a different set of
temperatures from the ones where it was experimentally measured, it is
necessary to interpolate between the two. The interpolation could be
performed by the driver, but Dakota also can do it.

To use Dakota's interpolation feature, `field_calibration_terms` must
be specified.  Scalar terms may not be used. In this example, there is
one field term with a length of 12 (the number of displacement
predictions returned by the driver). The values of the independent
coordinate (temperature, here) must be provided. Currently, Dakota is
limited to linear interpolation in one dimension, and the length of
the field and its coordinates must remain constant throughout the
study.

Instead of specifying the name of a `calibration_data_file`, which is
applicable only for scalar responses, the `calibration_data` group of
keywords must be used. Here, the number of experiments and
configuration variables may be specified, as well as the type of
experimental variance provided, if any. Finally, the `interpolate`
keyword activates interpolation.

Dakota expects to find all the data required for calibration in files
with predefined names. For this study, they are:

- **displacement.N.coords**: Temperatures at which displacement was
  *measured* in experiment N=[1,2].
- **displacement.N.dat**: Measurements of displacement for experiment N=[1,2].
- **displacement.N.sigma**: Uncertainty information for displacement
  measurements for experiment N=[1,2].
- **experiment.N.config**: Configuration variable values for experiment N=[1,2].
- **displacement.coords**: Temperatures at which displacement
  *predictions* will be returned by the driver. The name of this
  file differs from the name(s) of the experiment coordinates
  file(s) only by the lack of experiment number.

Note that `displacement.coords` is 12 lines long, corresponding to the
12 predicted values of displacement that Dakota expects from
`cantilever.py`. The other files are 20 lines long, corresponding to
the number of data points collected in each experiment.


## Analysis Driver

The model to be calibrated predicts the dependence of the Young’s
modulus $`E`$ of carbon steel on temperature. Over a wide range of
temperature, this relationship is linear to a very good approximation:

$`E(T) = E0 + Es \cdot T`$

The parameters $`E0`$ and $`Es`$ are to be calibrated. We don’t have
experimental values of $`E(T)`$. Rather, an experiment was performed
on a carbon steel cantilever beam with a rectangular cross
section. The beam was placed under a vertical load of 400 lbs, and the
displacement at the free end was measured at a sequence of 20 evenly
spaced temperatures between -20&deg;F and 500&deg;F. The experiment
was then repeated with a vertical load of 600 lbs.

The displacement of a rectangular cantilever beam can be predicted
using a well-known formula that depends on E. The script cantilever.py
implements this formula.


### Inputs

The cantilever.py driver has three inputs: the slope, $`E0`$; the
intercept, $`Es`$, and the vertical load $`Y`$. The slope and the
intercept are to be calibrated.

### Outputs

The analysis driver returns one value, the displacement at 12 (not 20)
evenly spaced temperatures between -20°F and 500°F and writes these
predictions in Dakota results format.

 
# Interpret the results
 
## Screen Output

Dakota produces the following output to the screen (redirected to
`dakota_cal.out`):

~~~~
<<<<< Best parameters (experiment config variables omitted) =
                      2.9891897415e+07 E0
                     -5.3290120824e+03 Es
Original (as-posed) response:
<<<<< Best model responses 
<<<<< Best configuration variables (experiment 1) =
                      4.0000000000e+02 Y
<<<<< Best model responses (experiment 1) =
                      6.3213084277e+00 displacement_1
                      6.3748421676e+00 displacement_2
                      6.4292903823e+00 displacement_3
                      6.4846767057e+00 displacement_4
                      6.5410255930e+00 displacement_5
                      6.5983623567e+00 displacement_6
                      6.6567132051e+00 displacement_7
                      6.7161052814e+00 displacement_8
                      6.7765667066e+00 displacement_9
                      6.8381266232e+00 displacement_10
                      6.9008152425e+00 displacement_11
                      6.9646638941e+00 displacement_12
<<<<< Best configuration variables (experiment 2) =
                      6.0000000000e+02 Y
<<<<< Best model responses (experiment 2) =
                      9.4819626416e+00 displacement_1
                      9.5622632514e+00 displacement_2
                      9.6439355735e+00 displacement_3
                      9.7270150586e+00 displacement_4
                      9.8115383894e+00 displacement_5
                      9.8975435351e+00 displacement_6
                      9.9850698076e+00 displacement_7
                      1.0074157922e+01 displacement_8
                      1.0164850060e+01 displacement_9
                      1.0257189935e+01 displacement_10
                      1.0351222864e+01 displacement_11
                      1.0446995841e+01 displacement_12
Variance-weighted original (as-posed) residuals:
<<<<< Best residual terms =
                     -7.2611272260e-01
                      9.5422015546e-01
                     -1.6527960587e+00
                      1.1034264768e-01
                      5.3624640239e-01
                     -1.0538840359e+00
                     -1.0069828611e+00
                      5.0709417365e-01
                     -1.2489724140e-01
                      2.1528694585e+00
                     -1.2197505405e+00
                     -1.0407887364e+00
                     -9.8221187331e-01
                      2.0147955413e+00
                      3.4856487808e-01
                      3.5271195224e-02
                     -3.4548781725e-01
                     -2.0633140528e-01
                     -1.2141138472e+00
                      1.6766187405e+00
                     -3.3087718927e-01
                      3.2969032213e-01
                     -2.5623105866e-01
                      1.8726683810e+00
                     -4.3213453094e-01
                      7.3043573074e-01
                     -1.0599627805e-02
                     -1.4771855968e-01
                     -8.6461480807e-01
                     -3.0508400820e-01
                     -9.1072364046e-01
                      1.3969672970e+00
                      1.3730854934e+00
                      9.4458974678e-02
                      5.6272997808e-01
                      1.8200909522e-01
                     -2.9405478392e-01
                      1.1827352805e-01
                     -4.5869401385e-01
                     -1.4159456595e+00
<<<<< Best residual norm =  6.0316523501e+00; 0.5 * norm^2 =  1.8190415036e+01
<<<<< Best residual terms =
                     -7.2611272260e-01
                      9.5422015546e-01
                     -1.6527960587e+00
                      1.1034264768e-01
                      5.3624640239e-01
                     -1.0538840359e+00
                     -1.0069828611e+00
                      5.0709417365e-01
                     -1.2489724140e-01
                      2.1528694585e+00
                     -1.2197505405e+00
                     -1.0407887364e+00
                     -9.8221187331e-01
                      2.0147955413e+00
                      3.4856487808e-01
                      3.5271195224e-02
                     -3.4548781725e-01
                     -2.0633140528e-01
                     -1.2141138472e+00
                      1.6766187405e+00
                     -3.3087718927e-01
                      3.2969032213e-01
                     -2.5623105866e-01
                      1.8726683810e+00
                     -4.3213453094e-01
                      7.3043573074e-01
                     -1.0599627805e-02
                     -1.4771855968e-01
                     -8.6461480807e-01
                     -3.0508400820e-01
                     -9.1072364046e-01
                      1.3969672970e+00
                      1.3730854934e+00
                      9.4458974678e-02
                      5.6272997808e-01
                      1.8200909522e-01
                     -2.9405478392e-01
                      1.1827352805e-01
                     -4.5869401385e-01
                     -1.4159456595e+00
<<<<< Best residual norm =  6.0316523501e+00; 0.5 * norm^2 =  1.8190415036e+01
<<<<< Best data not found in evaluation cache

Warning: Confidence intervals may be inaccurate when num_experiments > 1
Confidence Intervals on Calibrated Parameters:
            E0: [ 2.9632495414e+07, 3.0151299416e+07 ]
            Es: [ -6.1849389192e+03, -4.4730852456e+03 ]
~~~~

The final results include:

* The best parameters (those that minimize the sum of the squared errors)
* For the best parameters, the best "original" model responses for each configuration. In this example,
  there are 12 original model responses.
* The best set of residuals. Notice that this list is 40 items long: the 12 predictions of displacement 
  for each of the two experiments have been interpolated onto the 20 experimental measurements, yielding 
  40 total residuals. The residuals are printed twice; the second set has any user-specified weighting
  applied and the first is unweighted.
* The norm of the best residuals (printed for the weighted and unweighted cases).
* Confidence intervals on the calibrated parameters (these should be 
  ignored for the multi-experiment case).
 
---

The points in the figure below are experimental data for the two configurations, 
and the lines are from the calibrated model.

![Calibrated Model](configresult.png)
 
---
