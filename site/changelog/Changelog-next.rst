:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.3rc5**.

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

-  Fix, comparisons and add or subtract operations of Python ``long``
   values with C ``long`` operands could produce wrong results. (Fixed
   in 4.2.1 already.)

-  **Python 3.14:** Fix, deferred annotations did not work with hard
   import names, e.g. ``io.BytesIO``, since those were unnecessarily
   generated as ``__import__`` calls. (Fixed in 4.2.1 already.)

-  **Python 3.14:** Fix, the
   ``--devel-no-bytecode-to-compiled-fallback`` option was not honored
   when source generation for an ``__annotate__`` function failed, where
   the fallback to compiled code happened anyway. (Fixed in 4.2.1
   already.)

-  **Python 3.14:** Fix, source generation for ``__annotate__``
   functions did not handle closures, constants, and calls correctly.
   Closure variables were then rejected to fall back to compiled code,
   and values like non-finite floats, empty sets, and types from modules
   are rendered as valid source. (Fixed in 4.2.1 already.)

-  **Plugins:** Fix, nested uses of the ``forkserver`` context were not
   working. (Fixed in 4.2.1 already.)

-  **Compatibility:** Fix, conditional expressions did not decide their
   type shapes from the branches properly, which could lead to wrong
   optimization of list appends and subscript operations. (Fixed in
   4.2.2 already.)

-  **Compatibility:** Fix, keyword arguments created from ``str``
   subclass instances were rejected, since the check compared the exact
   type instead of allowing subclasses. (Fixed in 4.2.2 already.)

-  **Windows:** Fix, MSYS2 builds now link the compiler runtime
   statically, avoiding a runtime dependency on e.g.
   ``libwinpthread-1.dll``, which also fixes module mode requiring that
   DLL. (Fixed in 4.2.2 already.)

-  **MSYS2:** Fix, adapting Python header files did not work on that
   flavor yet. (Fixed in 4.2.2 already.)

-  **macOS:** Fix, newer Xcode versions only ship tools like
   ``install_name_tool``, ``lipo``, ``nm``, and ``otool`` as ARM64
   binaries, which fail to run in an ``x86_64`` translated process.
   These are now invoked with ``arch -arm64`` as needed, and the same
   for the C compiler and ``ccache``. (Fixed in 4.2.2 already.)

-  **Debian:** Fix, onefile mode was no longer usable when the ``zstd``
   inline copy is absent, e.g. in the official Debian package, since the
   system ``zstd`` and ``zlib`` are now linked statically instead.
   (Fixed in 4.2.2 already.)

-  **Installer:** Fix, Linux installer creation crashed in onefile mode,
   now informs the user that ``--mode=app-dist`` (or
   ``--mode=standalone``) mode is required. (Fixed in 4.2.2 already.)

-  Fix, when outline functions were removed, e.g. class bodies that
   raise, the variable tracing was not undone, so the value traces could
   be inconsistent, this is now reversed properly.

-  Fix, cloned outline functions did not copy the variables they take
   from the enclosing scope, so the clones could lack closure variables.

-  Fix, the context manager for directory changes only restored the
   previous directory on success, now it does so also on errors, which
   the ``nuitka-watch`` tool depends on.

-  Fix, recursion decisions for modules restored from the bytecode cache
   could differ from a cold cache, since the excluded module names were
   derived from the decision cache rather than the module usages.

-  Fix, temporary variable names in cloned outline functions, e.g. from
   comprehensions in ``finally`` blocks, could collide with the ones of
   the original, giving wrong results.

-  Fix, async generator expressions had a code object kind of a plain
   generator, which could give incorrect behavior for them.

-  Fix, the generator heap space was limited to a hard coded 1024 bytes,
   which could overflow and crash for very complex generators, now the
   exact needed size is captured, which also reduces context memory for
   running generators.

-  Fix, dictionaries put into containers were not escaped, so mutating a
   constant dictionary through the container could corrupt compile time
   decisions made for it.

-  Fix, ``visitTree`` recursed once per node, so very deep node trees
   could exceed the Python recursion limit and raise ``RecursionError``
   during finalization, variable closure and inlining, they are now
   visited iteratively, which is also a lot faster.

-  Fix, the traceback of exceptions thrown into not yet started
   generators, coroutines, and async generators was not preserved, the
   frame is now added to an existing traceback, and the traceback of an
   exception instance that is thrown is used when none is given.

