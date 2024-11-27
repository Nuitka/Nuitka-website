:orphan:

######
 Tips
######

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

On this page, you'll find helpful tips and techniques for optimizing
your experience with Nuitka. From maximizing compilation efficiency to
managing dependencies and runtime considerations.

****************************
 Nuitka Options in the code
****************************

You can create a build script or directly track the Nuitka command line
options inside the source code. The latter is a much cleaner approach
than a build script that constructs a command line to invoke Nuitka.

In your build script, you use ``python -m nuitka some_script.py
--output-dir=dist`` and put only options that are not generally
relevant; in the main ``script.py`` you have lines like these.

.. code:: python

   # The PySide6 plugin covers qt-plugins
   # nuitka-project: --enable-plugin=pyside6
   # nuitka-project: --include-qt-plugins=qml

You can have conditions, you can evaluate environment variables, you can
use locations relative to the main script, and many more things. For
reference, check out the page :ref:`nuitka-project-options`, which
contains all the information.

***************************
 Python command line flags
***************************

For passing things like ``-O`` or ``-S`` to Python, to your compiled
program, there is a command line option name ``--python-flag=`` which
makes Nuitka emulate these options.

The most important ones are supported, but we will add more if a use
case exists.

*****************************
 Caching compilation results
*****************************

When invoked with identical input files, the C compiler will take a long
time and require a lot of CPU to compile over and over. Make sure to
have ``ccache`` installed and configured when using gcc. It will make
repeated compilations much faster, even if things are not yet
perfect, i.e. changes to the program can cause many C files to change,
requiring a new compilation instead of using the cached result.

On **Windows**, with the included MinGW64 **Nuitka** supports using
``ccache.exe`` and will offer to download from an official source and
use it automatically, and using that is recommended for Windows, as
other versions are known to very often have severe quality issues; for
example, they spuriously cause errors or hang indefinitely or don't work
at all.

Nuitka will pick up ``ccache`` if located in system ``PATH``, and it
will also be possible to provide if by setting ``NUITKA_CCACHE_BINARY``
to the full path of the binary. This is for use in CI systems where
environments might be non-standard.

For the MSVC compilers and ClangCL setups, using the ``clcache`` is
automatic and included in Nuitka.

On macOS and Intel, there is an automatic download of a ``ccache``
binary from our site. For arm64 arches, it's recommended to use this
setup, which installs Homebrew and ccache. Nuitka picks that one up
automatically if it is on that kind of machine. You need and should not
use Homebrew with Nuitka; otherwise, it's not the best for standalone
deployments, but we can take ``ccache`` from there.

.. code:: bash

   export HOMEBREW_INSTALL_FROM_API=1
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
   eval $(/opt/homebrew/bin/brew shellenv)
   brew install ccache

***************************
 Control where Caches live
***************************

The storage for cache results of all kinds, downloads, and cached
compilation results from C and **Nuitka**, is done in a
platform-dependent directory as determined by the ``appdirs`` package.
However, you can override it by setting the environment variable
``NUITKA_CACHE_DIR`` to a base directory. This is for use in
environments where the home directory does not persist but other paths
do.

There is also per cache control of these caches. Here is a table of
environment variables that you can set before starting the compilation,
to make Nuitka store some of these caches in an entirely separate space.

+------------------+-----------------------------------+-----------------------------------------+
| Cache name       | Environment Variable              | Data Put there                          |
+==================+===================================+=========================================+
| downloads        | NUITKA_CACHE_DIR_DOWNLOADS        | Downloads made, e.g., dependency walker |
+------------------+-----------------------------------+-----------------------------------------+
| ccache           | NUITKA_CACHE_DIR_CCACHE           | Object files created by gcc             |
+------------------+-----------------------------------+-----------------------------------------+
| clcache          | NUITKA_CACHE_DIR_CLCACHE          | Object files created by MSVC            |
+------------------+-----------------------------------+-----------------------------------------+
| bytecode         | NUITKA_CACHE_DIR_BYTECODE         | Bytecode of demoted modules             |
+------------------+-----------------------------------+-----------------------------------------+
| dll-dependencies | NUITKA_CACHE_DIR_DLL_DEPENDENCIES | DLL dependencies                        |
+------------------+-----------------------------------+-----------------------------------------+

*********
 Runners
*********

Avoid running the ``nuitka`` binary; doing ``python -m nuitka`` will
make sure that you are using what you think you are. Using the wrong
Python will make it give you ``SyntaxError`` or ``ImportError`` for
installed modules. That happens, when you run **Nuitka** with Python2 on
Python3 code and vice versa. You avoid that issue by explicitly calling
the same Python interpreter binary.

*********************
 Fastest C Compilers
*********************

The fastest binaries of ``pystone.exe`` on Windows with 64 bits version
of Python proved to be significantly faster with MinGW64, roughly 20%
better score. So, it is recommended for use over MSVC. Using
``clang-cl.exe`` of Clang7 was faster than MSVC but still significantly
slower than MinGW64 and will be harder to use, so it that's not
recommended as well.

