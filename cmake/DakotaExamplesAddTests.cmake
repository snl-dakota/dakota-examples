#  _______________________________________________________________________
#
#  DAKOTA: Design Analysis Kit for Optimization and Terascale Applications
#  Copyright 2014-2020
#  National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#  This software is distributed under the GNU Lesser General Public License.
#  For more information, see the README file in the top Dakota directory.
#  _______________________________________________________________________

include(DakotaExamplesPathTools)


# Register an example with _example_path relative to the examples source dir
# 
# Sets in caller scope: _example_src, _example_bin
# Appends in caller: registered_dakota_examples, dakota_examples_required_files 
macro(dakota_example_init _example_path)
  string(REPLACE "/" "-" _example_name "${_example_path}")
  if( NOT ${_example_name} IN_LIST registered_dakota_examples)
    list(APPEND registered_dakota_examples ${_example_name})
    setup_test_directory(${_example_path})
  endif()
endmacro()


# If _depends_on is populated, make test _test_name depend on it 
function(add_conditional_dependence _test_name _depends_on)
  if(_depends_on)
    set_tests_properties(${_test_name} PROPERTIES DEPENDS ${_depends_on})
  endif()
endfunction()


# Handler for applying any necessary properties to all tests, such as
# ENVIRONMENT, RUN_SERIAL, WILL_FAIL
function(apply_test_properties _test_name _depends_on)
  set_tests_properties(${_test_name} PROPERTIES LABELS "DakotaExample")

  add_conditional_dependence(${_test_name} "${_depends_on}")

  set(_env_path
    "PATH=${DAKOTA_DPREPRO_PATH}:${DAKOTA_TEST_DRIVERS_PATH}:$ENV{PATH}")
  set(_env_python_path "PYTHONPATH=${DAKOTA_PYTHON_PATH}:$ENV{PYTHONPATH}")

  # Can only have generator expressions in certain commands:
  if(TARGET surrogates)
    set_tests_properties(${_test_name} PROPERTIES
      ENVIRONMENT "${_env_path};PYTHONPATH=$<TARGET_FILE_DIR:surrogates>:${DAKOTA_PYTHON_PATH}:$ENV{PYTHONPATH}")
  else()
    set_tests_properties(${_test_name} PROPERTIES
      ENVIRONMENT "${_env_path};${_env_python_path}")
  endif()
endfunction()


# Add a test to check an input file
#
# Sets in caller scope: _last_test_added
function(test_check_input _example_path _input_name _depends_on)
  build_example_names("${_example_path}" "${_input_name}")
  set(_test_name ${_example_name}-${_input_name_we}-check)

  add_test(NAME ${_test_name}
    COMMAND $<IF:$<BOOL:${DAKOTA_EXE}>,${DAKOTA_EXE},$<TARGET_FILE:dakota>>
      -check -input ${_input_name}
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${_example_path}"
    )
  apply_test_properties(${_test_name} "${_depends_on}")

  set(_last_test_added ${_test_name} PARENT_SCOPE)
endfunction()


# Add a test to run an input file
#
# Sets in caller scope: _last_test_added
function(test_run_input _example_path _input_name _depends_on)
  build_example_names("${_example_path}" "${_input_name}")
  set(_test_name ${_example_name}-${_input_name_we}-run)

  add_test(NAME ${_test_name}
    COMMAND $<IF:$<BOOL:${DAKOTA_EXE}>,${DAKOTA_EXE},$<TARGET_FILE:dakota>>
      -input ${_input_name}
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${_example_path}"
    )
  apply_test_properties(${_test_name} "${_depends_on}")

  set(_last_test_added ${_test_name} PARENT_SCOPE)
endfunction()


# Add a test to regress an input file against baseline
#
# Sets in caller scope: _last_test_added
function(test_regress_input _example_path _input_name _depends_on)
  build_example_names("${_example_path}" "${_input_name}")
  set(_test_name ${_example_name}-${_input_name_we}-regress)

  set(_input_name_base
    "${CMAKE_CURRENT_SOURCE_DIR}/${_example_path}/${_input_name_we}.base")
  if(NOT EXISTS "${_input_name_base}")
    message(FATAL_ERROR "Example ${_example_path}/${_input_name} has no "
      "baseline ${_input_name_base}")
  endif()

  if(DAKOTA_EXE)
    get_filename_component(_dakota_exe_dir ${DAKOTA_EXE} DIRECTORY)
  endif()
  add_test(NAME ${_test_name}
    COMMAND "${DAKOTA_TEST_PERL}" --save-output
      --bin-dir="$<IF:$<BOOL:${DAKOTA_EXE}>,${_dakota_exe_dir},$<TARGET_FILE_DIR:dakota>>"
      ${_input_name}
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${_example_path}"
    )
  apply_test_properties(${_test_name} "${_depends_on}")

  set(_last_test_added ${_test_name} PARENT_SCOPE)
