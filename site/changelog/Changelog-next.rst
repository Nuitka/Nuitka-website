:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.4rc13**.

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

-  Fix, the loader built the containing package name in a fixed size
   buffer without checking the length, so a module name longer than the
   buffer could overflow it. Longer names are now rejected before
   copying, matching the entry name comparison that already rejected
   them.

-  Fix, the safe string helpers did not reserve room for the terminating
   NUL when appending wide strings, and copying wide strings checked the
   buffer while writing instead of checking the source length up front.
   Appending now requires room for two characters, and copying verifies
   the source length first.

-  Fix, cloning function bodies together with an enclosing outline scope
   did not translate their closure and taken variables, so cloned
   generator, lambda, and comprehension bodies could reference variables
   of the original scope. Closure variables and taken variables are now
   translated, with tests for generator and lambda closures in list
   contractions and cloned ``finally`` blocks.

-  Fix, error path checks compared unicode filenames and messages with
   ``strcmp`` on a temporary UTF-8 encoding, which could fail while
   handling another exception. Added
   ``Nuitka_Unicode_CompareWithASCIIString``, which compares ASCII text
   without encoding or raising, and used it for these checks.

-  Fix, a file lock acquired through ``withFileLock`` was released only
   after the ``yield``, so an exception left it held. The release now
   happens in a ``finally`` block.

-  Fix, the retry decorator reported and slept after the final attempt,
   so a final failure was delayed by another retry interval. The retry
   message and sleep now only happen when another attempt remains, and
   the final failure is reported immediately.

-  Fix, ``set`` construction and set displays leaked the partially built
   set when an element expression raised through a nested cleanup block,
   e.g. for ``s = {1, [1, h()]}``. The set now has a local exception
   target and is released before jumping to the enclosing handler.

-  Fix, plugin-provided package extra scan paths were applied to
   subpackages using the parent package directory, so imports could be
   scanned from the wrong location. They now use the candidate directory
   of each subpackage, are only considered when it exists, and missing
   import warnings name the actual import source instead of the
   importing module.

-  Fix, ``StopIteration`` and ``StopAsyncIteration`` subclasses raised
   by generators, coroutines, and async generators were not converted to
   ``RuntimeError``, since the code compared the exception type pointer
   instead of matching the exception. Exception matching is now used, so
   subclasses are converted too.

-  Fix, the handled exception state was not kept in generator,
   coroutine, and async generator objects while they ran, so
   ``sys.exc_info()`` and implicit chaining were wrong, and throwing
   into a suspended object on Python 3.9+ did not chain to its handled
   exception. The handled state is now kept in the object while it runs,
   chained when throwing, and the caller state restored afterwards.
   Saved exceptions are restored and cleared when yielding outside a
   handler on Python up to 3.6, and ``yield from`` preserves the handler
   state across delegation and forwards sent values to delegated
   generators.

   .. code:: python

      def gen():
          try:
              raise KeyError("handled")
          except KeyError:
              yield


      generator = gen()
      next(generator)

      try:
          generator.throw(ValueError("thrown"))
      except ValueError as exception:
          print(exception.__context__)

      # 4.4rc8: None on Python 3.9+ (wrong)
      # 4.4rc9: KeyError('handled')

-  Fix, calls to C functions using ``METH_FASTCALL``, with or without
   ``METH_KEYWORDS``, dispatched with the wrong argument counts and
   tuple usage on some Python versions. The fast call variants are now
   selected by exact flags, and missing error checks and reference
   handling for method descriptors, ``__init__`` results, and called
   objects were added, avoiding leaks on rare errors.

-  Fix, the ``ascii`` specialization used the ``repr`` parameter spec,
   and the ``issubclass`` specialization used the ``isinstance`` spec,
   so argument handling and errors could be wrong. Each now uses its own
   spec.

-  Fix, async methods with class-private names were not mangled, because
   the source or bytecode function builder received the unmangled name,
   so the method was bound under its source name. The mangled binding
   name is now passed for normal and async functions, while the
   function's ``__name__`` stays unmangled like CPython.

-  Fix, the DLL subdirectory search did not normalize the search root
   and parent candidates, so a path with a trailing slash could make the
   walk up to the root loop endlessly. The paths are now normalized and
   termination is asserted.

-  Fix, slice handling had several issues: a step of 1 was optimized
   away although it is observable in the resulting slice, constant
   ``None`` bounds were treated as values, and integer constants were
   not distinguished from other small number constants. Only a ``None``
   step is removed now, ``None`` bounds are unbounded, and integer
   constants use their index value.

-  Fix, the exact frozenset shape mixin overrode the list shape
   predicate instead of the frozenset one, so frozenset exact shapes
   were misreported. It now overrides ``hasShapeFrozensetExact``.

-  Fix, ``close()`` on generators and coroutines returned a boolean
   internally, so compiled frames could not distinguish success from an
   exception or release the close result. The close helpers now return
   the result object, and Python 3.13+ returns the value of a
   ``StopIteration`` raised while handling ``GeneratorExit``.

-  Fix, runtime helpers had several garbage collection and reference
   issues: function objects did not visit their defaults, keyword
   defaults, annotations, type parameters, and annotate functions; type
   parameters were not cloned; function table offset bounds and code
   object description fields were wrong; and coroutine origin frames,
   frozen module detection, and loaded extension module references were
   handled incorrectly. The traversal, cloning, bounds, descriptions,
   frame counting, detection, and references are now correct.

-  Fix, statement code generation replaced the current source reference
   without restoring it, and exception normalization used the statement
   source reference instead of the exception type's. The previous
   reference is now restored in a ``finally`` block, and exception
   normalization uses the exception type's reference.

-  Fix, locals dictionary deletions did not apply tolerated deletions
   correctly, and synchronization did not release the locals mapping.
   Deletions now clear errors when tolerated and raise the proper
   ``NameError`` otherwise, the mapping is released after
   synchronization, and the closure check for ``exec`` uses the correct
   Python version. Exact dictionaries now only raise for a name that was
   never set, while value finalizer exceptions are ignored like CPython.

-  Fix, attaching ``name`` and ``path`` attributes to ``ImportError``
   and ``AttributeError`` overwrote existing references without
   releasing them, and used the outer temporary instead of the actual
   exception object. ``Py_XSETREF`` and the actual exception value name
   are now used.

-  Fix, dual-typed ``int``/``long`` values had multiple bugs, including
   missing truth checks and assignment conversions, incorrect reference
   handling for in-place assignments, and wrong object value accesses.
   Truth checks and conversions were added, references are now released
   and taken correctly, and exception checks use the validity field.

-  Fix, range and xrange element value predictions used off-by-one index
   bounds, mishandled a zero step, estimated lengths incorrectly for
   negative steps, and checked the upper bound in the wrong direction.
   The bounds, length estimates, and direction checks were corrected.

-  Fix, constant dictionary item lookups used the item node's own
   constant instead of the dictionary argument, so the wrong object was
   indexed, and ``dict.get`` extracted side effects from a nonexistent
   ``defaults`` child instead of the default node. Both now use the
   correct operands.

-  Fix, ``importlib.metadata`` integration reported found distributions
   as missing, and the standard and backport entry point value
   references used each other's base classes. Found distributions are
   now successful, and each implementation uses its own base classes.

-  Fix, ignored directory and filename matching was case-insensitive in
   some places but not others, and single suffix strings could be
   treated as iterables of characters. The matching is now shared and
   normalizes both sides.

-  Fix, a class whose name consisted only of underscores produced an
   empty mangling prefix, so private names were mangled differently.
   Such classes now leave private names unmangled, matching CPython.

-  Fix, ``NuitkaCalledProcessError`` did not initialize its base class,
   so the exit code and command were not stored, and missing optional
   tools returned bytes when text was requested and vice versa. The base
   initializer is now called, and the empty result matches the requested
   text or bytes decoding.

-  Fix, module version comparison did not pad detected versions with
   zeros and kept comparing after a detected part was greater, so usable
   Python installations could be rejected. Detected versions are now
   padded, and comparison stops when a part is greater.

-  Fix, cloning class bodies dropped the class name, flags, qualname
   setup, deferred annotations, annotation state, and static attributes,
   and qualname references still pointed at the original body. The clone
   state is now preserved and qualname references are updated.

-  Fix, tree cloning could fail because several nodes lacked
   ``getDetails`` implementations or finalization, unresolved function
   references were not supported, and the compile node expected a
   different source parameter name. The missing details and finalization
   were added, and package resource usage attempts use the resolved
   package name. Parent and variable-trace references are now also
   cleaned up for locals, key/value, and assignment nodes that can be
   finalized after cloning.

-  Fix, non-constant key/value pair nodes called a nonexistent method
   when checking for constant string keys, so mapping detection could
   fail. They now use ``isExpressionConstantStrRef``.

-  Fix, cloned function bodies did not keep variables owned by the
   cloned scope, including locals dictionary, class, module, and
   import-star variables, so cloned code could refer to the original
   scope. The variables are now cloned with the scope, and the missing
   setters and class frame details were added. Function flags,
   auto-release variables, ``needs_creation`` and ``needs_direct``,
   qualname setup and provider, and non-local declarations are now
   preserved, provider translations keep qualname providers and outline
   entry points pointed at the clones, and cloned outlines get unique
   temporary variable names. Exec locals closure variables are
   translated when cloning and unregistered from the closure set, and
   class body clones translate their qualname provider as well.

-  Fix, function inlining did not apply cloned-scope translations to
   parameters, temporaries, taken variables, closures, and auto-release
   variables, and release statements kept the old node type when a
   variable changed class. The translations are now applied and release
   statements replaced.

-  Fix, borrowed values used as call arguments or binary operation
   operands could be released by later arguments that rebind the source
   variable, leaving a dangling reference. Such values are now promoted
   to owned references when a later expression may write the variable.

