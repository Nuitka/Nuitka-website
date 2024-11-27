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
   Nuitka standalone backend support and enhanced 3.12 performance,
   experimental 3.13 support and scalability in general.

This release in not complete yet.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  **Windows:** Fixed a regression in onefile mode that incorrectly
   handled program and command line paths containing spaces. Fixed in
   2.4.4 already.

-  **Windows:** Corrected an issue where console output handles were
   being opened with closed file handles. Fixed in 2.4.2 already.

-  **Standalone:** Restored the ability to use trailing slashes on the
   command line to specify the target directory for data files on
   Windows. Fixed in 2.4.2 already.

-  **Compatibility:** Fixed a parsing error that occurred with relative
   imports in ``.pyi`` files, which could affect some extension modules
   with available source code. Fixed in 2.4.3 already.

-  **Modules:** Ensured that extension modules load correctly into
   packages when using Python 3.12. Fixed in 2.4.4 already.

-  **Windows:** Improved command line handling for onefile mode to
   ensure full compatibility with quoting. Fixed in 2.4.4 already.

-  **Data Directories:** Allowed the use of non-normalized paths on the
   command line when specifying data directories. Fixed in 2.4.5
   already.

-  **Python 3.11+:** Fixed an issue where ``inspect`` module functions
   could raise ``StopIteration`` when examining compiled functions on
   the stack. Fixed in 2.4.5 already.

-  **importlib_metadata:** Improved compatibility with
   ``importlib_metadata`` by handling cases where it might be broken,
   preventing potential compilation crashes. Fixed in 2.4.5 already.

-  **Plugins:** Fixed a crash that occurred when using the
   ``no_asserts`` YAML configuration option. Fixed in 2.4.6 already.

-  **Scons:** Improved error tolerance when reading ``ccache`` log files
   to prevent crashes on Windows caused by non-ASCII module names or
   paths. Fixed in 2.4.11 already.

-  **Scons:** Prevented the C standard option from being applied to C++
   compilers, resolving an issue with the splash screen on Windows when
   using Clang. Fixed in 2.4.8 already.

-  **macOS:** Enhanced handling of DLL self-dependencies to accommodate
   cases where DLLs use both ``.so`` and ``.dylib`` extensions for
   self-references. Fixed in 2.4.8 already.

-  **Compatibility:** Fixed a memory leak that occurred when using
   ``deepcopy`` on compiled methods. Fixed in 2.4.9 already.

-  **MSYS2:** Excluded the ``bin`` directory from being considered a
   system DLL folder when determining DLL inclusion. Fixed in 2.4.9
   already.

-  **Python 3.10+:** Fixed a crash that could occur when a ``match``
   statement failed to match a class with arguments. Fixed in 2.4.9
   already.

-  **MSYS2:** Implemented a workaround for non-normalized paths returned
   by ``os.path.normpath`` in MSYS2 Python environments. Fixed in 2.4.11
   already.

-  **Python 3.12:** Resolved an issue where Nuitka's constant code was
   triggering assertions in Python 3.12.7. Fixed in 2.4.10 already.

-  **--include-package:** Ensured that the ``--include-package`` option
   includes both Python modules and extension modules that are
   sub-modules of the specified package. Fixed in 2.4.11 already.

-  **Windows:** Prevented encoding issues with CMD files used for
   accelerated mode on Windows.

-  **Standalone:** Improved the standard library scan to avoid assuming
   the presence of specific files, which might have been deleted by the
   user or a Python distribution.

-  **Compatibility:** Added ``suffix``, ``suffixes``, and ``stem``
   attributes to Nuitka resource readers to improve compatibility with
   file objects.

-  **Compatibility:** Backported the error message change for ``yield
   from`` used at the module level, using dynamic detection instead of
   hardcoded text per version.

-  **Compatibility:** Fixed an issue where calling built-in functions
   with keyword-only arguments could result in errors due to incorrect
   argument passing.

-  **Compatibility:** Fixed reference leaks that occurred when using
   ``list.insert`` and ``list.index`` with 2 or 3 arguments.

-  **Windows:** Prioritized relative paths over absolute paths for the
   result executable when absolute paths are not file system encodable.
   This helps address issues related to non-ASCII short paths on some
   Chinese systems.

