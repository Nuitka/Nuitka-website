:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.4rc1**.

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

-  Fix, when the main module raised an exception during its execution,
   it was unregistered and released like any other module, although its
   code objects and functions can still be used afterwards, e.g. by
   ``__del__`` methods making frames during interpreter finalization,
   which could crash. The main module is now kept registered and
   referenced. (Fixed in 4.3.1 already.)

-  **Python3:** Fix, the ``__path__`` of compiled namespace packages was
   created with the compile time full name of the package, which does
   not necessarily match the ``__name__`` the module has at run time, so
   the namespace path could not find its submodules, e.g. for a nested
   implicit namespace package inside a compiled package. The module
   ``__name__`` attribute is now used. (Fixed in 4.3.1 already.)

-  **Python 3.14+:** Fix, deferred annotations did not account for
   conditional execution, so annotations in blocks that did not run,
   e.g. under ``if TYPE_CHECKING:``, were still included in
   ``__annotations__``, unlike CPython, which only includes such
   annotations if their assignment registered its index in
   ``__conditional_annotations__``. The registration is now done at run
   time and checked when the annotations are created. (Fixed in 4.3.1
   already.)

   .. code:: python

      from typing import TYPE_CHECKING

      condition = True

      if TYPE_CHECKING:
          checked_only: set

      if condition:
          executed: str
      else:
          not_executed: bytes

      # 4.3: all annotations present in "__annotations__"
      # 4.3.1: only annotations of executed statements present

-  **Standalone:** The Tk version 9 interpreter on Windows is now
   created with the ``PATH`` environment variable temporarily removed,
   since Tk loads ICU DLLs dynamically and prefers versioned DLLs found
   in the ``PATH`` over the ones included with Windows, which could make
   the program depend on third party software. (Fixed in 4.3.1 already.)

-  **Plugins:** Fix, the probe that decides whether compiled methods
   need cached wrappers to avoid the unlimited API ``PySide6`` via
   ``SystemError`` in signal slots used temporary bound methods, which
   were not protected from the other bug we normally work around. (Fixed
   in 4.3.1 already.)

-  **Anaconda:** Fix, the ``include/python`` directory used on Windows
   by Anaconda and conda-forge Python since version 3.15 was not
   considered when locating the Python headers, so compilation aborted
   with a message about an unsupported embeddable distribution. (Fixed
   in 4.3.1 already.)

-  **Module:** Fix, the file system paths of loader entries used the
   package prefix that is added to the runtime name when a compiled unit
   is loaded as a package, e.g. producing ``ns/pkg`` instead of ``pkg``,
   so data and resource files were looked up at the wrong location. The
   prefix is now removed for the file system paths. (Fixed in 4.3.1
   already.)

Package Support
===============

-  None yet.

New Features
============

-  **Python 3.15+:** Added support for module export hooks, where an
   extension module provides a ``PyModExport_<name>`` or
   ``PyModExportU_<name>`` function returning a slots array, which
   CPython prefers over the ``PyInit_<name>`` entry point function, with
   the meta path based loader checking for it first and falling back to
   ``PyInit_``. Modules from export hooks are created with
   ``PyModule_FromSlotsAndSpec``, with a ``SystemError`` reported for
   hooks that fail without setting an exception or raise an unreported
   one, and a missing export function now gives an ``ImportError``
   naming both functions that were tried. (Added in 4.3.1 already.)

Optimization
============

-  Type descriptions are now exported uniformly as pointer variables and
   declared only in the generated module that uses them, so adding a
   description no longer changes the shared ``__constants.h`` header and
   thereby avoids rebuilding unrelated modules. (Added in 4.3.1
   already.)

Anti-Bloat
==========

-  None yet.

Organizational
==============

-  **Debian:** Fix, the ``py2dsc`` based Debian packaging on mounts that
   report all files as executable, e.g. container builds using Windows
   shares, gave the copied Debian config files the executable bit, and
   debhelper then executed ``nuitka.install`` instead of reading it,
   which failed. The executable permission is now removed from the
   copied files, keeping only ``rules`` executable. (Fixed in 4.3.1
   already.)

Tests
=====

-  None yet.

Cleanups
========

-  None yet.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
