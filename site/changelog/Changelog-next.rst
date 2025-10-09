:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes and ongoing development for the
upcoming **Nuitka** |NUITKA_VERSION_NEXT|, serving as a draft changelog.
It also includes details on hot-fixes applied to the current stable
release, |NUITKA_VERSION|.

**************************************************
 **Nuitka** Release |NUITKA_VERSION_NEXT| (Draft)
**************************************************

.. note::

   These are the draft release notes for **Nuitka**
   |NUITKA_VERSION_NEXT|. A primary goal for this version is to deliver
   significant enhancements in scalability.

Development is ongoing, and this documentation might lag slightly behind
the latest code changes.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  **Standalone**: For the "Python Build Standalone" flavor ensured that
   debug builds correctly recognize all their specific built-in modules,
   preventing potential errors. (Fixed in 2.7.2 already.)

-  **Linux**: Fixed a crash when attempting to modify the RPATH of
   statically linked executables (e.g., from ``imageio-ffmpeg``). (Fixed
   in 2.7.2 already.)

-  **Anaconda**: Updated ``PySide2`` support to correctly handle path
   changes in newer Conda packages and improved path normalization for
   robustness. (Fixed in 2.7.2 already.)

-  **macOS**: Corrected handling of ``QtWebKit`` framework resources.
   Previous special handling was removed as symlinking is now default,
   which also resolved an issue of file duplication. (Fixed in 2.7.2
   already.)

-  **Debugging**: Resolved an issue in debug builds where an incorrect
   assertion was done during the addition of distribution metadata.
   (Fixed in 2.7.1 already.)

-  **Module**: Corrected an issue preventing ``stubgen`` from
   functioning with Python versions earlier than 3.6. (Fixed in 2.7.1
   already.)

-  **UI**: Prevented **Nuitka** from crashing when ``--include-module``
   was used with a built-in module. (Fixed in 2.7.1 already.)

-  **Module**: Addressed a compatibility issue where the ``code`` mode
   for the constants blob failed with the C++ fallback. This fallback is
   utilized on very old GCC versions (e.g., default on **CentOS7**),
   which are generally not recommended. (Fixed in 2.7.1 already.)

-  **Standalone**: Resolved an assertion error that could occur in
   certain Python setups due to extension module suffix ordering. The
   issue involved incorrect calculation of the derived module name when
   the wrong suffix was applied (e.g., using ``.so`` to derive a module
   name like ``gdbmmodule`` instead of just ``gdbm``). This was observed
   with Python 2 on **CentOS7** but could potentially affect other
   versions with unconventional extension module configurations. (Fixed
   in 2.7.1 already.)

-  **Python 3.12.0**: Corrected the usage of an internal structure
   identifier that is only available in Python 3.12.1 and later
   versions. (Fixed in 2.7.1 already.)

-  **Plugins**: Prevented crashes in Python setups where importing
   ``pkg_resources`` results in a ``PermissionError``. This typically
   occurs in broken installations, for instance, where some packages are
   installed with root privileges. (Fixed in 2.7.1 already.)

-  **macOS**: Implemented a workaround for data file names that
   previously could not be signed within app bundles. The attempt in
   release 2.7 to sign these files inadvertently caused a regression for
   cases involving illegal filenames. (Fixed in 2.7.1 already.)

-  **Python 2.6**: Addressed an issue where ``staticmethod`` objects
   lacked the ``__func__`` attribute. **Nuitka** now tracks the original
   function as a distinct value. (Fixed in 2.7.1 already.)

-  Corrected behavior for ``orderedset`` implementations that lack a
   ``union`` method, ensuring **Nuitka** does not attempt to use it.
   (Fixed in 2.7.1 already.)

-  **Python 2.6**: Ensured compatibility for setups where the
   ``_PyObject_GC_IS_TRACKED`` macro is unavailable. This macro is now
   used beyond assertions, necessitating support outside of debug mode.
   (Fixed in 2.7.1 already.)

-  **Python 2.6**: Resolved an issue caused by the absence of
   ``sys.version_info.releaselevel`` by utilizing a numeric index
   instead and adding a new helper function to access it. (Fixed in
   2.7.1 already.)

-  **Module**: Corrected the ``__compiled__.main`` value to accurately
   reflects the package in which a module is loaded, this was not the
   case for Python versions prior to 3.12. (Fixed in 2.7.1 already.)

