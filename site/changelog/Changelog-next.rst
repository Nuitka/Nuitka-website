:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.2rc3**.

**************************************************
 **Nuitka** Release |NUITKA_VERSION_NEXT| (Draft)
**************************************************

.. note::

   These are the draft release notes for the upcoming **Nuitka**
   |NUITKA_VERSION_NEXT| release. A primary goal for this version is to
   deliver significant enhancements in C compilation scalability, and to
   make 3.14 officially supported. Development is ongoing, and this
   documentation might lag slightly behind the latest code changes.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  **Python3:** Fix, nested generators did not make the exception being
   handled in the delegating generator visible to the code they delegate
   to, so ``sys.exc_info()`` gave wrong results there. (Fixed in 4.1.1
   already.)

   .. code:: python

      import sys


      def inner():
          print(sys.exc_info()[0])  # 4.1: None (bug), 4.1.1: KeyError (correct)
          yield 1


      def outer():
          try:
              raise KeyError("caught")
          except KeyError:
              yield from inner()


      next(outer())

-  **Python 3.10+:** Fix, compiled coroutines left the result of their
   send slot uninitialized when they finished by raising, so callers
   like ``asyncio`` could observe garbage values. (Fixed in 4.1.1
   already.)

-  **Python 3.14:** Fix, debug builds in module mode needed handling for
   the reference tracing runtime access, and adapted headers are no
   longer used for MSVC, where the compiler and runtime layouts match.
   (Fixed in 4.1.1 already.)

-  **Python 3.11/3.12:** Fix, optimized class calls bypassing
   ``object_new`` did not initialize the managed dict inline values, so
   the first attribute assignment fell back to a separately allocated
   dictionary, which was non-optimal and caused incompatibility in
   corner cases. (Fixed in 4.1.2 already.)

-  **Python 3.11+:** Fix, compiled frame locals were not stored in the
   interpreter frame ``localsplus`` slots, making them invisible to
   CPython frame introspection. (Fixed in 4.1.2 already.)

-  **Python 3.12+:** Fix, the ``__type_params__`` attribute of generic
   functions was always empty. (Fixed in 4.1.2 already.)

-  **Python 3.14:** Fix, frame locals were cleared too late in the
   deallocator, after the code object and extra locals were already
   released, which could cause crashes. (Fixed in 4.1.2 already.)

-  **Python 3.14:** Fix, type complaint exception messages now use the
   ``__qualname__`` of the offending type, as CPython does. (Fixed in
   4.1.2 already.)

-  **Python 3.14:** Fix, the ``ctypes`` dependency configuration did not
   work in flavors where ``_ctypes`` is a built-in module rather than an
   extension module. (Fixed in 4.1.3 already.)

-  **Python 3.12+:** Fix, the ``has_builtin_module`` helper of Nuitka
   package configuration did not return a boolean value, which could
   break conditional configuration. (Fixed in 4.1.3 already.)

-  **Standalone:** Fix, standard library path detection for the "Python
   Build Standalone" flavor now considers symlinks in directory
   components. (Fixed in 4.1.2 already.)

-  **Plugins:** Fix, ``mypyc`` runtime detection didn't happen for
   submodules of a package, which affected at least the ``chardet``
   module. (Fixed in 4.1.1 already.)

-  **Windows:** Enables UTF-8 mode for attached consoles, since
   otherwise the CRT runtime could hang or corrupt outputs and inputs.
   (Fixed in 4.1.1 already.)

-  **Windows:** Fix, ``multiprocessing`` was not fully working in
   onefile DLL mode, since spawning needs to point to the outer binary,
   not the DLL. (Fixed in 4.1.1 already.)

-  **Windows:** Fix, memory issue for 32 bit Python onefile compression,
   where parallel zstandard compression ran into memory issues for even
   small files when using multiple threads. (Fixed in 4.1.1 already.)

-  **Windows:** Fix, console attaching did not work for onefile DLL mode
   with runtime DLLs included, since the DLL uses a separate CRT
   instance with uninitialized stdio streams, so Python level output and
   input were not working. (Fixed in 4.1.3 already.)

-  **Windows:** Fix, relative paths for the onefile temp directory
   specification did not work in onefile DLL mode. (Fixed in 4.1.3
   already.)

-  **Windows:** Fix, DLL dependency scanning failed when it encountered
   folders without read permission, these are now ignored. (Fixed in
   4.1.3 already.)

