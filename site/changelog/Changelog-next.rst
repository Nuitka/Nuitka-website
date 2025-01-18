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

-  **MSYS2:** Need to normalize paths to native in more places for MinGW
   variant

   Since ``os.path.normpath`` doesn't actually normalize to native Win32
   paths with **MSYS2**, but to forward slashes, we need to do it on our
   own. Fixed in 2.5.1 already.

-  Fix, extensions modules that failed to locate could crash the
   compilation starting with 2.5, rather than giving proper error as
   before. Fixed in 2.5.1 already.

-  Fix, was considering files as potential sub-modules for
   ``--include-package`` that actually have an illegal name, due to
   ``.`` in their basename. These need to be skipped. Fixed in 2.5.1
   already.

-  Stubgen: Do not crash when ``stubgen`` crashes on code it cannot
   handle and ignore its exceptions. Fixed in 2.5.1 already.

-  Stubgen: Do not crash on assignments to non-variables. Fixed in 2.5.1
   already.

-  Python3: Fixed a regression of 2.5 with exception handling of
   generators that could lead to segfaults. Fixed in 2.5.2 already.

-  Python3.11+: Fix, dictionary copies of large split directories could
   become corrupt. Fixed in 2.5.2 already.

   This mostly affects instance dictionaries, which are created as this
   kind of copy until they are updated. These then these would present
   issues when being updated with new keys afterwards.

-  Python3.11+: Fix, must not assume module dictionary to be a string
   dictionary. Some modules have non-strings being put there, e.g
   ``Foundation`` on macOS. Fixed in 2.5.2 already.

-  Fix, the ``--deployment`` didn't impact the C side as intended, only
   the individual disables were applied there. Fixed in 2.5.2 already.

-  Fix, unary operations could crash the compilation if used inside a
   binary operation. Fixed in 2.5.3 already.

-  Onefile: Fix, the handling of ``__compiled__.original_argv0`` was
   incorrect and could lead to crashes. Fixed in 2.5.4 already.

-  Fix, calls to ``tensorflow.function`` using only keyword arguments
   segfaulted at runtime. Fixed in 2.5.5 already.

-  macOS: Ignore harmless warning given for x64 DLLs on arm64 with newer
   macOS. Fixed in 2.5.5 already.

-  Python3.13: Fix, our dictionary code could crash copying dictionaries
   due to internal Python changes not yet followed. Fixed in 2.5.6
   already.

-  macOS: Improve signing onefile mode, was not applying
   ``--macos-signed-app-name`` in the signature of the binaries, was
   only used for app bundles so far. Fixed in 2.5.6 already.

-  Fix, was adding too many paths as extra directories from Nuitka
   package configuration. This only affected ``win32com`` package as it
   is the only user of the ``package-dirs`` import hack right now. Fixed
   in 2.5.6 already.

-  Python2: Fix, can have negative CRC32 values, leading to crashes when
   creating onefile with Python2 on macOS, this might affect more
   versions though. Fixed in 2.5.6 already.

-  Plugins: Fix the code provided in ``pre-import-code`` didn't have an
   effect anymore due to a regression. Fixed in 2.5.6 already.

-  macOS: Fix, do not recommend app bundle mode if the user already uses
   it. Fixed in 2.5.6 already.

-  macOS: Fix, need to normalize paths using ``~`` when as part of
   output directory argument.

-  macOS: Fix, need to consider GitHub Actions Python a Homebrew Python,
   too. Otherwise some DLLs cannot be resolved. Fixed in 2.5.7 already.

-  Fix, could reference leak values send into generator objects. Was not
   affecting asyncgen and coroutines, they did that correctly already.
   Fixed in 2.5.7 already.

-  Fix, ``--include-package`` scan picked up both package init file and
   competing Python files both, leading to compile time conflicts. Fixed
   in 2.5.7 already.

-  Module: Fix, for modules created for Python 3.12, the handling of
   string constants could still trigger assertions and the loading of
   modules created with 3.12.7 or newer failed on older Python 3.12
   versions when created with Nuitka 2.5.5-2.5.6. Fixed in 2.5.7
   already.

-  Python3.10+: Calling some method descriptors could use incorrect
   tuple code. We don't commonly use that though, so this was only
   observed in a Python2 assertion which wouldn't be affected. Fixed in
   2.5.7 already.

-  Python3.13: Fix, resource readers accept multiple arguments for
   ``importlib.resources.read_text`` and ``encoding`` and ``errors``
   became keyword-only, which we need to follow as well.

-  Scons: Avoid using platform encoding to decode ``ccache`` log. Not
   all encoding implement encoding errors, but ``latin1`` cannot give
   them, so lets use that, it's sufficient to match filenames across log
   lines. Fixed in 2.5.7 already.

