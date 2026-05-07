:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.1rc11**.

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

-  **Python 3.14:** Fix, decorators were breaking when disabling
   deferred annotations. (Fixed in 4.0.1 already.)

-  Fix, nested loops could have wrong traces lead to mis-optimization.
   (Fixed in 4.0.1 already.)

-  **Plugins:** Fix, run-time check of package configuration was
   incorrect. (Fixed in 4.0.1 already.)

-  **Compatibility:** Fix, ``__builtins__`` lacked necessary
   compatibility in compiled functions. (Fixed in 4.0.1 already.)

-  **Distutils:** Fix, incorrect UTF-8 decoding was used for TOML input
   file parsing. (Fixed in 4.0.1 already.)

-  Fix, multiple hard value assignments could cause compile time
   crashes. (Fixed in 4.0.1 already.)

-  Fix, string concatenation was not properly annotating exception
   exits. (Fixed in 4.0.2 already.)

-  **Windows:** Fix, ``--verbose-output`` and ``--show-modules-output``
   did not work with forward slashes. (Fixed in 4.0.2 already.)

-  **Python 3.14:** Fix, there were various compatibility issues
   including dictionary watchers and inline values. (Fixed in 4.0.2
   already.)

-  **Python 3.14:** Fix, stack pointer initialization to ``localsplus``
   was incorrect to avoid garbage collection issues. (Fixed in 4.0.2
   already.)

-  **Python 3.12+:** Fix, generic type variable scoping in classes was
   incorrect. (Fixed in 4.0.2 already.)

-  **Python 3.12+:** Fix, there were various issues with function
   generics. (Fixed in 4.0.2 already.)

-  **Python 3.8+:** Fix, names in named expressions were not mangled.
   (Fixed in 4.0.2 already.)

-  **Plugins:** Fix, module checksums were not robust against quoting
   style of module-name entry in YAML configurations. (Fixed in 4.0.2
   already.)

-  **Plugins:** Fix, doing imports in queried expressions caused
   corruption. (Fixed in 4.0.2 already.)

-  **UI:** Fix, support for ``uv_build`` in the ``--project`` option was
   broken. (Fixed in 4.0.2 already.)

-  **Compatibility:** Fix, names assigned in assignment expressions were
   not mangled. (Fixed in 4.0.2 already.)

-  **Python 3.12+:** Fix, there were still various issues with function
   generics. (Fixed in 4.0.3 already.)

-  **Clang:** Fix, debug mode was disabled for clang generally, but only
   ClangCL and macOS Clang didn't want it. (Fixed in 4.0.3 already.)

-  **Zig:** Fix, ``--windows-console-mode=attach|disable`` was not
   working when using Zig. (Fixed in 4.0.3 already.)

-  **macOS:** Fix, yet another way self dependencies can look like,
   needed to have support added. (Fixed in 4.0.3 already.)

-  **Python 3.12+:** Fix, generic types in classes had bugs with
   multiple type variables. (Fixed in 4.0.3 already.)

-  **Scons:** Fix, repeated builds were not producing binary identical
   results. (Fixed in 4.0.3 already.)

-  **Scons:** Fix, compiling with newer Python versions did not fall
   back to Zig when the developer prompt MSVC was unusable, and error
   reporting could crash. (Fixed in 4.0.4 already.)

-  **Zig:** Fix, the workaround for Windows console mode ``attach`` or
   ``disable`` was incorrectly applied on non-Windows platforms. (Fixed
   in 4.0.4 already.)

-  **Standalone:** Fix, linking with Python Build Standalone failed
   because ``libHacl_Hash_SHA2`` was not filtered out unconditionally.
   (Fixed in 4.0.4 already.)

-  **Python 3.6+:** Fix, exceptions like ``CancelledError`` thrown into
   an async generator awaiting an inner awaitable could be swallowed,
   causing crashes. (Fixed in 4.0.4 already.)