-  Fix, error results from ``DICT_HAS_ITEM`` and ``HAS_ATTR_BOOL2`` were
   treated as "not found" in fromlist imports, loader post-load binding,
   ``eval``/``exec``, and dictionary updates, and the compact dictionary
   lookup could leave its result pointer uninitialized. The errors are
   now propagated, the result pointer is initialized, and parent module
   resolution releases its temporary reference.

-  Fix, class namespace lookups treated exceptions from custom mappings
   as a missing name. The checks now mark the access as potentially
   raising and emit the error exit.

-  Fix, ``os.path.isabs`` used as a value had no code generation
   dispatch, so compilation failed. It is now dispatched like the other
   ``os.path`` hard imports.

-  Fix, method calls through a custom ``__getattribute__`` invoked
   ``__get__`` again on the returned callable data descriptor, so the
   descriptor was not called. The ``tp_getattro`` result is now used
   directly, and attribute lookup errors are propagated.

-  Fix, assigning to a read-only attribute whose class has a descriptor
   reported that the object has no such attribute. It now reports that
   the attribute is read-only.

-  Fix, a function dictionary ``__module__`` lookup error was ignored
   and fell back to the module name. The error is now propagated.

-  Fix, generated ``os.path.join`` calls did not emit the call line
   number, kept the argument array in function scope, leaked the result,
   and always checked for errors. The line number is emitted, the array
   is scoped, the result is cleaned up, and the error check only happens
   when the call can raise.

-  Fix, a yield-from target without a ``throw`` attribute was treated as
   a failed throw instead of delegating into the generator, and other
   attribute lookup failures were ignored. A missing ``throw`` now
   delegates, and non-``AttributeError`` failures propagate.

-  Fix, calls through an uncertain class-scope locals dictionary
   evaluated arguments twice or in the wrong order when a later argument
   changed the shadowing. Such calls are now outlined, evaluating
   arguments once in source order, with a conditional for the locals
   dictionary lookup.

-  Fix, replacing a call to a just-created function with a direct call
   dropped side effects from defaults, keyword defaults, annotations,
   and type parameters. Those are now evaluated before the direct call,
   and preserved on the exception path.

-  Fix, the unhashable-key ``TypeError`` for dictionary displays
   evaluated keys and values in the wrong order and could drop side
   effects. Preceding pairs, the key, and its value are now evaluated in
   source order before the error is raised.

   .. code:: python

      {[]: 1}  # TypeError: unhashable type: 'list'

-  Fix, the three-argument ``type()`` call always set ``__module__``
   from the compile-time module name after class creation, overriding
   the frame globals or metaclass behavior. ``type_new`` now resolves it
   from the active frame globals, only falls back when no frame is
   active, and handles non-type metaclass results and lookup errors.

-  Fix, building replacement ``TypeError`` messages released the
   original exception state before reading type names, and replaced
   exception values were not released. Messages are now built first,
   values are released correctly, and generator exception matching uses
   direct subtype checks on Python 3.

-  Fix, ``TUPLE_COPY`` filled the copied tuple with ``PyList_SET_ITEM``,
   and the long sign helpers overwrote unrelated tag bits and missed
   setting the digit size when updating from a C long. Tuple items use
   ``PyTuple_SET_ITEM``, the sign is masked, and the digit size is set.

-  Fix, resolved and unresolved binary paths shared one cache slot,
   ``print`` newline calls used stdout instead of the requested file,
   and Python 2 class ``__name__`` assignment checked for a dictionary.
   The caches are separate, the requested file is used, and ``__name__``
   requires a string.

-  Fix, docstring removal replaced any first ``Constant`` body
   expression with an empty string, including ``None``. It now only
   clears string constants, leaving other constants untouched for
   compatibility.

-  Fix, boolean assignments did not release the value used, and boolean
   and cell targets overwrote their old reference. In-place operations
   also lost ownership for module variables and cleanup temporaries. Old
   values are now released before replacement, boolean and cell targets
   use ``Py_NewRef_IMMORTAL``, and in-place operands keep correct
   ownership.

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

-  **Python 2:** Fix, ``str.translate`` and ``unicode.translate`` did
   not accept the optional ``delete`` argument, since the specialized
   nodes used a single argument spec for all versions. The specs are now
   split by Python version, and the Python 2 variant passes the
   ``delete`` argument.

-  **Python 3.13+:** Fix, the built-in ``eval``, ``exec``, ``locals``,
   ``vars``, and ``dir`` used CPython's frame locals proxy, which
   requires an exact frame object and fails for compiled frames. The
   builtins are now replaced with versions that supply globals and
   locals from compiled frames, installed after global constants and
   before module constants, with tests for indirect calls.

-  **Python 3.10+:** Fix, class patterns looked up each keyword
   attribute twice, because a separate existence check ran before
   ``MATCH_CLASS_ARGS``, which already checks keyword attributes and
   returns ``None`` when one is missing. The redundant lookup was
   removed.

-  **Python 3.14:** Fix, CPython 3.14 gives ``_PyObject_GC_TRACK`` and
   ``_PyObject_GC_UNTRACK`` file and line arguments, so headers that
   still called them bypassed Nuitka's replacements. The macros are now
   redirected to the Nuitka versions where CPython uses this signature.

-  **Python 2:** Fix, the ``long`` specialization used the ``int``
   parameter spec and an ``int`` constant, and the comparison helpers
   converted the left ``int`` operand instead of the right one. It now
   uses the ``long`` spec and constant, and the correct operand is
   converted.

-  **Python 2:** Fix, hashing of ``long`` values did not convert them to
   text, and booleans were not handled at all, so cache key generation
   could fail. ``long`` values are now converted to text, and booleans
   are hashed distinctly.

-  **Python 3.13:** Fix, frame clearing and GC traversal treated locals
   as owned even when the frame's locals pointer did not point at its
   own storage, so references from unowned locals could be traversed and
   released. Ownership is now checked before releasing or traversing
   locals.

-  **Python 3.14+:** Fix, writes of non-exact integers to dual-typed
   locals in the frame locals proxy were accepted, and the previous
   value was released before taking the new reference. Such writes now
   raise ``RuntimeError``, and the new reference is taken first.

-  **Python 3.13+:** Fix, ``locals()`` in optimized scopes returned the
   live dictionary, while PEP 667 makes it return a fresh snapshot. The
   locals copy node is now used there.

-  **Python 3.5+:** Fix, ``async for`` over values that are not async
   iterable did not raise the proper ``TypeError`` and could lose side
   effects when the check was decided at compile time. It now raises
   ``TypeError``, preserves side effects, and uses a separate slot for
   the async iterator minimum length.

-  **Python 2:** Fix, print statements with a value that had side
   effects failed to compile, because the side effects were not split
   into separate statements before replacing the print value. They are
   now split and the statement compiles.

-  **Python3:** Fix, compiled calls raised assertions or wrong messages
   for duplicate keyword arguments and non-string keyword names. They
   now raise ``TypeError`` like CPython in full compat mode, covering
   compiled functions, vectorcall, methods, and ``functools.partial``.

-  **Python 3.8+:** Fix, direct compiled function and method calls did
   not track recursion depth, so deep recursion could overflow the C
   stack instead of raising ``RecursionError``. Method calls now use the
   small stack, vectorcalls without keywords have a fast path, and
   keyword vectorcalls pass the argument offset.

-  **Python 3.9+:** Fix, formatting the abstract class instantiation
   error computed the method count after releasing the sorted method
   list, causing a use-after-free, and the message pluralization and
   wording did not match Python 3.9+ and 3.12+. The count is computed
   before release and the message matches CPython.

-  **Python 3.12+:** Fix, the import blocker used by import detection
   only implemented ``find_module``, which Python 3.12+ no longer
   consults, so modules that failed detection could be imported later.
   It now implements ``find_spec`` and keeps failed modules failed.

-  **Python3:** Fix, ``all`` and ``any`` on constant ranges computed
   wrong results for empty, negative, and negative-step ranges because
   range length and indexed values were simulated by iteration. They are
   now computed directly, with side-effecting bounds preserved.

-  **Python 3.13+:** Fix, class code objects and ``__firstlineno__``
   used the class line instead of the first decorator line, so they now
   match CPython.

-  **Python 2:** Fix, project variable keys were validated with
   ``str.isidentifier``, which does not exist on Python 2, so
   ``nuitka-project-set`` failed there. The shared
   ``isPythonIdentifier`` helper is now used.

-  **Python 2:** Fix, ``hasattr`` only suppressed ``AttributeError``,
   while CPython suppresses all exceptions from the attribute access. It
   now suppresses all exceptions on Python 2 and still only
   ``AttributeError`` on Python 3.

-  **Python3:** Fix, keyword-only defaults were resolved separately in
   each argument parser, and errors from keyword default dictionary
   lookups were ignored. The resolution is now shared, and lookup errors
   propagate.

-  **Python3:** Fix, keyword argument name comparisons that raised
   ``__eq__`` were treated as unmatched, hiding the exception. Errors
   now propagate for plain, star-dict, keyword-only, vectorcall, and
   ``eval`` calls.

-  **Python 3.6+:** Fix, ``throw()`` and ``asend().throw()`` did not
   pass the close-on-``GeneratorExit`` flag like CPython, so
   ``aclose()`` and nested coroutines could fail to close yield-from
   targets. The flag is now passed, exception clearing uses the shared
   helpers for ``StopIteration`` and ``GeneratorExit``, and the obsolete
   closing assertion was removed.

-  **Python 3.6+:** Fix, ``__init_subclass__`` and ``__class_getitem__``
   were always wrapped in ``classmethod``, even when decorated with
   ``staticmethod``, an explicit ``classmethod``, or a descriptor. They
   are now wrapped only when the final class dict entry is a plain
   function.

