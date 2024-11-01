:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per-version changes and comments for the
upcoming Nuitka |NUITKA_VERSION_NEXT| as a draft about hot-fixes of the
current stable release as |NUITKA_VERSION| as well.

****************************
 Nuitka Release 2.5 (Draft)
****************************

.. note::

   This a draft of the release notes for 2.5, which is supposed to add
   Nuitka standalone backend support and enhanced 3.12 performance and
   scalability in general.

   The main focus shall be scalability and a few open issues for
   performance enhancements that later Python versions enable us to.

This release in not complete yet.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  Windows: The onefile handling of ``sys.argv`` was seriously regressed
   for program and command line paths with spaces. Fixed in 2.4.4
   already.

-  Windows: Fix, console output handles were opened with close file
   handles, but that is not allowed. Fixed in 2.4.2 already.

-  Standalone: Fix, using trailing slashes to mark the target directory
   for data files no longer worked on Windows. Fixed in 2.4.2 already.

-  Fix, the ``.pyi`` parser could fail for relative imports. This could
   break some packages that are extension modules, but with source code
   available too. Fixed in 2.4.3 already.

-  Modules: Fix, extension modules didn't load into packages with
   Python3.12. Fixed in 2.4.4 already.

-  Windows: Fix, command line handling for onefile mode on was not fully
   compatible with quoting. Fixed in 2.4.4 already.

-  Fix, accept non-normalized paths on the command line for data
   directories. Fixed in 2.4.5 already.

-  Python3.11: Fix, ``inspect`` module functions could raise
   ``StopIteration`` looking at compiled functions on the stack. Fixed
   in 2.4.5 already.

-  Fix, cannot trust that ``importlib_metadata`` always works, it some
   situations it's actually broken and that could crash the compilation
   then. Fixed in 2.4.5 already.

-  Plugins: Fix, ``no_asserts`` yaml configuration was crashing the
   compilation. Fixed in 2.4.6 already.

-  Scons: Fix, need to read ccache log files error tolerant. Otherwise
   on Windows it can crash for non-ASCII module names or paths. Fixed in
   2.4.11 already.

-  Scons: Fix, specifying the C standard should not be done towards C++
   compilers. For splash screen on Windows we use C++ and the Clang
   rejects this option there. Fixed in 2.4.8 already.

-  macOS: Handle one more oddity with self-dependencies. Can apparently
   switch freely between ``.so`` and ``.dylib`` for self-dependencies.
   Fixed in 2.4.8 already.

Fix, leaked a reference to the object compiled methods are associated to
when ``deepcopy`` is used on them. Fixed in 2.4.9 already.

-  MSYS2: Fix, need to consider ``bin`` directory not as system DLL
   folder for DLL inclusion. Fixed in 2.4.9 already.

-  Python3.10+: Fix, failed ``match`` of class with args could crash.
   Fixed in 2.4.9 already.

-  MSYS2: Workaround for not normalized ``/`` from ``os.path.normpath``
   on this Python flavor. Fixed in 2.4.11 already.

-  Fix, with 3.12.7 our constant code was triggering assertions. Fixed
   in 2.4.10 already.

-  Fix, the ``--include-package`` didn't include extension modules that
   are sub-modules of the package, but only Python modules. Fixed in
   2.4.11 already.

Package Support
===============

-  Standalone: Improved ``arcade`` configuration. Added in 2.4.3
   already.

-  Standalone: Add data file for ``license-expression``. package Added
   in 2.4.6 already.

-  Standalone: Added missing implicit dependency for ``pydantic`` needed
   for deprecated decorators to work. Fixed in 2.4.5 already.

-  Standalone: Added missing implicit dependency for ``spacy`` package.
   Added in 2.4.7 already.

-  Standalone: Added support for newer ``trio`` package. Added in 2.4.8
   already.

-  Standalone: Added support for newer ``tensorflow`` package. Added in
   2.4.8 already.

-  Standalone: Added support for ``pygame-ce``. Added in 2.4.8 already.

-  Standalone: Added support for newer ``toga`` on Windows. Added in
   2.4.9 already.

-  Fix, workaround ``django`` debug wanting to extract column numbers of
   compiled frames. Added in 2.4.9 already.

-  Standalone: Allow more potentially unusable plugins for ``PySide6``
   to be recognized on macOS. Added in 2.4.9 already.

-  Standalone: Added missing dependency of ``polars`` package. Added in
   2.4.9 already.

-  Standalone: Enhanced handling of absence of django settings module
   parameter. Added in 2.4.9 already.

-  Standalone: Added missing implicit dependency of ``win32ctypes``
   modules on Windows. Added in 2.4.9 already.

-  Standalone: Added missing data file for ``arcade`` packaged. Added in
   2.4.9 already.

-  Standalone: Allow PySide6 extras to not be installed on macOS, was
   complaining about missing DLLs, which of course can be normal in that
   case. Added in 2.4.11 already.

-  Standalone: Added ``driverless-selenium`` support. Added in 2.4.11
   already.

-  Standalone: Added support for newer ``tkinterdnd2``. Added in 2.4.11
   already.

-  Standalone: Added support for newer ``kivymd``. Added in 2.4.11
   already.

-  Standalone: Added support for ``gssapi``. Added in 2.4.11 already.

New Features
============

-  Plugins: Change data files configuration over to list of items as
   well, which allows to use ``when`` conditions. Done in 2.4.6 already.

-  Onefile: Splash screen no longe requires MSVC, but works with
   MinGW64, Clang, and ClangCL too. Done for 2.4.8 already.

-  Reports: Add file system encoding of compiling Python to aid in
   debugging encoding issues.

Optimization
============

Anti-Bloat
==========

-  Avoid including ``importlib_metadata`` for ``numpy`` package. Added
   in 2.4.2 already.

-  Anti-Bloat: Avoid ``dask`` usage in ``pandera`` package. Added in
   2.4.5 already.

-  Anti-Bloat: Removed ``numba`` for newer ``shap`` as well. Added in
   2.4.6 already.

-  Anti-Bloat: Avoid attempts to include Python2 and Python3 code both
   for ``aenum``. This avoids ``SyntaxError`` warnings with that
   package. Added in 2.4.7 already.

-  Anti-Bloat: Enhanced handling for ``sympy`` package. Added in 2.4.7
   already.

-  Anti-Bloat: Need to allow ``pydoc`` for ``pyqtgraph`` package. Added
   in 2.4.7 already.

-  Anti-Bloat: Avoid ``pytest`` in ``time_machine`` package. Added in
   2.4.9 already.

Organizational
==============

-  Quality: Use ``clang-format-20`` in GitHub actions.

-  Release script tests for Debian and PyPI used old runner names, not
   the new ones. Changed in 2.4.1 already.

-  UI: Disable locking of progress bar, as Nuitka doesn't use threads at
   this time.

-  Debugging: The explain reference counts could crash on strange
   ``dict`` values. Can mistake them be for a module, when that's not
   the case.

Tests
=====

Cleanups
========

-  WASI: Make sure C function getters and setters of compiled types have
   the correct signature that they are being called with. Cast locally
   to the compiled types only, rather than in the function signature.

-  Indentation of generated code was regressed and generating unaligned
   code in some cases.

-  Quality: Avoid format differences for ``clang-format-20``, so it
   doesn't matter if the new or old version is used.

Summary
=======

This release is not done yet.

.. include:: ../dynamic.inc
