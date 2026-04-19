:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.0rc11**.

**************************************************
 **Nuitka** Release |NUITKA_VERSION_NEXT| (Draft)
**************************************************

.. note::

   These are the draft release notes for the upcoming **Nuitka**
   |NUITKA_VERSION_NEXT| release. A primary goal for this version is to
   deliver significant enhancements in scalability. Development is
   ongoing, and this documentation might lag slightly behind the latest
   code changes.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  **Python 3.14:** Fix, decorators were breaking when disabling
   deferred annotations. (Fixed in 4.0.1 already.)

-  Fix, nested loops could have wrong traces lead to mis-optimization.
   (Fixed in 4.0.1 already.)

-  **Plugins:** Fix, run-time check of package configuration was
   incorrect. (Fixed in 4.0.1 already.)

-  **Compatibility:** Fix, ``__builtins__`` lacked necessary
   compatibility in compiled functions. (Fixed in 4.0.1 already.)

-  **Distutils:** Fix, incorrect UTF-8 decoding was used for TOML input
   file parsing. (Fixed in 4.0.1 already.)

-  Fix, multiple hard value assignments could cause compile time
   crashes. (Fixed in 4.0.1 already.)

-  Fix, string concatenation was not properly annotating exception
   exits. (Fixed in 4.0.2 already.)

-  **Windows:** Fix, ``--verbose-output`` and ``--show-modules-output``
   did not work with forward slashes. (Fixed in 4.0.2 already.)

-  **Python 3.14:** Fix, various compatibility issues including
   dictionary watchers and inline values. (Fixed in 4.0.2 already.)

-  **Python 3.14:** Fix, stack pointer initialization to ``localsplus``
   was incorrect to avoid garbage collection issues. (Fixed in 4.0.2
   already.)

-  **Python 3.12+:** Fix, generic type variable scoping in classes was
   incorrect. (Fixed in 4.0.2 already.)

-  **Python 3.12+:** Fix, there were various issues with function
   generics. (Fixed in 4.0.2 already.)

-  **Python 3.8+:** Fix, names in named expressions were not mangled.
   (Fixed in 4.0.2 already.)

-  **Plugins:** Fix, module checksums were not robust against quoting
   style of module-name entry in YAML configurations. (Fixed in 4.0.2
   already.)

-  **Plugins:** Fix, doing imports in queried expressions caused
   corruption. (Fixed in 4.0.2 already.)

-  **UI:** Fix, support for ``uv_build`` in the ``--project`` option was
   broken. (Fixed in 4.0.2 already.)

-  **Compatibility:** Fix, names assigned in assignment expressions were
   not mangled. (Fixed in 4.0.2 already.)

-  **Python 3.12+:** Fix, there were still various issues with function
   generics. (Fixed in 4.0.3 already.)

-  **Clang:** Fix, debug mode was disabled for clang generally, but only
   ClangCL and macOS Clang didn't want it. (Fixed in 4.0.3 already.)

-  **Zig:** Fix, ``--windows-console-mode=attach|disable`` was not
   working when using Zig. (Fixed in 4.0.3 already.)

-  **macOS:** Fix, yet another way self dependencies can look like,
   needed to have support added. (Fixed in 4.0.3 already.)

-  **Python 3.12+:** Fix, generic types in classes had bugs with
   multiple type variables. (Fixed in 4.0.3 already.)

-  **Scons:** Fix, repeated builds were not producing binary identical
   results. (Fixed in 4.0.3 already.)

-  **Scons:** Fix, compiling with newer Python versions did not fall
   back to Zig when the developer prompt MSVC was unusable, and error
   reporting could crash. (Fixed in 4.0.4 already.)

-  **Zig:** Fix, the workaround for Windows console mode ``attach`` or
   ``disable`` was incorrectly applied on non-Windows platforms. (Fixed
   in 4.0.4 already.)

-  **Standalone:** Fix, linking with Python Build Standalone failed
   because ``libHacl_Hash_SHA2`` was not filtered out unconditionally.
   (Fixed in 4.0.4 already.)

-  **Python 3.6+:** Fix, exceptions like ``CancelledError`` thrown into
   an async generator awaiting an inner awaitable could be swallowed,
   causing crashes. (Fixed in 4.0.4 already.)

-  Fix, not all ordered set modules accepted generators for update.
   (Fixed in 4.0.5 already.)

-  **Plugins:** Disabled warning about rebuilding the ``pytokens``
   extension module. (Fixed in 4.0.5 already.)

-  **Standalone:** Filtered ``libHacl_Hash_SHA2`` from link libs
   unconditionally. (Fixed in 4.0.5 already.)

