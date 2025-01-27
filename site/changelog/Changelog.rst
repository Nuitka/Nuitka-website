:orphan:

#################
 Current Release
#################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per-version changes and comments for
|NUITKA_VERSION_MINOR| down to Nuitka 2.0 release.

.. contents:: Table of Contents
   :local:

********************
 Nuitka Release 2.6
********************

This release has all-around improvements, with a lot effort spent on bug
fixes in the memory leak domain, and preparatory actions for scalability
improvements.

Bug Fixes
=========

-  **MSYS2:** Path normalization to native Windows format was required
   in more places for the ``MinGW`` variant of **MSYS2**.

   The ``os.path.normpath`` function doesn't normalize to native Win32
   paths with MSYS2, instead using forward slashes. This required manual
   normalization in additional areas. (Fixed in 2.5.1)

-  **UI:** Fix, give a proper error when extension modules asked to
   include failed to be located. instead of a proper error message.
   (Fixed in 2.5.1)

-  Fix, files with illegal module names (containing ``.``) in their
   basename were incorrectly considered as potential sub-modules for
   ``--include-package``. These are now skipped. (Fixed in 2.5.1)

-  **Stubgen:** Improved stability by preventing crashes when stubgen
   encounters code it cannot handle. Exceptions from it are now ignored.
   (Fixed in 2.5.1)

-  **Stubgen:** Addressed a crash that occurred when encountering
   assignments to non-variables. (Fixed in 2.5.1)

-  **Python 3:** Fixed a regression introduced in 2.5 release that could
   lead to segmentation faults in exception handling for generators.
   (Fixed in 2.5.2)

-  **Python 3.11+:** Corrected an issue where dictionary copies of large
   split directories could become corrupted. This primarily affected
   instance dictionaries, which are created as copies until updated,
   potentially causing problems when adding new keys. (Fixed in 2.5.2)

-  **Python 3.11+:** Removed the assumption that module dictionaries
   always contain only strings as keys. Some modules, like
   ``Foundation`` on macOS, use non-string keys. (Fixed in 2.5.2)

-  **Deployment:** Ensured that the ``--deployment`` option correctly
   affects the C compilation process. Previously, only individual
   disables were applied. (Fixed in 2.5.2)

-  **Compatibility:** Fixed a crash that could occur during compilation
   when unary operations were used within binary operations. (Fixed in
   2.5.3)

-  **Onefile:** Corrected the handling of
   ``__compiled__.original_argv0``, which could lead to crashes. (Fixed
   in 2.5.4)

-  **Compatibility:** Resolved a segmentation fault occurring at runtime
   when calling ``tensorflow.function`` with only keyword arguments.
   (Fixed in 2.5.5)

-  **macOS:** Harmless warnings generated for x64 DLLs on arm64 with
   newer macOS versions are now ignored. (Fixed in 2.5.5)

-  **Python 3.13:** Addressed a crash in Nuitka's dictionary code that
   occurred when copying dictionaries due to internal changes in Python
   3.13. (Fixed in 2.5.6)

-  **macOS:** Improved onefile mode signing by applying
   ``--macos-signed-app-name`` to the signature of binaries, not just
   app bundles. (Fixed in 2.5.6)

-  **Standalone:** Corrected an issue where too many paths were added as
   extra directories from the Nuitka package configuration. This
   primarily affected the ``win32com`` package, which currently relies
   on the ``package-dirs`` import hack. (Fixed in 2.5.6)

-  **Python 2:** Prevented crashes on macOS when creating onefile
   bundles with Python 2 by handling negative CRC32 values. This issue
   may have affected other versions as well. (Fixed in 2.5.6)

-  **Plugins:** Restored the functionality of code provided in
   ``pre-import-code``, which was no longer being applied due to a
   regression. (Fixed in 2.5.6)

-  **macOS:** Suppressed the app bundle mode recommendation when it is
   already in use. (Fixed in 2.5.6)

-  **macOS:** Corrected path normalization when the output directory
   argument includes "~".

-  **macOS:** GitHub Actions Python is now correctly identified as a
   Homebrew Python to ensure proper DLL resolution. (Fixed in 2.5.7)

-  **Compatibility:** Fixed a reference leak that could occur with
   values sent to generator objects. Asyncgen and coroutines were not
   affected. (Fixed in 2.5.7)

-  **Standalone:** The ``--include-package`` scan now correctly handles
   cases where both a package init file and competing Python files
   exist, preventing compile-time conflicts. (Fixed in 2.5.7)

-  **Modules:** Resolved an issue where handling string constants in
   modules created for Python 3.12 could trigger assertions, and modules
   created with 3.12.7 or newer failed to load on older Python 3.12
   versions when compiled with Nuitka 2.5.5-2.5.6. (Fixed in 2.5.7)

-  **Python 3.10+:** Corrected the tuple code used when calling certain
   method descriptors. This issue primarily affected a Python 2
   assertion, which was not impacted in practice. (Fixed in 2.5.7)

-  **Python 3.13:** Updated resource readers to accept multiple
   arguments for ``importlib.resources.read_text``, and correctly handle
   ``encoding`` and ``errors`` as keyword-only arguments.

-  **Scons:** The platform encoding is no longer used to decode
   ``ccache`` logs. Instead, ``latin1`` is used, as it is sufficient for
   matching filenames across log lines and avoids potential encoding
   errors. (Fixed in 2.5.7)

-  **Python 3.12+:** Requests to statically link libraries for ``hacl``
   are now ignored, as these libraries do not exist. (Fixed in 2.5.7)

-  **Compatibility:** Fixed a memory leak affecting the results of
   functions called via specs. This primarily impacted overloaded hard
   import operations. (Fixed in 2.5.7)

-  **Standalone:** When multiple distributions for a package are found,
   the one with the most accurate file matching is now selected. This
   improves handling of cases where an older version of a package (e.g.,
   ``python-opencv``) is overwritten with a different variant (e.g.,
   ``python-opencv-headless``), ensuring the correct version is used for
   Nuitka package configuration and reporting. (Fixed in 2.5.8)

-  **Python 2:** Prevented a potential crash during onefile
   initialization on Python 2 by passing the directory name directly
   from the onefile bootstrap, avoiding the use of ``os.dirname`` which
   may not be fully loaded at that point. (Fixed in 2.5.8)

-  **Anaconda:** Preserved necessary ``PATH`` environment variables on
   Windows for packages that require loading DLLs from those locations.
   Only ``PATH`` entries not pointing inside the installation prefix are
   removed. (Fixed in 2.5.8)

-  **Anaconda:** Corrected the ``is_conda_package`` check to function
   properly when distribution names and package names differ. (Fixed in
   2.5.8)

-  **Anaconda:** Improved package name resolution for Anaconda
   distributions by checking conda metadata when file metadata is
   unavailable through the usual methods. (Fixed in 2.5.8)

-  **MSYS2:** Normalized the downloaded gcc path to use native Windows
   slashes, preventing potential compilation failures. (Fixed in 2.5.9)

-  **Python 3.13:** Restored static libpython functionality on Linux by
   adapting to a signature change in an unexposed API. (Fixed in 2.5.9)

-  **Python 3.6+:** Prevented ``asyncgen`` from being resurrected when a
   finalizer is attached, resolving memory leaks that could occur with
   ``asyncio`` in the presence of exceptions. (Fixed in 2.5.10)

-  **UI:** Suppressed the gcc download prompt that could appear during
   ``--version`` output on Windows systems without MSVC or with an
   improperly installed gcc.

-  Ensured compatibility with monkey patched ``os.lstat`` or ``os.stat``
   functions, which are used in some testing scenarios.

-  **Data Composer:** Improved the determinism of the JSON statistics
   output by sorting keys, enabling reliable build comparisons.

-  **Python 3.6+:** Fixed a memory leak in ``asyncgen`` with finalizers,
   which could lead to significant memory consumption when using
   ``asyncio`` and encountering exceptions.

-  **Scons:** Optimized empty generators (an optimization result) to
   avoid generating unused context code, eliminating C compilation
   warnings.

-  **Python 3.6+:** Fixed a reference leak affecting the ``asend`` value
   in ``asyncgen``. While typically ``None``, this could lead to
   observable reference leaks in certain cases.

-  **Python 3.5+:** Improved handling of ``coroutine`` and ``asyncgen``
   resurrection, preventing memory leaks with ``asyncio`` and
   ``asyncgen``, and ensuring correct execution of ``finally`` code in
   coroutines.

-  **Python 3:** Corrected the handling of ``generator`` objects
   resurrecting during deallocation. While not explicitly demonstrated,
   this addresses potential issues similar to those encountered with
   coroutines, particularly for old-style coroutines created with the
   ``types.coroutine`` decorator.

-  **PGO:** Fixed a potential crash during runtime trace collection by
   ensuring timely initialization of the output mechanism.

Package Support
===============

-  **Standalone:** Added inclusion of metadata for ``jupyter_client`` to
   support its own usage of metadata. (Added in 2.5.1)

-  **Standalone:** Added support for the ``llama_cpp`` package. (Added
   in 2.5.1)

-  **Standalone:** Added support for the ``litellm`` package. (Added in
   2.5.2)

-  **Standalone:** Added support for the ``lab_lamma`` package. (Added
   in 2.5.2)

-  **Standalone:** Added support for ``docling`` metadata. (Added in
   2.5.5)

-  **Standalone:** Added support for ``pypdfium`` on Linux. (Added in
   2.5.5)

-  **Standalone:** Added support for using the ``debian`` package.
   (Added in 2.5.5)

-  **Standalone:** Added support for the ``pdfminer`` package. (Added in
   2.5.5)

-  **Standalone:** Included missing dependencies for the
   ``torch._dynamo.polyfills`` package. (Added in 2.5.6)

-  **Standalone:** Added support for ``rtree`` on Linux. The previous
   static configuration only worked on Windows and macOS; this update
   detects it from the module code. (Added in 2.5.6)

-  **Standalone:** Added missing ``pywebview`` JavaScript data files.
   (Added in 2.5.7)

-  **Standalone:** Added support for newer versions of the ``sklearn``
   package. (Added in 2.5.7)

-  **Standalone:** Added support for newer versions of the ``dask``
   package. (Added in 2.5.7)

-  **Standalone:** Added support for newer versions of the
   ``transformers`` package. (Added in 2.5.7)

-  **Windows:** Placed ``numpy`` DLLs at the top level for improved
   support in the Nuitka VM. (Added in 2.5.7)

-  **Standalone:** Allowed excluding browsers when including
   ``playwright``. (Added in 2.5.7)

-  **Standalone:** Added support for newer versions of the ``sqlfluff``
   package. (Added in 2.5.8)

-  **Standalone:** Added support for the ``opencv`` conda package,
   disabling unnecessary workarounds for its dependencies. (Added in
   2.5.8)

-  **Standalone:** Added support for newer versions of the ``soundfile``
   package.

-  **Standalone:** Added support for newer versions of the ``coincurve``
   package.

-  **Standalone:** Added support for newer versions of the
   ``apscheduler`` package.

-  **macOS:** Removed the error and workaround forcing that required
   bundle mode for PyQt5 on macOS, as standalone mode now appears to
   function correctly.

-  **Standalone:** Added support for ``seleniumbase`` package downloads.

New Features
============

-  **Module:** Implemented 2-phase loading for all modules in Python 3.5
   and higher. This improves loading modules as sub-packages in Python
   3.12+, where the loading context is no longer accessible.

-  **UI:** Introduced the ``app`` value for the ``--mode`` parameter.
   This creates an app bundle on macOS and a onefile binary on other
   platforms, replacing the ``--macos-create-app-bundle`` option. (Added
   in 2.5.5)

-  **UI:** Added a ``package`` mode, similar to ``module``, which
   automatically includes all sub-modules of a package without requiring
   manual specification with ``--include-package``.

-  **Module:** Added an option to completely disable the use of
   ``stubgen``. (Added in 2.5.1)

-  **Homebrew:** Added support for ``tcl9`` with the ``tk-inter``
   plugin.

-  **Package Resolution:** Improved handling of multiple distributions
   installed for the same package name. Nuitka now attempts to identify
   the most recently installed distribution, enabling proper recognition
   of different versions in scenarios like ``python-opencv`` and
   ``python-opencv-headless``.

-  **Python 3.13.1 Compatibility:** Addressed an issue where a
   workaround introduced for Python 3.10.0 broke standalone mode in
   Python 3.13.1. (Added in 2.5.6)

-  **Plugins:** Introduced a new feature for absolute source paths
   (typically derived from variables or relative to constants). This
   offers greater flexibility compared to the ``by_code`` DLL feature,
   which may be removed in the future. (Added in 2.5.6)

-  **Plugins:** Added support for ``when`` conditions in ``variable``
   sections within Nuitka Package configuration.

-  **macOS:** App bundles now automatically switch to the containing
   directory when not launched from the command line. This prevents the
   current directory from defaulting to ``/``, which is rarely correct
   and can be unexpected for users. (Added in 2.5.6)