-  **macOS:** Fix, header padding is now also possible for
   ``--mode=dll``, since otherwise ``install_name_tool`` cannot rewrite
   the load paths of the output. (Fixed in 4.1.1 already.)

-  **macOS:** Fix, existing signatures of frameworks were no longer
   copied, as they became invalid after relocation and broke re-signing
   of the binaries. (Fixed in 4.1.1 already.)

-  **macOS:** Fix, now handles another form of self dependency from
   absolute paths. (Fixed in 4.1.1 already.)

-  **macOS:** Fix, detection of statically linked libraries did not
   work, since the ``file`` command output was not used yet, so they
   were treated like dynamic ones, leading to errors. (Fixed in 4.1.2
   already.)

-  **macOS:** Fix, now detects another variation of self dependencies,
   where a less-versioned binary depends on its more versioned self.
   (Fixed in 4.1.2 already.)

-  **Debian:** Fix, ``--disable-ccache`` did not work when the compiler
   binary was a symlink, e.g. from the Debian ``ccache`` package. (Fixed
   in 4.1.2 already.)

-  **Linux:** Fix, large constant blobs could cause linker errors on the
   ``x86_64`` architecture, since the default small code model limits
   code and data to 2GB, now the medium code model is used in that case.
   (Fixed in 4.1.3 already.)

-  **AIX:** Fix, potential memory leak in the ``dladdr`` helper. (Fixed
   in 4.1.3 already.)

-  Fix, no longer depended on ``os.__file__`` for detecting the standard
   library path, since that is not a usable path when Nuitka itself is
   compiled in accelerated mode, now ``types.__file__`` is used instead.

-  Fix, trimming the ``importlib`` bootstrap frames off the traceback on
   error exit now handles missing tracebacks, since very early failures
   can have no traceback at all.

-  Fix, when creating generator, coroutine, and asyncgen objects, the
   assignment of closure variables was not checked for exceptions, so
   such assignments could be wrongly optimized away.

   .. code:: python

      def make(flag):
          if flag:
              raise ValueError

          x = 1

          def gen():
              yield x  # x is a closure variable

          return gen()

      make(True)  # must raise ValueError here

-  Fix, when running a package main module with ``--python-flag=-m``,
   the ``__spec__`` value was ``None``, breaking code that uses it, e.g.
   ``importlib.resources.files()``, now a proper ``ModuleSpec`` is set.

   .. code:: python

      # package_main/__main__.py
      import importlib.resources

      # Running as "python -m package_main", this needs __spec__.
      print(importlib.resources.files("package_main"))

-  Fix, for fixed import modules, accessing a missing import name used
   the attribute lookup and raised ``AttributeError``, now it raises
   ``ImportError`` as CPython does.

-  Fix, fixed imports that failed at runtime could segfault, now the
   failure is handled properly.

-  Fix, the hard import modules ``site``, ``pkg_resources``, and
   ``importlib_resources`` are now treated as possibly raising, since
   they can be broken in broken installs.

-  Fix, file listing no longer crashes on case-insensitive filesystems
   when a directory that needs to be ignored differs in actual case.

-  Fix, the optimization was not fully deterministic, since iterating
   over the set of escapable variables had unstable ordering, causing
   behavior differences between otherwise identical builds.

-  Fix, decoding of localized filenames only copied the bytes, so
   multi-byte characters in paths were not decoded at all. On Linux the
   environment locale is now respected with a UTF-8 fallback, and
   FreeBSD and NetBSD use the macOS UTF-8 handling.

-  **Python 2:** Fix, when Nuitka itself was compiled by Nuitka,
   executing Scons could race on the import lock, since
   ``subprocess.Popen(close_fds=True)`` imports the ``resource`` module
   late, which is now pre-loaded.

-  **Python 2.6:** Fix, ``re.sub(flags=...)`` does not work there, now a
   wrapper is used when flags argument is needed.

-  **Python 3.5:** Fix, now uses ``PyImport_CreateModuleFromInitfunc``
   for the meta path loader.

-  **Python 3.7+:** Fix, the outermost iterator of an async
   comprehension was wrongly awaited, since whether the qualifier is
   async was not checked before wrapping, causing a ``TypeError`` at
   runtime.

   .. code:: python

      import asyncio

      async def source():
          yield 1
          yield 2

      async def main():
          # The outermost iterator of an async comprehension must be
          # a plain iterable, it must not be awaited.
          return [i for x in [1] async for i in source()]

      print(asyncio.run(main()))  # [1, 2], not TypeError