-  **Python 3.8+:** Fix, ``yield`` inside list, set, and dict
   comprehensions and directly in class bodies was accepted in some
   cases. It is now rejected with CPython's ``SyntaxError`` wording and
   source location, including comprehensions wrapped in outline
   functions.

-  **Python 3.10+:** Fix, the pattern matching argument count
   ``TypeError`` swapped the maximum allowed and actual counts and
   formatted ``Py_ssize_t`` with ``%d``. The counts are in the right
   order and use ``%zd``.

-  **Python 3.11+:** Fix, function body kind detection did not inspect
   comprehension elements, targets, or all generators, so nested
   ``await`` and ``async for`` inside generator expressions were missed.
   They are now inspected, and the body is marked asynchronous.

-  **Python 3.13:** Fix, freezing the GC during compilation corrupted
   object state on CPython 3.13.0 free-threaded builds. Freezing is
   skipped for that build, and the collector is unfrozen before
   finalization to avoid Python 3.11 debug build assertions.

-  **Python 3.13+:** Fix, ``update()`` and ``|=`` on the frame locals
   proxy only accepted dictionaries and proxy instances and used
   ``items()``, so dict subclasses with overridden ``items()`` or
   general mappings behaved incorrectly. General mappings and other
   proxies are now accepted via ``keys()`` and ``__getitem__``, and
   self-updates and mutation during iteration are handled.

-  **Python 3.13+:** Fix, defaults for ``TypeVar``, ``TypeVarTuple``,
   and ``ParamSpec`` were evaluated eagerly and passed as values, so
   forward references and lazy default evaluation failed. Deferred
   evaluation functions are now built, including starred
   ``TypeVarTuple`` unpacking, and passed through type aliases and
   runtime type parameter objects.

-  **Python 3.15:** Fix, ``bytes.replace`` did not mark ``old`` and
   ``new`` as positional-only starting with Python 3.15. The specs now
   match, and calls with those keywords are rejected.

-  **Python 3.15:** Fix, dictionary unpacking in displays and
   comprehensions used the generic update path, giving wrong
   ``TypeError`` messages for non-mapping and non-iterable keys, and did
   not support the Python 3.15 ``DictComp(key=..., value=None)``
   representation for ``**`` in comprehensions. A dedicated unpack path
   now emits version-appropriate messages and handles both forms.

-  **Python 3.12+:** Fix, constants were classified as immortal merely
   by being immutable, including the GC-tracked ``ExceptionGroup`` heap
   type, and ``sys.version_info`` was treated as immortal. Constants are
   now tracked as guaranteed immortal, known mutable, or unknown, and
   generic constant returns only use constants that are certainly
   immortal.

-  **Python 3.12+:** Fix, the caught exception type extracted the
   exception instance instead of its type. It now uses
   ``Py_TYPE(exception_value)``, matching CPython's exception state.

-  **Python 3.7+:** Fix, class subscription used separate constant and
   runtime paths, so ``__class_getitem__`` set to ``None``,
   non-callables, descriptors, and metaclass attribute errors behaved
   differently. Both paths now share one helper with version-appropriate
   errors.

   .. code:: python

      class C:
          __class_getitem__ = None

      C[int]  # Python 3.11+: TypeError: type 'C' is not subscriptable

-  **Python 3.5+:** Fix, assigning to ``cr_frame`` raised the generator
   attribute message ``gi_frame is not writable``. It now names
   ``cr_frame``.

-  **Python 2:** Fix, list extension used the Python 3 length hint API
   and mishandled failing hints. It now uses the Python 2 private API,
   reports a missing exception as ``SystemError``, and only resizes for
   positive hints.

-  **Python 3.12+:** Fix, ``TypeAliasType`` instances created in
   compiled code got the wrong ``__module__``, because ``typing``
   derives it from the caller frame's function object. Compiled caller
   frames now get a temporary function object, and ``TypeAliasType`` is
   included in the patched typing types.

   .. code:: python

      from typing import TypeAliasType

      Alias = TypeAliasType("Alias", int)
      print(Alias.__module__)  # the module that defines Alias

-  **Standalone:** Fix, symlinks to shared libraries, e.g. versioned
   aliases like ``libfoo.so`` pointing to ``libfoo.so.1.2``, were copied
   as separate regular files, which could load duplicate library state.
   Symlinks are now preserved, with their targets copied first, and
   macOS binary path fixing is skipped for the link itself.

-  **Standalone:** Fix, the loader's ``find_spec`` raised the excluded
   module import error instead of returning ``None``, so availability
   probes like ``importlib.util.find_spec`` did not behave like for
   missing modules. It now returns ``None`` for excluded modules, and
   only the actual import attempt raises.

-  **Standalone:** Fix, when DLLs with the same name were found in
   different locations, the first one won regardless of whether it came
   from the Python installation or the system. DLL paths are now
   classified as inside, VC redist, or system, and copies from the
   Python installation and program directories are preferred over system
   ones.

-  **Standalone:** Fix, Python allocators were captured before
   interpreter initialization, so allocator settings from the
   environment were not respected, and hook allocator contexts were
   cached after they became invalid. The allocators are now captured
   after initialization, hook allocators are routed through the Python
   API, and standalone mode ignores ``PYTHONMALLOC``,
   ``PYTHONTRACEMALLOC``, ``PYTHONDEVMODE``, and ``PYTHON_GIL`` from the
   environment. The free allocator is now captured for all Python
   versions, not only free-threaded builds.

-  **Standalone:** Fix, a failing ``ldd`` call was ignored and
   dependency detection continued with incomplete output. The exit code
   is now checked and the error output reported.

-  **Standalone:** Fix, the ``{PROGRAM_DIR}`` template expansion on
   non-Windows started its backwards directory scan at the terminating
   NUL byte instead of the last character, so the value expanded
   incorrectly. The scan now starts one character earlier.

-  **Standalone:** Fix, scanning a package path for extension modules
   did not handle missing parent modules or ``__path__``, leaked the
   path, filenames, and stored extension module references, and kept
   scanning after a match. Missing parents now count as not found,
   references are released, and scanning stops at the first matching
   extension module.

-  **Standalone:** Fix, a reentrant fixed import during extension module
   initialization saw the loader placeholder instead of the real module
   in ``sys.modules``. Reentrant imports of the owning thread now use
   the real module. Internal loader modules stay registered when their
   execution fails, so reentrant imports can still find them.

-  **Standalone:** Fix, the ``ldd`` cache was keyed only by DLL name
   even though results depend on the package and original directory, and
   dependency cycles could recurse endlessly. The cache key now includes
   package and directory, visited DLLs are tracked, and the Python
   executable is resolved with ``os.path.realpath()``.

-  **Standalone:** Fix, storing the JIT source dictionary in the
   builtins module leaked the dictionary reference. It is now released
   after storing, and the assignment is checked in debug mode.

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

-  **Plugins:** Fix, DLL configuration entries with a ``relative_to``
   module or relative destination paths failed when that module was not
   available, instead of being ignored. Missing modules are now
   tolerated when resolving destination paths, and no entry is created
   then.

-  **Plugins:** Fix, a plugin decision of ``never`` for recompiling
   extension modules could be overridden by later plugin decisions or
   the command line source preference. It is now cached and returned
   immediately.

-  **Plugins:** Fix, the ``gi`` plugin only patched one quote style of
   PyGObject's ``DynamicImporter`` setup, and included platform specific
   ``Gio``/``GLib`` typelib files without their generated virtual module
   imports. Both quote styles are now patched, and the platform
   namespaces are included through the virtual module imports.

-  **Plugins:** Fix, preprocessor symbols were cached globally across
   onefile and backend builds, although plugins can provide different
   symbols for each. The cache is now keyed by the build kind.

-  **Plugins:** Fix, the help text of ``--noinclude-qt-translations``
   described the option as including Qt translations, although it
   excludes them. The help text now describes the exclusion.

-  **Plugins:** Fix, conflict handling treated two negative dependency
   or missing DLL decisions as conflicting instead of only an opposite
   decision, and short option conflicts were detected by testing the
   whole short option list rather than membership. Conflicting decisions
   now require opposite values, short options are compared correctly,
   and unhandled plugin option conflicts are reported.

-  **Plugins:** Fix, plugin conditions for ``arch_x86``, ``arch_amd64``,
   and ``arch_arm64`` only recognized one spelling each. They now accept
   common aliases such as ``i386``/``i686``, ``amd64``, and ``aarch64``.

-  **Plugins:** Fix, a stale or incompatible ``setuptools`` installation
   raising ``SyntaxError`` during ``pkg_resources`` import aborted
   compilation. It now counts as unavailable.

-  **Plugins:** Fix, configuration ``when`` expressions were evaluated
   even for entries that did not configure the requested item, recording
   plugin influences that were not real. They are now only evaluated for
   matching entries.

-  **Plugins:** Fix, JIT-generated functions were compiled with
   ``<string>`` and without the module's future flags, so kernel
   compilers could not read or parse their source. They now use the
   module filename and future flags, and plugin docstring decisions are
   applied.

-  **Plugins:** Fix, permission error handling for DLL and data file
   scans imported the built-in ``PermissionError``, which does not exist
   on Python 2. It is now imported from the compatibility module.

-  **Plugins:** Fix, a partially removed tkinter installation that
   imports without ``TkVersion`` now counts as unavailable instead of
   failing compilation.

-  **Plugins:** Fix, merging duplicate YAML configuration sections
   replaced list entries instead of appending them, did not copy list or
   dictionary sections, and did not recheck sections after merging,
   while mismatched section types could be silently merged as
   dictionaries. Lists and dictionaries are now copied, list entries
   append, sections are rechecked, the configuration module is passed
   through expression evaluation, and mismatched types are rejected.