-  Fix, not all ordered set modules accepted generators for update.
   (Fixed in 4.0.5 already.)

-  **Plugins:** Disabled warning about rebuilding the ``pytokens``
   extension module. (Fixed in 4.0.5 already.)

-  **Standalone:** Filtered ``libHacl_Hash_SHA2`` from link libs
   unconditionally. (Fixed in 4.0.5 already.)

-  **Debugging:** Disabled unusable unicode consistency checks for
   Python versions 3.4 to 3.6. (Fixed in 4.0.5 already.)

-  **Python3.12+** Avoided cloning call nodes on class level which
   caused issues with generic functions in combination with decorators.
   (Added in 4.0.5 already.)

-  **Python 3.12+:** Added support for generic type variables in ``async
   def`` functions. (Added in 4.0.5 already.)

-  **UI:** Fix, flushing outputs for prompts was not working in all
   cases when progress bars were enabled. (Fixed in 4.0.6 already.)

-  **UI:** Fix, unused variable warnings were missing at C compile time
   when using ``zig`` as a C compiler. (Fixed in 4.0.6 already.)

-  **Scons:** Fix, forced stdout and stderr paths as a feature was
   broken. (Fixed in 4.0.6 already.)

-  Fix, replacing a branch did not accurately track shared active
   variables causing optimization crashes. (Fixed in 4.0.7 already.)

-  **macOS:** Fix, failed to remove extended attributes because files
   need to be made writable first. (Fixed in 4.0.7 already.)

-  Fix, dict ``pop`` and ``setdefault`` using with ``:=`` rewrites
   lacked exception-exit annotations for un-hashable keys. (Fixed in
   4.0.8 already.)

-  **Python 3.13:** Fix, the ``__parameters__`` attribute of generic
   classes was not working. (Fixed in 4.0.8 already.)

-  **Python 3.11+:** Fix, starred arguments were not working as type
   variables. (Fixed in 4.0.8 already.)

-  **Python2:** Fix, ``FileNotFoundError`` compatibility fallback
   handling was not working properly. (Fixed in 4.0.8 already.)

-  **Compatibility:** Fix, loop ownership check in value traces was
   missing, causing issues with nested loops.

-  **Windows:** Improved ``--windows-console-mode=attach`` to properly
   handle console handles, enabling cases like ``os.system`` to work
   nicely.

-  **Python2:** Fix, there was a compatibility issue where providing
   default values to the ``mkdtemp`` function was failing.

-  **Windows:** Fix, there were spurious issues with C23 embedding in
   32-bit MinGW64 by switching to ``coff_obj`` resource mode for it as
   well.

-  **Plugins:** Fix, the ``post-import-code`` execution could fail
   because the triggering sub-package was not yet available in
   ``sys.modules``.

-  **UI:** Fix, listing package DLLs with ``--list-package-dlls`` was
   broken due to recent plugin lifecycle changes.

-  **UI:** Fix, ``--list-package-exe`` was not working properly on
   non-Windows platforms failing to detect executable files correctly.

-  **UI:** Handled paths starting with ``{PROGRAM_DIR}`` the same as a
   relative path when parsing the ``--onefile-tempdir-spec`` option.

-  **Plugins:** Followed multiprocessing ``forkserver`` changes for
   newer Python versions.

-  **Python 3.12+:** Fix, generic class type parameters handling was
   incorrect.

-  **Python 3.12:** Fix, deferred evaluation of type aliases was
   failing.

-  **Python 3.12+:** Aligned ``sum`` built-in float summation with
   CPython's compensated sum for better accuracy.

-  **Python 3.10+:** Fix, uncompiled coroutine ``throw()`` return
   handling was incorrect, restoring completed coroutine results via
   ``StopIteration.value`` rather than exposing them as ordinary return
   values to the outer await chain.

-  **Python 3.13+:** Fix, uncompiled coroutine ``cancel()/await``
   suspension handling was incorrect, improved to ensure integration
   compatibility.

