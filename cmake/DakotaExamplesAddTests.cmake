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
  add_conditional_dependence(${_test_name} "${_depends_on}")

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
  add_conditional_dependence(${_test_name} "${_depends_on}")

  set(_last_test_added ${_test_name} PARENT_SCOPE)
endfunction()


# Add a test to regress an input file against baseline
#
# Sets in caller scope: _last_test_added
function(test_regress_input _example_path _input_name _depends_on)
  build_example_names("${_example_path}" "${_input_name}")
  set(_test_name ${_example_name}-${_input_name_we}-regress)

  # TODO: WARNING if .base DNE
  if(DAKOTA_EXE)
    get_filename_component(_dakota_exe_dir ${DAKOTA_EXE} DIRECTORY)
  endif()
  add_test(NAME ${_test_name}
    COMMAND "${DAKOTA_TEST_PERL}" --save-output
      --bin-dir="$<IF:$<BOOL:${DAKOTA_EXE}>,${_dakota_exe_dir},$<TARGET_FILE_DIR:dakota>>"
      ${_input_name}
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${_example_path}"
    )
  add_conditional_dependence(${_test_name} "${_depends_on}")

  set(_last_test_added ${_test_name} PARENT_SCOPE)
endfunction()


# Add a test to run an arbitrary command
#
# Sets in caller scope: _last_test_added
function(test_command _example_path _test_command _depends_on)
  string(REPLACE "/" "-" _example_name "${_example_path}")
  # TODO: need unique name if multiple commands
  set(_test_name ${_example_name}-command)

  add_test(NAME ${_test_name}
    COMMAND ${_test_command}
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${_example_path}"
    )
  add_conditional_dependence(${_test_name} "${_depends_on}")

  set(_last_test_added ${_test_name} PARENT_SCOPE)
endfunction()


# Add a Dakota Example test with the specified test variants
#
# Appends in caller: registered_dakota_examples, dakota_examples_required_files,
#   _last_test_added
macro(dakota_example_test)
  set(_options)
  set(_oneValueArgs DEPENDS PATH)
  set(_multiValueArgs CHECK RUN REGRESS COMMAND)
  cmake_parse_arguments(_example "${_options}" "${_oneValueArgs}"
    "${_multiValueArgs}" ${ARGN})

  if(NOT _example_PATH)
    message(FATAL_ERROR "dakota_example_test requires PATH")
  endif()

  dakota_example_init("${_example_PATH}")

  # tests in a given directory depend on each other
  set(_last_test_added)
  if(_example_DEPENDS)
    set(_last_test_added ${_example_DEPENDS})
  endif()

  foreach(_input_check ${_example_CHECK})
    test_check_input("${_example_PATH}" ${_input_check} "${_last_test_added}")
  endforeach()

  foreach(_input_runs ${_example_RUN})
    test_run_input("${_example_PATH}" ${_input_runs} "${_last_test_added}")
  endforeach()

  foreach(_input_regress ${_example_REGRESS})
    test_regress_input("${_example_PATH}" ${_input_regress} "${_last_test_added}")
  endforeach()

  if(_example_COMMAND)
    test_command("${_example_PATH}" "${_example_COMMAND}" "${_last_test_added}")
  endif()

endmacro()