-  **Plugins:** Fix, variable configurations were numbered from zero
   while constants started at one, so runtime information cache names
   were not stable. They now start at one.

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

-  **Windows:** Fix, Windows error messages used the ANSI
   ``FormatMessage`` and formatted error codes as signed, which could
   lose or garble non-ASCII system messages. Wide character
   ``FormatMessageW`` is now used, with unsigned error codes and an
   unknown-message fallback.

-  **Windows:** Fix, Windows resource reading used missing ctypes
   signatures and did not always free loaded libraries, and version
   resources used the wrong structure version, 16-bit header fields,
   string lengths, and padding. The signatures and resource names are
   now correct, libraries are freed, and version info fields are written
   correctly.

-  **Windows:** Fix, clcache released its mutex even when it was not
   acquired, did not capture and print compiler output consistently when
   ``CLCACHE_DISABLE`` was set, and modified the caller environment. The
   mutex is only released when acquired, output is captured and printed
   consistently, and the environment is copied before modification.

-  **Windows:** Fix, the NSIS installer embedded the whole icon group
   and rejected non-ICO images, so ``--windows-icon-from-ico`` with a
   PNG or an icon index produced a broken installer. Non-ICO icons are
   now converted to ICO, and the icon index is stripped because NSIS
   cannot apply it.

-  **Windows:** Fix, ``nuitka-run.cmd`` relied on a quoted invocation of
   ``nuitka.cmd`` that did not reliably find Python. It now locates
   ``python.exe`` next to the launcher or its parent directory, like
   ``nuitka.cmd``.

-  **Windows:** Fix, conda DLL search paths were only detected for the
   conda base installation, not for virtual environments created from
   it, and ``Library/bin`` was missing from the scan directories. The
   conda base prefix is now detected through the system prefix, and
   ``Library/bin`` is included for DLL scanning.

-  **Windows:** Fix, executing a compiled binary with ``--run`` used a
   bare name, which Windows does not search in the current directory
   when ``NoDefaultCurrentDirectoryInExePath`` is set. Bare names now
   get an explicit current-directory prefix.

-  **Windows:** Fix, generated launch scripts quoted ``set`` assignments
   incorrectly, and batch files with arguments or parentheses were not
   executed reliably. ``set`` values are now quoted, bare batch paths
   get an explicit current-directory prefix, and batch files run through
   ``cmd.exe /d /s /c`` with an outer quoted command.

-  **Windows:** Fix, path comparisons relied on ``os.path.normcase``,
   which is a no-op on macOS and MSYS2 POSIX Python despite
   case-insensitive file systems, and import scanning used a separate
   case-sensitivity decision. Added ``isCaseInsensitiveOS()`` and
   normalized casing for comparisons and import scans.

-  **Windows:** Fix, drive path restoration could turn a UNC path into a
   drive path when the share root was only a name prefix, and drive
   roots without trailing separators were mishandled. Restoration now
   checks the share root as an actual prefix, and drive splitting uses
   ``ntpath`` for MSYS2 compatibility.

-  **macOS:** Fix, DMG creation converted the source icon again instead
   of reusing the app bundle's actual ``.icns`` file, and an app bundle
   without external files was passed directly to ``create-dmg``, which
   flattened the bundle into the volume root. The bundle icon is now
   remembered and reused for the volume icon, and the bundle and
   external files are staged so the bundle stays intact.

-  **macOS:** Fix, the ``.dylibs`` directory next to a package was only
   added when the package directory existed, not the ``.dylibs``
   directory itself, and an unsupported DLL configuration did not stop
   after reporting it. The actual ``.dylibs`` directory is now checked,
   and the unsupported configuration returns immediately.

-  **macOS:** Fix, dependencies that referenced a library with an ABI
   suffix were resolved with the specific suffix slice instead of the
   ABI suffix, so the actual extension module file was not found and
   left unresolved. The correct suffix is now replaced.

-  **macOS:** Fix, the generated console mode wrapper script started
   with an unwanted blank line. The template now uses a backslash line
   continuation.

-  **macOS:** Fix, architecture-specific versioned dylibs such as
   ``libgcc_s_x86_64.1.dylib`` were not detected, because only the
   version suffix was considered. Architecture-suffixed variants are now
   checked before the version suffix.

-  **macOS:** Fix, accepted missing macOS dependencies were handled by
   raising and catching ``NuitkaForbiddenDLLEncounter``. Accepted
   dependencies are now skipped directly, while Qt plugin private
   dependencies are still excluded.

-  **macOS:** Fix, DLL detection cached results without the package
   rpath state, later binary fixups could get a different result than
   the copy step, and package rpaths were keyed by string. The cache key
   includes the rpath snapshot, the first result is reused for fixups,
   and rpaths are keyed by ``ModuleName``.

-  **Linux:** Fix, an explicitly given Linux installer output filename
   had its extension changed to ``.AppImage`` again, so a custom name
   could be altered. The given filename is now used as-is, and only the
   default output gets the ``.AppImage`` extension.

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

-  **Compatibility:** Fix, modules demoted to bytecode used their
   original filename when the file reference mode was not ``original``,
   so tracebacks and code objects did not match the requested file
   reference choice. The runtime filename is now used for demoted
   modules in those modes.

-  **Compatibility:** Fix, a class dictionary could be propagated to a
   temporary variable while a locals reference in a conditional branch
   was still undecided, so the class namespace was no longer available
   at run time. The propagation is now prevented for such references,
   and branch trace collection updates mark escaped locals.

-  **Compatibility:** Fix, class body lookups could not distinguish
   class namespace names from enclosing function locals when the locals
   were assigned later in the function, because the bindings were only
   known after visiting the assignments. Names bound by assignments and
   deletions are now registered while building the tree, with
   ``nonlocal`` declarations checked before they are consumed, and
   function variable assignment prefers provided variables over taken
   ones.

-  **Compatibility:** Fix, on non-Windows systems a closed standard
   input was replaced with ``/dev/null``, while CPython leaves
   ``sys.stdin`` as ``None`` when file descriptor 0 is closed. The
   replacement is now skipped for ``stdin`` on POSIX, preserving child
   process behavior that e.g. multiprocessing relies on.

-  **Compatibility:** Fix, built-in parameter specs could not express a
   Python visible keyword that differs from the internal argument name,
   so ``os.path.isdir`` on Windows with Python 3.12.0 rejected its
   ``path`` keyword, while that version used it before the rename to
   ``s``. Keyword aliases are now supported for built-in specs, and the
   alias is used for the platform dependent argument name.

-  **Compatibility:** Fix, a value read from a variable could be used as
   a borrowed reference while generating an expression, and a later
   write to the same variable, e.g. by a walrus assignment, released it
   before the expression used it. Borrowed references are now tracked
   and a reference is taken before such writes, with the C type property
   ``holdsObjectReference`` handling dual and non-reference-counted
   types. Tracking now also covers slices, operations, call arguments,
   and dictionary keys.

   .. code:: python

      value = "".join(["a"] * 1000)
      other = value + (value := "b")

      # 4.4rc6: the string could be released before the addition
      # 4.4rc7: the value stays alive until the expression is done

-  **Compatibility:** Fix, slices were always considered unhashable,
   although Python 3.12+ slices are hashable when their components are.
   Slice hashability now follows the components, ranges, unions, generic
   aliases, and anonymous values are handled in constant hashability
   checks, and the bitwise, matrix multiplication, and bytearray modulo
   shape tables were corrected.

-  **Compatibility:** Fix, ``with`` and ``async with`` looked up
   ``__enter__``/``__aenter__`` before ``__exit__``/``__aexit__`` and
   could call the enter method even when the exit lookup failed. Both
   special methods are now looked up first, with the version-specific
   order for Python 3.6+, 3.9+, and 3.14, and enter is not called if the
   exit lookup fails.

-  **Compatibility:** Fix, the text constructor with ``encoding`` or
   ``errors`` but no object did not validate those arguments and failed
   instead of returning an empty string. It now validates them and
   returns an empty string like CPython.

-  **Compatibility:** Fix, ``float()`` and membership tests used the
   wrong CPython error messages on some versions and lost argument side
   effects when raising. The messages now match the Python version, side
   effects are preserved, and exception template placeholders are
   validated.

-  **Compatibility:** Fix, unhashable keys suppressed exceptions for
   ``dict.get`` and ``dict.pop``, and ``dict.clear()`` did not
   invalidate knowledge or preserve finalizer side effects. The
   operations now raise correctly, and ``dict.clear()`` invalidates
   dictionary knowledge with control flow escaping.

-  **Compatibility:** Fix, ``list.count`` was treated as unable to raise
   and as having no side effects, so a dropped result lost exceptions
   and comparison side effects. It is now treated as able to raise and
   run arbitrary comparison code.

-  **Compatibility:** Fix, more type shape differences with CPython
   remained for loop alternative comparisons, ``str``/``unicode`` binary
   operations, and ``not`` on non-bool comparison results. The shapes
   were corrected, and ``not`` now leaves non-bool results to runtime
   truth testing.

-  **Compatibility:** Fix, star argument iterability checks looked up
   ``__iter__`` and ``__getitem__`` attributes, which a custom
   ``__getattribute__`` could hide. The checks now inspect type slots,
   so iterable objects remain iterable.

   .. code:: python

      class HiddenIter:
          def __iter__(self):
              return iter((1, 2))

          def __getattribute__(self, name):
              if name == "__iter__":
                  raise AttributeError(name)
              return object.__getattribute__(self, name)

      print([*HiddenIter()])  # [1, 2]

-  **Debugging:** Fix, on Windows, the PDB file of an unstripped target
   was left in the build directory after moving the executable, so it
   was lost. It is now moved next to the final binary, and the ``.pdb``
   suffix is cleaned up with the other intermediate files.