-  **macOS:** Made finding ``create-dmg`` more robustly by also checking
   the Homebrew path for Intel and from ``PATH`` properly.

-  **Compatibility:** Fix, class frames were not exposing frame locals.

-  **UI:** Detected ``static-libpython`` problems, which affected some
   forms of Anaconda.

-  **Distutils:** Rejected ``--project`` mixed with ``--main`` arguments
   as it is not useful.

-  **macOS:** Fix, ``zig`` from ``PATH`` or from ``ziglang`` was not
   being used.

-  **Distutils:** Fix, the wrong ``module-root`` config value was being
   checked for ``uv`` build backend.

-  **macOS:** Fix, was attempting to change removed (rejected) DLLs,
   which of course failed and errored out.

-  **Python 3.14:** Fix, tuple reuse was not fully compatible,
   potentially causing crashes due to outdated hash caches.

-  Fix, fake modules were still being attempted to located when imported
   by other code, which could conflict with existing modules.

-  **Python 3.5+:** Fix, failed to send uncompiled coroutines the sent
   in value in ``yield from``.

-  Fix, older ``gcc`` compilers lacking newer intrinsic methods had
   compilation issues that needed to be addressed.

-  **Standalone:** Fix, multiphase module extension modules with
   post-load code were not working properly.

-  Fix, Avoid using the non-inline copy of ``pkg_resources`` with the
   inline copy of Jinja2. These could mismatch and cause errors.

-  Fix, loops could make releasing of previous values very unclear,
   causing optimization errors.

-  Fix, ``incbin`` resource mode was not working with old ``gcc`` C++
   fallback.

-  **Python 3.4 to 3.6:** Fix, bytecode demotion was not working
   properly for these versions, also bytecode only files not working.

-  **Plugins:** Added a check for the broken ``patchelf`` versions 0.10
   and 0.11 to prevent breaking Qt plugins.

-  **Android:** Allowed ``patchelf`` version 0.18 on Android.

-  **Windows:** Fix, the header path for self uninstalled Python was not
   detected correctly.

-  **Release:** Fix, inclusion of the ``pkg_resources`` inline copy for
   Python 2 to source distributions was missing.

-  **UI:** Detected the OBS versions of SUSE Linux better.

-  **Suse:** Allowed using ``patchelf`` 0.18.0 there too.

-  **Python 3.11:** Fix, package and module dicts were not aligned close
   enough to avoid a CPython bug.

-  Fix, unbound compiled methods could crash when called without an
   object passed.

-  **Standalone:** Fix, multiphase module extension modules with
   postload. (Fixed in 4.0.8 already.)

-  **Onefile:** Fix, while waiting for the child, it may already be
   terminated.

-  **macOS:** Removed existing absolute rpaths for Homebrew and
   MacPorts.

-  **Python 3.14:** Avoided warning in CPython headers.

-  **Python 3.14:** Followed allocator changes more closely.

-  **Compatibility:** Avoided using ``pkg_resources`` for Jinja2
   template location for loading.

-  **No-GIL:** Applied some bug fixes to get basic things to work.

Package Support
===============

-  **Standalone:** Add support for newer ``paddle`` version. (Added in
   4.0.1 already.)

-  **Standalone:** Add workaround for refcount checks of ``pandas``.
   (Fixed in 4.0.1 already.)

-  **Standalone:** Add support for newer ``h5py`` version. (Added in
   4.0.2 already.)

-  **Standalone:** Add support for newer ``scipy`` package. (Added in
   4.0.2 already.)

-  **Plugins:** Revert accidental ``os.getenv`` over ``os.environ.get``
   changes in anti-bloat configurations that stopped them from working.
   Affected packages are ``networkx``, ``persistent``, and
   ``tensorflow``. (Fixed in 4.0.5 already.)

-  **Standalone:** Added missing DLLs for ``openvino``. (Added in 4.0.7
   already.)