-  **Python 3.8+:** Fix, when ``anext()`` or ``aclose()`` failed with
   "asynchronous generator is already running", the ``asend`` and
   ``athrow`` wrappers were left unclosed, so using them again could
   misbehave.

-  **Python 3.9+:** Fix, generic aliases did not release their values
   when being released, now they do.

-  **Python 3.11+:** Fix, a ``__class_getitem__`` set to ``None`` or a
   non-callable now makes the type non-subscriptable with ``TypeError``
   correctly.

-  **Python 3.12.4+:** Fix, throwing an exception into the ``asend`` or
   ``athrow`` wrappers of an already running async generator was not
   rejected, which could run the generator body concurrently.

-  **Python 3.13+:** Fix, was rejecting clearing of suspended frames in
   general, now only generator-owned suspended frames are rejected, as
   CPython does.

-  **Python 3.13+:** Fix, when adapting header files, an assertion in
   ``pycore_long.h`` referenced a stripped macro, causing link errors in
   debug builds.

-  **Python 3.14:** Fix, now follows the CPython changes in
   ``async``/``await`` error messages and the ``with`` statement
   attribute lookup order.

-  **Python 3.14:** Fix, reference count leaked the ``__annotate__``
   functions, now they are properly released.

-  **Python 3.14.7+:** Fix, the error message for source files with
   encoding issues matches CPython 3.14.7 changes, where the byte
   position is reported relative to the seek point after the encoding
   declaration.

-  **Python 3.15:** Fix, follow ``__cached__`` module attribute removal.

-  **Python 3.15:** Fix, follow the ``TypeVarTuple`` object changes.

-  **Python 3.15:** Fix, follow the changes in duplicate parameter and
   encoding error messages.

-  **Python 3.15:** Fix, follow the complex call argument error message
   changes.

-  **Python 3.15:** Fix, the ``_math_integer`` extension module reports
   its ``__name__`` wrongly as ``math.integer``, which is now worked
   around as well.

-  **Compatibility:** Fix, the ``__builtins__`` value of compiled
   functions is not always a module, but can already be a dict, e.g. for
   functions created with ``exec``, so accessing ``__builtins__`` failed
   in those cases.

   .. code:: python

      import builtins

      namespace = {"__builtins__": vars(builtins)}

      exec(
          """
      def f():
          return 42
      """,
          namespace,
      )

      f = namespace["f"]
      print(f.__builtins__ is vars(builtins))  # must be True

-  **Plugins:** Fix, permission errors during DLL and data file scans
   now give a clear error message pointing at the unreadable directory
   and its likely cause, instead of crashing outright.

-  **Plugins:** Fix, ``replacements_re`` were not really working newline
   neutral.

-  **Plugins:** Fix, now splits comma-separated
   ``--noinclude-qt-plugins`` just like ``--include-qt-plugins``.

-  **Windows:** Fix, the length check for generated C source filenames
   only considered the basename, so long build directory paths could
   exceed the path length limit, now the full path is budgeted and a
   hashed name is used when needed.

-  **Windows:** Fix, removing an environment variable during startup did
   not clear the underlying process environment, so unset variables
   could still be visible to child processes, causing issues with PGO at
   times.

-  **Windows:** Fix, prevented a file handle leak in the pefile-based
   DLL dependency detection, which is used for ARM64 or with
   ``--experimental=force-dependencies-pefile``, since the PE file was
   not closed after use.

-  **MSYS2:** Fix, DLL configuration paths were not normalized, which
   turned them into illegal paths errors during compilation.

-  **macOS:** Fix, now checks for the ``create-dmg`` tool availability
   early during options processing.

-  **macOS:** Fix, dependency scans no longer run into permission
   issues.

-  **macOS:** Fix, no longer crashes at runtime on Chinese app names.

-  **macOS:** Fix, now unlocks the keychain more robustly for CI and ssh
   contexts.

-  **Linux:** Fix, onefile mode now links ``pthread`` explicitly, which
   older Linux versions require, since there ``pthread`` is not yet part
   of ``libc``.

-  **Distutils:** Fix, for ``--project`` the ``tool.nuitka`` options
   were not used.

-  **Distutils:** Fix, using ``--project`` with a project that has no
   name set now gives a clear error message telling where to set it,
   instead of failing later in confusing ways.

