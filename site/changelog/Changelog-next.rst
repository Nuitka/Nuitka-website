:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.2rc1**.

**************************************************
 **Nuitka** Release |NUITKA_VERSION_NEXT| (Draft)
**************************************************

.. note::

   These are the draft release notes for the upcoming **Nuitka**
   |NUITKA_VERSION_NEXT| release. A primary goal for this version is to
   deliver significant enhancements in C compilation scalability, and to
   make 3.14 officially supported. Development is ongoing, and this
   documentation might lag slightly behind the latest code changes.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  **Python3:** Fix, nested generators did not publish exceptions
   properly. (Fixed in 4.1.1 already.)

-  **Python 3.10+:** Fix, compiled coroutines left the result of their
   send slot uninitialized when they finished by raising, so callers
   like ``asyncio`` could observe garbage values. (Fixed in 4.1.1
   already.)

-  **Python 3.14:** Fix, for Python debug module mode, the runtime
   access for reference tracing needed handling, and adapted headers
   were not used for MSVC non-modules anymore, where they are not
   needed. (Fixed in 4.1.1 already.)

-  **Plugins:** Fix, ``mypyc`` runtime detection didn't happen for
   submodules of a package, which affected at least the ``chardet``
   module. (Fixed in 4.1.1 already.)

-  **Plugins:** Fix, ``pkg_resources`` newer version lost some features
   with newer versions where e.g. the ``EggProvider`` imports fail.
   (Fixed in 4.1.1 already.)

-  **Windows:** Enabled UTF-8 mode for attached consoles, since
   otherwise the CRT runtime could hang or corrupt outputs and inputs.
   (Fixed in 4.1.1 already.)

-  **Windows:** Fix, ``multiprocessing`` was not fully working in
   onefile DLL mode, since spawning needs to point to the outer binary,
   not the DLL. (Fixed in 4.1.1 already.)

-  **Windows:** Fix, memory issue for 32 bit Python onefile compression,
   where parallel zstandard compression ran into memory issues for even
   small files when using multiple threads. (Fixed in 4.1.1 already.)

-  **macOS:** Fix, needed to make sure header padding is possible for
   ``--mode=dll`` mode as well. (Fixed in 4.1.1 already.)

-  **macOS:** Fix, did not include existing signatures for frameworks
   anymore. (Fixed in 4.1.1 already.)

-  **macOS:** Fix, added handling for another form of self dependency
   from absolute paths. (Fixed in 4.1.1 already.)

Package Support
===============

-  **Standalone:** Added support for the ``pyDOE3`` package. (Added in
   4.1.1 already.)

-  **Standalone:** Added support for the ``mssql_python`` package.
   (Added in 4.1.1 already.)

-  **Standalone:** No longer proposed to recompile the
   ``charset_normalizer`` extension module. (Added in 4.1.1 already.)

-  **Plugins:** Fix, PyQt5 markdown data files caused errors on Linux,
   they are now excluded. (Fixed in 4.1.1 already.)

New Features
============

-  **Python 3.14:** Added support for ``__annotate__`` for classes, and
   delaying class level annotations when the experimental flag is given.
   (Added in 4.1.1 already.)

Optimization
============

-  None yet.

Anti-Bloat
==========

-  Avoided more ``tkinter`` dependencies from ``PIL``. (Fixed in 4.1.1
   already.)

-  Avoided including ``matplotlib`` due to ``pandas`` plotting. (Fixed
   in 4.1.1 already.)

Organizational
==============

-  **Project:** Corrected a few mistakes done when changing the license,
   referencing the runtime exception everywhere and using a proper link
   to the correct version of the license file on the web. (Fixed in
   4.1.1 already.)

-  **Debian:** Made builds work inside containers that have the
   ``x-bit`` stripped from the install file, by making it an executable
   script. (Fixed in 4.1.1 already.)

-  **Release:** Fix, the inline copy of ``atomicwrites`` was still
   needed for Python 2. (Fixed in 4.1.1 already.)

-  **UI:** Fix, duplicate data file targets were not detected, which now
   warns and uses the first variant. (Fixed in 4.1.1 already.)

Tests
=====

-  Disabled parts of the ``pkgutil_usage`` test with newer
   ``pkg_resources`` versions that lost some features. (Fixed in 4.1.1
   already.)

-  Ignored clang download warnings in output comparisons as well. (Fixed
   in 4.1.1 already.)

-  Ignored differences from messages about Qt font usage in output
   comparisons. (Fixed in 4.1.1 already.)

-  Rejected using ``--all`` and ``--pattern`` at the same time in the
   test runner. (Fixed in 4.1.1 already.)

-  **macOS:** Ignored the ``libffi-trampolines.dylib`` system library
   used by Python 3.14 in test comparisons. (Fixed in 4.1.1 already.)

-  **Debugging:** Fix, deep hashing checks failed with active
   exceptions, which was relatively easy to trigger, e.g. with
   ``SystemExit`` being set. (Fixed in 4.1.1 already.)

Cleanups
========

-  Fixed pylint warnings in the coverage rendering tool. (Fixed in 4.1.1
   already.)

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
