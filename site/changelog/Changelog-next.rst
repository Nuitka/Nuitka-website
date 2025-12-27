:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.0rc3**.

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

-  **UI:** The ``--output-dir`` option was not being honored in
   accelerated mode when ``--output-filename`` was also provided. (Fixed
   in 2.8.2 already.)

-  **UI:** The ``--output-filename`` option help said it wouldn't work
   for standalone mode when in fact it did for a while already. (Fixed
   in 2.8.2 already.)

-  **Onefile:** On **Windows**, fixed a crash when using
   ``--output-dir`` where it was checking for the wrong folder to exist.
   (Fixed in 2.8.2 already.)

-  **macOS:** Fixed a crash that could occur when many package-specific
   directories were used, which could lead to the ``otool`` command line
   being too long. (Fixed in 2.8.2 already.)

-  **Standalone:** For the "Python Build Standalone" flavor, ensured
   that debug builds correctly recognize all their specific built-in
   modules, preventing potential errors. (Fixed in 2.8.4 already.)

-  **macOS:** Fix, avoid setting ``$ORIGIN`` r-paths that end up unused
   and in some cases cause errors because the header space is exhausted
   preventing the build entirely. (Fixed in 2.8.5 already.)

-  **macOS:** Fix, make sure to use system ``xattr`` binary.

   Otherwise using ``arch -x86_64 python`` for compilation can fail when
   some packages are installed that provide ``xattr`` too, as that is a
   ``arm64`` binary only and then wouldn't work. (Fixed in 2.8.5
   already.) ``arm64`` binary only and then wouldn't work. (Fixed in
   2.8.5 already.)

-  **UI:** Fixed a misleading typo in the rejection message for
   unsupported Python 3.13.4. (Fixed in 2.8.5 already.)

-  **Accelerated:** The runner scripts ``.cmd`` or ``.sh`` now are also
   placed respecting the ``--output-filename`` and ``--output-dir``
   options. (Fixed in 2.8.5 already.)

-  **Plugins:** Ensured that plugins detected by namespace usage are
   also activated in module mode. (Fixed in 2.8.5 already.)

-  **Standalone:** Fixed an issue where non-existent packages listed in
   ``top_level.txt`` files could cause errors during metadata
   collection. (Fixed in 2.8.6 already.)

-  **Standalone:** Corrected the classification of the ``site`` module,
   which was previously treated as a standard library module in some
   cases. (Fixed in 2.8.6 already.)

-  **Windows:** Ensured that temporary link libraries and export files
   created during compilation are properly deleted, preventing them from
   being included in the standalone distribution. (Fixed in 2.8.6
   already.)

-  **Python3.14:** Adapted to core changes by no longer inlining
   ``hacl`` code for this version. (Fixed in 2.8.6 already.)

-  Fixed a potential for mis-optimization for uses of locals
   ``locals()`` when transforming the variable name reference call.
   (Fixed in 2.8.6 already.)

-  **Module:** Fixed ``pkgutil.iter_modules`` not working when loading a
   module into a namespace. (Fixed in 2.8.7 already.)

-  **Reports:** Fixed a crash when creating the compilation report
   before the source directory is created. (Fixed in 2.8.7 already.)

-  **Standalone:** Fixed ignoring of non-existent packages from
   ``top_level.txt`` for metadata. (Fixed in 2.8.7 already.)

-  **UI:** The ``--no-progress-bar`` option was not disabling the
   **Scons** progress bars. (Fixed in 2.8.7 already.)

-  **UI:** Fixed an exception in the ``tqdm`` progress bar during
   process shutdown. (Fixed in 2.8.7 already.)

-  **Windows:** Fixed incorrect ``sys.executable`` value in onefile DLL
   mode. (Fixed in 2.8.9 already.)

-  **Python3.14:** Added missing implicit dependency for ``_ctypes`` on
   **Windows**. (Fixed in 2.8.9 already.)

-  **Python3.13+:** Fixed missing export of ``PyInterpreter_*`` API.

-  **Python3.14:** Adapted to change in evaluation order of ``__exit__``
   and ``__enter__``.

Package Support
===============

-  **Anti-Bloat:** Avoided a warning during program shutdown when using
   a compiled ``xgboost`` package. (Fixed in 2.8.1 already.)

-  **Standalone:** Added support for the ``oracledb`` package. (Fixed in
   2.8.2 already.)

-  **macOS:** Added support for newer ``PySide6`` versions. (Fixed in
   2.8.4 already.)

-  **Standalone:** Added support for including more metadata for the
   ``transformers`` package. (Fixed in 2.8.5 already.)

-  **Standalone:** Metadata from Nuitka Package Configuration is now
   only included if the corresponding package is part of the
   compilation. (Fixed in 2.8.5 already.)

-  **Standalone:** Added support for the ``win32ctypes`` package. (Fixed
   in 2.8.6 already.)

-  **Standalone:** Added support for newer versions of the ``dask``
   package. (Fixed in 2.8.6 already.)