-  **Distutils:** Fix, the entry point options now pass the project name
   through, so ``--main-entry-point`` builds derive their output name
   from the project, and the misnamed ``--project-requires`` option was
   renamed.

-  **PGO:** Fix, the Python PGO output is now initialized before the
   meta path loader, since probes during loader setup otherwise wrote to
   an uninitialized file handle and crashed.

-  **PGO:** Fix, executing the compiled binary during Python PGO did not
   work for uninstalled Python, where the execution environment setup
   was missing. It is now executed via a script if necessary, and
   internal ``NUITKA_*`` environment variables are no longer passed to
   it, since they could cause the created binary to fail at runtime.

-  **Onefile:** Fix, memory issues with parallel zstandard compression
   are now avoided on 32 bit Python in general, since the check is based
   on the Python itself rather than the x86 architecture, and Android
   32/64 bit detection was corrected.

-  **Onefile:** Fix, manually sent signals were not forwarded to the
   Python process in onefile mode, and on non-Windows the child process
   was not terminated on them at all. It now distinguishes signals from
   the terminal, forwarding only manually sent ones, terminates the
   child process on non-Windows, and suppresses duplicated ``SIGINT``
   delivery to the child.

-  **Report:** Fix, could crash when writing the report before the build
   directory was created.

-  **Zig:** Fix, need to use the newest ``zig`` on macOS.

-  **Zig:** Fix, produced binaries for the native CPU architecture of
   the compilation machine by default, making them not portable to older
   machines. Nuitka now creates machine portable binaries by default,
   with the new ``--target-arch`` option allowing to select a higher
   baseline ISA for speed.

-  **NoGil:** Fix, frame objects are now owned by the frame object
   rather than the generator.

-  **NoGil:** Fix, clearing list objects now stores the item pointer
   atomically and frees with shared-aware allocation in GIL-disabled
   builds.

-  **NoGil:** Now tracks more connections in our ``tp_traverse`` methods
   of compiled types.

-  **UI:** Fix, no longer emits a false missing-file warning for
   ``--include-data-files-external``.

-  **AIX:** Added COFF dump based DLL dependency detection, with various
   fixes to the parsing, e.g. ignoring hex values and ``exp`` archive
   members, column based parsing, more error checks, and listing only
   the native architecture.

-  **AIX:** The Python DLL locating code is now more general, and a
   wrong structure entry for the ``dladdr`` helper was corrected.

Package Support
===============

-  **Standalone:** Added support for the ``pyDOE3`` package. (Added in
   4.1.1 already.)

-  **Standalone:** Added support for the ``mssql_python`` package.
   (Added in 4.1.1 already.)

-  **Standalone:** No longer proposes to recompile the
   ``charset_normalizer`` extension module. (Added in 4.1.1 already.)

-  **Standalone:** Added support for the ``emoji`` package. (Added in
   4.1.2 already.)

-  **Standalone:** Added support for the ``mitmproxy`` package. (Added
   in 4.1.2 already.)

-  **Plugins:** Fix, PyQt5 markdown data files caused errors on Linux,
   they are now excluded. (Fixed in 4.1.1 already.)

-  **Plugins:** Added support for newer ``pkg_resources`` versions,
   where the ``EggProvider`` was removed. (Added in 4.1.1 already.)

-  **Plugins:** Fix, build artifacts with ``.a``, ``.prl``, and ``.la``
   suffixes in QML directories were no longer included, now they are
   included again. (Fixed in 4.1.2 already.)

-  **Standalone:** Added automatic detection of ``cffi`` dependencies.

-  **Standalone:** Added support for newer ``scipy``.

-  **Standalone:** Added support for newer ``sqlfluff``.

-  **Standalone:** Added support for newer ``datasets``.

-  **Standalone:** Added support for newest ``toga``.

-  **Standalone:** Added a workaround for deep recursion in the
   ``univers.maven`` package, where its ``list2tuple`` function was
   replaced with a non-recursive version.

-  **Standalone:** Fix, platform specific ``gi`` modules are now
   included as well.

-  **Plugins:** Fix, added the missing ``webview.platforms.win32``
   dependency for newer ``pywebview``, and fixed accidental assignments
   instead of comparisons that caused too many modules to be included
   when Qt was used.

-  **Plugins:** Detects Qt plugin XML and webview modules automatically.

