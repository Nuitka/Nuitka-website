:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per-version changes and comments for the
upcoming Nuitka |NUITKA_VERSION_NEXT| as a draft about hot-fixes of the
current stable release as |NUITKA_VERSION| as well.

****************************
 Nuitka Release 2.7 (Draft)
****************************

.. note::

   This a draft of the release notes for 2.7, which is supposed to add
   enhanced 3.13 compatibility, and lots of scalability in general,
   aiming at an order of magnitude improvement for compile times.

This release is in progress still and documentation might lag behind
development.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  **macOS**: Fix, need to also recognize self-dependencies of DLLs with
   architecture suffix on ``x86_64``. Fixed in 2.6.1 already.

-  **Standalone:** Fix, wasn't detecting ``.pyi`` files with versioned
   extension module filenames. Fixed in 2.6.1 already.

-  **Standalone:** Fix, single line triple quotes were breaking the
   ``.pyi`` file parsing. Fixed in 2.6.1 already.

-  **Standalone:** Fix, for ``__init__`` as extension modules, the
   origin path of ``__spec__`` was wrong. Fixed in 2.6.1 already.

   This mostly only affected the module ``repr`` string, but some code
   could also use ``origin`` to locate something and run into errors as
   a result. Fixed in 2.6.1 already.

-  **Multidist:** Fix, binaries now use the name they launched with.

   Before they were using the path of the actual running binary, which
   made it "ineffective" if explicitly launched through a different
   process name. Now entrypoints can be invoked from a single binary
   using ``subprocess`` with process names. Fixed in 2.6.1 already.

-  **Windows**: Fix, when attaching to a console with
   ``--windows-console-mode=attach`` and no terminal present, the
   ``sys.stdin`` was not actually usable and lead to errors when forking
   processes. Fixed in 2.6.1 already.

-  **Modules:** Fix, was crashing in module mode on importlib
   distribution calls that would be optimizable, but due to module mode
   are not. Fixed in 2.6.1 already.

-  **Python3:** Fix, for namespace packages, not providing a
   ``path_finder`` was leading to errors with newer setuptools versions.
   Fixed in 2.6.1 already.

-  **Windows:** Fix, one header file had a UTF-8 comment that could
   cause MSVC to properly compile on systems with some locales. Fixed in
   2.6.2 already.

-  **Standalone:** Fix, need to clear all associated tags for data files
   discovered, if they are inhibited by the user, otherwise plugins can
   get confused. Fixed in 2.6.2 already.

-  **Standalone:** Fix, ``pkgutil.iter_modules`` could fail to list all
   modules.

   When a directory for the package exists, the file finder of Python
   could take our package responsibility, giving very incomplete results
   that do not contained compiled modules. Fixed in 2.6.2 already.

-  **Windows** Fix, with onefile compression there was a C warning on 32
   bit Windows when compiling the bootstrap.

-  **Python3.12+**: Fix, accessing the module attribute of ``type``
   variables gave a ``SystemError`` exception.

-  **Metadata**: Fix, reading record data from distribution files may
   not be possible in some cases, as the files don't always exist. Fixed
   in 2.6.3 already.

-  **Compatibility:** Fix, for used shared libraries that were symbolic
   links, on non-Windows the dependencies were not properly resolved if
   they came from the symlink target and that was not in the system path
   for libraries, or nearby in symlink form as well. Fixed in 2.6.3
   already.

-  **Standalone:** Avoid using ``msvcp140.dll`` from ``PySide6``
   (actually ``shiboken6``) for other packages, they may not be
   compatible with it causing crashes. Fixed in 2.6.3 already.

-  **Standalone:** Fix, comments after imports could break the ``.pyi``
   file parsing. Fixed in 2.6.3 already.

-  **UI:** Fix, output of listing DLLs and EXE didn't supply correct
   sub-folders anymore. Fixed in 2.6.3 already.

-  **macOS:** Fix, icons were no longer attached to application bundles.
   Fixed in 2.6.3 already.