-  **Plugins**: Further improved the ``dill-compat`` plugin by
   preventing assertions related to empty annotations and by removing
   hard-coded module names for greater flexibility. (Fixed in 2.7.1
   already.)

-  **Windows**: For onefile mode using DLL mode, ensure all necessary
   environment variables are correctly set for ``QtWebEngine``.
   Previously, default Qt paths could point incorrectly near the onefile
   binary. (Fixed in 2.7.3 already.)

-  **PySide6**: Fixed an issue with ``PySide6`` where slots defined in
   base classes might not be correctly handled, leading to them only
   working for the first class that used them. (Fixed in 2.7.3 already.)

-  **Plugins**: Enhanced Qt binding plugin support by checking for
   module presence without strictly requiring metadata. This improves
   compatibility with environments like Homebrew or ``uv`` where package
   metadata might be absent. (Fixed in 2.7.3 already.)

-  **macOS**: Ensured the ``apple`` target is specified during linking
   to prevent potential linker warnings about using an ``unknown``
   target in certain configurations. (Fixed in 2.7.3 already.)

-  **macOS**: Disabled the use of static ``libpython`` with ``pyenv``
   installations, as this configuration is currently broken. (Fixed in
   2.7.3 already.)

-  **macOS**: Improved error handling for the
   ``--macos-app-protected-resource`` option by catching cases where a
   description is not provided. (Fixed in 2.7.3 already.)

-  **Plugins**: Enhanced workarounds for ``PySide6``, now also covering
   single-shot timer callbacks. (Fixed in 2.7.4 already.)

-  **Plugins**: Ensured that the Qt binding module is included when
   using accelerated mode with Qt bindings. (Fixed in 2.7.4 already.)

-  **macOS**: Avoided signing through symlinks and minimized their use
   to prevent potential issues, especially during code signing of
   application bundles. (Fixed in 2.7.4 already.)

-  **Windows**: Implemented path shortening for paths used in onefile
   DLL mode to prevent issues with long or Unicode paths. This also
   benefits module mode. (Fixed in 2.7.4 already.)

-  **UI**: The options nanny plugin no longer uses a deprecated option
   for macOS app bundles, preventing potential warnings or issues.
   (Fixed in 2.7.4 already.)

-  **Plugins**: Ensured the correct macOS target architecture is used.
   This particularly useful for ``PySide2`` with universal CPython
   binaries, to prevent compile time crashes e.g. when cross-compiling
   for a different architecture. (Fixed in 2.7.4 already.)

-  **UI**: Fixed a crash that occurred on **macOS** if the ``ccache``
   download was rejected by the user. (Fixed in 2.7.4 already.)

-  **UI**: Improved the warning message related to macOS application
   icons for better clarity. (Added in 2.7.4 already.)

-  **Standalone**: Corrected an issue with QML plugins on **macOS** when
   using newer ``PySide6`` versions. (Fixed in 2.7.4 already.)

-  **Python 3.10+**: Fixed a memory leak where the matched value in
   pattern matching constructs was not being released. (Fixed in 2.7.4
   already.)

-  **Python3**: Fixed an issue where exception exits for larger
   ``range`` objects, which are not optimized away, were not correctly
   annotated by the compiler. (Fixed in 2.7.4 already.)

-  **Windows**: Corrected an issue with the automatic use of icons for
   ``PySide6`` applications on non-Windows if Windows icon options were
   used. (Fixed in 2.7.4 already.)

-  **Onefile**: When using DLL mode there was a load error for the DLL
   with MSVC 14.2 or earlier, but older MSVC is to be supported. (Fixed
   in 2.7.5 already.)

-  **Onefile**: Fix, the splash screen was showing in DLL mode twice or
   more; these extra copies couldn't be stopped. (Fixed in 2.7.5
   already.)

-  **Standalone**: Fixed an issue where data files were no longer
   checked for conflicts with included DLLs. The order of data file and
   DLL copying was restored, and macOS app signing was made a separate
   step to remove the order dependency. (Fixed in 2.7.6 already.)

-  **macOS**: Corrected our workaround using symlinks for files that
   cannot be signed. When ``--output-directory`` was used, as it made
   incorrect assumptions about the ``dist`` folder path. (Fixed in 2.7.6
   already.)

-  **UI**: Prevented checks on onefile target specifications when not
   actually compiling in onefile mode, e.g. on macOS with
   ``--mode=app``. (Fixed in 2.7.6 already.)

-  **UI**: Improved error messages for data directory options by include
   the relevant part in the output. (Fixed in 2.7.6 already.)

