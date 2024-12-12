#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "swmm5" for configuration "Release"
set_property(TARGET swmm5 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(swmm5 PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/swmm5.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/swmm5.dll"
  )

list(APPEND _cmake_import_check_targets swmm5 )
list(APPEND _cmake_import_check_files_for_swmm5 "${_IMPORT_PREFIX}/lib/swmm5.lib" "${_IMPORT_PREFIX}/bin/swmm5.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
