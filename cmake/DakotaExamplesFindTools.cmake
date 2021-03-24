#  _______________________________________________________________________
#
#  DAKOTA: Design Analysis Kit for Optimization and Terascale Applications
#  Copyright 2014-2020
#  National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#  This software is distributed under the GNU Lesser General Public License.
#  For more information, see the README file in the top Dakota directory.
#  _______________________________________________________________________

# Find required tools such as dakota executable

##set(DAKOTA_EXE ${CMAKE_CURRENT_SOURCE_DIR}/../../build.opt/src/dakota)
if(NOT DAKOTA_EXE)
  message(STATUS "DAKOTA_EXE not set.\n"
    "   DakotaExamples tests will attempt to use dakota executable target")
endif()

add_test(NAME dakota-exe-version
  COMMAND $<IF:$<BOOL:${DAKOTA_EXE}>,${DAKOTA_EXE},$<TARGET_FILE:dakota>>
  -version
  )


##set(DAKOTA_TEST_PERL ${CMAKE_CURRENT_SOURCE_DIR}/../test/dakota_test.perl)
if(NOT DAKOTA_TEST_PERL)
  if(Dakota_SOURCE_DIR)
    set(DAKOTA_TEST_PERL ${Dakota_SOURCE_DIR}/test/dakota_test.perl)
  else()
    message(FATAL_ERROR
      "Need DAKOTA_TEST_PERL or Dakota_SOURCE_DIR for dakota_test.perl.")
  endif()
endif()

add_test(NAME dakota-test-perl-help COMMAND ${DAKOTA_TEST_PERL} --help)


##set(DAKOTA_TEST_DRIVERS_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../../build.opt/test)
if(NOT DAKOTA_TEST_DRIVERS_PATH)
  if(Dakota_BINARY_DIR)
    set(DAKOTA_TEST_DRIVERS_PATH "${Dakota_BINARY_DIR}/test")
  else()
    message(WARNING
      "Some DakotaExamples tests require DAKOTA_TEST_DRIVERS_PATH (not found)")
  endif()
endif()
# TODO: validate driver location test at test time, maybe with cmake -P


##set(DAKOTA_PYTHON_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../interfaces/Python")
if(NOT DAKOTA_PYTHON_PATH)
  if(Dakota_SOURCE_DIR)
    set(DAKOTA_PYTHON_PATH "${Dakota_SOURCE_DIR}/interfaces/Python")
  else()
    message(WARNING
      "Some DakotaExamples tests require DAKOTA_PYTHON_PATH (not found)")
  endif()
endif()

# TODO: This won't work outside a Dakota build unless Python_EXECUTABLE set
if(Python_EXECUTABLE)
  add_test(NAME dakota-interfacing-import
    COMMAND ${Python_EXECUTABLE} -c "import dakota.interfacing")
  set_tests_properties(dakota-interfacing-import PROPERTIES
    ENVIRONMENT "PYTHONPATH=${DAKOTA_PYTHON_PATH}:$ENV{PYTHONPATH}")
endif()


##set(DAKOTA_DPREPRO_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../scripts/pyprepro")
if(NOT DAKOTA_DPREPRO_PATH)
  if(Dakota_SOURCE_DIR)
    set(DAKOTA_DPREPRO_PATH "${Dakota_SOURCE_DIR}/scripts/pyprepro")
  else()
    message(WARNING
      "Some DakotaExamples tests require DAKOTA_DPREPRO_PATH (not found)")
  endif()
endif()

add_test(NAME dprepro-help COMMAND "${DAKOTA_DPREPRO_PATH}/dprepro" --version)
