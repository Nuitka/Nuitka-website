:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.4rc6**.

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

-  Fix, in-place updates of module variables stored in the module
   dictionary did not keep the previous value alive during the
   operation, so it could be released while still in use, leaving a
   dangling reference. The operation now holds a new reference to the
   value until the update is complete.

-  Fix, the frame scope could be reduced during optimization while node
   replacements were still pending, so the decision was based on an
   untraced state. It now waits for the next pass when any node changed.

-  Fix, the frame locals proxy did not hash the lookup key before
   comparing variable names, so unhashable keys did not raise
   ``TypeError``. The key is now hashed up front, and names with
   different hashes are skipped.

-  Fix, the temporary path template expansion formatted
   ``timeval.tv_sec`` with ``%ld``, which is too narrow where ``time_t``
   is wider than C ``long``, e.g. for the WASI target. It now uses
   ``%lld`` with a cast.

-  Fix, assigning ``__file__`` or other module constants to a local
   variable could crash the optimization in standalone mode, since the
   specialized variable assignment still expected a variable reference
   after constant folding, e.g. where ``__file__`` becomes a path
   relative to the program directory. Such assignments are now converted
   to generic assignments, and the self-assignment checks verify the
   source is a variable reference first.

-  Fix, the set display optimization treated any constant element as
   hashable, so a constant set literal containing an unhashable
   constant, e.g. an empty list, was created at compile time instead of
   raising ``TypeError`` at run time. Constant set creation now requires
   known hashable elements, iteration prediction for single element sets
   only applies to hashable ones, and set creation error exits release
   the created set, so it can be used in boolean conditions.

-  Fix, deferred releases of pinned references were emitted at the end
   of the code scope instead of with the owning reference, and were not
   handled on error exits, so the custom release could happen too late
   or not at all. They are now emitted by the regular release code when
   the owning reference is dropped, and by error exit code for values
   still owned when an error occurs, with the scope end emission removed
   from sub-collectors.

-  **Python 3.14:** Fix, exception messages that name the type of a
   mistyped object used only the type name, while CPython 3.14 uses the
   fully qualified name. The complaint helpers now use
   ``Nuitka_PyType_GetFullyQualifiedName``, which includes the module
   for heap types outside ``builtins`` and ``__main__``.

-  **Python 3.14+:** Fix, template string interpolations asserted that
   no conversion was present, so ``!r``, ``!s``, and ``!a`` were not
   supported. The conversions are now mapped to the
   ``_PyInterpolation_Build`` codes, including format specifications and
   nested specifications.

-  **Python 3.14+:** Fix, template strings and interpolations were
   generated without ``withObjectCodeTemporaryAssignment``, so they did
   not work in boolean contexts and unused ones were not safely
   discarded. They now use the regular temporary assignment and cleanup.

-  **Python 3.4-3.7:** Fix, standalone mode did not provide a loader
   entry for ``multiprocessing.semaphore_tracker``, which these versions
   spawn instead of ``multiprocessing.resource_tracker``, so the tracker
   process could not start. The entry is now registered and used when
   the tracker module name matches.

-  **Python 3.4-3.7:** Fix, ``chr()`` used the Python 3.8+ argument
   conversion, so values outside the C ``int`` range gave the wrong
   errors there. It now converts to a C ``long`` first and reports
   ``OverflowError`` with CPython's messages for values above or below
   the C ``int`` range.

-  **Python 2:** Fix, ``chr()`` rejected float values on Python 2.6,
   where CPython truncates them. It now truncates them on 2.6, while 2.7
   continues to reject them.

-  **Python 3.10+:** Fix, the implicit ``staticmethod`` wrapping of
   ``__new__`` was applied only on Python 2, so compiled ``__new__``
   functions in class bodies were not treated like CPython's. It is now
   applied on Python 3.10 and later too, but not before 3.10, where
   ``staticmethod`` objects are not callable and ``enum`` calls
   ``__new__`` from the class namespace directly.

-  **Python 3.11:** Fix, invalid ``return``, ``break``, and ``continue``
   statements in ``except*`` blocks were not rejected, so invalid code
   compiled. They now raise CPython's ``SyntaxError`` when they escape
   the block, while nested functions, classes, and loops remain allowed.

-  **Python 3.12:** Fix, the ``long`` update helpers used
   ``Py_ABS(Py_SIZE())`` as the digit count, which no longer matches the
   digit count on Python 3.12, where it is packed into the object tag.
   They now use ``Nuitka_LongGetDigitSize``.

-  **Python 3.12+:** Fix, type aliases declared in nested generic
   functions could not be created, because the alias node used a
   variable reference for its name and claimed it could not raise. The
   written name is now passed as a constant and child expressions are
   evaluated for exceptions.

-  **Python 3.12.0:** Fix, a generator or coroutine closed before it was
   started was reported as closed by ``inspect.getgeneratorstate()`` and
   ``inspect.getcoroutinestate()``, while CPython 3.12.0 fails to clear
   the frame and reports it as created. The closed-before-start state is
   now tracked and reported like CPython.

-  **Python 3.11+:** Fix, ``except*`` re-raise detection compared the
   contained leaf exceptions, so re-raising a leaf exception and raising
   a new group that reused the same leaf were treated the same. The
   exception notes, traceback, cause, and context are now compared like
   CPython to distinguish actual re-raises.

