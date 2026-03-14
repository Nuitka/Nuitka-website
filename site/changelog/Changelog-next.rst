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

-  **Python 3.14:** Fixed decorators breaking when disabling deferred
   annotations. (Fixed in 4.0.1 already.)

-  Fixed an issue where nested loops could have wrong traces. (Fixed in
   4.0.1 already.)

-  **Plugins:** Fixed run-time check of package configuration. (Fixed in
   4.0.1 already.)

-  **Compatibility:** Fixed ``__builtins__`` in compiled functions.
   (Fixed in 4.0.1 already.)

-  **Distutils:** Use correct UTF-8 decoding for TOML input file
   parsing. (Fixed in 4.0.1 already.)

-  Fixed an issue where multiple hard value assignments could cause
   issues. (Fixed in 4.0.1 already.)

Package Support
===============

-  **Standalone:** Added support for newer ``paddle`` version. (Added in
   4.0.1 already.)

-  **Standalone:** Added workaround for refcount checks of ``pandas``.
   (Fixed in 4.0.1 already.)

New Features
============

-  **UI:** Added message to inform users about ``Nuitka[onefile]`` if
   compression is not installed. (Added in 4.0.1 already.)

-  **UI:** Added support for ``uv_build`` in the ``--project`` option.
   (Added in 4.0.1 already.)

Optimization
============

-  Avoided including ``importlib._bootstrap`` and
   ``importlib._bootstrap_external``. (Added in 4.0.1 already.)

Anti-Bloat
==========

-  None yet

Organizational
==============

-  **Debian:** Removed recommendation for ``libfuse2`` package as it is
   no longer useful.

Tests
=====

-  None yet

Cleanups
========

-  **UI:** Fixed double space in Windows Runtime DLLs inclusion message.
   (Fixed in 4.0.1 already.)

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
