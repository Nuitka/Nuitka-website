:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per-version changes and comments for the
upcoming Nuitka |NUITKA_VERSION_NEXT| as a draft about hot-fixes of the
current stable release as |NUITKA_VERSION| as well.

****************************
 Nuitka Release 2.4 (Draft)
****************************

.. note::

   This a draft of the release notes for 2.4, which is supposed to add
   Python 3.13 beta2 support and the usual additions of new packages
   supported out of the box.

   The main focus shall be scalability and a few open issues for
   performance enhancements that later Python versions enable us to.

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

.. include:: ../dynamic.inc
