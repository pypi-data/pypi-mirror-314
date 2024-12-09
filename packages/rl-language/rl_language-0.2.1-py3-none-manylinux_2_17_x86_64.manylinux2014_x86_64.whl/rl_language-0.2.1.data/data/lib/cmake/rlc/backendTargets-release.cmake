#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "rlc::backend" for configuration "Release"
set_property(TARGET rlc::backend APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(rlc::backend PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libbackend.a"
  )

list(APPEND _cmake_import_check_targets rlc::backend )
list(APPEND _cmake_import_check_files_for_rlc::backend "${_IMPORT_PREFIX}/lib64/libbackend.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
