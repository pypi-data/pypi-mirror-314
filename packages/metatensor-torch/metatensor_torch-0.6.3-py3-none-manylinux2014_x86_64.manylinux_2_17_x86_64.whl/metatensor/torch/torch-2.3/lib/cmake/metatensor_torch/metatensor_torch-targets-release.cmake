#----------------------------------------------------------------
# Generated CMake target import file for configuration "release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "metatensor_torch" for configuration "release"
set_property(TARGET metatensor_torch APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(metatensor_torch PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmetatensor_torch.so"
  IMPORTED_SONAME_RELEASE "libmetatensor_torch.so"
  )

list(APPEND _cmake_import_check_targets metatensor_torch )
list(APPEND _cmake_import_check_files_for_metatensor_torch "${_IMPORT_PREFIX}/lib/libmetatensor_torch.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
