:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes and ongoing development for the
upcoming **Nuitka** |NUITKA_VERSION_NEXT|, serving as a draft changelog.
It also includes details on hot-fixes applied to the current stable
release, |NUITKA_VERSION|.

**************************************************
 **Nuitka** Release |NUITKA_VERSION_NEXT| (Draft)
**************************************************

.. note::

   These are the draft release notes for **Nuitka**
   |NUITKA_VERSION_NEXT|. A primary goal for this version is to deliver
   significant enhancements in scalability.

Development is ongoing, and this documentation might lag slightly behind
the latest code changes.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  **Standalone**: For the "Python Build Standalone" flavor ensured that
   debug builds correctly recognize all their specific built-in modules,
   preventing potential errors. (Fixed in 2.7.2 already.)

-  **Linux**: Fixed a crash when attempting to modify the RPATH of
   statically linked executables (e.g., from ``imageio-ffmpeg``). (Fixed
   in 2.7.2 already.)

-  **Anaconda**: Updated ``PySide2`` support to correctly handle path
   changes in newer Conda packages and improved path normalization for
   robustness. (Fixed in 2.7.2 already.)

-  **macOS**: Corrected handling of ``QtWebKit`` framework resources.
   Previous special handling was removed as symlinking is now default,
   which also resolved an issue of file duplication. (Fixed in 2.7.2
   already.)

-  **Debugging**: Resolved an issue in debug builds where an incorrect
   assertion was done during the addition of distribution metadata.
   (Fixed in 2.7.1 already.)

-  **Module**: Corrected an issue preventing ``stubgen`` from
   functioning with Python versions earlier than 3.6. (Fixed in 2.7.1
   already.)

-  **UI**: Prevented **Nuitka** from crashing when ``--include-module``
   was used with a built-in module. (Fixed in 2.7.1 already.)

-  **Module**: Addressed a compatibility issue where the ``code`` mode
   for the constants blob failed with the C++ fallback. This fallback is
   utilized on very old GCC versions (e.g., default on **CentOS7**),
   which are generally not recommended. (Fixed in 2.7.1 already.)

-  **Standalone**: Resolved an assertion error that could occur in
   certain Python setups due to extension module suffix ordering. The
   issue involved incorrect calculation of the derived module name when
   the wrong suffix was applied (e.g., using ``.so`` to derive a module
   name like ``gdbmmodule`` instead of just ``gdbm``). This was observed
   with Python 2 on **CentOS7** but could potentially affect other
   versions with unconventional extension module configurations. (Fixed
   in 2.7.1 already.)

-  **Python 3.12.0**: Corrected the usage of an internal structure
   identifier that is only available in Python 3.12.1 and later
   versions. (Fixed in 2.7.1 already.)

-  **Plugins**: Prevented crashes in Python setups where importing
   ``pkg_resources`` results in a ``PermissionError``. This typically
   occurs in broken installations, for instance, where some packages are
   installed with root privileges. (Fixed in 2.7.1 already.)

-  **macOS**: Implemented a workaround for data file names that
   previously could not be signed within app bundles. The attempt in
   release 2.7 to sign these files inadvertently caused a regression for
   cases involving illegal filenames. (Fixed in 2.7.1 already.)

-  **Python 2.6**: Addressed an issue where ``staticmethod`` objects
   lacked the ``__func__`` attribute. **Nuitka** now tracks the original
   function as a distinct value. (Fixed in 2.7.1 already.)

-  Corrected behavior for ``orderedset`` implementations that lack a
   ``union`` method, ensuring **Nuitka** does not attempt to use it.
   (Fixed in 2.7.1 already.)

-  **Python 2.6**: Ensured compatibility for setups where the
   ``_PyObject_GC_IS_TRACKED`` macro is unavailable. This macro is now
   used beyond assertions, necessitating support outside of debug mode.
   (Fixed in 2.7.1 already.)

-  **Python 2.6**: Resolved an issue caused by the absence of
   ``sys.version_info.releaselevel`` by utilizing a numeric index
   instead and adding a new helper function to access it. (Fixed in
   2.7.1 already.)

-  **Module**: Corrected the ``__compiled__.main`` value to accurately
   reflects the package in which a module is loaded, this was not the
   case for Python versions prior to 3.12. (Fixed in 2.7.1 already.)

-  **Plugins**: Further improved the ``dill-compat`` plugin by
   preventing assertions related to empty annotations and by removing
   hard-coded module names for greater flexibility. (Fixed in 2.7.1
   already.)

-  **Windows**: For onefile mode using DLL mode, ensure all necessary
   environment variables are correctly set for ``QtWebEngine``.
   Previously, default Qt paths could point incorrectly near the onefile
   binary. (Fixed in 2.7.3 already.)

-  **PySide6**: Fixed an issue with ``PySide6`` where slots defined in
   base classes might not be correctly handled, leading to them only
   working for the first class that used them. (Fixed in 2.7.3 already.)

-  **Plugins**: Enhanced Qt binding plugin support by checking for
   module presence without strictly requiring metadata. This improves
   compatibility with environments like Homebrew or ``uv`` where package
   metadata might be absent. (Fixed in 2.7.3 already.)

-  **macOS**: Ensured the ``apple`` target is specified during linking
   to prevent potential linker warnings about using an ``unknown``
   target in certain configurations. (Fixed in 2.7.3 already.)

-  **macOS**: Disabled the use of static ``libpython`` with ``pyenv``
   installations, as this configuration is currently broken. (Fixed in
   2.7.3 already.)

-  **macOS**: Improved error handling for the
   ``--macos-app-protected-resource`` option by catching cases where a
   description is not provided. (Fixed in 2.7.3 already.)

