.. post:: 2025/05/30 07:02
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 2.7
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release adds a ton of new features and corrections.

***********
 Bug Fixes
***********

-  **macOS:** Correctly recognize self-dependencies of DLLs that include
   an architecture suffix on ``x86_64``. (Fixed in 2.6.1 already.)

-  **Standalone:** Resolved an issue where ``.pyi`` files associated
   with versioned extension module filenames were not detected. (Fixed
   in 2.6.1 already.)

-  **Standalone:** Fixed ``.pyi`` file parsing failures caused by
   single-line triple quotes. (Fixed in 2.6.1 already.)

-  **Standalone:** Corrected the ``__spec__.origin`` path for packages
   where ``__init__`` is an extension module.

   While this primarily affected the module's ``repr`` string, code
   relying on ``origin`` for resource location could previously
   encounter errors. (Fixed in 2.6.1 already.)

-  **Multidist:** Ensured created binaries use the name they were
   launched with, rather than the path of the actual binary file.

   This allows entry points invoked via ``subprocess`` with different
   process names to function correctly from a single binary
   distribution. (Fixed in 2.6.1 already.)

-  **Windows:** Fixed unusable ``sys.stdin`` when attaching to a console
   (``--windows-console-mode=attach``) without an active terminal, which
   previously led to errors when forking processes. (Fixed in 2.6.1
   already.)

-  **Modules:** Prevented crashes in module mode when encountering
   potentially optimizable ``importlib`` distribution calls that are
   non-optimizable in this mode. (Fixed in 2.6.1 already.)

-  **Python3:** Resolved errors with newer ``setuptools`` versions
   caused by namespace packages not providing a ``path_finder``. (Fixed
   in 2.6.1 already.)

-  **Windows:** Removed a UTF-8 comment from a C header file that could
   prevent MSVC from compiling correctly in certain system locales.
   (Fixed in 2.6.2 already.)

-  **Standalone:** Ensured that user-inhibited data files have their
   associated tags cleared to prevent confusion in plugins. (Fixed in
   2.6.2 already.)

-  **Standalone:** Corrected ``pkgutil.iter_modules`` to prevent
   incomplete module listings.

   Previously, if a package directory existed, Python's file finder
   could interfere, yielding incomplete results that excluded compiled
   modules. (Fixed in 2.6.2 already.)

-  **Windows:** Addressed a C compiler warning related to onefile
   compression on 32-bit Windows during bootstrap compilation.

-  **Python3.12+:** Resolved a ``SystemError`` when accessing the
   ``module`` attribute of ``type`` variables.

-  **Metadata:** Handled cases where reading record data from
   distribution files might fail because the files do not always exist.
   (Fixed in 2.6.3 already.)

-  **Compatibility:** Fixed dependency resolution for shared libraries
   that are symbolic links on non-Windows platforms.

   Resolution failed if dependencies originated from the symlink target
   and that target was not in the system library path or nearby as
   another symlink. (Fixed in 2.6.3 already.)

-  **Standalone:** Prevented the use of ``msvcp140.dll`` from
   ``PySide6`` (specifically ``shiboken6``) by other packages to avoid
   potential compatibility crashes. (Fixed in 2.6.3 already.)

-  **Standalone:** Fixed ``.pyi`` file parsing failures caused by
   comments appearing after ``import`` statements. (Fixed in 2.6.3
   already.)

-  **UI:** Corrected the output of DLL and EXE listings, which no longer
   provided the correct sub-folder information. (Fixed in 2.6.3
   already.)

-  **macOS:** Restored the attachment of icons to application bundles.
   (Fixed in 2.6.3 already.)

-  **Onefile:** Resolved a C compiler warning on 32-bit Windows related
   to missing type conversion for the decompression buffer size. (Fixed
   in 2.6.3 already.)

-  **Python3.12+:** Ensured type aliases have a usable ``module``
   attribute containing the correct module name. (Fixed in 2.6.3
   already.)

-  **Python3.12+:** Improved compatibility for type alias values.

   Corrected the creation process for compound type aliases, resolving
   errors in libraries like ``pydantic`` when used in schemas. (Fixed in
   2.6.5 already.)

-  **Python3.12+:** Implemented a workaround for extension modules
   failing to set the correct package context, which previously caused
   significant compatibility issues (e.g., namespace collisions).

   This was particularly problematic when static libpython was
   unavailable (common on Windows and official macOS CPython). The
   workaround involves saving/restoring the module context and
   correcting potentially wrongly named sub-modules created during
   extension module loading.

   This improves compatibility for packages like ``PySide6QtAds``,
   ``onnx``, ``mediapipe``, ``paddleocr``, and newer ``scipy`` versions,
   which were previously affected. (Fixed in 2.6.6 already.)