-  **Compatibility:** Relaxed the restriction on setting the compiled
   frame ``f_trace``. Instead of outright rejection, the deployment flag
   ``--no-deployment-flag=frame-useless-set-trace`` can be used to allow
   it, although it will be ignored.

-  **Windows:** Added the ability to detect extension module entry
   points using an inline copy of ``pefile``. This enables
   ``--list-package-dlls`` to verify extension module validity on the
   platform. It also opens possibilities for automatic extension module
   detection on major operating systems.

-  **Watch:** Added support for using ``conda`` packages instead of PyPI
   packages.

-  **UI:** Introduced ``--list-package-exe`` to complement
   ``--list-package-dlls`` for package analysis when creating Nuitka
   Package Configuration.

-  **Windows ARM:** Removed workarounds that are no longer necessary for
   compilation. While the lack of dependency analysis might require
   correction in a hotfix, this configuration should now be supported.

Optimization
============

-  **Scalability:** Implemented experimental code for more compact code
   object usage, leading to more scalable C code and constants usage.
   This is expected to speed up C compilation and code generation in the
   future once fully validated.

-  **Scons:** Added support for C23 embedding of the constants blob.
   This will be utilized with Clang 19+ and GCC 15+, except on Windows
   and macOS where other methods are currently employed.

-  **Compilation:** Improved performance by avoiding redundant path
   checks in cases of duplicated package directories. This significantly
   speeds up certain scenarios where file system access is slow.

-  **Scons:** Enhanced detection of static libpython, including for
   self-compiled, uninstalled Python installations.

Anti-Bloat
==========

-  Improved ``no_docstrings`` support for the ``xgboost`` package.
   (Added in 2.5.7)

-  Avoided unnecessary usage of ``numpy`` for the ``PIL`` package.

-  Avoided unnecessary usage of ``yaml`` for the ``numpy`` package.

-  Excluded ``tcltest`` TCL code when using ``tk-inter``, as these TCL
   files are unused.

-  Avoided using ``IPython`` from the ``comm`` package.

-  Avoided using ``pytest`` from the ``pdbp`` package.

Organizational
==============

-  **UI:** Added categories for plugins in the ``--help`` output.
   Non-package support plugin options are now shown by default.
   Introduced a dedicated ``--help-plugins`` option and highlighted it
   in the general ``--help`` output. This allows viewing all plugin
   options without needing to enable a specific plugin.

-  **UI:** Improved warnings for onefile and OS-specific options. These
   warnings are now displayed unless the command originates from a
   Nuitka-Action context, where users typically build for different
   modes with a single configuration set.

-  **Nuitka-Action:** The default ``mode`` is now ``app``, building an
   application bundle on macOS and a onefile binary on other platforms.

-  **UI:** The executable path in ``--version`` output now uses the
   report path. This avoids exposing the user's home directory,
   encouraging more complete output sharing.

-  **UI:** The Python flavor name is now included in the startup
   compilation message.

-  **UI:** Improved handling of missing Windows version information. If
   only partial version information (e.g., product or file version) is
   provided, an explicit error is given instead of an assertion error
   during post-processing.

-  **UI:** Corrected an issue where the container argument for
   ``run-inside-nuitka-container`` could not be a non-template file.
   (Fixed in 2.5.2)

-  **Release:** The PyPI upload ``sdist`` creation now uses a virtual
   environment. This ensures consistent project name casing, as it is
   determined by the setuptools version. While currently using the
   deprecated filename format, this change prepares for the new format.

-  **Release:** The ``osc`` binary is now used from the virtual
   environment to avoid potential issues with a broken system
   installation, as currently observed on Ubuntu.

-  **Debugging:** Added an experimental option to disable the automatic
   conversion to short paths on Windows.

-  **UI:** Improved handling of external data files that overwrite the
   original file. Nuitka now prompts the user to provide an output
   directory to prevent unintended overwrites. (Added in 2.5.6)

-  **UI:** Introduced the alias ``--include-data-files-external`` for
   the external data files option. This clarifies that the feature is
   not specific to onefile mode and encourages its wider use.

-  **UI:** Allowed ``none`` as a valid value for the macOS icon option.
   This disables the warning about a missing icon when intentionally not
   providing one.

-  **UI:** Added an error check for icon filenames without suffixes,
   preventing cases where the file type cannot be inferred.

-  **UI:** Corrected the examples for ``--include-package-data`` with
   file patterns, which used incorrect delimiters.

-  **Scons:** Added a warning about using gcc with LTO when ``make`` is
   unavailable, as this combination will not work. This provides a
   clearer message than the standard gcc warnings, which can be
   difficult for Python users to interpret.

-  **Debugging:** Added an option to preserve printing during reference
   count tests. This can be helpful for debugging by providing
   additional trace information.

-  **Debugging:** Added a small code snippet for module reference leak
   testing to the Developer Manual.

Tests
=====

-  Temporarily disabled tests that expose regressions in Python 3.13.1
   that mean not to follow.

-  Improved test organization by using more common code for package
   tests. The scanning for test cases and main files now utilizes shared
   code.

-  Added support for testing variations of a test with different extra
   flags. This is achieved by exposing a ``NUITKA_TEST_VARIANT``
   environment variable.

-  Improved detection of commercial-only test cases by identifying them
   through their names rather than hardcoding them in the runner. These
   tests are now removed from the standard distribution to reduce
   clutter.

-  Utilized ``--mode`` options in tests for better control and clarity.
   Standalone mode tests now explicitly check for the application of the
   mode and error out if it's missing. Mode options are added to the
   project options of each test case instead of requiring global
   configuration.

-  Added a test case to ensure comprehensive coverage of external data
   file usage in onefile mode. This helps detect regressions that may
   have gone unnoticed previously.

-  Increased test coverage for coroutines and async generators,
   including checks for ``inspect.isawaitable`` and testing both
   function and context objects.

Cleanups
========

-  Unified the code used for generating source archives for PyPI
   uploads, ensuring consistency between production and standard
   archives.

-  Harmonized the usage of ``include <...>`` vs ``include "..."`` based
   on the origin of the included files, improving code style
   consistency.

-  Removed code duplication in the exception handler generator code by
   utilizing the ``DROP_GENERATOR_EXCEPTION`` functions.

-  Updated Python version checks to reflect current compatibility.
   Checks for ``>=3.4`` were changed to ``>=3``, and outdated references
   to Python 3.3 in comments were updated to simply "Python 3".

-  **Scons:** Simplified and streamlined the code for the command
   options. An ``OrderedDict`` is now used to ensure more stable build
   outputs and prevent unnecessary differences in recorded output.

-  Improved the ``executeToolChecked`` function by adding an argument to
   indicate whether decoding of returned ``bytes`` output to ``unicode``
   is desired. This eliminates redundant decoding in many places.

Summary
=======

This a major release that it consolidates Nuitka big time.

The scalability work has progressed, even if no immediately visible
effects are there yet, the next releases will have them, as this is the
main area of improvement these days.

The memory leaks found are very important and very old, this is the
first time that ``asyncio`` should be working perfect with Nuitka, it
was usable before, but compatibility is now much higher.

Also, this release puts out a much nicer help output and handling of
plugins help, which no longer needs tricks to see a plugin option that
is not enabled (yet), during ``--help``. The user interface is hopefully
more clean due to it.

********************
 Nuitka Release 2.5
********************

This release focused on Python 3.13 support, but also on improved
compatibility, made many performance optimizations, enhanced error
reporting, and better debugging support.

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

Organizational
==============

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

Tests
=====

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

Cleanups
========

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

Summary
=======

This a major release that brings support for Python 3.13, relatively
soon after its release.

Our plugin system and Nuitka plugin configuration was used a lot for
support of many more third-party packages, and numerous other
enhancements in the domain of avoiding bloat.

This release focuses on improved compatibility, new break through
performance optimizations, to build on in the future, enhanced error
reporting, and better debugging support.

********************
 Nuitka Release 2.4
********************

This release largely contains bug fixes for the previous changes, but
also finishes full compatibility with the ``match`` statements of 3.10,
something that was long overdue since there were always some
incompatible behaviors there.

In terms of bug fixes, it's also huge. An upgrade is required,
especially for new ``setuptools`` that made compiled programs segfault
at startup.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  UI: Fix, we had reversed ``disable`` / ``force`` and wrong option
   name recommendation for ``--windows-console-mode`` when the user used
   old-style options.

-  Python3.10+: Fix, must not check for ``len`` greater or equal of 0 or
   for sequence ``match`` cases. That is unnecessary and incompatible
   and can raise exceptions with custom sequences not implementing
   ``__len__``. Fixed in 2.3.1 already.

-  Python3.10+: Fix, ``match`` sequence with final star arguments failed
   in some cases to capture the rest. The assigned value then was
   empty.when it shouldn't have been. Fixed in 2.3.1 already.

-  Python3.8+: Fix, calls to variable args functions now need to be done
   differently, or else they can crash, as was observed with 3.10 in PGO
   instrumentation, at least. Fixed in 2.3.1 already.

-  PGO: Fix, using ``nuitka-run`` did not execute the program created as
   expected. Fixed in 2.3.1 already.

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

-  Python3.11+: Added support for newer Python with ``dill-compat``.
   Fixed in 2.3.4 already.

-  Standalone: Support locating Windows icons for ``pywebview``. Fixed
   in 2.3.4 already.

-  Standalone: Added support for ``spacy`` related packages. Fixed in
   2.3.4 already.

-  Python3.12: Fix, our workaround for ``cv2`` support cannot use the
   ``imp`` module anymore. Fixed in 2.3.4 already.

-  Compatibility: Added support for ``__init__`` files that are
   extension modules. Architecture checks for macOS were false negatives
   for them, and the case insensitive import scan failed to find them on
   Windows. Fixed in 2.3.4 already.

-  Standalone: Added missing dependencies for standard library extension
   modules, mainly exhibited on macOS. Fixed in 2.3.4 already.

-  Windows: Fix build failures on mapped network drives. Fixed in 2.3.4
   already.

-  Python3.12: Fix, need to set frame ``prev_inst`` or else ``f_lasti``
   is random. Some packages; for example PySide6; use this to check what
   bytecode calls them or how they import them and it could crash when
   attempting it. Fixed in 2.3.6 already.

-  Fix, fork bomb in ``cpuinfo`` package no longer happens. Fixed in
   2.3.8 already.

-  Nuitka-Python: Fix, cannot ask for shared library prefixes. Fixed in
   2.3.8 already.

-  Standalone: Make sure ``keras`` package dependency for ``tensorflow``
   is visible. Fixed in 2.3.10 already.

-  Linux: Fix, for static executables we should ignore errors setting a
   DLL load path. Fixed in 2.3.10 already.

-  Compatibility: Fix, nuitka resource readers also need to have
   ``.parent`` attribute. Fixed in 2.3.10 already.

-  Fix, need to force no-locale language outputs for tools outputs on
   non-Windows. Our previous methods were not forcing enough.

   For non-Windows this makes Nuitka work on systems with locales active
   for message outputs only. Fixed in 2.3.10 already.

-  Fix, was not using proper result value for ``SET_ATTRIBUTE`` to check
   success in a few corner cases. Fixed in 2.3.10 already.

-  Windows: Retry deleting dist and build folders, allowing users to
   recognize still running programs and not crashing on Anti-Virus
   software still locking parts of them.

-  Fix, ``dict.fromkeys`` didn't give compatible error messages for no
   args given.

-  Fix, output correct unsupported exception messages for in-place
   operations

   For in-place ``**``, it was also incompatible, since it must not
   mention the ``pow`` function.

-  Fix, included metadata could lead to instable code generation. We
   were using a dictionary for it, but that is not as stable order for
   the C compiler to fully benefit.

-  Fix, including data files for packages that are extension modules was
   not working yet.

-  macOS: Detect the DLL path of ``libpython`` (if used) by looking at
   dependencies of the running Python binary rather than encoding what
   CPython does. Doing that covers other Python flavors as well.

-  Fix, need to prefer extension modules over Python code for packages.

-  Fix, immutable constant values are not to be treated as very trusted.

-  Python3: Fix, the ``__loader__`` attribute of a module should be an
   object and not only the class, otherwise only static methods can
   work.

-  Python3: Added ``.name`` and ``.path`` attributes to Nuitka loader
   objects for enhanced compatibility with code that expects source code
   loaders.

-  Fix, the ``sys.argv[0]`` needs to be absolute for best usability.

   For ``dirname(sys.argv[0])`` to be usable even if the program is
   launched via ``PATH`` environment by a shell, we cannot rely on how
   we are launched since that won't be a good path, unlike with Python
   interpreter, where it always is.

-  Standalone: Fix, adding missing dependencies for some crypto
   packages.

-  Python3.12: Need to write to thread local variable during import.
   This however doesn't work for Windows and non-static libpython
   flavors in general.

-  macOS: Enforce using system ``codesign`` as the Anaconda one is not
   working for us.