-  **Plugins**: Enhanced workarounds for ``PySide6``, now also covering
   single-shot timer callbacks. (Fixed in 2.7.4 already.)

-  **Plugins**: Ensured that the Qt binding module is included when
   using accelerated mode with Qt bindings. (Fixed in 2.7.4 already.)

-  **macOS**: Avoided signing through symlinks and minimized their use
   to prevent potential issues, especially during code signing of
   application bundles. (Fixed in 2.7.4 already.)

-  **Windows**: Implemented path shortening for paths used in onefile
   DLL mode to prevent issues with long or Unicode paths. This also
   benefits module mode. (Fixed in 2.7.4 already.)

-  **UI**: The options nanny plugin no longer uses a deprecated option
   for macOS app bundles, preventing potential warnings or issues.
   (Fixed in 2.7.4 already.)

-  **Plugins**: Ensured the correct macOS target architecture is used.
   This particularly useful for ``PySide2`` with universal CPython
   binaries, to prevent compile time crashes e.g. when cross-compiling
   for a different architecture. (Fixed in 2.7.4 already.)

-  **UI**: Fixed a crash that occurred on **macOS** if the ``ccache``
   download was rejected by the user. (Fixed in 2.7.4 already.)

-  **UI**: Improved the warning message related to macOS application
   icons for better clarity. (Added in 2.7.4 already.)

-  **Standalone**: Corrected an issue with QML plugins on **macOS** when
   using newer ``PySide6`` versions. (Fixed in 2.7.4 already.)

-  **Python 3.10+**: Fixed a memory leak where the matched value in
   pattern matching constructs was not being released. (Fixed in 2.7.4
   already.)

-  **compatibility**: Fixed an issue where exception exits for larger
   ``range`` objects, which are not optimized away, were not correctly
   annotated by the compiler. (Fixed in 2.7.4 already.)

-  **Windows**: Corrected an issue with the automatic use of icons for
   ``PySide6`` applications on non-Windows, if Windows icon options were
   used. (Fixed in 2.7.4 already.)

-  **Onefile**: When using DLL mode there was a load error for the DLL
   with MSVC 14.2 or earlier, but older MSVC is to be supported. (Fixed
   in 2.7.5 already.)

-  **Onefile**: Fix, the splash screen was showing in DLL mode twice or
   more, these extra copies couldn't be stopped. (Fixed in 2.7.5
   already.)

Package Support
===============

-  **Standalone**: Introduced support for the ``nicegui`` package.
   (Added in 2.7.1 already.)

-  **Standalone**: Extended support to include ``xgboost.core`` on
   **macOS**. (Added in 2.7.1 already.)

-  **Standalone**: Added needed data files for ``ursina`` package.
   (Added in 2.7.1 already.)

-  **Standalone**: Added support for newer versions of the ``pydantic``
   package. (Added in 2.7.4 already.)

-  **Standalone**: Extended ``libonnxruntime`` support to **macOS**,
   enabling its use in compiled applications on this platform. (Added in
   2.7.4 already.)

-  **Standalone**: Added necessary data files for the ``pygameextra``
   package. (Added in 2.7.4 already.)

-  **Standalone**: Included GL backends for the ``arcade`` package.
   (Added in 2.7.4 already.)

-  **Standalone**: Added more data directories for the ``ursina`` and
   ``panda3d`` packages, improving their out-of-the-box compatibility.
   (Added in 2.7.4 already.)

-  **Standalone**: Added support for newer ``skimage`` package. (Added
   in 2.7.5 already.)

New Features
============

-  None yet

Optimization
============

-  Enhanced detection of ``raise`` statements that use compile-time
   constant values which are not actual exception instances.

   This improvement prevents **Nuitka** from crashing during code
   generation when encountering syntactically valid but semantically
   incorrect code, such as ``raise NotImplemented``. While such code is
   erroneous, it should not cause a compiler crash. (Added in 2.7.1
   already.)

-  **macOS**: Enhanced ``PySide2`` support, removing the general
   requirement for onefile mode. Onefile mode is now only enforced for
   ``QtWebEngine`` due to its specific stability issues if not bundled
   this way. (Added in 2.7.4 already.)

Anti-Bloat
==========

-  Improved handling of the ``astropy`` package by implementing global
   replacements instead of per-module ones. Similar global handling has
   also been applied to ``IPython`` to reduce overhead. (Added in 2.7.1
   already.)

-  Avoid ``docutils`` usage in ``markdown2`` package. (Added in 2.7.1
   already.)

-  Reduced compiled size by avoiding the use of "docutils" within the
   ``markdown2`` package. (Added in 2.7.1 already.)

Organizational
==============

-  **Release:** Ensured proper handling of newer ``setuptools`` versions
   during Nuitka installation. (Fixed in 2.7.4 already.)

Tests
=====

-  Improved test robustness against short paths for package-containing
   directories. (Added in 2.7.4 already.)

-  Prevented test failures caused by rejected download prompts during
   test execution, making CI more stable. (Added in 2.7.4 already.)

-  Refactored common testing code to avoid using ``doctests``,
   preventing warnings in specific standalone mode test scenarios
   related to reference counting. (Added in 2.7.4 already.)

Cleanups
========

-  **Plugins**: Improved ``pkg_resources`` integration by using the
   ``__loader__`` attribute of the registering module for loader type
   registration, avoiding modification of the global ``builtins``
   dictionary. (Fixed in 2.7.2 already.)

-  Improved the logging mechanism for module search scans. It is now
   possible to enable tracing for individual ``locateModule`` calls,
   significantly enhancing readability and aiding debugging efforts.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
