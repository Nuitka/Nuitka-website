:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.0rc9**.

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

-  **Python 3.14:** Follow allocator changes and immortal flags changes.

-  **Python 3.14:** Follow GC changes for compiled frames as well.

-  **Python 3.14:** Catch attempts to clear a compiled suspended frame
   object.

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

-  **Multiprocessing:** Fixed issue where ``sys.argv`` was not yet
   corrected when ``argparse`` was used early in spawned processes.

-  **Scons:** Fixed an issue where Zig was not used as a fallback when
   MinGW64 was present but unusable.

-  **Windows:** Made onefile binary work on systems without runtime DLLs
   installed as well.

-  **Scons:** Made tracing robust against threaded outputs.

-  **Python3.12+:** Enhanced workaround for loading of extension modules
   with sub-packages to cover more cases.

-  **Scons:** Fixed missing Zig version output.

-  **Scons:** Fixed Zig detection to enforce PATH or CC usage on macOS
   instead of download, since it's not available.

-  **UI:** Fixed normalization of user paths, improving macOS support
   for reporting.

-  **Linux:** Fix, the workaround for ``memset`` zero length warning was
   wrongly applied to **Clang** as well, but only **GCC** needs it and
   **Clang** complained about it.

-  **Linux:** More robust fallback to ``g++`` when ``gcc`` is too old
   for C11 support.

-  **Compatibility:** Fix, ``del`` of a subscript could cause wrong
   runtime behavior due to missing control flow escape annotation for
   the subscript value itself and the index.

-  **macOS:** Fix, ``Info.plist`` user facing entitlements keys mapping
   to multiple internal entitlements were not handled correctly.

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

-  **Standalone:** Added support for ``puremagic``, ``pygment.lexers``
   and ``tomli`` in standalone mode.

-  **Standalone:** Added automatic detection of ``mypyc`` runtime
   dependencies, no need to manually configure that anymore. Also our
   configuration was often only correct for a single OS, and single
   upstream versions which is now fixed for packages having it before.

New Features
============

-  **UI:** Added support for ``--project`` parameter to build using
   configuration from ``pyproject.toml`` (e.g. Poetry, Setuptools).

   With this, you can simply run ``python -m nuitka --project
   --mode=onefile`` and it will use the ``pyproject.toml`` or
   ``setup.py/setup.cfg`` files to get the configuration and build the
   Nuitka binary.

   Previously Nuitka could only be used for building wheels with
   ``build`` package, and for building wheels that is still the best
   way.

   The ``--project`` option is currently compatible with ``build`` and
   ``poetry`` and detects the used build system automatically.

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

-  **Debugging:** Added ``--debug-self-forking`` to debug fork bombs.

-  **Windows:** Added ``--include-windows-runtime-dlls`` option to
   control inclusion of Windows C runtime DLLs. Defaults to ``auto``.

-  **Python 3.14:** Added experimental support for deferred annotations.

-  **Plugins:** Added option ``--qt-debug-plugins`` for debugging Qt
   plugin loading.

-  **DLLs:** Added support for DLL tags to potentially control inclusion
   with more granularity.

-  **macOS:** Added support for many more protected resource
   entitlements (Siri, Bluetooth, HomeKit, etc.) to the bundle details.

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

   -  Decide presence of writing traces for parameter variables faster.

-  Avoiding unnecessary micro passes.

   -  Detect variable references discarded sooner for better micro-pass
      efficiency. We were spending an extra pass on the whole module to
      stabilize the variable usage, which can end up being a lot of
      work.

   -  After a module optimization pass found no changes, we no longer
      make an extra micro pass to avoid stabilization bugs, but only
      check against it not happening in debug mode. Depending on the
      number of micro passes, this can be a relatively high performance
      gain. For the ``telethon.tl.types`` module this was a 13%
      performance gain on top.

-  For "PASS 1" of ``telethon.tl.types`` which has been one of the known
   trouble makers with many classes and type annotations all changes
   combined improve the compilation time by 1500%.

-  Faster code generation.

   -  Indentation in generated C code is no longer performed to speed up
      code generation. To restore readability, use the new option
      ``--devel-generate-readable-code`` which will use ``clang-format``
      to format the C code.

-  Recognized module variable usages inside outlined functions that are
   in a loop, which improves the effectiveness of caching at run-time.
   (Added in 2.8.6 already.)

-  **Standalone:** Solve partially a TODO of minimizing intermediate
   directories in r-paths of ELF platforms, by only putting them there
   if the directory the point to will contain DLLs or binaries. This
   removes unused elements and reduces r-path size.

