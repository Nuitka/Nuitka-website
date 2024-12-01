:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per-version changes and comments for the
upcoming Nuitka |NUITKA_VERSION_NEXT| as a draft about hot-fixes of the
current stable release as |NUITKA_VERSION| as well.

****************************
 Nuitka Release 2.6 (Draft)
****************************

.. note::

   This a draft of the release notes for 2.6, which is supposed to add
   Nuitka standalone backend support and enhanced 3.13 compatibility,
   and lots of scalability in general, aiming at an order of magnitude
   improvement for compile times.

This release is in progress still and documentation might lag behind
development.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  **MSYS2:** Need to normalize paths to native in more places for MinGW
   variant

   Since ``os.path.normpath`` doesn't actually normalize to native Win32
   paths with MSYS2, but to forward slashes, we need to do it on our
   own. Fixed in 2.5.1 already.

-  Fix, extensions modules that failed to locate could crash the
   compilation starting with 2.5, rather than giving proper error as
   before. Fixed in 2.5.1 already.

-  Fix, was considering files as potential sub-modules for
   ``--include-package`` that actually have an illegal name, due to
   ``.`` in their basename. These need to be skipped. Fixed in 2.5.1
   already.

-  Stubgen: Do not crash when ``stubgen`` crashes on code it cannot
   handle and ignore its exceptions. Fixed in 2.5.1 already.

-  Stubgen: Do not crash on assignments to non-variables. Fixed in 2.5.1
   already.

-  Python3: Fixed a regression of 2.5 with exception handling of
   generators that could lead to segfaults. Fixed in 2.5.2 already.

-  Python3.11+: Fix, dictionary copies of large split directories could
   become corrupt. Fixed in 2.5.2 already.

   This mostly affects instance dictionaries, which are created as this
   kind of copy until they are updated. These then these would present
   issues when being updated with new keys afterwards.

-  Python3.11+: Fix, must not assume module dictionary to be a string
   dictionary. Some modules have non-strings being put there, e.g
   ``Foundation`` on macOS. Fixed in 2.5.2 already.

-  Fix, the ``--deployment`` didn't impact the C side as intended, only
   the individual disables were applied there. Fixed in 2.5.2 already.

-  Fix, unary operations could crash the compilation if used inside a
   binary operation. Fixed in 2.5.3 already.

-  Onefile: Fix, the handling of ``__compiled__.original_argv0`` was
   incorrect and could lead to crashes. Fixed in 2.5.4 already.

-  Fix, calls to ``tensorflow.function`` using only keyword arguments
   segfaulted at runtime. Fixed in 2.5.5 already.

-  macOS: Ignore harmless warning given for x64 DLLs on arm64 with newer
   macOS. Fixed in 2.5.5 already.

Package Support
===============

-  Standalone: Add inclusion of metadata for ``jupyter_client`` as it
   uses that itself. Added in 2.5.1 already.

-  Standalone: Added support for ``llama_cpp`` package. Added in 2.5.1
   already.

-  Standalone: Added support for ``litellm`` package. Added in 2.5.2
   already.

-  Standalone: Added support for ``lab_lamma`` package. Added in 2.5.2
   already.

-  Standalone: Added support for ``docling`` metadata. Added in 2.5.5
   already.

-  Standalone: Added support for ``pypdfium`` on Linux too. Added in
   2.5.5 already.

-  Standalone: Added support for using ``debian" package``. Added in
   2.5.5 already.

-  Standalone: Added support for ``pdfminer`` package. Added in 2.5.5
   already.

New Features
============

-  Module: Allow disabling the use of ``stubgen`` entirely. Added in
   2.5.1 already.

-  UI: Added ``app`` module for ``--mode`` parameter. On macOS it's an
   app, elsewhere it's a onefile binary. This replaces
   ``--macos-create-app-bundle`` for which we didn't have something yet.
   Added in 2.5.5 already.

-  Homebrew: Added support for ``tcl9`` with ``tk-inter`` plugin.

-  When multiple distributions are installed for the same package name,
   try and figure out which one was installed less, such that
   ``python-opencv`` and ``python-opencv-headless`` with different
   versions installed are properly recognized for the version used.

Optimization
============

No changes documented yet.

Anti-Bloat
==========

No changes documented yet.

Organizational
==============

-  UI: Use report path for executable in ``--version`` output.

   We don't want people to be forced to output their home directory
   path, it only makes them want to avoid giving the whole output.

-  UI: The container argument couldn't be a non-template file for
   ``run-inside-nuitka-container``. Fixed in 2.5.2.

-  Release: Use virtualenv for PyPI upload ``sdist`` creation. The
   setuptools version decides the project name casing. For now, we use
   the one that produces deprecated filenames.

-  Debugging: Allow disabling changing to short paths on Windows with an
   experimental option.

Tests
=====

No changes documented yet.

Cleanups
========

-  Unified production or standard source archives and code used for PyPI
   uploads, so the result is identical and code is shared.

-  Harmonized the usage of ``include <...>`` vs ``include "..."`` by
   origin of files to be included.

Summary
=======

This release is not complete yet.

.. include:: ../dynamic.inc