-  **Onefile:** Fix, this gave a C compiler warning on 32 bit Windows
   due to lack of type conversion for decompression buffer size. Fixed
   in 2.6.3 already.

-  **Python3.12+**: Fix, must type aliases had not usable ``module``
   attribute with the containing module name. Fixed in 2.6.3 already.

-  **Python3.12+**: Fix, type aliases were not fully compatible for
   values as well.

   We were creating them in the wrong way for compound type aliases
   leading to errors in uses like ``pydantic`` schemas. Fixed in 2.6.5
   already.

-  **Python3.12+**: Workaround for failure to set package context for
   extension modules causing major compatibility issues previously.

   Without static libpython we don't have the ability to set the package
   context and then extension modules corrupt global namespace by
   creating a module without the package name. This can collide with
   existing package names. For ``PySide6QtAds`` package this was
   happening. Protect against that by saving and restoring old module
   value and correct the loaded module name afterwards.

   Previously, e.g. ``PySide6.QtWidgets`` was loaded as ``QtWidgets`` as
   well in ``sys.modules`` and that was corrected by the Nuitka loader
   storing it under the correct name as well, only.

   Also rename further sub-modules potentially created by extension
   modules during their load already. This should increase its coverage
   by a lot. We had manually done this for ``onnx`` and ``mediapipe`` so
   far, but e.g. ``paddleocr`` was affected too, any maybe other
   packages. Most recently new ``scipy`` added itself to that list.

   The most important platform this impacts is Windows and also macOS if
   using official CPython flavor. Fixed in 2.6.6 already.

-  **Plugins:** In case of data files not naively found, the
   ``get_data`` helper function for Nuitka Package Configuration crashed
   on the fallback to ``pkgutil``. Fixed in 2.6.6 already.

-  **Standalone:** For DLLs in sub-folders the r-path value used for
   finding used DLLs on non-Windows, didn't include the DLLs's own
   folder ``$ORIGIN`` but only the folders above, on some cases that
   prevented those DLLs from loading. Fixed in 2.6.7 already.

-  **Standalone:** Treat shared library dependencies with paths as if
   they were given as ``rpaths`` as well.

   This fixes builds using for Pythons that like **Python Build
   Standalone** (the Python distribution installed by uv), which have an
   ``$ORIGIN``-relative libpython dependency that should be respected as
   well. Fixed in 2.6.7 already.

-  **Python3:** Fix, generators need to preserve outside exceptions and
   restore their own on resume. Otherwise when used as context managers
   and handling an exception wit ha yield, an other ``with`` statement
   could not be able to re-raise its own exception if any occurs in its
   body. Fixed in 2.6.7 already.

-  **Android:** Fix, standalone builds were retaining the Termux
   ``rpath`` value pointing into its installation, which after APK
   packaging wouldn't have any effect due to how Android security works,
   but it shouldn't be there. Fixed in 2.6.7 already.

-  **Python Build Standalone**: Add rpath to where libpython is in all
   modes by default and not just where we think it may be needed. This
   fixes Pythons that have a ``libpython`` that is uninstalled on
   **Linux**. Fixed in 2.6.8 already.

-  **Standalone:** Older Linux didn't work due to newer ``patchelf``
   options being used starting with the 2.6.8 ``rpath`` changes. Fixed
   in 2.6.9 already.

-  **Python3.9**: Fix, older ``importlib.metadata`` versions errored out
   for ``spacy`` plugin. Fixed in 2.6.8 already.

-  **Standalone**: Fix, ``requests`` package imports could be corrupted
   to be a sub-package instead. Fixed in 2.6.8 already.

-  **Distutils on macOS**: Fixup for distutils integration with
   extension modules scanned, the architecture is hard to know. Fixed in
   2.6.8 already.

-  **Windows**: Fix, need to define ``dotnet`` as a dependency to
   properly use it enabling all UI features.

-  **Scons:** : Fix, need to make sure to use proper ``link`` executable
   for MSVC backend compiler, and not e.g. the one that ``git`` adds to
   ``PATH`` potentially. Fixed in 2.6.9 already.