-  **Plugins:** Prevented a crash in the Nuitka Package Configuration
   helper function ``get_data`` when falling back to ``pkgutil`` for
   data files not found naively. (Fixed in 2.6.6 already.)

-  **Standalone:** Corrected the rpath value used for finding dependent
   DLLs in sub-folders on non-Windows platforms.

   It previously excluded the DLL's own folder (``$ORIGIN``), sometimes
   preventing DLLs from loading. (Fixed in 2.6.7 already.)

-  **Standalone:** Preserved existing ``$ORIGIN``-relative rpaths in
   DLLs on Linux.

   Some PyPI packages rely on these existing paths to reference content
   in other packages; replacing them previously broke these setups.
   (Fixed in 2.6.7 already.)

-  **Standalone:** Now treats shared library dependencies specified with
   paths as implicit rpaths.

   This fixes builds using Python distributions like **Python Build
   Standalone** (installed by ``uv``), which may have an
   ``$ORIGIN``-relative ``libpython`` dependency that needs to be
   respected. (Fixed in 2.6.7 already.)

-  **Python3:** Ensured generators preserve external exceptions and
   restore their own upon resuming.

   This fixes issues where generators used as context managers, handling
   an exception via ``yield``, could prevent an outer ``with`` statement
   from correctly re-raising its own exception. (Fixed in 2.6.7
   already.)

-  **Android:** Removed the Termux ``rpath`` value pointing into its
   installation from standalone builds.

   While ineffective after APK packaging due to Android security, this
   value should not have been present. (Fixed in 2.6.7 already.)

-  **Python Build Standalone:** Added the rpath to ``libpython`` by
   default in all modes for **Python Build Standalone** distributions.

   This resolves issues with uninstalled ``libpython`` on **Linux**.
   (Fixed in 2.6.8 already.)

-  **Standalone:** Resolved incompatibility with older Linux
   distributions caused by using newer ``patchelf`` options introduced
   in 2.6.8's rpath changes. (Fixed in 2.6.9 already.)

-  **Python3.9:** Fixed errors in the ``spacy`` plugin when using older
   ``importlib.metadata`` versions. (Fixed in 2.6.8 already.)

-  **Standalone:** Prevented ``requests`` package imports from being
   incorrectly treated as sub-packages. (Fixed in 2.6.8 already.)

-  **Distutils on macOS:** Improved integration for scanned extension
   modules where determining the correct architecture can be difficult.
   (Fixed in 2.6.8 already.)

-  **Windows:** Defined ``dotnet`` as a dependency to ensure all UI
   features requiring it are properly enabled.

-  **Scons:** Ensured the correct ``link.exe`` executable is used for
   the MSVC backend, avoiding potential conflicts with linkers added to
   the ``PATH`` (e.g., by ``git``). (Fixed in 2.6.9 already.)

-  **Scons:** Avoided using ``config.txt`` with ``clcache`` when using
   MSVC.

   This prevents potential race conditions during the first use where
   multiple ``clcache`` threads might attempt to create the file
   simultaneously. (Fixed in 2.6.9 already.)

-  **Standalone:** Ensured extension modules are loaded during the
   ``create_module`` phase of the Nuitka loader for better
   compatibility.

   Loading them later during ``exec_module`` caused issues with some
   extension modules, such as those created by ``mypy`` (used in
   ``black``).

-  **Python3.13:** Corrected the workaround for extension module package
   context issues, resolving errors that occurred when the module and
   package names were identical.

-  **Module:** Prevented stub generation attempts for namespace
   packages, which previously resulted in warnings as there is no source
   code to process.

-  **Debian:** Ensured consistent casing for the installer name used in
   Debian package metadata.

-  **Poetry:** Updated detection logic for newer ``poetry`` versions to
   handle changes in installer name casing, which could previously
   impact system DLL usage determination.

-  **Module:** Improved stub generation (``stubgen``) for generics,
   handling of missing ``typing`` imports, and other cases.

-  **Plugins:** Fixed potential corruption and crashes in the
   ``dill-compat`` plugin when handling functions with keyword defaults.

-  **Standalone:** Added support for newer ``py-cpuinfo`` versions on
   non-Windows platforms.

