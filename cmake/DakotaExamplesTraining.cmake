#  _______________________________________________________________________
#
#  DAKOTA: Design Analysis Kit for Optimization and Terascale Applications
#  Copyright 2014-2020
#  National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#  This software is distributed under the GNU Lesser General Public License.
#  For more information, see the README file in the top Dakota directory.
#  _______________________________________________________________________

# Register tests for training examples

dakota_example_test(
  PATH training/solutions/calibration/cantilever/
  REGRESS dakota_cantilever_nl2sol.in
  )

dakota_example_test(
  PATH training/solutions/optimization/1
  REGRESS dakota_cantilever_nominal.in
  )

dakota_example_test(
  PATH training/solutions/optimization/2
  REGRESS dakota_opt_cons_cantilever.in
  )

# TODO: review what breaks on WIN32
if(NOT WIN32)
  dakota_example_test(
    PATH training/solutions/optimization/3
    REGRESS dakota_opt_quasisine.in
    )
endif()

dakota_example_test(
  PATH training/solutions/sens_analysis/1
  REGRESS dakota_cantilever_centered.in
  )

dakota_example_test(
  PATH training/solutions/sens_analysis/2
  REGRESS dakota_cantilever_sampling.in
  )

dakota_example_test(
  PATH training/solutions/sens_analysis/3
  REGRESS dakota_cantilever_moat.in
  )

dakota_example_test(
  PATH training/solutions/uncertainty_analysis/1
  REGRESS dakota_sampling_cantilever.in
  )

dakota_example_test(
  PATH training/solutions/uncertainty_analysis/2
  REGRESS dakota_qsf_egra.in dakota_qsf_mpp.in dakota_qsf_mv.in
  dakota_qsf_pce.in dakota_qsf_sampling.in
  )
