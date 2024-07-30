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

-  Windows: Fix, console output handles were opened with close file handles, but
   that is not allowed. Fixed in 2.4.2 already.

-  Standalone: Fix, using trailing slashes to mark the target directory
   for data files no longer worked on Windows. Fixed in 2.4.2 already.

-  Fix, the ``.pyi`` parser could fail for relative imports. This could break
   some packages that are extension modules, but with source code available too.
   Fixed in 2.4.3 already.

-  Modules: Fix, extension modules didn't load into packages with Python3.12.
   Fixed in 2.4.4 already.

Package Support
===============

-  Standalone: Improved ``arcade`` configuration. Added in 2.4.3 already.

New Features
============

Optimization
============

Anti-Bloat
==========

-  Avoid including ``importlib_metadata`` for ``numpy`` package. Added in 2.4.2
   already.

Organizational
==============

-  Quality: Use ``clang-format-20`` in GitHub actions.

-  Release script tests for Debian and PyPI used old runner names, not
   the new ones. Changed in 2.4.1 already.

-  UI: Disable locking of progress bar, as Nuitka doesn't use threads at
   this time.

Tests
=====

Cleanups
========

-  WASI: Make sure C function getters and setters of compiled types have
   the correct signature that they are being called with. Cast locally
   to the compiled types only, rather than in the function signature.

-  Indentation of generated code was regressed and generating unaligned
   code in some cases.

Summary
=======

This release is not done yet.

.. include:: ../dynamic.inc
