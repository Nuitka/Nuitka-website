:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.4rc2**.

**************************************************
 **Nuitka** Release |NUITKA_VERSION_NEXT| (Draft)
**************************************************

.. note::

   These are the draft release notes for the upcoming **Nuitka**
   |NUITKA_VERSION_NEXT| release. A primary goal for this version is to
   improve Python 3.15 support, with work planned on frame locals
   proxies as in Python 3.13, optimization of iterator unpacking, and
   inlining of generator expressions. Development is ongoing, and this
   documentation might lag slightly behind the latest code changes.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  Fix, when the main module raised an exception during its execution,
   it was unregistered and released like any other module, although its
   code objects and functions can still be used afterwards, e.g. by
   ``__del__`` methods making frames during interpreter finalization,
   which could crash. The main module is now kept registered and
   referenced. (Fixed in 4.3.1 already.)

-  **Python3:** Fix, the ``__path__`` of compiled namespace packages was
   created with the compile time full name of the package, which does
   not necessarily match the ``__name__`` the module has at run time, so
   the namespace path could not find its submodules, e.g. for a nested
   implicit namespace package inside a compiled package. The module
   ``__name__`` attribute is now used. (Fixed in 4.3.1 already.)

-  **Python 3.14+:** Fix, deferred annotations did not account for
   conditional execution, so annotations in blocks that did not run,
   e.g. under ``if TYPE_CHECKING:``, were still included in
   ``__annotations__``, unlike CPython, which only includes such
   annotations if their assignment registered its index in
   ``__conditional_annotations__``. The registration is now done at run
   time and checked when the annotations are created. (Fixed in 4.3.1
   already.)

   .. code:: python

      from typing import TYPE_CHECKING

      condition = True

      if TYPE_CHECKING:
          checked_only: set

      if condition:
          executed: str
      else:
          not_executed: bytes

      # 4.3: all annotations present in "__annotations__"
      # 4.3.1: only annotations of executed statements present

-  **Standalone:** The Tk version 9 interpreter on Windows is now
   created with the ``PATH`` environment variable temporarily removed,
   since Tk loads ICU DLLs dynamically and prefers versioned DLLs found
   in the ``PATH`` over the ones included with Windows, which could make
   the program depend on third party software. (Fixed in 4.3.1 already.)

-  **Plugins:** Fix, the probe that decides whether compiled methods
   need cached wrappers to avoid the unlimited API ``PySide6`` via
   ``SystemError`` in signal slots used temporary bound methods, which
   were not protected from the other bug we normally work around. (Fixed
   in 4.3.1 already.)

-  **Anaconda:** Fix, the ``include/python`` directory used on Windows
   by Anaconda and conda-forge Python since version 3.15 was not
   considered when locating the Python headers, so compilation aborted
   with a message about an unsupported embeddable distribution. (Fixed
   in 4.3.1 already.)

-  **Module:** Fix, the file system paths of loader entries used the
   package prefix that is added to the runtime name when a compiled unit
   is loaded as a package, e.g. producing ``ns/pkg`` instead of ``pkg``,
   so data and resource files were looked up at the wrong location. The
   prefix is now removed for the file system paths. (Fixed in 4.3.1
   already.)

-  Fix, ``dict.fromkeys`` nodes were marked as unable to raise for
   iterables without a known small length, so e.g. unhashable keys or a
   raising iterator could go unhandled and crash. They are now always
   considered able to raise, while the compile time computation remains
   limited to small known iterables. (Fixed in 4.3.2 already.)

-  Fix, isolated mode (``--python-flag=isolated``) still registered the
   meta path based loader's ``sys.path_hooks`` entry, which always
   raised ``ImportError``, so a path hook was present where none should
   be. No path hook is now registered at all. (Fixed in 4.3.2 already.)

-  Fix, the inline ordered dictionary used on Python 2.6 had
   ``setdefault`` return ``None`` instead of the value, which could
   break YAML configuration handling there. It now returns the value
   like the built-in ``dict`` method. (Fixed in 4.3.2 already.)