-  **Python 3.15+:** Fix, ``async`` and ``await`` errors now use the
   Python 3.15 message formats, with fully qualified type names for
   ``__await__`` returning a coroutine or a non-iterator, and for
   awaiting a non-awaitable object, using the new
   ``SET_CURRENT_EXCEPTION_TYPE_COMPLAINT_QUALIFIED2`` helper, while
   keeping the Python 3.14 full compat and truncated type name handling.

-  **Python 3.15+:** Fix, call and class keyword argument errors now
   match Python 3.15. Calls with positional arguments use the generic
   "Value after * must be an iterable, not ..." message for the value
   after ``*``, non-string keyword names are reported after all mappings
   are merged so duplicate keyword errors take precedence, and class
   keywords use the CPython call helper in full compat mode so errors
   name ``__build_class__``.

-  **Python 3.12+:** Fix, ``importlib.resources.files`` used ``package``
   as its only argument name, while Python 3.12 renamed it to ``anchor``
   and kept a wrapper accepting ``package`` only until Python 3.15, so
   keyword calls were rejected or attributed to the wrong argument. The
   3.12 to 3.14 variant now accepts both names, the 3.15 variant only
   ``anchor``, and the generated version criteria were tightened.

-  **Python 3.12+:** Fix, type variable constraints were passed as the
   bound, so a constrained type variable had the tuple of constraints as
   its ``__bound__`` and no ``__constraints__``. Constraints are now
   passed separately when creating the type variable, with tests for
   function and class constraints, forward references, and lazy
   evaluation.

-  **Python 3.12+:** Fix, type alias, type variable, and deferred
   annotation scopes nested in class bodies resolved names against
   module globals rather than the class namespace, so forward references
   and class attributes shadowed at module level gave wrong results.
   Names are now looked up in the class namespace first with module
   globals as fallback, capturing the namespace before the class body
   runs and using the created class dictionary afterwards, with the
   prepared namespace as fallback when a metaclass returns a non-class.

-  **Python 3.14+:** Fix, the forkserver launcher kept its own ``-c``
   invocation in ``sys.argv``, and when no main path was passed the
   forked children executed the main module again. The parent process
   arguments are now passed through, the launcher options are removed
   from ``sys.argv``, and ``__parents_main__`` is pre-loaded as
   ``__main__`` when no main path is given.

-  **Standalone:** Fix, symlinks to shared libraries, e.g. versioned
   aliases like ``libfoo.so`` pointing to ``libfoo.so.1.2``, were copied
   as separate regular files, which could load duplicate library state.
   Symlinks are now preserved, with their targets copied first, and
   macOS binary path fixing is skipped for the link itself.

-  **Plugins:** Fix, the onefile compression warning of the ``upx``
   plugin checked the ``isOnefileMode`` function object instead of
   calling it, so the warning was never effective. The check now calls
   it.

-  **Plugins:** Fix, the ``source-inclusion`` probe did not record
   source files loaded by child processes. It now injects a generated
   ``sitecustomize`` module that writes each record immediately, so
   records from worker processes survive even when they are killed, and
   conflicting records for a module are reported as an error.

-  **Plugins:** Fix, the ``PyQt5`` and ``PyQt6`` slot decorators forced
   slot methods to remain uncompiled, and the PyQt5 plugin only applied
   in standalone mode, so decorated slots were not real Python methods
   and signal connections, disconnections, and ``QTimer.singleShot``
   could reject them or not track the receiver lifetime. Slots are now
   compiled, with runtime wrappers that expose decorated methods as real
   Python methods and convert compiled methods for signal
   ``connect``/``disconnect`` and timers while preserving receiver
   lifetime tracking. Accelerated builds get the support too.

-  **Plugins:** Fix, plugin decisions for docstrings and assertions were
   only applied through the global Python flags when building trees and
   resolving ``__debug__``, so per-module anti-bloat configuration for
   docstrings and assertions had no effect there. The module's decisions
   are now used when extracting docstrings and creating builtin
   references, and standard library modules always drop docstrings.

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

-  **Windows:** Fix, some Python installations failed in accelerated
   mode when the Python DLL was only found through the system search
   path, because extension modules could not be located. The exact
   ``sys.path`` is now passed in ``NUITKA_PYTHONPATH`` for execution
   when no launcher script is created.

-  **Windows:** Fix, MinGW64 and Zig builds for 64-bit Python before 3.8
   used the wrong ``long double`` ABI, and before 3.12 missed
   ``MS_WIN64``. The flags now match the MSVC ABI, and function pointer
   casts use unions to avoid debug build warnings.

-  **Windows:** Fix, ``getFileMode`` returned 0 for missing files, while
   the POSIX implementation returns -1, so callers such as
   ``isExecutableFile`` could treat a missing file as existing. It now
   checks ``GetFileAttributesW`` and returns -1 for invalid attributes.

-  **Windows:** Fix, the standalone loader used ``.pyd`` as the filename
   suffix for extension modules, so extension modules of debug Python
   builds, which use ``_d.pyd``, could not be found. The suffix now
   matches the freezer and uses ``_d.pyd`` for debug builds.

