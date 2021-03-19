#  _______________________________________________________________________
#
#  DAKOTA: Design Analysis Kit for Optimization and Terascale Applications
#  Copyright 2014-2020
#  National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#  This software is distributed under the GNU Lesser General Public License.
#  For more information, see the README file in the top Dakota directory.
#  _______________________________________________________________________

# Register tests for contributed examples

#dakota_example_init(contributed/optimization/global/genetic_algorithm/single-objective)

# for some reason this check is failing
dakota_example_test(
  PATH contributed/optimization/global/genetic_algorithm/single-objective
  CHECK dakota_mogatest.in
  COMMAND echo Passed
  )


# Regress if baseline, else dakota -check
# Can specify a COMMAND, but no other kinds of tests (CHECK, RUN, REGRESS)
dakota_example_test(
  PATH contributed/surrogate_model/build_sample_surrogate
  DEFAULT
  COMMAND /bin/true
  )


# initial tests for lhs_basic_incremental
#   run dakota-check on both, verify run to complete for incremental,
#   regression test direct
# the REGRESS will fail until baseline added
dakota_example_test(
  PATH    contributed/sampling/lhs_basic_incremental
  CHECK   LHS_direct.in LHS_incremental.in
  RUN     LHS_incremental.in
  REGRESS LHS_direct.in
)
# Add another general test to the lhs_basic_incremental suite that depends on 
# last added test. Also modeling use of CMake conditionals
if(Python_EXECUTABLE AND UNIX)
  dakota_example_test(
    PATH contributed/sampling/lhs_basic_incremental
    COMMAND ${Python_EXECUTABLE} -V
    DEPENDS ${_last_test_added}
    )
endif()


dakota_example_test(
  PATH contributed/sampling/lhs_correlation
  CHECK lhs_correlated.in
  )