-  **Plugins:** Fix, avoided a warning when the ``gi`` module is not
   usable.

-  **Plugins:** Added support for ``Tcl`` and ``Tk`` from zip files.

-  **Plugins:** Fix, object files on Windows are now also ignored for
   ``PySide6``.

-  **macOS:** No longer needs the onefile workaround for ``PySide2``.

-  **macOS:** Added a workaround for a ``PySide6`` packaging issue.

-  **macOS:** Added a non-deployment handler for ``urllib.request``,
   catching the common case where ``certifi`` is not used.

New Features
============

-  **Python 3.14:** Pronounced Python 3.14 as officially supported.

-  **Python 3.14:** Made deferred annotations the default mode.

-  **Python 3.14:** Added support for module-level deferred annotations,
   and Python source generation for ``__annotate__`` functions.

-  **Python 3.14:** Added support for ``__annotate__`` for classes, and
   delaying class level annotations when the
   ``--experimental=deferred-annotations`` flag is given. With 4.2, this
   is the default mode. (Added in 4.1.1 already.)

-  **Python 3.14:** Added the
   ``--experimental=no-bytecode-to-compiled-fallback`` flag for
   requiring bytecode code generation to succeed.

-  **Python 3.15:** Added initial support for compiling with Python
   3.15.

-  **Python 3.7+:** Added support for ``importlib.resources.contents``
   and ``importlib.resources.is_resource``, which had been overlooked so
   far. (Added in 4.1.3 already.)

-  **Python 3.12+:** Added support for the no-argument form of
   ``importlib.resources.files()`` as well.

-  **Linux:** Added support for ``app`` mode, creating a ``.desktop``
   file for the compiled result, usable with standalone and onefile.

-  **Installer:** Added an installer for Windows via NSIS with
   ``--windows-create-installer``, and relocated the macOS DMG creation
   into the installer as ``--macos-create-installer``.

-  **Installer:** Added support for a Linux installer via AppImage with
   ``--linux-create-installer``, using ``appimagetool`` from ``PATH`` or
   a cached download.

-  **OS400:** Detects IBMi Python as a flavor.

-  **Plugins:** Added the ability to resolve variable references to
   compile-time constants during tree building, used for ``pyqtgraph``
   to resolve ``QT_LIB``, enabling dead code elimination of unused Qt
   binding branches. (Added in 4.1.3 already.)

-  **Plugins:** Added the ``onMetaPathLoaderEntryTemplate`` plugin
   method, allowing plugins to modify the template arguments used to
   generate the meta path loader entries for modules.

-  **Plugins:** Added the ability to set defines differently for onefile
   builds and backend builds.

-  **UI:** Added the ``--update-check`` option to check if a newer
   Nuitka version is available.

-  **macOS:** Added the ``--macos-app-macos-min-version`` option for the
   minimum app version, and now sets ``CFBundleVersion``.

-  **macOS:** Added the ``--macos-app-category-type`` option to set the
   app category for the app store.

-  **PGO:** Added the ``--pgo-python-error-exit`` option to control
   error-exit handling.

-  **Reports:** Added totals for C compilation and linking as well,
   reporting the accumulated user and system CPU time and module count
   of compilation, and the CPU time of linking, next to the existing
   code generation totals.

Optimization
============

-  **Python 3.14:** Added ``_zstd`` and ``_remote_debugging`` to the
   standard library modules known to never raise on import, allowing
   their imports to be optimized accordingly. (Fixed in 4.1.2 already.)

-  Replaced our uses of ``PyCallable_Check`` with a direct ``tp_call``
   NULL check, which avoids the expensive ``__call__`` attribute lookup
   fallback that ``PyCallable_Check`` does.

-  Runtime ``isinstance`` checks now use our own implementation with the
   faster type checking helpers, instead of the generic
   ``PyObject_IsInstance``.

-  Made the new style code objects the default. These are treated as
   constant objects now and remove the need for a special path to
   generate them. It reduces the generated code volume by a lot.

-  Loop value traces for the same loop are now considered the same,
   regardless of being complete or incomplete, enabling more merging of
   optimization traces.

-  The constant blob is now always created as an object file, removing
   the special Windows resource mode, and the blob creation code was
   made generic.

-  Loader tables no longer need a NULL terminator, since the entry count
   is now passed into the using code, making them more compact.

