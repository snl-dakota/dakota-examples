#  _______________________________________________________________________
#
#  DAKOTA: Design Analysis Kit for Optimization and Terascale Applications
#  Copyright 2014-2020
#  National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#  This software is distributed under the GNU Lesser General Public License.
#  For more information, see the README file in the top Dakota directory.
#  _______________________________________________________________________

# Register tests for official examples

# TODO:
# Condense these with DEFAULT test option
# Add/change to REGRESS to these as baselines are reviewed

dakota_example_test(
  PATH official/bayes_calibration/multiple_qoi
  CHECK dakota_bayes_calib_multi_qoi.in
  )

dakota_example_test(
  PATH official/centered_parameter_study
  CHECK dakota_cantilever_center.in
  )

dakota_example_test(
  PATH official/deterministic_calibration/field_interpolate
  CHECK dakota_cal.in
  )

dakota_example_test(
  PATH official/deterministic_calibration/scalar_multiexperiment_config
  CHECK dakota_cal.in
  )

dakota_example_test(
  PATH official/deterministic_calibration/scalar_residual
  CHECK dakota_cal.in
  )

dakota_example_test(
  PATH official/global_sensitivity/direct_pce
  CHECK direct_pce.in
  )

dakota_example_test(
  PATH official/global_sensitivity/direct_sampling
  CHECK direct_sample.in
  )

dakota_example_test(
  PATH official/global_sensitivity/moat
  CHECK dakota_moat.in
  )

dakota_example_test(
  PATH official/global_sensitivity/pce_on_data
  CHECK pce_oli.in pce_oversample.in pce_undersample.in
  )

dakota_example_test(
  PATH official/local_reliability
  CHECK logratio_uq_reliability.in
  )

dakota_example_test(
  PATH official/local_reliability_mean_value
  CHECK logratio_uq_reliability.in
  )

dakota_example_test(
  PATH official/multidim_parameter_study
  CHECK rosen_multidim.in
  )

dakota_example_test(
  PATH official/optimization/local/derivative-free
  CHECK dakota_opt_apps_bounds.in
  )

dakota_example_test(
  PATH official/optimization/local/gradient-based
  CHECK dakota_opt_qnewton_constrained.in
  )
