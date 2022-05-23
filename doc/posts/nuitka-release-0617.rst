.. post:: 2021/11/11 13:40
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.6.17
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release has a focus on performance improvements, while also
polishing plugins and adding many new features.

***********
 Bug Fixes
***********

-  Fix, plugins were not catching being used on packages not installed.
   Fixed in 0.6.16.2 already.

-  macOS: Fix weaknesses in the ``otool`` parsing to determine DLL
   dependency parsing. Fixed in 0.6.16.2 already.

-  Linux: Allow onefile program args with spaces contained to be
   properly passed. Fixed in 0.6.16.3 already.

-  Windows: Avoid using less portable C function for ``%PID%``
   formatting, which restores compilation on Windows 7 with old
   toolchains. Fixed in 0.6.16.3 already.

-  Standalone: Added support for ``fstrings`` package. Fixed in 0.6.16.3
   already.

-  Compatibility: Fix, need to import ``.pth`` files after ``site``
   module, not before. This was causing crashes on CentOS7 with Python2.
   Fixed in 0.6.16.3 already.

-  Compatibility: Fix, when extension modules failed to load, in some
   cases the ``ImportError`` was lost to a ``KeyError``. Fixed in
   0.6.16.3 already.

-  Fix, linker resource modes ``code`` and ``linker`` were not working
   anymore, but are needed with LTO mode at least. Fixed in 0.6.16.3
   already.

-  Standalone: Bytecode modules with null bytes in standard library,
   typically from disk corruption, were not handled properly. Fixed in
   0.6.16.3 already.

-  Fix, failed ``.throw()`` into generators could cause corruption.
   Fixed in 0.6.16.4 already.

-  Python2: Fix, the bytecode compilation didn't respect the
   ``--python-flag=no_asserts`` mode. Fixed in 0.6.16.4 already.

-  Fix, calls were not annotating their arguments as escaped, causing
   corruption of mutable in static optimization. Fixed in 0.6.16.5
   already.

-  Fix, some sequence objects, e.g. ``numpy.array`` actually implement
   in-place add operations that need to be called. Fixed in 0.6.16.5
   already.

-  Windows: Fix, onefile binaries were not working after being signed.
   This now works.

-  Standalone: Added missing implicit dependency for ``sklearn``.

-  Compatibility: Modules giving ``SyntaxError`` from source were not
   properly handled, giving runtime ``ImportError``. Now they are giving
   ``SyntaxError``.

-  Fix, the LTO mode has issues with ``incbin`` usage on older gcc, so
   use ``linker`` mode when it is enabled.

-  Python3: Fix, locals dict codes were not properly checking errors
   that the mapping might raise when setting values.

-  Fix, modules named ``entry`` were causing compile time errors in the
   C stage.

-  macOS: Never include files from OS private frameworks in standalone
   mode.

-  Fix, the python flag ``--python-flag=no_warning`` wasn't working on
   all platforms.

-  Compatibility: Fix, the main code of the ``site`` module wasn't
   executing, so that its added builtins were not there. Of course, you
   ought to use ``--python-flag=no_site`` to not have it in the normal
   case.

-  Python2: Added code path to handle edited standard library source
   code which then has no valid bytecode file.

-  Anaconda: In module mode, the CondaCC wasn't recognized as form of
   gcc.

-  Fix, bytecode modules could shadow compiled modules of the same name.

-  Onefile: Fix, expansion of ``%PID%`` wasn't working properly on
   non-Windows, making temp paths less unique. The time stamp is not
   necessarily enough.

-  Fix, ``multiprocessing`` error exits from slave processes were not
   reporting tracebacks.

-  Standalone: Added ``xcbglintegrations`` to the list of sensible Qt
   plugins to include by default, otherwise rendering will be inferior.

-  Standalone: Added ``platformthemes`` to the list of sensible Qt
   plugins to include by default, otherwise file dialogs on non-Windows
   would be inferior.

-  Fix, created ``.pyi`` files were not ordered deterministically.

-  Standalone: Added support for ``win32file``.

-  Fix, namespace packages were not using runtime values for their
   ``__path__`` value.

-  Python3.7+: Fix, was leaking ``AttributeError`` exceptions during
   name imports.

-  Fix, standard library detection could fail for relative paths.

**************
 New Features
**************

-  Added experimental support for C level PGO (Profile Guided
   Optimization), which runs your program and then uses feedback from
   the execution. At this time only gcc is supported, and only C
   compiler is collecting feedback. Check the User Manual for a table
   with current results.

