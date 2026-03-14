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

Optimization
============

-  Avoid including ``importlib._bootstrap`` and
   ``importlib._bootstrap_external``. (Added in 4.0.1 already.)

Anti-Bloat
==========

-  Fix, memory bloat occurred when C compiling ``sqlalchemy``. (Fixed in
   4.0.2 already.)

-  Avoid using ``pydoc`` in ``PySimpleGUI``. (Added in 4.0.2 already.)

Organizational
==============

-  **Debian:** Remove recommendation for ``libfuse2`` package as it is
   no longer useful.

Tests
=====

-  Install only necessary build tools for test cases.

Cleanups
========

-  **UI:** Fix, there was a double space in the Windows Runtime DLLs
   inclusion message. (Fixed in 4.0.1 already.)

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