-  **Python 3.5+:** Fix, generators decorated with ``types.coroutine``
   were not awaitable, since the compiled generator type did not
   implement the ``__await__`` slot, which returns itself for iterable
   coroutines now, and raises the matching ``TypeError`` otherwise.

-  **Python 3.5+:** Fix, two phase initialization of extension modules
   below compiled packages was not working, as their module definition
   was not executed, which e.g. left ``gi._gi`` without its attributes.

-  **Python 3.5:** Fix, the runtime YAML checks used exact ``dict`` type
   comparisons, which failed for the ordered dictionaries used before
   Python 3.6, giving errors for valid configurations.

-  **Python 3.6+:** Fix, the ``__classcell__`` value was set through the
   dictionary API, which is wrong when the class namespace is a custom
   mapping returned by the ``__prepare__`` method, and is now set
   through the mapping interface like the class body does.

-  **Python 3.7+:** Fix, asynchronous generator expressions inside
   synchronous generator expressions were detected as making the outer
   expression asynchronous as well, while only the inner scope is
   asynchronous.

-  **Python 3.7+:** Fix, namespace packages did not set ``__file__`` to
   ``None`` like CPython does since that version, which could make
   detecting namespace packages already loaded at compile time differ.

-  **Python 3.8+:** Fix, assignment expressions inside generator
   expressions bound their target in the module when the enclosing
   function did not otherwise use the name, since it had no such
   variable, now the target is made a variable of the enclosing
   function.

-  **Python 3.10+:** Fix, duplicate constant keys of mapping patterns
   were not rejected at compile time, duplicate non-constant keys were
   not checked at match time, and class pattern matching leaked
   references in some cases.

-  **Python 3.11+:** Fix, the ``except*`` support was incomplete and
   barely usable, now each handler is matched against the remaining
   exception group in sequence, the match is published as the current
   exception for ``sys.exc_info()`` and a bare ``raise``, exceptions
   raised by handlers are collected, and the unhandled remainder is
   raised again with the matching context.

-  **Python 3.11+:** Fix, the ``eval`` built-in did not accept
   ``globals`` and ``locals`` as keyword arguments that Python 3.13
   allows, while for ``exec`` these arguments are positional only in
   Python 3.11 and 3.12, which is now enforced as well.

-  **Python 3.12:** Fix, type variables of a class had the wrong scope,
   which put them into the class dictionary instead of an enclosing
   scope, they now get a dedicated scope, making them usable from
   methods and bases, but not visible as class attributes.

-  **Python 3.12:** Fix, threading could dead lock, since the evaluation
   breaker did not consider work indications of the main thread.

-  **Python 3.12+:** Fix, the ``__bound__`` of type variables was always
   ``None``, since the bound was not used when creating them.

-  **Python 3.12+:** Fix, the awaitables of ``aclose()`` and
   ``athrow()`` of asynchronous generators were not closed when they
   terminated the generator, so reusing them gave ``StopIteration``
   instead of the matching errors, and for Python 3.13 and higher,
   ``asend().close()`` and ``athrow().close()`` now use
   ``throw(GeneratorExit)``.

-  **Python 3.12+:** Fix, the ``__module__`` attribute of type
   variables, parameter specifications, and type variable tuples was
   wrong, since compiled frames lack the function object for the runtime
   to determine it from, which is now patched.

-  **Python 3.12+:** Fix, the patched ``sys._getframemodulename`` looked
   up ``__name__`` as an attribute of ``f_globals`` instead of a
   dictionary key, required the depth argument although it is optional,
   and registered a wrong method name.

-  **Python 3.12+:** Fix, the bound of type variables was evaluated
   immediately, instead of only when ``__bound__`` is accessed, which
   could run expressions too early, especially in classes.

-  **Python 3.13:** Fix, the new internal ``_IncompleteInputError``
   exception was not supported, e.g. when used in tuples of caught
   exception types.

-  **Python 3.14+:** Fix, ``__annotate__`` functions now have frames,
   since they can use closure variables and must be able to raise
   errors.

-  **Python 3.14+:** Fix, objects that are already immortal had their
   reference counter modified by the static immortal handling, degrading
   them from static immortals to plain immortals and changing e.g.
   ``sys.getrefcount`` values, which is now avoided.

