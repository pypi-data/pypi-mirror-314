# Windows

## Visual Studio 2022

Install *Visual Studio 2022* with:

* C++ compiler (check **Workload &rarr; Desktop development with C++**)
* `cmake` and `ninja` (check **Installation Details &rarr; Desktop development with C++ &rarr; C++ CMake tools for Windows**)

You will have to load the `vcvarsall.bat` before being able to run the `cmake`
or `ninja` installed by *Visual Studio 2022*.

## Qt6

Install *Qt6* with:

* Qt6 for *MSVC 2022 64-bit* (for example: **Qt &rarr; Qt 6.X.Y &rarr; MSVC 2022 64-bit**)
* (optional) if you plan to debug the code, install *Qt Debug Information Files*
  (**Qt &rarr; Qt 6.X.Y &rarr; Qt Debug Information Files**)
* (optional) if you want to use *Qt Creator* for development:
  * **Qt Creator &rarr; Qt Creator X.Y.Z**
  * **CDB Debugger Support**
  * **Debugging Tools for Windows**

### cmake and ninja from Qt

You only need to install `cmake` and `ninja` from *Qt* installer if you plan to build with
*MinGW*. Python bindings should be built with *MSVC*, so they are not required by this
project.
