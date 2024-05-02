:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per-version changes and comments for the
upcoming Nuitka |NUITKA_VERSION_NEXT| as a draft about hot-fixes of the
current stable release as |NUITKA_VERSION| as well.

****************************
 Nuitka Release 2.3 (Draft)
****************************

.. note::

   This a draft of the release notes for 2.3, which is supposed to add
   Python 3.12 support, and the usual additions of new packages
   supported out of the box and will also aim at scalability if
   possible.

This release is not done yet.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  Standalone: Added support for ``python-magic-bin`` package. Fixed in
   2.2.1 already.

-  Fix: The cache directory creation could fail when multiple
   compilations started simultaneously. Fixed in 2.2.1 already.

-  macOS: For ``arm64`` builds, DLLs can also have an architecture
   dependent suffix; check that as well. Makes the ``soundfile``
   dependency scan work. Fixed in 2.2.1 already.

-  Fix: Modules where lazy loaders handling adds hard imports when a
   module is first processed did not affect the current module,
   potentially causing it not to resolve hidden imports. Fixed in 2.2.1
   already.

New Features
============

-  Plugins: Added support to include directories entirely unchanged by
   adding ``raw_dir`` values for ``data-files`` section, see
   :doc:`Nuitka Package Configuration
   </user-documentation/nuitka-package-config>`.

-  UI: The new command line option ``--include-raw-dir`` was added to
   allow including directories entirely unchanged.

Optimization
============

-  Python3.5+: Directly use the **Python** allocator functions for
   object creation, avoiding the DLL API calls. The coverage is complete
   with Python3.11 or higher, but many object types like ``float``,
   ``dict``, ``list``, ``bytes`` benefit even before that version.

-  Optimization: Faster creation of ``StopIteration`` objects for
   **Python3**.

   With Python 3.12, the object is created directly and set as the
   current exception without normalization checks.

   We also added a new specialized function to create the exception
   object and populate it directly, avoiding the overhead of calling of
   the ``StopIteration`` type.

-  Optimization: For Python3.8+, call uncompiled functions via vector
   calls.

   We avoid an API call that ends up being slower than using the same
   function via the vector call directly.

Organizational
==============

-  Detect ``patchelf`` usage in buggy version ``0.18.0`` and ask the
   user to upgrade or downgrade it, as this specific version is known to
   be broken.

Tests
=====

-  No changes yet.

Cleanups
========

-  Solved a TODO about using unified code for setting the
   ``StopIteration``.

Summary
=======

This release is not yet done.

.. include:: ../dynamic.inc