-  Python3.12+: Fix, static link libraries for ``hacl`` if asked for do
   not exist, ignore these. Fixed in 2.5.7 already.

-  Fix, memory leak for results of functions called via specs. This
   could leak memory leaks for a few operations. Hard import operations
   we overloaded were most affected. Fixed in 2.5.7 already.

-  Fix, when finding multiple distributions for a package, choose the
   one most correctly matching files. This helps in cases, where an
   older version of ``python-opencv`` was forcefully overwritten with
   ``python-opencv-headless`` or vice version, picking the actual
   version to use, and make proper decisions for our Nuitka package
   configuration and reporting. Fixed in 2.5.8 already.

-  Python2: Fix, initializing ``containing_dir`` for onefile could crash
   when trying to convert binary name to directory name with the
   ``os.dirname`` function that may not yet be fully loaded. We now pass
   the directory name from the onefile bootstrap, which also is simpler
   code. Fixed in 2.5.8 already.

-  **Anaconda**: Fix, some packages need to load DLLs via ``PATH``
   environment variables on Windows, therefore cannot remove all usage
   of ``PATH``, but only those not pointing to inside of the
   installation prefix. Fixed in 2.5.8 already.

-  **Anaconda**: Fix, is ``is_conda_package`` was not working properly
   when distribution name and package name were divergent. Fixed in
   2.5.8 already.

-  **Anaconda**: Fix, need to check conda meta data to resolve package
   names of distributions, for some packages there is not files metadata
   available via the typical files. Fixed in 2.5.8 already.

-  **MSYS2**: Fix, downloaded gcc path needs to be normalized to native
   slashes or else it can fail during compilation. Fixed in 2.5.9
   already.

-  **Python3.13**: Fix, static libpython wasn't working for Linux, an
   unexposed API that we use changed the signature and we needed to
   follow that. Fixed in 2.5.9 already.

-  **Python3.6+**: Fix, ``asyncgen`` resurrected when they had a
   finalizer attached, leading to memory leaks with asyncio in case of
   exceptions in the ``asyncgen``. Fixed in 2.5.10 already.

-  UI: Fix, do not prompt for gcc download during ``--version`` output.
   This could happen on Windows without MSVC or improper gcc installed.

-  Fix, wasn't compatible of ``os.lstat`` or ``os.stat`` were monkey
   patched, which some tests seem to do.

-  **Data Composer**: Fix, need to make sure the json statistics output
   is deterministic, as the keys were not sorted, making build
   comparisons fail on them.

-  **Python3.6+** Fix, ``asyncgen`` with finalizer leaked their objects
   causing potentially large memory leaks when using ``asyncio`` in case
   of exceptions.

-  Fix, empty generators (necessarily an optimization result) still
   produced context code that ended up being unused, leading to C
   compilation warnings.

-  **Python3.6+**: Fix, lost a reference to **asend** value. As this is
   typically ``None`` this was more a reference leak then a memory leak,
   but could show up in some cases.

-  **Python3.5+**: Properly handle ``coroutine`` and ``asyncgen``
   resurrecting.

   This could cause memory leaks with ``asyncio`` and ``asyncgen`` and
   also incompatibility with ``finally`` code in coroutines that wasn't
   executed in some cases, although it should have due to too early
   closing.

-  **Python3**: Properly handle ``generator`` objects resurrecting
   during their deallocation. There has been no demonstration this is
   actually needed, but potentially old-style coroutines via decorator
   ``types.coroutine`` could have had the same issues as coroutines did.

-  **PGO**: Fix, during taking the runtime traces, the output was
   initialized too late, which could cause crashes.

Package Support
===============

-  Standalone: Add inclusion of metadata for ``jupyter_client`` as it
   uses that itself. Added in 2.5.1 already.

-  Standalone: Added support for ``llama_cpp`` package. Added in 2.5.1
   already.

-  Standalone: Added support for ``litellm`` package. Added in 2.5.2
   already.

-  Standalone: Added support for ``lab_lamma`` package. Added in 2.5.2
   already.

-  Standalone: Added support for ``docling`` metadata. Added in 2.5.5
   already.

-  Standalone: Added support for ``pypdfium`` on Linux too. Added in
   2.5.5 already.

-  Standalone: Added support for using ``debian" package``. Added in
   2.5.5 already.

-  Standalone: Added support for ``pdfminer`` package. Added in 2.5.5
   already.

-  Standalone: Added missing dependencies of ``torch._dynamo.polyfills``
   package. Added in 2.5.6 already.

