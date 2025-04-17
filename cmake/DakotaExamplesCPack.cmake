#  _______________________________________________________________________
#
#  Dakota: Explore and predict with confidence.
#  Copyright 2014-2025
#  National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#  This software is distributed under the GNU Lesser General Public License.
#  For more information, see the README file in the top Dakota directory.
#  _______________________________________________________________________


file(GLOB _dir_contents RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
  "${CMAKE_CURRENT_SOURCE_DIR}/*")

set(_examples_cpack_source_ignore)
foreach(_dir_entry ${_dir_contents})
  if(_dir_entry IN_LIST dakota_examples_binary)
    if(IS_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/${_dir_entry}")
      install(DIRECTORY ${_dir_entry}
	DESTINATION ${DAKOTA_EXAMPLES_INSTALL}/examples
	USE_SOURCE_PERMISSIONS
	# Manually account for case_studies as not at top-level
	PATTERN "case_studies" EXCLUDE
        PATTERN "__pycache__" EXCLUDE
        PATTERN "*.py[cdo]" EXCLUDE
	)
    else()
      install(FILES ${_dir_entry}
	DESTINATION ${DAKOTA_EXAMPLES_INSTALL}/examples)
    endif()
  endif()

  if(NOT _dir_entry IN_LIST dakota_examples_source)
    list(APPEND _examples_cpack_source_ignore
      "^${CMAKE_CURRENT_SOURCE_DIR}/${_dir_entry}")
  endif()
endforeach()

# Manually account for case_studies as not at top-level
list(APPEND _examples_cpack_source_ignore
  "^${CMAKE_CURRENT_SOURCE_DIR}/official/case_studies")

list(APPEND _examples_cpack_source_ignore "__pycache__" ".*\\\\.py[cdo]")

if(_examples_cpack_source_ignore)
  set(DAKOTA_EXAMPLES_CPACK_SOURCE_IGNORE ${_examples_cpack_source_ignore}
    CACHE STRING "Dakota example files to omit from source packages")
endif()