-  **Python 3.14+:** Fix, the compiled types used the CPython generic
   attribute and allocation functions directly, which debug mode on
   Windows rejects, they are now set up by ``Nuitka_PyType_Ready`` from
   indicators instead.

-  **Python 3.15:** Fix, the ``_math_integer`` extension module was
   missing from the standard library modules known to never raise on
   import, which prevented optimizing its imports.

-  **Python 3.15:** Fix, the ``Py_GetPath`` API was no longer available,
   requiring an explicit declaration again.

-  **Python 3.15:** Fix, the older inline copy of Scons no longer works
   there, now all Python 3.7+ versions use the newer copy that was
   previously only used on Windows.

-  **Python 3.15:** Fix, creating ``long`` objects triggered assertions
   there, since the tag field needs initialization before setting the
   sign and digit count.

-  **Python 3.15:** Fix, the layout of type variable objects gained a
   ``qualname`` field that needs to be filled in from the code object of
   the function that computes the value.

-  **Standalone:** Fix, the source package ``__init__.py`` is now
   preferred over a C extension ``__init__.so`` or ``__init__.pyd``
   file, respecting the recompile decisions of the user, whose plugin
   queries are now also cached.

-  **Standalone:** Fix, packages with both source and extension module
   files gave duplicate module entries when included by the user, now
   the recompile decision decides the preferred one, like it already did
   for package ``__init__`` files.

-  **Reports:** Fix, plugin report data was silently discarded, since
   the report generation did not use the key/value pairs and swallowed
   all errors, it is now included and validated.

-  **Plugins:** Fix, plugins that put files into the build directory
   could not do that after other processing, as the directory was
   removed before the final result callback, which is now called first.

-  **Windows:** Fix, the experimental MinGW64 usage with Python 3.13 and
   higher did not work in Python debug mode, as the internal structure
   offsets for debug builds were missing.

-  **Windows:** Fix, NTFS junctions were not resolved before the drive
   letter check when testing if a filename is inside a path, so e.g.
   relative report paths could escape their prefix.

-  **Windows:** Fix, the increased stack size was not applied to onefile
   DLL mode, as it was only done in EXE mode.

-  **MSYS2:** Fix, normalized paths were missing in plugin and DLL
   handling, e.g. for the ``pywin32`` system directory and ``glfw``
   library paths.

-  **macOS:** Fix, code signing no longer mutates the keychain file,
   since the ``security`` commands change it in place, a temporary copy
   is now used instead.

-  **macOS:** Fix, the architecture prefix is now also applied to
   ``git`` and other tool invocations in the process execution helpers,
   since these only exist as ARM64 binaries in newer Xcode versions,
   which broke e.g. the test tooling in translated ``x86_64`` processes.

-  **macOS:** Fix, debugging translated ``x86_64`` binaries on Rosetta
   did not work, since the ``lldb`` shim of newer Xcode is ARM64 only,
   now getting the ``arch`` prefix, and the debug server requires the
   binary to allow being debugged, so accelerated mode with a
   ``--debugger`` is now signed with the entitlements that standalone
   mode already uses.

-  **Compatibility:** Fix, nested frames used the same exception line
   number storage, leading to corruption of either the inner or outer
   line numbers in exceptions, they now have separate storage.

-  **Compatibility:** Fix, values used in ``and`` and ``or`` expressions
   could lose their escape tracking, so e.g. adding to a set through
   them could corrupt values, they now handle their operands like the
   conditional expressions do.

-  **Scons:** Fix, the linker response file workaround for command line
   length limits was only used for GCC mode, so linking could fail with
   many modules for Clang and Zig modes, which now benefit from it as
   well.

-  **Scons:** Fix, the target of the build is now always created as
   ``_nuitka_temp`` with the proper extension in the build directory and
   renamed into place after the build, avoiding paths that the C
   compiler cannot encode, e.g. for Unicode output binary filenames.

-  **Scons:** Fix, the stack size limit of the scons process is now
   raised on non-Windows, so compiling very large generated source files
   cannot crash the C compiler child processes with a stack overflow.

-  **AIX:** Fix, COFF dump based dependency detection for archives now
   extracts object members to a temporary file before dumping them,
   since the direct member selection was not portable.

-  **OpenBSD:** Added support for getting the binary path on OpenBSD 8
   using the ``getexecpath`` function intended for that.

Package Support
===============

