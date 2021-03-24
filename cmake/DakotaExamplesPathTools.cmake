#  _______________________________________________________________________
#
#  DAKOTA: Design Analysis Kit for Optimization and Terascale Applications
#  Copyright 2014-2020
#  National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#  This software is distributed under the GNU Lesser General Public License.
#  For more information, see the README file in the top Dakota directory.
#  _______________________________________________________________________

include(AddFileCopyCommand)


# Translate path to hyphen-delimited and strip input file extension
#
# Sets in caller scope: _example_name, _input_name_we
macro(build_example_names _example_path _input_name)
  set(_input_name_fq
    "${CMAKE_CURRENT_SOURCE_DIR}/${_example_path}/${_input_name}")
  if(NOT EXISTS "${_input_name_fq}")
    message(FATAL_ERROR "Specified example file does not exist: "
      "${_input_name_fq}")
  endif()
  string(REPLACE "/" "-" _example_name "${_example_path}")
  get_filename_component(_input_name_we ${_input_name} NAME_WE)
endmacro()


# Setup the test directory for an _example_path relative to examples
# source dir, including copying all test files to the build tree
#
# Sets in caller scope: _example_src, _example_bin
# Appends in caller: dakota_examples_required_files
macro(setup_test_directory _example_path)
  set(_example_src "${CMAKE_CURRENT_SOURCE_DIR}/${_example_path}")
  set(_example_bin "${CMAKE_CURRENT_BINARY_DIR}/${_example_path}")

  if(NOT EXISTS "${_example_src}")
    message(FATAL_ERROR "Example PATH does not exist: ${_example_src}")
  endif()

  file(MAKE_DIRECTORY "${_example_bin}")
  file(GLOB _example_all_files "${_example_src}/*")

  # absolute paths to generated files for adding to a parent target
  set(_example_copied_files)
  foreach(_src_file_fq ${_example_all_files})
    get_filename_component(_src_file_name ${_src_file_fq} NAME)
    set(_dest_file_fq "${_example_bin}/${_src_file_name}")
    add_file_copy_command("${_src_file_fq}" "${_dest_file_fq}")
    list(APPEND _example_copied_files "${_dest_file_fq}")
  endforeach()

  list(APPEND dakota_examples_required_files ${_example_copied_files})

endmacro()