-  The shape of ``iter`` results is now always known, enabling more
   optimizations in general. As a consequence, ``os.uname()[0]``, the OS
   name, is now known at compile time, allowing platform checks based on
   it to be statically optimized.

-  Added ``enumerate`` and ``zip`` built-in nodes, in preparation of
   full optimization for them.

-  Expanded dual type operations with previously missing sub helpers,
   and fixed mistakes for existing ones.

Anti-Bloat
==========

-  Avoided more ``tkinter`` dependencies from ``PIL``. (Fixed in 4.1.1
   already.)

-  Avoided including ``matplotlib`` due to ``pandas`` plotting. (Fixed
   in 4.1.1 already.)

-  Avoided including ``setuptools_scm`` when using ``shtab``. (Fixed in
   4.1.3 already.)

-  Avoided including ``setuptools`` when using ``vcs_versioning``.
   (Fixed in 4.1.3 already.)

-  Avoided using ``click`` when using ``httpx``.

-  Avoided a ``toga`` cleanup error during program shutdown on Windows.

Organizational
==============

-  **Actions:** Introduced an "integration" branch as an intermediate
   step before develop, for PRs that are not considered fully
   merge-safe, or that may hit a hotfix release instead.

-  **Project:** Corrected a few mistakes done when changing the license,
   referencing the runtime exception everywhere and using a proper link
   to the correct version of the license file on the web. (Fixed in
   4.1.1 already.)

-  **Debian:** Made builds work inside containers that have the
   ``x-bit`` stripped from the install file, by making it an executable
   script. (Fixed in 4.1.1 already.)

-  **Release:** Fix, the inline copy of ``atomicwrites`` was still
   needed for Python 2. (Fixed in 4.1.1 already.)

-  **UI:** Fix, duplicate data file targets were not detected, which now
   warns and uses the first variant. (Fixed in 4.1.1 already.)

-  **RPM:** Fix, the inline copy of ``atomicwrites`` was still needed
   for the update check, and is no longer executed during RPM builds.
   (Fixed in 4.1.3 already.)

-  **Release:** Better error message for build failures in the PyPI
   release script.

-  **Zed:** Added autoformatting on save for source files and Nuitka
   Package Configuration files.

-  **AI:** Added the ``--assume-yes-for-downloads`` flag to autoformat
   commands.

-  **AI:** Expanded agent guidance with a verification matrix, skill
   index, and syntax restrictions.

-  **AI:** Made it clear that the issue template is to be followed
   strictly by AI assistants, and that issues ignoring it will be closed
   as invalid.

-  **AI:** Disallowed local imports unless necessary.

-  **AI:** Pointed to the CMD files for repo tools on Windows.

-  **AI:** Modernized the agent config, removing cursor compatibility,
   splitting rules into multiple files, and dropping OpenAI and Gemini
   specific files.

-  **Visual Code:** Also generated a clangd config for the OS/Python
   combination.

-  **Visual Code:** No longer started the pylint check automatically.

-  **Modules:** Merged upstream enhancements into the inline ``stubgen``
   copy, improving the generated type stubs.

-  **Actions:** Enabled Python 3.14 in CI.

-  **Actions:** Dropped an unneeded requirements file installation in
   CI.

-  **Docs:** Updated the man pages with the new CodeMeter plugin
   options.

-  **Plugins:** Added separate ``plugin-warning`` and ``plugin-error``
   levels for plugin messages in package configuration, allowing plugins
   to report errors.

-  **UI:** Added ``{PYTHON_VERSION}`` and ``{PYTHON_VERSION_FULL}``
   variables for project expansion.

-  **Debugging:** Added the ``--devel-no-bytecode-to-compiled-fallback``
   option to check coverage.

-  **Quality:** Added checker tools for pyright, basedpyright, ruff, and
   clangd, plus initial cleanups for fewer linter errors.

-  **Quality:** Added ``--assume-yes-for-downloads`` support to the
   checker tools.

-  **Quality:** Use PyLint from the private pip space.

-  **Quality:** Autoformat now removes empty module configurations from
   the YAML package configuration, which had accumulated when config
   features were removed.

-  **Quality:** The autoformat tool now outputs the diff when generated
   files would change with the ``--check`` option.

-  **Quality:** Autoformat converts em-dashes to regular dashes in C
   files.

-  **Quality:** Autoformat removes the spaces between words in
   ``spell-checker: ignore`` lines.