-  Standalone: Add support for ``rtree`` on Linux as well. The old
   static config only worked on Windows and macOS, this detects it from
   the module code. Added in 2.5.6 already.

-  Standalone: Add missing ``pywebview`` js data files. Added in 2.5.7
   already.

-  Standalone: Added support for newer ``sklearn`` package. Added in
   2.5.7 already.

-  Standalone: Added support for newer ``dask`` package. Added in 2.5.7
   already.

-  Standalone: Added support for newer ``transformers`` package. Added
   in 2.5.7 already.

-  Windows: Put ``numpy`` DLLs top level for enhanced support in Nuitka
   VM. Added in 2.5.7 already.

-  Standalone: Allow including no browsers with ``playwright``. Added in
   2.5.7 already.

-  Standalone: Added support for newer ``sqlfluff`` package. Added in
   2.5.8 already.

-  Standalone: Added support for the ``opencv`` conda package. We needed
   to disable workarounds not needed there for dependencies. Added in
   2.5.8 already.

-  Standalone: Added support for newer ``soundfile`` package.

-  Standalone: Added support for newer ``coincurve`` package.

-  Standalone: Added support for newer ``apscheduler`` package.

-  macOS: Seems PyQt5 in standalone mode works on macOS now and no
   longer requires bundle mode, so we remove the error and forcing of a
   workaround in there.

-  Standalone: Added support for ``seleniumbase`` package downloads.

New Features
============

-  Module: Use 2-phase loading for all modules with Python3.5 or higher.
   This enhances loading them as sub-packages for Python3.12+ where the
   loading context is no longer accessible.

-  UI: Added ``app`` module for ``--mode`` parameter. On macOS it's an
   app, elsewhere it's a onefile binary. This replaces
   ``--macos-create-app-bundle`` for which we didn't have something yet.
   Added in 2.5.5 already.

-  UI: Added ``package`` mode, which is similar to ``module``, but also
   includes all sub-modules of the package automatically without having
   to ask for that with ``--include-package`` manually.

-  Module: Allow disabling the use of ``stubgen`` entirely. Added in
   2.5.1 already.

-  Homebrew: Added support for ``tcl9`` with ``tk-inter`` plugin.

-  When multiple distributions are installed for the same package name,
   try and figure out which one was installed less, such that
   ``python-opencv`` and ``python-opencv-headless`` with different
   versions installed are properly recognized for the version used.

-  The release 3.13.1 broke standalone mode of Nuitka by making a
   workaround added for 3.10.0 breaking. Added in 2.5.6 already.

-  Plugins: Uses new feature for absolute source paths (typically of
   course from variables or relative to constants), these can be
   populated from variables and be more powerful the ``by_code`` DLL
   feature, that we might end up removing in favor of it. Added in 2.5.6
   already.

-  Plugins: In Nuitka Package configuration ``variable`` sections can
   also have ``when`` conditions.

-  macOS: For app bundles, automatically switch to containing directory
   if not launched from the command line. Otherwise the current
   directory is ``/`` which is almost never correct and contrary to some
   users expectations too. Added in 2.5.6 already.

-  Compatibility: Do not reject setting compiled frame ``f_trace``
   outright, instead a deployment flag
   ``--no-deployment-flag=frame-useless-set-trace`` can be used to allow
   it, but it will be ignored.

-  Windows: Added ability to detect extension module entry points, using
   an inline copy of ``pefile``. With that ``--list-package-dlls`` can
   now check if an extension module is really valid on that platform as
   well. It also means we could consider detecting extension modules
   automatically on the 3 major OSes.

-  Watch: Added support for using ``conda`` packages rather than PyPI
   packages.

-  UI: Added ``--list-package-exe`` to complement
   ``--list-package-dlls`` for analysis of packages when making Nuitka
   Package Configuration.

-  **Windows ARM**: Remove workarounds no longer needed to compile. The
   lack of dependency analysis might have to be corrected in a hotfix,
   then this configuration ought to be supported.

Optimization
============

-  Experimental code for more compact code object usage leading to more
   scalable C code and constants usage. This will allow to speed up C
   compilation and code generation a future once properly validated.

-  Scons: Add support for C23 embedding of the constants blob. With
   Clang 19+ and GCC 15+ it is going to be used, unless it's Windows or
   macOS where we use other methods currently.

-  In case of duplicated package dirs, avoid checking paths multiple
   times, as file system accesses can become very slow this makes some
   cases much faster.

-  Detect possible static libpython for self compiled uninstalled Python
   too.

Anti-Bloat
==========

-  Improved ``no_docstrings`` support for ``xgboost`` package. Added in
   2.5.7 already.