-  Enhanced the package configuration YAML schema by adding the
   ``relative_to`` parameter for ``from_filenames`` DLL specification,
   avoiding error-prone purely relative paths.

-  **Standalone:** Fix, ``flet_desktop`` app assets were missing, now
   preserving the packaged runtime and sidecar DLLs.

-  **Standalone:** Added support for the ``tyro`` package.

-  **Standalone:** Added data files for the ``perfetto`` package.

-  **Standalone:** Added support for ``anyio`` process forking.

-  **Standalone:** Added support for the ``plotly.graph`` package.

-  **Anaconda:** Fix, dependencies for the ``numpy`` conda package on
   Windows were incorrect.

-  **Plugins:** Enhanced the auto-icon hack in PySide6 to use compatible
   class names.

-  **Standalone:** Fix, Qt libraries were duplicated with ``PySide6``
   WebEngine framework support on macOS.

-  **Plugins:** Fix, automatic detection of ``mypyc`` runtime
   dependencies was including all top level modules of the containing
   package by accident. (Fixed in 4.0.5 already.)

-  **Anaconda:** Fix, ``delvewheel`` plugin was not working with Python
   3.8+. This enhances compatibility with installed PyPI packages that
   use it for their DLLs. (Fixed in 4.0.6 already.)

-  **Plugins:** Fix, our protection workaround could confuse methods
   used with ``PySide6``.

New Features
============

-  **UI:** Added the ``--recommended-python-version`` option to display
   recommended Python versions for supported, working, or commercial
   usage.

-  **UI:** Add message to inform users about ``Nuitka[onefile]`` if
   compression is not installed. (Added in 4.0.1 already.)

-  **UI:** Add support for ``uv_build`` in the ``--project`` option.
   (Added in 4.0.1 already.)

-  **Onefile:** Allow extra includes as well. (Added in 4.0.2 already.)

-  **UI:** Add ``nuitka-project-set`` feature to define project
   variables, checking for collisions with reserved runtime variables.
   (Added in 4.0.2 already.)

-  **Scons:** Added new option to select ``--reproducible`` builds or
   not. (Added in 4.0.6 already.)

-  **Python 3.10+:** Added support for
   ``importlib.metadata.package_distributions()``. (Added in 4.0.8
   already.)

-  **Plugins:** Added support for the multiprocessing ``forkserver``
   context. (Added in 4.0.8 already, for 4.1 Python 3.6 and earlier, as
   well as 3.14 support were added too.)

-  **Reports:** Added structured resource usage (``rusage``) performance
   information to compilation reports.

-  **Reports:** Included individual module-level C compiler caching
   (``ccache``/``clcache``) statistics in compilation reports.

-  Added support for detecting and correctly resolving the Python prefix
   for the ``PyEnv on Homebrew`` Python flavor.

-  **macOS:** Added support for ``rusage`` information for Scons.

-  **UI:** Added the ``__compiled__.extension_filename`` attribute to
   give the real filename of the containing extension module.

-  **Windows:** Added support for ``--clang`` or ARM. (Added in 4.0.8
   already.)

-  **Windows:** Added support for resources names as not just integers,
   important when we copy them from template files.

-  **MacPorts:** Added basic support for this Python flavor. More work
   will be needed to get it to work fully though.

Optimization
============

-  Avoid including ``importlib._bootstrap`` and
   ``importlib._bootstrap_external``. (Added in 4.0.1 already.)

-  **Linux:** Cached the ``syscall`` used for time keeping during
   compilation to avoid loading ``libc`` for each trace. (Added in 4.0.8
   already.)

-  **UI:** Output a warning for modules that remain unfinished after the
   third optimization pass.

-  Added an extra micro pass trigger when new variables are introduced
   or variable usage changes severely, ensuring optimizations are fully
   propagated, avoiding unnecessary extra full passes.

-  Provided scripts to compile Python statically with PGO tailored for
   Nuitka on Linux, Windows, and macOS.

