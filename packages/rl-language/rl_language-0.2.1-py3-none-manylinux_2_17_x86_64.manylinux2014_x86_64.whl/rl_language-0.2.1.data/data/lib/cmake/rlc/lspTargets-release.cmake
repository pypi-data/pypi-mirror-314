#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "rlc::lsp" for configuration "Release"
set_property(TARGET rlc::lsp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(rlc::lsp PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/liblsp.a"
  )

list(APPEND _cmake_import_check_targets rlc::lsp )
list(APPEND _cmake_import_check_files_for_rlc::lsp "${_IMPORT_PREFIX}/lib64/liblsp.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
