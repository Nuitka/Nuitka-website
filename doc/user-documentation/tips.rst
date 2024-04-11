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

.. _nuitka-project-options:

****************************
 Nuitka Options in the code
****************************

One clean way of providing options to Nuitka, that you will always use
for your program, is to put them into the main file you compile. There
is even support for conditional options, and options using pre-defined
variables, this is an example:

.. code:: python

   # Compilation mode, support OS-specific options
   # nuitka-project-if: {OS} in ("Windows", "Linux", "Darwin", "FreeBSD"):
   #    nuitka-project: --onefile
   # nuitka-project-else:
   #    nuitka-project: --standalone

   # The PySide2 plugin covers qt-plugins
   # nuitka-project: --enable-plugin=pyside2
   # nuitka-project: --include-qt-plugins=qml

The comments must be at the start of lines, and indentation inside of
them is to be used, to end a conditional block, much like in Python.
There are currently no other keywords than the used ones demonstrated
above.

You can put arbitrary Python expressions there, and if you wanted to
e.g. access a version information of a package, you could simply use
``__import__("module_name").__version__`` if that would be required to
e.g. enable or disable certain Nuitka settings. The only thing Nuitka
does that makes this not Python expressions, is expanding ``{variable}``
for a pre-defined set of variables:

Table with supported variables:

+------------------+--------------------------------+------------------------------------------+
| Variable         | What this Expands to           | Example                                  |
+==================+================================+==========================================+
| {OS}             | Name of the OS used            | Linux, Windows, Darwin, FreeBSD, OpenBSD |
+------------------+--------------------------------+------------------------------------------+
| {Version}        | Version of Nuitka              | e.g. (1, 6, 0)                           |
+------------------+--------------------------------+------------------------------------------+
| {Commercial}     | Version of Nuitka Commercial   | e.g. (2, 1, 0)                           |
+------------------+--------------------------------+------------------------------------------+
| {Arch}           | Architecture used              | x86_64, arm64, etc.                      |
+------------------+--------------------------------+------------------------------------------+
| {MAIN_DIRECTORY} | Directory of the compiled file | some_dir/maybe_relative                  |
+------------------+--------------------------------+------------------------------------------+
| {Flavor}         | Variant of Python              | e.g. Debian Python, Anaconda Python      |
+------------------+--------------------------------+------------------------------------------+

The use of ``{MAIN_DIRECTORY}`` is recommended when you want to specify
a filename relative to the main script, e.g. for use in data file
options or user package configuration yaml files,

.. code:: python

   # nuitka-project: --include-data-files={MAIN_DIRECTORY}/my_icon.png=my_icon.png
   # nuitka-project: --user-package-configuration-file={MAIN_DIRECTORY}/user.nuitka-package.config.yml

***************************
 Python command line flags
***************************

For passing things like ``-O`` or ``-S`` to Python, to your compiled
program, there is a command line option name ``--python-flag=`` which
makes Nuitka emulate these options.

The most important ones are supported, more can certainly be added.

*****************************
 Caching compilation results
*****************************

The C compiler, when invoked with the same input files, will take a long
time and much CPU to compile over and over. Make sure you are having
``ccache`` installed and configured when using gcc (even on Windows). It
will make repeated compilations much faster, even if things are not yet
not perfect, i.e. changes to the program can cause many C files to
change, requiring a new compilation instead of using the cached result.

On Windows, with gcc Nuitka supports using ``ccache.exe`` which it will
offer to download from an official source and it automatically. This is
the recommended way of using it on Windows, as other versions can e.g.
hang.

Nuitka will pick up ``ccache`` if it's found in system ``PATH``, and it
will also be possible to provide if by setting ``NUITKA_CCACHE_BINARY``
to the full path of the binary, this is for use in CI systems where
things might be non-standard.

For the MSVC compilers and ClangCL setups, using the ``clcache`` is
automatic and included in Nuitka.

On macOS and Intel, there is an automatic download of a ``ccache``
binary from our site, for arm64 arches, it's recommended to use this
setup, which installs Homebrew and ccache in there. Nuitka picks that
one up automatically if it on that kind of machine. You need and should
not use Homebrew with Nuitka otherwise, it's not the best for standalone
deployments, but we can take ``ccache`` from there.