-  Fix, we need to read ``.pyi`` files as source code. Otherwise unicode
   characters can cause crashes.

-  Standalone: Fix, some packages query private values for distribution
   objects, so use the same attribute name for the path.

-  Multidist: Make sure to follow the multidist reformulation modules.
   Otherwise in accelerated mode, these could end up not being included.

-  Fix, need to hold a reference of the iterable while converting it to
   ``list``.

-  Plugins: Fix, this wasn't properly ignoring ``None`` values in load
   descriptions as intended.

-  macOS: Need to allow DLLs from all Homebrew paths.

-  Reports: Do not crash during report writing for very early errors.

-  Python3.11+: Fix, need to make sure we have ``split`` as a constant
   value when using exception groups.

-  Debian: More robust against problematic distribution folders with no
   metadata, these apparently can happen with OS upgrades.

-  Fix, was leaking exception in case of ``--python-flag=-m`` mode that
   could cause errors.

-  Compatibility: Close standard file handles on process forks as
   CPython does. This should enhance things for compilations using
   ``attach`` on Windows.

Package Support
===============

-  Standalone: Added data file for older ``bokeh`` version. Fixed in
   2.3.1 already.

-  Standalone: Support older ``pandas`` versions as well.

-  Standalone: Added data files for ``panel`` package.

-  Standalone: Added support for the newer ``kivy`` version and added
   macOS support as well. Fixed in 2.3.4 already.

-  Standalone: Include all ``kivy.uix`` packages with ``kivy``, so their
   typical config driven usage is not too hard.

-  Standalone: Added implicit dependencies of ``lxml.sax`` module. Fixed
   in 2.3.4 already.

-  Standalone: Added implicit dependencies for ``zeroconf`` package.
   Fixed in 2.3.4 already.

-  Standalone: Added support for ``numpy`` version 2. Fixed in 2.3.7
   already.

-  Standalone: More complete support for ``tables`` package. Fixed in
   2.3.8 already.

-  Standalone: Added implicit dependencies for ``scipy.signal`` package.
   Fixed in 2.3.8 already.

-  Standalone: Added support for ``moviepy`` and ``imageio_ffmeg``
   packages. Fixed in 2.3.8 already.

-  Standalone: Added support for newer ``scipy``. Fixed in 2.3.10
   already.

-  Standalone: Added data files for ``bpy`` package. For full support
   more work will be needed.

-  Standalone: Added support for ``nes_py`` and ``gym_tetris`` packages.

-  Standalone: Added support for ``dash`` and ``plotly``.

-  Standalone: Added support for ``usb1`` package.

-  Standalone: Added support for ``azure.cognitiveservices.speech``
   package.

-  Standalone: Added implicit dependencies for ``tinycudann`` package.

-  Standalone: Added support for newer ``win32com.server.register``.

-  Standalone: Added support for ``jaxtyping`` package.

-  Standalone: Added support for ``open3d`` package.

-  Standalone: Added workaround for ``torch`` submodule import function.

-  Standalone: Added support for newer ``paddleocr``.

New Features
============

-  Experimental support for Python 3.13 beta 3. We try to follow its
   release cycle closely and aim to support it at the time of CPython
   release. We also detect no-GIL Python and can make use of it. The GIL
   status is output in the ``--version`` format and the GIL usage is
   available as a new ``{GIL}`` variable for project options.

-  Scons: Added experimental option
   ``--experimental=force-system-scons`` to enforce system Scons to be
   used. That allows for the non-use of inline copy, which can be
   interesting for experiments with newer Scons releases. Added in 2.3.2
   already.

-  Debugging: A new non-deployment handler helps when segmentation
   faults occurred. The crashing program then outputs a message pointing
   to a page with helpful information unless the deployment mode is
   active.

-  Begin merging changes for WASI support. Parts of the C changes were
   merged and for other parts, command line option ``--target=wasi`` was
   added, and we are starting to address cross platform compilation for
   it. More work will be necessary to fully merge it, right not it
   doesn't work at all yet.

-  PGO: Added support for using it in standalone mode as well, so once
   we use it more, it will immediately be practical.

-  Make the ``--list-package-dlls`` use plugins as well, and make
   ``delvewheel`` and announce its DLL path internally, too. Listing
   DLLs for packages using plugins can use these paths for more complete
   outputs.

-  Plugins: The ``no-qt`` plugin was usable in accelerated mode.

-  Reports: Added included metadata and reasons for it.

-  Standalone: Added support for ``spacy`` with a new plugin.

-  Compatibility: Use existing source files as if they were ``.pyi``
   files for extension modules. That gives us dependencies for code that
   installs source code and extension modules.

-  Plugins: Make version information, onefile mode, and onefile cached
   mode indication available in Nuitka Package Configuration, too.

-  Onefile: Warn about using ``tendo.singleton`` in non-cached onefile
   mode.

   Tendo uses the running binary name for locking by default. So it's
   not going to work if that changes for each execution, make the user
   aware of that, so they can use cached mode instead.

-  Reports: Include the micro pass counts and tracing merge statistics
   so we can see the impact of new optimization.

-  Plugins: Allow to specify modes in the Nuitka Package Configuration
   for ``annotations``, ``doc_strings``, and ``asserts``. These overrule
   global configuration, which is often not practical. Some modules may
   require annotations, but for other packages, we will know they are
   fine without them. Simply disabling annotations globally barely
   works. For some modules, removing annotations can give a 30%
   compile-time speedup.

-  Standalone: Added module configuration for Django to find commands
   and load its engine.

-  Allow negative values for --jobs to be relative to the system core
   count so that you can tell Nuitka to use all but two cores with
   ``--jobs=-2`` and need not hardcode your current code count.

-  Python3.12: Annotate libraries that are currently not supported

   We will need to provide our own Python3.12 variant to make them work.

-  Python3.11+: Catch calls to uncompiled function objects with compiled
   code objects. We now raise a ``RuntimeError`` in the bytecode making
   it easier to catch them rather than segfaulting.

Optimization
============

-  Statically optimize constant subscripts of variables with immutable
   constant values.

-  Forward propagate very trusted values for variable references
   enabling a lot more optimization.

-  Python3.8+: Calls of C functions are faster and more compact code
   using vector calls, too.

-  Python3.10+: Mark our compiled types as immutable.

-  Python3.12: Constant returning functions are dealing with immortal
   values only. Makes their usage slightly faster since no reference
   count handling is needed.

-  Python3.10+: Faster attribute descriptor lookups. Have our own
   replacement of ``PyDesc_IsData`` that had become an API call, making
   it very slow on Windows specifically.

-  Avoid using Python API function for determining sequence sizes when
   getting a length size for list creations.

-  Data Composer: More compact and portable Python3 ``int`` (Python2
   ``long``) value representation.

   Rather than fixed native length 8 or 4 bytes, we use variable length
   encoding which for small values uses only a single byte.

   This also avoids using ``struct.pack`` with C types, as we might be
   doing cross platform, so this makes part of the WASI changes
   unnecessary at the same time.

   Large values are also more compact because middle 31-bit portions can
   be less than 4 bytes and save space on average.

-  Data Composer: Store bytecode blob size more efficient and portable,
   too.

-  Prepare having knowledge of ``__prepare__`` result to be dictionaries
   per compile time decisions.

-  Added more hard trust for the ``typing`` module.

   The ``typing.Text`` is a constant too. In debug mode, we now check
   all exports of ``typing`` for constant values. This will allow to
   find missing values sooner in the future.

   Added the other types to be known to exist. That should help
   scalability for types intensive code somewhat by removing error
   handling for them.

-  macOS: Should use static libpython with Anaconda as it works there
   too, and reduces issues with Python3.12 and extension module imports.

-  Standalone: Statically optimize by OS in ``sysconfig``.

   Consequently, standalone distributions can exclude OS-specific
   packages such as ``_aix_support`` and ``_osx_support``.

-  Avoid changing code names for complex call helpers

   The numbering of complex call helper as normally applied to all
   functions are, caused this issue. When part of the code is used from
   the bytecode cache, they never come to exist and the C code of
   modules using them then didn't match.

   This avoids an extra C re-compilation for some modules that were
   using renumbered function the second time around a compilation
   happens. Added in 2.3.10 already.

-  Avoid using C-API when creating ``__path__`` value.

-  Faster indentation of generated code.

Anti-Bloat
==========

-  Add new ``pydoc`` bloat mode to trigger warnings when using it.

-  Recognize usage of ``numpy.distutils`` as ``setuptools`` bloat for
   more direct reporting.

-  Avoid compiling large ``opcua`` modules that generate huge C files
   much like ``asyncua`` package. Added in 2.3.1 already.

-  Avoid ``shiboken2`` and ``shiboken6`` modules from ``matplotlib``
   package when the ``no-qt`` plugin is used. Added in 2.3.6 already.

-  Changes for not using ``pydoc`` and ``distutils`` in ``numpy``
   version 2. Added in 2.3.7 already.

-  Avoid ``numpy`` and ``packaging`` dependencies from ``PIL`` package.

-  Avoid using ``webbrowser`` module from ``pydoc``.

-  Avoid using ``unittest`` in ``keras`` package. Added in 2.3.1
   already.

-  Avoid ``distutils`` from ``_oxs_support`` (used by ``sysconfig``)
   module on macOS.

-  Avoid using ``pydoc`` for ``werkzeug`` package. Fixed in 2.3.10
   already.

-  Avoid using ``pydoc`` for ``site`` module. Fixed in 2.3.10 already.

-  Avoid ``pydoc`` from ``xmlrpc.server``. Fixed in 2.3.10 already.

-  Added ``no_docstrings`` support for numpy2 as well. Fixed in 2.3.10
   already.

-  Avoid ``pydoc`` in ``joblib.memory``.

-  Avoid ``setuptools`` in ``gsplat`` package.

-  Avoid ``dask`` and ``jax`` in ``scipy`` package.

-  Avoid using ``matplotlib`` for ``networkx`` package.

Organizational
==============

-  Python3.12: Added annotations of official support for **Nuitka** PyPI
   package and test runner options that were still missing. Fixed in
   2.3.1 already.

-  UI: Change runner scripts. The ``nuitka3`` is no more. Instead, we
   have ``nuitka2`` where it applies. Also, we now use CMD files rather
   than batch files.

-  UI: Check filenames for data files for illegal paths on the
   respective platforms. Some user errors with data file options become
   more apparent this way.

-  UI: Check spec paths more for illegal paths as well. Also do not
   accept system paths like ``{TEMP}`` and no path separator after it.

-  UI: Handle report writing interrupt with CTRL-C more gracefully. No
   need to present this this as a general problem, rather inform the
   user that he did it.

-  NoGIL: Warn if using a no-GIL Python version, as this mode is not yet
   officially supported by **Nuitka**.

-  Added badges to the ``README.rst`` of **Nuitka** to display package
   support and more. Added in 2.3.1 already.

-  UI: Use the retry decorator when removing directories in general. It
   will be more thorough with properly annotated retries on Windows. For
   the dist folder, mention the running program as a probable cause.

-  Quality: Check ``replacements`` and ``replacements_plain`` Nuitka
   package configuration values.

-  Quality: Catch backlashes in paths provided in Nuitka Package
   Configuration values for ``dest_path``, ``relative_path``, ``dirs``,
   ``raw_dirs`` and ``empty_dirs``.

-  Debugging: Disable pagination in ``gdb`` with the ``--debugger``
   option.

-  PGO: Warn if the PGO binary does not run successfully.

-  UI: The new console mode option is a Windows-specific option now,
   move it to that group.

-  UI: Detect "rye python" on macOS. Added in 2.3.8 already.

-  UI: Be forgiving about release candidates; Ubuntu shipped one in a
   LTS release. Changed in 2.3.8 already.

-  Debugging: Allow fine-grained debug control for immortal checks

   Can use ``--no-debug-immortal-assumptions`` to allow for corrupted
   immortal objects, which might be done by non-Nuitka code and then
   break the debug mode.

-  UI: Avoid leaking compile time Nuitka environment variables to the
   child processes.

   They were primarily visible with ``--run``, but we should avoid it
   for everything.

   For non-Windows, we now recognize if we are the exact re-execution
   and otherwise, reject them.

-  Watch: Delete the existing ``virtualenv`` in case of errors updating
   or upgrading it.

-  Watch: Keep track of Nuitka compiled program exit code in newly added
   result files, too.

-  Watch: Redo compilations in case of previous errors when executing
   the compile program.

-  Quality: Wasn't detecting files to ignore for PyLint on Windows
   properly, also detect crashes of PyLint.

Tests
=====

-  Added test to cover the ``dill-compat`` plugin.

-  macOS: Make actual use of ``ctypes`` in its standalone test to ensure
   correctness on that OS, too.

-  Make compile extension module test work on macOS, too.

-  Avoid using ``2to3`` in our tests since newer Python no longer
   contains it by default, we split up tests with mixed contents into
   two tests instead.