-  **Compatibility:** Improved compatibility with C extensions by
   handling cases where the attribute slot is not properly implemented,
   preventing potential segfaults.

-  **Compatibility:** Prevent the leakage of ``sys.frozen`` when using
   the ``multiprocessing`` module and its plugin, resolving a
   long-standing TODO and potentially breaking compatibility with
   packages that relied on this behavior.

-  **Compatibility:** Fixed an issue where matching calls with
   keyword-only arguments could lead to incorrect optimization and
   argument passing errors.

-  **Compatibility:** Corrected the handling of iterators in for loops
   to avoid assuming the presence of slots, preventing potential issues.

-  **macOS:** Added support for cyclic DLL dependencies, where DLLs have
   circular references.

-  **Compatibility:** Ensured the use of updated expressions during
   optimization phase for side effects to prevent crashes caused by
   referencing obsolete information.

-  **Python 3.10+:** Fixed a crash that could occur in complex cases
   when re-formulating ``match`` statements.

-  **Python 3.4-3.5:** Corrected an issue in Nuitka's custom
   ``PyDict_Next`` implementation that could lead to incorrect results
   in older Python 3 versions.

-  **Python 3.10+:** Ensured that ``AttributeError`` is raised with the
   correct keyword arguments, avoiding a ``TypeError`` that occurred
   previously.

-  **Plugins:** Added a data file function that avoids loading packages,
   preventing potential crashes caused by incompatible dependencies
   (e.g., ``numpy`` versions).

-  **Compatibility:** Ensured that Nuitka's package reader closes data
   files after reading them to prevent resource warnings in certain
   Python configurations.

-  **Standalone:** Exposed ``setuptools`` contained vendor packages in
   standalone distributions to match the behavior of the ``setuptools``
   package.

-  **Accelerated Mode:** Enabled the ``django`` module parameter in
   accelerated mode to correctly detect used extensions.

-  **Compatibility:** Prevented resource warnings for unclosed files
   when trace outputs are sent to files via command line options.

-  **Compatibility:** Enabled the use of ``xmlrpc.server`` without
   requiring the ``pydoc`` module.

-  **Plugins:** Fixed an issue in the ``anti-bloat`` configuration where
   ``change_function`` and ``change_classes`` ignored "when" clauses,
   leading to unintended changes.

-  **Python 3.12 (Linux):** Enhanced static ``libpython`` handling for
   Linux. Static ``libpython`` is now used only when the inline copy is
   available (not in official Debian packages). The inline copy of
   ``hacl`` is used for all Linux static ``libpython`` uses with Python
   3.12 or higher.

-  **Standalone:** Further improved the standard library scan to avoid
   assuming the presence of files that might have been manually deleted.

Package Support
===============

-  **arcade:** Improved standalone configuration for the ``arcade``
   package. Added in 2.4.3 already.

-  **license-expression:** Added a missing data file for the
   ``license-expression`` package in standalone distributions. Added in
   2.4.6 already.

-  **pydantic:** Included a missing implicit dependency required for
   deprecated decorators in the ``pydantic`` package to function
   correctly in standalone mode. Fixed in 2.4.5 already.

-  **spacy:** Added a missing implicit dependency for the ``spacy``
   package in standalone distributions. Added in 2.4.7 already.

-  **trio:** Updated standalone support for newer versions of the
   ``trio`` package. Added in 2.4.8 already.

-  **tensorflow:** Updated standalone support for newer versions of the
   ``tensorflow`` package. Added in 2.4.8 already.

-  **pygame-ce:** Added standalone support for the ``pygame-ce``
   package. Added in 2.4.8 already.

-  **toga:** Added standalone support for newer versions of the ``toga``
   package on Windows. Added in 2.4.9 already.

-  **django:** Implemented a workaround for a ``django`` debug feature
   that attempted to extract column numbers from compiled frames. Added
   in 2.4.9 already.

-  **PySide6:** Improved standalone support for ``PySide6`` on macOS by
   allowing the recognition of potentially unusable plugins. Added in
   2.4.9 already.

-  **polars:** Added a missing dependency for the ``polars`` package in
   standalone distributions. Added in 2.4.9 already.

