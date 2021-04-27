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

dakota_example_test(
  PATH official/linked_interfaces/Python
  RUN dakota_rosenbrock_python.in
  )
# This is a workaround to enforce consistency between the Python used
# to build Dakota and which one gets used to run the driver script
# associated with this test.
get_test_property(${_last_test_added} ENVIRONMENT _linked_python_env)
set(_env_python_home
  "PYTHONHOME=${Python_STDLIB}:${Python_STDARCH}:$ENV{PYTHONHOME}")
set_tests_properties(${_last_test_added} PROPERTIES
  ENVIRONMENT "${_linked_python_env};${_env_python_home}")

# external_drivers tests
if (UNIX)
  dakota_example_test(
    PATH official/external_drivers/bash/
    RUN dakota_rosenbrock.in
  )
endif()

if (WIN32)
  dakota_example_test(
    PATH official/external_drivers/windows_bat
    RUN dakota_rosenbrock.in
  )
endif()

if (Python_EXECUTABLE)
  dakota_example_test(
    PATH official/external_drivers/Python
    RUN dakota_rosenbrock_python.in
  )
endif()

dakota_example_test(
  PATH official/external_drivers/MATLAB/linux
  CHECK dakota_matlab_rosenbrock.in
)

dakota_example_test(
  PATH official/external_drivers/MATLAB/windows
  CHECK dakota_matlab_rosenbrock.in
)

if(DAKOTA_HAVE_HDF5)
  dakota_example_test(
    PATH official/hdf5/centered_parameter_study
    RUN dakota_centered.in
  )
  
  if( Python_EXECUTABLE) # should also test for h5py
    dakota_example_test(
      PATH official/hdf5/centered_parameter_study
      COMMAND ${Python_EXECUTABLE} -B test_centered.py
      DEPENDS ${_last_test_added}
    )
  endif()
  
  dakota_example_test(
    PATH official/hdf5/incremental_sampling
    RUN dakota_refine.in
  )

  if( Python_EXECUTABLE) # should also test for h5py
    dakota_example_test(
      PATH official/hdf5/incremental_sampling
      COMMAND ${Python_EXECUTABLE} -B test_refine.py
      DEPENDS ${_last_test_added}
    )
  endif()
endif()
# Surrogates
dakota_example_test(
  PATH official/surrogates/dace
  RUN dakota_sampling_surrogate.in
)

dakota_example_test(
  PATH official/surrogates/imported
  RUN dakota_sampling_surrogate.in
)


dakota_example_test(
  PATH official/surrogates/surfpack
  RUN dakota_surrogate.in
)

dakota_example_test(
  PATH official/surrogates/surfpack
  COMMAND $<TARGET_NAME:surfpack_exe> sp_build_surrogate.spk
)

dakota_example_test(
  PATH official/surrogates/surfpack
  COMMAND $<TARGET_NAME:surfpack_exe> sp_eval_surrogate.spk
  DEPENDS ${_last_test_added}
)

if(DAKOTA_PYTHON AND Python_EXECUTABLE)
  
  dakota_example_test(
    PATH official/surrogates/library
    COMMAND ${Python_EXECUTABLE} -B test_notebook.py
  )

  dakota_example_test(
    PATH official/surrogates/library
    RUN dakota_morris_gp_study.in
  )

  dakota_example_test(
    PATH official/surrogates/library
    COMMAND ${Python_EXECUTABLE} -B test_load_gp.py
    DEPENDS ${_last_test_added}
  )
endif()