-  Python3.11+: Make large constants test executable for as well. We no
   longer can easily create those values on the fly and output them due
   to security enhancements.

-  Python3.3: Remove support from the test runner as well.

-  Tests: Added construct-based tests for coroutines so we can compare
   their performance as well.

Cleanups
========

-  Make try/finally variable releases through common code. It will allow
   us to apply special exception value trace handling for only those for
   scalability improvements, while also making many re-formulations
   simpler.

-  Avoid using ``anti-bloat`` configuration values ``replacements``
   where ``replacements_plain`` is good enough. A lot of config pre-date
   its addition.

-  Avoid Python3 and Python3.5+ specific Jinja2 modules on versions
   before that, and consequently, avoid warning about the
   ``SyntaxError`` given.

-  Moved code object extraction of ``dill-compat`` plugin from Python
   module template to C code helper for shared usage and better editing.

-  Also call ``va_end`` for standards compliance when using
   ``va_start``. Some C compilers may need that, so we better do it even
   if what we have seen so far doesn't need it.

-  Don't pass main filename to the tree building anymore, and make
   ``nuitka.Options`` functions usage explicit when importing.

-  Change comments that still mentioned Python 3.3 as where a change in
   Python happened since we no longer support this version. Now, we
   consider what's first seen in Python 3.4 is a Python3 change.

-  Cleanup, change Python 3.4 checks to 3.0 checks as Python3.3 is no
   longer supported. Cleans up version checks, as we now treat ``>=3.4``
   either as ``>=3`` or can drop checks entirely.

-  The usual flow of spelling cleanups, this time for C codes.

Summary
=======

This release cycle was a longer than usual, with much new optimization
and package support requiring attention.

For optimization we got quite a few things going, esp. with more forward
propagation, but the big ones for scalability are still all queued up
and things are only prepared.

The 3.13 work was continuing smoothly and seems to be doing fine. We are
still on track for supporting it right after release.

The parts where we try and address WASI prepare cross-compilation, but
we will not aim at it generally immediately, and target our own Nuitka
standalone backend Python that is supposed to be added in coming
releases.

********************
 Nuitka Release 2.3
********************

This release bumps the long-awaited 3.12 support to a complete level.
Now, Nuitka behaves identically to CPython 3.12 for the most part.

In terms of bug fixes, it's also huge. Especially for Unicode paths and
software with Unicode extension module names and Unicode program names,
and even non-UTF8 code names, there have been massive amounts of
improvements.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  Standalone: Added support for ``python-magic-bin`` package. Fixed in
   2.2.1 already.

-  Fix: The cache directory creation could fail when multiple
   compilations started simultaneously. Fixed in 2.2.1 already.

-  macOS: For ``arm64`` builds, DLLs can also have an architecture
   dependent suffix; check that as well. Makes the ``soundfile``
   dependency scan work. Fixed in 2.2.1 already.

-  Fix: Modules where lazy loaders handling adds hard imports when a
   module is first processed did not affect the current module,
   potentially causing it not to resolve hidden imports. Fixed in 2.2.1
   already.

-  macOS: The use of ``libomp`` in ``numba`` needs to cause the
   extension module not to be included and not to look elsewhere. Fixed
   in 2.2.1 already.

-  Python3.6+: Fix, added support for keyword arguments of
   ``ModuleNotFoundError``. Fixed in 2.2.1 already.

-  macOS: Detect more versioned DLLs and ``arm64`` specific filenames.
   Fixed in 2.2.1 already.

-  Fix, was not annotating exception exit when converting an import to a
   hard submodule import. Fixed in 2.2.2 already.

-  Fix, branches that became empty can still have traces that need to be
   merged.

   Otherwise, usages outside the branch will not see propagated
   assignment statements. As a result, these falsely became unassigned
   instead. Fixed in 2.2.2 already.

-  Windows: Fix, uninstalled self-compiled Python didn't have proper
   installation prefix added for DLL scan, resulting in runtime DLLs not
   picked up from there. Fixed in 2.2.2 already.

-  Standalone: Added support for newer ``PySide6`` version 6.7. It
   needed correction on macOS and has a new data file type. Fixed in
   2.2.3 already.

-  Standalone: Complete support for ``pyocd`` package. Fixed in 2.2.3
   already.

-  Module: Fix, the created ``.pyi`` files were incomplete.

   The list of imported modules created in the finalization step was
   incomplete, we now go over the actual done modules and mark all
   non-included modules as dependencies.

-  Scons: Fix, need to avoid using Unicode paths towards the linker on
   Windows. Instead, use a temporary output filename and rename it to
   the actual filename after Scons has completed.

-  Windows: Avoid passing Unicode paths to the dependency walker on
   Windows, as it cannot handle those. Also, the temporary filenames in
   the build folder must be in short paths, as it cannot handle them in
   case that is a Unicode path.

-  Scons: For ``ccache`` on Windows, the log filename must be a short
   path too, if the build folder is a Unicode path.

-  Windows: Make sure the Scons build executes inside a short path as
   well, so that a potential Unicode path is visible to the C compiler
   when resolving the current directory.

-  Windows: The encoding of Unicode paths for accelerated mode values of
   ``__file__`` was not making sure that hex sequences were correctly
   terminated, so in some cases, it produced ambiguous C literals.

-  Windows: Execute binaries created with ``--windows-uac-admin`` with
   and ``--run`` options with proper UAC prompt.

-  Fix, need to allow for non-UTF8 Unicode in variable names, function
   names, class names, and method names.

-  Python3.10+: Fix, ``match`` statements that captured the rest of
   mapping checks were not working yet.

   .. code:: python

      match value:
         case {"key1": 5, **rest}:
            ... # rest was not assigned here

-  Windows: When deleting build folders, make sure the retries leading
   to a complete deletion always.

-  Python2: Fix, could crash with non-``unicode`` program paths on
   Windows.

-  Avoid giving ``SyntaxWarning`` from reading source code

   For example, the standard ``site`` module of Python 3.12 gives
   warnings about illegal escape sequences that nobody cares about
   apparently.

-  Fix, the ``matplotlib`` warnings by ``options-nanny`` were still
   given even if the ``no-qt`` plugin was used, since the variable name
   referenced there was not actually set yet by that plugin.

-  Windows: Fix, when using the uninstalled self-compiled Python, we
   need ``python.exe`` to find DLL dependencies. Otherwise it doesn't
   locate the MSVC runtime and Python DLL properly.

-  Standalone: Added support for ``freetype`` package.

New Features
============

-  Support for Python 3.12 is finally there. We focused on scalability
   first and because we did things the correct way immediately, rather
   than rushing to get it working and improving only later.

   As a result, the correctness and performance of **Nuitka** with
   previous Python releases are improved as well.

   Some things got delayed, though. We need to do more work to take
   advantage of other core changes. Concerning exceptions normalized at
   creation time, the created module code doesn't yet take advantage.
   Also, more efficient two-digit long handling is possible with Python
   3.12, but not implemented. It will take more time before we have
   these changes completed.

-  Experimental support for Python 3.13 beta 1 is also there, and
   potentially surprising, but we will try and follow its release cycle
   closely and aim to support it at the time of release.

   **Nuitka** has followed all of its core changes so far, and basic
   tests are passing; the accelerated, module, standalone, and onefile
   modes all work as expected. The only thing delayed is the uncompiled
   generator integration, where we need to replicate the exact CPython
   behavior. We need to have perfect integration only for working with
   the ``asyncio`` loop, so we wait with it until release candidates
   appear.

-  Plugins: Added support to include directories entirely unchanged by
   adding ``raw_dir`` values for ``data-files`` section, see
   :doc:`Nuitka Package Configuration
   </user-documentation/nuitka-package-config>`.

-  UI: The new command line option ``--include-raw-dir`` was added to
   allow including directories entirely unchanged.

-  Module: Added support for creating modules with Unicode names. Needs
   a different DLL entry function name and to make use of two-phase
   initialization for the created extension module.

-  Added support for OpenBSD standalone mode.

Optimization
============

-  Python3: Avoid API calls for allocators

   Most effective with Python 3.11 or higher but also many other types
   like ``bytes``, ``dict`` keys, ``float``, and ``list`` objects are
   faster to create with all Python3 versions.

-  Python3.5+: Directly use the **Python** allocator functions for
   object creation, avoiding the DLL API calls. The coverage is complete
   with Python3.11 or higher, but many object types like ``float``,
   ``dict``, ``list``, ``bytes`` benefit even before that version.

-  Python3: Faster creation of ``StopIteration`` objects.

   With Python 3.12, the object is created directly and set as the
   current exception without normalization checks.

   We also added a new specialized function to create the exception
   object and populate it directly, avoiding the overhead of calling of
   the ``StopIteration`` type.

-  Python3.10+: When accessing freelists, we were not passing for
   ``tstate`` but locally getting the interpreter object, which can be
   slower by a few percent in some configurations. We now use the free
   lists more efficient with ``tuple``, ``list``, and ``dict`` objects.

-  Python3.8+: Call uncompiled functions via vector calls.

   We avoid an API call that ends up being slower than using the same
   function via the vector call directly.

-  Python3.4+: Avoid using ``_PyObject_LengthHint`` API calls in
   ``list.extend`` and have our variant that is faster to call.

-  Added specialization for ``os.path.normpath``. We might benefit from
   compile time analysis of it once we want to detect file accesses.

-  Avoid using module constants accessor for global constant values

   For example, with ``()``, we used the module-level accessor for no
   reason, as it is already available as a global value. As a result,
   constant blobs shrink, and the compiled code becomes slightly smaller
   , too.

-  Anti-Bloat: Avoid using ``dask`` from the ``sparse`` module. Added in
   2.2.2 already.

Organizational
==============

-  UI: Major change in console handling.

   Compiled programs on Windows now have a third mode, besides console
   or not. You can now create GUI applications that attach to an
   available console and output there.

   The new option ``--console`` controls this and allows to enforce
   console with the ``force`` value and disable using it with the
   ``disable`` value, the ``attach`` value activates the new behavior.

   .. note::

      Redirection of outputs to a file in ``attach`` mode only works if
      it is launched correctly, for example, interactively in a shell,
      but some forms of invocation will not work; prominently,
      ``subprocess.call`` without inheritable outputs will still output
      to a terminal.

   On macOS, the distinction doesn't exist anymore; technically it
   wasn't valid for a while already; you need to use bundles for
   non-console applications, though, by default otherwise a console is
   forced by macOS itself.

-  Detect ``patchelf`` usage in buggy version ``0.18.0`` and ask the
   user to upgrade or downgrade it, as this specific version is known to
   be broken.

-  UI: Make clear that the ``--nofollow-import-to`` option accepts
   patters.

-  UI: Added warning for module mode and usage of the options to force
   outputs as they don't have any effect.

-  UI: Check the success of Scons in creating the expected binary
   immediately after running it and not only once we reach
   post-processing.

-  UI: Detect empty user package configuration files

-  UI: Do not output module ``ast`` when a plugin reports an error for
   the module, for example, a forbidden import.

-  Actions: Update from deprecated action versions to the latest
   versions.

Tests
=====

-  Use :ref:`Nuitka Project Options <nuitka-project-options>` for the
   user plugin test rather than passing by environment variables to the
   test runner.

-  Added a new search mode, ``skip, `` to complement ``resume`` which resumes right
      after the last test ``resume`` stopped on. We can use that while
      support for a Python version is not complete.

Cleanups
========

-  Solved a TODO about using unified code for setting the
   ``StopIteration``, coroutines, generators, and asyncgen used to be
   different.

-  Unified how the binary result filename is passed to Scons for modules
   and executables to use the same ``result_exe`` key.

Summary
=======

This release marks a huge step in catching up with compatibility of
Python. After being late with 3.12 support, we will now be early with
3.13 support if all goes well.

The many Unicode support related changes also enhanced Nuitka to
generate 2 phase loading extension modules, which also will be needed
for sub-interpreter support later on.

From here on, we need to re-visit compatibility. A few more obscured
3.10 features are missing, the 3.11 compatibility is not yet complete,
and we need to take advantage of the new caching possibilities to
enhance performance for example with attribute lookups to where it can
be with the core changes there.

For the coming releases until 3.13 is released, we hope to focus on
scalability a lot more and get a much needed big improvement there, and
complete these other tasks on the side.

********************
 Nuitka Release 2.2
********************

This release focused on compatibility and significant optimization
progress for loops, such as list operations within. The main line of
change is to be able to support Python 3.12 in the next release.

Bug Fixes
=========

-  Standalone: Added support for ``pypdfium2`` package. Fixed in 2.1.1
   already.

-  Standalone: Make ``cefpython3`` work on Linux. Fixed in 2.1.1
   already.

-  ArchLinux: Added platform linker option to be usable with their
   current Arch Python package. Fixed in 2.1.1 already.

-  Fix, ``ctypes.CDLL`` optimization used a misspelled argument name for
   ``use_last_error``, such that keyword argument calls were statically
   optimized into ``TypeError`` at compile-time. Fixed in 2.1.1 already.

