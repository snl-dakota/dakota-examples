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

list(INSERT CMAKE_MODULE_PATH 0 "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

if(DAKOTA_TEST_EXAMPLES_REPO)

  enable_testing()

  # Locations of required tools like dakota executable, Perl script
  include(DakotaExamplesFindTools)
  include(DakotaExamplesAddTests)

  # Initialize test-tracking variables

  # names of added tests
  set(registered_dakota_examples)
  # absolute path to each file on which tests depend
  set(dakota_examples_required_files)

  # Register tests for various components
  include(DakotaExamplesOfficial)
  include(DakotaExamplesTraining)
  if(IS_DIRECTORY contributed)
    include(DakotaExamplesContributed)
  endif()

  # Post-processing
  add_custom_target(dakota_examples_required_files ALL
    DEPENDS ${dakota_examples_required_files}
    COMMENT "Copy examples required files into binary test subdirs"
    )

endif()


# Unconditionally generate install and packaging rules

# Only distribute select examples
# case_studies conditional in sub-lists as not at top-level

# Example contents to package with binaries
set(dakota_examples_binary official README.md training)

# Example contents to package with source
set(dakota_examples_source ${dakota_examples_binary} cmake CMakeLists.txt)

# Selectively include/excludes content from packaging,
# publishing DAKOTA_EXAMPLES_CPACK_SOURCE_IGNORE to cache
include(DakotaExamplesCPack)