-  **Plugins**: Suppressed ``UserWarning`` messages from the
   ``pkg_resources`` module during compilation. (Fixed in 2.7.6
   already.)

-  **Python3.11+**: Fixed an issue where descriptors for compiled
   methods were incorrectly exposed for Python 3.11 and 3.12. (Fixed in
   2.7.7 already.)

-  **Plugins**: Avoided loading modules when checking for data file
   existence. This prevents unnecessary module loading and potential
   crashes in broken installations. (Fixed in 2.7.9 already.)

-  **Plugins**: The ``global_change_function`` anti-bloat feature now
   operates on what should be the qualified names (``__qualname__``)
   instead of just function names, preventing incorrect replacements of
   methods with the same name in different classes. (Fixed in 2.7.9
   already.)

-  **Onefile**: The ``containing_dir`` attribute of the ``__compiled__``
   object was regressed in DLL mode on **Windows**, pointing to the
   temporary DLL directory instead of the directory containing the
   onefile binary. (Fixed in 2.7.10 already, note that the solution in
   2.7.9 had a regression.)

-  **Compatibility**: Fixed a crash that occurred when an import
   attempted to go outside its package boundaries. (Fixed in 2.7.11
   already.)

-  **macOS**: Ignored a warning from ``codesign`` when using self-signed
   certificates. (Fixed in 2.7.11 already.)

-  **Onefile**: Fixed an issue in DLL mode where environment variables
   from other onefile processes (related to temporary paths and process
   IDs) were not being ignored, which could lead to conflicts. (Fixed in
   2.7.12 already.)

-  **Compatibility**: Fixed a potential crash that could occur when
   processing an empty code body. (Fixed in 2.7.13 already.)

-  **Plugins**: Ensured that DLL directories created by plugins could be
   at the top level when necessary, improving flexibility. (Fixed in
   2.7.13 already.)

-  **Onefile**: On **Windows**, corrected an issue in DLL mode where
   ``original_argv0`` was ``None``; it is now properly set. (Fixed in
   2.7.13 already.)

-  **macOS**: Avoided a warning that appeared on newer macOS versions.
   (Fixed in 2.7.13 already.)

-  **macOS**: Allowed another DLL to be missing for ``PySide6`` to
   support more setups. (Fixed in 2.7.13 already.)

-  **Standalone**: Corrected the existing import workaround for Python
   3.12 that was incorrectly renaming existing modules of matching names
   into sub-modules of the currently imported module. (Fixed in 2.7.14
   already.)

-  **Standalone**: On **Windows**, ensured that the DLL search path
   correctly uses the proper DLL directory. (Fixed in 2.7.14 already.)

-  **Python 3.5+**: Fixed a memory leak where the called object could be
   leaked in calls with keyword arguments following a star dict
   argument. (Fixed in 2.7.14 already.)

-  **Python 3.13**: Fixed an issue where ``PyState_FindModule`` was not
   working correctly with extension modules due to sub-interpreter
   changes. (Fixed in 2.7.14 already.)

-  **Onefile**: Corrected an issue where the process ID (PID) was not
   set in a timely manner, which could affect onefile operations. (Fixed
   in 2.7.14 already.)

-  **Compatibility**: Fixed a crash that could occur when a function
   with both a star-list argument and keyword-only arguments was called
   without any arguments. (Fixed in 2.7.16 already.)

-  **Standalone**: Corrected an issue where distribution names were not
   checked case-insensitively, which could lead to metadata not being
   included. (Fixed in 2.7.16 already.)

-  **Linux**: Avoid using full zlib with extern declarations but instead
   only the CRC32 functions we need. Otherwise conflicts with OS headers
   could occur.

-  **Standalone**: Fix, scanning for standard library dependencies
   should not be necessary

   We now ignore doing it for standard library for all flavors,
   previously we only had it for Anaconda.

-  **Plugins**: Make run time query code robust against modules output
   in stdout during import

   This affected at least ``toga`` giving some warnings on Windows with
   mere stdout prints. We now have a marker for the start of our output
   that we look for and safely ignore them.

-  **Windows**: Do not attach when running in DLL mode. For onefile with
   DLL mode, this was unnecessary since the bootstrap already does it,
   and for pure DLL mode it's not desired.

-  **Onefile:** No need to monitor the parent process in onefile DLL
   mode; there is no child process launched.