-  Fix, ``list.insert`` was not properly annotating exceptions. Raises
   by producing the inserted value raised or the index was not annotated
   and, therefore, could fail to be caught locally. Fixed in 2.1.1
   already.

-  Standalone: Added support for ``selenium`` package. Fixed in 2.1.2
   already.

-  Standalone: Added support for ``hydra`` package. Fixed in 2.1.2
   already.

-  Standalone: Updated ``dotenv`` workaround for newer version. Fixed in
   2.1.3 already.

-  Fix, **PySide6** slots failed to be moved between threads. For that
   we need to make function renames visible in the owning class as well.
   Fixed in 2.1.3 already.

-  Standalone: Added support for ``win32com.server.register``. Fixed in
   2.1.3 already.

-  Standalone: Handle "string" import errors of ``uvicorn`` gracefully.
   Fixed in 2.1.3 already.

-  Fix, the ``dill-compat`` plugin needs also needs to expose the
   compiled type names as built-ins for the ``pickle`` module to find
   them.

-  Standalone: Added support for ``gruut`` package. Fixed in 2.1.3
   already.

-  Standalone: Added support for newer ``toga`` to also include
   ``toga_winforms`` metadata. Fixed in 2.1.3 already.

-  Standalone: Added support for newer ``tensorflow`` package. Fixed in
   2.1.4 already.

-  Standalone: Fix, ``matplotlib`` needs to emit a dependency on the
   backend to be included. Otherwise it could be missing at run-time in
   some cases. Fixed in 2.1.4 already.

-  Onefile: Respect ``XDG_CACHE_HOME`` variable on non-Windows
   platforms. Some users might configure that to not to be ``~/.cache``,
   respect that. Fixed in 2.1.4 already.

-  Python2: Some cases of ``list.insert`` were not properly handling all
   index types. Fixed in 2.1.4 already.

-  Fix, optimized ``list.remove`` failed to handle tuple arguments
   properly. Removing tuple values from lists could cause errors. Fixed
   in 2.1.4 already.

-  Standalone: Added missing implicit dependencies for
   ``pyarrow.datasets``. Fixed in 2.1.4 already.

-  Standalone: Added support for ``dask.dataframe`` module. Fixed in
   2.1.4 already.

-  Standalone: Added DLLs for ``tensorrt_libs`` package. Fixed in 2.1.4
   already.

-  Standalone: Added missing metadata of ``numpy`` for ``xarray``
   package. Fixed in 2.1.4 already.

-  Standalone: Added support for newer ``scipy``. Fixed in 2.1.5
   already.

-  Standalone: Fix, older ``gcc`` could give warning about C code to
   work with ``PYTHONPATH`` which caused build errors on older systems.
   Fixed in 2.1.5 already.

-  Fix, ``locals`` representing nodes could not be cloned, and as a
   result, some code re-formulations failed to compile in ``try``
   constructs. Fixed in 2.1.5 already.

-  Standalone: Added data files for ``names`` package. Fixed in 2.1.5
   already.

-  Standalone: Added data files for ``randomname`` package. Fixed in
   2.1.5 already.

-  Standalone: Fix, the standalone standard library scan was not fully
   ignoring git folders, subfolders were still looked at and could cause
   issues. Fixed in 2.1.5 already.

-  Standalone: Added support for newer ``transformers``. Fixed in 2.1.5
   already.

-  Standalone: Add support for newer ``bitsandbytes``. Fixed in 2.1.5
   already.

-  Scons: Fix, when locating binaries, do not use directories but only
   files.

   A directory on ``PATH`` that was named ``gcc`` could be mistaken to
   be a ``gcc`` binary causing errors. Fixed in 2.1.6 already.

-  Windows: Fix, by default, scan only for ``.bin`` and ``.exe``
   binaries for Nuitka Package Configuration EXE dependency patterns.
   This was the intended value, but it had not taken effect yet. Fixed
   in 2.1.6 already.

-  Fix, the ``__compiled__.containing_dir`` should be an absolute path.
   For it to be usable after a change of directory is done by the
   program that is required. Fixed in 2.1.6 already.

-  Standalone: Added support for more parts of ``networkx`` package.
   Fixed in 2.1.6 already.

-  Windows: Fix working with UNC paths and re-parse points at compile
   time.

   Now Nuitka should work with mapped and even unmapped to drive paths
   like ``\\some-hostname\unc-test`` as they are common in some VM
   setups.

-  Windows: Make sure the download path is an external use path in scons
   as well, otherwise the home directory could be an unusable path for
   MinGW64, causing it not to find files.

-  Standalone: Added missing dependency of ``sspilib`` that prevented
   ``requests-ntlm`` from working on Windows.

-  Python3.5+: Add support for using dictionary un-packings in class
   declarations. That is a rarely used in actual Python code, but was
   found missing by tests recently.

-  Python3.11: Fix, code objects ``co_qualname`` attribute was not
   actually the qualified name, but the same as ``co_name`` only.

-  Anaconda: Fix, must not consider the Anaconda ``lib`` directory as a
   system directory, because then those DLLs that are not included.

-  Fix, cannot trust dynamic hard modules as much otherwise,
   ``huggingface_hub.utils.tqdm`` ended up being a module and not the
   class it's supposed to be.

-  macOS: Fix, on newer macOS the ``libc++`` and ``libz`` DLLs cannot be
   found anymore, we need to ignore that actively as our code insists on
   full resolution to catch bugs.

-  Fix, support for newer ``zaber_motion`` was not really working.

-  Standalone: Added required data files for ``pyviz_comms``.

-  Standalone: Added required data files for ``panel`` package.

-  Standalone: Added required data files for ``bokeh`` package.

-  Standalone: Fixup ``scipy`` for Anaconda.

-  Fix, need to make parent module usages more explicit.

   Otherwise, plugin mechanisms like ``no-follow`` from a parent module
   cannot affect its child modules, as they can end up being followed to
   only after them.

-  Fix, the ``dill-compat`` plugin in module mode cannot assume the main
   module name to be the one from compile time, need to look the actual
   one up at runtime.

New Features
============

-  Added experimental support for Python 3.12, this is passing basic
   tests, but known to crash a lot at run-time still, you are
   recommended to use pre-releases of Nuitka, as official support is not
   going to happen before 2.3 release.

-  Standalone: Added support for ``tensorflow.function`` JIT

   With preserved source code of decorated functions and we can provide
   it at run-time to ``tensorflow`` JIT so it can do its tracing
   executions.

-  For Nuitka Package Configuration, we now have ``change_class``
   similar to ``change_function`` to replace a full class definition
   with something else, this can be used to modify classes to become
   stubs or even unusable.

-  For the experimental ``@pyqtSlot`` decorator, we also should handle
   the ``@asyncSlot`` the same way. Added in 2.1.1 already.

-  Added new kind of warning of ``plugin`` category and use it in the
   Nuitka Package Configuration to inform ``matplotlib`` users to select
   a GUI backend via plugin selection. Added in 2.1.4 already.

-  Zig: Added support for ``zig`` as CC value. Due to it not supporting
   C11 fully yet, we need to use the C++ workaround and cannot compile
   for Python 3.11 or higher yet.

-  For the ``__compiled__`` value, we now have a ``__compiled__.main``
   that is the name of the compiled module. For modules, **Nuitka**
   determines this at run time; in other modes, it is the name of the
   main module.

Optimization
============

-  Use ``set`` specific API in contains tests, rather than generic
   sequence one.

-  Lower ``value in something`` tests for known ``set`` and ``list``
   values to use ``frozenset`` and ``tuple`` respectively.

-  Recognize exact type shapes of loop variables where possible. This
   enables appends to list to be optimized to their dedicated nodes
   among other things, with those often being a lot faster than generic
   code. This speeds up e.g. list ``append`` tests by a significant
   amount.

-  Optimization: Have dedicated helper for ``list.remove``, such that it
   is not using a Python DLL call where that is slow.

-  ArchLinux: Enable static libpython by default, it is usable indeed.
   Added in 2.1.2 already.

-  Anti-Bloat: Avoid ``unittest`` usage in ``antlr`` package.

-  Anti-Bloat: Avoid ``IPython`` in ``celery`` package. Added in 2.1.2
   already.

-  Anti-Bloat: Avoid using ``setuptools`` in ``transformers`` package
   for more modules. Added in 2.1.3 already.

-  Anti-Bloat: Avoid testing packages for newer ``tensorflow`` package
   as well. Added in 2.1.4 already.

-  Optimization: Avoid recompiling ``azure`` package which is not
   performance relevant. Added in 2.1.4 already.

-  Avoid packages owned by Nuitka plugins in ``matploblib`` backends
   unless the corresponding plugin is actually active. Added in 2.1.4
   already.

-  Anti-Bloat: Avoid ``setuptools`` in ``deepspeed`` package. Added in
   2.1.4 already.

-  Anti-Bloat: Avoid ``setuptools`` in ``transformers`` package. Added
   in 2.1.4 already.

-  Anti-Bloat: Avoid ``scipy`` usage causing ``torch`` or ``cupy``
   usage. Added in 2.1.4 already.

-  Anti-Bloat: Recognize ``keras`` testing modules as ``unittest``
   bloat.

-  Faster code generation due to enhancements in how identifiers are
   cached for module names and the indentation codes.

-  Optimization: Handle ``no_docstrings`` issue for ``torio`` package.

-  Anti-Bloat: Avoid ``IPython`` from ``imgui_bundle`` package.

-  Anti-Bloat: Remove testing module usage when ``dask`` is used.

-  Anti-Bloat: Avoid ``unitest`` usage in ``tf_keras`` package as well.

-  Anti-Bloat: Avoid ``IPython`` from ``bokeh`` package.

Organizational
==============

-  UI: Catch conflicts between data files and EXE/DLLs/extension module
   filenames. Previously, you could overwrite binaries with data files,
   but that is now rejected as an explicit error.

-  Onefile: Avoid using the program name without suffix inside the dist
   folder, as that avoids collisions with data file directories of the
   same name, e.g., if the package and main binary have the same name,
   they would clash previously, but adding a ``.bin`` suffix to the
   binary avoids that entirely.

-  UI: Don't force ``{VERSION}`` in specs to be resolved to four digits.

   That made it hard for users, who will be surprised to see ``1.0``
   become ``1.0.0.0`` when that is only needed for Windows version
   information really.

-  UI: Catch wrong values for ``--jobs`` value sooner, negative and
   non-integer values error exit immediately. Added in 2.1.1 already.

-  UI: Nicer usage name when invoked with ``python -m nuitka``

   The recommended form of invocation of Nuitka should not have an ugly
   invocation reference mentioning ``__main__.py`` instead put the
   ``python -m nuitka`` notion there.

-  UI: Reorder options for the plugins group to be more readable.

-  Plugins: Remove obsolete plugins from standard plugin documentation.
   Removed in 2.1.4 already.

-  UI: The Windows release was coming from the compiling **Python** and
   as such wrong, for example, **Windows 11** always showed up as
   **Windows 10**, and some older versions of **Python** didn't know
   Windows 10, yet, so this could be confusing in issue analysis.

-  UI: Do not warn about static libpython for Python debug mode
   compilation. It is misleading as often it doesn't work for that
   configuration, and it's only a distraction since debugging Python
   reference counts is not about performance. Changed in 2.1.4 already.

-  UI: Catch newlines in spec values. They break code C code generation
   potentially; they also are likely copy&paste mistakes that won't do
   what the user expects. Added in 2.1.4 already.

-  Quality: Updated to the latest version of black.

-  Quality: Fix, ``isort`` and ``black`` can corrupt outputs, catch
   that.

-  Debugging: Generate Scons debug script

   It can serve to quickly re-execute a Scons compilation without
   re-executing Nuitka again. This is best used where there is no Python
   level change but only C changes and no expectation of producing a
   usable result.

   Because no post-processing is applied, and as a consequence this is
   not usable to produce binaries that work. In the future, we might
   expand this to be able to run post-processing still.

-  Debugging: Disabling all freelists is now honored for more code,
   tuples and empty dictionaries as well.

-  UI: Add macOS version to help output, which is sometimes vital for
   issue analysis.

-  Reports: Add the OS release to reports as well.

-  Reports: Exclude parent path imports from compilation reports for
   module usages that are found and end up not being excluded.

-  Watch: Reporting more problems, catching more errors, and adding the
   ability to create PRs from changes. However, it does not yet do it
   automatically.

-  Visual Code: Have plugins C files in the include path as well.

Tests
=====

-  Tests: Fix, cannot assume ``setuptools`` to be installed, some RPM
   based systems don't have it.

-  Run commercial code signing test only on Windows.

-  Allow for standalone testing file access to the Azure agent folders.
   For tests on Azure, it's like the home directory.

-  Make sure optimization tests are named to make it clear that they are
   tests.

Cleanups
========

-  Remove useless ``--execute-with-pythonpath`` option, we don't use
   that anymore at all.