-  **Accelerated:** Prevented Nuitka's ``sys.path_hook`` from overriding
   standard Python path loader hooks, as it doesn't yet support all
   their functionalities.

-  **Python3.12.7+:** Set additional unicode immortal attributes
   (including for non-attributes) to prevent triggering Python core
   assertions when enabled.

-  **Compatibility:** Ensured errors are properly fetched during class
   variable lookups.

   Previously, an error exit could occur without an exception being set,
   leading to crashes when attempting to attach tracebacks.

-  **Python3.13:** Adapted dictionary value creation and copying to
   follow internal layout changes, preventing potential crashes and
   corruption caused by using obsolete Python 3.11/3.12 code.

-  **Scons:** Corrected the default LTO module count calculation to
   refer to the number of compiled modules.

-  **Package:** Ensured namespace parent modules are included in
   compiled packages.

   These were previously missed due to the removal of reliance on
   ``--include-package`` for delayed namespace package handling.

-  **macOS:** Ensured data files included in application bundles are
   also signed.

-  **Windows:** Applied short path conversion to the directory part of
   ``sys.argv[0]`` as well.

   This prevents issues with tools called using this path that might not
   handle non-shortened (potentially unicode) paths correctly.

*****************
 Package Support
*****************

-  **Standalone:** Included necessary data files for the ``blib2to3``
   package. (Added in 2.6.1 already.)

-  **Standalone:** Added support for newer ``numba`` versions. (Added in
   2.6.2 already.)

-  **Standalone:** Added support for newer ``huggingface_hub`` versions.
   (Added in 2.6.2 already.)

-  **Anti-Bloat:** Provided additional ``numpy.testing`` stubs required
   for proper execution of some ``sklearn`` modules. (Fixed in 2.6.2
   already.)

-  **Standalone:** Enhanced configuration for ``fontTools``. Avoided
   configuring hidden dependencies now detected by parsing provided
   Python files like ``.pyi`` files. (Fixed in 2.6.2 already.)

-  **Standalone:** Corrected plugin configuration for newer ``PySide6``
   ``sqldrivers`` on macOS. (Fixed in 2.6.3 already.)

-  **Python3.12+:** Introduced standalone support for ``mediapipe``,
   including a workaround for extension module sub-module creation
   issues. (Fixed in 2.6.3 already.)

-  **Python3.12+:** Introduced standalone support for ``onnx``,
   including a workaround for extension module sub-module creation
   issues. (Fixed in 2.6.3 already.)

-  **Standalone:** Added support for newer ``sqlglot`` versions. (Added
   in 2.6.5 already.)

-  **Standalone:** Included ``asset`` data files for the ``arcade``
   package. (Added in 2.6.5 already.)

-  **Standalone:** Added implicit dependencies for ``sqlalchemy.orm``.
   (Added in 2.6.5 already.)

-  **macOS:** Included additional frameworks required for PySide 6.8
   web-engine support. (Added in 2.6.5 already.)

-  **Standalone:** Enhanced ``cv2`` support to handle potentially Python
   minor version-specific config files by allowing optional data file
   discovery in plugins. (Added in 2.6.6 already.)

-  **Standalone:** Added support for the ``scipy`` sub-module loader
   mechanism.

   By treating it as a lazy loader, implicit dependencies within
   ``scipy`` are now correctly detected without requiring explicit
   configuration. (Added in 2.6.7 already.)

-  **Standalone:** Automatically include Django database engine modules.
   (Added in 2.6.7 already.)

-  **Homebrew:** Added ``tk-inter`` support for Python versions using
   **Tcl/Tk** version 9.

-  **Standalone:** Included a missing data file for the ``jenn``
   package.

-  **Standalone:** Added support for newer ``scipy.optimize._cobyla``
   versions. (Fixed in 2.6.8 already.)

-  **Anaconda:** Fixed issues with bare ``mkl`` usage (without
   ``numpy``).

-  **Standalone:** Included a missing data file for the ``cyclonedx``
   package.

-  **Compatibility:** Enabled pickling of local compiled functions using
   ``cloudpickle`` and ``ray.cloudpickle``.

-  **Standalone:** Added support for ``mitmproxy`` on macOS.

-  **Standalone:** Included necessary data files for ``python-docs`` and
   ``mne``.

-  **Standalone:** Added support for newer ``toga`` versions, requiring
   handling of its lazy loader.

-  **Standalone:** Introduced support for the ``black`` code formatter
   package.

-  **Standalone:** Included metadata when the ``travertino`` package is
   used.

