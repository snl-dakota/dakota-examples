# Summary
Adjust the parameters of a model to make its predictions more closely match 
data, when data for multiple experiments run under different configurations 
are available.
 
### Run Dakota
    $ dakota -i dakota_cal.in -o dakota_cal.out
 
### More about running this example

This example uses the driver `cantilever.py`, which requires Python.
 
# What problem does this solve?

This example demonstrates how to calibrate a model to data from multiple
experiments that has been collected at different *configurations*, or conditions.

The configurations are distinguished by one or more configuration variables. The user 
provides values of these variables to Dakota in a data file, and Dakota is responsible 
for running the user's driver at each configuration to construct a composite set of 
residuals for all the experiments. This is in contrast to requiring the user to design 
a more complex driver that manages running the simlation multiple times.

## Math Equation

minimize: $` \qquad \qquad f(\theta) = \sum_{j=1}^{N_{configs}} {\sum_{i=1}^{N_{data}} { ( y_i^{model}(\theta; \chi_j) - y_{i,j}^{data} )^2  }} `$

Where:
* $`N_{configs}`$ is the number of experimental configurations (`num_experiments` in the Dakota input file)
* $`N_{data}`$ is the number of data points (this must be the same for all configurations; `calibration_terms` in the Dakota input file)
* $`y_i^{model}(\theta; \chi_j)`$ is the model prediction for the $`i`$th datapoint and configuration $`j`$.
* $`\theta`$ are the parameters to be calibrated.
* $`\chi_j`$ are the configuration variables for configuration $`j`$.
* $`y_{i,j}^{data}`$ is the $`i`$th datapoint for configuration $`j`$.

# What method will we use?

The method used in this example, `nl2sol`, is a gradient-based local optimizer
that is tailored to calibration problems. It is often a good method to use when
discovering a local minimum will achieve the goal of the calibration, and the 
residuals have smooth gradients.

## Analysis Driver

The model to be calibrated predicts the dependence of the Young’s modulus $`E`$ of
carbon steel on temperature. Over a wide range of temperature, this relationship
is linear to a very good approximation:

$`E(T) = E0 + Es \cdot T`$

The parameters $`E0`$ and $`Es`$ are to be calibrated. We don’t have experimental 
values of $`E(T)`$. Rather, two experiments were performed on a carbon steel cantilever 
beam with a rectangular cross section. In the first experiment, the beam was placed 
under a vertical load $`Y = 400 lbs`$, and the displacement at the free end was measured at a 
sequence of 20 evenly spaced temperatures between -20&deg;F and 500&deg;F. The vertical load 
was then increased to 600 lbs and the experiment was repeated.

The displacement of a rectangular cantilever beam can be predicted using a 
well-known formula that depends on $`E`$. The script `cantilever.py` 
implements this formula. It accepts Dakota parameter files as input, and 
expects to find the calibration parameters $`E0`$ and $`Es`$, as well as the vertical 
load $`Y`$. It predicts displacement at the same 20 temperatures for which
we have data and writes these predictions in Dakota results format.

Notice that our driver is limited to making predictions at just one vertical load
condition. To obtain residuals at both of the load conditions for which we have data,
the driver must be run twice, once for each experiment.

### Inputs

In the `reponses` section of the Dakota input file, the keywords `num_experiments` 
and `num_config_variables` are set to 2 and 1, respectively. The keyword 
`calibration_data_file` also appears and is set to `displacements.dat`. This file
has an initial header line that may contain column headings or other information 
helpful to the user (Dakota treats it as a comment) followed by one line per 
experiment. Each of these lines contains the value of our single configuration 
variable (the verical load, $`Y`$), followed by 20 measurements of the displacement.
As Dakota performs evaluations, it will insert these values of $`Y`$ into the 
`continuous_state` variable $`Y`$ that is defined in the `variables` section of
the input file.

### Outputs
 
The only output produced by this example is the file `dakota_cal.out`.

# Interpret the results
 
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
<<<<< Best data not found in evaluation cache

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