endfunction()


# Add a test to run an arbitrary command
#
# Sets in caller scope: ${_example_name}_command_num,  _last_test_added
function(test_command _example_path _test_command _depends_on)
  string(REPLACE "/" "-" _example_name "${_example_path}")

  # No easy way to name based on the command itself, so number them as added
  if (${_example_name}_command_num)
    math(EXPR _command_num_plus_one "${${_example_name}_command_num} + 1")
  else()
    set(_command_num_plus_one 1)
  endif()
  set(${_example_name}_command_num ${_command_num_plus_one} PARENT_SCOPE)

  set(_test_name ${_example_name}-command-${_command_num_plus_one})

  add_test(NAME ${_test_name}
    COMMAND ${_test_command}
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${_example_path}"
    )
  apply_test_properties(${_test_name} "${_depends_on}")

  set(_last_test_added ${_test_name} PARENT_SCOPE)
endfunction()


# Register default tests for all ${_example_path}/*.in
# REGRESS if *.base, else CHECK
#
# Uses/modifies : _last_test_added from PARENT_SCOPE
macro(test_inputs_with_defaults _example_path)
  set(_example_src "${CMAKE_CURRENT_SOURCE_DIR}/${_example_path}")
  file(GLOB _example_in_files_fq "${_example_src}/*.in")

  if(NOT _example_in_files_fq)
    message(WARNING "In setting up default examples tests, no *.in files in: "
      "${_example_src}")
  endif()

  foreach(_example_in ${_example_in_files_fq})
    get_filename_component(_example_in_we ${_example_in} NAME_WE)
    if(EXISTS "${_example_src}/${_example_in_we}.base")
      test_regress_input("${_example_PATH}" ${_example_in_we}.in
	"${_last_test_added}")
    else()
      test_check_input("${_example_PATH}" ${_example_in_we}.in
	"${_last_test_added}")
    endif()
  endforeach()
endmacro()


# Add a Dakota Example test with the specified test variants
# DEFAULT will test each *.in file, REGRESS if *.base, else CHECK
#
# Appends in caller: registered_dakota_examples, dakota_examples_required_files,
#   _last_test_added
macro(dakota_example_test)
  set(_options DEFAULT)
  set(_oneValueArgs DEPENDS PATH)
  set(_multiValueArgs CHECK RUN REGRESS COMMAND)
  cmake_parse_arguments(_example "${_options}" "${_oneValueArgs}"
    "${_multiValueArgs}" ${ARGN})

  if(NOT _example_PATH)
    message(FATAL_ERROR "dakota_example_test requires PATH")
  endif()
  dakota_example_init("${_example_PATH}")

  # Block mutually exclusive options
  if( _example_DEFAULT AND
      (_example_CHECK OR _example_RUN OR _example_REGRESS) )
    message(FATAL_ERROR "Processing example ${_example_PATH}:\n"
      "DEFAULT cannot be specified with other input file test modes")
  endif()

  # tests in a given directory depend on each other
  set(_last_test_added)
  if(_example_DEPENDS)
    set(_last_test_added ${_example_DEPENDS})
  endif()

  if(_example_DEFAULT)
    test_inputs_with_defaults("${_example_PATH}")
  else()
    foreach(_input_check ${_example_CHECK})
      test_check_input("${_example_PATH}" ${_input_check} "${_last_test_added}")
    endforeach()

    foreach(_input_runs ${_example_RUN})
      test_run_input("${_example_PATH}" ${_input_runs} "${_last_test_added}")
    endforeach()

    foreach(_input_regress ${_example_REGRESS})
      test_regress_input("${_example_PATH}" ${_input_regress} "${_last_test_added}")
    endforeach()
  endif()

  if(_example_COMMAND)
    test_command("${_example_PATH}" "${_example_COMMAND}" "${_last_test_added}")
  endif()

endmacro()