-  macOS: Added experimental support for creating application bundles.
   For these, icons can be specified and console can be disabled. But at
   this time, onefile and accelerated mode are not yet usable with it,
   only standalone mode works.

-  Plugins: Add support for ``pkg_resources.require`` calls to be
   resolved at compile time. These are not working at runtime, but this
   avoids the issue very nicely.

-  Plugins: Massive improvements to the ``anti-bloat`` plugin, it can
   now make ``numpy``, ``scipy``, ``skimage``, ``pywt``, and
   ``matplotlib`` use much less packages and has better error handling.

-  Plugins: Added ``anti-bloat`` ability ability to append code to a
   module, which might get used in the future by other plugins that need
   some sort of post load changes to be applied.

-  Plugins: Added ability to replace code of functions at parse time,
   and use this in ``anti-bloat`` plugin to replace functions that do
   unnecessary stuff with variants that often just do nothing. This is
   illustrated here.

   .. code:: yaml

      gevent._util:
      description: "remove gevent release framework"
      change_function:
         "prereleaser_middle": "'(lambda data: None)'"
         "postreleaser_before": "'(lambda data: None)'"

   This example is removing ``gevent`` code that loads dependencies used
   for their CI release process, that need not be part of normal
   programs.

-  Added ability to persist source code changes done by plugins in the
   Python installation. This is considered experimental and needs write
   access to the Python installation, so this is best done in a
   virtualenv and it may confuse plugins.

-  Added support for ``multiprocessing.tracker`` and spawn mode for all
   platforms. For non-default modes outside of Windows, you need to
   ``--enable-plugin=multiprocessing`` to use these.

-  Plugins: Allow multiple entry points to be provided by one or several
   plugins for the same modules. These are now merged into one
   automatically.

-  Standalone: Fix for numpy not working when compiling with
   ``--python-flag=no_docstrings``.

-  Fix, method calls were not respecting descriptors provided by types
   with non-generic attribute lookups.

-  Windows: Add support for using self-compiled Python3 from the build
   folder too.

-  Added support for Nuitka-Python 2.7, which will be our faster Python
   fork.

-  Colorized output for error outputs encountered in Scons, these are
   now yellow for better recognition.

**************
 Optimization
**************

-  Faster threading code was used for Python3.8 or higher, and this has
   been extended to 3.7 on Windows, but we won't be able to have it
   other platforms and not on earlier Python3 versions.

-  Faster calls esp. with keyword arguments. Call with keywords no
   longer create dictionaries if the call target supports that, and with
   3.8 or higher, non-compiled code that allows vectorcall is taken
   advantage of.

-  Faster class creation that avoids creation of argument tuples and
   dictionaries.

-  Faster attribute check code in case of non-present attributes.

-  Faster unbound method calls, unlike bound methods calls these were
   not optimized as well yet.

-  Type shapes for star arguments are now known and used in
   optimization.

   .. code:: python

      def f(*args, **kwargs):
         type(args) # Statically known to be tuple
         type(kwargs) # Statically known to be dict

-  Python2: Faster old-style class creation. These are classes that do
   not explicitly inherit from ``object``.

-  Python2: Faster string comparisons for Python by specializing for the
   ``str`` type as well.

-  Python3: Added specialization for ``bytes`` comparisons too. These
   are naturally very much the same as ``str`` comparisons in Python2.

-  Added specialization for ``list`` comparisons too. We had them for
   ``tuples`` only so far.

-  Faster method calls when called from Python core, our ``tp_call``
   slot wasn't as good as it can be.

-  Optimization: Faster deep copies of constants. This can speed up
   constant calls with mutable types. Before it was checking the type
   too often to be fast.

-  Allow using static linking with Debian Python giving much better
   performance with the system Python. This is actually a huge
   improvement as it makes things much faster. So far it's only
   automatically enabled for Python2, but it seems to work for Python3
   on Debian too. Needs more tweaking in the future.

-  Optimization: Added ``functools`` module to the list of hard imports
   in preparation of optimizing ``functools.partial`` to work better
   with compiled functions.

-  Python2: Demote to ``xrange`` when iterating over ``range`` calls,
   even for small ranges, they are always faster. Previously this was
   only done for values with at least 256 values.

-  Enable LTO automatically for Debian Python, this also allows more
   optimization.

-  Enable LTO automatically for Anaconda with CondaCC on non-Windows,
   also allowing more optimization.