-  **Debugging:** Fix, the mapping length helper asserted that
   ``mp_length()`` did not raise or return a negative value, hiding the
   original error. Raising and negative results now propagate, so
   ``len()`` and iteration report the real exception.

   .. code:: python

      class BadLen(dict):
          def __len__(self):
              return -1

      len(BadLen())  # ValueError: __len__() should return >= 0

-  **Debugging:** Fix, debug checks for compiled types compared
   ``tp_subclasses`` against the wrong base field, a ``type_params``
   setter checked ``self`` twice, and frame debug output used the
   compiled frame printer. The assertions and setter now check the right
   values.

-  **Cache:** Fix, the bytecode cache did not restore whether a module
   usage source reference was internal, so warm-cache compilation
   reports could differ from cold-cache ones. The cache format now
   stores and restores that flag.

-  **Onefile:** Fix, the splash screen was only shown when the payload
   was compressed, although the option is independent of compression. It
   is now shown whenever it is enabled.

-  **Onefile:** Fix, payload file sizes were truncated to 32 bits on
   Windows, and checksums could not handle files larger than 32-bit
   sizes. Added ``calcCRC32With64BitSize()``, used ``GetFileSizeEx()``,
   and handled zero-sized files without failing memory mapping.

-  **Onefile:** Fix, the Posix child wait loop converted milliseconds to
   nanoseconds with ``* 1000``, so grace timeouts expired a thousand
   times too early. It now uses ``* 1000000L``.

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

-  **Scons:** Fix, in the ``linker`` resource mode, blob paths were
   turned into linker symbol names, so modules whose names differed only
   in characters that map to ``_``, e.g. ``a.b`` and ``a_b``, could
   collide. Blob symbol bases are now restricted to ASCII letters,
   digits, and underscores, adding a hash of the source filename where
   needed to make them unique, and their readable part is limited to
   keep blob filenames within Windows path limits. The ``#embed`` path
   is relative to the generated file rather than the working directory.

-  **Scons:** Fix, interrupting a build left compiler processes running
   and spawn threads blocked on their output pipes, and hanging child
   processes could block indefinitely. Interrupts now stop the spawn
   threads and kill the compiler process family, with process tree
   termination on Windows, and process communication and import
   detection have timeouts.

-  **Scons:** Fix, external C caching tools such as ``ccache`` could
   reuse a compiled object when the contents of an embedded constant
   blob changed, since the generated C code itself did not change. The
   generated code for the ``c23_embed`` and ``incbin`` resource modes
   now includes a checksum of the blob, so caches notice the change.

-  **Scons:** Fix, unexpected Python exceptions in Scons build actions
   were converted to build errors without their traceback, so only the
   message was shown. The traceback is now passed through.

-  **Scons:** Fix, clcache accepted cache entries with missing or
   zero-sized object files, which caused linker errors, and only checked
   that the object file existed after compilation. Unusable entries are
   now removed and treated as misses, and only successful compilations
   with a usable object file are cached.

-  **Scons:** Fix, compiler command lines in ``CC`` and ``CXX`` were
   treated as a single path, so options were lost and unquoted Windows
   paths with spaces failed. The command line is now split into compiler
   path and options, options are preserved when injecting ``ccache``,
   and compiler detection uses the split path.

-  **Scons:** Fix, Scons imported ``readline`` for its interactive mode,
   which could pull in ``libedit`` and emit termcap warnings. The import
   is now blocked for the non-interactive build.

-  **Scons:** Fix, on Python 2, Scons arguments were not decoded with
   the ``argument_encoding`` option it expects, and a missing
   ``sys.__stdout__.encoding`` could fail decoding. Arguments are
   decoded only on Python 2 with the expected option, and missing
   encodings fall back to locale and UTF-8. Environment variable updates
   now tolerate missing entries and encode Python 2 unicode values for
   subprocess compatibility.

-  **Scons:** Fix, adapted Python header include paths were appended
   behind the normal include paths, so they were not reliably preferred.
   The adapted directory is now prepended, and the duplicate
   ``SYSFLAG_DONTWRITEBYTECODE`` build definition was removed.

-  **Scons:** Fix, Homebrew ccache guesses pointed at a directory
   instead of the binary and accepted directories as binaries, and the
   ``CLCACHE_MEMCACHED`` warning was emitted during ccache setup. The
   guesses point at ``ccache`` binaries, only files are accepted, and
   the warning moved into clcache setup.

-  **Scons:** Fix, Scons options, environment variables, build
   definitions, no-deployment flags, plugin preprocessor symbols,
   include directories, and link inputs were emitted in nondeterministic
   order. They are now sorted, and plugin APIs are asserted not to
   return sets.

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

-  **UI:** Fix, the error message for a debugger that was not found in
   ``PATH`` was missing the debugger name, and the module parameter
   error had a stray quote. Both messages are now formatted correctly.

-  **UI:** Fix, path checks used manual decisions and did not reject
   paths that were only a drive or a root without a drive. Path validity
   decisions now carry a reason and are used for legal path errors and
   DLL directory scans.

-  **UI:** Fix, user input paths from command-line options and
   environment variables were not normalized consistently, and ``~``
   expansion on Windows could treat ``~1.txt`` as a user home. Paths are
   now normalized at the option boundaries, including data files, icons,
   installer outputs, container paths, and external tools, and Windows
   only expands the plain ``~`` shorthand.

-  **UI:** Fix, the unusual-code warning for a local module shadowing a
   standard library module used a nonexistent attribute and could crash.
   It now uses the actual module filename found during import.

-  **Reports:** Sensitive option values are now redacted in compilation
   reports and container command output by matching option name
   patterns, including abbreviated long options, with default patterns
   for ``password``, ``salt``, and ``secret`` options.

-  **PGO:** Fix, demoting unused modules to bytecode crashed when a
   plugin provided fake modules for them, since only trigger modules
   were replaced in the plugin module tables. Fake modules are now
   replaced as well, and only actual compiled modules get source code
   assigned.

-  **PGO:** Fix, cached modules demoted to bytecode were compiled
   without the module facts needed for plugin decisions, so docstring
   removal and the package flag passed to the frozen module bytecode
   hook could be wrong. The module name, package status, and docstring
   decision are now passed explicitly, with docstring decisions
   available by module name and filename for modules not in the registry
   yet.

-  **PGO:** Fix, modules that were too complex to compile and demoted to
   bytecode used a separate path without plugin docstring decisions.
   They now use the shared demotion path, so docstring decisions are
   applied consistently.

-  **Persistence:** Fix, code object positional-only argument names were
   serialized as a tuple, parameter details were restored with the wrong
   types, and ``co_qualname``, future flags, and async generator
   expressions were missing when saved code objects were loaded. The
   details are now serialized and restored correctly. Temporary variable
   types, variable versions, and persisted version numbers for
   assignment and deletion nodes are now restored as well.

-  **Project:** Fix, unknown ``[tool.uv]`` config keys always produced a
   warning, including known keys that do not affect how the project is
   built. The known ``index``, ``managed``, and ``sources`` keys are now
   ignored, and the warning for unknown keys was reworded.

-  **Distributions:** Fix, distribution metadata handling now tolerates
   missing metadata and falls back to the ``.dist-info`` directory name
   for Debian packages, only logs a missing distribution warning when
   the lookup was unsuccessful, and detects the vendored
   ``setuptools/_vendor`` path.

-  **Multidist:** Fix, multidist basename detection stripped any
   trailing characters matching ``.py``/``.exe``/``.bin`` instead of
   actual extensions, did not normalize case for matching, and inserted
   module names and basenames without quoting. It now strips only real
   extensions, compares normalized names, and uses ``repr`` for
   generated code.

-  **Distutils:** Fix, the check that rejects ``--project`` together
   with ``--main`` did not recognize ``--module`` and ``--mode=package``
   as module mode, so the combination could pass. Both forms are now
   treated as module mode.

-  **Quality:** Fix, the stderr filter for tool calls treated the
   presence of unfiltered error lines as a successful filtered run, so a
   failing tool could be reported as success, while output that was
   entirely benign kept the failure. It now returns success only when
   there was output and all of it was filtered as benign, and leaves the
   exit code in effect otherwise.

-  **Watch:** Fix, the watch tool did not recompile a case when the
   selected Python installation version changed, since the compilation
   report's Python version was not considered. The Python version is now
   read from the report and compared with the selected interpreter, and
   existing Pipenv virtualenvs are checked and recreated when their
   Python version differs.

-  **NoGIL:** Fix, GCC warned about ``stringop-overflow`` in the NULL
   branch it creates for atomic reference count operations in
   free-threaded CPython code, which is GCC bug 105585. The warning is
   now disabled for GCC builds of such code, unless warnings are errors.

-  **NoGIL:** Fix, Scons is not free-threading safe and gave sporadic
   errors during parallel builds with free-threaded Python.
   ``PYTHON_GIL=1`` is now set for the build tool only.

-  **NoGIL:** Fix, string reuse and in-place operations used
   ``Py_REFCNT(...) == 1``, which is not sufficient for free-threaded
   builds and could mutate shared objects. They now use
   ``_PyObject_IsUniquelyReferenced`` with a fallback for Python before
   3.13.4.

-  **NoGIL:** Fix, module and builtin dictionary lookups returned
   borrowed references in free-threaded builds, while concurrent
   mutation could invalidate them, and builtin caches were updated
   without atomics. The lookups now return owned references using
   critical sections, builtin caches use atomic operations, and unlocked
   static caches are avoided.

-  **MSYS2:** Fix, the runner created for entry points used a
   non-normalized path, which could produce mixed path separators. The
   generated runner filename now uses ``getNormalizedPathJoin``.

-  **MSYS2:** Fix, MSYS2 package detection checked for Anaconda Python
   instead of MSYS2 and POSIX Windows Python, so MSYS2 packages were not
   detected there. The check now uses the MSYS2 flavors.

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

