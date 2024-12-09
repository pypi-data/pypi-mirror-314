# Synopsis

**zdev** -  Versatile collection of routines & tools for common development tasks.

# Contents

This library provides handy routines & tools for common tasks during development as well as for productive use in Python programs (e.g. stripping 'fileparts()'). Application focus is on *scripts for automation* as well as on *algorithmic* functions.

The package is structured into the following modules:  

- **base**: init for Python console session & tools for automatic project deployment

- **core**: main collection of development functions (e.g. for type-checks, info strings, mass file operations or dependency tracking)

- **indexing**: helpers related to "find-type" of tasks (e.g. runlength sections or file-goto)

- **parallel**: convenience function for Python's native 'multiprocessing' pkg and classes for controllable dispatching of jobs onto N cores (e.g. 'Progress', 'Dispatcher')

- **plot**: routines for a single-line yet sophisticated control of figures based on 'matplotlib' or 'ploty'  
*Note: This requires access to the 'zynamon' package in order to enable 'TimeSeries' support!*

- **testing**: set of small dummy functions w/ and w/o arguments that can be used for testing (e.g. for routines in 'zdev.parallel')

- **validio**: functions for a robust I/O behaviour (i.e. automatic replacement of "problematic" characters etc)

- **colors**: central definition of common color codes (RGB) in human-readable form (e.g. 'cPurple')

- **searchstr**: central definition of common strings used in regular expressions


More specialized tools can be found in:
- **ccnx**: simplified access to C-code DLLs (using 'ctypes')
- **libDSP**: support for access to "libDSP.dll" - a hand-crafted C-code library for signal processing
- **xlcmp**: functions to compare rows or sheets of Excel workbooks and highlighting results in exported copies (using 'openpyxl')
- **sigproc**: some basic signal processing tests [ALPHA]


[ Dr. Marcus Zeller | dsp4444@gmail.com | Erlangen, Germany | 2019-2024 ]