Summary
=======

The JIT mechanism added for ``tensorflow`` should be possible to
generalize and will be applied to other JITs, like ``numba`` and others
in the future as well.

The road to Python 3.12 is not fully complete, but the end feels closer
now, and the subsequent release hopefully will add the official support
for it.

********************
 Nuitka Release 2.1
********************

This release had focus on new features and new optimization. There is a
also a large amount of compatibility with things newly added to support
anti-bloat better, and workaround problems with newer package versions
that would otherwise need source code at run-time.

Bug Fixes
=========

-  Windows: Using older MSVC before 14.3 was not working anymore. Fixed
   in 2.0.1 already.

-  Compatibility: The ``dill-compat`` plugin didn't work for functions
   with closure variables taken. Fixed in 2.0.1 already.

   .. code:: python

      def get_local_closure(b):
        def _local_multiply(x, y):
          return x * y + b
        return _local_multiply

      fn = get_local_closure(1)
      fn2 = dill.loads(dill.dumps(fn))
      print(fn2(2, 3))

-  Windows: Fix, sometimes ``kernel32.dll`` is actually reported as a
   dependency, remove assertion against that. Fixed in 2.0.1 already.

-  UI: The help output for ``--output-filename`` was not formatted
   properly. Fixed in 2.0.1 already.

-  Standalone: Added support for the ``scapy`` package. Fixed in 2.0.2
   already.

-  Standalone: Added ``PonyORM`` implicit dependencies. Fixed in 2.0.2
   already.

-  Standalone: Added support for ``cryptoauthlib``, ``betterproto``,
   ``tracerite``, ``sklearn.util``, and ``qt_material`` packages. Fixed
   in 2.0.2 already.

-  Standalone: Added missing data file for ``scipy`` package. Fixed in
   2.0.2 already.

-  Standalone: Added missing DLLs for ``speech_recognition`` package.
   Fixed in 2.0.2 already.

-  Standalone: Added missing DLL for ``gmsh`` package. Fixed in 2.0.2
   already.

-  UI: Using reporting path in macOS dependency scan error message,
   otherwise these contain home directory paths for no good reason.
   Fixed in 2.0.2 already.

-  UI: Fix, could crash when compiling directories with trailing slashes
   used. At least on Windows, this happened for the "/" slash value.
   Fixed in 2.0.2 already.

-  Module: Fix, convenience option ``--run`` was not considering
   ``--output-dir`` directory to load the result module. Without this,
   the check for un-replaced module was always triggering for module
   source in current directory, despite doing the right thing and
   putting it elsewhere. Fixed in 2.0.2 already.

-  Python2: Avoid values for ``__file__`` of modules that are unicode
   and solve a TODO that restores consistency over modules mode
   ``__file__`` values. Fixed in 2.0.2 already.

-  Windows: Fix, short paths with and without dir name cached wrongly,
   which could lead to shorted paths even where not asked for them.
   Fixed in 2.0.2 already.

-  Fix, comparing list values that changed could segfault. This is a bug
   fix Python did, that we didn't follow yet and that became apparent
   after using our dedicated list helpers more often. Fixed in 2.0.2
   already.

-  Standalone: Added support for ``tiktoken`` package. Fixed in 2.0.2
   already.

-  Standalone: Fix, namespace packages had wrong runtime ``__path__``
   value. Fixed in 2.0.2 already.

-  Python3.11: Fix, was using tuples from freelist of the wrong size

   -  CPython changed the index for the size, to not use zero, which was
      wasteful when introduced with 3.10, but to ``size-1`` but we did
      not follow that and then used a tuple one bit larger than
      necessary.

   -  As a result, code producing a lot short living tuples could end up
      creating new ones over and over, causing bad memory allocations
      and slow performance.

   Fixed in 2.0.2 already.

-  macOS: Fix, need to allow non-existent and versioned dependencies of
   DLLs to themselves. Fixed in 2.0.2 already.

-  Windows: Fix PGO (Profile Guided Optimization) build errors with
   MinGW64, this feature is not yet ready for general use, but these
   errors shouldn't happen. Fixed in 2.0.2 already.

-  Plugins: Fix, do not load ``importlib_metadata`` unless really
   necessary.

   The ``pkg_resources`` plugin used to load it, and that then had
   harmful effects for our handling of distribution information in some
   configurations. Fixed in 2.0.3 already.

-  Plugins: Avoid warnings from plugin evaluated code, it could happen
   that a ``UserWarning`` would be displayed during compilation. Fixed
   in 2.0.3 already.

-  Fix, loading pickles with compiled functions in module mode was not
   working. Fixed in 2.0.3 already.

-  Standalone: Added data files for ``h2o`` package. Fixed in 2.0.3
   already.

-  Fix, variable assignment from variables that started to raise were
   not recognized.

   When a variable assignment from a variable became a raise expression,
   that wasn't caught and propagated as it should have been. Fixed in
   2.0.3 already.

-  Make the ``NUITKA_PYTHONPATH`` usage more robust. Fixed in 2.0.3
   already.

-  Fix, PySide2/6 argument name for slot connection and disconnect
   should be ``slot``, wasn't working with keyword argument calls. Fixed
   in 2.0.3 already.

-  Standalone: Added support for ``paddle`` and ``paddleocr`` packages.
   Fixed in 2.0.4 already.

-  Standalone: Added support for ``diatheke``. Fixed in 2.0.4 already.

-  Standalone: Added support for ``zaber-motion`` package. Fixed in
   2.0.4 already.

-  Standalone: Added support for ``plyer`` package. Fixed in 2.0.4
   already.

-  Fix, added handling of ``OSError`` for metadata read, otherwise
   corrupt packages can have Nuitka crashing. Fixed in 2.0.4 already.

-  Fix, need to annotate potential exception exit when making a fixed
   import from hard module attribute. Fixed in 2.0.4 already.

-  Fix, didn't consider Nuitka project options with ``--main`` and
   ``--script-path``. This is of course the only way Nuitka-Action does
   call it, so they didn't work there at all. Fixed in 2.0.4 already.

-  Scons: Fix, need to close progress bar when about to error exit.
   Otherwise error outputs will be garbled by incomplete progress bar.
   Fixed in 2.0.4 already.

-  Fix, need to convert relative from imports to hard imports too, or
   else packages needed to be followed are not included. Fixed in 2.0.5
   already.

-  Standalone: Added ``pygame_menu`` data files. Fixed in 2.0.6 already.

-  Windows: Fix, wasn't working when compiling on network mounted drive
   letters. Fixed in 2.0.6 already.

-  Fix, the ``.pyi`` parser was crashing on some comments with a leading
   ``from`` in the line, recognize these better. Fixed in 2.0.6 already.

-  Actions: Fix, some yaml configs could fail to load plugins. Fixed in
   2.0.6 already.

-  Standalone: Added support for newer ``torch`` packages that otherwise
   require source code.

-  Fix, inline copies of ``tqdm`` etc. left sub-modules behind, removing
   only the top level ``sys.modules`` entry may not be enough.

New Features
============

-  Plugins: Added support for ``constants`` in Nuitka package
   configurations. We can now using ``when`` clauses, define variable
   values to be defined, e.g. to specify the DLL suffix, or the DLL
   path, based on platform dependent properties.

-  Plugins: Make ``relative_path``, ``suffix``, ``prefix`` in DLL Nuitka
   package configurations allowed to be an expression rather than just a
   constant value.

-  Plugins: Make not only booleans related to the python version
   available, but also strings ``python_version_str`` and
   ``python_version_full_str``, to use them when constructing e.g. DLL
   paths in Nuitka Package Configuration.

-  Plugins: Added helper function ``iterate_modules`` for producing the
   submodules of a given package, for using in expressions of Nuitka
   package configuration.

-  macOS: Added support for Tcl/Tk detection on Homebrew Python.

-  Added ``module`` attribute to ``__compiled__`` values

   So far it was impossible to distinguish non-standalone, i.e.
   accelerated mode and module compilation by looking at the
   ``__compiled__`` attribute, so we add an indicator for module mode
   that closes this gap.

-  Plugins: Added ``appdirs`` and ``importlib`` for use in Nuitka
   package config expressions.

-  Plugins: Added ability to specify modules to not follow when a module
   is used. This ``nofollow`` configuration is for rare use cases only.

-  Plugins: Added values ``extension_std_suffix`` and
   ``extension_suffix`` for use in expressions, to e.g. construct DLL
   suffix patterns from it.

-  UI: Added more control over caching with per cache category
   environment variables, as `documented in the User Manual.
   <https://nuitka.net/doc/user-manual.html#control-where-caches-live>`_.

-  Plugins: Added support for reporting module detections

   The ``delvewheel`` plugin now puts the version of that packaging tool
   used by a particular module in the report rather than tracing it to
   the user, that in the normal case won't care. This is more for
   debugging purposes of Nuitka.

Optimization
============

-  Scalability: Do not make loop analysis at all for very trusted value
   traces, their point is to not change, and waiting for that to be
   confirmed has no point.

-  Use very trusted value traces in functions not just as mere assign
   traces or else expected optimization will not be done on them in many
   cases. With this a lot more cases of hard values are optimized
   leading also to generally more compact and correct results in terms
   of imports, metadata, code avoided on the wrong OS, etc.

-  Scalability: When specializing assignments, make sure to have the
   proper value trace immediately.

   When changing to a hard value, the value trace was still an assign
   trace and not very trusted for one for micro pass of the module.

   This had the effect to need one more micro pass to get to benefiting
   of the unescapable nature of those values, which meant more micro
   passes than necessary and those being more complex due to escaped
   traces, and therefore taking longer for affected modules.

-  Scalability: The code trying avoid merge traces of merge traces, and
   to instead flatten merge traces was only handling part of these
   correctly, and correcting it reduced optimization time for some
   functions from infinite to instant. Less memory usage should also
   come out of this, even where this was not affecting compile time as
   much. Added in 2.0.1 already.

-  Scalability: Some codes that checked for variables were testing for
   temporary variable and normal variable both one after another, making
   some optimization steps and code generation slower than necessary due
   to the extra calls.

-  Scalability: A variable assignment from variable that were later
   recognized to become a raise was not recognized as such, and this
   then wasn't caught and propagated as it should, preventing more
   optimization of the affected code. Make sure to convert more directly
   when observing things to change, rather than doing it one pass later.

-  The fix proper reuse of tuples released to the freelist with matching
   sizes causes less memory usage and faster performance for the 3.11
   version. Added in 2.0.2 already.

-  Statically optimize ``sys.exit`` into exception raise of
   ``SystemExit``.

   This should make a bunch of dead code obvious to Nuitka, it can now
   tell this aborts execution of a branch, potentially eliminating
   imports, etc.

-  macOS: Enable python static link library for Homebrew too. Added in
   2.0.1 already. Added in 2.0.3 already.

-  Avoid compiling bloated module namespace of ``altair`` package. Added
   in 2.0.3 already.

-  Anti-Bloat: Avoid including ``kubernetes`` for ``tensorflow`` unless
   used otherwise. Added in 2.0.3 already.

-  Anti-Bloat: Avoid including setuptools for ``tqdm``. Added in 2.0.3
   already.

-  Anti-Bloat: Avoid ``IPython`` in ``fire`` package. Added in 2.0.3
   already.

-  Anti-Bloat: Avoid including ``Cython`` for ``pydantic`` package.
   Added in 2.0.3 already.

-  Anti-Bloat: Changes to avoid ``triton`` in newer ``torch`` as well.
   Added in 2.0.5 already.

-  Anti-Bloat: Avoid ``setuptools`` via ``setuptools_scm`` in
   ``pyarrow``.

-  Anti-Bloat: Made more packages equivalent to using ``setuptools``
   which we want to avoid, all of ``Cython``, ``cython``, ``pyximport``,
   ``paddle.utils.cpp_extension``, ``torch.utils.cpp_extension`` were
   added for better reports of the actual causes.

Organizational
==============

-  Moved the changelog of Nuitka to the website, just point to there
   from Nuitka repo.

-  UI: Proper error message from Nuitka when scons build fails with a
   detail mnemonic page. Read more on :doc:`the info page
   </info/scons-backend-failure>` for detailed information.

-  Windows: Reject all MinGW64 that are not are not the ``winlibs`` that
   Nuitka itself downloaded. As these packages break very easily, we
   need to control if it's a working set of ``ccache``, ``make``,
   ``binutils`` and gcc with all the necessary workarounds and features
   like ``LTO`` working on Windows properly.

-  Quality: Added auto-format of PNG and JPEG images. This aims at
   making it simpler to add images to our repositories, esp. Nuitka
   Website. This now makes ``optipng`` and ``jpegoptim`` calls as
   necessary. Previously this was manual steps for the website to be
   applied.

-  User Manual: Be more clear about compiler version needs on Windows
   for Python 3.11.

-  User Manual: Added examples for error message with low C compiler
   memory, such that maybe they can be found via search by users.

