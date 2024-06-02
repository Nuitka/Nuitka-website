:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per-version changes and comments for the
upcoming Nuitka |NUITKA_VERSION_NEXT| as a draft about hot-fixes of the
current stable release as |NUITKA_VERSION| as well.

****************************
 Nuitka Release 2.4 (Draft)
****************************

.. note::

   This a draft of the release notes for 2.4, which is supposed to add
   Python 3.13 beta2 support and the usual additions of new packages
   supported out of the box.

   The main focus shall be scalability and a few open issues for
   performance enhancements that later Python versions enable us to.

This release is not done yet.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  Python3.12: Added annotations of official support for **Nuitka** PyPI
   package and test runner options that were still missing. Fixed in
   2.3.1 already.

-  UI: Fix, correct reversed ``disable`` / ``force`` recommendation for
   ``--windows-console-mode`` when the user used old-style options.

-  Python3.10+: Fix, must not check for ``len`` greater or equal of 0 or
   for sequence ``match`` cases. That is unnecessary and incompatible
   and can raise exceptions with custom sequences not implementing
   ``__len__``. Fixed in 2.3.1 already.

-  Python3.10+: Fix, ``match`` sequence with final star arguments failed
   in some cases to capture the rest and left the assigned value empty. Fixed in 2.3.1 already.

-  Standalone: Added data file for older ``bokeh`` version. Fixed in
   2.3.1 already.

New Features
============

-  None yet.

Optimization
============

-  Anti-Bloat: Avoid using ``unittest`` in ``keras`` package. Added in
   2.3.1 already.

Organizational
==============

-  Added badges to the ``README.rst`` of **Nuitka** to display package
   support and more. Added in 2.3.1 already.

-  UI: Use the retry decorator when removing directories in general. It
   will be more thorough with properly annotated retries on Windows. For
   the dist folder, mention the running program as a probable cause.

Tests
=====

-  None yet

Cleanups
========

-  Minor spelling cleanups.

Summary
=======

This release is not yet done.

.. include:: ../dynamic.inc
