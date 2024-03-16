:orphan:

##############################################
 Nuitka |NUITKA_VERSION_NEXT| Changelog Draft
##############################################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per version changes and comments for the
upcoming Nuitka |NUITKA_VERSION_NEXT| as a draft about hot-fixes of the
current stable release as |NUITKA_VERSION| as well.

****************************
 Nuitka Release 2.2 (Draft)
****************************

This a draft of the release notes for 2.2, which is supposed to contains
the usual additions of new packages supported out of the box and will
aim at scalability.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  Standalone: Added support for ``pypdfium2`` package. Fixed in 2.1.1
   already.

-  Standalone: Make ``cefpython3`` work on Linux. Fixed in 2.1.1
   already.

-  ArchLinux: Need to add linker option for it to be usable with their
   current Arch Python package. Fixed in 2.1.1 already.

-  Fix, ``ctypes.CDLL`` optimization was using mis-spelled argument name
   for ``use_last_error``, such that keyword argument calls using it
   were statically optimized into ``TypeError`` at compile-time. Fixed
   in 2.1.1 already.

-  Fix, ``list.insert`` was not properly annotating exceptions. Raises
   by producing the inserted value raised or the index were not
   annotated, and therefore could fail to be caught locally. Fixed in
   2.1.1 already.

-  Standalone: Added support for ``selenium`` package. Fixed in 2.1.2
   already.

-  Standalone: Added support for ``hydra`` package. Fixed in 2.1.2
   already.

New Features
============

-  For Nuitka package configuration, we now have ``change_class``
   similar to ``change_function`` to replace a full class definition
   with something else, this can be used to modify classes to become
   stubs or even unusable.

-  For the experimental ``@pyqtSlot`` decorator, we also should handle
   the ``@asyncSlot`` just the same. Added in 2.1.1 already.

Optimization
============

-  ArchLinux: Enable static libpython by default, it is usable indeed.
   Added in 2.1.2 already.

-  Anti-Bloat: Avoid ``unittest`` usage in ``antlr`` package.

-  Anti-Bloat: Avoid ``IPython`` in ``celery`` package. Added in 2.1.2
   already.

Organisational
==============

-  UI: Catch wrong values for ``--jobs`` value sooner, negative and
   non-integer values error exit immediately. Added in 2.1.1 already.

Summary
=======

This release is not yet done, but is supposed to focus again on
scalability.

.. include:: ../dynamic.inc