-  **django:** Enhanced handling of cases where the ``django`` settings
   module parameter is absent in standalone distributions. Added in
   2.4.9 already.

-  **win32ctypes:** Included missing implicit dependencies for
   ``win32ctypes`` modules on Windows in standalone distributions. Added
   in 2.4.9 already.

-  **arcade:** Added a missing data file for the ``arcade`` package in
   standalone distributions. Added in 2.4.9 already.

-  **PySide6:** Allowed ``PySide6`` extras to be optional on macOS in
   standalone distributions, preventing complaints about missing DLLs
   when they are not installed. Added in 2.4.11 already.

-  **driverless-selenium:** Added standalone support for the
   ``driverless-selenium`` package. Added in 2.4.11 already.

-  **tkinterdnd2:** Updated standalone support for newer versions of the
   ``tkinterdnd2`` package. Added in 2.4.11 already.

-  **kivymd:** Updated standalone support for newer versions of the
   ``kivymd`` package. Added in 2.4.11 already.

-  **gssapi:** Added standalone support for the ``gssapi`` package.
   Added in 2.4.11 already.

-  **azure.cognitiveservices.speech:** Added standalone support for the
   ``azure.cognitiveservices.speech`` package on macOS.

-  **mne:** Added standalone support for the ``mne`` package.

-  **fastapi:** Added a missing dependency for the ``fastapi`` package
   in standalone distributions.

-  **pyav:** Updated standalone support for newer versions of the
   ``pyav`` package.

-  **py_mini_racer:** Added standalone support for the ``py_mini_racer``
   package.

-  **keras:** Improved standalone support for ``keras`` by extending its
   sub-modules path to include the ``keras.api`` sub-package.

-  **transformers:** Updated standalone support for newer versions of
   the ``transformers`` package.

-  **win32com.server.register:** Updated standalone support for newer
   versions of the ``win32com.server.register`` package.

-  **Python 3.12+:** Added support for ``distutils`` in ``setuptools``
   for Python 3.12 and later.

-  **cv2:** Enabled automatic scanning of missing implicit imports for
   the ``cv2`` package in standalone distributions.

-  **lttbc:** Added standalone support for the ``lttbc`` package.

-  **win32file:** Added a missing dependency for the ``win32file``
   package in standalone distributions.

-  **kivy:** Fixed an issue where the ``kivy`` clipboard was not working
   on Linux due to missing dependencies in standalone distributions.

-  **paddleocr:** Added missing data files for the ``paddleocr`` package
   in standalone distributions.

-  **playwright:** Added standalone support for the ``playwright``
   package with a new plugin.

-  **PySide6:** Allowed ``PySide6`` extras to be optional on macOS in
   standalone distributions, preventing complaints about missing DLLs
   when they are not installed.

New Features
============

-  **Python 3.13:** Added experimental support for Python 3.13.

   .. warning::

      Python 3.13 support is not yet recommended for production use due
      to limited testing. On Windows, only MSVC and ClangCL are
      currently supported due to workarounds needed for incompatible
      structure layouts.

-  **UI:** Introduced a new ``--mode`` selector to replace the options
   ``--standalone``, ``--onefile``, ``--module``, and
   ``--macos-create-app-bundle``.

   .. note::

      The ``app`` mode creates an app bundle on macOS and a onefile
      binary on other operating systems to provide the best deployment
      option for each platform.

-  **Windows:** Added a new ``hide`` choice for the
   ``--windows-console-mode`` option. This generates a console program
   that hides the console window as soon as possible, although it may
   still briefly flash.

-  **UI:** Added the ``--python-flag=-B`` option to disable the use of
   bytecode cache (``.pyc``) files during imports. This is mainly
   relevant for accelerated mode and dynamic imports in non-isolated
   standalone mode.

-  **Modules:** Enabled the generation of type stubs (``.pyi`` files)
   for compiled modules using an inline copy of ``stubgen``. This
   provides more accurate and informative type hints for compiled code.

   .. note::

      Nuitka also adds implicit imports to compiled extension modules,
      ensuring that dependencies are not hidden.

-  **Plugins:** Changed the data files configuration to a list of items,
   allowing the use of ``when`` conditions for more flexible control.
   (Done in 2.4.6 already)