-  **Standalone:** Added support for newer ``PyAV``. (Added in 4.2.1
   already.)

-  **Standalone:** Fix, ``vtk8`` was no longer working, since the
   package path configuration was needlessly restricted to ``vtk``
   version 9 and higher. (Fixed in 4.2.1 already.)

-  **Standalone:** Added support for the latest ``toga`` on macOS, with
   the ``toga_cocoa.resources`` dependency now included. (Added in 4.2.1
   already.)

-  **Standalone:** Added support for Tkinter version 9.1.

-  **Plugins:** Fix, the ``PySide6`` ``singleShot`` timer workaround
   protected the wrong argument when called with more arguments,
   allowing the issue it is meant to avoid to occur. (Fixed in 4.2.1
   already.)

-  **Plugins:** Made ``PySide6`` work in module mode using configuration
   references.

-  **Plugins:** Added support for ``gi.repository`` namespaces, using
   virtual modules that resolve them at run time and include their
   typelib dependencies, replacing the previous inclusion of all typelib
   files.

-  **Plugins:** Added support for newer versions of the ``lazy_loader``
   package, using its ``attach_stub`` interface rather than the private
   stub visitor.

New Features
============

-  **Python 3.13:** Added a "FrameLocalsProxy" implementation, with
   frame locals of compiled functions now held in a C struct that the
   frame can point at, and available for all scopes with
   ``--experimental=force-locals-frame-proxy``, where the proxy is a
   write-through mapping, coming with a performance penalty.

-  **Python 3.14:** Added source generation for function calls and more
   hard import types for ``__annotate__`` functions. (Added in 4.2.1
   already.)

-  **Python 3.14:** Added source generation for more constant value
   types for ``__annotate__`` functions, e.g. ``bytes``, ``range``,
   ``slice``, ``bytearray``, and ``complex`` values, including
   non-finite components. (Added in 4.2.1 already.)

-  **Python 3.15:** Pronounced Python 3.15 as partially supported.

-  **Python 3.15:** Added support for unpacking in comprehensions, e.g.
   ``[*i for i in values]`` and ``{**d for d in mappings}``, including
   the async variants.

-  **Python 3.15:** Added support for the new ``frozendict`` type as a
   constant, including optimization of its constant values, where deep
   copies are only made when nested values can still change.

-  Package configuration can now reference other configurations with
   ``include-config``, and configure the main module through the
   ``<main>`` pseudo name.

-  **Plugins:** Added support for virtual modules, i.e. modules that
   plugins provide generated source code for, used for modules that only
   exist at run time, and that can also be included on the command line.

-  **PGO:** The class dictionary shape of ``__prepare__`` call results
   is now detected and captured, allowing classes with a plain
   dictionary namespace to benefit from optimizations, with mismatches
   ignored by default, raising a ``RuntimeError`` when the
   ``pgo-assertions`` non-deployment flag is active, and aborting in
   debug mode.

-  **UI:** Added the ``__uncompiled__`` module value for modules
   provided as bytecode, with the same information as ``__compiled__``,
   so ``globals().get("__uncompiled__", globals().get("__compiled__"))``
   tells whether Nuitka provided a module, whether compiled or as
   bytecode, and the new ``python_runtime_dir`` and ``process_exe``
   fields of ``__compiled__`` replace the deprecated
   ``__nuitka_binary_dir`` and ``__nuitka_binary_exe`` variables.

-  **Plugins:** Implicit imports can now have a reason provided by the
   plugin, and compilation reports include implicit module usages with
   it, making it easier to see where and why a module was added.

-  **Windows:** Added age based cleanup for ``clcache``, removing cache
   entries not modified for a while, controlled by the
   ``NUITKA_CLCACHE_MAX_AGE_DAYS`` environment variable, defaulting to
   30 days, with a value of 0 disabling it, and performed at most every
   ``NUITKA_CLCACHE_CLEANUP_INTERVAL_DAYS`` days, defaulting to 7,
   replacing the previous maximum size based full cleanup.

Optimization
============

-  **Standalone:** Moved implicit import consideration from module
   recursion into the optimization pass, avoiding an unnecessary third
   pass for standard library modules using a cold bytecode cache. (Added
   in 4.2.2 already.)

-  **Standalone:** Enabled LTO for the "Python Build Standalone" flavor
   as well, since it is known to be supported. (Added in 4.2.2 already.)