-  Fix, closing a generator or coroutine before it was started returned
   success without marking it as finished, so its state stayed
   ``GEN_CREATED`` or ``CORO_CREATED`` and a later ``next()`` would
   start the body instead of raising ``StopIteration``. Closing now
   marks it as finished. (Fixed in 4.3.2 already.)

-  Fix, a ``break`` or ``continue`` of a loop created inside a
   ``finally`` block released the pending return value, although it does
   not abandon the ``return``, so a released object could be returned.
   The release now only happens for loops that were active when the
   return handler was entered. (Fixed in 4.3.2 already.)

-  **Python 3.5+:** Fix, coroutine and async generator returns did not
   run the local variable cleanup, so their locals dictionary and the
   values it holds stayed alive after finishing. The return exit now
   releases them like the exception exits already did. (Fixed in 4.3.2
   already.)

-  **Python 3.8+:** Fix, an uncaught ``KeyboardInterrupt`` gave exit
   code 1 instead of the SIGINT style exit code CPython uses since 3.8,
   i.e. ``128 + SIGINT`` on POSIX and ``0xC000013A`` on Windows. (Fixed
   in 4.3.2 already.)

-  **Python 3.13+:** Fix, ``--python-flag=no_warnings`` gave errors,
   since the warning options were applied before the meta path based
   loader was ready, while the interpreter imports the ``warnings``
   module during startup on 3.13. The disabling now happens after the
   loader setup. (Fixed in 4.3.2 already.)

-  **Python 3.14:** Fix, creating single character and empty ``bytes``
   objects used the internal ``_Py_SINGLETON`` macro, which is fragile
   there, and now accesses the runtime static objects directly. (Fixed
   in 4.3.2 already.)

-  **Python 3.14:** Fix, the ``ValueError`` message of ``list.index()``
   did not match CPython 3.14, which uses the static text
   ``list.index(x): x not in list`` instead of naming the value. (Fixed
   in 4.3.2 already.)

-  **Plugins:** Fix, the ``PySide6`` signal workaround kept the receiver
   objects alive, since it held references to the compiled methods
   rather than only to their function objects, which is all that needs
   protection from the over-release issue. Receivers are now released
   normally. (Fixed in 4.3.2 already.)

-  **Plugins:** Fix, the ``PySide6`` signal workaround could crash
   during shutdown, since PySide6 releases the compiled function object
   once too often, potentially after interpreter finalization. A
   keep-alive reference is now leaked for the function to survive this,
   and the wrappers use weak references to the receiver, dropping
   connections and cached wrappers when it is released, which also keeps
   memory usage under control. (Fixed in 4.3.2 already.)

-  **macOS:** Fix, onefile signal forwarding did not handle signals sent
   directly to the bootstrap process, since ``kill(2)`` delivers
   ``si_code == 0`` there rather than ``SI_USER``. Signals are now
   always forwarded on macOS, and the child suppresses the duplicate
   SIGINT it already received from the terminal process group. (Fixed in
   4.3.2 already.)

-  **macOS:** Fix, code signing with a keychain file could fail because
   ``codesign`` only searches the keychains in the user's search list,
   and the temporary copy used for signing was not part of it. The
   temporary keychain is now added to the search list while signing and
   the previous list restored afterwards, and identity names are
   resolved to their unique hashes so other keychains cannot make them
   ambiguous. (Fixed in 4.3.2 already.)

-  **macOS:** Fix, the onefile parent bootstrap could forward SIGINT
   after the child had already received the same signal from the
   terminal process group, so the duplicate arrived only when the
   handler was already running and interrupted the shutdown. When the
   signal did not come from the parent, the handler now waits briefly
   for a possible forwarding while SIGINT is blocked, so a duplicate
   that arrives then is suppressed. (Fixed in 4.3.2 already.)