-  **Standalone:** Significantly enhanced support for detecting
   dependencies derived from ``django`` settings.

-  **Standalone:** Added support for the ``duckdb`` package.

**************
 New Features
**************

-  **DLL Mode:** Introduced a new experimental mode (``--mode=dll``) to
   create standalone DLL distributions.

   While functional for many cases, documentation is currently limited,
   and features like multiprocessing require further work involving
   interaction with the launching binary.

   This mode is intended to improve Windows GUI compatibility (tray
   icons, notifications) for onefile applications by utilizing an
   internal DLL structure.

-  **Windows:** Onefile mode now internally uses the new DLL mode by
   default, interacting with a DLL instead of an executable in temporary
   mode.

   Use ``--onefile-no-dll`` to revert to the previous behavior if issues
   arise.

-  **Windows:** Added support for dependency analysis on Windows ARM
   builds using ``pefile`` (as Dependency Walker lacks ARM support).

-  **Android:** Enabled module mode support when using Termux Python.
   (Added in 2.6.7 already.)

-  **Compatibility:** Added support for **Python Build Standalone**
   distributions (e.g., as downloaded by ``uv``).

   Note that static ``libpython`` is not supported with these
   distributions as the included static library is currently unusable.
   (Added in 2.6.7 already.)

-  **Windows:** Enabled taskbar grouping for compiled applications if
   product and company names are provided in the version information.
   (Added in 2.6.4 already.)

-  **Windows:** Automatically use icons provided via
   ``--windows-icon-from-ico`` for ``PySide6`` applications.

   This eliminates the need to separately provide the icon as a PNG
   file, avoiding duplication.

-  **Nuitka Package Configuration:** Allowed using values from
   ``constants`` and ``variable`` declarations within ``when``
   conditions where feasible.

-  **Reports:** Clearly indicate if an included package is "vendored"
   (e.g., packages bundled within ``setuptools``).

-  **Compatibility:** Added support for the ``safe_path`` (``-P``)
   Python flag, preventing the use of the current directory in module
   searches.

-  **Compatibility:** Added support for the ``dont_write_bytecode``
   (``-B``) Python flag, disabling the writing of ``.pyc`` files at
   runtime (primarily for debugging purposes, as compiled code doesn't
   generate them).

-  **UI:** Introduced a new experimental tool for scanning distribution
   metadata, producing output similar to ``pip list -v``. Intended for
   debugging metadata scan results.

-  **Plugins:** Enhanced the ``dill-compat`` plugin to transfer
   ``__annotations__`` and ``__qualname__``.

   Added an option to control whether the plugin should also handle
   ``cloudpickle`` and ``ray.cloudpickle``.

-  **AIX:** Implemented initial enhancements towards enabling Nuitka
   usage on AIX, although further work is required.

**************
 Optimization
**************

-  Optimized finalizer handling in compiled generators, coroutines, and
   asyncgens by avoiding slower C API calls introduced in 2.6, restoring
   performance for these objects.

-  Implemented a more compact encoding for empty strings in data blobs.

   Instead of 2 bytes (unicode) + null terminator, a dedicated type
   indicator reduces this frequent value to a single byte.

************
 Anti-Bloat
************

-  Avoided including ``matplotlib`` when used by the ``tqdm`` package.
   (Added in 2.6.2 already.)

-  Avoided including ``matplotlib`` when used by the ``scipy`` package.
   (Added in 2.6.2 already.)

-  Avoided including ``cython`` when used by the ``fontTools`` package.
   (Added in 2.6.2 already.)

-  Avoided including ``sparse`` when used by the ``scipy`` package.
   (Added in 2.6.3 already.)

-  Avoided including ``ndonnx`` when used by the ``scipy`` package.
   (Added in 2.6.3 already.)

-  Avoided including ``setuptools`` for the ``jaxlib`` package.

   Also prevented attempts to query the version from ``jaxlib`` source
   code using git. (Added in 2.6.3 already.)

-  Avoided including ``yaml`` when used by the ``scipy`` package. (Added
   in 2.6.4 already.)

-  Avoided including ``charset_normalizer`` for the ``numpy`` package.
   (Added in 2.6.5 already.)

-  Avoided including ``lxml`` for the ``pandas`` package. (Added in
   2.6.5 already.)

-  Avoided including ``PIL`` (Pillow) for the ``sklearn`` package.
   (Added in 2.6.5 already.)

-  Avoided including ``numba`` when used by the ``smt`` package. (Added
   in 2.6.7 already.)