.. code:: bash

   export HOMEBREW_INSTALL_FROM_API=1
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
   eval $(/opt/homebrew/bin/brew shellenv)
   brew install ccache

***************************
 Control where Caches live
***************************

The storage for cache results of all kinds, downloads, cached
compilation results from C and Nuitka, is done in a platform dependent
directory as determined by the ``appdirs`` package. However, you can
override it with setting the environment variable ``NUITKA_CACHE_DIR``
to a base directory. This is for use in environments where the home
directory is not persisted, but other paths are.

There is also per cache control of these caches, here is a table of
environment variables that you can set before starting the compilation,
to make Nuitka store some of these caches in an entirely separate space.

+------------------+-----------------------------------+----------------------------------------+
| Cache name       | Environment Variable              | Data Put there                         |
+==================+===================================+========================================+
| downloads        | NUITKA_CACHE_DIR_DOWNLOADS        | Downloads made, e.g. dependency walker |
+------------------+-----------------------------------+----------------------------------------+
| ccache           | NUITKA_CACHE_DIR_CCACHE           | Object files created by gcc            |
+------------------+-----------------------------------+----------------------------------------+
| clcache          | NUITKA_CACHE_DIR_CLCACHE          | Object files created by MSVC           |
+------------------+-----------------------------------+----------------------------------------+
| bytecode         | NUITKA_CACHE_DIR_BYTECODE         | Bytecode of demoted modules            |
+------------------+-----------------------------------+----------------------------------------+
| dll-dependencies | NUITKA_CACHE_DIR_DLL_DEPENDENCIES | DLL dependencies                       |
+------------------+-----------------------------------+----------------------------------------+

*********
 Runners
*********

Avoid running the ``nuitka`` binary, doing ``python -m nuitka`` will
make a 100% sure you are using what you think you are. Using the wrong
Python will make it give you ``SyntaxError`` for good code or
``ImportError`` for installed modules. That is happening, when you run
Nuitka with Python2 on Python3 code and vice versa. By explicitly
calling the same Python interpreter binary, you avoid that issue
entirely.

*********************
 Fastest C Compilers
*********************

The fastest binaries of ``pystone.exe`` on Windows with 64 bits Python
proved to be significantly faster with MinGW64, roughly 20% better
score. So it is recommended for use over MSVC. Using ``clang-cl.exe`` of
Clang7 was faster than MSVC, but still significantly slower than
MinGW64, and it will be harder to use, so it is not recommended.

On Linux, for ``pystone.bin``, the binary produced by ``clang6`` was
faster than ``gcc-6.3``, but not by a significant margin. Since gcc is
more often already installed, that is recommended to use for now.

Differences in C compilation times have not yet been examined.

**********************
 Unexpected Slowdowns
**********************

Using the Python DLL, like standard CPython does, can lead to unexpected
slowdowns, e.g. in uncompiled code that works with Unicode strings. This
is because calling to the DLL rather than residing in the DLL causes
overhead, and this even happens to the DLL with itself, being slower,
than a Python all contained in one binary.

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

+------------------+-------------+----------+
| Visual C version | Redist Year | CPython  |
+==================+=============+==========+
| 14.3             | 2022        | 3.11     |
+------------------+-------------+----------+
| 14.2             | 2019        | 3.5-3.10 |
+------------------+-------------+----------+
| 14.1             | 2017        | 3.5-3.8  |
+------------------+-------------+----------+
| 14.0             | 2015        | 3.5-3.8  |
+------------------+-------------+----------+
| 10.0             | 2010        | 3.4      |
+------------------+-------------+----------+
| 9.0              | 2008        | 2.6, 2.7 |
+------------------+-------------+----------+

When using MingGW64 as downloaded by Nuitka, you'll need the following
redist versions:

+----------------------------+-------------+---------------------+
| MingGW64 version           | Redist Year | CPython             |
+============================+=============+=====================+
| WinLibs automatic download | 2015        | 2.6, 2.7, 3.4- 3.11 |
+----------------------------+-------------+---------------------+

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
necessary. Beware, of course, that is this is only useful if you know
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