-  **Standalone:** The import lowering to fixed and hard imports now
   also handles the ``fromlist`` submodule imports that ``__import__``
   performs, so those apply there correctly.

-  Unpacking from values that are known to be indexable now uses direct
   subscript access instead of the iterator protocol, making e.g. ``a, b
   = some_tuple`` a lot faster, with starred unpacking to follow once
   this has proven stable.

-  The ``io.open`` built-in is now treated like ``open``, so that file
   tracing for embedded data files applies to it as well.

-  Loop value traces now detect identity stability of values, enabling
   more optimizations, and when the loop analysis gives up, the continue
   traces are now reversed properly, which could otherwise produce false
   results.

-  Slice values built from constants are now cached, except when they
   contain mutable values, which are still created at runtime to avoid
   corruption.

-  Internal source code references are now actually used again, which
   was lost in a memory saving refactor years ago, lowering the
   generated code amount for some constructs.

-  Replaced runtime assertions with static assertions where possible,
   using a shared ``STATIC_ASSERT`` helper.

-  The meta path loader entries now reference their pre-load, post-load,
   and parent entries directly rather than relying on name based
   lookups, with the main module now determined by a flag rather than
   its name.

-  Avoided passing the frozen module count as a C define, since that
   could break caching, using an accessor function instead.

-  Module and class code objects are now specialized with fixed details,
   saving constant blob space, and the module code object name is now
   always ``<module>``, which actual upstream code relies on to identify
   module frames.

-  Generator expression code objects are now specialized, since they
   lack attributes of functions, saving space and sharing the
   ``<genexpr>`` name.

-  Direct CPython C-API calls were replaced with Nuitka helper
   replacements where they exist, e.g. ``LOOKUP_ATTRIBUTE`` and
   ``SET_SUBSCRIPT``, which is mostly a cleanup, but relevant for the
   locals dictionary handling at startup.

-  Binary operations of compile time constants are now folded during
   tree building already, avoiding optimization churn and giving
   compatible ``match`` behavior, e.g. for folded complex literals.

-  Compile time constant folding now uses the same limits as CPython for
   too large results, e.g. 128 bit integers for multiplication, 256
   items for collections, and 4096 characters for strings.

-  **macOS:** The Homebrew rpath scan is now limited to directories that
   hold libraries, pruning include, docs and other trees, which
   previously registered tens of thousands of paths on every standalone
   build.

-  Package configuration parsing now prefers the C based ``CSafeLoader``
   of a libyaml built PyYAML when available, and caches the ordered
   loader class, making it several times faster on the large
   configuration file.

-  The ``try``/``else`` construct no longer uses an indicator variable
   when the handling aborts, since only normal completion of the ``try``
   block can reach the ``else`` block then.

-  Loop traces that are not used no longer mark late attached continue
   traces as used, which could prevent dead assignment removal.

-  The generated ``getVisitableNodes`` implementations now use tuple
   literals and concatenation instead of building and converting lists,
   which speeds up tree visits for many node types.

Anti-Bloat
==========

-  Avoided using ``pydoc`` in the official ``PySimpleGUI`` package as
   well, which so far was only done for the non-official one. (Fixed in
   4.2.1 already.)

Organizational
==============

-  **UI:** Made the ``--file-description`` help text clear that it is no
   longer Windows only, as it is also used as the summary of the
   AppStream metadata of Linux ``--mode=app`` mode. (Fixed in 4.2.1
   already.)

-  **Release:** Added ``clangd`` to the CI container to allow checking
   with it. (Added in 4.2.2 already.)

-  **Release:** Made it clear that on Python 3.14 and higher, the
   standard library ``compression.zstd`` is used instead of the
   ``zstandard`` package in the requirements.

-  **AI:** Added the ``setup-pr-branch`` skill for setting up fork pull
   request branches for pushing updates, pointed the
   ``module-not-found`` skill at the MRE workflow, and ignored the
   scratch folder used for AI work.

-  **Docs:** Made it clear in the Developer Manual that Python 3.14 is
   covered by feature parity.

-  **Docs:** Integrated the website documentation changes into the User
   Manual, including the report template data tables and the CPU
   architecture baseline section.

-  **Quality:** Disabled more ``ruff`` warnings that are not important
   for Nuitka, and enhanced the ``clangd`` and Visual Code configuration
   for correctness.

