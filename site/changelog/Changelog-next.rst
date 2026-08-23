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

-  **Python3:** Fix, nested generators did not make the exception being
   handled in the delegating generator visible to the code they delegate
   to, so ``sys.exc_info()`` gave wrong results there. (Fixed in 4.1.1
   already.)

   .. code:: python

      import sys


      def inner():
          print(sys.exc_info()[0])  # 4.1: None (bug), 4.1.1: KeyError (correct)
          yield 1


      def outer():
          try:
              raise KeyError("caught")
          except KeyError:
              yield from inner()


      next(outer())

-  **Python 3.10+:** Fix, compiled coroutines left the result of their
   send slot uninitialized when they finished by raising, so callers
   like ``asyncio`` could observe garbage values. (Fixed in 4.1.1
   already.)

-  **Python 3.14:** Fix, debug builds in module mode needed handling for
   the reference tracing runtime access, and adapted headers are no
   longer used for MSVC, where the compiler and runtime layouts match.
   (Fixed in 4.1.1 already.)

-  **Python 3.11/3.12:** Fix, optimized class calls bypassing
   ``object_new`` did not initialize the managed dict inline values, so
   the first attribute assignment fell back to a separately allocated
   dictionary, which was non-optimal and caused incompatibility in
   corner cases. (Fixed in 4.1.2 already.)

-  **Python 3.11+:** Fix, compiled frame locals were not stored in the
   interpreter frame ``localsplus`` slots, making them invisible to
   CPython frame introspection. (Fixed in 4.1.2 already.)

-  **Python 3.12+:** Fix, the ``__type_params__`` attribute of generic
   functions was always empty. (Fixed in 4.1.2 already.)

-  **Python 3.14:** Fix, frame locals were cleared too late in the
   deallocator, after the code object and extra locals were already
   released, which could cause crashes. (Fixed in 4.1.2 already.)

-  **Python 3.14:** Fix, type complaint exception messages now use the
   ``__qualname__`` of the offending type, as CPython does. (Fixed in
   4.1.2 already.)

-  **Standalone:** Fix, standard library path detection for the "Python
   Build Standalone" flavor needed to consider symlinks in directory
   components. (Fixed in 4.1.2 already.)

-  **Plugins:** Fix, ``mypyc`` runtime detection didn't happen for
   submodules of a package, which affected at least the ``chardet``
   module. (Fixed in 4.1.1 already.)

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
   ``--mode=dll`` mode as well, otherwise ``install_name_tool`` cannot
   rewrite the load paths of the output. (Fixed in 4.1.1 already.)

-  **macOS:** Fix, existing signatures of frameworks were no longer
   copied, as they became invalid after relocation and broke re-signing
   of the binaries. (Fixed in 4.1.1 already.)

-  **macOS:** Fix, added handling for another form of self dependency
   from absolute paths. (Fixed in 4.1.1 already.)

-  **macOS:** Fix, detection of statically linked libraries did not
   work, since the ``file`` command output was not used yet, so they
   were treated like dynamic ones, leading to errors. (Fixed in 4.1.2
   already.)

-  **macOS:** Fix, detected another variation of self dependencies,
   where a less-versioned binary depends on its more versioned self.
   (Fixed in 4.1.2 already.)

-  **Debian:** Fix, ``--disable-ccache`` did not work when the compiler
   binary was a symlink, e.g. from the Debian ``ccache`` package. (Fixed
   in 4.1.2 already.)

Package Support
===============

-  **Standalone:** Added support for the ``pyDOE3`` package. (Added in
   4.1.1 already.)

-  **Standalone:** Added support for the ``mssql_python`` package.
   (Added in 4.1.1 already.)

-  **Standalone:** No longer proposed to recompile the
   ``charset_normalizer`` extension module. (Added in 4.1.1 already.)

-  **Standalone:** Added support for the ``emoji`` package. (Added in
   4.1.2 already.)

-  **Standalone:** Added support for the ``mitmproxy`` package. (Added
   in 4.1.2 already.)

-  **Plugins:** Fix, PyQt5 markdown data files caused errors on Linux,
   they are now excluded. (Fixed in 4.1.1 already.)

-  **Plugins:** Added support for newer ``pkg_resources`` versions,
   where the ``EggProvider`` was removed. (Added in 4.1.1 already.)

-  **Plugins:** Fix, build artifacts with ``.a``, ``.prl``, and ``.la``
   suffixes in QML directories were no longer included. (Fixed in 4.1.2
   already.)

New Features
============

-  **Python 3.14:** Added support for ``__annotate__`` for classes, and
   delaying class level annotations when the
   ``--experimental=deferred-annotations`` flag is given. With 4.2, this
   is the default mode. (Added in 4.1.1 already.)

Optimization
============

-  **Python 3.14:** Added ``_zstd`` and ``_remote_debugging`` to the
   standard library modules known to never raise on import, allowing
   their imports to be optimized accordingly. (Fixed in 4.1.2 already.)

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

-  **Quality:** Enforced the required versions for the private pipspace
   packages used for YAML formatting. (Fixed in 4.1.2 already.)

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