-  **Scons:** : Fix, avoid using ``config.txt`` with ``clcache`` as used
   when using MSVC. It can exhibit a race during first use with two
   ``clcache`` threads trying to create it and failing it. Solved by not
   writing or reading it at all and using default values instead. Fixed
   in 2.6.9 already.

-  **Standalone:** Fix, need to load extension modules during
   ``create_module`` of our loader already to be compatible.

   Doing it later in ``exec_module`` seems to at least broken ``mypy``
   created extension modules as used in the ``black`` package for
   example.

Package Support
===============

-  **Standalone:** Added data files needed for ``blib2to3`` package.
   Added in 2.6.1 already.

-  **Standalone:** Added support for newer ``numba`` package. Added in
   2.6.2 already.

-  **Standalone:** Added support for newer ``huggingface_hub`` package.
   Added in 2.6.2 already.

-  **Anti-Bloat:** Fix, need to provide more ``numpy.testing`` stubs,
   otherwise some ``sklearn`` modules didn't properly execute. Fixed in
   2.6.2 already.

-  **Standalone:** Enhanced configuration for ``fontTools`` package. Do
   not configure hidden dependencies that we now detect by looking at
   the provided Python files as if they were ``.pyi`` files. Fixed in
   2.6.2 already.

-  **Standalone:** Fix, for newer ``PySide6`` plugin ``sqldrivers`` on
   macOS. Fixed in 2.6.3 already.

-  **Python3.12+**: Added standalone mode support for ``mediapipe``
   package with Python3.12+, with a workaround for the problems of
   extension modules creating sub-modules. Fixed in 2.6.3 already.

-  **Python3.12+**: Added standalone mode support for ``onnx`` package
   with Python3.12+, with a workaround for the problems of extension
   modules creating sub-modules. Fixed in 2.6.3 already.

-  **Standalone:** Added support for newer ``sqlglot`` package. Added in
   2.6.5 already.

-  **Standalone:** Include ``asset`` data files of ``arcade`` package,
   too. Added in 2.6.5 already.

-  **Standalone:** Added implicit dependencies for ``sqlalchemy.orm``.
   Added in 2.6.5 already.

-  **MacOS:** Fix, need more frameworks including for PySide 6.8
   web-engine. Added in 2.6.5 already.

-  **Standalone:** Enhanced ``cv2`` package support, config files
   apparently can be Python minor version specific as well, make data
   files reading in plugins allowed to find them only optionally. Added
   in 2.6.6 already.

-  **Standalone:** Added support for ``scipy`` sub-module loader. They
   can be used without explicit support, by handling it as a lazy
   loader, we see these implicit dependencies as well. Added in 2.6.7
   already.

-  **Standalone:** Include django db engine modules automatically as
   well. Added in 2.6.7 already.

-  **Homebrew:** Added support for ``tk-inter`` with Python versions
   with **Tcl/Tk** version 9.

-  **Standalone:** Added missing datafile for ``jenn`` package.

-  **Standalone**: Added support for newer ``scipy.optimize._cobyla``
   package. Fixed in 2.6.8 already.

New Features
============

-  **DLL:** Added new mode to produce standalone DLL distributions

   This is experimental at this time, but appears to work for many
   things, however documentation is very weak right now. Multiprocessing
   and potentially other things will need help from launched binary, and
   that's not currently working.

   Intended for improvement of Windows GUI compatibility with tray icons
   and notifications in onefile mode, which will use this internally.

-  **Windows:** The onefile mode is now using internally DLL mode and
   properly interacts with a created DLL rather than an executable when
   used in temporary mode. Use ``--onefile-no-dll`` to deactivate it
   if it is causing any issues.

-  **Windows:** Added support for Windows ARM and dependency analysis.
   We do it via ``pefile`` since dependency walker doesn't know about
   ARM.

-  **Android:** Added support for module mode with Termux Python as
   well. Added in 2.6.7 already.

