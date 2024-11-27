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

-  Standalone: Improved ``arcade`` configuration. Added in 2.4.3
   already.

-  Standalone: Add data file for ``license-expression``. package Added
   in 2.4.6 already.

-  Standalone: Added missing implicit dependency for ``pydantic`` needed
   for deprecated decorators to work. Fixed in 2.4.5 already.

-  Standalone: Added missing implicit dependency for ``spacy`` package.
   Added in 2.4.7 already.

-  Standalone: Added support for newer ``trio`` package. Added in 2.4.8
   already.

-  Standalone: Added support for newer ``tensorflow`` package. Added in
   2.4.8 already.

-  Standalone: Added support for ``pygame-ce``. Added in 2.4.8 already.

-  Standalone: Added support for newer ``toga`` on Windows. Added in
   2.4.9 already.

-  Fix, workaround ``django`` debug wanting to extract column numbers of
   compiled frames. Added in 2.4.9 already.

-  Standalone: Allow more potentially unusable plugins for ``PySide6``
   to be recognized on macOS. Added in 2.4.9 already.

-  Standalone: Added missing dependency of ``polars`` package. Added in
   2.4.9 already.

-  Standalone: Enhanced handling of absence of django settings module
   parameter. Added in 2.4.9 already.

-  Standalone: Added missing implicit dependency of ``win32ctypes``
   modules on Windows. Added in 2.4.9 already.

-  Standalone: Added missing data file for ``arcade`` packaged. Added in
   2.4.9 already.

-  Standalone: Allow PySide6 extras to not be installed on macOS, was
   complaining about missing DLLs, which of course can be normal in that
   case. Added in 2.4.11 already.

-  Standalone: Added ``driverless-selenium`` support. Added in 2.4.11
   already.

-  Standalone: Added support for newer ``tkinterdnd2``. Added in 2.4.11
   already.

-  Standalone: Added support for newer ``kivymd``. Added in 2.4.11
   already.

-  Standalone: Added support for ``gssapi``. Added in 2.4.11 already.

-  Standalone: Added support for ``azure.cognitiveservices.speech`` on
   macOS too.

-  Standalone: Added support for ``mne``.

-  Standalone: Added missing dependency of ``fastapi`` package.

-  Standalone: Added support for newer ``pyav`` package.

-  Standalone: Added support for ``py_mini_racer`` package.

-  Standalone: Support ``keras`` extending its sub-modules path to the
   ``keras.api`` sub-package.

-  Standalone: Added support for newer ``transformers`` package.

-  Standalone: Added support for newer ``win32com.server.register``
   package.

-  Python3.12+: Added support for ``distutils`` in ``setuptools``.

-  Standalone: Added missing implicit imports for ``cv2`` package, now
   they are scanned automatically.

-  Standalone: Added support for ``lttbc`` package.

-  Standalone: Added missing dependency of ``win32file`` package.

-  Standalone: Fix, ``kivy`` clipboard was not working on Linux due to
   missing dependencies.

-  Standalone: Add missing ``paddleocr`` data files.

-  Standalone: Added support for ``playwright`` package.

-  Standalone: Allow PySide6 extras to not be installed on macOS. Was
   complaining about missing DLLs, which of course can be normal if
   these are not installed.

New Features
============

-  Added experimental support for Python 3.13, it is not recommended to
   be used yet, since the amount of testing applied is not yet up to the
   task. Also on Windows, only MSVC and ClangCL work with it at this
   time, as workarounds for incompatible structure layouts will take
   time.

-  UI: Added new selector ``--mode``.

   This will replace the other options ``--standaone``, ``--onefile``,
   ``--module``, and ``--macos-create-app-bundle``.

   .. note::

      To address differences between macOS and other OSes for best
      deployment option, the value ``app`` with create an app bundle on
      macOS and a onefile binary elsewhere.

-  UI: Add new choice ``hide`` for ``--windows-console-mode`` option.
   With this mode, a console program is generated, but it hides the
   console as soon as possible, but it might still flash briefly.

-  UI: Added support for not using bytecode cache files

   With ``--python-flag=-B`` we can make imports use only source files
   and never ``.pyc`` files. Mostly relevant for accelerated mode and
   dynamic imports in case of non-isolation standalone mode.

-  Modules: Generate type stubs for generated modules

   Using ``stubgen`` as an inline copy, we can now finally provide
   meaningful stubs that should even be better than with other tools,
   but since the tool is fresh it may still have a lot of issues to
   discover.

   Also adds implicit imports still, so compiled extension modules don't
   hide dependencies.

-  Plugins: Change data files configuration over to list of items as
   well, which allows to use ``when`` conditions. Done in 2.4.6 already.

-  Onefile: Splash screen no longe requires MSVC, but works with
   MinGW64, Clang, and ClangCL too. Done for 2.4.8 already.

-  Reports: Add file system encoding of compiling Python to aid in
   debugging encoding issues.

-  Windows: Console mode ``attach`` enhancements for forced redirects
   work better now, but it's still not perfect.

