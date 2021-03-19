#  _______________________________________________________________________
#
#  DAKOTA: Design Analysis Kit for Optimization and Terascale Applications
#  Copyright 2014-2020
#  National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#  This software is distributed under the GNU Lesser General Public License.
#  For more information, see the README file in the top Dakota directory.
#  _______________________________________________________________________

project(DakotaExamples LANGUAGES NONE)
cmake_minimum_required(VERSION 3.12)

enable_testing()


list(INSERT CMAKE_MODULE_PATH 0 "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(DakotaExamplesAddTests)

# REMOVE (for testing)
list(INSERT CMAKE_MODULE_PATH 0
  "${CMAKE_CURRENT_SOURCE_DIR}/../cmake/semsCMake")
include(AddFileCopyCommand)

# Locations of required tools
set(DAKOTA_EXE ${CMAKE_CURRENT_SOURCE_DIR}/../../build.opt/src/dakota)
set(DAKOTA_TEST_PERL ${CMAKE_CURRENT_SOURCE_DIR}/../test/dakota_test.perl)


# Initialize test-tracking variables

# names of added tests
set(registered_dakota_examples)
# absolute path to each file on which tests depend
set(dakota_examples_required_files)


# Register tests for various components
include(DakotaExamplesOfficial)
include(DakotaExamplesContributed)


# Post-processing
add_custom_target(dakota_examples_required_files ALL
  DEPENDS ${dakota_examples_required_files}
  COMMENT "Copy examples required files into binary test subdirs"
  )