-  **Compatibility:** Fix, floating point power operations handled
   underflow as an error and infinite results without ``errno`` as
   success. Underflow now gives the zero result, and infinite results
   raise ``OverflowError``, matching CPython's ``_Py_ADJUST_ERANGE1``.
   (Fixed in 4.3.2 already.)

-  **Module:** Fix, loader entry names were always prefixed with the
   package prefix in module mode, even when the compiled unit was built
   under its full dotted name, so imports were attempted with duplicated
   names like ``ns.sub.ns.sub.pkg.models``. Only entries rooted at the
   loaded leaf name are prefixed now. (Fixed in 4.3.2 already.)

-  **Onefile:** Fix, when the child process was terminated by a signal,
   the bootstrap used ``WEXITSTATUS`` on its status, reporting success
   instead of the signal exit code. It now reports ``128 + signal``.
   (Fixed in 4.3.2 already.)

-  **Onefile:** Fix, the compressor failed with ``libzstd`` builds
   without multithreading support, since a positive thread count is
   rejected there. The thread count is now limited to the supported
   range, and the ``zstandard`` fallback uses a single thread. (Fixed in
   4.3.2 already.)

-  **Onefile:** Fix, the child exit code could be lost when the child
   was reaped by the signal handler, since the main wait then got
   ``ECHILD`` and reported 0. The reaped status is now recorded and used
   for the exit code. (Fixed in 4.3.2 already.)

-  **BSD:** Fix, onefile binaries were not linked with ``pthread``,
   although the parent monitoring thread uses ``pthread_create()`` and
   ``pthread_detach()``, which need it on the BSDs as well. (Fixed in
   4.3.2 already.)

-  **BSD:** Fix, defining ``_POSIX_C_SOURCE`` on BSD systems restricted
   the system headers to strict POSIX, hiding BSD specific interfaces,
   e.g. ``getexecpath`` was left undeclared in the onefile bootstrap on
   OpenBSD. It is no longer defined there. (Fixed in 4.3.2 already.)

-  **BSD:** Fix, the ``sendfile()`` fallback for file copying reported
   success even when reading or writing failed, since it returned a
   boolean while the caller compared against -1, and the read error
   check tested the function rather than the byte count. It now returns
   the copied byte count, handles ``EINTR``, completes short writes, and
   is also used on FreeBSD. (Fixed in 4.3.2 already.)

-  Fix, when the stop argument of ``list.index()`` failed its index
   conversion, the ``LIST_INDEX4`` helper released the start index a
   second time, risking a crash from the over-release. It is now only
   released once. (Fixed in 4.3.3 already.)

-  Fix, sequence item access converted oversized indices with
   ``PyNumber_AsSsize_t`` and no exception type, so indices that did not
   fit ``Py_ssize_t`` were clamped to the platform maximum instead of
   raising ``IndexError`` like CPython. The conversion now passes
   ``PyExc_IndexError``, so such indices raise the matching
   ``IndexError``. (Fixed in 4.3.3 already.)

-  Fix, the compiled ``chr()`` used ``PyInt_AsLong`` and replaced
   conversion errors with a generic ``TypeError``, so ``__index__``
   errors did not propagate, floats were accepted on Python 2 and gave
   the wrong message before Python 3.9, and values outside the C ``int``
   range gave the wrong exception. It now uses
   ``Nuitka_PyLong_AsLongAndOverflow``, rejects floats, propagates
   ``__index__`` errors, and gives ``OverflowError`` before Python 3.13
   and ``ValueError`` afterwards. (Fixed in 4.3.3 already.)

-  Fix, ``HAS_ATTR_BOOL2`` did not release the result of the attribute
   lookup after converting it to a boolean, so a reference leaked on
   every call. The result is now released. (Fixed in 4.3.3 already.)

-  Fix, the ``list.copy`` node always registered an exception exit,
   while the code generation assumed that the operation cannot raise, so
   dead code for an error that was never considered was emitted. (Fixed
   in 4.3.3 already.)

