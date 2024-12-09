#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "rlc::fuzzer" for configuration "Release"
set_property(TARGET rlc::fuzzer APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(rlc::fuzzer PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libfuzzer.a"
  )

list(APPEND _cmake_import_check_targets rlc::fuzzer )
list(APPEND _cmake_import_check_files_for_rlc::fuzzer "${_IMPORT_PREFIX}/lib64/libfuzzer.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