-  Distutils: Allow disabling nuitka in ``pyproject.toml`` builds as
   well. A new setting ``build_with_nuitka`` can be used to specify to
   fallback to the standard ``build`` backend instead. This can be
   passed on the command line too, with ``--config-setting`` and allows
   to disable Nuitka without changing code or configuration.

-  Distutils: Added support for commercial file embedding, now packages
   can be built with this.

-  Linux: Added support for uninstalled self-compiled Python on this OS
   as well.

-  Plugins: Have ``matplotlib`` plugin react to active Qt and
   ``tk-inter`` plugins for backend selection.

-  Added new attribute ``original_argv0`` to ``__compiled__`` value to
   make the start value accessible.

   When we make ``sys.argv[0]`` an absolute value, information is lost
   that might be needed. The new attribute can be used by application
   that need this information.

-  Reports: Added list of DLLs actively excluded due to being outside of
   the PyPI package.

-  Plugins: Can now override compilation mode for standard library
   modules if necessary, previously that was ignored.

Optimization
============

-  Experimental support for dual types. For specific cases, speed ups of
   integer operating loops of 12x and more are achieved. This code is
   not fully ready for prime time yet, but a lot of improvements are
   going to come from this direction in the future.

-  Faster module variables accesses

   For Python3.6 up to 3.10 inclusive, this is based on dictionary
   version tags and prone to them changing with module variable writes,
   so it's not effective in cases where variables are written
   alternating.

   For Python3.11+ this is based on dictionary keys versions and less
   prone to dictionary changes affecting it, but also slower in case of
   cache hits compared to 3.10 cache hits.

-  Faster string dictionary lookups for Python3.11+, solving a TODO
   about taking advantage of special knowledge we have about the key and
   the module dictionary likely being a string dictionary.

-  Do not update module dictionaries unless it's actually a value
   change. This makes caching more effective in some cases.

-  Enhanced exception handling

   Use exception state to abstract 3.12 or before differences. This
   solves a TODO about more very in-efficient C code generated that also
   requires many conversions of exceptions back and forth from 3 value
   form to normalized. The new code is also better for older Python
   versions.

-  Avoid using CPython APIs for exception context and cause values,
   these can be a lot slower to call.

-  For creating ``int`` or ``long`` values, some codes were not using
   our own creation methods that will be faster to use since we avoid
   API calls.

-  Have our own variant of ``_PyGen_FetchStopIterationValue`` to avoid
   slower API calls in generator handling.

-  Windows: Follow CPython undoing its own inline function usage for
   reference counting on Windows for Python3.12+. Without this, LTO can
   make us a lot slower without clear boundaries.

-  Also statically optimize unary operations, so we can have more
   complete number operations, and be well geared for full support of
   dual types with number types.

-  Statically optimize ``os.stat`` and ``os.lstat`` calls as well.

-  Pass the exception state into unpacking functions for more efficient
   code. No need to fetch exceptions per use of those into the exception
   state, but it can directly write to there.

-  Solve TODO and have dedicated helper for unpacking length check,
   giving faster and more compact code.

-  Have our own variant of ``_PyGen_FetchStopIterationValue`` to avoid
   API calls in generator handling.

-  Generate more efficient code for raising exceptions of builtin type.
   Rather than calling them as a function, create them via base
   exception new directly which will be much quicker.

-  Faster exception creation, avoid having ``args`` and a tuple needed
   to hold them for empty exceptions avoiding one more allocation.

-  Removed remaining uses of ``PyTuple_Pack`` and replace with our own
   helpers to avoid API calls.

-  Avoid implicit exception raise nodes with delayed creation, and have
   direct exception making nodes instead.

-  Windows and Python3.12+: Follow CPython undoing its own inline
   function usage for reference count handling. Without this, LTO can
   make us a lot slower without due to MSVC issues.

-  Avoid API calls when creating ``int`` values in more cases. Some of
   our specialization code and many helpers as well as the constants
   blob loading codes were not avoiding these unnecessary calls, since
   we have faster code for a while already.

-  Windows: Avoid even scanning for DLLs in ``PATH`` if we don't want to
   use them from the system anyway. This ought to avoid crashes related
   to found DLLs with non-encodable paths, as they never get detected
   and need not be discarded later on.

-  Windows: Use newer MinGW64 version, this should produce slight better
   final code.

-  Avoid module level constants for our global values ``-1``, ``0``,
   ``1`` as we have global values for them already leading to smaller
   constant blobs.

-  Put ``NameError`` exceptions directly into the thread state as passed
   for more compact C code generated with variables.

-  The values ``sys.ps1`` and ``sys.ps2`` are statically optimized to
   not exist compiling for the module mode. This should enable more
   static optimization of imports with some packages trying to detect
   interactive usage on the Python REPL.

-  UI: Only use ``tqdm`` locking in no-GIL and inside Scons builds where
   threading actually plays a role at this time.

-  Optimization: Faster check for non-frame statement sequences. Frames
   and normal statement sequence are no longer directly related, but use
   mixin code instead. Dedicated accessors will be faster and are used a
   lot during the optimization phase.

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
