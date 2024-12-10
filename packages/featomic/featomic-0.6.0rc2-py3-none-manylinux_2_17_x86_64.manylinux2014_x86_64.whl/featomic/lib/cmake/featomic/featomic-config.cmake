
####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was featomic-config.in.cmake                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

cmake_minimum_required(VERSION 3.16)

if(featomic_FOUND)
    return()
endif()

enable_language(CXX)

get_filename_component(FEATOMIC_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

if (WIN32)
    set(FEATOMIC_SHARED_LOCATION ${FEATOMIC_PREFIX_DIR}/bin/libfeatomic.so)
    set(FEATOMIC_IMPLIB_LOCATION ${FEATOMIC_PREFIX_DIR}/lib/libfeatomic.so.lib)
else()
    set(FEATOMIC_SHARED_LOCATION ${FEATOMIC_PREFIX_DIR}/lib/libfeatomic.so)
endif()

set(FEATOMIC_STATIC_LOCATION ${FEATOMIC_PREFIX_DIR}/lib/libfeatomic.a)
set(FEATOMIC_INCLUDE ${FEATOMIC_PREFIX_DIR}/include/)

if (NOT EXISTS ${FEATOMIC_INCLUDE}/featomic.h OR NOT EXISTS ${FEATOMIC_INCLUDE}/featomic.hpp)
    message(FATAL_ERROR "could not find featomic headers in '${FEATOMIC_INCLUDE}', please re-install featomic")
endif()

find_package(metatensor 0.1 REQUIRED CONFIG)

# Shared library target
if (OFF OR ON)
    if (NOT EXISTS ${FEATOMIC_SHARED_LOCATION})
        message(FATAL_ERROR "could not find featomic library at '${FEATOMIC_SHARED_LOCATION}', please re-install featomic")
    endif()

    add_library(featomic::shared SHARED IMPORTED GLOBAL)
    set_target_properties(featomic::shared PROPERTIES
        IMPORTED_LOCATION ${FEATOMIC_SHARED_LOCATION}
        INTERFACE_INCLUDE_DIRECTORIES ${FEATOMIC_INCLUDE}
        BUILD_VERSION "0.6.0-rc2"
    )
    target_link_libraries(featomic::shared INTERFACE metatensor::shared)

    target_compile_features(featomic::shared INTERFACE cxx_std_17)

    if (WIN32)
        if (NOT EXISTS ${FEATOMIC_IMPLIB_LOCATION})
            message(FATAL_ERROR "could not find featomic library at '${FEATOMIC_IMPLIB_LOCATION}', please re-install featomic")
        endif()

        set_target_properties(featomic::shared PROPERTIES
            IMPORTED_IMPLIB ${FEATOMIC_IMPLIB_LOCATION}
        )
    endif()
endif()


# Static library target
if (OFF OR NOT ON)
    if (NOT EXISTS ${FEATOMIC_STATIC_LOCATION})
        message(FATAL_ERROR "could not find featomic library at '${FEATOMIC_STATIC_LOCATION}', please re-install featomic")
    endif()

    add_library(featomic::static STATIC IMPORTED GLOBAL)
    set_target_properties(featomic::static PROPERTIES
        IMPORTED_LOCATION ${FEATOMIC_STATIC_LOCATION}
        INTERFACE_INCLUDE_DIRECTORIES ${FEATOMIC_INCLUDE}
        INTERFACE_LINK_LIBRARIES "gcc_s;util;rt;pthread;m;dl;c"
        BUILD_VERSION "0.6.0-rc2"
    )
    target_link_libraries(featomic::static INTERFACE metatensor::shared)

    target_compile_features(featomic::static INTERFACE cxx_std_17)
endif()


# Export either the shared or static library as the featomic target
if (ON)
    add_library(featomic ALIAS featomic::shared)
else()
    add_library(featomic ALIAS featomic::static)
endif()