-  User Manual: Removed sections that are unnecessary or better
   maintained as separate pages on the website.

-  Quality: Avoid empty ``no-auto-follow`` values, for silently ignoring
   it there is a dedicated string ``ignore`` that must be used.

-  Quality: Enforce normalized paths for ``dest_path`` and
   ``relative_path``. Users were uncertain if a leading dot made sense,
   but we now disallow it for clarity.

-  Quality: Check more keys with expressions for syntax errors, to catch
   these mistakes in configuration sooner.

-  Quality: Scanning through all files with the auto-format tool should
   now be faster, and CPython test suite directories (test submodules)
   if present are ignored.

-  Release: Remove month from manpage generation, that's only noise in
   diffs.

-  Removed digital art folders, these were only making checkouts larger
   for no good reason. We will have better ones on the website in the
   future.

-  Scons: Allow C warnings when compiling for running in debugger
   automatically.

-  UI: The macOS app bundle option is not experimental at all. This has
   been untrue for years now, remove that cautioning.

-  macOS: Discontinue support for PyQt6.

   With newer PyQt6 we would have to package frameworks properly, and we
   don't have that yet and it will be a lot of developer time to get it.

   Instead point people to PySide6 which is the better choice and is
   perfectly supported by Qt company and Nuitka.

-  Removed version numbering, month of creation, etc. from the man pages
   generated.

-  Moved ``Credits.rst`` file to be on the website and maintain it there
   rather than syncing of from the Nuitka repository.

-  Bumped copyright year and split the license text such that it is now
   at the bottom of the files rather than eating up the first page, this
   is aimed at making the code more readable.

Cleanups
========

-  With ``sys.exit`` being optimized, we were able to make our trick to
   avoid following ``nuitka`` because of accidentally finding the
   ``setup`` as an import more simple.

   .. code:: python

      # Don't allow importing this, and make recognizable that
      # the above imports are not to follow. Sometimes code imports
      # setup and then Nuitka ends up including itself.
      if __name__ != "__main__":
         sys.exit("Cannot import 'setup' module of Nuitka")

-  Scons: Don't scan for ``ccache`` on Windows, the ``winlibs`` package
   contains it nowadays, and since it's now required to be used, there
   is no point for this code anymore.

-  Minor cleanups coming from trying out ``ruff`` as a linter on Nuitka,
   it found a few uses of not using ``not in``, but that was it.

Tests
=====

-  Removed test with chinese filenames, we need to avoid chinese names
   in the repo. These have been seen as preventing installation on some
   systems that are not capable of handling them in the git, zip, pip
   tooling, so lets avoid them entirely now that Nuitka handles these
   just fine.

-  Tests: More macOS standalone tests that need to be bundles were
   getting the project configuration to do it.

Summary
=======

This release added much needed tools for our Nuitka Package
configuration, but also cleans up scalability and optimization that was
supposed to work, but did not yet, or not anymore.

The usability improved again, as it does always, but the big
improvements for scalability that will implement existing algorithms
more efficient, are yet to come, this release was mainly driven by the
need to get ``torch`` to work in its latest version out of the box with
stable Nuitka, but this couldn't be done as a hotfix

********************
 Nuitka Release 2.0
********************

This release had focus on new features and new optimization. There is a
really large amount of compatibility with things newly added, but also
massive amounts of new features, and esp. for macOS and Windows, lot of
platform specified new abilities and corrections.

Bug Fixes
=========

-  Fix, workaround for private functions as Qt slots not having names
   mangled. Fixed in 1.9.1 already.

-  Fix, when using Nuitka with ``pdm`` it was not detected as using pip
   packages. Fixed in 1.9.1 already.

-  Fix, for ``pydantic`` our lazy loader parser didn't handle all cases
   properly yet. Fixed in 1.9.1 already.

-  Standalone: Added data files for ``pyocd`` package. Fixed in 1.9.1
   already.

-  Standalone: Added DLL for ``cmsis_pack_manager`` package. Fixed in
   1.9.1 already.

-  Standalone: Fix, the specs expanded at run time in some causes could
   contain random characters. Fixed in 1.9.2 already.

-  Fix, ``{"a":b, ...}.get("b")`` could crash at runtime. Fixed in 1.9.2
   already.

-  Standalone: Added data files for ``pyproj`` package. Fixed in 1.9.2
   already.

-  Standalone: Added more metadata requirements for ``transformers``
   package. Fixed in 1.9.2 already.

-  Plugins: Fix, could crash when including packages from the command
   line, if they had yaml configuration that requires checking the using
   module, e.g. anti-bloat work. Fixed in 1.9.3 already.

-  Standalone: Added support for ``delphifmx`` package. Fixed in 1.9.4
   already.

-  Android: Fix, cannot exclude ``libz`` on that platform, it's not a
   full Linux OS. Fixed in 1.9.3 already.

-  Standalone: Add needed DLLs for ``bitsandbytes`` package. Fixed in
   1.9.3 already.

-  Windows: Fix, newer ``joblib`` was not working anymore. Fixed in
   1.9.3 already.

-  Windows: Fix, could crash when working with junctions that switch
   drives. Fixed in 1.9.3 already.

-  Fix, was crashing with poetry installed environments. Fixed in 1.9.3
   already.

-  Standalone: Added support for newer ``chromadb`` package. Fixed in
   1.9.3 already.

-  Fix, could crash in report creation on modules excluded that were
   asked via command line for inclusion. Fixed in 1.9.3 already.

-  Anti-Bloat: Fix for newer ``streamlit``, it was causing
   ``SyntaxError`` for the compilation. Fixed in 1.9.4 already.

-  Arch: Added support for their OS release file location too. Fixed in
   1.9.4 already.

-  Windows: Fix, MinGW64 doesn't accept chinese module names a C source
   files. Use short paths for these instead. Fixed in 1.9.4 already.

-  Standalone: Added missing DLL for ``libusb_package`` package. Fixed
   in 1.9.4 already.

-  Fix, properly skip directories with non-module top level names when
   trying to find top level packages of distributions. Fixed in 1.9.4
   already.

-  Fix, avoid memory leak bug in triggered by ``rich`` package. Fixed in
   1.9.4 already.

-  Python3.11+: Fix, didn't detect non-keywords on star dict calls in
   some cases. Fixed in 1.9.4 already.

-  Fix, avoid crashes due to unrecognized installers on macOS and
   Windows, some packages that are built via legacy fallbacks of certain
   pip versions do not leave any indication of their origin at all.
   Fixed in 1.9.4 already.

-  Windows: Fix, need to indicate that the program is long path aware or
   else it cannot work with the paths. Fixed in 1.9.4 already.

-  Debian: The ``extern`` namespace might not exist in the
   ``pkg_resources`` module, make the code work with versions that
   remove it and use the proper external package names then. Fixed in
   1.9.6 already.

-  Compatibility: Fix, need to also have ``.exists`` method in our files
   reader objects. Fixed in 1.9.5 already.

-  macOS: Fix, PyQt5 standalone can fail due to ``libqpdf`` too.

-  Compatibility: Make ``dill-compat`` plugin support module mode too,
   previously this only worked for executables only. Fixed in 1.9.6
   already.

-  Standalone: Added data file for ``curl_cffi`` package. Fixed in 1.9.6
   already.

-  Windows: Fix warnings given by MinGW64 in debug mode for onefile
   compilation. Fixed in 1.9.6 already.

-  Python2: The handling of DLL permission changes was not robust
   against using unicode filenames. Fixed in 1.9.7 already.

-  Python2: Fix, could crash on Debian packages when detecting their
   installer. Fixed in 1.9.7 already.

-  Standalone: Added required data file for ``astor`` package. Fixed in
   1.9.7 already.

-  Reports: Fix, in case of build crashes during optimization, the bug
   report creation could be crashing because the module is not in the
   list of done modules yet. Fixed in 1.9.7 already.

-  Python2: Fix, ``unittest.mock`` was not yet available, code
   attempting to use it was crashing the compilation. Fixed in 1.9.7
   already.

-  Accelerated: Fix, tensorflow configuration removing ``site`` usage
   needs to apply only to standalone mode. Fixed in 1.9.7 already.

-  Plugins: Fix, the ``get_dist_name`` Nuitka Package Configuration
   function could crash in some rare configurations. Fixed in 1.9.7
   already.

-  Standalone: Added necessary data file for ``pygame`` package. Added
   in 1.9.7 already.

-  Standalone: Fix, was not properly handling standard library
   overloading module names for decisions. Inclusion and compilation
   mode were made as if the module was part of the standard library,
   rather than user code. This is now properly checking if it's also an
   actual standard library module.

-  Plugins: Fix, crashing on missing absence message with no UPX binary
   was found.

-  Windows: Fix, couldn't load extension modules from UNC paths, so
   standalone distributions failed to launch from network drives. This
   now works again and was a regression from adding support for symlinks
   on Windows.

-  Standalone: Added support for non-legacy ``pillow`` in ``imageio``
   package.

-  Standalone: Added required ``easyOCR`` data file.

-  Nuitka-Python: Fix, do not demote to non-LTO for "too many" modules
   there in the default auto mode, it doesn't work without it.

-  Fix, ``python setup.py install`` could fail. Apparently it tries to
   lookup Nuitka during installation, which then could fail, due to
   hacks we due to make sure wheels are platform dependent. That hack is
   of course not really needed for install, since no collision is going
   to happen there.

-  macOS: Fix, the standard ``matplotlib`` plugin that uses native UI
   was not included yet, and it was also not working due to bindings
   requiring uncompiled functions, which is now worked around.

-  Compatibility: Add back PySide6 workaround for overloading names like
   ``update`` with slots.

-  Standalone: Added ``geopandas`` data files.

-  Python2: Fix, code objects must be made from ``str`` exactly,
   ``unicode`` however was used in some configurations after recent
   improvements to the run time path handling.

-  Standalone: Added missing data files for ``boto``, the predecessor of
   ``boto3`` as well.

-  Standalone: Added missing DLL for ``tensorflow`` factorization
   module.

-  Compatibility: Fix, PySide2 and PySide6 signal disconnection without
   arguments were not working yet.

-  Standalone: Added support for ``toga``.

-  Scons: Fix, need to Avoid picking up ``clang`` from PATH on Windows
   with ``--clang`` provided, as only our winlibs version is really
   working.

-  Fix, version of ``setuptools`` when included (which we try to avoid
   very much) was ``None`` which breaks some users of it, now it's the
   correct version so checks of e.g. ``setuptools_scm`` can succeed.

-  Fix, icon options for platforms were conflated, so what should be
   windows only icon could get used on other platforms as well.

-  Fix, could not create compiled methods from compiled methods. Also
   now errors out for invalid types given properly.

New Features
============

-  Plugins: Added support for module decisions, these are ``parameters``
   provided by the user which can be used to influence the Nuitka per
   package configuration with a new ``get_parameter`` function. We are
   using these to control important choices in the user, sometimes
   warning it to make that decision, if the default can be considered
   problematic.

-  Plugins: Added support for ``variables`` in Nuitka package
   configurations. We can now query at compile time, values from
   installed packages and use them, e.g. to know what backend is to be
   used.

-  Standalone: Added module decision to disable Torch JIT. This is
   generally the right idea, but the decision is still asked for since
   some packages and programs want to do Torch Tracing, and that is then
   disabled as well. This makes a bunch of transformers programs work.

-  Standalone: Added module decision to disable Numba JIT. This makes
   ``numba`` work in some cases, but not all. Some packages go very deep
   with JIT integration, but simpler uses will now compile.

-  New option ``--include-onefile-external-data`` allows you to specify
   file patterns that you included by other data files others, but to
   put those files not inside, but on the outside of the onefile binary.
   This makes it easier to create deployments fully within Nuitka
   project configuration, and to change your mind back and forth without
   adding/removing the data file option.

-  macOS: Added new value ``auto`` for detecting signing identity, if
   only one is available in the system.

-  macOS: Added support for ``--copyright`` and ``--trademark``
   information to be in app bundles as well, this was previously Windows
   only.

-  Windows: Added support for using junctions in the Python environment,
   these are used e.g. when installing via ``scoop``. Added in 1.9.2
   already.

-  Added option ``--cf-protection`` to select the control flow
   protection mode for the GCC compiler and deviate from default values
   of some environments to less strict values.

-  Reports: Added output filename to report, mainly intended for
   automatically locating the compilation result independent of options
   used.

-  Plugins: Now provides a checksum for yaml files, but not yet verifies
   them at runtime, to ask the user to run the checker tool to update it
   when they make modifications.

-  Windows: Detect when we create too large compiled executables. There
   is a limit of 2GB that you might e.g. violate by attempting to embed
   very large files. This doesn't cover onefile yet.

-  Watch: The tool can now create PRs with the changes in Nuitka-Watch
   for merging, this is for using it in the CI.

-  Watch: Scanning for Python versions now requires ``pipenv`` to be
   installed in them to be found.

