:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.3rc1**.

**************************************************
 **Nuitka** Release |NUITKA_VERSION_NEXT| (Draft)
**************************************************

.. note::

   These are the draft release notes for the upcoming **Nuitka**
   |NUITKA_VERSION_NEXT| release. A primary goal for this version is to
   improve Python 3.15 support, with work planned on frame locals
   proxies as in Python 3.13, optimization of iterator unpacking, and
   inlining of generator expressions. Development is ongoing, and this
   documentation might lag slightly behind the latest code changes.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  Fix, comparisons and add or subtract operations of Python ``long``
   values with C ``long`` operands could produce wrong results. (Fixed
   in 4.2.1 already.)

-  **Python 3.14:** Fix, deferred annotations did not work with hard
   import names, e.g. ``io.BytesIO``, since those were unnecessarily
   generated as ``__import__`` calls. (Fixed in 4.2.1 already.)

-  **Python 3.14:** Fix, the
   ``--devel-no-bytecode-to-compiled-fallback`` option was not honored
   when source generation for an ``__annotate__`` function failed, where
   the fallback to compiled code happened anyway. (Fixed in 4.2.1
   already.)

-  **Python 3.14:** Fix, source generation for ``__annotate__``
   functions did not handle closures, constants, and calls correctly.
   Closure variables were then rejected to fall back to compiled code,
   and values like non-finite floats, empty sets, and types from modules
   are rendered as valid source. (Fixed in 4.2.1 already.)

-  **Plugins:** Fix, nested uses of the ``forkserver`` context were not
   working. (Fixed in 4.2.1 already.)

-  **Compatibility:** Fix, conditional expressions did not decide their
   type shapes from the branches properly, which could lead to wrong
   optimization of list appends and subscript operations. (Fixed in
   4.2.2 already.)

-  **Compatibility:** Fix, keyword arguments created from ``str``
   subclass instances were rejected, since the check compared the exact
   type instead of allowing subclasses. (Fixed in 4.2.2 already.)

-  **Windows:** Fix, MSYS2 builds now link the compiler runtime
   statically, avoiding a runtime dependency on e.g.
   ``libwinpthread-1.dll``, which also fixes module mode requiring that
   DLL. (Fixed in 4.2.2 already.)

-  **MSYS2:** Fix, adapting Python header files did not work on that
   flavor yet. (Fixed in 4.2.2 already.)

-  **macOS:** Fix, newer Xcode versions only ship tools like
   ``install_name_tool``, ``lipo``, ``nm``, and ``otool`` as ARM64
   binaries, which fail to run in an ``x86_64`` translated process.
   These are now invoked with ``arch -arm64`` as needed, and the same
   for the C compiler and ``ccache``. (Fixed in 4.2.2 already.)

-  **Debian:** Fix, onefile mode was no longer usable when the ``zstd``
   inline copy is absent, e.g. in the official Debian package, since the
   system ``zstd`` and ``zlib`` are now linked statically instead.
   (Fixed in 4.2.2 already.)

-  **Installer:** Fix, Linux installer creation crashed in onefile mode,
   now informs the user that ``--mode=app-dist`` (or
   ``--mode=standalone``) mode is required. (Fixed in 4.2.2 already.)

Package Support
===============

-  **Standalone:** Added support for newer ``PyAV``. (Added in 4.2.1
   already.)

-  **Standalone:** Fix, ``vtk8`` was no longer working, since the
   package path configuration was needlessly restricted to ``vtk``
   version 9 and higher. (Fixed in 4.2.1 already.)

-  **Standalone:** Added support for the latest ``toga`` on macOS, with
   the ``toga_cocoa.resources`` dependency now included. (Added in 4.2.1
   already.)

-  **Plugins:** Fix, the ``PySide6`` ``singleShot`` timer workaround
   protected the wrong argument when called with more arguments,
   allowing the issue it is meant to avoid to occur. (Fixed in 4.2.1
   already.)

New Features
============

-  **Python 3.14:** Added source generation for function calls and more
   hard import types for ``__annotate__`` functions. (Added in 4.2.1
   already.)

-  **Python 3.14:** Added source generation for more constant value
   types for ``__annotate__`` functions, e.g. ``bytes``, ``range``,
   ``slice``, ``bytearray``, and ``complex`` values, including
   non-finite components. (Added in 4.2.1 already.)

Optimization
============

-  **Standalone:** Moved implicit import consideration from module
   recursion into the optimization pass, avoiding an unnecessary third
   pass for standard library modules using a cold bytecode cache. (Added
   in 4.2.2 already.)

-  **Standalone:** Enabled LTO for the "Python Build Standalone" flavor
   as well, since it is known to be supported. (Added in 4.2.2 already.)

Anti-Bloat
==========

-  Avoided using ``pydoc`` in the official ``PySimpleGUI`` package as
   well, which so far was only done for the non-official one. (Fixed in
   4.2.1 already.)

Organizational
==============

-  **UI:** Made the ``--file-description`` help text clear that it is no
   longer Windows only, as it is also used as the summary of the
   AppStream metadata of Linux ``--mode=app`` mode. (Fixed in 4.2.1
   already.)

-  **Release:** Added ``clangd`` to the CI container to allow checking
   with it. (Added in 4.2.2 already.)

Tests
=====

-  Added support for the ``win32``, ``linux``, and ``macos`` variables
   in ``wait_for`` conditions of ``nuitka-watch`` test cases. (Added in
   4.2.1 already.)

Cleanups
========

-  The temporary filename context manager now deletes the file itself,
   also on errors, simplifying its users such that don't have to do it.
   (Fixed in 4.2.1 already.)

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