-  **Compatibility:** Fix, a relative import whose level exceeded the
   package depth was resolved to a parent package that was not there,
   instead of giving a not found result. It now stops at the top-level
   package, and this also applies when a package is compiled as a
   module, where the runtime parent package is not known at compile
   time.

-  **Compatibility:** Fix, assignments and deletions of ``__debug__``
   were not diagnosed as ``SyntaxError`` in all places, e.g. in named
   expressions, imports, function arguments, class keywords, type
   aliases, pattern matching, and function and class names. They now
   raise the same ``SyntaxError`` as the corresponding Python version,
   with its version-specific exceptions respected.

-  **Compatibility:** Fix, ``list.insert`` considered non-constant index
   values unable to raise and constant ones able to raise, which is the
   reverse of the actual behavior, so a ``float`` or ``None`` index went
   unchecked and later gave a ``SystemError``, and its ``TypeError``
   message lacked "object". Before Python 3.10, a ``float`` index now
   gives the argument parsing error like CPython. The ``insert``
   operation now raises ``OverflowError`` for index values too large for
   ``Py_ssize_t``, ``list.index`` clamps start and stop values like
   CPython, and ``__index__`` errors other than ``TypeError`` propagate.

-  **Compatibility:** Fix, more number operation corner cases, including
   in-place ``float **= nan`` returning the right operand without taking
   a reference, so objects still in use could be freed, ``2.0 ** inf``
   and ``0.0 ** -inf`` giving ``0.0`` instead of ``inf``, float floor
   division with a negative divisor using the dividend sign, and Python3
   float power with a negative base and fractional exponent raising
   ``ValueError`` instead of giving a complex result. Python2 in-place
   complex power now delegates to ``PyNumber_InPlacePower``, which
   handles the coercion that the generic helper path did not. Sequence
   repeat factors at the ``Py_ssize_t`` boundaries are now handled, and
   the type shapes of power operations include the possible results and
   exceptions.

   .. code:: python

      print(2.0 ** float("inf"))
      print(0.0 ** -float("inf"))
      print(1.0 // -2.5)
      print((-1.0) ** 0.5)

      # 4.3: 0.0, 0.0, -0.0, ValueError
      # 4.4: inf, inf, -1.0, (6.123233995736766e-17+1j)

-  **Compatibility:** Fix, type shapes disagreed with CPython for some
   operations: ``bytes + bytearray`` was considered ``bytearray``
   instead of ``bytes``, ``type < type`` on Python3 was considered
   unable to raise although metaclasses can overload it, ``int()``,
   ``long()``, and ``float()`` of ``bytearray`` were rejected as
   impossible at compile time, and ``None | type`` on Python 3.10+ was
   rejected instead of producing a ``types.UnionType``.

-  **Compatibility:** Fix, compilation of some ``enumerate`` and ``zip``
   calls failed because calls known not to raise still jumped to an
   exception exit the function did not have. ``needs_check`` is now
   passed from ``mayRaiseException``, ``enumerate`` start values and
   ``zip`` strict truth checks are considered potentially raising, and
   ``mayRaiseExceptionIndex`` and ``mayRaiseExceptionIter`` shape
   methods were added.

-  **Compatibility:** Fix, ``next`` with a default value crashed for
   values that are not iterators. It now checks ``HAS_ITERNEXT`` and
   raises CPython's ``TypeError``, and uses the optimized iterator path
   when the value is known to be an iterator.

-  **Compatibility:** Fix, the keyword argument specs of some built-in
   methods were wrong: ``dict.get``, ``pop``, ``setdefault``,
   ``fromkeys``, and Python2 ``has_key`` accepted keyword arguments that
   CPython rejects, while ``str.replace`` on Python 3.13+ now allows
   ``count`` as a keyword, and ``bytes.translate`` on Python 3.6+ allows
   ``delete`` as a keyword, with the other arguments remaining
   positional-only. The positional-only argument error in ``matchCall``
   now gives CPython's "takes at least N positional arguments" message.

-  **Compatibility:** Fix, truth checks of comparison results converted
   ``CHECK_IF_TRUE`` to ``nuitka_bool`` with a ternary, so an exception
   raised by ``__bool__`` was silently turned into false.
   ``CHECK_IF_TRUE_NBOOL`` now preserves the exception indicator, and
   the comparison and binary operation helpers use it, so e.g. a
   comparison yielding an object whose ``__bool__`` raises now
   propagates the exception.

   .. code:: python

      class BadBool:
          def __bool__(self):
              raise ValueError("no truth value")


      class Comparable:
          def __eq__(self, other):
              return BadBool()


      [Comparable()] == [Comparable()]  # now raises ValueError

-  **Compatibility:** Fix, when a module replaced itself in
   ``sys.modules`` while executing, the loader used the replacement for
   the load state too, so compiled code's frame globals became the
   replacement, which may lack ``__builtins__``. The executed module is
   now kept in the load state, and only the importer receives the
   replacement.

-  **Compatibility:** Fix, class base ``__mro_entries__`` results were
   extended directly, so a non-tuple result was accepted or failed
   differently. The result is now stored in a temporary and checked to
   be a tuple in full compat mode, raising ``TypeError`` like CPython.

-  **Compatibility:** Fix, ``super()`` with deleted implicit arguments
   compiled a reference to a variable without a value instead of raising
   CPython's ``RuntimeError``, e.g. "super(): empty __class__ cell" or
   "super(): arg[0] deleted". These errors are now raised when the
   traces show the arguments are unset, and full compat mode also
   observes a dynamically shadowed ``super`` in the module namespace.

-  **Compatibility:** Fix, variable deletions in full compat mode did
   not update the line number before generating the deletion, so errors
   raised by ``del`` reported the line of the previous statement. The
   line number is now updated first.

-  **Compatibility:** Fix, resuming a generator did not check for
   pending calls and signals, so a ``KeyboardInterrupt`` was delivered
   later in the caller instead of at the ``yield`` expression like
   CPython's ``RESUME`` instruction. The check now happens when the
   generator is resumed, excluding ``throw`` into the generator, which
   already has an exception set.

-  **Compatibility:** Fix, ``eval``, ``exec``, and ``execfile``
   evaluated the globals and locals arguments before the source code or
   filename, so function calls and other side effects in expressions
   like ``eval(source(), globals())`` happened out of order. The source
   is now stored in a temporary variable first, preserving CPython's
   evaluation order.

-  **Debugging:** Fix, on Windows, the PDB file of an unstripped target
   was left in the build directory after moving the executable, so it
   was lost. It is now moved next to the final binary, and the ``.pdb``
   suffix is cleaned up with the other intermediate files.

-  **Cache:** Fix, the bytecode cache did not restore whether a module
   usage source reference was internal, so warm-cache compilation
   reports could differ from cold-cache ones. The cache format now
   stores and restores that flag.

-  **Onefile:** Fix, the compressed payload body size was written in
   little-endian, while the C bootstrap reads it with a direct
   ``memcpy``, so compressed onefile payloads were broken on big-endian
   systems. The size is now written in native endianness.

-  **Scons:** Fix, the exit code of a Scons build did not distinguish
   signal termination, because ``os.WEXITSTATUS`` was used
   unconditionally. Signal exits now report the negative signal number.

-  **Scons:** Fix, MSVC builds with Python 2.6 headers warned about
   C4273 from the declarations of ``acosh``, ``asinh``, ``atanh``, and
   ``log1p``. That warning is now disabled for this combination.

-  **Scons:** Fix, the ``-Wc23-extensions`` diagnostic pragma was
   emitted for all resource modes and all Clang versions, so older Clang
   could fail on the unknown warning group. It is now emitted only for
   the ``#embed`` resource mode and Clang 19 or later.

-  **Scons:** Fix, constant blob filenames in generated code used
   backslashes, and the MinGW symbol name got a leading underscore on
   all architectures, so 64-bit MinGW builds could fail to link the
   blobs. Forward slashes are now used for the paths, and the underscore
   is only added for 32-bit x86.

-  **UI:** Fix, conflicting data file destination paths were only
   detected for exact path matches, so non-normalized paths could fail
   later at run time. Conflicts now use normalized paths and
   case-insensitive comparison on such file systems, with an error that
   names the reason.

-  **UI:** Fix, ``--version`` required a usable C compiler and could
   give an error message or attempt downloads. It now uses a download
   mode of ``no`` and reports ``Version C compiler: not found.``
   instead, and the separate ``assume_yes_for_downloads`` and
   ``download_ok`` flags were merged into one download mode of ``no``,
   ``ask``, or ``yes``.

-  **Reports:** Sensitive option values are now redacted in compilation
   reports and container command output by matching option name
   patterns, including abbreviated long options, with default patterns
   for ``password``, ``salt``, and ``secret`` options.

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

-  **Standalone:** Extended ``vLLM`` and added ``SGLang`` support,
   including the CUDA, NCCL, and NVSHMEM binding layers, ``cutlass``,
   and kernel packages such as ``flash_attn``, ``flashinfer``,
   ``sgl_kernel``, ``triton_kernels``, ``deep_ep``, ``deep_gemm``,
   ``quack``, ``xgrammar``, and ``kernels``, with their metadata, data
   files, CUDA and Triton kernel sources, and ``*.jinja`` chat
   templates.

-  **Standalone:** Added support for the ``triton`` package, including
   implicit imports for its backends, data files for the AMD and NVIDIA
   backends and their ``driver.c``, Python headers for in-place C
   compilation, and a replacement for ``triton_key`` with the value of
   the build environment. The ``cuda_utils`` module is not covered yet.

-  **Standalone:** Avoided including the Qt plugins and fonts of
   non-headless ``opencv-python`` when a Qt binding plugin is enabled,
   since they conflict with the binding's own Qt libraries, and added a
   warning recommending ``opencv-python-headless`` instead.

-  **Standalone:** Added support for newer ``astropy`` versions. PLY
   parser construction methods now request frame locals through the new
   ``frame_locals`` configuration, generated lexer and parser tables are
   included as implicit imports and no longer written into the compiled
   program's directory, IERS data files are included, and the constants
   data modules use wildcard imports.

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

-  **Onefile:** Enhanced payload caching. The payload now starts with a
   table of contents containing checksums, sizes, and symlink and
   executable flags, so unpacked files can be validated without
   decompressing the payload. The CRC32 is encoded in the file
   modification time, and the deprecated ``--onefile-as-archive`` option
   is now a no-op and hidden, with the separate compression cache and
   its ``--disable-cache=compression`` name removed.

-  **Plugins:** The ``source-inclusion`` plugin now supports module
   mode. Since there is no unique main program,
   ``--source-inclusion-main`` names a program that exercises the
   compiled module, and the recorded source hook is installed before the
   top-level module body. The ``dash`` package configuration now warns
   when ``dash.long_callback`` uses ``inspect.getsource()`` for caching
   and recommends the plugin and option.

-  **macOS:** Added support for C backtraces with
   ``--experimental=dump-c-tracebacks``, including Mach-O symbol lookup
   and signal-context unwinding on x86_64, i386, and ARM64.

-  **UI:** Added a ``barflow`` progress bar backend, selectable with
   ``--progress-bar=barflow``. It is not selected by ``auto``, which
   still prefers ``tqdm`` and then ``rich``.

-  **Targets:** Added the experimental ``nuitka.targets`` package with
   ABI specifications for the native platform, ``wasm32-wasi``, and
   ``i686-w64-mingw32``, carrying C ``long`` and ``long long`` sizes,
   pointer size, binary format, RPATH usage, and Python digit limits.
   ``--target`` now defaults to ``native`` and accepts aliases such as
   ``wasi``, ``wasm32-wasip1``, ``win32``, and ``windows-x86``, and
   unknown targets are rejected. Code generation takes C type limits
   from the selected target instead of the running Python.

-  **WASI:** Added experimental cross compilation and runtime support
   for ``--target=wasm32-wasi``. It uses Clang mode with WASI SDK 20,
   downloaded and cached unless ``--wasi-sdk-path`` is given, and a WASI
   CPython prefix, downloaded and cached unless ``--wasi-python-prefix``
   is given. Binaries get the ``.wasm`` extension and are run through
   Wasmtime 50, with DLL detection and extension module loading skipped
   for the target.

-  **Win32:** Added the experimental ``i686-w64-mingw32`` cross target.
   ``--win32-python-exe`` starts the 32-bit Windows Python as a broker
   to query its prefix, include path, DLL, and static library,
   translating paths with ``wslpath``, ``winepath``, or relative to the
   executable. Produced binaries are run directly on Windows and WSL,
   and through Wine on other hosts. Non-Windows hosts require ``--zig``.

-  **Targets:** Compile-time evaluation now runs in the target Python
   through a framed JSON broker. Hard import constants,
   ``sys.version_info`` values, and ``importlib`` package discovery use
   the target, so version-dependent constants and module availability
   follow the target rather than the host. Targets without DLL support,
   such as WASI, skip DLL detection entirely.

-  **No-GIL:** Added experimental support for compiling and running with
   free-threaded Python builds. Compiled types use per-free-list locks,
   list operations use critical sections, dictionary helpers have
   borrowed and new-reference variants for free-threaded builds, frame
   caches are thread safe, and pending calls are processed at thread
   checkpoints. Testing is ongoing, with Python 3.13t best covered so
   far.

-  **UI:** The recommended Python version for commercial usage was
   bumped to 3.13.

-  **Debugging:** Added ``--debug-thread-sanitizer`` for GCC and Clang
   on Linux and macOS, passing ``-fsanitize=thread`` to the compiler and
   linker and keeping debug information. It cannot be combined with
   ``--debug-address-sanitizer`` and is not available on Windows. For
   compiled extension modules, the host program must preload the
   ThreadSanitizer runtime, e.g. via ``LD_PRELOAD`` on Linux or
   ``DYLD_INSERT_LIBRARIES`` on macOS.

-  **Plugins:** Added a ``frame_locals`` anti-bloat configuration item
   and ``decideNeedsFrameLocalsProxy`` plugin hook, which decide per
   function or class whether a frame locals proxy is needed, using
   qualified name patterns. The locals struct is still only published in
   the frame when required, keeping the normal case faster and more
   compact. Added a ``QualifiedName`` base class so function and class
   qualified names can be matched like module names.

-  **Plugins:** Added a non-deployment handler for ``pickle`` that turns
   an ``ImportError`` raised while loading pickle data into a
   ``RuntimeError`` naming the missing module and recommending
   ``--include-module`` for it. The standard library package
   configuration was also split into shared, Python2-only, and
   Python3-only files, so Python3 compilations no longer load the
   Python2-only parts.

-  **Python 3.15+:** Added support for the ``sentinel`` built-in,
   including the correct ``__module__`` value for sentinels created in
   compiled code, type shape and attribute knowledge, and PGO type
   checks.

-  **Module:** Added ``--module-force-namespace``, which requires a
   compiled module to be loaded below the given namespace, with an empty
   namespace requiring top-level loading. This makes ``__name__`` and
   ``__package__`` compile time constants and allows more optimization
   in module mode.

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

-  **Imports:** Compiled modules and startup modules such as the main
   module, ``__parents_main__``, multiprocessing, joblib, and anyio
   helpers now load through their loader entries directly.
   ``ModuleSpec`` values carry a loader instance, module directory and
   file values use the runtime module name when available, and repeated
   ``findEntry`` lookups and extra C-API calls during startup are
   avoided.

-  **Variables:** Value traces now detect more local variables as
   definitely initialized, and unused variables are removed from local
   dict mappings, e.g. ``__class__`` after its ``super`` usage
   disappears, reducing unbound-local error handling and locals dict
   overhead.

-  **Code Generation:** Annotate functions that can be re-entered now
   share a cached code object instead of unmarshalling it for each
   function, and class bodies are no longer assumed to be able to
   recurse, avoiding unnecessary frame handling.

-  **Subscripts:** Constant subscripts of tuples and tuple subclasses,
   e.g. named tuples, now use a direct table access fast path, with
   ``IndexError`` messages matching tuples.

-  **Hard Imports:** Added hard import nodes for ``os.path.join``,
   ``importlib.resources.open_binary`` and ``open_text``, and
   runtime-relative paths, plus a vectorcall-based
   ``CALL_FUNCTION_WITH_ARGS`` helper used by ``print`` and ``zip``.

-  **Optimization:** More C-API calls were replaced with Nuitka helpers,
   including ``CHECK_AND_CLEAR_ATTRIBUTE_ERROR_OCCURRED`` and
   ``CHECK_AND_CLEAR_TYPE_ERROR_OCCURRED``, reducing temporary exception
   handling in generated code.

-  **Optimization:** All direct CPython dictionary access in
   Nuitka-owned code now goes through the ``DICT_`` helpers implemented
   directly on the ``PyDictObject`` state, so dictionaries can still be
   freely passed between Nuitka and CPython. Added
   ``DICT_SET_ITEM_STRING``, ``DICT_REMOVE_ITEM_STRING``,
   ``DICT_GET_ITEM_STRING``, ``DICT_UPDATE_FROM``, and
   ``DICT_UPDATE_FROM_SEQ``, replacing ``PyDict_SetItem``,
   ``PyDict_DelItem``, ``PyDict_GetItemString``, ``PyDict_Merge``,
   ``PyDict_MergeFromSeq2``, and ``PyDict_Update`` in the loader,
   exception state handling, built-ins, attributes, keyword arguments,
   frame locals, and deepcopy.

-  **Optimization:** Added dictionary set implementations without Python
   C-API calls for all supported versions, generated from a template and
   using dedicated lookup functions instead of the CPython lookup
   function pointers. Added ``DICT_SET_ITEM1``, which consumes the value
   reference on success and failure.

-  **Optimization:** Used ``CHECK_IF_TRUE`` for truth checks and
   ``RICH_COMPARE_*_NBOOL_*`` for comparisons, compared with ``Py_None``
   directly since ``Py_IsNone`` is not available on all supported Python
   versions, and used ``Nuitka_PyLong_AsLongAndOverflow`` in
   ``sys._getframemodulename``, avoiding calls into the Python C-API
   implementation.

-  **Optimization:** Added ``Nuitka_PyLong_AsSsize_t``,
   ``Nuitka_PyLong_AsSsize_tAndOverflow``, and
   ``Nuitka_Number_AsSsize_t``, replacing the Python C-API equivalents
   in slicing, subscripting, list indexing, and ``int`` construction,
   with the version-specific overflow and type error messages preserved.

-  **Strings:** Added specialized operation nodes for the ``casefold``,
   ``isascii``, ``isdecimal``, ``isidentifier``, ``isnumeric``, and
   ``isprintable`` methods of ``str``, so calls to them compile to
   direct helpers instead of generic method calls.

-  **Variables:** Added ``getUnboundLocalErrorMessage``, which uses the
   short message unless full compat mode is enabled, avoiding the
   code-object based message construction. Frame-less outline code such
   as comprehensions now generates ``Nuitka_FormatUnboundLocalError``
   instead of asserting that a frame based error is available.

-  **Trace Collections:** Trace collection merging now copies the first
   collection's dictionary and uses lists instead of sets for the
   normally small version collections, avoiding generator and set
   objects and speeding up compilation by about 5%.

-  **Trace Collections:** Merge trace flattening and deduplication moved
   to the collection layer and only happens when a nested merge is
   present, with a direct two-trace merge path. The loop dependency and
   cached must-have-value state of merge traces are now a single state
   field, and single-predecessor behavior moved into a mixin, reducing
   per-merge memory use and speeding up decisions.

-  **Trace Collections:** The value trace implementation moved to
   ``nuitka.optimizations.value_traces``, with generated
   ``ValueTraceMerge2`` through ``ValueTraceMerge6`` classes that use
   direct trace slots and unrolled hot methods. Nested merges are
   flattened through dedicated helpers, and two-trace merges are
   special-cased, saving memory and avoiding loops for the common merge
   sizes.

-  **Frame Caching:** Compiled frame caches now use a
   ``Nuitka_FrameCacheHandle`` with an in-use flag, falling back to an
   uncached frame when another call owns the cache. Idle cached frames
   drop their hidden locals and are untracked by the garbage collector,
   and ownership is tracked for normal returns, exception exits, and
   generator frames.

-  **Scons:** Scons builds now use a generated
   ``source_files_index.txt`` created after generated sources are
   complete, instead of scanning source directories, so the backend,
   offsets, and onefile builds use the precise list of generated files
   and avoid directory scans.

-  **Trace Collections:** ``mustHaveValue`` queries now pass a per-query
   context that caches loop dependent merge results, so shared trace
   subgraphs are not revisited exponentially. Results that depended on a
   loop recursion assumption are discarded when the assumption no longer
   applies.

-  **Dictionaries:** Dictionary mutation helpers now pass the thread
   state through, so watcher callbacks and free-threaded operations can
   use it. Added hash and equality supplied lookups for cache
   dictionaries and free-threaded set and delete implementations, and
   preserved watcher bits in version tags.

-  **Dictionaries:** Added ``MAKE_DICT_FROM_KWARGS`` and used it in the
   generated call helpers, replacing the repeated private
   ``_PyDict_NewPresized`` and set loop for keyword arguments.

-  **Dictionaries:** Added ``MAKE_DICT_PRESIZED`` and a unicode-only
   variant, so dictionaries with constant string keys use a compact keys
   object, and used the unicode variants at C call sites with known
   string keys. The keyword argument dictionary is pre-sized and uses
   the unicode-only keys object.

-  **Dictionaries:** Added untracked set variants that skip garbage
   collection tracking and watcher notifications for Nuitka-owned
   dictionaries, and used them for dictionary creations and constant
   caches, also using value reference ownership transfer.

-  **Dictionaries:** Added constant blob tags for empty dictionaries and
   for dictionaries and frozendicts with unicode-only keys, and the blob
   decoder now uses the pre-sized dictionary helpers.

-  **Dictionaries:** Dictionary and frozendict copies now use the
   pre-sized dictionary helpers, with the unicode-only keys variant when
   possible.

-  **Optimization:** Tuple and dictionary untracking is now implemented
   locally instead of using private CPython garbage collection API
   calls, making garbage collection of containers faster.

-  **Optimization:** Added ``LIST_DEL_SLICE`` for exact list slice
   deletion, with the same index clamping as ``PyList_SetSlice`` and
   deferred reference releases, and used it for ``sys.path`` and joblib
   argument cleanup in the main program.

-  **Imports:** Added dedicated nodes for ``sys.modules`` lookups,
   ``get``, ``pop``, assignment, and deletion, using the loader entry as
   the source of truth for included modules. ``importlib.reload`` is
   supported for private modules, which are kept out of ``sys.modules``
   and marked in the compilation report.

-  **Standalone:** Copied ELF and Mach-O shared libraries and extension
   modules are now stripped of symbols unless ``--unstripped`` or a
   debug or runtime trace mode requires them, reducing the size of
   standalone distributions. Known ``strip`` failures leave the file
   unstripped instead of aborting.

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

-  **Packages:** Allowed ``setuptools`` where Triton kernels and
   in-place extension builds require it, and dropped ``tilelang`` and
   heavy test-only ``torch`` modules from serving builds.

-  **Packages:** Avoid docstring dependencies and set
   ``TORCH_COMPILE_DISABLE`` for vLLM serving, worked around empty
   ``entry_points()`` truth values, and replaced the forked subprocess
   model inspection in ``vllm.model_executor``.

-  **Telethon:** Disabled docstrings for ``telethon`` and avoided
   following its optional ``PIL`` dependency in
   ``telethon.client.uploads``, which is only used for image thumbnails.

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

-  **Docs:** Expanded the Developer Manual's CPython API to Nuitka
   helper mapping table with more helpers, ownership and precondition
   details, generated helper families, and version-specific internals
   for 3.13 and 3.14.

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

-  **Quality:** Private pip tools now fall back to the private pip space
   when an installed package raises any exception during import, not
   only ``ImportError``. When the private space contains both
   ``site-packages`` and ``dist-packages`` layouts, the layout of the
   Python that runs pip, and the one a tool binary belongs to, are
   preferred on ``PYTHONPATH``.

-  **Debugging:** GCC and Clang builds now enable ``-Wshadow``, so
   accidental variable shadowing is detected during regular builds
   instead of only in later MSVC CI runs.

-  **Zed:** The editor configuration now excludes generated and build
   artifacts from file scanning and restricts basedpyright diagnostics
   to open Python files.

-  **Watch:** The watch tool now passes ``--update-check=never`` to
   Nuitka, avoiding update check noise for its test compilations.

-  **Watch:** The watch tool now records the case version and case file
   hash in its reports, so a changed version triggers recompilation.
   Build directories are removed after execution via
   ``--remove-output``.

-  **Quality:** Updated all tools to the latest versions, including
   ``black`` 26.10.1, ``isort`` 9.0.2, ``yamllint`` 1.38.0,
   ``clang-format`` 23.1.3, ``codespell`` 2.4.3, ``pylint`` 4.1.3, and
   ``astroid`` 4.3.4, and split the ``jsonschema`` and ``tomli``
   requirements by Python version.

-  **Actions:** Updated the GitHub Actions to ``actions/checkout@v7``,
   ``actions/setup-python@v7``, and ``actions/upload-artifact@v7`` for
   Node.js 24 support, and replaced ``ilammy/msvc-dev-cmd`` with
   ``TheMrMilchmann/setup-msvc-dev@v4``.

-  **Quality:** PyLint is now used from the global environment when the
   installed versions of ``pylint`` and ``astroid`` match the required
   ones, without prompting for downloads. The existing private pip space
   is consulted even without download permission, and a missing PyLint
   is now an error instead of a silent success.

-  **RPM:** Fix, the spec file conditions for Fedora and RHEL Python2
   packages were also true on openSUSE 16, where the Fedora and RHEL
   macros are unset. The conditions are now guarded so they only apply
   when ``suse_version`` is below 1600.

-  **Quality:** Consolidated the MSVC warning flags so ``/W4``, the
   intentional-construct suppressions, and ``/WX`` are applied as a set
   when C compiler warnings are made errors in debug mode, and
   ``-Wno-unused-but-set-variable`` is selected by compiler mode and
   version.

-  **Debian:** Added ``python-atomicwrites`` to the build and runtime
   dependencies where ``base-files`` does not provide it, and moved the
   source copy and permission fixup for Debian builds into shared code
   used by both the regular and the mentors packaging, so permission
   fixups also apply to mentor builds.

-  **Debian:** The WSL clock is now synchronized before a Debian package
   build starts, since clock skew breaks builds and package repository
   signatures.

-  **Quality:** ``codespell`` now accepts the git arguments of the other
   quality tools and uses the git paths by default, and shell pattern
   expansion is shared through ``resolveShellPatternsToFilenames``.

-  **Quality:** The ``-Wcast-function-type-strict`` suppression is now
   only used where the compiler actually supports the warning instead of
   for all Clang versions, avoiding warnings on older Clang.

-  **Quality:** Pyright now targets Python 3.15 and ignores vendored
   ``inline_copy`` code.

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

-  Extended the power operator tests with a literal base to cover
   underflow and subnormal results at run time.

-  Tests now honor ``--mode=standalone`` and ``--mode=onefile`` from
   ``NUITKA_EXTRA_OPTIONS``, removing them before passing options to
   Nuitka, so test setups can select the compilation mode without
   duplicating it.

-  Added ``nuitka.tools.testing.Coverage`` with shared coverage command
   wrapping and publishing. Coverage data in SQLite format is now
   normalized in the database, and the CPython comparison, optimization
   tests, and test runner use the helper.

-  The test runners now report whether the tested Python has the GIL
   enabled, so free-threaded interpreters are distinguishable in
   outputs.

-  Output comparisons now allow process ID differences in test support
   temporary names, matching the normalization already done for ``/tmp``
   and Windows temp files.

-  The CPython results cache is now written to a temporary file and
   moved into place atomically, so a crash cannot leave a truncated
   cache file. Damaged cache files are reported and the results
   recalculated.

-  Reference count checks now use the object based count for
   free-threaded builds before Python 3.14, where deferred reference
   counting makes ``sys.gettotalrefcount()`` unreliable, while debug
   builds with the GIL and Python 3.14+ free-threaded builds keep the
   faster total count.

-  Output comparisons now strip the CPython 3.15 hint about site
   initialization being disabled from import errors, since Nuitka's
   subinterpreters inherit the delayed site import state.

-  Extended the dictionary structure tests with same-value update checks
   and C helper operations through a test plugin, and added a standalone
   concurrency harness that links the dictionary helpers and drives
   shared dictionaries from native threads.

-  The package test runner now falls back to ``__init__.py`` for project
   options when a package directory has no ``__main__.py``, uses
   per-test ``--mode=module`` project options, and the top level
   attributes entry point is now actually tested.

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

-  **Progress:** Progress bars now use a ``withProgressBar`` context
   manager for C source generation, DLL copying, and DLL detection,
   ensuring they are closed on errors.

-  Removed the fallback for unbound local errors without a frame, which
   is no longer reachable and now asserts instead.

-  **LSP:** Added missing includes and configured ``.c`` and ``.h``
   files as C in clangd, reducing spurious diagnostics.

-  Removed the unused ``DICT_GET_ITEM_WITH_HASH_ERROR0`` and
   ``MODULE_NAME0`` helpers, converting their remaining callers to the
   new-reference variants and updating the Developer Manual mapping
   table.

-  Added ``getPathWithForwardSlashes`` and use it for git paths, IDE
   configuration, and adapted Python header filenames, avoiding
   replacement of backslashes that are valid filename characters on
   MSYS2 flavor.

-  Added ``NUITKA_UNREFERENCED_PARAMETER`` macro for intentionally
   unused C parameters and marked the onefile fatal error helpers and
   the corruption abort helpers as non-returning with
   ``NUITKA_NO_RETURN``, dropping unreachable returns.

-  The ``PYTHONPATH`` separator in ``callExecPython`` now uses
   ``getEnvironmentPathAdded``, so the platform path separator is used
   on Windows too.

-  **Python 2.6:** Added ``_PyObject_GC_IS_TRACKED`` and
   ``_PyObject_GC_MAY_BE_TRACKED`` equivalents, so GC tracking code no
   longer needs version-specific dummy checks.

-  Warning filters for ``DeprecationWarning`` and ``SyntaxWarning``
   moved into ``nuitka/__init__.py``, so all tools importing Nuitka
   modules get them automatically, and the ``withNoSyntaxWarning``
   helper was removed.

-  Child processes now receive an explicit copy of the environment with
   added paths, using ``getEnvironmentWithPathAdded``,
   ``getPrivatePipSitePackagesEnvironment``, and ``getExecutablePath``
   with ``extra_dir``, instead of temporarily modifying ``os.environ``.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