-  Avoided including more optional ``pygame`` dependencies. (Added in
   2.6.8 already.)

-  Avoided including ``setuptools``, ``tomli``, and ``tomllib`` for the
   ``incremental`` package.

-  Avoided including ``IPython`` when used by the ``rich`` package
   vendored within ``pip``.

-  For reporting purposes, treated usage of ``ipywidgets`` as equivalent
   to using ``IPython``.

-  Added support for ``assert_raises`` within Nuitka's ``numpy.testing``
   stub.

****************
 Organizational
****************

-  **UI:** Improved the output format for used command line options.

   Filenames provided as positional arguments now use the report path
   format. Info traces now support an optional leader for intended value
   output, enhancing readability.

-  **Reports:** Saved and restored timing information for cached
   modules.

   This eliminates timing differences based on whether a module was
   loaded from cache, reducing noise in **Nuitka-Watch** comparisons
   where cached module timings previously changed with every new
   compilation.

-  **Actions:** Added compilation report artifacts to all CI runs
   involving empty module compilations.

-  **Debugging:** Enabled the ``--edit`` option to find modules within
   ``.app`` bundles created on macOS. (Added in 2.6.1 already.)

-  **User Manual:** Updated the Nuitka-Action example; linking directly
   to its documentation might be preferable. (Changed in 2.6.1 already.)

-  **Quality:** Enforced ASCII encoding for all Nuitka C files to
   prevent accidental inclusion of non-ASCII characters.

-  **Quality:** Added syntax validation for ``global_replacements``
   result values, similar to existing checks for ``replacements``.

   Also added validation to ensure ``global_replacements_re`` and
   ``replacements_re`` result values are valid regular expressions.

-  **Plugins:** Ensured error messages for illegal module names in
   implicit imports correctly report the originating plugin name.

-  **Quality:** Enabled use of ``clang-format-21`` if available and
   applied formatting changes specific to this newer version.

-  **Quality:** Suppressed ``pylint`` warnings related to ``setuptools``
   usage when running with Python 3.12+.

-  **UI:** Disallowed mixed usage of Anaconda and Poetry *without* an
   active Poetry virtual environment.

   This avoids issues caused by a Poetry bug where it incorrectly sets
   the ``INSTALLER`` metadata for Conda packages in this scenario,
   making reliable detection of Conda packages impossible.

-  **macOS:** Deprecated ``--macos-target-arch`` in favor of the
   standard ``--target-arch`` option, with plans for eventual removal.

-  **Release:** Ensured usage of a compatible ``setuptools`` version
   during ``osc`` uploads.

-  **UI:** Improved the error message for invalid custom anti-bloat
   modes by listing the allowed values.

-  **Release:** Removed CPython test git submodules from the repository.

   These submodules caused issues, such as being cloned during ``pip
   install`` and sometimes failing, potentially breaking Nuitka
   installation.

*******
 Tests
*******

-  Enabled passing extra options via the ``NUITKA_EXTRA_OPTIONS``
   environment variable for ``distutils`` test cases involving
   ``pyproject.toml``.

-  Removed the standalone test for the ``gi`` package, as it's better
   covered by Nuitka-Watch and prone to failures in CI due to lack of an
   X11 display.

-  Ensured tests correctly ignore the current directory when necessary
   by using the new ``--python-flag=safe_path``.

   This forces the use of the original source code as intended, rather
   than potentially finding modules in the current directory.

-  Corrected the implementation of the ``retry`` mechanism for
   ``pipenv`` installation within the ``nuitka-watch`` tool.

-  Added support for passing extra options via environment variables to
   the ``nuitka-watch`` tool.

**********
 Cleanups
**********

-  **Distutils:** Standardized usage to ``--module=package`` where
   appropriate, instead of manually adding package contents, resulting
   in more conventional Nuitka command lines.

-  Refactored ``.pyi`` file creation into a dedicated function,
   simplifying the post-processing code.

*********
 Summary
*********

This release was supposed to focus on scalability, but that didn't
happen due to a variety of important issues coming up as well as
unplanned private difficulties.

The added DLL mode will be very interesting to many users, but needs
more polish in future releases.

For compatibility, working with the popular (yet - not yes recommended
**UV-Python**), **Windows** UI fixes for temporary onefile and **macOS**
improvements, as well as improved **Android** support are excellent.

The next release of Nuitka however will have to focus on scalability and
maintenance only. But as usual, not sure if it can happen.