-  **Standalone:** Added support for the ``dataparser`` package. (Added
   in 2.8.7 already.)

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

-  Standalone: Honor ``--nofollow-import-to`` for stdlib modules as
   well.

   This allows users to manually reduce the standard library usage too,
   but of course also to shoot themselves into their feet and have
   crashes from extension modules not prepared for absence of standard
   library modules.

-  Onefile: Allow to disable onefile timeout and hard killing on CTRL-C
   entirely by providing ``--onefile-child-grace-time=infinity``.

-  **Scons:** Added newer inline copy of **Scons** which supports Visual
   Studio 2026. (Added in 2.8.7 already.)

-  **Scons:** Allowed using Python versions only partially supported for
   **Nuitka** with **Scons**. (Added in 2.8.7 already.)

-  **UI:** Added option ``--devel-profile-compilation`` for compile time
   profiling. Also renamed the old runtime profiling option
   ``--profile`` to ``--debug-profile-runtime``, that is however still
   broken.

-  **Reports:** Including CPU instr and cycle counters in timing on
   native Linux.

   -  With appropriate configuration on Linux this allows to get at very
      precise timing configuration so we can judge even small compile
      time improvements correctly. We then don't need many runs to
      average out noise from other effects.

   -  Don't use wall clock but process time for steps that are not doing
      IO like module optimization for more accurate values otherwise, it
      is however not very accurate still.

-  **Python3.12+:** Added support for function type syntax (generics).

-  **Python3.14:** Added groundwork for deferred evaluation of function
   annotations.

-  **Python3.14:** Added support for uncompiled generator integration
   which is crucial for ``asyncio`` correctness and general usability
   with modern frameworks.

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

-  **Windows:** Made the caching of external paths effective, which
   significantly speeds up DLL resolution in subsequent compilations.
   (Fixed in 2.8.6 already.)

-  Recognized module variable usages inside outlined functions that are
   in a loop, which improves the effectiveness of caching. (Fixed in
   2.8.6 already.)

-  **Optimization:** Avoid including ``tzdata`` on non-Windows
   platforms. (Fixed in 2.8.7 already.)

-  **macOS:** Removed extended attributes from data files as well,
   improving performance. (Fixed in 2.8.7 already.)

-  **Scons:** Stopped detecting installed **MinGW** to avoid overhead as
   it is not supported. (Fixed in 2.8.9 already.)

-  Much faster Python passes.

   -  The "Escape" and "Unknown" traces now have their own number
      spaces. This allows to do some tests for a trace without using the
      actual object.

   -  Narrow the scope of variables to the outline scope that uses them,
      so that they don't need to be dealt with in merging later code
      where they don't ever change anymore and are not used at all.

   -  When checking for unused variables, do not ask the trace
      collection to filter its traces, instead work of the ones attached
      in the variable already. This avoids a lot of searching work. Also
      use a method to decide if a trace constitutes usage rather than a
      long ``elif`` chain.

   -  For "PASS 1" of ``telethon.tl.types`` which has been one of the
      known trouble makers with many classes and type annotations all
      changes combined improve the compilation time by 800%.

-  Also decide presence of writing traces for parameter variables
   faster.

-  Faster variable trace maintenance.

   -  We now trace variables in trace collection as a dictionary per
      variable with a dictionary of the versions, this is closer to out
      frequent usage per variable.

   -  That makes it a lot easier to update variables after the tracing
      is finished to know their users and writers.

   -  Requires a lot less work, but also makes work less memory local
      such that the performance gain is relatively small despite less
      work being done.

   -  Also avoids that a per variable set for the using scopes of it is
      to be maintained.

-  Detect variable references discarded sooner for better micro-pass
   efficiency. We were spending an extra pass on the whole module to
   stabilize the variable usage, which can end up being a lot of work.

-  After a module optimization pass found no changes, we no longer make
   an extra micro pass to avoid stabilization bugs, but only check
   against it not happening in debug mode. Depending on the number of
   micro passes, this can be a relatively high performance gain. For the
   ``telethon.tl.types`` module this was a 13% performance gain on top.

Anti-Bloat
==========

None yet.

Organizational
==============

-  UI: Don't say ``--include-data-files-external`` doesn't work in
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

-  UI: The help text for ``--include-data-files-external`` was updated
   to reflect that it works in standalone mode. (Fixed in 2.8.5
   already.)

-  **Release:** Use lowercase names for source archives in PyPI uploads.
   (Fixed in 2.8.7 already.)

-  **Quality:** Fix, wasn't passing assume yes for downloads for the
   commit hook.

-  **UI:** Improved wording for missing C compiler message.

-  **Debugging:** More clear verbose trace for dropped expressions.

-  **Debugging:** Output what module had extra changes during debug
   extra micro pass.

Tests
=====

None yet.

Cleanups
========

-  **Python3.14:** Fixed a type mismatch warning seen with **MSVC**.
   (Fixed in 2.8.9 already.)

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
