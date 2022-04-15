# Summary

Calibrate a model to data from multiple experiments when simulation
predictions must be interpolated onto the data.

# Description

The example demonstrates how to use Dakota's interpolation feature when performing
a calibration. In addition, it shows how to use field calibration terms, which are 
required when performing interpolation.

When calibrating a model, one challenge that can arise is that
the simulation does not make predictions on coordinates that match the
experimental data, complicating calculation of accurate residuals.

Dakota can interpolate (in one dimension) simulation predictions onto the
coordinates of the data. Residuals are computed using the interpolated 
values. For each experiment, in addition to the observations, 
configuration, and uncertainty, the user provides the coordinates at which
the data were taken. The user also provides the coordinates at which the
simulation predictions are made. (A current limitation of the interpolation
feature is that the prediction coordinates are fixed for the duration of the
study.)

In this example, measurements of the tip displacement of a cantilever beam
are used to calibrate a model for the temperature dependence of the Young's
modulus of carbon steel. Two experiments were performed at different vertical loads.
In both, tip displacement was measured at a series of temperatures. The temperatures
in the experiments differ from those at which the simulation predicts displacements, 
and interpolation is needed to reconcile them.


# Calibration Problem

Over a wide range of temperature, the Young's modulus $`E`$ of carbon
steel is linearly related to temperature:
```math
E(T) = E0 + Es \cdot T
```

The parameters $`E0`$ and $`Es`$ are to be calibrated.

We don’t have direct experimental measurements of $`E(T)`$. Experiments were
performed on a carbon steel cantilever beam. The beam was placed under a vertical
load and the displacement of the tip, which depends on $`E(T)`$, was measured at
a series of temperatures. Dakota will use a cantilever beam model that incorporates
the linear model for $`E(T)`$ to determine the values of $`E0`$ and $`Es`$ that 
result in the closest fit between the measured and predicted tip displacements.

# Experimental Data

Two experiments were performed under different vertical loads. In both, the 
displacement of a cantilever beam tip under vertical load was measured at 20
temperatures between -20&deg;F and 500&deg;F.

The experimental observations are recorded in the files `displacement.1.dat` and
`displacement.2.dat`. The temperatures at which the displacements were measured
can be found in `displacements.1.coords` and `displacements.2.coords`. These files
all contain 20 values, and in general the number of coordinates must match the
number of observations for each experiment, although different experiments can
have different numbers of observations.

Finally, measurement variance is provided for each experiment in the files 
`displacement.1.sigma` and `displacement.2.sigma`. They contain a single value,
as specified in the Dakota input file (`experiment_variance_type = 'scalar'`). Dakota
also supports specification of per observation variance, or a full covariance
matrix per experiment.

Dakota infers the information each file contains based on its name, as explained in the 
[Reference Manual](https://dakota.sandia.gov//sites/default/files/docs/6.13/html-ref/responses-calibration_terms-calibration_data.html). The file names are composed
of the *response descriptor*, followed by the *experiment number*, followed by a
label *coords*, *sigma*, or *dat*.

# Simulation Coordinates

To perform the 1D interpolation, Dakota also must know the temperatures at which
the simulation will predict the tip displacement. These are provided in the file
`displacement.coords`. This filename contains the response descriptor and the label
*coords*. The lack of experimental number distinguishes it from the coordinate files the 
experimental data. Note that it contains 12 values, in agreement with the response 
specification in the Dakota input file (`lengths 12`).

Dakota will read the simulation coordinate file one time at the beginning of the study.
A limitation of Dakota is that all evaluations of the simulation are required to share these coordinates.

# Analysis Driver

The analysis driver for this study is the script `cantilever.py`.
It has three inputs:

* $`Y`$: The vertical load. In this study, $`Y`$ is a configuration variable that
  Dakota sets to values provided by the user in `displacements.1.coords` and 
  `displacements.2.coords` as needed. It is specified as a `continuous_state` 
  variable in the Dakota input.
* $`E0`$ and $`Es`$: the parameters being calibrated, the intercept
  and slope of the linear Young's modulus model. These are `continuous_design`
  variables in the Dakota input file.

When called by Dakota, the driver predicts beam tip displacement for the input
vertical load at the 12 temperatures listed in `displacements.dat`. It returns
these 12 predictions to Dakota. A single `field_calibration_term` of length 12
is specified in  the `responses` section of the Dakota  input file for the 12
predictions. Dakota handles interpolating these 12 predictions onto the 20 
temperatures provided for the experiments and calculating the residuals.

# How to run the example

    $ dakota -i dakota_cal.in -o dakota_cal.out
 
# Requirements

Python 2 or 3 with numpy

# Contents

* `dakota_cal.in`: Dakota input file
* `cantilever.py`: Combined simulator and analysis driver
* Experimental data:
  * `displacements.{1,2}.dat`: Data from the two experiments to calibrate to.
  * `displacements.{1,2}.coords`: Temperatures at which the data were collected.
  * `displacements.{1,2}.sigma`: Variance (uncertainty) of the measurements
* `displacements.dat`: Temperatures at which `cantilever.py` predicts displacements.
* `configresult.png`: Plot of experimental data and best fit using calibrated Young's modulus coefficients.

# Study Results
 
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
<<<<< Best evaluation ID not available
(This warning may occur when the best iterate is comprised of multiple interface
evaluations or arises from a composite, surrogate, or transformation model.)

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