-  **Onefile:** Removed the MSVC requirement for the splash screen in
   onefile mode. It now works with MinGW64, Clang, and ClangCL. (Done
   for 2.4.8 already)

-  **Reports:** Added information about the file system encoding used
   during compilation to help debug encoding issues.

-  **Windows:** Improved the ``attach`` mode for
   ``--windows-console-mode`` when forced redirects are used.

-  **Distutils:** Added the ability to disable Nuitka in
   ``pyproject.toml`` builds using the ``build_with_nuitka`` setting.
   This allows falling back to the standard ``build`` backend without
   modifying code or configuration. This setting can also be passed on
   the command line using ``--config-setting``.

-  **Distutils:** Added support for commercial file embedding in
   ``distutils`` packages.

-  **Linux:** Added support for using uninstalled self-compiled Python
   installations on Linux.

-  **Plugins:** Enabled the ``matplotlib`` plugin to react to active Qt
   and ``tkinter`` plugins for backend selection.

-  **Runtime:** Added a new ``original_argv0`` attribute to the
   ``__compiled__`` value to provide access to the original start value
   of ``sys.argv[0]``, which might be needed by applications when Nuitka
   modifies it to an absolute path.

-  **Reports:** Added a list of DLLs that are actively excluded because
   they are located outside of the PyPI package.

-  **Plugins:** Allowed plugins to override the compilation mode for
   standard library modules when necessary.

Optimization
============

-  **Performance:** Implemented experimental support for "dual types",
   which can significantly speed up integer operations in specific cases
   (achieving speedups of 12x or more in some very specific loops). This
   feature is still under development but shows promising potential for
   future performance gains, esp. when combined with future PGO (Profile
   Guided Optimization) work revealing likely runtime types more often
   and more types being covered.

-  **Performance:** Improved the speed of module variable access.

      -  For Python 3.6 to 3.10, this optimization utilizes dictionary
         version tags but may be less effective when module variables
         are frequently written to.

      -  For Python 3.11+, it relies on dictionary key versions, making
         it less susceptible to dictionary changes but potentially
         slightly slower for cache hits compared to Python 3.10.

-  **Performance:** Accelerated string dictionary lookups for Python
   3.11+ by leveraging knowledge about the key and the module
   dictionary's likely structure. This also resolves a previous TODO
   item, where initial 3.11 support was not as fast as our support for
   3.10 was in this domain.

-  **Performance:** Optimized module dictionary updates to occur only
   when values actually change, improving caching efficiency.

-  **Performance:** Enhanced exception handling by removing bloat in the
   abstracted differences between Python 3.12 and earlier versions. This
   simplifies the generated C code, reduces conversions, and improves
   efficiency for all Python versions. This affects both C compile time
   and runtime performance favorably and solves a huge TODO for Python
   3.12 performance.

-  **Performance:** Removed the use of CPython APIs calls for accessing
   exception context and cause values, which can be slow.

-  **Performance:** Utilized Nuitka's own faster methods for creating
   ``int`` and ``long`` values, avoiding slower CPython API calls.

-  **Performance:** Implemented a custom variant of
   ``_PyGen_FetchStopIterationValue`` to avoid CPython API calls in
   generator handling, further improving performance on generators,
   coroutines and asyncgen.

-  **Windows:** Aligned with CPython's change in reference counting
   implementation on Windows for Python 3.12+, which improves
   performance with LTO (Link Time Optimization) enabled.

-  **Optimization:** Expanded static optimization to include unary
   operations, improving the handling of number operations and preparing
   for full support of dual types.

-  **Optimization:** Added static optimization for ``os.stat`` and
   ``os.lstat`` calls.

-  **Performance:** Passed the exception state directly into unpacking
   functions, eliminating redundant exception fetching and improving
   code efficiency.

-  **Performance:** Introduced a dedicated helper for unpacking length
   checks, resulting in faster and more compact code helping scalability
   as well.

-  **Performance:** Generated more efficient code for raising built-in
   exceptions by directly creating them through the base exception's
   ``new`` method instead of calling them as functions. This can speed
   up some things by a lot.