-  **Standalone:** Added the missing implicit import for
   ``pydantic.type_adapter``.

-  **Standalone:** Added CUDA 13 and NVVM library paths for ``nvidia``,
   the runtime version library for ``cutlass``, package configuration
   for ``humming``, and data files for ``flashinfer``, ``sglang``,
   ``torch``, and ``vllm``.

-  **Standalone:** Platform backends of ``pywebview`` are now included
   by default and only backends unusable on the current platform are
   excluded, so new backends work without a Nuitka change. Added the
   .NET 4.6.2 webview DLLs and updated the EdgeChromium native path
   workaround.

-  **macOS:** Added PyQt6 support, including Qt library and translation
   target paths, framework detection, WebEngine process paths, and
   framework bundle normalization with Mach-O checks, helper executable
   rpaths, and version symlinks. Removed the PyQt6 unsupported check and
   filtered non-DLL Qt plugin files from wheels.

-  **Standalone:** Fixed the ``vLLM`` lazy-loader mapping to track
   submodule attributes by submodule name with the attribute names as
   values, so lazy-loaded attributes are included correctly.

-  **Standalone:** Added the ``torchvision.extension._C_stable``
   implicit dependency, since it is a DLL named like an extension
   module.

-  **Standalone:** Removed the unnecessary ``pyarrow._*`` implicit
   imports for ``dask.dataframe``.

New Features
============

-  **Python 3.15:** Pronounced Python 3.15 as officially supported. The
   recommended working version and the recommendation for commercial
   usage remain Python 3.13 until the bloat from deferred annotations is
   under better control.

-  **Python 3.16:** Added experimental support for Python 3.16, which is
   now partially supported. Initialization and opcode handling are
   covered, the ``site`` and ``verbose`` flags use the new configuration
   API, the new ``_Py_LATIN1_CHR`` dangerous macro is handled, and
   ``python3.16`` shebangs are recognized. With 3.16a2 on Linux, most
   things work.

-  **Python 3.14+:** Annotation source generation now handles shadowed
   builtins through ``builtins``, f-strings, lambdas with full parameter
   signatures (positional-only markers, defaults, keyword-only
   arguments, ``*args``, and ``**kwargs``), builtin and hard-import
   calls, unpacking, method operations, runtime paths, module
   attributes, class scopes, and raise branches. This allows more
   ``__annotate__`` functions to be generated from source instead of
   falling back to bytecode.

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

-  **Python 3.12.5+:** The Python build script now builds Tcl/Tk 9 from
   source with ``--enable-zipfs``, so Tkinter can use the DLL overlay
   path and standalone distributions no longer need the many separate
   Tcl/Tk data files. Downloads are shared between Python and Tcl/Tk,
   and installation works for non-writable prefixes. The appended zip
   overlay is preserved when binaries are stripped or their RPATHs are
   changed.

-  **Plugins:** Added the ``onFinalResultFinished`` hook, which runs
   after all ``onFinalResult`` modifications, so plugins can inspect the
   final binary, e.g. to calculate its checksum. (Added in 4.3.5
   already.)

-  **Onefile:** Added an ``overlay`` resource mode, which attaches the
   onefile payload to the end of the executable instead of embedding it
   as a constant blob. It is used automatically on Windows when the
   payload would exceed the PE file size limit. The bootstrap maps its
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

-  **Plugins:** The ``tk-inter`` plugin now detects Tcl/Tk libraries
   embedded in DLL zip overlays, avoids packaging duplicate data
   directories when they are used, and sets or clears ``TCL_LIBRARY``
   and ``TK_LIBRARY`` according to where the libraries were found. Tk
   version detection on Python 2 now uses the correct module name.

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

-  **NoGIL:** Added experimental support for compiling and running with
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

-  **Container:** Added ``--container-python-version`` to build and use
   a different Python inside the container, plus
   ``--container-requirements`` and ``--container-wheels-dir`` to
   install packages before compiling. Project requirements and options
   are now checked against the container environment, with project
   parsing deferred to the in-container Nuitka. A CentOS Stream 8
   container definition is also included.

-  **Plugins:** Added ``--gi-version`` to select the version of a
   GObject Introspection namespace when multiple versions are installed.
   Versions are propagated from parent namespaces and dependencies, and
   used for typelib data files, dependencies, and platform specific
   namespace imports.

-  **UI:** ``--lto=auto`` now detects ``-flto`` and ``-fno-lto`` flags
   in ``CFLAGS``, ``CCFLAGS``, ``CXXFLAGS``, and ``LDFLAGS``, and
   resolves accordingly. Conflicting flags in the environment, or
   conflicts with an explicit ``--lto=yes`` or ``--lto=no``, are now
   errors.

-  **UI:** Added the ``no_unraisable`` Python flag, which compiles out
   Nuitka's own unraisable exception writes on all versions and ignores
   CPython internal unraisable writes on Python 3.8 and later.

-  **PGO:** Added standalone and app-dist profiling support. The
   distribution is prepared before the profiling run and reset before
   the final compilation pass, and MSVC PGD/PGC files are kept in the
   build directory.

-  **Plugins:** Added a ``plugin_priority`` attribute to request that a
   plugin is called later, e.g. for signing after compression. Active
   plugins are sorted stably by it, keeping the standard and user plugin
   order for equal priorities.

-  **Plugins:** Added a ``downloads`` section to the Nuitka Package
   Configuration, which downloads files into the Nuitka cache for
   inclusion, and added the ``tiktoken`` data file download and cache
   environment setup.

-  **Plugins:** Added CuTe DSL support to the ``numba`` plugin, keeping
   functions decorated with ``cutlass.cute.jit`` and
   ``cutlass.cute.kernel`` uncompiled since the CuTe DSL rewrites their
   ``__code__``. Decorator matching now uses fully qualified names
   resolved through import statements, so aliases like ``from numba
   import jit`` are recognized, and Numba nested functions now work too.
   The JIT disable reason now distinguishes an explicit
   ``--numba-enable-jit=no`` from the standalone default.

-  **Plugins:** Replaced the uncompiled decorator name hook with JIT
   decorator registrations that can request bytecode or run a callback
   with the decorated function's source range. Added ``AstUnparsing``
   for Python versions without ``ast.unparse``, preserved source line
   numbers for bytecode functions, and registered Triton, CuTe, and CUDA
   tile decorators for source inclusion.

-  **Plugins:** Added support for plugins that replaced other plugins to
   recognize the name they were enabled with, before renames are
   applied, through ``getPluginsEnabledUnrenamed``.

-  **Distutils:** Project requirement checks now work without
   ``packaging`` or ``pip``, by parsing PEP 508 requirements and PEP 440
   versions with a fallback implementation, e.g. in a ``uv`` virtualenv.
   Unmet requirements are reported as unsatisfied rather than
   uninstalled.

-  **Plugins:** Added experimental ``cutlass.cute.experimental.jit`` and
   ``cutlass.cute.experimental.kernel`` and
   ``triton.experimental.gluon.jit`` decorators, handled like their
   stable counterparts for bytecode and source inclusion.

-  **Debugging:** Added ``--devel-show-slow-paths``, which reports
   runtime slow paths taken by generators, coroutines, and async
   generators to stderr. The previous disabled trace blocks were
   replaced with tracing macros.

-  **UI:** Command line help now uses descriptive metavars for module
   patterns, paths, choices, packages, directories, and plugin options,
   and no longer shows metavars for boolean flags. Always-enabled
   package-support plugin options are also shown in the default help.

-  **macOS:** PySide6 applications in app-bundle mode now load the
   bundle icon into ``QApplication``, using the icon filename for the
   plist. A standalone macOS test covers the icon.

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

-  **Scons:** Constant blob symbols are now marked with hidden
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

-  **Code Generation:** The cleanup exception handler is now an
   always-false conditional block rather than a ``goto`` and label,
   removing an unnecessary jump from the normal path of generated code.

-  **Code Generation:** Cleanup code for newly created locals
   dictionaries now uses the scoped ``withCleanupFinally`` helper, so
   the dictionary is released by the local exception handler instead of
   being kept in the outer cleanup scope, and the created dictionary
   variable is used consistently when the dictionary already exists.

-  **Subscripts:** Constant subscripts of tuples and tuple subclasses,
   e.g. named tuples, now use a direct table access fast path, with
   ``IndexError`` messages matching tuples.

-  **Hard Imports:** Added hard import nodes for ``os.path.join``,
   ``importlib.resources.open_binary`` and ``open_text``, their
   ``importlib_resources`` backport variants, and runtime-relative
   paths, plus a vectorcall-based ``CALL_FUNCTION_WITH_ARGS`` helper
   used by ``print`` and ``zip``. The generated resource calls use the
   module of the recognized call, so the backport variants import from
   ``importlib_resources``.

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

-  **Optimization:** Fetched exception checks now carry the unlikely
   branch hint, so the C compiler does not treat error exits with the
   same weight as the normal path.

-  **Python 3.10+:** Added a dedicated ``NameError`` creation node, so
   manually created exceptions support the keyword-only ``name``
   argument and carry the ``name`` attribute.

-  **Optimization:** Type lookups on Python 3.11 to 3.15 now read
   CPython's per-interpreter lookup cache directly, avoiding a call into
   the Python DLL on Windows, while free-threaded builds and Python 3.16
   keep using ``_PyType_Lookup``. This reduces ``with`` statement
   overhead by about 15%, since its ``__enter__`` and ``__exit__``
   lookups commonly hit the cache.

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

-  **Variables:** Module variable reads now use specialized checked,
   checked-global, and infallible accessors, with the error handling
   moved into the accessor. This reduces branches and temporaries, and
   lets the C compiler inline an accessor that is used once without
   forcing inline code at every use.