-  **UI:** The error message for ``--static-libpython=yes`` with the
   "Python Build Standalone" flavor now includes a hint for downloading
   the full build that supports it.

-  **Quality:** Made the check for unpushed files work for branches
   without a remote, comparing against the merge base or default branch
   instead.

-  **Docs:** Removed the Doxygen based API documentation generation and
   its tooling, as it never reached a usable state and is not used
   anymore.

-  **Scons:** Slow C compilation reports now name the C file that caused
   them, making it easier to identify scalability problems.

-  **Quality:** The private pip space is now usable with multiple
   site-packages layouts, e.g. from different Python installations of
   it, considering all of them instead of refusing.

-  **UI:** Added the ``--pgo-json`` option to write the PGO input file
   contents as JSON for debugging and testing, and the
   ``--devel-pgo-warn-unknown`` option to report PGO values that are not
   usable.

-  **AI:** The verification rules now hint at using the WSL host Python
   installations through ``/mnt/c``.

-  **Debian:** The package builder image script now uses archive URLs
   for old Debian and Ubuntu releases, trusts the expired ``jessie``
   archive key explicitly, and includes ``aptitude`` needed for the
   dependency resolution of pbuilder.

-  **Quality:** The pre-push hook now allows downloads for the
   ``pylint`` checks, like the formatting checks already do.

-  **Quality:** Tools of the private pip space that cannot be executed
   at all are quietly treated as not existing, so that a broken binary
   no longer stops their download.

-  **UI:** The anti-bloat plugin option help no longer advertises the
   ``nofollow`` choice, which was only available as a regular user
   command line option since last release.

-  **Scons:** ccache files are now stored in a directory per Python ABI
   version, so that cache cleanup does not interfere between versions.

Tests
=====

-  Added support for the ``win32``, ``linux``, and ``macos`` variables
   in ``wait_for`` conditions of ``nuitka-watch`` test cases. (Added in
   4.2.1 already.)

-  Added ``--devel-no-bytecode-to-compiled-fallback`` to
   ``nuitka-watch`` compilations with Python 3.14 and higher, requiring
   that annotate functions do not fall back to compiled code for the
   packages we actively monitor.

-  The test runner now displays the full Python version string, which is
   useful for release candidate versions, where the numeric version
   alone is ambiguous.

-  Allowed to specify test names without their version specific suffixes
   in the test runner.

-  Enhanced the XML comparison utility to run Nuitka with
   ``--generate-c-only`` and ``--nofollow-imports``, comparing the XML
   output files directly.

-  Fixed the ``BrotliUsing`` and ``PmwUsing`` tests to specify
   standalone mode, so they become usable of their own.

-  Avoided specifying default file reference choices in the CPython
   comparison tool, where they only cause warnings.

-  The test runner now supports the ``_3.py`` suffix for tests that
   require Python 3 at minimum, replacing the previous ``32`` suffix
   that was used for those.

-  The test runners now support ``--pattern`` filters and a ``--skip``
   option that implies resuming, with the ``only``, ``resume``,
   ``skip``, ``search``, ``coverage``, and ``all`` shortcuts adjusted,
   and partial runs no longer update or delete the resume state.

Cleanups
========

-  The temporary filename context manager now deletes the file itself,
   also on errors, simplifying its users such that don't have to do it.
   (Fixed in 4.2.1 already.)

-  **Quality:** Addressed the warnings reported by the ``clangd`` LSP,
   adding shared headers for the long digit, dictionary internal, power,
   and repeat helpers, and organizing the IDE only includes.

-  **Quality:** Updated the inline copy of ``hedley`` to the latest
   version, and added the dump backtraces declaration for the ``clangd``
   LSP.

-  Generalized the deferred release handling in code generation, now
   allowing values to be released at the end of their code scope when
   needed.

-  **Debugging:** Fixed that disabling all free lists was not fully
   effective, since the release path still used them.

-  Unbound local and closure errors are now formatted by helpers from
   the frame's code object, removing the per-raise-point variable name
   constants and inline exception chaining.

-  Removed dead code for generator expression frames that was no longer
   used.

-  Removed the ``--experimental=old-code-objects`` support, as the
   constants blob based code objects are the only mechanism now.

-  De-duplicated the ``MODLIBS`` entries used for linking.

-  Node classes can now use comma separated conditions, e.g. ranges, in
   their ``python_version_spec`` declaration.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