-  Avoid using ``numpy`` for ``PIL`` package.

-  Avoid using ``yaml`` for ``numpy`` package.

-  Avoid including ``tcltest`` TCL code when using tk-inter. Their TCL
   files will be unused for sure.

-  Anti-Bloat: Avoid using ``IPython`` from ``comm`` package.

-  Anti-Bloat: Avoid using ``pytest`` from ``pdbp`` package.

Organizational
==============

-  UI: Added categories for plugins and show non package-support plugin
   options by default in ``--help`` output. Added dedicated
   ``--help-plugins`` and point it out in the ``--help`` where all
   plugin options are shown without the need to enable a plugin.

-  UI: Enhanced warnings for onefile and OS specific options, these are
   now given unless coming from a Nuitka-Action context, where people do
   build for different modes with one set of configuration.

-  Nuitka-Action: The default for ``mode`` is now ``app``, which will
   build an application bundle on macOS and a onefile binary otherwise.

-  UI: Use report path for executable in ``--version`` output.

   We don't want people to be forced to output their home directory
   path, it only makes them want to avoid giving the whole output.

-  UI: Output the Python flavor name in startup compilation message.

-  UI: Detect missing product or file version if only other Windows
   version information is given and give an explicit error, rather than
   just an assertion error during post processing.

-  UI: The container argument couldn't be a non-template file for
   ``run-inside-nuitka-container``. Fixed in 2.5.2.

-  Release: Use virtualenv for PyPI upload ``sdist`` creation. The
   setuptools version decides the project name casing. For now, we use
   the one that produces deprecated filenames, but we should be ready
   for the new one with this.

-  Release: Use ``osc`` binary from virtualenv, system one can be
   broken, as is currently the case for Ubuntu.

-  Debugging: Allow disabling changing to short paths on Windows with an
   experimental option.

-  UI: Detect external data files that will be overwriting explicitly
   the original file, and ask the user to provide an output directory,
   so it can be done. Added in 2.5.6 already.

-  UI: Added alias ``--include-data-files-external`` for external data
   files option that is not onefile specific, since we want this feature
   to be universally used.

-  UI: Allow ``none`` as macOS icon option value to disable warning
   about not giving it, should that be what you want to do.

-  UI: Error out on icon filenames without suffixes, as no file type can
   be inferred.

-  UI: Examples for ``--include-package-data`` with file patterns were
   wrong, using the wrong delimiter.

-  Scons: Warn about using gcc with LTO and no ``make`` available, as
   that will not work. The gcc warnings are not easy to parse for normal
   Python people.

-  Debugging: Allow to not disable printing during reference count
   tests, this can be helpful to see traces added during debugging
   sessions.

-  Debugging: Developer Manual: Added small code snipped for reference
   leak testing of modules.

Tests
=====

-  Temporarily disable the tests that expose the 3.13.1 regressions.

-  Use more common code for package tests, the scanning for test cases
   and main files in there now uses common code, too.

-  Added support for testing variations of a test with different extra
   flags given and by exposing a ``NUITKA_TEST_VARIANT`` as a variable
   name.

-  Detect commercial-only test cases from their name rather than hard
   coding them into the runner. Also remove them from the standard
   distribution where they are not useful to have.

-  Use ``--mode`` options in tests, for standalone mode tests check if
   it was applied or error out, add them to project options of each test
   case instead of requiring it globally.

-  Added test case to cover external data file usage in onefile. We have
   had unnoticed regressions that this test would now detect right away.

-  Increased coroutine and asyncgen inspect coverage. So far we didn't
   cover ``inspect.isawaitable`` yet and we should test both function
   and context objects for all things.

Cleanups
========

-  Unified production or standard source archives and code used for PyPI
   uploads, so the result is identical and code is shared.

-  Harmonized the usage of ``include <...>`` vs ``include "..."`` by
   origin of files to be included.

-  Generator code for exception handlers was duplicating code, use the
   ``DROP_GENERATOR_EXCEPTION`` functions instead.

-  Changed more version Python checks on ``>=3.4`` to be ``>=3`` as that
   is what it means to us these days. Also a bunch of 3.3 references
   were still in comments, that too is Python3 to us now.

-  Scons: Share more of the code to build the command options and made
   it simpler to use. Now produces the options dictionary and using an
   ``OrderedDict`` should make it more stable. Otherwise differences in
   build outputs were observed where these are recorded.

-  Our function ``executeToolChecked`` often needs to decode the
   returned ``bytes`` output to ``unicode``. So we added an argument to
   indicate that is desired to be able remove this in many places.

Summary
=======

This release is not complete yet.

.. include:: ../dynamic.inc
