cmake_minimum_required(VERSION 3.24)

project(cippengio
    VERSION 0.1.0
    DESCRIPTION "A 2D C++ game engine built on SDL3"
    LANGUAGES CXX
)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

set(SDL_SHARED OFF CACHE BOOL "" FORCE)
set(SDL_STATIC ON CACHE BOOL "" FORCE)
set(SDL_TESTS OFF CACHE BOOL "" FORCE)
set(SDL_EXAMPLES OFF CACHE BOOL "" FORCE)
set(SDL_TEST_LIBRARY OFF CACHE BOOL "" FORCE)
set(SDL_INSTALL ON CACHE BOOL "" FORCE)

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/vendored/SDL/CMakeLists.txt")
    message(FATAL_ERROR
        "SDL3 was not found. Initialize the submodule with: "
        "git submodule update --init --recursive"
    )
endif()

add_subdirectory(vendored/SDL EXCLUDE_FROM_ALL)

add_library(cippengio STATIC
    src/core.cpp
)
add_library(cippengio::cippengio ALIAS cippengio)

target_compile_features(cippengio PUBLIC cxx_std_14)
target_include_directories(cippengio
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
target_link_libraries(cippengio PRIVATE SDL3::SDL3-static)

add_executable(cippengioDemo
    examples/cippengio_demo.cpp
)
target_compile_features(cippengioDemo PRIVATE cxx_std_14)
target_link_libraries(cippengioDemo PRIVATE cippengio SDL3::SDL3-static)

set(CIPPENGIO_INSTALL_CMAKEDIR "${CMAKE_INSTALL_LIBDIR}/cmake/cippengio")

configure_package_config_file(
    cmake/cippengioConfig.cmake.in
    "${CMAKE_CURRENT_BINARY_DIR}/cippengioConfig.cmake"
    INSTALL_DESTINATION "${CIPPENGIO_INSTALL_CMAKEDIR}"
)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/cippengioConfigVersion.cmake"
    VERSION "${PROJECT_VERSION}"
    COMPATIBILITY SameMajorVersion
)

install(TARGETS cippengio
    EXPORT cippengioTargets
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
)
install(DIRECTORY include/ DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}")
install(EXPORT cippengioTargets
    FILE cippengioTargets.cmake
    NAMESPACE cippengio::
    DESTINATION "${CIPPENGIO_INSTALL_CMAKEDIR}"
)
install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/cippengioConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/cippengioConfigVersion.cmake"
    DESTINATION "${CIPPENGIO_INSTALL_CMAKEDIR}"
)
