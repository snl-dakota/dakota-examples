# Summary

Calibrate a model to data from multiple experiments run under different
configurations using Dakota's configuration variable feature.

# Description

Model parameters can be calibrated to data from multiple experiments 
simultaneously, such that the resulting parameters are a best fit to all
the experiments. The experiments are distinguished from one another by
having been performed under different configurations. In addition to the
observations for each experiment, the user provides information about its
configuration in the form of *configuration variables*. To obtain predictions
for a particular experiment, Dakota runs the model with not only values
of the calibration parameters, but with forwarded values of the configuration
variables.

In this example, measurements of the tip displacement of a cantilever beam 
are used to calibrate a model for the temperature dependence of the Young's
modulus of carbon steel. Two experiments were performed. In both, tip displacement
was measured at a series of temperatures. The vertical load placed on the beam, which
is the configuration variable, differed for the two experiments. The example 
illustrates how to specify to Dakota both the observations for the experiments and
the configuration information.

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

Two experiments were performed. In both, the displacement of a cantilever beam tip
under vertical load was measured at a series of evenly-spaced temperatures between
 -20&deg;F and 500&deg;F.

The experiments differed in one respect. In the first, the vertical load was 400 lbs,
and in the second, it was 600 lbs.

These data are recorded in the file `displacements.dat`. The format of this file is
explained in the [Reference Manual](https://dakota.sandia.gov//sites/default/files/docs/6.13/html-ref/responses-calibration_terms-calibration_data_file.html). This example uses the default `annotated` format, in which the first line is a header, which is ignored by Dakota, and each subsequent line contains calibration data for one experiment. On each row:

**Item 1:** The experiment number

**Item 2:** Value of the configuration variable `Y`

**Items 3-22:** Experimental measurements of the displacement


# Analysis Driver

The analysis driver for this study is the script `cantilever.py`.
It has three inputs:

* $`Y`$: The vertical load. In this study, $`Y`$ is a configuration variable that
  Dakota sets to values provided by the user in `displacements.dat` as needed. It is 
  specified as a `continuous_state` variable in the Dakota input.
* $`E0`$ and $`Es`$: the parameters being calibrated, the intercept
  and slope of the linear Young's modulus model. These are `continuous_design`
  variables in the Dakota input file.

When called by Dakota, the driver predicts beam tip displacement for the input
vertical load at the 20 temperatures. It returns these 20 predictions to Dakota.
Twenty `calibration_terms` are specified in  the `responses` section of the Dakota 
input file for the 20 predictions. Dakota handles calculating the residuals by
differencing the predictions with the experimental measurements that the user
provided in `displacements.dat`.

# How to run the example

    $ dakota -i dakota_cal.in -o dakota_cal.out
 
# Requirements

Python 2 or 3 with numpy

# Contents

* `dakota_cal.in`: Dakota input file
* `cantilever.py`: Combined simulator and analysis driver
* `displacements.dat`: Experimental data to calibrate to.
* `configresult.png`: Plot of experimental data and best fit using calibrated Young's modulus coefficients.
 
# Study Results
 
## Screen Output

Screen output for this example is redirected to the file `dakota_cal.out`.

First, note that evaluations reported to the screen occur in pairs. For example,
look at evaluations 1 and 2:

~~~~
---------------------
Begin Evaluation    1
---------------------
Parameters for evaluation 1:
                      2.8000000000e+07 E0
                      0.0000000000e+00 Es
                      4.0000000000e+02 Y

blocking fork: python cantilever.py params.in.1 results.out.1

Active response data for evaluation 1:
Active set vector = { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 }
                      6.7724867725e+00 displacement01
                      6.7724867725e+00 displacement02
                      6.7724867725e+00 displacement03
                      6.7724867725e+00 displacement04
                      6.7724867725e+00 displacement05
                      6.7724867725e+00 displacement06
                      6.7724867725e+00 displacement07
                      6.7724867725e+00 displacement08
                      6.7724867725e+00 displacement09
                      6.7724867725e+00 displacement10
                      6.7724867725e+00 displacement11
                      6.7724867725e+00 displacement12
                      6.7724867725e+00 displacement13
                      6.7724867725e+00 displacement14
                      6.7724867725e+00 displacement15
                      6.7724867725e+00 displacement16
                      6.7724867725e+00 displacement17
                      6.7724867725e+00 displacement18
                      6.7724867725e+00 displacement19
                      6.7724867725e+00 displacement20



---------------------
Begin Evaluation    2
---------------------
Parameters for evaluation 2:
                      2.8000000000e+07 E0
                      0.0000000000e+00 Es
                      6.0000000000e+02 Y

blocking fork: python cantilever.py params.in.2 results.out.2

Active response data for evaluation 2:
Active set vector = { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 }
                      1.0158730159e+01 displacement01
                      1.0158730159e+01 displacement02
                      1.0158730159e+01 displacement03
                      1.0158730159e+01 displacement04
                      1.0158730159e+01 displacement05
                      1.0158730159e+01 displacement06
                      1.0158730159e+01 displacement07
                      1.0158730159e+01 displacement08
                      1.0158730159e+01 displacement09
                      1.0158730159e+01 displacement10
                      1.0158730159e+01 displacement11
                      1.0158730159e+01 displacement12
                      1.0158730159e+01 displacement13
                      1.0158730159e+01 displacement14
                      1.0158730159e+01 displacement15
                      1.0158730159e+01 displacement16
                      1.0158730159e+01 displacement17
                      1.0158730159e+01 displacement18
                      1.0158730159e+01 displacement19
                      1.0158730159e+01 displacement20
~~~~

Notice that the two evaluations had the same values of $`Es`$ and $`E0`$, but different
values of $`Y`$. Dakota set $`Y`$ to the two values provided in `displacements.dat`. When 
performing a calibration with configuration variables, Dakota runs the driver multiple times
at each point in design space where `nl2sol` requests an evaluation, one time for each 
experiment, inserting the configuration variable values in turn.

When configuration variables are employed, the final results that Dakota provides contains 
the following information:

---
~~~~
<<<<< Best parameters (experiment config variables omitted) =
                      2.9947590581e+07 E0
                     -5.5126113995e+03 Es
Original (as-posed) response:
<<<<< Best model responses 
<<<<< Best configuration variables (experiment 1) =
                      4.0000000000e+02 Y
<<<<< Best model responses (experiment 1) =
                      6.3088236515e+00 displacement01
                      6.3406497260e+00 displacement02
                      6.3727985341e+00 displacement03
                      6.4052750098e+00 displacement04
                      6.4380841884e+00 displacement05
                      6.4712312086e+00 displacement06
                      6.5047213157e+00 displacement07
                      6.5385598640e+00 displacement08
                      6.5727523200e+00 displacement09
                      6.6073042649e+00 displacement10
                      6.6422213980e+00 displacement11
                      6.6775095397e+00 displacement12
                      6.7131746348e+00 displacement13
                      6.7492227558e+00 displacement14
                      6.7856601062e+00 displacement15
                      6.8224930243e+00 displacement16
                      6.8597279867e+00 displacement17
                      6.8973716122e+00 displacement18
                      6.9354306658e+00 displacement19
                      6.9739120624e+00 displacement20
<<<<< Best configuration variables (experiment 2) =
                      6.0000000000e+02 Y
<<<<< Best model responses (experiment 2) =
                      9.4632354773e+00 displacement01
                      9.5109745890e+00 displacement02
                      9.5591978011e+00 displacement03
                      9.6079125148e+00 displacement04
                      9.6571262826e+00 displacement05
                      9.7068468129e+00 displacement06
                      9.7570819735e+00 displacement07
                      9.8078397960e+00 displacement08
                      9.8591284800e+00 displacement09
                      9.9109563973e+00 displacement10
                      9.9633320970e+00 displacement11
                      1.0016264310e+01 displacement12
                      1.0069761952e+01 displacement13
                      1.0123834134e+01 displacement14
                      1.0178490159e+01 displacement15
                      1.0233739536e+01 displacement16
                      1.0289591980e+01 displacement17
                      1.0346057418e+01 displacement18
                      1.0403145999e+01 displacement19
                      1.0460868094e+01 displacement20
Original (as-posed) residuals:
<<<<< Best residual terms =
                     -8.5096048483e-02
                      8.3770096004e-02
                     -1.7592032591e-01
                      1.3473698385e-03
                      4.4928028393e-02
                     -1.1300376140e-01
                     -1.0734525431e-01
                      4.5225964022e-02
                     -1.6975690025e-02
                      2.1194446486e-01
                     -1.2418247203e-01
                     -1.0516383029e-01
                     -9.8025935156e-02
                      2.0277522581e-01
                      3.7469896200e-02
                      7.3334942735e-03
                     -2.9444423322e-02
                     -1.4178567780e-02
                     -1.1367960420e-01
                      1.7691004244e-01
                     -6.8358742724e-02
                      3.1975669006e-02
                     -5.4395738862e-02
                      2.6636991476e-01
                     -7.7865097410e-02
                      9.8142322902e-02
                     -1.1560396468e-02
                     -3.0382963967e-02
                     -1.3642117004e-01
                     -5.0776322712e-02
                     -1.3991967305e-01
                      2.0791765957e-01
                      2.0625570227e-01
                      1.6112353721e-02
                      8.8329609299e-02
                      3.3010926410e-02
                     -3.6451679983e-02
                      2.7422888330e-02
                     -5.7206431307e-02
                     -1.9851959634e-01
<<<<< Best residual norm =  7.2079041625e-01; 0.5 * norm^2 =  2.5976941208e-01
<<<<< Best residual terms =
                     -8.5096048483e-02
                      8.3770096004e-02
                     -1.7592032591e-01
                      1.3473698385e-03
                      4.4928028393e-02
                     -1.1300376140e-01
                     -1.0734525431e-01
                      4.5225964022e-02
                     -1.6975690025e-02
                      2.1194446486e-01
                     -1.2418247203e-01
                     -1.0516383029e-01
                     -9.8025935156e-02
                      2.0277522581e-01
                      3.7469896200e-02
                      7.3334942735e-03
                     -2.9444423322e-02
                     -1.4178567780e-02
                     -1.1367960420e-01
                      1.7691004244e-01
                     -6.8358742724e-02
                      3.1975669006e-02
                     -5.4395738862e-02
                      2.6636991476e-01
                     -7.7865097410e-02
                      9.8142322902e-02
                     -1.1560396468e-02
                     -3.0382963967e-02
                     -1.3642117004e-01
                     -5.0776322712e-02
                     -1.3991967305e-01
                      2.0791765957e-01
                      2.0625570227e-01
                      1.6112353721e-02
                      8.8329609299e-02
                      3.3010926410e-02
                     -3.6451679983e-02
                      2.7422888330e-02
                     -5.7206431307e-02
                     -1.9851959634e-01
<<<<< Best residual norm =  7.2079041625e-01; 0.5 * norm^2 =  2.5976941208e-01
<<<<< Best evaluation ID not available
(This warning may occur when the best iterate is comprised of multiple interface
evaluations or arises from a composite, surrogate, or transformation model.)

Warning: Confidence intervals may be inaccurate when num_experiments > 1
Confidence Intervals on Calibrated Parameters:
            E0: [ 1.1863273575e+07, 4.8031907588e+07 ]
            Es: [ -6.5103878891e+04, 5.4078656092e+04 ]
~~~~

The final results include:

* The best parameters (those that minimize the sum of the squared errors)
* For the best parameters, the best "original" model responses for each configuration/experiment. The 
  two lists  of original model responses are each 20 items long.
* The best set of residuals. Dakota combines the residuals for all experiments into a composite set that is 40 items
  long. The residuals are printed twice; the second set have any user-specified weighting applied and the first are 
  unweighted.
* The norms of the unweighted and weighted residuals.
* Confidence intervals on the calibrated parameters (these should be 
  ignored for the multi-experiment case)
 
---

The points in the figure below are experimental data for the two configurations, 
and the lines are from the calibrated model.

![Calibrated Model](configresult.png)
 
---
