# cippengio

A C++14 game-engine library built on SDL3. The project produces a precompiled
static library and installs a CMake package that other C++ projects can consume.

## Requirements

- CMake 3.24 or newer
- A C++14 compiler
- Git
- Python and [pre-commit](https://pre-commit.com/) for the commit-message check

## Development

Install the commit-message hook with:

```powershell
python -m pip install pre-commit
pre-commit clean
pre-commit install --hook-type commit-msg
```

The hook requires commit subjects in this form:

```text
category: small explanation

optional complementary explanation
```

For example:

```text
feat: add window support

Create and manage the first SDL window.
```

Use one of these lowercase categories: `feat`, `fix`, `docs`, `refactor`,
`build`, or `chore`. The complementary explanation is optional, but when
present it must follow a blank line.

## Build and install

The easiest way to build and install the project is the Python build script:

```powershell
python utils/build.py
```

The script initializes the SDL3 submodule, configures the `release` preset,
builds it, and installs the project to `install/`.

Before configuring or building for the first time, initialize and update the
SDL3 submodule:

```powershell
git submodule update --init --recursive
```

Run this command again whenever the SDL3 submodule reference changes.

From the project root, configure, build, and install to a local prefix:

PowerShell:

```powershell
cmake -S . -B build -DCMAKE_INSTALL_PREFIX="$($PWD.Path)\install"
cmake --build build --config Release
cmake --install build --config Release
```

Bash or Git Bash:

```bash
cmake -S . -B build -G "MinGW Makefiles" -DCMAKE_INSTALL_PREFIX="$PWD/install"
cmake --build build --config Release
cmake --install build --config Release
```

Alternatively, use the checked-in preset in either shell:

```bash
cmake --preset debug
cmake --build --preset debug
```

If CMake previously selected NMake in the `build` directory, create a fresh
build directory or remove the old CMake cache before selecting MinGW Makefiles.

The install includes the `cippengio` static library, public headers, and CMake
package files. SDL3 is built statically as part of this project and its CMake
package is installed to the same prefix.

## Use from another CMake project

Add the install prefix to `CMAKE_PREFIX_PATH`, then link the exported target:

```cmake
find_package(cippengio CONFIG REQUIRED)

add_executable(MyGame main.cpp)
target_link_libraries(MyGame PRIVATE cippengio::cippengio)
```

For example, configure the consuming project with:

```powershell
cmake -S . -B build -DCMAKE_PREFIX_PATH="C:\path\to\cippengio\install"
```