-  **Python 2:** Fix, the ``BUILTIN_RANGE3`` helper checked the
   converted end value for failure instead of the converted step value,
   so ``range()`` with an object step that failed conversion left the
   error unhandled and could crash. The step conversion is now checked.
   (Fixed in 4.3.3 already.)

-  **Python 3.12+:** Fix, the replacement for
   ``sys._getframemodulename()`` converted its depth with an unbounded
   ``Py_ssize_t``, so values beyond the C ``int`` range were used for
   frame traversal instead of raising ``OverflowError`` like CPython.
   The conversion now uses ``PyLong_AsLongAndOverflow`` and rejects
   values that do not fit a C ``int``. (Fixed in 4.3.3 already.)

-  **Python 3.15+:** Fix, the meta path based loader set ``__spec__``,
   ``__file__``, and ``__path__`` on extension modules only after
   executing them, so the module code did not see them. The attributes
   are now set before execution, and the module is registered in
   ``sys.modules`` only after it executed successfully. (Fixed in 4.3.3
   already.)

-  **Compatibility:** Fix, in-place addition of a ``list`` or ``tuple``
   with a right value of unknown type used sequence concatenation
   whenever the value was a sequence, so a ``__radd__`` method of e.g. a
   ``tuple`` or ``str`` subclass was ignored. The number add slot of the
   right value is now tried first, and concatenation only happens when
   it is absent. (Fixed in 4.3.3 already.)

   .. code:: python

      class TupleWithRightAdd(tuple):
          def __radd__(self, other):
              return "TupleWithRightAdd.__radd__"


      values = [1]
      values += TupleWithRightAdd((2,))

      # 4.3.2: [1, 2] (wrong)
      # 4.3.3: "TupleWithRightAdd.__radd__" (correct)

-  **Multidist:** Fix, the runners generated for entry points called the
   user main function unconditionally, so importing one in a
   multiprocessing child process executed the program again. The call is
   now guarded by a ``__name__ == "__main__"`` check. (Fixed in 4.3.3
   already.)

-  **Onefile:** Fix, the SIGINT deduplication handler published the last
   SIGINT time only after waiting for a possible parent forward, so
   handlers in other threads could not suppress duplicates during the
   delay, an interrupted sleep shortened the wait, and ``errno`` was not
   preserved for the saved Python handler. It now distinguishes terminal
   delivery where the platform reports it, publishes the timestamp
   before waiting, retries interrupted sleeps, and restores ``errno``.
   (Fixed in 4.3.3 already.)

-  Fix, cloning a ``reversed()`` call node passed its child as
   ``object`` instead of ``object_arg``, which the node constructor does
   not accept, so cloning such a node, e.g. in tuple assignments using
   ``reversed()``, could crash the compiler. The clone arguments now use
   the constructor parameter names. (Fixed in 4.3.4 already.)

-  **macOS:** Fix, app bundles in forced console mode used the regular
   executable name in their ``Info.plist``, so the launcher script was
   not identified correctly. The executable name now gets a ``.sh``
   suffix in that mode. (Fixed in 4.3.5 already.)

-  **Compatibility:** Fix, comparison chains evaluated the right operand
   before the left one, so function calls and other side effects in
   expressions like ``a() < b() < c()`` happened out of order. The left
   operand is now stored in a temporary first, and each comparison uses
   its own temporary, preserving left-to-right evaluation and
   short-circuiting. (Fixed in 4.3.5 already.)

-  **Compatibility:** Fix, ``os.path.isdir`` used ``path`` as its
   argument name, while CPython uses ``s``, so calls with the keyword,
   e.g. ``os.path.isdir(s=...)``, failed. The keyword name is now ``s``,
   and the argument remains positional-only on Windows before Python
   3.8. (Fixed in 4.3.5 already.)