-  Watch: Added ability to create branch and PR from watch run results.

-  Plugins: Added ``overridden-environment-variables`` feature to
   package configuration. These are environment variable changes that
   only last during the import of that module and are undone later.

-  Plugins: Added ``force-environment-variables`` feature to package
   configuration. These are environment variable changes done on module
   import that are not undone.

-  Nuitka-Action: Nuitka options that can be given multiple times,
   cannot be specified multiple times in your workflow. As a workaround,
   Nuitka now allows in Actions, to use new lines as separator. This is
   best done with this kind of quoting a multiline string.

   .. code:: yaml

      include-data-dir: |
         a=b
         c=d

-  The Nuitka Package Configuration ``no-auto-follow`` now applies
   recursively, i.e. that a top level package can have it, and not every
   sub-package that uses a package but should not be automatically
   followed, does have to say this. With this e.g. ``networkx``
   configuration became simpler, and yet covered automatically older
   versions as well, and future changes too.

-  Windows: Added support for compiling in case sensitive folders. When
   this option is enabled, using ``os.path.normcase`` can make filenames
   not found, so with a few cleanups, for lazy code that wasn't really
   using the APIs designed for comparisons and filename suffix testing,
   this works now better.

-  The ``__compiled__`` value has a new attribute ``containing_dir``
   that allows to find where a module, accelerate executable, a
   standalone dist folder, a macOS app bundle, or the onefile binary
   lives in a consistent fashion. This allows esp. better use than
   ``sys.argv[0]`` which points deep into the ``.app`` bundle, and can
   be used cross platform.

Optimization
============

-  Scalability: Avoid variables that are not shared to be treated as if
   they were, marking their type shape as ``tshape_unknown`` in the
   first micro pass. These micro passes are not visible, but basically
   constitute a full visit of the module tree over and over, until no
   more optimization is changing it. This can lead to quicker
   resolution, as that unknown type shape effectively disallowed all
   optimization for variables and reduce the number of necessary micro
   passes by one.

-  Escaped variables did provide a type shape ``tshape_unknown`` and
   while a lot of optimization looks for value knowledge, and gets by
   the escaped nature of the value, sometimes, this was seriously
   inhibiting some of the type based optimization.

-  Loop type shape analysis now succeeds in detecting the types for this
   code example, which is sort of a break-through for future performance
   enhancements in generated code.

   .. code:: python

      # Initial the value of "i" is "NUITKA_NINT_UNASSIGNED" in its
      # indicator part. The C compiler will remove that assignment
      # as it's only checked in the assignment coming up.
      i = 0
      # Assignment from a constant, produces a value where both the C
      # and the object value are value. This is indicated by a value
      # of "NUITKA_NINT_BOTH_VALID". The code generation will assign
      # both the object member from a prepared value, and the clong
      # member to 0.

      # For the conditional check, "NUITKA_NINT_CLONG_VALID" will
      # always be set, and therefore function will resort to comparing
      # that clong member against 9 simply, that will always be very
      # fast. Depending on how well the C compiler can tell if an overflow
      # can even occur, such that an object might get created, it can even
      # optimize that statically. In this case it probably could, but we
      # do not rely on that to be fast.
      while i < 9:  # RICH_COMPARE_LT_CBOOL_NINT_CLONG
         # Here, we might change the type of the object. In Python2,
         # this can change from ``int`` to ``long``, and our type
         # analysis tells us that. We can consider another thing,
         # not "NINT", but "NINTLONG" or so, to special case that
         # code. We ignore Python2 here, but multiple possible types
         # will be an issue, e.g. list or tuple, float or complex.
         # So this calls a function, that returns a value of type
         # "NINT" (actually it will become an in-place operation
         # but lets ignore that too).
         # That function is "BINARY_OPERATION_ADD_NINT_NINT_CLONG"(i, 1)
         # and it is going to check if the CLONG is valid, add the one,
         # and set to result to a new int. It will reset the
         # "NUITKA_NINT_OBJECT_VALID" flag, since the object will not be
         # bothered to create.
         i = i + 1

      # Since "NUITKA_INT_OBJECT_VALID" not given, need to create the
      # PyObject and return it.
      return i

-  Python3.11+: Use ``tomllib`` from standard library for our distutils
   integration into pyproject based builds.

-  Avoid late specialization for ``None`` returns in generators and do
   it during tree building already, to remove noise.

-  Added successful detection of static libpython for self compiled
   Python Linux and macOS. This makes it work with ``pyenv`` as well.

-  Standalone: Avoid including ``.pyx`` files when scanning for data
   files, these are code files too, in this case source files that are
   definitely unused most of the time.

-  macOS: Make static libpython default with CPython for more compact
   standalone distribution and faster binaries.

-  Remove non-existent entries from ``sys.path``, avoiding many file
   system lookups during import scans.

-  Anti-Bloat: Avoid using ``triton`` in ``torch`` package in more
   cases. Added in 1.9.2 already.

-  Anti-Bloat: Avoid using ``pytest`` in ``knetworkx`` package in more
   cases. Added in 1.9.2 already.

-  Anti-Bloat: Avoid using ``IPython`` in ``distributed`` package. Added
   in 1.9.3 already.

-  Anti-Bloat: Avoid using ``dask`` in ``skimage``. Added in 1.9.3
   already.

-  Anti-Bloat: Avoid using ``triton`` in the ``bitsandbytes`` package.
   Added in 1.9.3 already.

-  Anti-Bloat: Avoid ``IPython`` in ``tf_keras`` package as well. Added
   in 1.9.6 already.

-  Anti-Bloat: Avoid ``unittest`` in ``mock.mock`` module. Added in
   1.9.7 already.

-  Avoid importing ``setuptools_scm`` during compilation when using the
   ``tqdm`` inline copy, this also avoids a warning on Ubuntu. Added in
   1.9.7 already.

-  Anti-Bloat: Avoid ``doctest`` in ``skimage`` in their ``tifffile``
   inline copy as well. Added in 1.9.7 already.

-  Anti-Bloat: Avoid ``h5py.tests`` with older ``h5py`` as well. Added
   in 1.9.7 already.

-  Anti-Bloat: Using ``distributed.utils_test`` is also considered using
   ``pytest``.

-  Anti-Bloat: Avoid ``IPython`` in the ``pip`` package.

-  Anti-Bloat: Avoid ``site`` module for older ``tensorflow`` versions
   too.

-  Anti-Bloat: Avoid more ``unittest`` usages in ``tensorflow``
   packages.

-  Anti-Bloat: Avoid ``nose`` in ``skimage`` package.

-  Anti-Bloat: Avoid ``nose`` in ``networkx`` package.

-  Anti-Bloat: Avoid ``nose`` in ``pywt`` package.

Organizational
==============

-  UI: Change template paths over from ``%VAR%`` to ``{VAR}``.

   The old spec values are migrated transparently and continue to work,
   but get a warning when used.

   The new code detects unknown variable names and more formatting
   issues than before.

   Using only the ``{PID}`` value for process ID, is now making it
   temporary value for onefile, that was previously a bug.

   The main benefit and reason of doing this, is that Windows
   ``CMD.EXE`` does expand those values before Nuitka sees them as even
   with quoting ``%TEMP%`` is the current one on the building machine, a
   recipe for disaster. As some people still use that, and e.g.
   ``os.system`` or ``subprocess`` with ``shell=True`` will use it too,
   this is just not sustainable for a good user experience.

   As a result, compile time and run time variables now clash, there is
   e.g. ``{VERSION}`` (program version information given) and
   ``{Version}`` (Nuitka version), and we should clean that up too.

-  Project: Added Code of Conduct. Adapted from the one used in the
   Linux kernel.

-  UI: Warnings given by Nuitka used to be in red color, changed those
   to be yellow for consistency.

-  User Manual: Added pointer for Nuitka-Action `Nuitka-Action
   <https://github.com/Nuitka/Nuitka-Action>`__ for users interested in
   using Nuitka in GitHub workflows.

-  Added ``.gitignore`` to build folder that just causes these folders
   to be ignored by git.

-  User Manual: Added information on how to debug fork bombs from
   created binaries.

-  Debugging: The output of ``--experimental=--report-refcounts`` that
   we use to show leaks of compiled time objects at program exit, now
   counts and reports on functions, generator objects and compiled cells
   as well.

-  Quality: Warnings from ``yamllint`` not disabled are errors. These
   were only output, but didn't cause the autoformat to error exit yet.

-  UI: Enhanced formatting of info traces, drop the ``:INFO`` part that
   shouts, and reserve that for errors and warnings. Also format info
   messages to make sure they fit into the line.

-  UI: Changed ``--show-source-changes`` to accept module pattern to
   make it easier to only see the ones currently being worked on. To get
   the old behavior of showing everything, use ``*`` as a pattern.

-  UI: Allow using ``~`` in data files source path for command line
   options and expand it properly.

-  Quality: Enhanced schema for our package configuration yaml files to
   detect suffixes with leading dots, that is not wanted. These now fail
   checks, but we also tolerate them now.

-  Quality: Check module names used in the package configuration yaml
   files for validity, this catches e.g. trailing dots.

-  Quality: Make sure to really prefer ``clang-format`` from Visual Code
   and MSVC for formatting C code, otherwise a system installed one
   could be used that gives slightly different outputs.

-  Scons: Allow disabling to enforce no warnings for C compilation

   Currently only for gcc, where we need it until loop tracing is
   better, we can now use ``--experimental=allow-c-warnings`` options to
   make ``--debug`` work for some known currently unavoidable warnings.

-  macOS: Make ``--macos-create-app-bundle`` imply standalone mode, it's
   not working or useful for accelerated mode anyway.

-  Standalone: Added support for using self-compiled Python versions
   that are not installed on Linux and macOS. This avoids having to do
   ``make install`` and can ease debugging with changes made in Python
   core itself. Added in 1.9.6 already.

-  Release: Added ability to simple re-date hotfixes. Previously the
   version bump commit needed to be dropped, now a fixup commit is easy
   to generate.

-  Release: Man pages are no longer built during package builds, but are
   available statically in the git, which should make it easier.

-  Release: Disable verbose output in package installation of Nuitka, it
   never was any use, and just makes things hard to read.

-  UI: Check user yaml file present immediately. Otherwise it was
   crashing when parsing yaml files first time with less comprehensible
   exceptions. Added in 1.9.7 already.

-  Quality: Updated to latest ``rstfmt``, ``black`` and ``isort``
   versions.

-  Debian: Remove references to PDF documentation that no longer exists.

-  Quality: Do not crash when collecting modified files due to deleted
   files.

-  UI: Detect the Alpine flavor of Python as well.

-  UI: Detect ``manylinux`` Pythons as a Python flavors as well.

-  UI: Detect self compiled uninstalled Python as a dedicated flavor.

Cleanups
========

-  For the Nuitka-Action part of the available options is now generated
   from Nuitka option definitions itself, adding some previously missing
   options as a result. As a result, adding
   ``--include-onefile-external-data`` was automatic this time.

-  The warnings for onefile only options without onefile mode provided
   have been moved to common code, and in some cases were having wrong
   texts corrected.

-  Use enum definitions in the Nuitka Package Configuration schema
   rather than manual ``oneOf`` types.

-  The User Manual was proof read and had a bunch of wordings improved.

-  Cleanup, avoid "unused but set variable" warning from the C compiler
   for hard some forms of hard imports.

-  Prefer ``os.getenv`` over ``os.environ.get`` for readability.

-  Changed parts of the C codes that ``clang-format`` had a hard time
   with to something more normal.

Tests
=====

-  When locating the standalone binary created, use a compilation report
   and resolve the path specified there. This allows macOS app bundles
   to be used in these tests as well.

-  Made the PyQt tests executable on macOS too adding necessary options.

-  Added reference test case for unpacking into a list, this was not
   covered but under suspect of reference leaking which turns out to be
   wrong.

-  Much enhanced usage of ``virtualenv`` in the ``distutils`` test
   cases. We make more sure to delete them even in case of issues. We
   disable warnings during Nuitka package installation. The code to
   execute a case was factored out and became more clear. We now handle
   errors in execution with stating what case actually failed, this was
   a bit hard to tell previously. Also do not install Nuitka when a
   pyproject case is used, since the build tool installs Nuitka itself.

Summary
=======

This release deserves the 2.0 marker, as it is ground breaking in many
ways. The loop type analysis stands out on the optimization front. This
will open an avenue for much optimized code at least for some benchmark
examples this summer.

The new features for package configuration, demonstrate abilities to
avoid plugins for Nuitka, where those previously would have been used.
The new ``variables`` and ``parameters`` made it unnecessary to have
them, and still add compile time variable use and user decisions and
information, without them.

The scope of supported Python configurations got expanded a bit, and the
the usual slew of anti-bloat work and new packages supported, makes
Nuitka an ever more round package.

The improved user dialog with less noisy messages and slightly better
coloring, continues a trend, where Nuitka becomes more and more easy to
use.

.. include:: ../dynamic.inc
