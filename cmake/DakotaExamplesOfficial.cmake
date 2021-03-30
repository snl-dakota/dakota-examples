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

if(HAVE_QUESO)
  dakota_example_test(
    PATH official/bayes_calibration/multiple_qoi
    RUN dakota_bayes_calib_multi_qoi.in
    )
#else() -check ?
endif()

# Case studies may be omitted from source distributions
if(IS_DIRECTORY official/case_studies)
#  dakota_example_test(
#    PATH official/case_studies/bayesian_ml_emulator/study
#    CHECK wind_inference.in
#    )
endif()

dakota_example_test(
  PATH official/centered_parameter_study
  RUN dakota_cantilever_center.in
  )

dakota_example_test(
  PATH official/deterministic_calibration/field_interpolate
  RUN dakota_cal.in
  )

dakota_example_test(
  PATH official/deterministic_calibration/scalar_multiexperiment_config
  RUN dakota_cal.in
  )

dakota_example_test(
  PATH official/deterministic_calibration/scalar_residual
  RUN dakota_cal.in
  )

dakota_example_test(
  PATH official/global_sensitivity/direct_pce
  RUN direct_pce.in
  )

dakota_example_test(
  PATH official/global_sensitivity/direct_sampling
  RUN direct_sample.in
  )

dakota_example_test(
  PATH official/global_sensitivity/moat
  RUN dakota_moat.in
  )

dakota_example_test(
  PATH official/global_sensitivity/pce_on_data
  RUN pce_oli.in pce_oversample.in pce_undersample.in
  )

dakota_example_test(
  PATH official/local_reliability
  RUN logratio_uq_reliability.in
  )

dakota_example_test(
  PATH official/local_reliability_mean_value
  RUN logratio_uq_reliability.in
  )

dakota_example_test(
  PATH official/multidim_parameter_study
  RUN rosen_multidim.in
  )

dakota_example_test(
  PATH official/optimization/local/derivative-free
  RUN dakota_opt_apps_bounds.in
  )

dakota_example_test(
  PATH official/optimization/local/gradient-based
  RUN dakota_opt_qnewton_constrained.in
  )