-  Fix, the ``locals()`` expression node did not include its locals
   scope in ``getDetails``, so cloning or displaying the node failed,
   e.g. in unpacking assignments that use ``locals()``. The scope is now
   included.

-  **Python 3.14:** Fix, exception messages that name the type of a
   mistyped object used only the type name, while CPython 3.14 uses the
   fully qualified name. The complaint helpers now use
   ``Nuitka_PyType_GetFullyQualifiedName``, which includes the module
   for heap types outside ``builtins`` and ``__main__``.

-  **Plugins:** Fix, the onefile compression warning of the ``upx``
   plugin checked the ``isOnefileMode`` function object instead of
   calling it, so the warning was never effective. The check now calls
   it.

-  **Plugins:** Fix, the ``source-inclusion`` probe did not record
   source files loaded by child processes. It now injects a generated
   ``sitecustomize`` module that writes each record immediately, so
   records from worker processes survive even when they are killed, and
   conflicting records for a module are reported as an error.

-  **Windows:** Fix, removing a directory tree with links on Python
   before 3.8 followed junctions and symlinks and deleted the contents
   of their target directories instead of only the links, which could
   lose unrelated files, e.g. of the Python installation. Links are now
   never followed, and a link given to ``removeDirectory`` itself is
   removed safely too.

-  **Windows:** Fix, for virtual environments of uninstalled self
   compiled Python, the DLLs next to the base executable were not
   scanned, since only the ``sys.executable`` directory and the system
   prefix were used. The directory of the system prefix executable is
   now included as well.

-  **Compatibility:** Fix, a relative import whose level exceeded the
   package depth was resolved to a parent package that was not there,
   instead of giving a not found result. It now stops at the top-level
   package, and this also applies when a package is compiled as a
   module, where the runtime parent package is not known at compile
   time.

-  **Debugging:** Fix, on Windows, the PDB file of an unstripped target
   was left in the build directory after moving the executable, so it
   was lost. It is now moved next to the final binary, and the ``.pdb``
   suffix is cleaned up with the other intermediate files.

-  **MSYS2:** Fix, the runner created for entry points used a
   non-normalized path, which could produce mixed path separators. The
   generated runner filename now uses ``getNormalizedPathJoin``.

Package Support
===============

-  **Standalone:** Added the missing ``._uuid`` dependency for the
   ``psycopg_c._psycopg`` extension module, like it already existed for
   ``psycopg_binary._psycopg``, so its dynamically imported UUID module
   is included. (Added in 4.3.2 already.)

-  **Standalone:** Added ``pyodbc`` to the modules that package system
   DLLs on macOS, so the dynamic library dependencies of its extension
   module are included. (Added in 4.3.4 already.)

-  **Standalone:** Added missing implicit imports for
   ``urllib3.contrib.resolver.factories`` and
   ``urllib3.contrib.resolver._async.factories``, so the resolver
   implementations that these factories load dynamically are included in
   standalone builds. (Added in 4.3.4 already.)

-  **Standalone:** Added support for the ``vLLM`` package, including
   data files for ``flashinfer``, ``cuda.tile``, and the ``templates``
   directories of ``torch._inductor.kernel`` and its ``flex`` variant,
   plus the ``tvm_ffi`` include directory and ``libtvm_ffi`` DLLs.

-  **Standalone:** Added support for the ``triton`` package, including
   implicit imports for its backends, data files for the AMD and NVIDIA
   backends and their ``driver.c``, Python headers for in-place C
   compilation, and a replacement for ``triton_key`` with the value of
   the build environment. The ``cuda_utils`` module is not covered yet.

-  **Standalone:** Avoided including the Qt plugins and fonts of
   non-headless ``opencv-python`` when a Qt binding plugin is enabled,
   since they conflict with the binding's own Qt libraries, and added a
   warning recommending ``opencv-python-headless`` instead.