-  **Plugins:** Fixed automatic detection of ``mypyc`` runtime
   dependencies, was including all top level modules of the containing
   package by accident. (Fixed in 4.0.5 already.)

-  **Debugging:** Disabled unusable unicode consistency checks for
   Python versions 3.4 to 3.6. (Fixed in 4.0.5 already.)

-  **Python3.12+** Avoided cloning call nodes on class level which
   caused issues with generic functions in combination with decorators.
   (Added in 4.0.5 already.)

-  **Python 3.12+:** Added support for generic type variables in ``async
   def`` functions. (Added in 4.0.5 already.)

-  **Anaconda:** Fixed ``delvewheel`` plugin not working with Python
   3.8+. This enhances compatibility with installed PyPI packages that
   use it for their DLLs. (Fixed in 4.0.6 already.)

-  **UI:** Fixed flushing outputs for prompts was not working in all
   cases when progress bars were enabled. (Fixed in 4.0.6 already.)

-  **UI:** Fixed missing unused variable warnings at C compile time when
   using ``zig`` as a C compiler. (Fixed in 4.0.6 already.)

-  **Scons:** Fix, forced stdout and stderr paths as a feature was
   broken. (Fixed in 4.0.6 already.)

-  Fix, replacing a branch did not accurately track shared active
   variables causing optimization crashes. (Fixed in 4.0.7 already.)

-  **macOS:** Fixed failure to remove extended attributes because files
   need to be made writable first. (Fixed in 4.0.7 already.)

Package Support
===============

-  **Standalone:** Add support for newer ``paddle`` version. (Added in
   4.0.1 already.)

-  **Standalone:** Add workaround for refcount checks of ``pandas``.
   (Fixed in 4.0.1 already.)

-  **Standalone:** Add support for newer ``h5py`` version. (Added in
   4.0.2 already.)

-  **Standalone:** Add support for newer ``scipy`` package. (Added in
   4.0.2 already.)

-  **Plugins:** Revert accidental ``os.getenv`` over ``os.environ.get``
   changes in anti-bloat configurations that stopped them from working.
   Affected packages are ``networkx``, ``persistent``, and
   ``tensorflow``. (Fixed in 4.0.5 already.)

-  **Standalone:** Added missing DLLs for ``openvino``. (Added in 4.0.7
   already.)

New Features
============

-  **UI:** Add message to inform users about ``Nuitka[onefile]`` if
   compression is not installed. (Added in 4.0.1 already.)

-  **UI:** Add support for ``uv_build`` in the ``--project`` option.
   (Added in 4.0.1 already.)

-  **Onefile:** Allow extra includes as well. (Added in 4.0.2 already.)

-  **UI:** Add ``nuitka-project-set`` feature to define project
   variables, checking for collisions with reserved runtime variables.
   (Added in 4.0.2 already.)

-  **Scons:** Added new option to select ``--reproducible`` builds or
   not. (Added in 4.0.6 already.)

Optimization
============

-  Avoid including ``importlib._bootstrap`` and
   ``importlib._bootstrap_external``. (Added in 4.0.1 already.)

Anti-Bloat
==========

-  Fix, memory bloat occurred when C compiling ``sqlalchemy``. (Fixed in
   4.0.2 already.)

-  Avoid using ``pydoc`` in ``PySimpleGUI``. (Added in 4.0.2 already.)

-  Avoided using ``doctest`` from ``zodbpickle``. (Added in 4.0.5
   already.)

-  Avoided inclusion of ``cython`` when using ``pyav``. (Added in 4.0.7
   already.)

-  Avoided including ``typing_extensions`` when using ``numpy``. (Added
   in 4.0.7 already.)

Organizational
==============

-  **Debian:** Remove recommendation for ``libfuse2`` package as it is
   no longer useful.

-  **Debian:** Used ``platformdirs`` instead of ``appdirs``.

-  **Debugging:** Removed Python 3.11+ restriction for ``clang-format``
   as it is available everywhere, even Python 2.7, and we still want
   nicely formatted code when we read things. (Added in 4.0.6 already.)

-  Removed no longer useful inline copy of ``wax_off``. We have our own
   stubs generator project.

Tests
=====

-  Install only necessary build tools for test cases.

-  Avoided spurious failures in reference counting tests due to Python
   internal caching differences. (Fixed in 4.0.3 already.)

-  Fixed the parsing of the compilation report for reflected tests.

-  **Python 3.14:** Ignored a syntax error message change.

Cleanups
========

-  **UI:** Fix, there was a double space in the Windows Runtime DLLs
   inclusion message. (Fixed in 4.0.1 already.)

-  **Onefile:** Separated files and defines for extra includes for
   onefile boot and Python build.

-  **Scons:** Provided nicer errors in case of "unset" variables being
   used, so we can tell it.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