-  **Anaconda**: Determine version and project name for conda packages
   more reliably

   It seems Anaconda is giving variables in package metadata and often
   no project name, so we derive it from the conda files and its meta
   data in those cases.

-  **macOS**: Make sure the SSL certificates are found when downloading
   on macOS.

-  **Windows**: Fix, console mode attach was not working in onefile DLL
   mode.

-  **Scons**: Fix, need to only use pragma with ``clang`` as older
   ``gcc`` can give warnings about them. This fixes building on older
   OSes with the system gcc.

-  **Compatibility**: Fix, need to avoid using filenames with more than
   250 chars for long module names.

   -  For cache files, const files, and C files, we need to make sure,
      we don't exceed the 255 char limits per path element that
      literally every OS has.

   -  Also enhanced the check code for legal paths to cover this, so
      user options are covered from this errors too.

   -  Moved file hashing to file operations where it makes more sense to
      allow module names to use hashing to provide a legal filename for
      themselves.

-  **Compatibility**: Fix, walking included compiled packages through
   the Nuitka loader could produce false names in some cases.

-  **Windows**: Fix, for when checking ``stderr`` during launch and it
   being ``None``, this make wrong method calls on that object.

-  **Debugging**: Fix, the segfault non-deployment handler needs to
   disable itself before doing anything else.

-  **Plugins**: Fix, the warning to choose a GUI plugin for
   ``matplotlib`` was given with ``tk-inter`` plugin enabled still,
   which is of course not appropriate.

-  **Distutils**: Fix, do not recreate the build folder with
   ``.gitignore`` contained.

   We were re-creating it as soon as we looked at what it would be, now
   it's created only when asking for that to happen.

-  **No-GIL**: More changes for dictionaries needed

   Fix compile errors for the free-threaded dictionary implementation
   were needed after a hotfix for 2.7 broke it.

-  **Compatibility**: Fix 3.12 generic classes and generic type
   declarations.

-  **macOS**: Fix entitlements were not properly given for code signing.

-  **Onefile**: Fix, was delaying shutdown for terminal applications in
   onefile DLL mode.

   Was waiting for non-used child processes, which don't exist and then
   the timeout for that operation, which is always happening on CTRL-C
   or terminal shutdown.

-  Python3.13: Fix, seems interpreter frames with None code objects
   exist and need to be handled as well.

-  **Standalone**: Fix, need to allow for ``setuptools`` package to be user
   provided.

-  **Windows:** Avoid using non-encodable dist and build folder names

   Some paths don't become short, but still be non-encodable from the
   file system for tools, in these cases use temporary filenames to
   avoid errors from C compilers and other tools.

-  Python3.13: Fix, ignore stdlib ``cgi`` module that might be left over
   from previous installs

   The module was removed during development, and if you install over an
   old alpha version of 3.13 a newer Python, Nuitka would crash on it.

-  **macOS**: Need to allow ``lib`` folder for Python Build Standalone
   flavor.

-  **macOS**: Need to allow libraries for ``rpath`` resolution to be found
   in all of Homebrew folders.

-  **Onefile**: Need to allow ``..`` in paths to allow outside
   installation paths.

Package Support
===============

-  **Standalone**: Introduced support for the ``nicegui`` package.
   (Added in 2.7.1 already.)

-  **Standalone**: Extended support to include ``xgboost.core`` on
   **macOS**. (Added in 2.7.1 already.)

-  **Standalone**: Added needed data files for ``ursina`` package.
   (Added in 2.7.1 already.)

-  **Standalone**: Added support for newer versions of the ``pydantic``
   package. (Added in 2.7.4 already.)

-  **Standalone**: Extended ``libonnxruntime`` support to **macOS**,
   enabling its use in compiled applications on this platform. (Added in
   2.7.4 already.)

-  **Standalone**: Added necessary data files for the ``pygameextra``
   package. (Added in 2.7.4 already.)

-  **Standalone**: Included GL backends for the ``arcade`` package.
   (Added in 2.7.4 already.)

-  **Standalone**: Added more data directories for the ``ursina`` and
   ``panda3d`` packages, improving their out-of-the-box compatibility.
   (Added in 2.7.4 already.)

-  **Standalone**: Added support for newer ``skimage`` package. (Added
   in 2.7.5 already.)

-  **Standalone**: Added support for the ``PyTaskbar`` package. (Added
   in 2.7.6 already.)

-  **macOS**: Added ``tk-inter`` support for Python 3.13 with official
   CPython builds, which now use framework files for Tcl/Tk. (Added in
   2.7.6 already.)

