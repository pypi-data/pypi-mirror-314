#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "rlc::driver" for configuration "Release"
set_property(TARGET rlc::driver APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(rlc::driver PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libdriver.a"
  )

list(APPEND _cmake_import_check_targets rlc::driver )
list(APPEND _cmake_import_check_files_for_rlc::driver "${_IMPORT_PREFIX}/lib64/libdriver.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
