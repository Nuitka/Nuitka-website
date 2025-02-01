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

-  **Standalone:** Fix, for newer ``PySide6`` plugin ``sqldrivers`` on macOS.

New Features
============

-  **Windows:** Added support for Windows ARM and dependency analysis.
   We do it via ``pefile`` since dependency walker doesn't know about
   ARM.

-  **Windows:** Enable taskbar grouping, if product name and company
   name are present in version information. Added in 2.6.1 already.

-  **Windows:** Use icons given for Windows automatically with
   ``PySide6``, this removes the need to also provide the application
   icon as a PNG file, duplicating it.

-  **Nuitka Package Configuration:** Allow using values of ``constants``
   ``variable`` declarations in ``when`` conditions where possible.

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