-  **Variables:** Added an infallible module variable accessor variant
   for the experimental ``no-module-globals-deleted`` mode. Escaped
   module variables that are still known to be assigned are tracked in
   value traces, so reads after an escape can use the infallible
   accessor, and non-deployment builds check for an unexpectedly deleted
   global and exit with an error instead of returning ``NULL``.

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

-  **Trace Collections:** ``isUnchangedResumeTrace`` queries now cache
   their answers per query, so shared merge traces are not traversed
   repeatedly. The trace graph does not change during a query, so the
   cached answers stay valid.

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

-  **Dictionaries:** Added infallible variants of the dictionary item
   insertion helpers for keys known to be hashable, and used them during
   dictionary creation to skip result checks and error exits. This
   generates more compact code with less local churn for the C compiler,
   reducing the generated C code size for large dictionaries.

-  **Dictionaries:** Extended the infallible dictionary item insertion
   helpers to dictionary copying, locals, module registration, deep
   copy, and frame locals. ``Nuitka_SetModule`` and
   ``Nuitka_SetModuleString`` now return void. Generated dictionary
   update and set code, and locals assignment for known dictionary
   shapes, use the infallible variants too, adding checks to previously
   unchecked locations.

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
   unstripped, and ELF files whose load segments would no longer be
   aligned after stripping are restored to the unstripped copy.

-  **Optimization:** Specialized attribute calls now compute the
   replacement expression immediately with ``computedExpressionResult``,
   unused ``str is bytes`` branches were removed, and a bug that
   reported too many generated base mixin aliases due to incorrect name
   matching was corrected.

-  **Optimization:** Added a dedicated ``delattr`` node and specialized
   ``getattr``, ``setattr``, ``delattr``, and ``hasattr`` with constant
   attribute names. CPython 3.11+ error message details for non-string
   attribute names are reported, constant-name ``setattr``/``delattr``
   calls are reduced to attribute statements when the result is unused,
   and compile-time constant type helpers were added.

-  **Optimization:** Exact type shapes are now marked hashable, and the
   default ``hasShapeTypeExact`` predicate was added, so type objects
   can use the hashable fast paths.

-  **Windows:** The onefile splash screen is now implemented in C
   instead of C++, so onefile builds no longer require a C++ compiler
   for it, and the unused ``Shlwapi`` library was dropped from the link
   libraries.

-  **Python 3.11+:** Attribute lookups and method calls on instances
   with managed dictionaries now read CPython's inline values and cached
   keys directly, avoiding creation of an instance dictionary. Attribute
   errors also get the ``name`` and ``obj`` details attached, matching
   CPython.

-  **Optimization:** Thread state lookup on Python 3.12+ now reads the
   runtime or thread-local storage directly where safe, avoiding a C-API
   call for every ``PyThreadState_GET``.

-  **Optimization:** Loop lookup now continues through outline functions
   instead of stopping there, while still stopping at real function
   bodies, so loops are no longer missed at outline boundaries.

-  **Optimization:** Node classes now reject redeclared ``__slots__``
   and ``named_children``, and dead slots were removed, reducing memory
   use and preventing inconsistencies.

-  **Optimization:** Module trees are now frozen before code generation,
   and the GC thresholds are raised for large compilations, so
   per-module objects are collected before repeated full collections.
   This gives large speedups for compilations past 20K modules and
   modest gains for intermediate ones.

-  **Optimization:** Recursive exception normalization now uses the
   single-class exception matching helper for ``MemoryError`` instead of
   the ``PyErr_GivenExceptionMatches`` C-API call.

-  **Optimization:** Quick call helpers used by each module are now
   tracked and declared only in that module's generated code instead of
   a global ``__helpers.h``, so adding or removing a module-specific
   call signature no longer invalidates the C cache for unrelated
   modules.

-  **Optimization:** Module lookup by name now uses a name-indexed
   dictionary of active and done modules instead of scanning both sets
   for every lookup.

-  **Optimization:** Added a hard import node for
   ``pkgutil.iter_modules`` that enumerates compiled packages from the
   loader entry table directly, and uses ``pkgutil.get_importer`` for
   regular paths. Internal loader modules stay out of the ``sys.path``
   hook.

   .. code:: python

      import pkgutil
      import some_package

      list(pkgutil.iter_modules(some_package.__path__))

-  **Optimization:** Dictionary item lookups now use the cached string
   hash and the concrete string hash slot for exact string and unicode
   keys, avoiding generic hash dispatch in the common case.

-  **Optimization:** General function calls now avoid tuple creation for
   zero and one argument calls, call compiled functions directly through
   their C entry points, and use the compiled function call helpers for
   Python functions before vectorcall.

-  **Optimization:** Iterator direct access replacement now records
   usages, releases, and deletions on the assignment trace and rewrites
   them after the pass instead of mutating the tree during iteration.
   The iterated-value temp variable is only allocated when direct access
   is possible, so cloning during trace collection produces a working
   state.

-  **Optimization:** ``os.path.join`` calls now collapse a single exact
   string argument and drop preceding relative paths once an absolute
   path is seen. The remaining calls use the generic C API code
   generation.

-  **Optimization:** Added ``Nuitka_Object_IsSubclass()`` with fast type
   and Python 2 old-style class paths, falling back to abstract subclass
   checks. It is used for exception matching, ``issubclass``, and
   unbound methods, and ``__subclasscheck__`` is in the default constant
   population.

-  **Optimization:** Unpacking checks now use the iterated value
   directly for too-many-values checks, with ``UNPACK_ITERATED_CHECK``
   and ``LOOKUP_SUBSCRIPT_CONST_FOR_UNPACK``. Iterator shapes and direct
   subscript unpacking were improved, including version-specific
   too-short and too-many error messages.

   .. code:: python

      try:
          a, b = [1, 2, 3]
      except ValueError as e:
          print(e)  # too many values to unpack (expected 2)

      try:
          a, b = [1]
      except ValueError as e:
          print(e)  # not enough values to unpack (expected 2, got 1)

-  **Optimization:** Added tri-state ``any()`` folding for generic,
   list/tuple, and range iteration handles. Exact string, bytes,
   bytearray, and range shapes are now treated as non-raising for
   ``all()`` and ``any()``.

-  **Optimization:** Function inlining is now scheduled as delayed work
   instead of mutating the tree during trace collection, and call
   details are derived from the call node.

-  **Optimization:** Exposed ``LOOKUP_SPECIAL_NO_ERROR()`` from the
   attribute helpers for reuse, avoiding duplicate special lookup code.

-  **Optimization:** Added ``Nuitka_PyObject_LengthHint()`` with the
   CPython semantics, avoiding a C-API call for length hints.

-  **Optimization:** Added ``Nuitka_PySequence_Check()`` implementing
   CPython's sequence check without a shared library call, used for
   iteration, exception group notes, and in-place sequence additions.

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

-  **Dill:** ``dill`` removals for ``depyf`` and ``torch`` are now only
   applied when the ``dill-compat`` plugin is not enabled, the
   ``datasets`` serialization check is a warning instead of an error,
   and the ``sglang`` datasets removal only applies to direct imports.

-  **Packages:** Replaced the CLI entry point import of ``httpx`` and
   ``httpx2`` with an ``ImportError`` and avoided following their
   ``_main`` modules, since the command line support pulls in ``click``,
   ``rich``, and ``pygments`` unnecessarily.

-  **Packages:** Replaced the ``pydoc_data`` module docs import in
   ``pydoc`` with an ``ImportError`` on Python 3.13 and later, removing
   the module documentation data used by the doc locator.

-  **Packages:** Avoided the macOS, Windows, and OpenSSL-specific
   implementations of ``truststore`` on platforms where they are not
   used.

-  **Packages:** Avoided following ``asyncio`` from
   ``typing_extensions`` before Python 3.12, where it is only used for
   deprecated coroutine wrappers.

-  **Packages:** Fixed the ``zope.interface`` anti-bloat rules for its
   test decorators, which replaced the decorated function with one
   returning ``None``. The decorators now keep the decorated function.

-  **Dask:** Avoided auto-following ``distributed`` from the ``dask``
   package, while allowing ``dask.distributed`` to follow it again,
   since that shim requires it. An ``allow`` value now overrides a
   parent module's ``no-auto-follow`` rule, and a module's own
   submodules are no longer suppressed.

-  **Dask-ML:** Avoided importing ``distributed`` only for its version
   in ``dask_ml._compat``, and avoided the eager model selection import.

-  **Packages:** Anti-bloat configuration matching now applies
   ``frame_locals`` patterns as part of the filter, restricts
   ``conditional-auto-follow`` to modules that can add suppressed
   namespaces, and uses the common configuration helpers for package
   system DLLs, pre/post import code, and environment overrides.

-  **Dask:** Avoided auto-following ``distributed`` and
   ``dask.distributed`` from ``fsspec``, ``joblib``, and ``xarray``,
   with helpful errors when their optional Dask transaction or backend
   is used without ``distributed``.

-  **Packages:** Removed the ``_json`` avoidance rules for
   ``json.decoder``, ``json.encoder``, and ``json.scanner``, since the
   fallback pure Python implementation can be much slower and the
   performance loss would not be discovered by users.

-  **Anti-Bloat:** Fixed the ``_distutils_hack`` replacement typo
   ``Mone`` to ``None``, so the distutils warning function is actually
   disabled.

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

-  **Actions:** The testing workflow now uses ``actions/setup-python``
   for Python 3.15 on Linux too, and includes Python 3.15 in the macOS,
   Windows, and Windows ARM matrices.

-  **Release:** The OSC upload now runs the documentation linting
   through the repository tool with download support, and builds the
   source distribution in its virtualenv, so it no longer depends on the
   system installation. The RPM source archive name now uses the
   lowercase ``nuitka`` prefix.

-  **Quality:** The VS Code, Zed, and Ruff configurations now exclude
   and ignore the ``tests`` directory, instead of only the CPython test
   copies.