-  **Windows:** Made the caching of external paths effective, which
   significantly speeds up DLL resolution in subsequent compilations.
   (Fixed in 2.8.6 already.)

-  **macOS:** Removed extended attributes from data files as well,
   improving performance. (Fixed in 2.8.7 already.)

-  **Scons:** Stopped detecting installed **MinGW** to avoid overhead as
   it is not supported. (Fixed in 2.8.9 already.)

-  **Scons:** Added caching for MSVC information to reduce compilation
   time and if already available, use that to detect Windows SDK
   location rather that using ``vswhere.exe`` each time.

-  Avoided large ``%`` string interpolations at compile time, these
   could cause large code as a result.

-  Avoid including ``importlib._bootstrap`` and
   ``importlib._bootstrap_external`` as they are available as frozen
   modules.

-  Fixed un-hashable dictionary keys not being properly optimized,
   forcing runtime handling.

Anti-Bloat
==========

-  Avoid including ``tzdata`` on non-Windows platforms. (Fixed in 2.8.7
   already.)

-  Avoid ``pyparsing.testing`` in ``pyparsing`` package.

-  Added configuration to avoid compiled via C for large generated files
   for the ``sqlfluff`` package.

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

-  **Quality:** Manage more development tools (``clang-format``, etc.)
   via private pip space for better consistency and isolation.

-  **AI:** Enhanced pull request template with directions for AI-driven
   PRs.

-  **AI:** Added agent command ``create-mre`` to assist in creating a
   minimal reproduction example (**MRE**).

-  **User Manual:** Added documentation about redistribution
   requirements for Python 3.12-3.14.

-  **Quality:** Added ``--un-pushed`` argument to auto-format tool for
   checking only un-pushed changes.

-  **Scons:** Improved error message to point to Zig support if no C
   compiler is found.

-  **MonolithPy:** Follow rename of our Python fork to **MonolithPy** to
   avoid confusion with the **Nuitka** compiler project itself.

-  **Scons:** Prefer English output and warn user for missing English
   language pack with MSVC in case or outputs being made.

-  **UI:** When running non-interactively, print the default response
   that is assumed for user queries to stdout as well, so it becomes
   visible in the logs.

-  **UI:** Warn when using protected resources options without
   standalone/bundle mode enabled on **macOS**.

-  **Reports:** Sort DLLs and entry points in compilation reports by
   destination path for deterministic output.

-  **Quality:** Skip files with ``spell-checker: disable`` in
   ``codespell`` checks.

-  **Release:** Avoid compiling bytecode for inline copies that are not
   compatible with the running **Python** version during install.

Tests
=====

-  Added support for ``--all`` with ``--max-failures`` option to the
   test runner to stop after a specified number of failures, or just run
   all tests and output the failed tests in the end.

   Also the tests specified can be a glob pattern, to match multiple
   tests, not just a test name.

   Added examples to the help output of the runner to guide the usage of
   the developers.

-  Ignore multiline source code outputs of Python3.14 in tracebacks for
   output comparison, Nuitka won't do those.

-  Added test cases for poetry and distutils. Also verify that
   standalone mode works with ``--project`` for the supported build
   systems.

-  Made the distutils tests cases much more consistent.

-  **Watch:** Improved binary name detection from compilation reports
   for better mode support beyond standalone mode.

-  Allow downloading tools (like ``clang-format``) for all test cases.

-  Added options to enforce **Zig** or **Clang** usage for C compiling.

-  Suppress ``pip`` output when not running interactively to avoid test
   output differences.

-  Added ``nuitka.format`` and ``nuitka.package_config`` to
   self-compilation tests.

Cleanups
========

-  Moved options to new ``nuitka.options`` package.

-  **Python3.14:** Fixed a type mismatch warning seen with **MSVC**.
   (Fixed in 2.8.9 already.)

-  Massive amounts of spelling cleanups. Correct spelling is more and
   more places allows identification of bugs more immediately, therefore
   these are very worthwhile.

-  Code cleanup and style improvements in ``Errors`` and
   ``OutputDirectories`` modules.

-  Replaced usages of ``os.environ.get`` with ``os.getenv`` for
   consistency and denser code.

-  Moved **MSVC** re-dist detection to ``DllDependenciesWin32``.

-  **Release:** Don't install ``zstandard`` by default anymore.

-  **UI:** Tone down complaint about checksum mismatches.

-  Static source files are now provided by Nuitka directly.

-  Renamed C function ``modulecode_`` to ``module_code_`` for
   consistency.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
