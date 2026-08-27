:orphan:

########################
 Legacy Windows Support
########################

Standard **Nuitka** requires a reasonably modern toolchain (e.g. MSVC
for Python 3.10+) which targets Windows 10 and newer. **Nuitka
Commercial** extends this support to **Windows 7** and **Windows XP**
for programs that are already compatible with these older operating
systems and much older Python versions.

**************
 How It Works
**************

**Nuitka Commercial** provides a dedicated container build that uses an
older toolchain and older versions of dependencies. This enables the
compiled output to run on legacy Windows versions that the default
toolchain no longer supports.

The underlying approach:

-  A separate build environment with an older MSVC version is used.

-  Older versions of Python and required packages are installed in this
   environment.

-  The compilation targets the older Windows CRT and APIs.

The result is a binary that runs on **Windows 7** or even **Windows
XP**, provided your program does the same when run directly with
**Python** on those systems.

***********************
 Important Limitations
***********************

**Nuitka Commercial** cannot make your program work on an older OS if it
does not already work there. For example:

-  **Qt6** requires at least a recent **Windows 10** version — no
   version of Qt6 runs on Windows 7 or XP. Compiling with an older
   toolchain does not help.

-  **Newer Python packages** may have dropped support for older Windows
   versions. The package versions used in the legacy build must be those
   that still support the target OS.

Put simply: if it works with **Python** on these OSes, **Nuitka
Commercial** allows you to make it portable as a compiled binary.

**********************
 Enabling the Feature
**********************

The legacy Windows builds are provided through a container. Contact us
for access to the container image and instructions specific to your
deployment needs.

Go `back to Nuitka Commercial
</doc/commercial.html#older-oses-and-special-needs>`__ overview to learn
about more features or to subscribe to `Nuitka Commercial
</doc/commercial.html#pricing>`__.
