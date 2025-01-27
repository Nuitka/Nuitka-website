:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per-version changes and comments for the
upcoming Nuitka |NUITKA_VERSION_NEXT| as a draft about hot-fixes of the
current stable release as |NUITKA_VERSION| as well.

****************************
 Nuitka Release 2.6 (Draft)
****************************

.. note::

   This a draft of the release notes for 2.6, which is supposed to add
   Nuitka standalone backend support and enhanced 3.13 compatibility,
   and lots of scalability in general, aiming at an order of magnitude
   improvement for compile times.

This release is in progress still and documentation might lag behind
development.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

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

Unified the code used for generating source archives for PyPI uploads,
ensuring consistency between production and standard archives.

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

This release is not complete yet.

.. include:: ../dynamic.inc