-  **Plugins:** Added a ``numba`` plugin. It compiles the modules of the
   ``numba`` package to bytecode, since Numba JITs functions of its own
   package even when the JIT is disabled, and leaves functions using the
   common Numba JIT decorators uncompiled when the JIT is enabled, plus
   ``stencil`` decorated functions always. The on-disk cache is disabled
   in standalone mode, where compiled functions have no file backing.
   The new ``--numba-enable-jit`` option controls the JIT, defaulting to
   ``no`` in standalone mode and ``yes`` otherwise.

New Features
============

-  **Python 3.15+:** Added support for module export hooks, where an
   extension module provides a ``PyModExport_<name>`` or
   ``PyModExportU_<name>`` function returning a slots array, which
   CPython prefers over the ``PyInit_<name>`` entry point function, with
   the meta path based loader checking for it first and falling back to
   ``PyInit_``. Modules from export hooks are created with
   ``PyModule_FromSlotsAndSpec``, with a ``SystemError`` reported for
   hooks that fail without setting an exception or raise an unreported
   one, and a missing export function now gives an ``ImportError``
   naming both functions that were tried. (Added in 4.3.1 already.)

-  **OpenBSD:** Added onefile mode support, removing OpenBSD from the
   list of systems where only standalone mode was supported. (Added in
   4.3.2 already.)

-  **Python 3.14:** Remote debugging via PEP 768 is now disabled in
   compiled programs, so another process cannot attach through
   ``sys.remote_exec`` and execute code in them. The new
   ``--devel-remote-debug`` option keeps the interface enabled for
   development. (Added in 4.3.5 already.)

-  **Plugins:** Added the ``onFinalResultFinished`` hook, which runs
   after all ``onFinalResult`` modifications, so plugins can inspect the
   final binary, e.g. to calculate its checksum. (Added in 4.3.5
   already.)

-  **Onefile:** Added an ``overlay`` resource mode, which attaches the
   onefile payload to the end of the executable instead of embedding it
   as a constant blob. It is used automatically on Windows when the
   payload would exceed the PE file size limit The bootstrap maps its
   own executable, uses the certificate table when the file is signed to
   find the payload end, and unpacks from there. Currently only Windows
   onefile mode supports this, as other OSes don't encounter these
   limits.

-  **Plugins:** The ``source-inclusion`` plugin now supports module
   mode. Since there is no unique main program,
   ``--source-inclusion-main`` names a program that exercises the
   compiled module, and the recorded source hook is installed before the
   top-level module body. The ``dash`` package configuration now warns
   when ``dash.long_callback`` uses ``inspect.getsource()`` for caching
   and recommends the plugin and option.

Optimization
============

-  Type descriptions are now exported uniformly as pointer variables and
   declared only in the generated module that uses them, so adding a
   description no longer changes the shared ``__constants.h`` header and
   thereby avoids rebuilding unrelated modules. (Added in 4.3.1
   already.)

-  **Scons:** Fix, the LTO job count was part of the C compilation
   flags, so the number of CPUs became part of the ``ccache`` key and
   made caching less successful. C compilation now uses plain ``-flto``,
   while the job count remains in the linker flags where parallel LTO
   matters. (Fixed in 4.3.5 already.)

-  **Scons**: Constant blob symbols are now marked with hidden
   visibility on ELF, since they are only referenced directly and were
   otherwise exported with ``-export-dynamic`` for no reason. (Added in
   4.3.5 already.)

-  **Scons:** Include paths below the Nuitka and Python installations
   are now replaced with build directory local symbolic links of stable
   names, and paths outside these roots get stable derived names. This
   keeps compiler command lines identical across machines, allowing
   ``ccache`` results to be shared and builds to be more reproducible.

Anti-Bloat
==========

-  **Packages:** Avoided following ``z3`` from ``tilelang`` and from
   ``torch.fx.experimental``, where it is only checked for being
   installed, or used for debug translation validation that serving does
   not need.

-  **Packages:** Avoided ``cython`` usage in ``zmq.backend.cython._zmq``
   when ``setuptools`` is not used.

