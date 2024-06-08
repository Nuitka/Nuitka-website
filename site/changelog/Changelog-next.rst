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

-  UI: Fix, correct reversed ``disable`` / ``force`` and wrong option
   name recommendation for ``--windows-console-mode`` when the user used
   old-style options.

-  Python3.10+: Fix, must not check for ``len`` greater or equal of 0 or
   for sequence ``match`` cases. That is unnecessary and incompatible
   and can raise exceptions with custom sequences not implementing
   ``__len__``. Fixed in 2.3.1 already.

-  Python3.10+: Fix, ``match`` sequence with final star arguments failed
   in some cases to capture the rest and left the assigned value empty.
   Fixed in 2.3.1 already.

-  Standalone: Added data file for older ``bokeh`` version. Fixed in
   2.3.1 already.

-  Python3.8+: Fix, calls to variable args functions now need to be done
   differently, or else they can crash, as was observed with 3.10 in PGO
   instrumentation, at least. Fixed in 2.3.1 already.

-  PGO: Fix, using ``nuitka-run`` did not execute the program created.
   Fixed in 2.3.1 already.

-  Standalone: Fix, avoid using ``os`` module before setting up our meta
   path based loader. Fixed in 2.3.1 already.

-  Standalone: Support older ``pandas`` versions as well.

-  Linux: Support extension modules used as DLLs by other DLLs or
   extension modules. That makes newer ``tensorflow`` and potentially
   more packages work again. Fixed in 2.3.1 already.

-  Python3.10+: Matches classes were not fully compatible.

   We need to check against case-defined class ``__match_args__``, not
   the matched value type ``__match_args`` that is not necessarily the
   same.

   Also, properly annotating the exception exit of subscript matches
   now; the subscript value can raise an exception.

   Collect keyword and positional match values in one go and detect
   duplicate attributes used, which we previously did not.

New Features
============

-  None yet.

Optimization
============

-  Statically optimize constant subscripts of variables with immutable
   constant values.

-  Python3.8+: Calls of C functions are faster and more compact code
   using vector calls too.

-  Anti-Bloat: Avoid using ``unittest`` in ``keras`` package. Added in
   2.3.1 already.

-  Standalone: Statically optimize by OS in ``sysconfig``.

   Consequently, standalone distributions can exclude OS-specific
   packages such as ``_aix_support`` and ``_osx_support``.

-  Anti-Bloat: Avoid ``distutils`` from ``_oxs_support`` (used by
   ``sysconfig``) module on macOS.

-  Avoid compiling large ``opcua`` modules that generate huge C files
   much like ``asyncua`` package. Added in 2.3.1 already.

Organizational
==============

-  Added badges to the ``README.rst`` of **Nuitka** to display package
   support and more. Added in 2.3.1 already.

-  UI: Use the retry decorator when removing directories in general. It
   will be more thorough with properly annotated retries on Windows. For
   the dist folder, mention the running program as a probable cause.

-  Quality: Check ``replacements`` and ``replacements_plain`` Nuitka
   package configuration values.

-  Debugging: Disable pagination in ``gdb`` with the ``--debugger``
   option.

-  PGO: Warn if the PGO binary does not run successfully.

-  UI: The new console mode option is a Windows-specific option now,
   move it to that group.

Tests
=====

-  macOS: Make actually use of ``ctypes`` in its standalone test to be
   sure it actually works fine.

Cleanups
========

-  Avoid using ``anti-bloat`` configuration values ``replacements``
   where ``replacements_plain`` is good enough.

-  Avoid Python3 and Python3.5+ specific Jinja2 modules on versions
   before that, and consequently avoid warning about the ``SyntaxError``
   given.

-  Minor spelling cleanups.

Summary
=======

This release is not yet done.

.. include:: ../dynamic.inc