-  **Compatibility** Added support for **Python Build Standalone** as
   downloaded by ``uv`` potentially, albeit it doesn't support static
   ``libpython`` as the included one is currently unusable. Added in
   2.6.7 already.

-  **Windows:** Enable taskbar grouping, if product name and company
   name are present in version information. Added in 2.6.4 already.

-  **Windows:** Use icons given for Windows automatically with
   ``PySide6``, this removes the need to also provide the application
   icon as a PNG file, which was duplicating it.

-  **Nuitka Package Configuration:** Allow using values of ``constants``
   ``variable`` declarations in ``when`` conditions where possible.

-  **Reports:** Make it clear if a package is "vendored", which is the
   case for ``setuptools`` contained packages if used from there.

Optimization
============

-  Avoid API call for finalizer usage in compiled generator, coroutines,
   and asyncgen. These had been added in Nuitka 2.6 to achieve enhanced
   compatibility but could slow down their operation, this change undoes
   that effect.

Anti-Bloat
==========

-  Avoid using ``matplotlib`` from ``tqdm`` package. Added in 2.6.2
   already.

-  Avoid using ``matplotlib`` from ``scipy`` package. Added in 2.6.2
   already.

-  Avoid using ``cython`` from the ``fontTools`` package. Added in 2.6.2
   already.

-  Avoid using ``sparse`` from ``scipy`` package. Added in 2.6.3
   already.

-  Avoid using ``ndonnx`` from ``scipy`` package. Added in 2.6.3
   already.

-  Avoid using ``setuptools`` for ``jaxlib`` package. Also do not call
   git to attempt and query the version from ``jaxlib`` source code.
   Added in 2.6.3 already.

-  Avoid using ``yaml`` from ``scipy`` package. Added in 2.6.4 already.

-  Avoid using ``charset_normalizer`` for ``numpy`` package. Added in
   2.6.5 already.

-  Avoid using ``lxml`` for ``pandas`` package. Added in 2.6.5 already.

-  Avoid using ``PIL`` for ``sklearn`` package. Added in 2.6.5 already.

-  Avoid ``numba`` in ``smt`` package. Added in 2.6.7 already.

-  Avoid more ``pygame`` optional dependencies. Added in 2.6.8 already.

Organizational
==============

-  **UI:** Enhanced output for used command line options

   -  Use the report path for filenames given as positional arguments,
      this is often the compiled file.
   -  Format info traces with a potential leader, allows intended values
      to be output, this makes the trace much more readable.

-  **Reports:** Save and restore timing information for cached modules

   -  In this way, we don't have a difference if a module is loaded from
      cache or not, which helps a lot in Nuitka-Watch where previously
      every new compilation yielded changes for the timing of those
      modules.

   -  Should make our life for **Nuitka-Watch** much easier by avoiding
      this noise.

-  **Actions:** Add compilation report artifacts to all empty module
   compilations.

-  **Debugging:** For ``--edit`` also find modules from ``.app`` paths
   as produced by application bundled on macOS. Added in 2.6.1 already.

-  **User Manual:** Updated example for Nuitka-Action, we should
   probably just point to its documentation instead. Changed in 2.6.1
   already.

-  **Quality:** Make sure all our C files are ASCII, to avoid unicode
   sneaking in as it did.

-  **Quality:** Check ``global_replacements`` result value for proper
   Python syntax as well, like we do for ``replacements`` already. Also
   check the ``global_replacements_re`` and ``replacements_re`` variants
   if the result value is actually a valid regular expression.

-  **Plugins**: When illegal module names are given for implicit
   imports, properly report plugin name.

-  **Quality:** Use ``clang-format-21`` if available. Applied changes
   only newest version do.

-  **Quality**: Avoid warnings with Python3.12+ from ``pylint`` for
   ``setuptools`` package use.

Tests
=====

-  None yet

Cleanups
========

-  None yet

Summary
=======

This release is not complete yet.

.. include:: ../dynamic.inc