-  **Performance:** Optimized exception creation by avoiding unnecessary
   tuple allocations for empty exceptions. This hack avoids hitting the
   memory allocator as much.

-  **Performance:** Replaced remaining uses of ``PyTuple_Pack`` with
   Nuitka's own helpers to avoid CPython API calls.

-  **Code Generation:** Replaced implicit exception raise nodes with
   direct exception creation nodes for improved C code generation.

-  **Windows:** Aligned with CPython's change in managing object
   reference counters on Windows for Python 3.12+, improving performance
   with LTO enabled.

-  **Performance:** Removed remaining CPython API calls when creating
   ``int`` values in various parts of the code, including specialization
   code, helpers, and constants loading.

-  **Windows:** Avoided scanning for DLLs in the ``PATH`` environment
   variable when they are not intended to be used from the system. This
   prevents potential crashes related to non-encodable DLL paths and
   makes those scans faster too.

-  **Windows:** Updated to a newer MinGW64 version from 13.2 to 14.2 for
   potentially improved binary code generation with that compiler.

-  **Code Size:** Reduced the size of constant blobs by avoiding
   module-level constants for the global values ``-1``, ``0``, and
   ``1``.

-  **Code Generation:** Improved code generation for variables by
   directly placing ``NameError`` exceptions into the thread state when
   raised, making for more compact C code.

-  **Optimization:** Statically optimized the ``sys.ps1`` and
   ``sys.ps2`` values to not exist (unless in module mode), potentially
   enabling more static optimization in packages that detect interactive
   usage checking them.

-  **Performance:** Limited the use of ``tqdm`` locking to no-GIL and
   Scons builds where threading is actively used.

-  **Optimization:** Implemented a faster check for non-frame statement
   sequences by decoupling frames and normal statement sequences and
   using dedicated accessors. This improves performance during the
   optimization phase.

Anti-Bloat
==========

-  Avoid including ``importlib_metadata`` for ``numpy`` package. Added
   in 2.4.2 already.

-  Anti-Bloat: Avoid ``dask`` usage in ``pandera`` package. Added in
   2.4.5 already.

-  Anti-Bloat: Removed ``numba`` for newer ``shap`` as well. Added in
   2.4.6 already.

-  Anti-Bloat: Avoid attempts to include Python2 and Python3 code both
   for ``aenum``. This avoids ``SyntaxError`` warnings with that
   package. Added in 2.4.7 already.

-  Anti-Bloat: Enhanced handling for ``sympy`` package. Added in 2.4.7
   already.

-  Anti-Bloat: Need to allow ``pydoc`` for ``pyqtgraph`` package. Added
   in 2.4.7 already.

-  Anti-Bloat: Avoid ``pytest`` in ``time_machine`` package. Added in
   2.4.9 already.

-  Anti-Bloat: Avoid ``pytest`` in ``anyio`` package.

-  Anti-Bloat: Avoid ``numba`` in ``pandas`` package.

-  Anti-Bloat: Updated for newer ``torch`` package with more coverage.

-  Anti-Bloat: Avoid ``pygame.tests`` and ``cv2`` for ``pygame``
   package.

-  Anti-Bloat: Need to allow ``unittest`` in ``absl.testing`` package.

-  Anti-Bloat: Need to allow ``setuptools`` in ``tufup`` package.

-  Anti-Bloat: Avoid test modules when using ``bsdiff4`` package.

-  Anti-Bloat: Using the ``wheel`` module is the same as using
   ``setuptools`` package.

Organizational
==============

-  Quality: Added dev containers support to the repository, for easy
   setup of a Linux based development environment. This needs more
   refinement though.

-  GitHub: Make it clear that the reproducer has to be tested against
   Python first, to make sure it's an issue of Nuitka to begin with.

-  GitHub: Make clear we do not want ``--deployment`` in issue reports
   are made, since it prevents automatic identification of issues.

-  UI: Make it more clear that the for using external file options, a
   file needs inclusion first.

-  UI: The Qt plugins should check if a plugin family to be included
   even exists. Specifying something that doesn't even exist went
   unnoticed so far.

-  UI: Added support for recognizing terminal link support
   heuristically. This prepares our command line options for adding
   links to options and their groups.

-  UI: Removed obsolete options related to caching from the help output,
   we now got the general ones that do it all.

