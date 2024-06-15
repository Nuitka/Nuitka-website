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

This release is not complete yet.

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
   in some cases to capture the rest. The assigned value then was
   empty.when it shouldn't have been. Fixed in 2.3.1 already.

-  Standalone: Added data file for older ``bokeh`` version. Fixed in
   2.3.1 already.

-  Python3.8+: Fix, calls to variable args functions now need to be done
   differently, or else they can crash, as was observed with 3.10 in PGO
   instrumentation, at least. Fixed in 2.3.1 already.

-  PGO: Fix, using ``nuitka-run`` did not execute the program created.
   Fixed in 2.3.1 already.

-  Standalone: Support older ``pandas`` versions as well.

-  Linux: Support extension modules used as DLLs by other DLLs or
   extension modules. That makes newer ``tensorflow`` and potentially
   more packages work again. Fixed in 2.3.1 already.

-  Python3.10+: Matches classes were not fully compatible.

   We need to check against case-defined class ``__match_args__``, not
   the matched value type ``__match_args`` that is not necessarily the
   same.

   Also, properly annotating the exception exit of subscript matches;
   the subscript value can indeed raise an exception.

   Collect keyword and positional match values in one go and detect
   duplicate attributes used, which we previously did not.

-  Scons: Fix, do not crash when ``clang`` is not reporting its version
   correctly. It happened if **Clang** usage was required with
   ``--clang`` option but not installed. Fixed in 2.3.2 already.

-  Debian: Fix, detecting the **Debian** flavor of Python was not
   working anymore, and as a result, the intended defaults were no
   longer applied by **Nuitka**, leading to incorrect suggestions that
   didn't work. Fixed in 2.3.3 already.

-  Ubuntu: Fix, the static link library for Python 3.12 is not usable
   unless we provide parts of **HACL** for the ``sha2`` module so as not
   to cause link errors. Fixed in 2.3.3 already.

-  Standalone: Fix, importing newer ``pkg_resources`` was crashing.
   Fixed in 2.3.3 already.

-  Python3.11+: Added support for ``dill-compat``. Fixed in 2.3.4
   already.

-  Standalone: Added support for the newer ``kivy`` version and added
   macOS support as well. Fixed in 2.3.4 already.

-  Standalone: Support locating Windows icons for ``pywebview``. Fixed
   in 2.3.4 already.

-  Standalone: Added support for ``spacy`` related packages. Fixed in
   2.3.4 already.

-  Python3.12: Our workaround for ``cv2`` support cannot use the ``imp``
   module anymore. Fixed in 2.3.4 already.

-  Added support for ``__init__`` files that are extension modules.
   Architecture checks for macOS were false negatives for them, and the
   case insensitive import scan failed to find them on Windows. Fixed in
   2.3.4 already.

-  Standalone: Added implicit dependencies of ``lxml.sax`` module. Fixed
   in 2.3.4 already.

-  Standalone: Added implicit dependencies for ``zeroconf`` package.
   Fixed in 2.3.4 already.

-  Standalone: Added missing dependencies for standard library extension
   modules, mainly exhibited on macOS. Fixed in 2.3.4 already.

-  Windows: Fix build failures on mapped network drives. Fixed in 2.3.4
   already.

New Features
============

-  Experimental support for Python 3.13 beta 2. We try and follow its
   release cycle closely and aim to support it at the time of Python
   release.

-  Scons: Added experimental option
   ``--experimental=force-system-scons`` to enforce system Scons to be
   used. That allows for the non-use of inline copy, which can be
   interesting for experiments with newer Scons releases. Added in 2.3.2
   already.

-  Debugging: A new non-deployment handler was added when segmentation
   faults occurred. The crashing program then outputs a message pointing
   to a page with helpful information unless the deployment mode is
   active.

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

-  macOS: Make actual use of ``ctypes`` in its standalone test to ensure
   correctness on that OS, too.

-  Make compile extension module test work on macOS, too.

Cleanups
========

-  Avoid using ``anti-bloat`` configuration values ``replacements``
   where ``replacements_plain`` is good enough.

-  Avoid Python3 and Python3.5+ specific Jinja2 modules on versions
   before that, and consequently, avoid warning about the
   ``SyntaxError`` given.

-  Moved code object extraction of ``dill-compat`` plugin from Python
   module template to C code helper for shared usage and better editing.

-  Minor spelling cleanups.

Summary
=======

This release is not yet done.

.. include:: ../dynamic.inc
