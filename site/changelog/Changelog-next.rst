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
   own.

Package Support
===============

No changes documented yet.

New Features
============

No changes documented yet.

Optimization
============

No changes documented yet.

Anti-Bloat
==========

No changes documented yet.

Organizational
==============

No changes documented yet.

Tests
=====

No changes documented yet.

Cleanups
========

No changes documented yet.

Summary
=======

This release is not complete yet.

.. include:: ../dynamic.inc