-  Added support for running the Data Composer tool from a compiled
   Nuitka binary without spawning an uncompiled Python process.

-  Enhanced the usage of ``vectorcall`` for ``PyCFunction`` objects by
   directly checking for its presence instead of relying purely on
   flags, allowing more frequent use of this faster execution path.

-  Cached frequently used declarations for top-level variables to speed
   up C code generation.

-  Sped up trace collection merging by avoiding unnecessary set creation
   and using a set instead of a list for escaped traces.

-  Optimized plugin hook execution by tracking overloaded methods and
   added an option to show plugin usage statistics.

-  Improved performance of module location by avoiding unnecessary
   module name reconstruction and redundant filesystem checks for
   pre-loaded packages.

-  Improved the caching of distribution name lookups to effectively
   avoid repeated IO operations across all package types.

-  **Plugins:** Cached callback plugin dispatch for
   ``onFunctionBodyParsing`` and ``onClassBodyParsing`` to skip argument
   computation when no plugin overrides them.

-  **Python 3.13:** Handled sub-packages of ``pathlib`` as hard modules.

-  Handled hard attributes through merge traces as well.

-  Made constant blobs more compact by avoiding repeated identifiers and
   unnecessary fields.

-  Enhanced Python compilation scripts further. (Fixed in 4.0.8
   already.)

-  Recognized late incomplete variables better. (Fixed in 4.0.8
   already.)

-  Made constant blobs more compact. (Fixed in 4.0.8 already.)

-  Optimized calls with only constant keywords and variable posargs too.

Anti-Bloat
==========

-  Fix, memory bloat occurred when C compiling ``sqlalchemy``. (Fixed in
   4.0.2 already.)

-  Avoid using ``pydoc`` in ``PySimpleGUI``. (Added in 4.0.2 already.)

-  Avoided using ``doctest`` from ``zodbpickle``. (Added in 4.0.5
   already.)

-  Avoided inclusion of ``cython`` when using ``pyav``. (Added in 4.0.7
   already.)

-  Avoided including ``typing_extensions`` when using ``numpy``. (Added
   in 4.0.7 already.)

Organizational
==============

-  **UI:** Relocated the warning about the available source code of
   extension modules to be evaluated at a more appropriate time.

-  **Debian:** Remove recommendation for ``libfuse2`` package as it is
   no longer useful.

-  **Debian:** Used ``platformdirs`` instead of ``appdirs``.

-  **Debugging:** Removed Python 3.11+ restriction for ``clang-format``
   as it is available everywhere, even Python 2.7, and we still want
   nicely formatted code when we read things. (Added in 4.0.6 already.)

-  Removed no longer useful inline copy of ``wax_off``. We have our own
   stubs generator project.

-  **Release:** Added missing package to the CI container for building
   Nuitka Debian packages.

-  **Developer:** Updated AI instructions for creating Minimal
   Reproducible Examples (MRE) to skip unneeded C compilation.

-  **Debugging:** Added an internal function for checking if a string is
   a valid Python identifier.

-  **AI:** Added a task in Visual Studio Code to export the currently
   selected Python interpreter path to a file, making it available as
   "python" and "pip" matching the selected interpreter. This makes it
   easier to use a specific version with no instructions needed.

-  **AI:** Updated the rules to instruct AI to only generate useful
   comments that add context not present in the code.

-  **Containers:** Added template rendering support for Jinja2 (``.j2``)
   container files in our internal Podman tools.

-  **Projects:** Clarified the current status and rationale of Python
   2.6 support in the developer manual.

-  **Debugging:** Added experimental flag
   ``--experimental=ignore-extra-micro-pass`` to allow ignoring extra
   micro pass detection.

-  **Visual Code:** Added integration scripts for ``bash`` and ``zsh``
   autocompletion of Nuitka CLI options. These are now also integrated
   into Visual Studio Code terminal profiles and the Debian package.

-  **RPM:** Included the Python compile script for Linux.

