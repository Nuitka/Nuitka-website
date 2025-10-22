:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

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

-  **Accelerated:** The enhanced detection for uninstalled Anaconda and
   WinPython was not fully working. (Fixed in 2.8.1 already.)

-  **Onefile:** Fixed an issue in DLL mode where signal handlers were
   not being registered, which could prevent proper program termination
   on signals like CTRL-C. (Fixed in 2.8.1 already.)

-  **Windows:** Fixed incorrect handling of forward slashes in cache
   directory paths, which caused issues with Nuitka-Action. (Fixed in
   2.8.1 already.)

-  macOS: Fix, avoid setting $ORIGIN r-paths that end up unused and in
   some cases cause errors because the header space is exhausted
   preventing the build entirely. (Fixed in 2.8.5 already.)

-  macOS: Fix, make sure to use system ``xattr`` binary.

   Otherwise using "arch -x86_64 python" for compilation can fail when
   some packages are installed that provide "xattr" too, as that is a
   "arm64" binary only. (Fixed in 2.8.5 already.)

Package Support
===============

-  **Anti-Bloat:** Avoided a warning during program shutdown when using
   a compiled ``xgboost`` package. (Fixed in 2.8.1 already.)

New Features
============

-  **Zig:** Added experimental support for using **Zig** project's ``zig
   cc`` as a C compiler backend for **Nuitka**. This can be enabled by
   setting the ``CC`` environment variable to point to the ``zig`` or
   ``zig.exe`` executable.

-  Reports: Start to capture ``rusage`` capture for OSes that support
   it.

   -  Only POSIX compliant OSes will do it, **Linux**, **macOS**, and
      all **BSD** variants do it, but **Android** does not.
   -  Not yet part of the actual report, as need to figure out how to
      use the and present the information.

-  Scons: Added experimental support for enabling Thin LTO with
   **Clang** compiler.

-  Standalone: Honor "--nofollow-import-to" for stdlib modules as well.

   This allows users to manually reduce the standard library usage too,
   but of course also to shoot themselves into their feet and have
   crashes from extension modules not prepared for absence of standard
   library modules.

-  Onefile: Allow to disable onefile timeout and hard killing on CTRL-C
   entirely by providing ``--onefile-child-grace-time=infinity``.

Optimization
============

-  Find previous assignment traces faster

   -  The assignment and del nodes were using functions to find what
      they already knew from the last micro pass. The
      ``self.variable_trace`` already kept track of the previous value
      trace situation.

   -  For matching unescaped traces we will do similar, but it's not
      really used right now, so make it only a TODO as that will
      eventually be very similar.

   -  Also speeds up the first micro pass even more, because it doesn't
      have to search and do other things, if not previous trace exists,
      that's then not attempted to be used.

   -  Also the common check if no by name or merges of a value occurred
      was always used inverted and now should be slightly faster to use
      and allow to short circuit.

   -  While this accelerated the first micro pass by a lot for per
      assignment work, it mainly means to cleanup the design such that
      traces are easier to re-recognize. And this is a first step with
      immediate impacts.

-  **Standalone:** Also solve partially a TODO of minimizing
   intermediate directories in r-paths of ELF platforms, by only putting
   them there if the directory the point to will contain DLLs or
   binaries. This removes unused elements and reduces r-path size.

Anti-Bloat
==========

None yet.

Organizational
==============

-  UI: Don't say "--include-data-files-external" doesn't work in
   standalone mode

   It actually does for a while, and we since renamed that option, but
   the help still said it wouldn't work in standalone mode.

-  Debugging: Added assertions for code object creation

   We wer getting assertions from Python when built with **Zig**, and
   these are supposed to do those as well.

-  Debugging: In case of tool commands failing, output the too long
   command line if that was the error given.

-  Anti-Bloat: Don't allow custom ``nofollow`` modes, point the user to
   the correct option instead. This was never needed, but two ways of
   providing this user decision make no sense.

Tests
=====

None yet.

Cleanups
========

None yet.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
