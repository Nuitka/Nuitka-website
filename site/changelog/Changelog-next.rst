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
   Nuitka standalone backend support and enhanced 3.12 performance
   and scalability in general.

   The main focus shall be scalability and a few open issues for
   performance enhancements that later Python versions enable us to.


This release in not complete yet.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========


Package Support
===============


New Features
============


Optimization
============


Anti-Bloat
==========


Organizational
==============


Tests
=====


Cleanups
========

-  WASI: Make sure C function getters and setters of compiled types have the
   correct signature that they are being called with. Cast locally to the
   compiled types only, rather than in the function signature.


Summary
=======

This release is not done yet.

.. include:: ../dynamic.inc