-  **Standalone**: Added support for the ``paddlex`` package. (Added in
   2.7.6 already.)

-  **Standalone**: Added support for the ``jinxed`` package, which
   dynamically loads terminal information. (Added in 2.7.6 already.)

-  **Windows**: Added support for the ``ansicon`` package by including a
   missing DLL. (Added in 2.7.6 already.)

-  **macOS**: Enhanced configuration for the ``pypylon`` package,
   however, it's not sufficient. (Added in 2.7.6 already.)

-  **Standalone**: Added support for newer ``numpy`` versions. (Added in
   2.7.7 already.)

-  **Standalone**: Added support for older ``vtk`` package. (Added in
   2.7.8 already.)

-  **Standalone**: Added support for newer ``certifi`` versions that use
   ``importlib.resources``. (Added in 2.7.9 already.)

-  **Standalone:** Added support for the ``reportlab.graphics.barcode``
   module. (Added in 2.7.9 already.)

-  **Standalone**: Added support for newer versions of the
   ``transformers`` package. (Added in 2.7.11 already.)

-  **Standalone**: Added support for newer versions of the ``sklearn``
   package. (Added in 2.7.12 already.)

-  **Standalone**: Added support for newer versions of the ``scipy``
   package. (Added in 2.7.12 already.)

-  **Standalone**: Added support for older versions of the ``cv2``
   package (specifically version 4.4). (Added in 2.7.12 already.)

-  **Standalone**: Added initial support for the ``vllm`` package.
   (Added in 2.7.12 already.)

-  **Standalone**: Ensured all necessary DLLs for the ``pygame`` package
   are included. (Added in 2.7.12 already.)

-  **Standalone**: Added support for newer versions of the
   ``zaber_motion`` package. (Added in 2.7.13 already.)

-  **Standalone**: Added missing dependencies for the ``pymediainfo``
   package. (Added in 2.7.13 already.)

-  **Standalone**: Added support for newer versions of the ``sklearn``
   package by including a missing dependency. (Added in 2.7.13 already.)

-  **Standalone**: Added support for newer versions of the ``toga``
   package. (Added in 2.7.14 already.)

-  **Standalone**: Added support for the ``wordninja-enhanced`` package.
   (Added in 2.7.14 already.)

-  **Standalone**: Added support for the ``Fast-SSIM`` package. (Added
   in 2.7.14 already.)

-  **Standalone**: Added a missing data file for the ``rfc3987_syntax``
   package. (Added in 2.7.14 already.)

-  **Standalone**: Added missing data files for the ``trimesh`` package.
   (Added in 2.7.15 already.)

-  **Standalone**: Added support for the ``gdsfactory``, ``klayout``,
   and ``kfactory`` packages. (Added in 2.7.15 already.)

-  **Standalone**: Added support for the ``vllm`` package. (Added in
   2.7.16 already.)

-  **Standalone**: Added support for newer versions of the
   ``tkinterweb`` package. (Added in 2.7.15 already.)

-  **Standalone**: Added support for newer versions of the
   ``cmsis_pack_manager`` package. (Added in 2.7.15 already.)

-  **Standalone**: Added missing data files for the ``idlelib`` package.
   (Added in 2.7.15 already.)

-  **Standalone**: Avoid including debug binary on non-Windows for Qt
   Webkit.

-  **Standalone**: Add dependencies for **pymediainfo** package.

-  **Standalone**: Added support for ``winpty`` package.

-  **Standalone:** Added support for newer versions of the ``gi``
   package.

-  **Standalone:** Added support for newer versions of the ``litellm``
   package.

-  **Standalone**: Added support for the ``traits`` package.

-  Standalone: Added support for ``pyface`` package.

-  **Standalone:** Added support for newer ``transformers`` package.

-  **Standalone**: Added data files for "rasterio" package.

-  **Standalone**: Added support for "ortools" package.

-  Standalone: Added support newer "vtk" package

New Features
============

-  **Python3.14**: Added experimental support for Python3.14, not
   recommended for use yet, as this is very fresh and might be missing a
   lot of fixes.

