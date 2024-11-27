.. post:: 2024/11/27
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 2.5
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release focused on Python 3.13 support, but also on improved
compatibility, made many performance optimizations, enhanced error
reporting, and better debugging support.

***********
 Bug Fixes
***********

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
   by ``os.path.normpath`` in **MSYS2** Python environments. Fixed in
   2.4.11 already.

-  **Python 3.12:** Resolved an issue where Nuitka's constant code was
   triggering assertions in Python 3.12.7. Fixed in 2.4.10 already.

-  **UI:** Ensured that the ``--include-package`` option includes both
   Python modules and extension modules that are sub-modules of the
   specified package. Fixed in 2.4.11 already.

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

-  **UI:** Fixed the ``--include-raw-dir`` option, which was not
   functioning correctly. Only the Nuitka Package configuration was
   being used previously.

*****************
 Package Support
*****************

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

**************
 New Features
**************

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
   Done in 2.4.6 already.

-  **Onefile:** Removed the MSVC requirement for the splash screen in
   onefile mode. It now works with MinGW64, Clang, and ClangCL. Done for
   2.4.8 already.

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

**************
 Optimization
**************

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

************
 Anti-Bloat
************

-  Prevented the inclusion of ``importlib_metadata`` for the ``numpy``
   package. Added in 2.4.2 already.

-  Avoided the use of ``dask`` in the ``pandera`` package. Added in
   2.4.5 already.

-  Removed ``numba`` for newer versions of the ``shap`` package. Added
   in 2.4.6 already.

-  Prevented attempts to include both Python 2 and Python 3 code for the
   ``aenum`` package, avoiding ``SyntaxError`` warnings. Added in 2.4.7
   already.

-  Enhanced handling for the ``sympy`` package. Added in 2.4.7 already.

-  Allowed ``pydoc`` for the ``pyqtgraph`` package. Added in 2.4.7
   already.

-  Avoided ``pytest`` in the ``time_machine`` package. Added in 2.4.9
   already.

-  Avoided ``pytest`` in the ``anyio`` package.

-  Avoided ``numba`` in the ``pandas`` package.

-  Updated anti-bloat measures for newer versions of the ``torch``
   package with increased coverage.

-  Avoided ``pygame.tests`` and ``cv2`` for the ``pygame`` package.

-  Allowed ``unittest`` in the ``absl.testing`` package.

-  Allowed ``setuptools`` in the ``tufup`` package.

-  Avoided test modules when using the ``bsdiff4`` package.

-  Treated the use of the ``wheel`` module the same as using the
   ``setuptools`` package.

****************
 Organizational
****************

-  **Development Environment:** Added experimental support for a
   devcontainer to the repository, providing an easier way to set up a
   Linux-based development environment. This feature is still under
   development and may require further refinement.

-  **Issue Reporting:** Clarified the issue reporting process on GitHub,
   emphasizing the importance of testing reproducers against Python
   first to ensure the issue is related to Nuitka.

-  **Issue Reporting:** Discouraged the use of ``--deployment`` in issue
   reports, as it hinders the automatic identification of issues, that
   should be the first thing to remove.

-  **UI:** Improved the clarity of help message of the option for
   marking data files as external, emphasizing that files must be
   included before being used.

-  **UI:** Added checks to the Qt plugins to ensure that specified
   plugin families exist, preventing unnoticed errors.

-  **UI:** Implemented heuristic detection of terminal link support,
   paving the way for adding links to options and groups in the command
   line interface.

-  **UI:** Removed obsolete caching-related options from the help
   output, as they have been replaced by more general options.

-  **Plugins:** Improved error messages when retrieving information from
   packages during compilation.

-  **Quality:** Implemented a workaround for an ``isort`` bug that
   prevented it from handling UTF-8 comments.

-  **Quality:** Updated GitHub actions to use ``clang-format-20``.

-  **Quality:** Updated to the latest version of ``black`` for code
   formatting.