On Linux, for ``pystone.bin``, the binary produced by ``clang6`` was
faster than ``gcc-6.3``, but not significantly. Since gcc is more often
already installed, it is recommended for use for now.

Differences in C compilation times were not examined.

**********************
 Unexpected Slowdowns
**********************

Using the Python DLL, as standard CPython does, can lead to unexpected
slowdowns, for example in uncompiled code that works with Unicode
strings. This is because calling to the DLL rather than residing in the
DLL causes overhead, and this even happens to the DLL with itself, being
slower, than a Python all contained in one binary.

So if feasible, aim at static linking, which is currently only possible
with Anaconda Python on non-Windows, Debian Python2, self compiled
Pythons (do not activate ``--enable-shared``, not needed), and installs
created with ``pyenv``.

.. note::

   On Anaconda, you may need to execute ``conda install
   libpython-static``

*****************************************
 Standalone executables and dependencies
*****************************************

The process of making standalone executables for Windows traditionally
involves using an external dependency walker to copy necessary libraries
along with the compiled executables to the distribution folder.

There are plenty of ways to find that something is missing. Do not
manually copy things into the folder, esp. not DLLs, as that's not going
to work. Instead, make bug reports to get these handled by Nuitka
properly.

*******************************
 Windows errors with resources
*******************************

On Windows, the Windows Defender tool and the Windows Indexing Service
both scan the freshly created binaries, while Nuitka wants to work with
it, e.g. adding more resources, and then preventing operations randomly
due to holding locks. Make sure to exclude your compilation stage from
these services.

*******************************************
 Windows standalone program redistribution
*******************************************

Whether compiling with MingW or MSVC, the standalone programs have
external dependencies to Visual C Runtime libraries. Nuitka tries to
ship those dependent DLLs by copying them from your system.

Beginning with Microsoft Windows 10, Microsoft ships ``ucrt.dll``
(Universal C Runtime libraries) which handles calls to
``api-ms-crt-*.dll``.

With earlier Windows platforms (and wine/ReactOS), you should consider
installing Visual C runtime libraries before executing a Nuitka
standalone compiled program.

Depending on the used C compiler, you'll need the following redist
versions on the target machines. However, notice that compilation using
the 14.3 based version is always recommended, working and best
supported, unless you want to target Windows 7.

+------------------+-------------+-----------+
| Visual C version | Redist Year | CPython   |
+==================+=============+===========+
| 14.3             | 2022        | 3.12-3.10 |
+------------------+-------------+-----------+
| 14.2             | 2019        | 3.5-3.10  |
+------------------+-------------+-----------+
| 14.1             | 2017        | 3.5-3.8   |
+------------------+-------------+-----------+
| 14.0             | 2015        | 3.5-3.8   |
+------------------+-------------+-----------+
| 10.0             | 2010        | 3.4       |
+------------------+-------------+-----------+
| 9.0              | 2008        | 2.6, 2.7  |
+------------------+-------------+-----------+

When using MingGW64 as downloaded by Nuitka, you'll need the following
redist versions (same for all versions):

+----------------------------+-------------+--------------------+
| MingGW64 version           | Redist Year | CPython            |
+============================+=============+====================+
| WinLibs automatic download | 2015        | 2.6, 2.7, 3.4-3.12 |
+----------------------------+-------------+--------------------+

Once the corresponding runtime libraries are installed on the target
system, you may remove all ``api-ms-crt-*.dll`` files from your Nuitka
compiled dist folder.

******************************
 Detecting Nuitka at run time
******************************

Nuitka does *not* ``sys.frozen`` unlike other tools because it usually
triggers inferior code for no reason. For Nuitka, we have the module
attribute ``__compiled__`` to test if a specific module was compiled,
and the function attribute ``__compiled__`` to test if a specific
function was compiled.

*************************************************
 Providing extra Options to Nuitka C compilation
*************************************************

Nuitka will apply values from the environment variables ``CCFLAGS``,
``LDFLAGS`` during the compilation on top of what it determines to be
necessary. Beware, of course, that this is only useful if you know
what you are doing, so should this pose issues, raise them only with
perfect information.

******************************************************
 Producing a 32 bit binary on a 64 bit Windows system
******************************************************

Nuitka will automatically target the architecture of the Python you are
using. If this is 64 bit, it will create a 64 bit binary, if it is 32
bit, it will create a 32 bit binary. You have the option to select the
bits when you download the Python. In the output of ``python -m nuitka
--version`` there is a line for the architecture. It's ``Arch: x86_64``
for 64 bits, and just ``Arch: x86`` for 32 bits.

The C compiler will be picked to match that more or less automatically.
If you specify it explicitly, and it mismatches, you will get a warning
about the mismatch and informed that your compiler choice was rejected.