-  **Release**: Added an extra dependency group for the Nuitka
   build-backend, intended for use in ``pyproject.toml`` and other
   build-system dependencies. To use it depend in
   ``Nuitka[build-wheel]`` instead of Nuitka. (Added in 2.7.7 already.)

   For release we also added ``Nuitka[onefile]``,
   ``Nuitka[standalone]``, ``Nuitka[app]`` as extra dependency groups.
   If icon conversions are used, e.g.
   ``Nuitka[onefile,icon-conversion]`` adds the necessary packages for
   that. If you don't care about what's being pulled in ``Nuitka[all]``
   can be used, by default ``Nuitka`` only comes with the bare minimum
   needed and will inform about missing packages.

-  **macOS**: Added options ``--macos-sign-keyring-filename`` and
   ``--macos-sign-keyring-password`` to automatically unlock a keyring
   for use during signing. This is very useful for CI where no UI prompt
   can be used.

-  **Windows**: Detect when ``input`` cannot be used due to no console
   or the console not providing proper standard input and produce a
   dialog for entry instead. Shells like ``cmd.exe`` execute inputs as
   commands entered when attaching to them. With this, the user is
   informed to make the input into the dialog instead. In case of no
   terminal, this just brings up the dialog for GUI mode.

-  **Plugins**: Introduced ``global_change_function`` to the anti-bloat
   engine, allowing function replacements across all sub-modules of a
   package at once. (Added in 2.7.6 already.)

-  **Reports**: For Python 3.13+, the compilation report now includes
   information on GIL usage. (Added in 2.7.7 already.)

-  **macOS**: Added an option to prevent an application from running in
   multiple instances. (Added in 2.7.7 already.)

-  **AIX**: Added support for this OS as well, now standalone and module
   mode work there too.

-  **Scons**: When C a compilation fails to due warnings in ``--debug``
   mode, recognize that and provide the proper extra options to use if
   you want to ignore that.

-  **Non-Deployment**: Added non-deployment handler to catch modules
   that error exit on import, while assumed to work perfectly.

   This will give people an indication that the ``numpy`` module is
   expected to work and that maybe just the newest version is not and
   we need to be told about it.

-  **Non-Deployment**: Added non-deployment handler for
   ``DistributionNotFound`` main program exception exits that point the
   user to metadata options needed.

-  **UI**: Make ``--include-data-files-external`` the main option name
   for put data files alongside the created program.

   This now works with standalone mode too, and is no longer onefile
   specific, the name should reflect that and people can now use it more
   broadly.

-  **Plugins**: Added support for multiple warnings of the same kind.
   The ``dill-compat`` plugin needs that as it supports multiple
   packages.

-  **Plugins**: Added detector for the ``dill-compat`` plugin that
   detects usages of ``dill``, ``cloudpickle`` and ``ray.cloudpickle``.

-  **Standalone**: Add support for including Visual Code runtime dlls on
   Windows

   -  When MSVC (Visual Studio) is installed, we take the runtime DLLs
      from its folders. We couldn't take the ones from the ``redist``
      packages installed to system folders legally.

   -  Gives a warning when these DLLs would be needed, but were not
      found.

   -  We might want to add an option later to exclude them again, for
      size purposes, but correctness out of the box is more important
      for now.

-  **UI**: Make sure the distribution name is correct for
   ``--include-distribution-metadata`` values.

-  **Plugins**: Added support for configuring re-compilation of extension
   modules from their source code.

   -  When we have both Python code and an extension module, we only had
      a global option available on the command line.

   -  This adds ``--recompile-extension-modules`` for more fine grained
      choices as it allows to specify names and patterns.

   -  For ``zmq`` we need to enforce it to never be compiled, as it
      checks if it is compiled with Cython at runtime, so re-compilation
      is never possible.

-  **Reports**: Include environment flags for C compiler and linker
   picked up for the compilation. Sometimes these cause compilation
   errors that and this will reveal there presence.

Optimization
============

-  Enhanced detection of ``raise`` statements that use compile-time
   constant values which are not actual exception instances.

   This improvement prevents **Nuitka** from crashing during code
   generation when encountering syntactically valid but semantically
   incorrect code, such as ``raise NotImplemented``. While such code is
   erroneous, it should not cause a compiler crash. (Added in 2.7.1
   already.)

-  With unknown locals dictionary variables trust very hard values there
   too.

   -  With this using hard import names also optimize inside of classes.
   -  This makes ``gcloud`` metadata work, which previously wasn't
      resolved in their code.

-  **macOS**: Enhanced ``PySide2`` support, removing the general
   requirement for onefile mode. Onefile mode is now only enforced for
   ``QtWebEngine`` due to its specific stability issues if not bundled
   this way. (Added in 2.7.4 already.)