-  **RPM:** Removed the requirement for ``distutils`` in the spec.

Tests
=====

-  Install only necessary build tools for test cases.

-  Avoided spurious failures in reference counting tests due to Python
   internal caching differences. (Fixed in 4.0.3 already.)

-  Fix, the parsing of the compilation report for reflected tests was
   incorrect.

-  **Python 3.14:** Ignored a syntax error message change.

-  **Python 3.14:** Added test execution support options to the main
   test runner to use this version as well.

-  Fix, the runner binary path was mishandled for the third pass of
   reflected compilations.

-  Removed the usage of obsolete plugins in reflected compilation tests.

-  **Debugging:** Prevented boolean testing of ``namedtuples`` to avoid
   unexpected bugs.

-  Added the ``Test`` suffix to syntax test files and disabled "python"
   mode and spell checking for them to resolve issues reported in IDEs.

-  Fix, newline handling in diff outputs from the output comparison tool
   was incorrect.

-  Covered ``post-import-code`` functionality with a new subpackage test
   case.

-  Prevented the program test suite from running an unnecessary variant
   to save execution time.

-  **macOS:** Ignored differences from GUI framework error traces in
   headless runs in output comparisons.

-  Reflected test for Nuitka, where it compiles itself and compares its
   operation has been restored to functional state.

-  Used the new method to clear internal caches if available for
   reference counts.

-  Disabled running nested loops test with Python 2.6.

-  **Containers:** Detected Python 2 defaulting containers in Podman
   tooling.

Cleanups
========

-  **UI:** Fix, there was a double space in the Windows Runtime DLLs
   inclusion message. (Fixed in 4.0.1 already.)

-  **Onefile:** Separated files and defines for extra includes for
   onefile boot and Python build.

-  **Scons:** Provided nicer errors in case of "unset" variables being
   used, so we can tell it.

-  Refactored the process execution results to correctly utilize our
   ``namedtuples`` variant, that makes it easier to understand what code
   does with the results.

-  **Quality:** Enabled automatic conversion of em-dashes and en-dashes
   in code comments to the autoformat tool. AI won't stop producing them
   and they can cause ``SyntaxError`` for older Python versions, nor is
   unnecessarily using UTF-8 welcome.

-  Ensured that cloned outline nodes are assigned their correct names
   immediately upon creation, that avoids inconsistencies during their
   creation.

-  **Quality:** Updated to the latest versions of ``black`` and adopted
   a faster ``isort`` execution by caching results.

-  **Quality:** Modified the PyLint wrapper to exit gracefully instead
   of raising an error when no matching files require checking.

-  **Quality:** Avoided checking YAML package configuration files twice,
   since autoformat already handles them.

-  **Quality:** Ensured that YAML package configuration checks output
   the original filename instead of the temporary one when a failure
   occurs.

-  **Quality:** Prevented pushing of tags from triggering git pre-push
   quality checks.

-  **Quality:** Silenced the output of ``optipng`` and ``jpegoptim``
   during image optimization auto-formatting.

-  **Visual Code:** Added the generated Python alias path file to the
   ignore list.

-  **Quality:** Enabled auto-formatting for the Nuitka devcontainer
   configuration file.

-  **Watch:** Avoided absolute paths in compilation to make reports more
   comparable across machines.

-  **Quality:** Changed ``mdformat`` checks to run only once and
   silently.

-  **Scons:** Disabled format security errors in debug mode and moved
   Python-related warning disables into common build setup code.

-  **Quality:** Updated to the latest ``deepdiff`` version.

-  **Scons:** Avoided MSVC telemetry since it can produce outputs that
   break CI.

-  **Debugging:** Enhanced non-deployment handler for importing excluded
   modules.

-  Split import module finding functionality into more pieces for
   enhanced readability.

-  **Debugging:** Added more assertions for constants loading and
   checking.

-  **macOS:** Dropped the ``universal`` target arch.

-  **Debugging:** Added more traces for deep hash verification.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