****************
 Organisational
****************

-  Added section in the User Manual on how to deal with memory issues
   and C compiler bugs. This is a frequent topic and should serve as a
   pointer for this kind of issue.

-  The ``--lto`` option was changed to require an argument, so that it
   can also be disabled. The default is ``auto`` which is the old
   behaviour where it's enabled if possible.

-  Changed ``--no-progress`` to ``--no-progressbar`` in order to make it
   more clear what it's about. Previously it was possible to relate it
   to ``--show-progress``.

-  No longer require specific versions of dependencies in our
   ``requirements.txt`` and relegate those to only being in
   ``requirements-devel.txt`` such that by default Nuitka doesn't
   collide with user requirements on those same packages which
   absolutely all the time don't really make a difference.

-  Added ability to check all unpushed changes with pylint with a new
   ``./bin/check-nuitka-with-pylint --unpushed`` option. Before it was
   only possible to make the check (quickly) with ``--diff``, but that
   stopped working after commits are made.

-  Revived support for ``vmprof`` based analysis of compiled programs,
   but it requires a fork of it now.

-  Make Windows specific compiler options visible on all platforms.
   There is no point in them being errors, instead warnings are given
   when they are specified on non-Windows.

-  Added project variable ``Commercial`` for use in Nuitka project
   syntax.

-  Consistent use of metavars for nicer help output should make it more
   readable.

-  Avoid ``ast`` tree dumps in case of ``KeyboardInterrupt`` exceptions,
   they are just very noisy. Also not annotate where Nuitka was in
   optimization when a plugin is asking to ``sysexit``.

**********
 Cleanups
**********

-  Encoding names for UTF8 in calls to ``.encode()`` were used
   inconsistent with and without dashes in the source code, added
   cleanup to auto-format that picks the one blessed.

-  Cleanup taking of runtime traces of DLLs used in preparation for
   using it in main code eventually, moving it to a dedicated module.

-  Avoid special names for Nuitka options in test runner, this only adds
   a level of confusion. Needs more work in future release.

-  Unify implementation to create modules into single function. We had 3
   forms, one in recursion, one for main module, and one for plugin
   generated code. This makes it much easier to understand and use in
   plugins.

-  Further reduced code duplication between the two Scons files, but
   more work will be needed there.

-  Escaped variables are still known to be assigned/unassigned rather
   than unknown, allowing for many optimizations to still work on them.,
   esp. for immutable value

-  Enhanced auto-format for rest documents, bullet list spacing is now
   consistent and spelling of organisational is unified automatically.

-  Moved icon conversion functionality to separate module, so it can be
   reused for other platforms more easily.

*******
 Tests
*******

-  Removed ``reflected`` test, because of Nuitka special needs to
   restart with variable Python flags. This could be reverted though,
   since Nuitka no longer needs anything outside inline copies, and
   therefore no longer loads from site packages.

-  Use ``anti-bloat`` plugin in standalone tests of Numpy, Pandas and
   tests to reduce their compile times, these have become much more
   manageable now.

-  Enhanced checks for used files to use proper below path checks for
   their ignoring.

-  Remove reflected test, compiling Nuitka with Nuitka has gotten too
   difficult.

-  Verify constants integrity at program end in debug mode again, so we
   catch corruption of them in tests.

*********
 Summary
*********

This release is one of the most important ones in a long time. The PGO
and LTO, and static libpython work make a big different for performance
of created binaries.

The amount of optimization added is also huge, calls are much faster
now, and object creations too. These avoiding to go through actual
dictionaries and tuples in most cases when compiled code interacts gives
very significant gains. This can be seen in the increase of pystone
performance.

The new type specializations allow many operations to be much faster.
More work will follow in this area and important types, ``str`` and
``int`` do not have specialized comparisons for Python3, holding it back
somewhat to where our Python2 performance is for these things.

For scalability, the ``anti-bloat`` work is extremely valuable, and this
plugin should become active by default in the future, for now it must be
strongly recommended. It needs more control over what parts you want to
deactivate from it, in case of it causing problems, then we can and
should do it.

The support for macOS has been enhanced a lot, and will become perfect
in the next release (currently develop). The bundle mode is needed for
all kinds of GUI programs to not need a console. This platform is
becoming as well supported as the others now.

Generally this release marks a huge step forward. We hope to add Python
level PGO in the coming releases, for type knowledge retrofitted without
any annotations used. Benchmarks will become more fun clearly.