-  **Scons:** Added support for C23 embedding of the constants blob with
   ClangCL too avoiding the use of resources. Since the onefile
   bootstrap doesn't yet honor this for its payload, this is still not
   complete but could help with size limitations in the future.

-  **Plugins:** Overhaul of the UPX plugin.

   Use better compression than before, hint the user at disabling
   onefile compression where applicable to avoid double compression.
   Output warnings for files that are not considered compressible. Check
   for ``upx`` binary sooner.

-  **Scons**: Avoid compiling hacl code for macOS where it's needed.

Anti-Bloat
==========

-  Improved handling of the ``astropy`` package by implementing global
   replacements instead of per-module ones. Similar global handling has
   also been applied to ``IPython`` to reduce overhead. (Added in 2.7.1
   already.)

-  Avoid ``docutils`` usage in the ``markdown2`` package. (Added in 2.7.1
   already.)

-  Reduced compiled size by avoiding the use of "docutils" within the
   ``markdown2`` package. (Added in 2.7.1 already.)

-  Avoid including the testing framework from the ``langsmith`` package.
   (Added in 2.7.6 already.)

-  Avoid including ``setuptools`` from ``jax.version``. (Added in 2.7.6
   already.)

-  Avoid including ``unittest`` from the ``reportlab`` package. (Added
   in 2.7.6 already.)

-  Avoid including ``IPython`` for the ``keras`` package using a more
   global approach. (Added in 2.7.11 already.)

-  Avoid including the ``triton`` package when compiling
   ``transformers``. (Added in 2.7.11 already.)

-  Avoid a bloat warning for an optional import in the ``seaborn``
   package. (Added in 2.7.13 already.)

-  Avoid compiling generated ``google.protobuf.*_pb2`` files. (Added in
   2.7.7 already.)

-  Avoid including ``triton`` and ``setuptools`` when using the
   ``xformers`` package. (Added in 2.7.16 already.)

-  Refined ``dask`` support to not remove ``pandas.testing`` when
   ``pytest`` usage is allowed. (Added in 2.7.16 already.)

-  Avoid compiling the ``tensorflow`` module that is very slow and contains
   generated code.

-  Avoid using ``setuptools`` in ``cupy`` package.

-  Avoid false bloat warning in ``seadoc`` package.

-  Avoid using ``dask`` in ``sklearn`` package.

-  Avoid using ``cupy.testing`` in ``cupy`` package.

-  Avoid using "IPython" in "roboflow" package.

-  Avoid including "ray" for "vllm" package.

-  Anti-Bloat: Avoid using "dill" in "torch" package.

Organizational
==============

-  **UI**: Remove obsolete options to control the compilation mode from
   help output. We are keeping them only to not break existing
   workflows, but ``--mode=`` should be used now and these options will
   start triggering warnings soon.

-  **Python3.13.4**: Reject broken CPython official release for Windows.

   The link library included is not the one needed for GIL, and as such
   it breaks Nuitka heavily and must be errored out on, all smaller or
   larger micro versions work, but this one does not.

-  **Release**: Do not use Nuitka 2.7.9 as it broke data file access via
   ``__file__`` in onefile mode on Windows. This is a brown paper bag
   release, with 2.7.10 containing only the fix for that. Sorry for the
   inconvenience.

-  **Release**: Ensured proper handling of newer ``setuptools`` versions
   during Nuitka installation. (Fixed in 2.7.4 already.)

-  **UI**: Sort ``--list-distribution-metadata`` output and remove
   duplicates. (Changed in 2.7.8 already.)

-  **Visual Code**: Added Python2.6 config for Win32 to use for
   comparisons, still checking things there a lot.

-  **UI**: List available Qt plugin families if ``--include-qt-plugin``
   cannot find one.

-  **UI**: Warn about compiling a file named ``__main__.py`` which
   should be avoided, instead you should specify the package directory
   in that case.

   -  **UI**: Make it an error to compile a file named ``__init__.py``
      for standalone mode.

-  **Debugging**: Also find files for ``--edit`` for temporary file
   paths that are not short, but long paths.

-  **Debugging**: Make the ``pyside6`` plugin enforce
   ``--no-debug-immortal-assumptions`` when ``--debug`` is on because
   PySide6 violates these and we don't need Nuitka to check for that
   then as it will abort when it finds them.

-  **Quality**: Avoid writing auto-formatted files with same contents

   -  That avoids stirring up tools that listen to changes.
   -  For example the Nuitka website auto-builder otherwise rebuilt per
      release post on docs update.