-  Plugins: Better error messages when querying information from
   packages at compile time.

-  Quality: Workaround ``isort`` bug that cannot handle UTF8 comments.

-  Quality: Use ``clang-format-20`` in GitHub actions.

-  Quality: Use the latest version of ``black``.

-  Release script tests for Debian and PyPI used old runner names, not
   the new ones. Changed in 2.4.1 already.

-  UI: Disable locking of progress bar, as Nuitka doesn't use threads at
   this time.

-  UI: Added support for recognizing terminal link support
   heuristically. And added a first terminal link as an experiment to be
   completed later.

-  Debugging: The explain reference counts could crash on strange
   ``dict`` values. Can mistake them be for a module, when that's not
   the case.

-  Debugging: Print reference counts of tracebacks too when dumping
   reference counts at program end.

-  Debugging: Added assertions and traces for input/output handling.

-  Quality: Check configuration module names in Nuitka package
   configuration. This should catch cases where filenames are used
   mistakenly.

-  UI: Removed obsolete options controlling cache options, should use
   the general ones now.

-  Fix, the option ``--include-raw-dir`` was not working, only the
   Nuitka Package configuration was.

-  Scons: Fix, ``CC`` environment was not used for ``--version`` and not
   for the onefile bootstrap build, but only the Python build. This lead
   to inconsistent outputs and inconsistent compiler usage in these
   cases.

-  Added mnemonic ``compiled-package-hidden-by-package`` for use in
   distutils as it's normal to get this warning there, when we replace
   the Python package with a compiled package and have still to delete
   the Python code.

-  Started experimental support for downloaded Nuitka dependencies like
   ``ordered-set`` and the like. Not ready for general use yet.

Tests
=====

-  Added Python3.13 to GitHub Actions.

-  Much enhanced construct based tests for clearer results. We now just
   execute the code and its alternative with a boolean flag passed
   rather than producing different code, might lead to removing our
   custom templating entire.

-  Remove ``2to3`` conversion code, we don't want to use it anymore as
   its getting removed from newer Python, instead split up tests as
   necessary with version requirements.

-  Fix, test runner didn't discover and therefore did not use
   Python3.12+ leading to almost no tests being run for it on GitHub
   Action.

-  Make sure to default to executing python when comparing results with
   ``compare_with_cpython`` rather than expecting ``PYTHON`` environment
   to be set.

-  Azure: Set up CI with Azure Pipelines to run the Nuitka tests against
   factory branch on commit.

-  Always use static libpython for construct based tests. We don't
   really want to see DLL call overhead there.

-  Made many construct tests less susceptible to other unrelated
   optimization changes.

-  Remove test only working for Nuitka commercial, not useful to always
   skip it for the standard version. Commercial tests are now recognized
   from their names as well.

-  Catch segfault for distutils test cases and give debug output there
   as well, useful in case of these kind of test failures.

-  Avoid resource warning for unclosed files in reflected test.

Cleanups
========

-  WASI: Make sure C function getters and setters of compiled types have
   the correct signature that they are being called with. Cast locally
   to the compiled types only, rather than in the function signature.

   Also the call entries offered now have the matching signature as used
   by Python C code.

-  WASI: Cleanup, follow ``PyCFunction`` signatures as well.

-  Indentation of generated code was regressed and generating unaligned
   code in some cases.

-  Quality: Avoid format differences for ``clang-format-20``, so it
   doesn't matter if the new or old version is used.

-  Cleanup, enforce proper indentation of Nuitka cache files in Json
   format.

-  Changed checks for Python3.4 or higher to be Python3, since that's
   what this means to us, since Python3.3 is no longer supported. In
   some cases, re-formulation of some codes got simpler from this.

-  Cleanup, found remaining Python3.3 only code in frame templates and
   removed it.

-  Many spelling cleanups, renaming internal helper functions where
   needed.

-  Plugins: Renamed ``get_module_directory`` Nuitka Package
   Configuration helper to a name without leading underscore.

-  Move ``numexpr.cpuinfo`` workaround to proper Nuitka Package
   configuration. This solves an old TODO.

Summary
=======

This release is not done yet.

.. include:: ../dynamic.inc