-  **Quality:** The repo ruff configuration no longer formats, since our
   own autoformat is used, and more unwanted warnings were disabled.

-  **Quality:** Autoformat now respects the exclusion of certain areas
   for JSON files and image files too, which it previously formatted and
   optimized regardless.

-  **Quality:** The git pre-push hook no longer fails on submodules that
   are not checked out, skipping the missing files.

-  **Quality:** The YAML checker no longer outputs traces on success,
   only reporting problems, and the autoformat progress bar total was
   improved.

Tests
=====

-  Disabled parts of the ``pkgutil_usage`` test with newer
   ``pkg_resources`` versions that lost some features. (Fixed in 4.1.1
   already.)

-  Ignored clang download warnings in output comparisons as well. (Fixed
   in 4.1.1 already.)

-  Ignored differences from messages about Qt font usage in output
   comparisons. (Fixed in 4.1.1 already.)

-  Rejected using ``--all`` and ``--pattern`` at the same time in the
   test runner. (Fixed in 4.1.1 already.)

-  **macOS:** Ignored the ``libffi-trampolines.dylib`` system library
   used by Python 3.14 in test comparisons. (Fixed in 4.1.1 already.)

-  **Debugging:** Fix, deep hashing checks failed with active
   exceptions, which was relatively easy to trigger, e.g. with
   ``SystemExit`` being set. (Fixed in 4.1.1 already.)

-  Added support for compiled-only and uncompiled-only exclusive output
   lines to the output comparison tool, allowing tests of
   Nuitka-exclusive features while still comparing the rest of the
   output.

-  Allowed file accesses under system library paths in tests for the
   Debian Python flavor, since its Python relies on system-packaged
   libraries.

-  No longer update resume information for "only" search mode runs.

-  **Python 3.11+:** Normalized traceback comparison by dropping the PEP
   657 caret lines from CPython's output, which Nuitka does not produce,
   and stripping blank lines between frames.

-  Added ``--no-debug-immortal-assumptions`` to PySide tests.

-  **Linux:** Allowed reading the ``/usr/share/zoneinfo`` directory
   itself in test file access checks, not just paths below it, since the
   system time zone info lives there.

-  Added app bundle mode and signature verification to the comparison
   test tool, where the signature is verified before running, since some
   programs like Qt WebEngine modify themselves on launch.

-  **Python 3.15:** Added support for running tests with it.

-  Added a ``wait_for`` condition for test cases of ``nuitka-watch``,
   where a case is skipped until the condition is met, used e.g. to wait
   for pip installs to start working.

Cleanups
========

-  Fixed pylint warnings in the coverage rendering tool. (Fixed in 4.1.1
   already.)

-  **Quality:** Enforced the required versions for the private pipspace
   packages used for YAML formatting. (Fixed in 4.1.2 already.)

-  Fixed the styling of links in informational messages, as the
   underline of the link was not reset and leaked into the following
   text. (Fixed in 4.1.3 already.)

-  **Quality:** Updated to the latest ``ruamel.yaml`` package and
   stopped using its private interface. (Fixed in 4.1.3 already.)

-  Generated internal class names in the node code now start with an
   underscore, so it is obvious they must not be used directly, and the
   stable alias names should be used instead.

-  Cleaned up the pylint watching code.

-  **Watch:** The ``nuitka-watch`` tool retries git operations on all
   platforms.

-  **Watch:** The ``nuitka-watch`` tool outputs which pip update failed.

-  **Watch:** The ``nuitka-watch`` tool writes XML reports like
   ElementTree does.

-  **Watch:** Improved the automatic staging of changes of
   ``nuitka-watch``.

-  The warning about a missing ``clang-format`` binary now uses the
   shared once-per-warning mechanism, instead of a hand-coded flag.

-  Completed the finalization of dead trailing statements, so that
   removed dead statements free their nodes properly when optimization
   removes them.

-  Nuitka's internal value hashing is now stable for dict values, with
   sorted items, where previously the insertion order was used. Since
   dicts with the same contents can have different insertion orders,
   equal dicts could hash differently, which matters for reproducible
   builds and caching, preparing this for future use.

-  The Jinja2 inline copy no longer imports the ``pkg_resources`` inline
   copy unless ``PackageLoader`` is used.

-  **Windows:** ``pdb`` files included as data files are now properly
   traced, avoiding warnings in onefile mode, and allowing manual
   copying of such files to be rejected in the future.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