-  **Triton:** Replaced the ``triton_key`` computation with the value of
   the build environment.

Organizational
==============

-  **Debian:** Fix, the ``py2dsc`` based Debian packaging on mounts that
   report all files as executable, e.g. container builds using Windows
   shares, gave the copied Debian config files the executable bit, and
   debhelper then executed ``nuitka.install`` instead of reading it,
   which failed. The executable permission is now removed from the
   copied files, keeping only ``rules`` executable. (Fixed in 4.3.1
   already.)

-  **Docs:** Documented Clang as the default compiler on OpenBSD in the
   Developer Manual, matching the compiler settings that already forced
   it there. (Fixed in 4.3.2 already.)

-  **Actions:** Fix, the retry for the initial compilation that
   downloads compilers was only done on macOS, so transient runner
   failures on other systems failed the workflow. It is now used on all
   operating systems, and the produced files are cleaned up before each
   attempt. (Fixed in 4.3.3 already.)

-  **UI:** Error and warning messages now name the actual compilation
   mode, e.g. ``app`` or ``onefile``, instead of saying ``standalone``
   as the problematic part of the mode. Or package rather than module
   mode.

-  **Quality:** The pre-push hook now also runs ``codespell`` on changed
   Python, C, RST, text, template, and Markdown files unless disabled at
   install time.

-  **Quality:** ``autoformat`` now sorts, de-duplicates, and fills
   ``spell-checker: ignore`` word lists, merging consecutive plain lines
   up to the line length.

-  **Debugging:** GCC and Clang builds now enable ``-Wshadow``, so
   accidental variable shadowing is detected during regular builds
   instead of only in later MSVC CI runs.

-  **Zed:** The editor configuration now excludes generated and build
   artifacts from file scanning and restricts basedpyright diagnostics
   to open Python files.

-  **Watch:** The watch tool now passes ``--update-check=never`` to
   Nuitka, avoiding update check noise for its test compilations.

Tests
=====

-  **Windows:** Fix, runtime tracing used the Dependency Walker module
   tree, which resolves names through the search order and includes
   delay loaded DLLs that were never used, so files could be reported as
   loaded that never were. It now uses only the profiling log, with
   ``PATH`` search disabled via a Dependency Walker configuration file,
   which also makes the tracing substantially faster by not scanning
   ``PATH``, and the GitHub Actions workarounds for modules found there
   are no longer needed. (Fixed in 4.3.2 already.)

-  Ignored GCC LTO ``make`` warnings about files with modification times
   in the future in output comparisons, since they are caused by clock
   skew in the environment and are not relevant to the test result.
   (Fixed in 4.3.5 already.)

-  The test runner now records the current test and marks it as failed
   when an error is reported through the runner code separately, so such
   failures are no longer missed.

-  Windows-only tests are now recognized by their ``Win`` or
   ``windows_`` name prefix and skipped on other systems, instead of
   listing every such test explicitly.

-  Extended the nested namespace package tests to cover
   ``pkgutil.iter_modules`` and ``pkgutil.walk_packages`` on compiled
   packages inside namespace packages.

-  Extended the Python 3.14 annotation tests to cover
   ``annotationlib.Format.FORWARDREF`` calls on class and method
   ``__annotate__`` functions.

Cleanups
========

-  Removed the obsolete ``CodeObjectsMixin`` and its
   ``getCodeObjectHandle`` methods; code generation now calls
   ``getCodeObjectAccessCode`` directly.

-  **WASI:** Type slots now use the ``PyObject *self`` signatures that
   CPython expects, and method table calls use
   ``Nuitka_PyCFunctionUnion`` with the actual function signatures.
   ``-Wcast-function-type`` is enabled for GCC, Clang, and Zig, so
   incompatible function casts are detected earlier.

-  Moved the Python installation prefix helpers from ``PythonVersions``
   into the new ``PythonPrefixes`` module, removing cyclic dependencies.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