-  **Release Process:** Updated the release script tests for Debian and
   PyPI to use the correct runner names. (Changed in 2.4.1 already.

-  **UI:** Disabled progress bar locking, as Nuitka currently doesn't
   utilize threads.

-  **UI:** Added heuristic detection of terminal link support and
   introduced an experimental terminal link as a first step towards a
   more interactive command line interface.

-  **Debugging:** Fixed a crash in the "explain reference counts"
   feature that could occur with unusual ``dict`` values mistaken for
   modules.

-  **Debugging:** Included reference counts of tracebacks when dumping
   reference counts at program end.

-  **Debugging:** Added assertions and traces to improve debugging of
   input/output handling.

-  **Quality:** Added checks for configuration module names in Nuitka
   package configuration to catch errors caused by using filenames
   instead of module names.

-  **UI:** Removed obsolete options controlling cache behavior,
   directing users to the more general cache options.

-  **Scons:** Ensured that the ``CC`` environment variable is used
   consistently for ``--version`` and onefile bootstrap builds, as well
   as the Python build, preventing inconsistencies in compiler usage and
   outputs.

-  **Distutils:** Added the ``compiled-package-hidden-by-package``
   mnemonic for use in ``distutils`` to handle the expected warning when
   a Python package is replaced with a compiled package and the Python
   code is yet to be deleted.

-  **Dependency Management:** Started experimental support for
   downloading Nuitka dependencies like ``ordered-set``. This feature is
   not yet ready for general use.

*******
 Tests
*******

-  Added Python 3.13 to the GitHub Actions test matrix.

-  Significantly enhanced construct-based tests for clearer results. The
   new approach executes code with a boolean flag instead of generating
   different code, potentially leading to the removal of custom
   templating.

-  Removed the ``2to3`` conversion code from the test suite, as it is
   being removed from newer Python versions. Tests are now split with
   version requirements as needed.

-  Fixed an issue where the test runner did not discover and use Python
   3.12+, resulting in insufficient test coverage for those versions on
   GitHub Actions.

-  Ensured that the ``compare_with_cpython`` test function defaults to
   executing the system's Python interpreter instead of relying on the
   ``PYTHON`` environment variable.

-  Set up continuous integration with Azure Pipelines to run Nuitka
   tests against the factory branch on each commit.

-  Enforced the use of static ``libpython`` for construct-based tests to
   eliminate DLL call overhead and provide more accurate performance
   measurements.

-  Improved the robustness of many construct tests, making them less
   sensitive to unrelated optimization changes.

-  Removed a test that was only applicable to Nuitka Commercial, as it
   was not useful to always skip it in the standard version. Commercial
   tests are now also recognized by their names.

-  Added handling for segmentation faults in ``distutils`` test cases,
   providing debug output for easier diagnosis of these failures.

-  Prevented resource warnings for unclosed files in a reflected test.

**********
 Cleanups
**********

-  **WASI:** Corrected the signatures of C function getters and setters
   for compiled types in ``WASI`` to ensure they match the calling
   conventions. Casts are now performed locally to the compiled types
   instead of in the function signature. Call entries also have the
   correct signature used by Python C code.

-  **WASI:** Improved code cleanliness by adhering to ``PyCFunction``
   signatures in ``WASI``.

-  **Code Generation:** Fixed a regression in code generation that
   caused misaligned indentation in some cases.

-  **Code Formatting:** Changed some code for identical formatting with
   ``clang-format-20`` to eliminate differences between the new and old
   versions.

-  **Caching:** Enforced proper indentation in Nuitka cache files stored
   in JSON format.

-  **Code Cleanliness:** Replaced checks for Python 3.4 or higher with
   checks for Python 3, simplifying the code and reflecting the fact
   that Python 3.3 is no longer supported.

-  **Code Cleanliness:** Removed remaining Python 3.3 specific code from
   frame templates.

-  **Code Cleanliness:** Performed numerous spelling corrections and
   renamed internal helper functions for consistency and clarity.

-  **Plugins:** Renamed the ``get_module_directory`` helper function in
   the Nuitka Package configuration to remove the leading underscore,
   improving readability.

-  **Plugins:** Moved the ``numexpr.cpuinfo`` workaround to the
   appropriate location in the Nuitka Package configuration, resolving
   an old TODO item.

*********
 Summary
*********

This a major release that brings support for Python 3.13, relatively
soon after its release.

Our plugin system and Nuitka plugin configuration was used a lot for
support of many more third-party packages, and numerous other
enhancements in the domain of avoiding bloat.

This release focuses on improved compatibility, new break through
performance optimizations, to build on in the future, enhanced error
reporting, and better debugging support.