-  **Quality**: Use latest version of ``deepdiff``.

-  **Quality**: Added autoformat for JSON files.

-  **Release**: The man pages were using outdated options and had no
   example for standalone or app modes. Also the actual options were no
   longer included.

-  **GitHub**: Use the ``--mode`` options in the issue template as well.

-  **GitHub**: Enhanced wordings for bug report template to give more
   directions and more space for excellent reports to be made.

-  **GitHub**: Also ask for output of our own package metadata listing
   tool as it contains more information about Nuitka seeing things.

-  **Debugging**: Don't disable all warnings with Clang, this has went
   unnoticed for a long time and prevented a few things from being
   recognized.

-  **Debugging**: Support arbitrary debuggers through
   `--debugger-choice`.

      Support arbitrary debuggers for use in the ``--debugger`` mode, if
      you specify all of their command line you can do anything there.

      Also added predefined ``valgrind-memcheck`` mode for memory
      checker tool of Valgrind to be used.

-  **UI**: Added rich as a progress bar that can be used. Since it's
   available in pip these days, it can be found most likely and needs no
   inline copy. Add colors and similar behavior for ``tqdm`` as well.

-  **UI**: Remove obsolete warning for Linux with ``upx`` plugin.

   We don't use ``appimage`` anymore for a while now, so its constraints
   do not matter.

-  **UI:** Add warnings for module specific options too. The logic to
   not warn on GitHub Actions was inverted, this restores warnings for
   normal users.

-  **UI**: Output the module name in question for ``options-nanny``
   plugin and parameter warnings.

-  **UI**: When a forbidden import comes from an implicit import, report
   that properly.

   Sometimes ``.pyi`` files from extension modules cause an import, but
   it wasn't clear which one, now it will be giving the module causing
   it.

-  **UI**: More clear error message in case a Python for scons was not
   found.

-  **Actions**: Cover debug mode compilation at least once.

-  **Quality**: Resolve paths from all OSes in ``--edit``. Sometime I
   want to look at a file on the wrong OS still, and there is no need to
   enforce being on the same one for resolutions to work.

-  **Actions**: Use newer Ubuntu for testing, otherwise we weren't able
   to get ``clang-format`` installed anymore.

-  **Debugging:** Allow for C stack output in signal handlers, this is
   most useful when doing the non-deployment handler that catches them
   to know where they came from more precisely.

-  **UI**: Show no-GIL in output of Python flavor in compilation if
   relevant.

Tests
=====

-  Removed Azure CI configuration, as testing has been fully migrated to
   GitHub Actions. (Changed in 2.7.9 already.)

-  Improved test robustness against short paths for package-containing
   directories. (Added in 2.7.4 already.)

-  Prevented test failures caused by rejected download prompts during
   test execution, making CI more stable. (Added in 2.7.4 already.)

-  Refactored common testing code to avoid using ``doctests``,
   preventing warnings in specific standalone mode test scenarios
   related to reference counting. (Added in 2.7.4 already.)

-  Tests: Cover the memory leaking call re-formulation with a reference
   count test.

Cleanups
========

-  **Plugins**: Improved ``pkg_resources`` integration by using the
   ``__loader__`` attribute of the registering module for loader type
   registration, avoiding modification of the global ``builtins``
   dictionary. (Fixed in 2.7.2 already.)

-  Improved the logging mechanism for module search scans. It is now
   possible to enable tracing for individual ``locateModule`` calls,
   significantly enhancing readability and aiding debugging efforts.

-  **Scons**: Refactored architecture specific options into dedicated
   functions to keep the code more clear.

-  **Spelling**: Cleanups

   -  Avoid using ``#ifdef`` in C code templates, and lets just avoid it
      generally.

   -  Added missing slot function names to the ignored word list.

   -  Renamed variables related to slots to be more verbose and proper
      spelling as a result, as that's for better understanding of their
      use anyway.

-  **Scons**: Specify versions supported for Scons by excluding the ones
   that are not rather than manually maintaining a list. This adds
   support for using Python 3.14 automatically.

-  **Plugins**: Remove useless use of ``intern`` as it doesn't do what I
   thought it does.

-  Attach copyright during code generation for code specializations

   -  This also enhances the formatting for almost all files by making
      leading and trailing new lines more consistent.
   -  One C file turns out unused and was removed as a left over from a
      previous refactoring.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