-  **Quality:** The clangd checker now uses the private pip space
   binary, disables background indexing, has a check timeout, and
   reports internal clangd failures. The ``.clangd`` configuration is
   generated independently of compiler detection and no longer defines
   the unused Windows ``UNICODE`` macros.

-  **Project:** Expanded the agent rules and Developer Manual with
   architecture, planning, comment and docstring conventions, Python 2
   compatibility, and verification guidance, and updated the OpenCode
   watcher configuration to ignore test copies, build artifacts, caches,
   and virtual environments.

-  **Quality:** Added Windows ``.cmd`` launchers for the quality and
   code generation scripts, which locate Python through ``PATH`` or the
   VS Code alias file, and the ruff checker now accepts explicit paths
   or defaults to ``nuitka/``.

-  **UI:** Corrected the inverted help text of the
   ``--not-installed-is-no-error`` options in the PyLint and Pyright
   checkers, which described them as insisting on the tools being
   installed.

-  **Quality:** ``codespell`` now ignores third-party ``inline_copy``
   files, and no matching files are reported as an informational message
   instead of an error.

-  **Watch:** The watch tool can now automatically accept plugin
   influence records, removed modules and distributions, removed search
   paths, and removed ``Pipfile.lock`` packages, and the new
   ``--accept-all`` option enables all automatic acceptance options.

-  **Release:** The release and PyPI scripts now install
   ``restructuredtext_lint`` and ``pygments`` into the private pip space
   when needed, with ``--assume-yes-for-downloads``, instead of
   requiring the development requirements.

-  **Watch:** The watch tool now detects whether the watched Nuitka is
   standard or commercial and keeps benchmark results in separate
   directories, so runs can co-exist in the same repository.

-  **Quality:** ``black`` now skips ``_2.py`` and ``_27.py`` test
   variants automatically, so new Python 2 tests need no explicit skip
   entries.

-  **Quality:** The ``ruff`` checker now runs from the private pip space
   with version validation and Windows support, instead of requiring a
   globally installed ``ruff``.

-  **Quality:** Launcher scripts for quality and testing tools now
   return the result of ``main`` through ``sys.exit``, so failures are
   visible to CI and callers instead of always exiting successfully.

-  **Quality:** A pre-commit check now rejects accidental executable bit
   changes unless explicitly marked as intended with
   ``GIT_COMMIT=unchecked``, and the ``.cmd`` helpers were normalized to
   mode 644.

-  **Quality:** The Zed formatter now goes through Git's POSIX shell
   wrapper, which uses the ``.cmd`` launcher on Windows and the native
   script elsewhere.

-  **Watch:** The watch tool now records a hash of
   ``NUITKA_EXTRA_OPTIONS`` in the report and recompiles when it
   changes, falling back to the recorded command line for older reports.

-  **Project:** Clarified the comment and work-in-progress rules to
   preserve existing TODOs, disabled code, and commercial plugin
   replacement-hook comments, while still removing debug prints and dead
   code.

-  **Project:** Clarified that every file in ``.agents/rules/`` must be
   read and the list updated when rules change, and that skills are
   referenced by name rather than path.

-  **Quality:** The ``clangd`` checker now includes ``nuitka/plugins``
   by default and skips Windows-only sources by folder, prefix, or
   suffix on other platforms.

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

-  The PGO test runner now recognizes ``--mode=app-dist`` and locates
   the binary from the compilation report, and a standalone data files
   PGO test was added.

-  The PyQt6 tests now use app distribution mode, the macOS skip was
   removed, and a Qt WebEngine frameworks regression test was added.

-  Test requirements now include the exception in the skip reason when a
   ``nuitka-skip-unless-expression`` fails, instead of always reporting
   that it evaluated to false. Tk standalone tests require ``TkVersion``
   so a partially removed tkinter is skipped with a useful reason.

-  The scheduled kill callbacks in the CPython comparison now bind the
   process per iteration, so an old timer cannot kill a later process.

-  Output comparison now accepts ``?`` line numbers in tracebacks, as
   produced by some generated code.

-  Added coverage for attribute access on a walrus target used on the
   right side of a boolean operation.

-  Test discovery now detects macOS-only tests by suffix as well as
   prefix, and output comparison normalizes Windows 8.3 short paths in
   tracebacks and import output.

-  The CPython comparison now runs ``.cmd`` wrappers on Windows and
   ``.sh`` wrappers elsewhere when present, prefixes bare names, and
   removes the wrapper files afterwards.

-  Output comparison now normalizes ``cannot import name`` paths
   independently of the exception class.

-  Output comparison now normalizes escaped Windows paths in
   ``WarningMessage`` reprs and the variable ``[N chars]`` truncation
   count.

Cleanups
========

-  Removed the obsolete ``CodeObjectsMixin`` and its
   ``getCodeObjectHandle`` methods; code generation now calls
   ``getCodeObjectAccessCode`` directly.

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

-  Moved the experimental feature indications into
   ``nuitka.options.Experimental``, a low-level module without
   dependencies, avoiding import cycles with distribution and execution
   helpers.

-  Removed the ``no-iterator-optimization`` experimental flag, which was
   never needed to disable the indexable iterator unpacking
   optimization.

-  Built-in type method helper generation now uses versioned parameter
   specs collected in ``Common``, with version specific conditions in C
   and version specific specs in the attribute node templates.

-  Cleaned up comments and docstrings across the runtime, freezer,
   installer, option, target, tool, and utility modules, in build and
   code generation code, in AST and optimization code, and in the plugin
   hook documentation, removing code narration, stale comments, and
   restatements of the code.

-  Generated classes and helpers no longer emit ``Generated from ...``
   boilerplate or duplicated method docstrings, and TODOs are kept in
   the templates instead of being generated into the code.

-  Builtin keyword-only arguments are now passed as keywords to
   optimized builtin node constructors, and the ``sentinel`` extractor
   maps its ``repr`` argument to the ``repr_value`` child.

-  Removed the duplicate Python2 ``bytes.decode`` spec.

-  Further cleaned up comments and docstrings across optimization, tree,
   specification, and finalization modules, including the locals
   dictionary construction code and the slice shape mixin description.

-  Used the compile-time constant type accessor for unicode key checks
   and the shared ``EllipsisType`` for pickle dispatch.

-  The try/finally node builders now assert the Python versions they are
   used for, and the Python 3 path calls the common builder directly
   instead of going through the Python 2-only wrapper.

-  Future imports and the future spec are now restored and cleared in a
   ``finally`` block after building a module, and other ``RuntimeError``
   exceptions are re-raised instead of being swallowed.

-  Removed restating comments and replaced stale or overly long
   docstrings with concise descriptions of non-obvious contracts across
   the build system, C runtime, and code generation.

-  Parameter specs now validate that argument names are tuples or lists
   of strings, and the ``splitlines`` specs were corrected to pass
   tuples.

-  Attribute lookup helpers are now generated from a specialization
   template, so the duplicated lookup logic is maintained consistently.
   The generated bool and int helpers now match ``hasattr`` semantics,
   clearing only ``AttributeError`` where required and returning the
   documented values.

-  Node classes now require all bases to be actual classes derived from
   ``object``, so slot checks apply to all of them.

-  Removed stale tooling: the mercurial autoformat exclusion, the
   obsolete ``macos_bundle_as_onefile`` schema entry, and the
   ``update-doc.py`` documentation sync tool.

-  Added braces to C conditionals, removed duplicate checks after
   infallible dictionary updates, and dropped an unreachable global
   constant case.

-  Plugin YAML configuration values are now yielded only once per
   recursive lookup, and duplicate list entries are rejected by the
   schema.

-  **Debugging:** The experimental toggles that disable the vectorcall
   slot, vectorcall usage, and uncompiled function call optimization now
   consistently gate all their uses, and the manual vectorcall fallback
   was removed.

-  Enabled additional ``ruff`` checks for boolean simplification,
   collection construction, dictionary iteration, string prefixes, and
   static string splitting, and applied the mechanical fixes.

-  Renamed ``once_decorator`` to ``onceDecorator``, replaced ``re.S``
   and ``re.M`` with ``re.DOTALL`` and ``re.MULTILINE``, and added the
   missing ``compiled_module.h`` header for IDE parsing of the module
   object layout.

-  Removed dead clcache code.

-  **Plugins:** YAML configuration helpers now return ``YamlConfigItem``
   and ``YamlConfigKeyValue`` named tuples, the ``options`` section uses
   a direct list of checks, and ``when`` is no longer accepted in
   ``variables`` and ``constants`` sections, since those are always
   defined and lazily evaluated elsewhere. The schema, formatter, and
   nanny plugin were updated.

-  Removed disabled abort checks and an unused manual long-zero
   stripping helper, simplified a debug variable-merge assertion, and
   corrected the YAML inline-copy docstring.

-  The Python 2 ``execfile`` optimization now uses
   ``makeExpressionBuiltinsOpenCall()`` with all optional arguments
   instead of constructing the open call node directly.

-  **Plugins:** Missing DLL checks now return a ``MissingDLLDecision``
   with tri-state ``decideAbstain()`` and optional reasons for
   ``decideYes()``, instead of a bare tuple.

-  Node classes now validate cloning interfaces: ``named_children``
   requires ``getCloneArgs()``, ``node_attributes`` requires
   ``getDetails()``, and required non-child parameters need details.
   Function and module cloning details were filled in, and unused
   ``makeCloneShallow()`` was removed.

-  Removed the duplicate module-level ``redactCommandLineArg`` helper
   and import it from the hooks module instead.

-  **Quality:** Generated IDE-only include blocks now keep dependent
   includes after the prelude, a missing iterator include and the
   ``FLY002`` ignore were added, and ``MAKE_LIST`` preallocation is
   documented.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
