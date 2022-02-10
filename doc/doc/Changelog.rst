

##############################
 Nuitka Release 0.6.20 (Draft)
##############################

Bug Fixes
=========

-  Fix, ``set`` creation wasn't annotating its possible exception exit
   from hashing values and is not as free of side effects as ``list``
   and ``tuple`` creations are. Fixed in 0.6.19.1 already.

-  Windows: Fix, experimental options got lost when switching from MSVC
   to MinGW64, making them have no effect. Fixed in 0.6.19.1 already.

-  Windows: Fix, Clang from MinGW64 doesn't support LTO at this time,
   default to ``no`` for it. Fixed in 0.6.19.1 already.

-  Debian: Fix, failed to detect Debian unstable as suitable for
   linking, it doesn't have the release number. Fixed in 0.6.19.1
   already.

-  Standalone: Added data files for ``pygsheets`` package.

-  Fix, paths from plugin related file paths need to be made absolute
   before used internally, otherwise the cache can fail to deduplicate
   them. Fixed in 0.6.19.2 already.

-  Python3: With gcc before 5, e.g. on CentOS 7, where we switch to
   using ``g++``, the gcc version checks could crash. Fixed in 0.6.19.2
   already.

-  Windows: Disable MinGW64 wildcard expansion for command line
   arguments. This was breaking command lines with arguments like
   ``--filename *.txt``, which under ``cmd.exe`` are left alone by the
   shell, and are to be expanded by the program. Fixed in 0.6.19.2
   already.

-  Standalone: Added missing implicit dependency needed for
   ``--follow-stdlib`` with Python for some uses of the ``locale``
   module. Fixed in 0.6.19.2 already.

-  Standalone: Added workarounds for newest ``numpy`` that wants to set
   ``__code__`` objects and required improvements for macOS library
   handling. Fixed in 0.6.19.3 already.

-  Windows: Caching of DLL dependencies for main programs was not really
   working, requiring to detect them anew for every standalone
   compilation. Fixed in 0.6.19.3 already.

-  Fix, wasn't checking the ``zstandard`` version and as a result could
   crash if too old versions of it. This is now checked.

-  Windows: Fix, CTRL-C from a terminal was not propagated to child
   processes on Windows. Fixed in 0.6.19.4 already.

-  Standalone: With ``certifi`` and Python3.10 the
   ``importlib.resource`` could trigger Virus scanner inflicted file
   access errors. Fixed in 0.6.19.4 already.

-  Python3.10: Reverted error back iteration past end of generator
   change for Python 3.10.2 or higher to become compatible with that
   too. Fixed in 0.6.19.5 already.

-  Standalone: Added support for ``anyio`` and by proxy for Solana.
   Fixed in 0.6.19.5 already.

-  Fix, compilation with resource mode ``incbin`` and ``--debugger`` was
   not working together. Fixed in 0.6.19.5 already.

-  Fix, format optimization of known ``str`` objects was not properly
   annotating its exception exit while being optimized away. Fixed in
   0.6.19.5 already.

-  Windows: Fix, ``clcache`` didn't work for non-standard encoding
   source paths due to using th direct mode, where wrong filenames are
   output by MSVC. Fixed in 0.6.19.5 already.

-  Windows: Fix, ``ccache`` cannot handle source code paths for
   non-standard encoding source paths. Fixed in 0.6.19.5 already.

-  Python2.6: Fix, calls to ``iteritems`` and ``iterkeys`` on known
   dictionary values could give wrong values. Fixed in 0.6.19.5 already.

-  Fix, the value of ``__module__`` if set by the metaclass was
   overwritten when creating types. Fixed in 0.6.19.6 already.

-  Plugins: Add support for the latest version of ``pkg_resources`` that
   has "vendored" even more packages. Fixed in 0.6.19.6 already.

New Features
============

-  Added support for compression in onefile mode through the use of an
   other Python installation, that has the ``zstandard`` module
   installed. With this it will work with 2.6 or higher, but require a
   3.5 or higher Python with it installed in either ``PATH`` or on
   Windows in the registry alternatively.

-  Added UPX plugin to compress created extension modules and binaries
   and for standalone mode, the included DLLs. For onefile, the
   compression is not useful since it is as payload already compressed.

-  Added more explicit way to list usable MSVC versions with
   ``--msvc=list`` rather than requiring an invalid value. Check values
   given in the same way that Scons will do.

Optimization
============

-  Standalone: Do not include ``encodings.bz2_codec`` and
   ``encodings.idna`` anymore, these are not file system encodings, but
   require extension modules.

Organisational
==============

-  There is now a `Discord server for Nuitka community
   <https://discord.gg/nZ9hr9tUck>`__ where you can hang out with the
   developers and ask questions. It is mirrored with the Gitter
   community chat, but offers more features.

-  Added section to User Manual that explains how to manually load
   files, such that it is cleaner and compatible code.

-  Report the MSVC version in Scons output during compilation.

Summary
=======

This release is not done yet.


######################
 Nuitka Release 0.6.19
######################

This release adds support for 3.10 while also adding very many new
optimization, and doing a lot of bug fixes.

Bug Fixes
=========

-  Calls to ``importlib.import_module`` with expressions that need
   releases, i.e. are not constant values, could crash the compilation.
   Fixed in 0.6.18.1 already.

-  After a fix for the previous release, modules that fail to import are
   attempted again when another import is executed. However, during this
   initialization for top level module in ``--module`` mode, this was
   was done repeatedly, and could cause issues. Fixed in 0.6.18.1
   already.

-  Standalone: Ignore warning given by ``patchelf`` on Linux with at
   least newer OpenSUSE. Fixed in 0.6.18.1 already.

-  Fix, need to avoid computing large values out of ``<<`` operation as
   well. Fixed in 0.6.18.2 already.

   .. code:: python

      # This large value was computed at runtime and then if used, also
      # converted to a string and potentially hashed, taking a long time.
      1 << sys.maxint

-  Standalone: Ignore warning given by ``patchelf`` on Linux about a
   workaround being applied.

-  Fix, calls to ``importlib.import_module`` were not correctly creating
   code for dynamic argument values that need to be released, causing
   the compilation to report the error. Fixed in 0.6.18.1 already.

-  MSYS2: Fix, the console scripts are actually good for it as opposed
   to CPython, and the batch scripts should not be installed. Fixed in
   0.6.18.2 already.

-  Setuptools: Added support older version of ``setuptools`` in meta
   ``build`` integration of Nuitka.

-  Fix, calls to ``importlib.import_module`` with 2 arguments that are
   dynamic, were not working at all. Fixed in 0.6.18.2 already.

-  Windows: Compiling with MinGW64 without ``ccache`` was not working
   due to issues in Scons. Fixed in 0.6.18.2 already.

-  Fix, the ``repr`` built-in was falsely annotated as producing a
   ``str`` value, but it can be also derived or ``unicode`` in Python2.

-  Fix, attribute nodes were not considering the value they are looking
   up on. Now that more values will know to have the attributes, that
   was causing errors. Fixed in 0.6.18.2 already.

-  Fix, left shifting can also produce large values and needs to be
   avoided in that case, similar to what we do for multiplications
   already. Fixed in 0.6.18.2 already.

-  UI: The new option ``--disable-ccache`` didn't really have the
   intended effect. Fixed in 0.6.18.3 already.

-  UI: The progress bar was causing tearing and corrupted outputs, when
   outputs were made, now using proper ``tqdm`` API for doing it, this
   has been solved. Fixed in 0.6.18.4 already.

-  Fix, the constant value ``sys.version_info`` didn't yet have support
   for its type to be also a compile time constant in e.g. tuples. Fixed
   in 0.6.18.4 already.

-  Onefile: Assertions were not disabled, and on Windows with MinGW64
   this lead to including the C filenames of the ``zstd`` inline copy
   files and obviously less optimal code. Fixed in 0.6.18.4 already.

-  Standalone: Added support for ``bottle.ext`` loading extensions to
   resolve at compile time. Fixed in 0.6.18.5 already.

-  Standalone: Added support for ``seedir`` required data file. Fixed in
   0.6.18.5 already.

-  MSYS2: Failed to link when using the static libpython, which is also
   now the default for MSYS2. Fixed in 0.6.18.5 already.

-  Python3.6+: Fix, the intended finalizer of compiled ``asyncgen`` was
   not present and in fact associated to help type. This could have
   caused corruption, but that was also very unlikely. Fixed in 0.6.18.5
   already.

-  Python3: Fix, need to set ``__file__`` before executing modules, as
   some modules, e.g. newer PyWin32 use them to locate things during
   their initialization already.

-  Standalone: Handle all PyWin32 modules that need the special DLLs and
   not just a few.

-  Fix, some ``.pth`` files create module namespaces with ``__path__``
   that does not exist, ignore these in module importing.

-  Python2.6-3.4: Fix, modules with an error could use their module name
   after it was released.

-  Distutils: When providing arguments, the method suggested in the docs
   is not compatible with all other systems, e.g. not
   ``setuptools_rust`` for which a two elemented tuple form needs to be
   used for values. Added support for that and documented its use as
   well in the User Manual.

-  Python3.7+: Do no longer allow deleting cell values, this can lead to
   corruption and should be avoided, it seems unlikely outside of tests
   anyway.

-  Standalone: Added support for more ciphers and hashes with
   ``pycryptodome`` and ``pycryptodomex``, while also only including
   Ciphers when needed.

-  Distutils: Was not including modules or packages only referenced in
   the entry point definition, but not in the list of packages. That is
   not compatible and has been fixed.

-  Fix, must not expose the constants blob from extension modules, as
   loading these into a compiled binary can cause issues in this case.

-  Standalone: Added support for including OpenGL and SSL libraries with
   ``PySide2`` and ``PySide6`` packages.

-  Windows: Fix, the ``cmd`` files created for uninstalled Python and
   accelerated programs to find the Python installation were not passing
   command line arguments.

-  Windows: Executing modules with ``--run`` was not working properly
   due to missing escaping of file paths.

-  Fix, parsing ``.pyi`` files that make relative imports was not
   resolving them correctly.

-  Python3: Fix, when disabling the console on Windows, make sure the
   file handles still work and are not ``None``.

-  Windows: Fix, need to claim all OS versions of Windows as supported,
   otherwise e.g. high DPI features are not available.

New Features
============

-  Programs that are to be executed with the ``-m`` flag, can now be
   compiled with ``--python-flag=-m`` and will then behave in a
   compatible way, i.e. load the containing package first, and have a
   proper ``__package__`` value at run time.

-  We now can write XML reports with information about the compilation.
   This is initially for use in PGO tests, to decide if the expected
   forms of inclusions have happened and should grow into a proper
   reporting tool over time. At this point, the report is not very
   useful yet.

-  Added support for Python 3.10, only ``match`` statements are not
   completely supported. Variations with ``|`` matches that also assign
   are not allowed currently.

-  Windows: Allow using ``--clang`` with ``--mingw64`` to e.g. use the
   ``clang.exe`` that is contained in the Nuitka automatic download
   rather than ``gcc.exe``.

-  Added support for Kivy. Works through a plugin that is automatically
   enabled and needs no other inputs, detecting everything from using
   Kivy at compile time.

-  Added initial support for Haiku OS, a clone of BeOS with a few
   differences in their Python installation.

-  Added experimental plugin ``trio`` that works around issues with that
   package.

Optimization
============

-  Also trust hard imports made on the module level in function level
   code, this unlocks many more static optimization e.g. with
   ``sys.version_info`` when the import and the use are not on the same
   level.

-  For the built-in type method calls with generic implementation, we
   now do faster method descriptor calls. These avoid creating a
   temporary ``PyCFunction`` object, that the normal call slot would,
   this should make these calls faster. Checking them for compiled
   function, etc. was only wasteful, so this makes it more direct.

-  Loop and normal merge traces were keeping assignments made before the
   loop or inside a branch, that was otherwise unused alive. This should
   enable more optimization for code with branches and loops. Also
   unused loop traces are now recognized and removed as well.

-  Avoiding merges of escaped traces with the unescaped trace, there is
   no point in them. This was actually happening a lot and should mean a
   scalability improvement and unlock new optimization as well.

-  Avoid escaping un-init traces. Unset values need not be considered as
   potentially modified as that cannot be done.

-  The ``str`` shape is now detected through variables, this enables
   many optimization on the function level.

-  Added many ``str`` operation nodes.

   These are specifically all methods with no arguments, as these are
   very generic to add, introduced a base class for them, where we know
   they all have no effect or raise, as these functions are all
   guaranteed to succeed and can be served by a common base class.

   This covers the ``str.capitalize``, ``str.upper``, ``str.lower``,
   ``str.swapcase``, ``str.title``, ``str.isalnum``, ``str.isalpha``,
   ``str.isdigit``, ``str.islower``, ``str.isupper``, ``str.isspace``,
   and ``str.istitle`` functions.

   For static optimization ``str.find`` and ``str.rfind`` were added, as
   they are e.g. used in a ``sys.version.find(...)`` style in the ``os``
   module, helping to decide to not consider ``OS/2`` only modules.

   Then, support for ``str.index`` and ``str.rindex`` was added, as
   these are very similar to ``str.find`` forms, only that these may
   raise an exception.

   Also add support for ``str.split`` and ``str.rsplit`` which will be
   used sometimes for code needed to be compile time computed, to e.g.
   detect imports.

   Same goes for ``endswith`` and ``startswith``, the later is e.g.
   popular with ``sys.platform`` checks, and can remove a lot of code
   from compilation with them now being decided at compile time.

   .. note::

      A few ``str`` methods are still missing, with time we will achieve
      all of them, but this will take time.

-  Added trust for ``sys.builtin_module_names`` as well. The ``os``
   module is using it to make platform determinations.

-  When writing constant values, esp. ``tuple``, ``list``, or ``dict``
   values, an encoding of "last value" has been added, avoiding the need
   to repeat the same value again, making many values more compact.

-  When starting Nuitka, it usually restarts itself with information
   collected in a mode without the ``site`` module loaded, and with hash
   randomization disabled, for deterministic behaviour. There is a
   option to prevent this from happening, where the goal is to avoid it,
   e.g. in testing, say for the coverage taking, but that meant to parse
   the options twice, which also loads a lot of code.

   Now only a minimal amount of code is used, and the options are parsed
   only on the restart, and then an error is raised when it notices, it
   was not allowed to do so. This also makes code a lot cleaner.

-  Specialized comparison code for Python2 ``long`` and Python3 ``int``
   code, making these operations much faster to use.

-  Specialized comparison code for Python2 ``unicode`` and Python3
   ``str`` code, making these operations much faster to use, currently
   only ``==`` and ``!=`` are fully accelerated, the other comparisons
   will follow.

-  Enable static libpython with Python3 Debian packages too. As with
   Python2, this will improve the performance of the created binary a
   lot and reduce size for standalone distribution.

-  Comparisons with ``in`` and ``not in`` also consider value traces and
   go through variables as well where possible. So far only the rich
   comparisons and ``is`` and ``is not`` did that.

-  Create fixed import nodes in re-formulations rather than
   ``__import__`` nodes, avoiding later optimization doing that, and of
   course that's simpler code too.

-  Python 3.10: Added support for ``union`` types as compiled time
   constants.

-  Modules are now fully optimized before considering which modules they
   are in turn using, this avoids temporary dependencies, that later
   turn out unused, and can shorten the compilation in some cases by a
   lot of time.

-  On platforms without a static link library, in LTO mode, and with
   gcc, we can use the ``-O3`` mode, which doesn't work for
   ``libpython``, but that's not used there. This also includes fake
   static libpython, as used by MinGW64 and Anaconda on Windows.

-  The ``anti-bloat`` plugin now also handles newer ``sklearn`` and
   knows more about the standard library, and its runners which it will
   exclude from compilation if use for it. Currently that is not the
   default, but it should become that.

Organisational
==============

-  Migrated the Nuitka blog from Nikola to Sphinx based ABlog and made
   the whole site render with Sphinx, making it a lot more usable.

-  Added a small presentation about Nuitka on the Download page, to make
   sure people are aware of core features.

-  The ``gi`` plugin is now always on. The copying of the typelib when
   ``gi`` is imported is harmless and people can disable the plugin if
   that's not needed.

-  The ``matplotlib`` plugin is new and also always on. It previously
   was part of the ``numpy`` plugin, which is doing too many unrelated
   things. Moving this one out is part of a plan to split it up and have
   it on by default without causing issues.

-  MSYS2: Detecting ``MinGW`` and ``POSIX`` flavors of this Python. For
   the ``MinGW`` flavor of MSYS2, the option ``--mingw64`` is now the
   default, before it could attempt to use MSVC, which is not going to
   work for it. And also the Tcl and Tk installations of it are being
   detected automatically for the ``tk-inter`` plugin.

-  Added Windows version to Nuitka version output, so we have this for
   bug reports.

-  User Manual: Added example explaining how to access values from your
   code in Nuitka project options.

-  UI: For Python flavors where we expect a static libpython, the error
   message will now point out how to achieve it for each flavor.

-  UI: Disable progress bar when ``--show-scons`` is used, it makes
   capturing the output from the terminal only harder.

-  UI: Catch error of specifying both ``--msvc=`` and ``--mingw64``
   options.

-  Distutils: Improved error messages when using ``setuptools`` or
   ``build`` integration and failing to provide packages to compile.

-  Plugins: Removed now unused feature to rename modules on import, as
   it was only making the code more complex, while being no more needed
   after recently adding a place for meta path based importers to be
   accounted for.

-  Twitter: Use embedded Tweet in Credits, and regular follow button in
   User Manual.

-  Warnings about imports not done, are now only given when optimization
   can not remove the usage, and no options relatved to following have
   been given.

-  Added Windows version to ``--version`` output of Nuitka. This is to
   more clearly recognize Windows 10 from Windows 11 report, and also
   the odd Windows 7 report, where tool chain will be different.

-  In Visual Code, the default Python used is now 3.9 in the "Linux" C
   configuration. This matches Debian Bullseye.

-  Nicer outputs from check mode of the autoformat as run for CI
   testing, displays problematic files more clearly.

-  Remove broken links to old bug tracker that is no longer online from
   the Changelog.

-  UI: When hitting CTRL-C during initial technical import detection, no
   longer ask to submit a bug report with the exception stack, instead
   exit cleanly.

-  Windows: Enable LTO mode for MinGW64 and other gcc by default. We
   require a version that can do it, so take advantage of that.

-  For cases, where code generation of a module takes long, make sure
   its name is output when CTRL-C is hit.

-  Windows: Splash screen only works with MSVC, added error indicator
   for MinGW64 that states that and asks for porting help.

Cleanups
========

-  Generate all existing C code for generic builtin type method calls
   automatically, and use those for method attribute lookups, making it
   easier to add more.

-  Changed ``TkInter`` module to data file providing interface, yielding
   the 2 directories in question, with a filter for ``demos``.

-  The importing code got a major overhaul and no longer works with
   relative filenames, or filenames combined with package names, and
   module names, but always only with module names and absolute
   filenames. This cleans up some of the oldest and most complex code in
   Nuitka, that had grown to address various requirements discovered
   over time.

-  Major cleanup of Jinja2 template organisation.

   Renamed all C templates from ``.j2`` to ``.c.j2`` for clarity, this
   was not done fully consistent before. Also move all C templates to
   ``nuitka.codegen`` package data, it will be confusing to make a
   difference between ones used during compile time and for the static
   generation, and the lines are going to become blurry.

   Added Jinja2 new macro ``CHECK_OBJECTS`` to avoid branches on
   argument count in the call code templates. More of these things
   should be added.

   Cleanup of code that generates header declarations, there was some
   duplication going on, that made it hard to generate consistent code.

-  Removed ``nuitka.finalizatios.FinalizationBase``, we only have one
   final visitor that does everything, and that of course makes a lot of
   sense for its performance.

-  Major cleanup of the Scons C compiler configuration setup. Moved
   things to the dedicate function, and harmonized it more.

-  Resolved deprecation warnings given by with ``--python-debug`` for
   Nuitka.

Tests
=====

-  Started test suite for Python PGO, not yet completely working though,
   it's not yet doing what is needed though.

-  Added generated test that exercises str methods in multiple
   variations.

-  Revived ``reflected`` test suite, that had been removed, because of
   Nuitka special needs. This one is not yet passing again though, due
   to a few details not yet being as compatible as needed.

-  Added test suite for CPython 3.10 and enable execution of tests with
   this version on Github actions.

Summary
=======

This release is another big step forward.

The amount of optimization added is again very large, some of which yet
again unlocks more static optimization of module imports, that
previously would have to be considered implicit. Now analysing these on
the function level as well, we can start searching for cases, where it
could be done, but is not done yet.

After starting with ``dict``, method optimization has focused on ``str``
which is esp. important for static optimization of imports. The next
goal will here be to cover ``list`` which are important for run time
performance and currently not yet optimized. Future releases will
progress there, and also add more types.

The C type specialization for Python3 has finally progressed, such that
it is also covering the ``long`` and ``unicode`` and as such not limited
to Python2 as much. The focus now needs to turn back to not working with
``PyObject *`` for these types, but e.g. with ``+= 1`` to make it
directly work with ``CLONG`` rather than ``LONG`` for which structural
changes in code generation will be needed.

For scalability, the ``anti-bloat`` work has not yet progressed as much
as to be able to enable it by default. It needs to be more possible to
disable it where it causes problems, e.g. when somebody really wants to
include ``pytest`` and test frameworks generally, that's something that
needs to be doable. Compiling without ``anti-bloat`` plugin is something
that is immediately noticeable in exploding module amounts. It is very
urgently recommended to enable it for your compilations.

The support for Windows has been further refined, actually fixing a few
important issues, esp. for the Qt bindings too.

This release adds support for 3.10 outside of very special ``match``
statements, bringing Nuitka back to where it works great with recent
Python. Unfortunately ``orderedset`` is not available for it yet, which
means it will be slower than 3.9 during compilation.

Overall, Nuitka is closing many open lines of action with this. The
``setuptools`` support has yet again improved and at this point should
be very good.


######################
 Nuitka Release 0.6.18
######################

This release has a focus on new features of all kinds, and then also new
kinds of performance improvements, some of which enable static
optimization of what normally would be dynamic imports, while also
polishing plugins and adding also many new features and a huge amount of
organisational changes.

Bug Fixes
=========

-  Python3.6+: Fixes to asyncgen, need to raise ``StopAsyncInteration``
   rather than ``StopIteration`` in some situations to be fully
   compatible.

-  Onefile: Fix, LTO mode was always enabled for onefile compilation,
   but not all compilers support it yet, e.g. MinGW64 did not. Fixed in
   0.6.17.1 already.

-  Fix, ``type`` calls with 3 arguments didn't annotate their potential
   exception exit. Fixed in 0.6.17.2 already.

-  Fix, trusted module constants were not working properly in all cases.
   Fixed in 0.6.17.2 already.

-  Fix, ``pkg-resources`` exiting with error at compile time for
   unresolved requirements in compiled code, but these can of course
   still be optional, i.e. that code would never run. Instead give only
   a warning, and runtime fail on these. Fixed in 0.6.17.2 already.

-  Standalone: Prevent the inclusion of ``drm`` libraries on Linux, they
   have to come from the target OS at runtime. Fixed in 0.6.17.2
   already.

-  Standalone: Added missing implicit dependency for ``ipcqueue``
   module. Fixed in 0.6.17.3 already.

-  Fix, Qt webengine support for everything but ``PySide2`` wasn't
   working properly. Partially fixed in 0.6.17.3 already.

-  Windows: Fix, bootstrap splash screen code for Windows was missing in
   release packages. Fixed in 0.6.17.3 already.

-  Fix, could crash on known implicit data directories not present.
   Fixed in 0.6.17.3 already.

-  macOS: Disable download of ``ccache`` binary for M1 architecture and
   systems before macOS 10.14 as it doesn't work on these. Fixed in
   0.6.17.3 already.

-  Standalone: The ``pendulum.locals`` handling for Python 3.6 was
   regressed. Fixed in 0.6.17.4 already.

-  Onefile: Make sure the child process is cleaned up even after its
   successful exit. Fixed in 0.6.17.4 already.

-  Standalone: Added support for ``xmlschema``. Fixed in 0.6.17.4
   already.

-  Standalone: Added support for ``curses`` on Windows. Fixed in
   0.6.17.4 already.

-  Standalone: Added support for ``coincurve`` module. Fixed in 0.6.17.5
   already.

-  Python3.4+: Up until Python3.7 inclusive, a workaround for stream
   encoding (was ASCII), causing crashes on output of non-ASCII, other
   Python versions are not affected. Fixed in 0.6.17.5 already.

-  Python2: Workaround for LTO error messages from older gcc versions.
   Fixed in 0.6.17.5 already.

-  Standalone: Added support for ``win32print``. Fixed in 0.6.17.6
   already.

-  Fix, need to prevent usage of static ``libpython`` in module mode or
   else on some Python versions, linker errors can happen. Fixed in
   0.6.17.6 already.

-  Standalone: Do not load ``site`` module early anymore. This might
   have caused issues in some configurations, but really only would be
   needed for loading ``inspect`` which doesn`t depend on it in
   standalone mode. Fixed in 0.6.17.6 already.

-  Fix, could crash with generator expressions in finally blocks of
   tried blocks that return. Fixed in 0.6.17.7 already.

   .. code:: python

      try:
         return 9
      finally:
         "".join(x for x in b"some_iterable")

-  Python3.5+: Compatibility of comparisons with ``types.CoroutineType``
   and ``types.AsyncGeneratorType`` types was not yet implemented. Fixed
   in 0.6.17.7 already.

   .. code:: python

      # These already worked:
      assert isinstance(compiledCoroutine(), types.CoroutineType) is True
      assert isinstance(compiledAsyncgen(), types.AsyncGeneratorType) is True

      # These now work too:
      assert type(compiledCoroutine()) == types.CoroutineType
      assert type(compiledAsyncgen()) == types.AsyncGeneratorType

-  Standalone: Added support for ``ruamel.yaml``. Fixed in 0.6.17.7
   already.

-  Distutils: Fix, when building more than one package, things could go
   wrong. Fixed in 0.6.17.7 already.

-  Fix, for module mode filenames are used, and for packages, you can
   specify a directory, however, a trailing slash was not working. Fixed
   in 0.6.17.7 already.

-  Compatibility: Fix, when locating modules, a package directory and an
   extension module of the same name were not used according to
   priority. Fixed in 0.6.17.7 already.

-  Standalone: Added workaround ``importlib_resources`` insisting on
   Python source files to exist to be able to load datafiles. Fixed in
   0.6.17.7 already.

-  Standalone: Properly detect usage of hard imports from standard
   library in ``--follow-stdlib`` mode.

-  Standalone: Added data files for ``opensapi_spec_validator``.

-  MSYS2: Fix, need to normalize compiler paths before comparing.

-  Anaconda: For accelerated binaries, the created ``.cmd`` file wasn't
   containing all needed environment.

-  macOS: Set minimum OS version derived from the Python executable
   used, this should make it work on all supported platforms (of that
   Python).

-  Standalone: Added support for automatic inclusion of ``xmlschema``
   package datafiles.

-  Standalone: Added support for automatic inclusion of ``eel`` package
   datafiles.

-  Standalone: Added support for ``h5py`` package.

-  Standalone: Added support for ``phonenumbers`` package.

-  Standalone: Added support for ``feedparser`` package, this currently
   depends on the ``anti-bloat`` plugin to be enabled, which will become
   enabled by default in the future.

-  Standalone: Added ``gi`` plugin for said package that copies
   ``typelib`` files and sets the search path for them in standalone
   mode.

-  Standalone: Added necessary datafiles for ``eel`` package.

-  Standalone: Added support for ``QtWebEngine`` to all Qt bindings and
   also make it work on Linux. Before only PySide2 on Windows was
   supported.

-  Python3: Fix, the ``all`` built-in was wrongly assuming that bytes
   values could not be false, but in fact they are if they contain
   ``\0`` which is actually false. The same does not happen for string
   values, but that's a difference to be considered.

-  Windows: The LTO was supposed to be used automatically on with MSVC
   14.2 or higher, but that was regressed and has been repaired now.

-  Standalone: Extension modules contained in packages, depending on
   their mode of loading had the ``__package__`` value set to a wrong
   value, which at least impacted new matplotlib detection of Qt
   backend.

-  Windows: The ``python setup.py install`` was installing binaries for
   no good reason.

New Features
============

-  Setuptools support. Documented ``bdist_nuitka`` and ``bdist_wheel``
   integration and added support for Nuitka as a ``build`` package
   backend in ``pyproject.toml`` files. Using Nuitka to build your
   wheels is supposed to be easy now.

-  Added experimental support for Python 3.10, there are however still
   important issues with compatibility with the CPython 3.9 test suite
   with at least asyncgen and coroutines.

-  macOS: For app bundles, version information can be provided with the
   new option ``--macos-app-version``.

-  Added Python vendor detection of ``Anaconda``, ``pyenv``, ``Apple
   Python``, and ``pyenv`` and output the result in version output, this
   should make it easiert to analyse reported issues.

-  Plugins: Also handle the usage of ``__name__`` for metadata version
   resolution of the ``pkg-resources`` standard plugin.

-  Plugins: The ``data-files`` standard plugin now reads configuration
   from a Yaml file that ``data-files.yml`` making it more accessible
   for contributions.

-  Windows: Allow enforcing usage of MSVC with ``--msvc=latest``. This
   allows you to prevent accidental usage of MinGW64 on Windows, when
   MSVC is intended, but achieves that without fixing the version to
   use.

-  Windows: Added support for LTO with MinGW64 on Windows, this was
   previously limited to the MSVC compiler only.

-  Windows: Added support for using ``--debugger`` with the downloaded
   MinGW64 provided ``gdb.exe``.

   .. note::

      It doesn`t work when executed from a Git bash prompt, but e.g.
      from a standard command prompt.

-  Added new experimental flag for compiled types to inherit from
   uncompiled types. This should allow easier and more complete
   compatibility, making even code in extension modules that uses
   ``PyObject_IsInstance`` work, providing support for packages like
   ``pydanctic``.

-  Plugins: The Qt binding plugins now resolve ``pyqtgraph`` selection
   of binding by hard coding ``QT_LIB``. This will allow to resolve its
   own dynamic imports depending on that variable at compile time. At
   this time, the compile time analysis is not covering all cases yet,
   but we hope to get there.

-  macOS: Provide ``minOS`` for standalone builds, derived from the
   setting of the Python used to create it.

-  UI: Added new option ``--disable-ccache`` to prevent Nuitka from
   injecting ``ccache`` (Clang, gcc) and ``clcache`` (MSVC) for caching
   the C results of the compilation.

-  Plugins: Added experimental support for ``PyQt6``. While using
   ``PySide2`` or ``PySide6`` is very much recommended with Nuitka, this
   allows its use.

-  UI: Added option ``--low-memory`` to allow the user to specify that
   the compilation should attempt to use less memory where possible,
   this increases compile times, but might enable compilation on some
   weaker machines.

Optimization
============

-  Added dedicated attribute nodes for attribute values that match names
   of dictionary operations. These are optimized into dedicate nodes for
   methods of dictionaries should their expression have an exact
   dictionary shape. These in turn optimize calls on them statically
   into dictionary operations. This is done for all methods of ``dict``
   for both Python2 and Python3, namely ``get``, ``items``,
   ``iteritems``, ``itervalues``, ``iterkeys``, ``viewvalues``,
   ``viewkeys``, ``pop``, ``setdefault``, ``has_key``, ``clear``,
   ``copy``, ``update``.

   The new operation nodes also add compile time optimization for being
   used on constant values where possible.

-  Also added dedicated attribute nodes for string operations. For
   operations, currently only part of the methods are done. These are
   currently only ``join``, ``strip``, ``lstrip``, ``rstrip``,
   ``partition``, ``rpartition``. Besides performance, this subset was
   enough to cover compile time evaluation of module name computation
   for ``importlib.import_module`` as done by SWIG bindings, allowing
   these implicit dependencies to be discovered at compile time without
   any help, marking a significant improvement for standalone usage.

-  Annotate type shape for dictionary ``in``/``not in`` nodes, this was
   missing unlike in the generic ``in``/``not in`` nodes.

-  Faster processing of "expression only" statement nodes. These are
   nodes, where a value is computed, but then not used, it still needs
   to be accounted for though, representing the value release.

   .. code:: python

      something() # ignores return value, means statement only node

-  Windows: Enabled LTO by default with MinGW64, which makes it produce
   much faster results. It now yield faster binaries than MSVC 2019 with
   pystone.

-  Windows: Added support for C level PGO (Profile Guided Optimization)
   with MSVC and MinGW64, allowing extra speed boosts from the C
   compilation on Windows as well.

-  Standalone: Better handling of ``requests.packages`` and
   ``six.moves``. The old handling could duplicate their code. Now uses
   a new mechanism to resolve metapath based importer effects at compile
   time.

-  Avoid useless exception checks in our dictionary helpers, as these
   could only occur when working with dictionary overloads, which we
   know to not be the case.

-  For nodes, have dedicated child mixin classes for nodes with a single
   child value and for nodes with a tuple of children, so that these
   common kind of nodes operate faster and don't have to check at
   runtime what type they are during access.

-  Actually make use of the egg cache. Nuitka was unpacking eggs in
   every compilation, but in wheel installs, these can be quite common
   and should be faster.

-  Star arguments annotated their type shape, but the methods to check
   for dictionary exactly were not affected by this preventing
   optimization in some cases.

-  Added ``anti-bloat`` configuration for main programs present in the
   modules of the standard library, these can be removed from the
   compilation and should lower dependencies detected.

-  Using static libpython with ``pyenv`` automatically. This should give
   both smaller (standalone mode) and faster results as is the case when
   using this feature..

-  Plugins: Added improvements to the ``anti-bloat`` plugin for
   ``gevent`` to avoid including its testing framework.

-  Python3.9+: Faster calls into uncompiled functions from compiled code
   using newly introduced API of that version.

-  Statically optimize ``importlib.import_module`` calls with constant
   args into fixed name imports.

-  Added support for ``sys.version_info`` to be used as a compile time
   constant. This should enable many checks to be done at compile time.

-  Added hard import and static optimization for
   ``typing.TYPE_CHECKING``.

-  Also compute named import lookup through variables, expanding their
   use to more cases, e.g. like this:

   .. code::

      import sys
      ...
      if sys.version_info.major >= 3:
         ...

-  Also optimize compile time comparisons through variable names if
   possible, i.e. the value cannot have changed.

-  Faster calls of uncompiled code with Python3.9 or higher avoiding DLL
   call overhead.

Organisational
==============

-  Commercial: There are ``Buy Now`` buttons available now for the
   direct purchase of the `Nuitka Commercial </pages/commercial.html>`__
   offering. Finally Credit Card, Google Pay, and Apple Pay are all
   possible. This is using Stripe. Get in touch with me if you want to
   use bank transfer, which is of course still best for me.

-  The main script runners for Python2 have been renamed to ``nuitka2``
   and ``nuitka2-run``, which is consistent with what we do for Python3,
   and avoids issues where ``bin`` folder ends up in ``sys.path`` and
   prevents the loading of ``nuitka`` package.

-  Windows: Added support for Visual Studio 2022 by updating the inline
   copy of Scons used for Windows to version 4.3.0, on non Windows, the
   other ones will keep being used.

-  Windows: Requiring latest MinGW64 with version 11.2 as released by
   winlibs, because this is known to allow LTO, where previous releases
   were missing needed binaries.

-  Reject standalone mode usage with Apple Python, as it works only with
   the other supported Pythons, avoiding pitfalls in attempting to
   distribute it.

-  Move hosting of documentation to Sphinx, added Changelog and some
   early parts of API documentation there too. This gives much more
   readable results than what we have done so far with Nikola. More
   things will move there.

-  User Manual: Add description how to access code attributes in
   ``nuitka-project`` style options.

-  User Manual: Added commands used to generate performance numbers for
   Python.

-  User Manual: List other Python's for which static linking is supposed
   to work.

-  Improved help for ``--include-package`` with a hint how to exclude
   some of the subpackages.

-  Started using Jinja2 in code templates with a few types, adding basic
   infrastructure to do that. This will be expanded in the future.

-  Updated plugin documentation with more recent information.

-  Added Python flavor as detected to the ``--version`` output for
   improved bug reports.

-  Linux: Added distribution name to ``--version`` output for improved
   bug reports.

-  Always enable the ``gevent`` plugin, we want to achieve this for all
   plugins, and this is only a step in that direction.

-  Added project URLs for PyPI, so people looking at it from there have
   some immediate places to checkout.

-  Debian: Use common code for included PDF files, which have page
   styles and automatic corrections for ``rst2pdf`` applied.

-  Updated to latest ``black``, ``isort``, ``pylint`` versions.

-  The binary names for Python2 changed from ``nuitka`` and
   ``nuitka-run`` to ``nuitka2`` and ``nuitka2-run``. This harmonizes it
   with Python2 and avoids issues, where the ``bin`` folder in
   ``sys.path`` can cause issues with re-execution of Nuitka finding
   those to import.

   .. note::

      You ought to be using ``python -m nuitka`` style of calling Nuitka
      anyway, as it gives you best control over what Python is used to
      run Nuitka, you can pick ``python2`` there if you want it to run
      with that, even with full path. Check the relevant section in the
      User Manual too.

-  Added support for Fedora 34 and Fedora 35.

Cleanups
========

-  In a change of mind ``--enable-plugin`` has become the only form to
   enable a plugin used in documentation and tests.

-  Massive cleanup of ``numpy`` and Qt binding plugins, e.g.
   ``pyside2``. Data files and DLLs are now provided through proper
   declarative objects rather than copied manually. The handling of
   PyQt5 from the plugin should have improved as a side effect.

-  Massive cleanups of all documentation in ReST format. Plenty of
   formatting errors were resolved. Many typos were identified and
   globally fixed. Spellings e.g. of "Developer Manual" are now enforced
   with automatic replacements. Also missing or wrong quotes were turned
   to proper methods. Also enforce code language for shell scripts to be
   the same everywhere.

-  Removed last usages of ``getPythonFlags()`` and made the function
   private, replacing their use with dedicated function to check for
   individual flags.

-  Avoid string comparison with ``nuitka.utils.getOS()`` and instead add
   accessors that are more readable, e.g. ``nuitka.utils.isMacOS()`` and
   put them to use where it makes sense.

-  Replaced usages of string tests in list of python flags specified,
   with functions that check for a specific name with a speaking
   function name.

-  Added mixin for expressions that have no side effect outside of their
   value, providing common method implementation more consistently.

-  Remove code geared to using old PyLint and on Python2, we no longer
   use that. Also removed annotations only used for overriding Python2
   builtins from Nuitka code.

-  The PDF specific annotations were moved into being applied only in
   the PDF building step, avoiding errors for raw PDF directives.

-  Apply Visual Code autoformat to our Yaml files. This is unfortunately
   not and automatic formatting yet.

-  Introduce dedicated ``nuitka.utils.Json`` module, as we intend to
   expand its usage, e.g. for caching.

-  Replacing remaining usages of ``print`` functions with uses of
   ``nuitka.Tracing`` instead.

-  Massive cleanup of the ``gevent`` plugin, user proper method to
   execute code after module load, rather than source patching without
   need. The plugin no longer messes with inclusions that other code
   already provides for standalone.

-  Using own helper to update ``sys`` module attributes, to avoid errors
   from old C compilers, and also cleaning up using code to not have to
   cast on string constants.

-  More consistent naming of plugin classes, and enforce a relationship
   of detector class names to the names of detected plugins. The new
   naming consistency is now enforced.

Tests
=====

-  Added CPython 3.10 test suite, it needs more work though.

-  Added generated test that exercises dictionary methods in multiple
   variations.

-  Test suite names were specified wrongly in a few of them.

Summary
=======

This release is again a huge step forward. It refines on PGO and LTO for
C level to work with all relevant compilers. Internally Python level PGO
is prepared, but only a future release will feature it. With that,
scalability improvements as well as even more performance improvements
will be unlocked.

The amount of optimization added this time is even bigger, some of which
unlocks static optimization of module imports, that previously would
have to be considered implicit. This work will need one extra step,
namely to also trace hard imports on the function level, then this will
be an extremely powerful tool to solve these kinds of issues in the
future. The next release will have this and go even further in this
area.

With the dictionary methods, and some string methods, also a whole new
kind of optimization has been started. These will make working with
``dict`` containers faster, but obviously a lot of ground is to cover
there still, e.g. ``list`` values are a natural target not yet started.
Future releases will progress here.

Type specialization for Python3 has not progressed though, and will have
to be featured in a future releases though.

For scalability, the ``anti-bloat`` work has continued, and this should
be the last release, where this is not on by default. Compiling without
it is something that is immediately noticeable in exploding module
amounts. It is very urgently recommended to enable it for your
compilations.

The support for macOS has been refined, with version information being
possible to add, and adding information to the binary about which OSes
are supported, as well as rejecting Apple Python, which is only a trap
if you want to deploy to other OS versions. More work will be needed to
support ``pyenv`` or even Homebrew there too, for now CPython is still
the recommended platform to use.

This release achieves major compatibility improvements. And of course,
the experimental support for 3.10 is not the least. The next release
will strive to complete the support for it fully, but this should be
usable at least, for now please stay on 3.9 if you can.


##############
Older Releases
##############

These are older releases of Nuitka.

Nuitka Release 0.6.17
=====================

This release has a focus on performance improvements, while also
polishing plugins and adding many new features.

Bug Fixes
---------

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

New Features
------------

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

Optimization
------------

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

Organisational
--------------

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

Cleanups
--------

-  Encoding names for UTF8 in calls to ``.encode()`` were used
   inconsistent with and without dashes in the source code, added
   cleanup to autoformat that picks the one blessed.

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

-  Enhanced autoformat for rest documents, bullet list spacing is now
   consistent and spelling of organisational is unified automatically.

-  Moved icon conversion functionality to separate module, so it can be
   reused for other platforms more easily.

Tests
-----

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

Summary
-------

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


Nuitka Release 0.6.16
=====================

This release is mostly polishing and new features. Optimization looked
only at threading performance, and LTO improvements on Windows.

Bug Fixes
---------

-  Fix, the ``pkg-resources`` failed to resolve versions for
   ``importlib.metadata`` from its standard library at compile time.
   Fixed in 0.6.15.1 already.

-  Standalone: Fix, ``--include-module`` was not including the module if
   it was an extension modules, but only for Python modules. Fixed in
   0.6.15.1 already.

-  Standalone: Added missing implicit dependencies for ``gi.overrides``.
   Fixed in 0.6.15.1 already.

-  Python3.9: Fix, could crash when using generic aliases in certain
   configurations. Fixed in 0.6.15.2 already.

-  Fix, the tensorflow plugin needed an update due to changed API. Fixed
   in 0.6.15.3 already.

-  When error exiting Nuitka, it now closes any open progress bar for
   cleaner display.

-  Standalone: Added missing dependency for ``skimage``.

-  Standalone: The ``numpy`` plugin now automatically includes Qt
   backend if any of the Qt binding plugins is active.

New Features
------------

-  Pyton3.5+: Added support for onefile compression. This is using
   ``zstd`` which is known to give very good compression with very high
   decompression, much better than e.g. ``zlib``.

-  macOS: Added onefile support.

-  FreeBSD: Added onefile support.

-  Linux: Added method to use tempdir onefile support as used on other
   platforms as an alternative to ``AppImage`` based.

-  Added support for recursive addition of files from directories with
   patterns.

-  Attaching the payload to onefile now has a progress bar too.

-  Windows: Prelimary support for the yet unfinished Nuitka-Python that
   allows static linking and higher performance on Windows, esp. with
   Nuitka.

-  Windows: In acceleration mode, for uninstalled Python, now a CMD file
   is created rather than copying the DLL to the binary directory. That
   avoids conflicts with architectures and of course useless file
   copies.

-  New abilities for plugin ``anti-bloat`` allow to make it an error
   when certain modules are imported. Added more specific options for
   usual trouble makes, esp. ``setuptools``, ``pytest`` are causing an
   explosion for some programs, while being unused code. This makes it
   now easier to oversee this.

-  It's now possible to override ``appdirs`` decision for where cache
   files live with an environment variable ``NUITKA_CACHE_DIR``.

-  The ``-o`` option now also works with onefile mode, it previously
   rejected anything but acceleration mode. Fixed in 0.6.15.3 already.

-  Plugins: It's now possible for multiple plugins to provide pre or
   post load code for the same module.

-  Added indications for compilation modes ``standalone`` and
   ``onefile`` to the ``__compiled__`` attribute.

-  Plugins: Give nicer error message in case of colliding command line
   options.

Optimization
------------

-  Faster threading code is now using for Python3.8 or higher and not
   only 3.9, giving a performance boost, esp. on Windows.

-  Using ``--lto`` is now the default with MSVC 2019 or higher. This
   will given smaller and faster binaries. It has been available for
   some time, but not been the default yet.

Cleanups
--------

-  Using different progress bar titles for C compilation of Python code
   and C compilation of onefile bootstrap.

-  Moved platform specific detections, for FreeBSD/OpenBSD/macOS out of
   the Scons file and to common Nuitka code, sometimes eliminating
   duplications with one version being more correct than the other.

-  Massive cleanup of datafile plugin, using pattern descriptions, so
   more code duplication can be removed.

-  More cleanup of the scons files, sharing more common code.

Organisational
--------------

-  Under the name Nuitka-Python we are now also developing a fork of
   CPython with enhancements, you can follow and joint it at
   https://github.com/Nuitka/Nuitka-Python but at this time it is not
   yet ready for prime time.

-  Onefile under Windows now only is temporary file mode. Until we
   figure out how to solve the problems with locking and caching, the
   mode where it installs to the AppData of the user is no longer
   available.

-  Renamed the plugin responsible for PyQt5 support to match the names
   of others. Note however, that at this time, PySide2 or PySide6 are to
   be recommended.

-  Make it clear that PySide 6.1.2 is actually going to be the supported
   version of PySide6.

-  Use MSVC in Github actions.

Summary
-------

This release had a massive focus on expanding existing features, esp.
for onefile, and plugins API, such that we can now configure
``anti-bloat`` with yaml, have really nice datafile handling options,
and have onefile on all OSes practically.


Nuitka Release 0.6.15
=====================

This release polished previous work with bug fixes, but there are also
important new things that help make Nuitka more usable, with one
important performance improvement.

Bug Fixes
---------

-  Fix, hard imports were not automatically used in code generation
   leading to errors when used. Fixed in 0.6.14.2 already.

-  Windows: Fix, ``clcache`` was disabled by mistake. Fixed in 0.6.14.2
   already.

-  Standalone: Added data files for ``jsonschema`` to be copied
   automatically.

-  Standalone: Support for ``pendulum`` wasn't working anymore with the
   last release due to plugin interface issues.

-  Retry downloads without SSL if that fails, as some Python do not have
   working SSL. Fixed in 0.6.14.5 already.

-  Fix, the ``ccache`` path wasn't working if it contained spaces. Fixed
   in 0.6.14.5 already.

-  Onefile: For Linux and ARM using proper download off appimage. Fixed
   in 0.6.14.5 already.

-  Standalone: Added support for ``pyreadstat``. Fixed in 0.6.14.5
   already.

-  Standalone: Added missing dependencies for ``pandas``. Fixed in
   0.6.14.6 already.

-  Standalone: Some preloaded packages from ``.pth`` do not have a
   ``__path__``, these can and must be ignored.

-  Onefile: On Linux, the ``sys.argv[0]`` was not the original file as
   advertised.

-  Standalone: Do not consider ``.mesh`` and ``.frag`` files as DLls in
   the Qt bindings when including the qml support. This was causing
   errors on Linux, but was generally wasteful.

-  Fix, project options could be injected twice, which could lead to
   errors with options that were only allowed once, e.g.
   ``--linux-onefile-icon``.

-  Windows: When updating the resources in created binaries, treat all
   kinds of ``OSError`` with information output.

-  Onefile: Remove onefile target binary path at startup as well, so it
   cannot cause confusion after error exit.

-  Onefile: In case of error exit from ``AppImage``, preserve its
   outputs and attempt to detect if there was a locking issue.

-  Standalone: Scan package folders on Linux for DLLs too. This is
   necessary to properly handle ``PyQt5`` in case of Qt installed in the
   system as well.

-  Standalone: On Linux, standard QML files were not found.

-  Standalone: Enforce C locale when detecting DLLs on Linux, otherwise
   whitelisting messages didn't work properly on newer Linux.

-  Standalone: Added support for ``tzdata`` package data files.

-  Standalone: Added support for ``exchangelib``.

-  Python3.9: Fix, type subscripts could cause optimization errors.

-  UI: Project options didn't properly handle quoting of arguments,
   these are normally removed by the shell.

-  Linux: The default icon for Python in the system is now found with
   more version specific names and should work on more systems.

-  Standalone: Do not include ``libstdc++`` as it should come from the
   system rather.

New Features
------------

-  Added plugin ``anti-bloat`` plugin, intended to fight bloat. For now
   it can make including certain modules an error, a warning, or force
   ``ImportError``, e.g. ``--noinclude-setuptools-mode=nofollow`` is
   very much recommended to limit compilation size.

-  The ``pkg-resources`` builtin now covers ``metadata`` and
   importlib_metadata packages for compile time version resolution as
   well.

-  Added support for ``PySide2`` on Python version before 3.6, because
   the patched code needs no workarounds. Fixed in 0.6.14.3 already.

-  Windows: Convert images to icon files on the fly. So now you can
   specify multiple PNG files, and Nuitka will create an icon out of
   that automatically.

-  macOS: Automatically download ``ccache`` binary if not present.

-  Plugins: New interface to query the main script path. This allows
   plugins to look at its directory.

-  UI: Output the versions of Nuitka and Python during compilation.

-  UI: Added option to control static linking. So far this had been
   enabled only automatically for cases where we are certain, but this
   allows to force enable or disable it. Now an info is given, if Nuitka
   thinks it might be possible to enable it, but doesn't do it
   automatically.

-  UI: Added ``--no-onefile`` to disable ``--onefile`` from project
   options.

Optimization
------------

-  Much enhanced GIL interaction with Python3.9 giving a big speed boost
   and better threading behaviour.

-  Faster conversion of iterables to ``list``, if size can be know,
   allocation ahead saves a lot of effort.

-  Added support for ``GenericAlias`` objects as compile time constants.

Organisational
--------------

-  Enhanced Github issue raising instructions.

-  Apply ``rstfmt`` to all documentation and make it part of the commit
   hook.

-  Make sure to check Scons files as well. This would have caught the
   code used to disable ``clcache`` temporarily.

-  Do not mention Travis in PR template anymore, we have stopped using
   it.

-  Updated requirements to latest versions.

-  Bump requirements for development to 3.7 at least, toosl like black
   do not work with 3.6 anymore.

-  Started work on Nuitka Python, a CPython fork intended for enhanced
   performance and standalone support with Nuitka.

Cleanups
--------

-  Determine system prefix without virtualenv outside of Scons, such
   that plugins can share the code. There was duplication with the
   ``numpy`` plugin, and this will only be more complete using all
   approaches. This also removes a lot of noise from the scons file
   moving it to shared code.

-  The Qt plugins now collect QML files with cleaner code.

Tests
-----

-  Nicer error message if a wrong search mode is given.

-  Windows: Added timeout for determining run time traces with
   dependency walker, sometimes this hangs.

-  Added test to cover the zip importer.

-  Making use of project options in onefile tests, making it easier to
   execute them manually.

Summary
-------

For Windows, it's now easier than ever to create an icon for your
deployment, because you can use PNG files, and need not produce ICO
files anymore, with Nuitka doing that for you.

The onefile for Linux had some more or less severe problems that got
addressed, esp. also when it came to QML applications with PySide.

On the side, we are preparing to greatly improve the caching of Nuitka,
starting with retaining modules that were demoted to bytecode. There are
changes in this release, to support that, but it's not yet complete. We
expect that scalability will then be possible to improve even further.

Generally this is mostly a maintenance release, which outside of the
threading performance improvement has very little to offer for faster
execution, but that actually does a lot. Unfortunately right now it's
limited to 3.9, but some of the newer Python's will also be supported in
later releases.


Nuitka Release 0.6.14
=====================

This release has few, but important bug fixes. The main focus was on
expanding standalone support, esp. for PySide2, but also and in general
with plugins added that workaround ``pkg_resources`` usage for version
information.

Also an important new features was added, e.g. the project configuration
in the main file should prove to be very useful.

Bug Fixes
---------

-  Compatibility: Fix, modules that failed to import, should be retried
   on next import.

   So far we only ever executed the module body once, but that is not
   how it's supposed to be. Instead, only if it's in ``sys.modules``
   that should happen, which is the case after successful import.

-  Compatibility: Fix, constant ``False`` values in right hand side of
   ``and``/``or`` conditions were generating wrong code if the left side
   was of known ``bool`` shape too.

-  Standalone: Fix, add ``styles`` Qt plugins to list of sensible
   plugins.

   Otherwise no mouse hover events are generated on some platforms.

-  Compatibility: Fix, relative ``from`` imports beyond level 1 were not
   loadingg modules from packages if necessary. Fixed in 0.6.13.3
   already.

-  Standalone: The ``crypto`` DLL check for Qt bindings was wrong. Fixed
   in 0.6.13.2 already.

-  Standalone: Added experimental support for PySide6, but for good
   results, 6.1 will be needed.

-  Standalone: Added support for newer matplotlib. Fixed in 0.6.12.1
   already.

-  Standalone: Reverted changes related to ``pkg_resources`` that were
   causing regressions. Fixed in 0.6.13.1 already.

-  Standalone: Adding missing implicit dependency for ``cytoolz``
   package. Fixed in 0.6.13.1 already.

-  Standalone: Matching for package names to not suggest recompile for
   was broken and didn't match. Fixed in 0.6.13.1 already.

New Features
------------

-  Added support for project options.

   When found in the filename provided, Nuitka will inject options to
   the commandline, such that it becomes possible to do a complex
   project with only using

   .. code:: bash

      python -m nuitka filename.py

   .. code:: python

      # Compilation mode, support OS specific.
      # nuitka-project-if: {OS} in ("Windows", "Linux"):
      #    nuitka-project: --onefile
      # nuitka-project-if: {OS} not in ("Windows", "Linux"):
      #    nuitka-project: --standalone

      # The PySide2 plugin covers qt-plugins
      # nuitka-project: --enable-plugin=pyside2
      # nuitka-project: --include-qt-plugins=sensible,qml

      # The pkg-resources plugin is not yet automatic
      # nuitka-project: --enable-plugin=pkg-resources

      # Nuitka Commercial only features follow:

      # Protect the constants from being readable.
      # nuitka-project: --enable-plugin=data-hiding

      # Include datafiles for Qt into the binary directory.
      # nuitka-project: --enable-plugin=datafile-inclusion
      # nuitka-project: --qt-datadir={MAIN_DIRECTORY}
      # nuitka-project: --qt-datafile-pattern=*.js
      # nuitka-project: --qt-datafile-pattern=*.qml
      # nuitka-project: --qt-datafile-pattern=*.svg
      # nuitka-project: --qt-datafile-pattern=*.png

   Refer to the User Manual for a table of directives and the variables
   allowed to be used.

-  Added option to include whole data directory structures in
   standalone.

   The new option ``--include-data-dir`` was added and is mostly
   required for onefile mode, but recommended for standalone too.

-  Added ``pkg-resources`` plugin.

   This one can resolve code like this at compile time without any need
   for pip metadata to be present or used.

   .. code:: python

      pkg_resources.get_distribution("module_name").version
      pkg_resources.get_distribution("module_name").parsed_version

-  Standalone: Also process early imports in optimization.

   Otherwise plugins cannot work on standard library modules. This makes
   it possible to handle them as well.

Optimization
------------

-  Faster binary operations.

   Applying lessons learnt during the enhancements for in-place
   operations that initially gave worse results than some manual code,
   we apply the same tricks for all binary operations, which speeds them
   up by significant margins, e.g. 30% for float addition, 25% for
   Python int addition, and still 6% for Python int addition.

-  More direct optimization of unary operations on constant value.

   Without this, ``-1`` was not directly a constant value, but had to go
   through the unary ``-`` operation, which it still does, but now it's
   done at tree building time.

-  More direct optimization for ``not`` in branches.

   Invertible comparisons, i.e. ``is``/``is not`` and ``in``/``not in``
   do not have do be done during optimization. This mainly avoids noise
   during optimization from such unimportant steps.

-  More direct optimization for constant slices.

   These are used in Python3 for all subscripts, e.g. ``a[1:2]`` will
   use ``slice(1,2)`` effectively. For Python2 they are used less often,
   but still. This also avoids a lot of noise during optimization,
   mostly on Python3

-  Scons: Avoid writing database to disk entirely.

   This saves a bit of disk churn and makes it unnecessary to specify
   the location such that it doesn't collide between Python versions.

-  For optimization passes, use previous max total as minimum for next
   pass. That will usually be a more accurate result, rather than
   starting from 1 again. Part of 0.6.13.1 already.

-  Enhancements to the branch merging improve the scalability of Nuitka
   somewhat, although the merging itself is still not very scalable,
   there are some modules that are very slow to optimize still.

-  Use ``orderset`` if available over the inline copy for ``OrderedSet``
   which is much faster and improves Nuitka compile times.

-  Make ``pkgutil`` a hard import too, this is in preparation of more
   optimization for its functions.

Organisational
--------------

-  Upstream patches for ``PySide6`` have been contributed and merged
   into the development branch ``dev``. Full support should be available
   once this is released as part of 6.1 which is waiting for Qt 6.1
   naturally.

-  Patches for ``PySide2`` are available to commercial customers, see
   `PySide2 support <https://nuitka.net/pages/pyside2.html>`__ page.

-  Formatted all documents with ``rstfmt`` and made that part of the
   commit hook for Nuitka. It now works for all documents we have.

-  Updated inline copy of ``tqdm`` to 4.59.0 which ought to address
   spurious errors given.

-  User Manual: Remove ``--show-progress`` from the tutoral. The default
   progress bar is then disabled, and is actually much nicer to use.

-  Developer Manual: Added description of how context managers should be
   named.

-  Cleanup language for some warnings and outputs.

   It was still using obsolete "recursion" language rather than talking
   about "following imports", which is the new one.

Cleanups
--------

-  Remove dead code related to constants marshal, the data composer has
   replaced this.

-  Avoid internal API usage for loading extension modules on Linux,
   there is a function in ``sys`` module to get the ld flags.

Tests
-----

-  Fix, the ``only`` mode wasn't working properly.

-  Use new project options feature for specific options in basic tests
   allowing to remove them from the test runner.

Summary
-------

For PySide2 things became more perfect, but it takes upstream patches
unfortunately such that only PySide6.1 will be working out of the box
outside of the commercial offering. We will also attempt to provide
workarounds, but there are some things that cannot be done that way.

This release added some more scalability to the optimization process,
however there will be more work needed to make efficient branch merges.

For onefile, a feature to include whole directories had been missing,
and could not easily be achieved with the existing options. This further
rounds this up, now what's considered missing is compression and macOS
support, both of which should be coming in a future release.

For the performance side of things, the binary operator work can
actually yield pretty good gains, with double digit improvements, but
this covers only so much. Much more C types and better type tracing
would be needed, but there was no progress on this front. Future
releases will have to revisit the type tracing to make sure, we know
more about loop variables, etc. so we can achieve the near C speed we
are looking for, at least in the field of ``int`` performance.

This release has largely been driven by the `Nuitka Commercial
</doc/commercial.html>`__ offering and needs for compatibility with more
code, which is of course always a good thing.


Nuitka Release 0.6.13
=====================

This release follows up with yet again massive improvement in many ways
with lots of bug fixes and new features.

Bug Fixes
---------

-  Windows: Icon group entries were not still not working properly in
   some cases, leading to no icon or too small icons being displayed.
   Fixed in 0.6.12.2 already.

-  Windows: Icons and version information were copied from the
   standalone executable to the onefile executable, but that failed due
   to race situations, sometimes reproducible. Instead we now apply
   things to both independently. Fixed in 0.6.12.2 already.

-  Standalone: Fixup scanning for DLLs with ``ldconfig`` on Linux and
   newer versions making unexpected outputs. Fixed in 0.6.12.2 already.

-  UI: When there is no standard input provided, prompts were crashing
   with ``EOFError`` when ``--assume-yes-for-downloads`` is not given,
   change that to defaulting to ``"no"`` instead. Fixed in 0.6.12.2
   already.

-  Windows: Detect empty strings for company name, product name, product
   and file versions rather than crashing on them later. Them being
   empty rather than not there can cause a lot of issues in other
   places. Fixed in 0.6.12.2 already.

-  Scons: Pass on exceptions during execution in worker threads and
   abort compilation immediately. Fixed in 0.6.12.2 already.

-  Python3.9: Still not fully compatible with typing subclasses, the
   enhanced check is now closely matching the CPython code. Fixed in
   0.6.12.2 already.

-  Linux: Nicer error message for missing ``libfuse`` requirement.

-  Compatibility: Lookups on dictionaries with ``None`` value giving a
   ``KeyError`` exception, but with no value, which is not what CPython
   does.

-  Python3.9: Fix, future annotations were crashing in debug mode. Fixed
   in 0.6.12.3 already.

-  Standalone: Corrections to the ``glfw`` were made. Fixed in 0.6.12.3
   already.

-  Standalone: Added missing ìmplicit dependency for ``py.test``. Fixed
   in 0.6.12.3 already.

-  Standalone: Adding missing implicit dependency for ``pyreadstat``.

-  Windows: Added workaround for common clcache locking problems. Since
   we use it only inside a single Scons process, we can avoiding using
   Windows mutexes, and use a process level lock instead.

-  Plugins: Fix plugin for support for ``eventlet``. Fixed in 0.6.12.3
   already.

-  Standalone: Added support for latest ``zmq`` on Windows.

-  Scons: the ``--quiet`` flag was not fully honored yet, with Scons
   still making a few outputs.

-  Standalone: Added support for alternative DLL name for newer
   ``PyGTK3`` on Windows. Fixed in 0.6.12.4 already.

-  Plugins: Fix plugin for support for ``gevent``. Fixed in 0.6.12.4
   already.

-  Standalone: Added yet another missing implicit dependency for
   ``pandas``.

-  Plugins: Fix, the ``qt-plugins`` plugin could stumble over ``.mesh``
   files.

-  Windows: Fix, dependency walker wasn't properly working with unicode
   ``%PATH%`` which could e.g. happen with a virtualenv in a home
   directory that requires them.

-  Python3: Fixed a few Python debug mode warnings about unclosed files
   that have sneaked into the codebase.

New Features
------------

-  Added new options ``--windows-force-stdout-spec`` and
   ``--windows-force-stderr-spec`` to force output to files. The paths
   provided at compile time can resolve symbolic paths, and are intended
   to e.g. place these files near the executable. Check the User Manual
   for a table of the currently supported values. At this time, the
   feature is limited to Windows, where the need arose first, but it
   will be ported to other supported OSes eventually. These are most
   useful for programs run as ``--windows-disable-console`` or with
   ``--enable-plugin=windows-service``.

-  Windows: Added option ``--windows-onefile-tempdir-spec`` to provide
   the temporary directory used with ``--windows-onefile-tempdir`` in
   onefile mode, you can now select your own pattern, and e.g. hardcode
   a base directory of your choice rather than ``%TEMP``.

-  Added experimental support for ``PySide2`` with workarounds for
   compiled methods not being accepted by its core. There are known
   issues with ``PySide2`` still, but it's working fine for some people
   now. Upstream patches will have to be created to remove the need for
   workarounds and full support.

Optimization
------------

-  Use binary operation code for their in-place variants too, giving
   substantial performance improvements in all cases that were not dealt
   with manually already, but were covered in standard binary
   operations. Until now only some string, some float operations were
   caught sped up, most often due to findings of Nuitka being terribly
   slower, e.g. not reusing string memory for inplace concatenation, but
   now all operations have code that avoids a generic code path, that is
   also very slow on Windows due calling to using the embedded Python
   via API being slow.

-  For mixed type operations, there was only one direction provided,
   which caused fallbacks to slower forms, e.g. with ``long`` and
   ``float`` values leading to inconsistent results, such that ``a - 1``
   and ``1 - a`` being accelerated or not.

-  Added C boolean optimization for a few operations that didn't have
   it, as these allow to avoid doing full computation of what the object
   result would have to do. This is not exhausted fully yet.

-  Python3: Faster ``+``/``-``/``+=``/``-=`` binary and in-place
   operations with ``int`` values providing specialized code helpers
   that are much faster, esp. in cases where no new storage is allocated
   for in-place results and where not a lot of digits are involved.

-  Python2: The Python3 ``int`` code is the Python2 ``long`` type and
   benefits from the optimization of ``+``/``-``/``+=``/``-=`` code as
   well, but of course its use is relatively rare.

-  Improved ``__future__`` imports to become hard imports, so more
   efficient code is generated for them.

-  Counting of instances had a runtime impact by providing a ``__del__``
   that was still needed to be executed and limits garbage collection on
   types with older Python versions.

-  UI: Avoid loading ``tqdm`` module before it's actually used if at all
   (it may get disabled by the user), speeding up the start of Nuitka.

-  Make sure to optimize internal helpers only once and immediately,
   avoiding extra global passes that were slowing down Python level
   compilation by of large programs by a lot.

-  Make sure to recognize the case where a module optimization can
   provide no immediate change, but only after a next run, avoiding
   extra global passes originating from these, that were slowing down
   compilation of large programs by a lot. Together with the other
   change, this can improve scalability by a lot.

-  Plugins: Remove implicit dependencies for ``pkg_resources.extern``
   and use aliases instead. Using one of the packages, was causing all
   that might be used, to be considered as used, with some being
   relatively large. This was kind of a mistake in how we supported this
   so far.

-  Plugins: Revamped the ``eventlet`` plugin, include needed DNS modules
   as bytecode rather than as source code, scanning them with
   ``pkgutil`` rather than filesystem, with much cleaner code in the
   plugin.

Organisational
--------------

-  Removed support for ``pefile`` dependency walker choice and inline
   copy of the code. It was never as good giving incomplete results, and
   after later improvements, slower, and therefore has lost the original
   benefit over using Dependency Walker that is faster and more correct.

-  Added example for onefile on Windows with the version information and
   with the temporary directory mode.

-  Describe difference in file access with onefile on Windows, where
   ``sys.argv[0]`` and ``os.path.dirname(__file__)`` will be different
   things.

-  Added inline copy of ``tqdm`` to make sure it's available for
   progress bar output for 2.7 or higher. Recommend having it in the
   Debian package.

-  Added inline copy of ``colorama`` for use on Windows, where on some
   terminals it will give better results with the progress bar.

-  Stop using old PyLint for Python2, while it would be nice to catch
   errors, the burden of false alarms seems to high now.

-  UI: Added even more checks on options that make no sense, made sure
   to do this only after a possible restart in proper environment, so
   warnings are not duplicated.

-  For Linux onefile, keep appimage outputs in case of an error, that
   should help debugging it in case of issues.

-  UI: Added traces for plugin provided implicit dependencies leading to
   inclusions.

-  Added inline copy of ``zstd`` C code for use in decompression for the
   Windows onefile bootstrap, not yet used though.

-  Added checks to options that accept package names for obvious
   mistakes, such that ``--include-package-data --mingw64`` will not
   swallow an option, as that is clearly not a package name, that would
   hide that option, while also not having any intended effect.

-  Added ignore list for decision to recompile extension modules with
   available source too. For now, Nuitka will not propose to recompile
   ``Cython`` modules that are very likely not used by the program
   anyway, and also not for ``lxml`` until it's clear if there's any
   benefit in that. More will be added in the future, this is mostly for
   cases, where Cython causes incompatibilities.

-  Added support for using abstract base classes in plugins. These are
   not considered for loading, and allow nicer implementation of shared
   code, e.g. between ``PyQt5`` and ``PySide2`` plugins, but allow e.g.
   to enforce the provision of certain overloads.

-  User Manual: Remove the instruction to install ``clcache``, since
   it's an inline copy, this makes no sense anymore and that was
   obsolete.

-  Updated PyLint to latest versions, and our requirements in general.

Cleanups
--------

-  Started removal of PyLint annotations used for old Python2 only. This
   will be a continuous action to remove these.

-  Jinja2 based static code generation for operations was cleaned up, to
   avoid code for static mismatches in the result C, avoiding language
   constructs like ``if (1 && 0)`` with sometimes larger branches,
   replacing it with Jinja2 branches of the ``{% if ... %}`` form.

-  Jinja2 based Python2 ``int`` code was pioniering the use of macros,
   but this was expanded to allow kinds of types for binary operations,
   allow their reuse for in-place operation, with these macros making
   returns via goto exits rather than return statements in a function.
   Landing pads for these exits can then assign target values for
   in-place different from what those for binary operation result return
   do.

-  Changed the interfacing of plugins with DLL dependency detection,
   cleaning up the interactions considerably with more unified code, and
   faster executing due to cached plugin decisons.

-  Integrate manually provided slot function for ``unicode`` and ``str``
   into the standard static code generation. Previously parts were
   generated and parts could be generated, but also provided with manual
   code. The later is now all gone.

-  Use a less verbose progress bar format with less useless infos,
   making it less likely to overflow.

-  Cleanup how payload data is accessed in Windows onefile bootstrap,
   preparing the addition of decompression, doing the reading from the
   file in only one dedicated function.

-  When Jinja2 generated exceptions in the static code, it is now done
   via proper Jinja2 macros rather than Python code, and these now avoid
   useless Python version branches where possible, e.g. because a type
   like ``bytes`` is already Python version specific, with the goal to
   get rid of ``PyErr_Format`` usage in our generated static code. That
   goal is future work though.

-  Move safe strings helpers (cannot overflow) to a dedicated file, and
   remove the partial duplication on the Windows onefile bootstrap code.

-  The Jinja2 static code generation was enhanced to track the usage of
   labels used as goto targets, so that error exits, and value typed
   exits from operations code no longer emitted when not used, and
   therefore labels that are not used are not present.

-  For implicit dependencies, the parsing of the ``.pyi`` file of a
   module no longer emits a dependency on the module itself. Also from
   plugins, these are now filtered away.

Tests
-----

-  Detect if onefile mode has required downloads and if there is user
   consent, otherwise skip onefile tests in the test runner.

-  Need to also allow accesses to files via short paths on Windows if
   these are allowed long paths.

-  The standalone tests on Windows didn't actually take run time traces
   and therefore were ineffective.

-  Added standalone test for ``glfw`` coverage.

-  Construct based tests for in-place operations are now using a value
   for the first time, and then a couple more times, allowing for real
   in-place usage, so we are sure we measure correctly if that's
   happening.

Summary
-------

Where the big change of the last release were optimization changes to
reduce the global passes, this release addresses remaining causes for
extra passes, that could cause these to still happen. That makes sure,
Nuitka scalability is very much enhanced in this field again.

The new features for forced outputs are at this time Windows only and
make a huge difference when it comes to providing a way to debug Windows
Services or programs in general without a console, i.e. a GUI program.
These will need even more specifiers, e.g. to cover program directory,
rather than exe filename only, but it's a very good start.

On the tooling side, not a lot has happened, with the clcache fix, it
seems that locking issues on Windows are gone.

The plugin changes from previous releases had left a few of them in a
state where they were not working, but this should be restored.
Interaction with the plugins is being refined constantly, and this
releases improved again on their interfaces. It will be a while until
this becomes stable.

Adding support for PySide2 is a headline feature actually, but not as
perfect as we are used to in other fields. More work will be needed,
also in part with upstream changes, to get this to be fully supported.

For the performance side of things, the in-place work and the binary
operations work has taken proof of concept stuff done for Python2 and
applied it more universally to Python3. Until we cover all long
operations, esp. ``*`` seems extremely important and is lacking, this
cannot be considered complete, but it gives amazing speedups in some
cases now.

Future releases will revisit the type tracing to make sure, we know more
about loop variables, to apply specific code helpers more often, so we
can achieve the near C speed we are looking for in the field of ``int``
performance.


Nuitka Release 0.6.12
=====================

This release is yet again a massive improvement in many ways with lots
of bug fixes and new features.

Bug Fixes
---------

-  Windows: Icon group entries were not working properly in some cases,
   leading to no icon or too small icons being displayed.

-  Standalone: The PyQt implicit dependencies were broken. Fixed in
   0.6.11.1 already.

-  Standalone: The datafile collector plugin was broken. Fixed in
   0.6.11.3 already.

-  Standalone: Added support for newer forms of ``matplotlib`` which
   need a different file layout and config file format. Fixed in
   0.6.11.1 already.

-  Plugins: If there was an error during loading of the module or
   plugin, it could still be attempted for use. Fixed in 0.6.11.1
   already.

-  Disable notes given by gcc, these were treated as errors. Fixed in
   0.6.11.1 already.

-  Windows: Fix, spaces in gcc installation paths were not working.
   Partially fixed in 0.6.11.4 already.

-  Linux: Fix, missing onefile icon error message was not complete.
   Fixed in 0.6.11.4 already.

-  Standalone: Workaround ``zmq`` problem on Windows by duplicating a
   DLL in both expected places. Fixed in 0.6.11.4 already.

-  Standalone: The ``dill-compat`` plugin wasn't working anymore. Fixed
   in 0.6.11.4 already.

-  Windows: Fix mistaken usage of ``sizeof`` for wide character buffers.
   This caused Windows onefile mode in temporary directory. Fixed in
   0.6.11.4 already.

-  Windows: Fix, checking subfolder natured crashed with different
   drives on Windows. Fixed in 0.6.11.4 already.

-  Windows: Fix, usage from MSVC prompt was no longer working, detect
   used SDK properly. Fixed in 0.6.11.4 already.

-  Windows: Fix, old clcache installation uses pth files that prevented
   our inline copy from working, workaround was added.

-  Windows: Also specify stack size to be used when compiling with gcc
   or clang.

-  Fix, claim of Python 3.9 support also in PyPI metadata was missing.
   Fixed in 0.6.11.5 already.

-  Python3.9: Subscripting ``type`` for annotations wasn't yet
   implemented.

-  Python3.9: Better matching of types for metaclass selection, generic
   aliases were not yet working, breaking some forms of type annotations
   in base classes.

-  Windows: Allow selecting ``--msvc-version`` when a MSVC prompt is
   currently activated.

-  Windows: Do not fallback to using gcc when ``--msvc-version`` has
   been specified. Instead it's an error if that fails to work.

-  Python3.6+: Added support for ``del ()`` statements, these have no
   effect, but were crashing Nuitka.

   .. code:: python

      del a  # standard form
      del a, b  # same as del a; del b
      del (a, b)  # braces are allowed
      del ()  # allowed for consistency, but wasn't working.

-  Standalone: Added support for ``glfw`` through a dedicated plugin.

-  macOS: Added support for Python3 from system and CPython official
   download for latest OS version.

New Features
------------

-  UI: With ``tqdm`` installed alongside Nuitka, experimental progress
   bars are enabled. Do not use `` --show-progress`` or ``--verbose`` as
   these might have to disable it.

-  Plugins: Added APIs for final processing of the result and onefile
   post processing.

-  Onefile: On Windows, the Python process terminates with
   ``KeyboardInterrupt`` when the user sends CTRL-break, CTRL-C,
   shutdown or logoff signals.

-  Onefile: On Windows, in case of the launching process terminating
   unexpectedly, e.g. due to Taskmanager killing it, or a ``os.sigkill``
   resulting in that, the Python process still terminates with
   ``KeyboardInterrupt``.

-  Windows: Now can select icons by index from files with multiple
   icons.

Optimization
------------

-  Avoid global passes caused by module specific optimization. The
   variable completeness os now traced per module and function scope,
   allowing a sooner usage. Unused temporary variables and closure
   variables are remove immediately. Recognizing possible auto releases
   of parameter variables is also instantly.

   This should bring down current passes from 5-6 global passes to only
   2 global passes in the normal case, reducing frontend compile times
   in some cases massively.

-  Better unary node handling. Dedicated nodes per operation allow for
   more compact memory usage and faster optimization.

-  Detect flow control and value escape for the repr of node based on
   type shape.

-  Enhanced optimization of caught exception references, these never
   raise or have escapes of control flow.

-  Exception matching operations are more accurately annotated, and may
   be recognized to not raise in more cases.

-  Added optimization for the ``issubclass`` built-in.

-  Removed scons caching as used on Windows entirely. We should either
   be using ``clcache`` or ``ccache`` automatically now.

-  Make sure to use ``__slots__`` for all node classes. In some cases,
   mixins were preventing the feature from being it. We now enforce
   their correct specification of slots, which makes sure we can't miss
   it anymore. This should again gain more speed and save memory at
   frontend compile time.

-  Scons: Enhanced gcc version detection with improved caching behavior,
   this avoids querying the same gcc binary twice.

Organisational
--------------

-  The description of Nuitka on PyPI was absent for a while. Added back
   by adding long description of the project derived from the README
   file.

-  Avoid terms ``blacklist``, ``whilelist`` and ``slave`` in the Nuitka
   code preferring ``blocklist``, ``ignorelist`` and ``child`` instead,
   which are actually more clear anyway. We follow a general trend to do
   this.

-  Configured the inline copy of Scons so pylance has an easier time to
   find it.

-  The git commit hook had stopped applying diffs with newest git,
   improved that.

-  Updated description for adding new CPython test suite.

-  Using https URLs for downloading dependency walker, for it to be more
   secure.

-  The commit hook can now be disabled, it's in the Developer Manual how
   to do it.

Cleanups
--------

-  Moved unary operations to their own module, the operators module was
   getting too crowded.

-  The scons files for Python C backend and Windows onefile got cleaned
   up some more and moved more common code to shared modules.

-  When calling external tools, make sure to provide null input where
   possible.

-  Unified calling ``install_name_tool`` into a single method for adding
   rpath and name changes both at the same time.

-  Unified how tools like ``readelf``, ``ldconfig`` etc. are called and
   error exits and outputs checked to make sure we don't miss anything
   as easily.

Tests
-----

-  Adapted for some openSUSE specific path usages in standalone tests.

-  Basic tests for onefile operation and with termination signal sent
   were added.

Summary
-------

The big changes in this release are the optimization changes to reduce
the global passes and the memory savings from other optimization. These
should again make Nuitka more scalable with large projects, but there
definitely is work remaining.

Adding nice stopping behaviour for the Onefile mode on Windows is
seemingly a first, and it wasn't easy, but it will make it more reliable
to users.

Also tooling of gcc and MSVC on Windows got a lot more robust, covering
more cases, and macOS support has been renewed and should be a lot
better now.

The progress bar is a nice touch and improves the overall feel of the
compilation process, but obviously we need to aim at getting faster
overall still. For projects using large dependencies, e.g. Pandas the
compilation is still far too slow and that will need work on caching
frontend results, and better optimization and C code generation for the
backend.


Nuitka Release 0.6.11
=====================

This release is a massive improvement in many ways with lots of bug
fixes and new features.

Bug Fixes
---------

-  Fix, the ``.pyi`` file parser didn't handle relative imports. Fixed
   in 0.6.10.1 already.

-  Windows: Fix, multiprocessing plugin was not working reliable
   following of imports from the additional entry point. Fixed in
   0.6.10.1 already.

-  Pipenv: Workaround parsing issue with our ``setup.py`` to allow
   installation from Github. Fixed in 0.6.10.1 already.

-  Merging of branches in optimization could give indeterministic
   results leading to more iterations than necessary. Fixed in 0.6.10.1
   already.

-  Windows: Avoid profile powershell when attempting to resolve
   symlinks. Fixed in 0.6.10.1 already.

-  Windows: Fix, always check for stdin, stdout, and stderr presence.
   This was so far restricted to gui mode applications, but it seems to
   be necessary in other situations too. Fixed in 0.6.10.1 already.

-  Python2: Fix, ``--trace-execution`` was not working for standalone
   mode but can be useful for debugging. Fixed in 0.6.10.1 already.

-  Windows: Onefile could run into path length limits. Fixed in 0.6.10.3
   already.

-  Windows: The winlib gcc download link became broken and was updated.
   Fixed in 0.6.10.3 already.

-  Plugins: The "__main__" module was not triggering all plugin hooks,
   but it needs to for completeness.

-  Standalone: Fix, symlinked Python installations on Windows were not
   working, with dependency walker being unable to look into these.
   Fixed in 0.6.10.4 already.

-  Standalone: Fix support for numpy on Windows and macOS, the plugin
   failed to copy important DLLs. Fixed in 0.6.10.4 already.

-  Python3: For versions before 3.7, the symlink resolution also needs
   to be done, but wasn't handling the bytes output yet. Fixed in
   0.6.10.4 already.

-  Fix, folder based inclusion would both pick up namespace folders and
   modules of the same name, crashing the compilation due to conflicts.
   Fixed in 0.6.10.4 already.

-  Fix, the ``--lto`` wasn't used for clang on non-Windows yet.

-  Fix, the order of locals dict releases wasn't enforced, which could
   lead to differences that break caching of C files potentially. Fixed
   in 0.6.10.5 already.

-  Fix, ``hash`` nodes didn't consider if their argument was raising,
   even if the type of the argument was ``str`` and therefore the
   operation should not. Fixed in 0.6.10.5 already.

-  Fix, need to copy type shape and escape description for the
   replacement inverted comparisons when used with ``not``, otherwise
   the compilation can crash as these are expected to be present at all
   times. Fixed in 0.6.10.5 already.

-  Fix, some complex constant values could be confused, e.g. ``-0j`` and
   ``0j``. These corner cases were not properly considered in the
   constant loading code, only for ``float`` so far.

-  Standalone: Fix, bytecode only standard library modules were not
   working. This is at least used with Fedora 33.

-  Linux: Fix, extension modules compiled with ``--lto`` were not
   working.

-  Windows: Retry if updating resources fails due to Virus checkers
   keeping files locked.

-  Plugins: Pre- and postload code of modules should not be allowed to
   cause ``ImportError``, as these will be invisible to the other parts
   of optimization, instead make them unraisable error traces.

-  Standalone: Adding missing import for SciPy 1.6 support.

-  Windows: Fix, only export required symbols when using MinGW64 in
   module mode.

New Features
------------

-  Python3.9: Added official support for this version.

-  Onefile: Added command line options to include data files. These are
   ``--include-package-data`` which will copy all non-DLLs and
   non-Python files of package names matching the pattern given. And
   ``--include-data-file`` takes source and relative target file paths
   and copies them. For onefile this is the only way to include files,
   for standalone mode they are mostly a convenience function.

-  Onefile: Added mode where the file is unpacked to a temporary folder
   before running instead of doing it to appdata.

-  Onefile: Added linux specific options ``--linux-onefile-icon`` to
   allow provision of an icon to use in onefile mode on Linux, so far
   this was only available as the hard coded path to a Python icon,
   which also didn't exist on all platforms.

-  UI: Major logging cleanup. Everything is now using our tracing
   classes and even error exits go through there and are therefore
   colored if possible.

-  Plugins: Make it easier to integrate commercial plugins, now only an
   environment variable needs to point to them.

-  UI: Enhanced option parsing gives notes. This complains about options
   that conflict or that are implied in others. Trying to catch more
   usage errors sooner.

-  Plugins: Ignore exceptions in buggy plugin code, only warn about them
   unless in debug mode, where they still crash Nuitka.

-  Scons: More complete scons report files, includes list values as well
   and more modes used.

-  Windows: The ``clcache`` is now included and no longer used from the
   system.

-  Output for ``clcache`` and ``ccache`` results got improved.

-  Enhanced support for ``clang``, on Windows if present near a
   ``gcc.exe`` like it is the case for some winlibs downloads, it will
   be used. To use it provide ``--mingw64 --clang`` both. Without the
   first one, it will mean ``clangcl.exe`` which uses the MSVC compiler
   as a host.

Optimization
------------

-  Some modules had very slow load times, e.g. if they used many list
   objects due to linear searches for memory deduplication of objects.
   We now have dictionaries of practically all constant objects loaded,
   making these more instant.

-  Use less memory at compile time due using ``__slots__`` for all node
   types, finally figured out, how to achieve this with multiple
   inheritance.

-  Use hedley for compiler macros like ``unlikely`` as they know best
   how to do these.

-  Special case the merging of 2 branches avoiding generic code and
   being much faster.

-  Hard imports have better code generated, and are being optimized into
   for the few standard library modules and builtin modules we handle,
   they also now annotate the type shape to be module.

-  No longer annotate hard module import attribute lookups as control
   flow escapes. Not present attributes are changed into static raises.
   Trust for values is configured for a few values, and experimental.

-  Avoid preloaded packages for modules that have no side effects and
   are in the standard library, typically ``.pth`` files will use e.g.
   ``os`` but that's not needed to be preserved.

-  Use ``incbin`` for including binary data through inline assembly of
   the C compiler. This covers many more platforms than our previous
   linker option hacks, and the fallback to generated C code. In fact
   everything but Windows uses this now.

Organisational
--------------

-  Windows: For Scons we now require a Python 3.5 or higher to be
   installed to use it.

-  Windows: Removed support for gcc older than version 8. This
   specifically affects CondaCC and older MinGW64 installations. Since
   Nuitka can now download the MinGW64 10, there is no point in having
   these and they cause issues.

-  We took over the maintenance of clcache as Nuitka/clcache which is
   not yet ready for public consumption, but should become the new
   source of clache in the future.

-  Include an inline copy of clcache in Nuitka and use it on Windows for
   MSVC and ClangCL.

-  Removed compatibility older aliases of follow option, ``--recurse-*``
   and require ``--follow-*`` options to be used instead.

-  For pylint checking, the tool now supports a ``--diff`` mode where
   only the changed files get checked. This is much faster and allows to
   do it more often before commit.

-  Check the versions of isort and black when doing the autoformat to
   avoid using outdated versions.

-  Handling missing pylint more gracefully when checking source code
   quality.

-  Make sure to use the codespell tool with Python3 and make sure to
   error exit when spelling problems were found, so we can use this in
   Github actions too.

-  Removed Travis config, we now only use Github actions.

-  Removed landscape config, it doesn't really exist anymore.

-  Bumped all PyPI dependnecies to their latest versions.

-  Recommend ccache on Debian, as we now consider the absence of ccache
   something to warn about.

-  Plugins: The DLLs asked for by plugins that are not found are no
   longer warned about.

-  Allow our checker and format tools to run on outside of tree code. We
   are using that for Nuitka/clcache.

-  Added support for Fedora 33 and openSUSE 15.3, as well as Ubuntu
   Groovy.

-  Windows: Check if Windows SDK is installed for MSVC and ClangCL.

-  Windows: Enhanced wording in case no compiler was found. No longer
   tell people how to manually install MinGW64, that is no longer
   necessary and ``pywin32`` is not needed to detect MSVC, so it's not
   installed if not found.

-  Detect "embeddable Python" by missing include files, and reject it
   with proper error message.

-  Added onefile and standalone as a use case to the manual and put also
   the DLL and data files problems as typically issues.

Cleanups
--------

-  Avoid decimal and string comparisons for Python versions checks,
   these were lazy and are going to break once 3.10 surfaces. In testing
   we now use tuples, in Nuitka core hexacimal values much like CPython
   itself does.

-  Stop using subnode child getters and setters, and instead only use
   subnode attributes. This was gradually changed so far, but in this
   release all remaining uses have migrated. This should also make the
   optimization stage go faster.

-  Change node constructors to not use a decorator to resolve conflicts
   with builtin names, rather handle these with manual call changes, the
   decorator only made it difficult to read and less performant.

-  Move safe string helpers to their own dedicated helper file, allowing
   for reuse in plugin code that doesn't want to use all of Nuitka C
   helpers.

-  Added utils code for inline copy imports, as we use that for quite a
   few things now.

-  Further restructured the Scons files to use more common code.

-  Plugins: The module name objects now reject many ``str`` specific
   APIs that ought to not be used, and the code got changed to use these
   instead, leading to cleaner and more correct usages.

-  Using named tuples to specify included data files and entry points.

-  Use ``pkgutil`` in plugins to scan for modules rather than listing
   directories.

Tests
-----

-  New option to display executed commands during comparisons.

-  Added test suite for onefile testing.

Summary
-------

This release has seen Python3.9 and Onefile both being completed. The
later needs compression added on Windows, but that can be added in a
coming release, for now it's fully functional.

The focus clearly has been on massive cleanups, some of which will
affect compile time performance. There is relatively little new
optimization otherwise.

The adoption of clcache enables a very fast caching, as it's now loaded
directly into the Scons process, avoiding a separate process fork.

Generally a lot of polishing has been applied with many cleanups
lowering the technical debt. It will be interesting to see where the
hard module imports can lead us in terms of more optimization. Static
optimization of the Python version comparisons and checks is needed to
lower the amount of imports to be processed.

Important fixes are also included, e.g. the constants loading
performance was too slow in some cases. The ``multiprocessing`` on
Windows and ``numpy`` plugins were regressed and finally everything
ought to be back to working fine.

Future work will have to aim at enhanced scalability. In some cases,
Nuitka still takes too much time to compile if projects like Pandas
include virtually everything installed as an option for it to use.


Nuitka Release 0.6.10
=====================

This release comes with many new features, e.g. onefile support, as well
as many new optimization and bug fixes.

Bug Fixes
---------

-  Fix, was memory leaking arguments of all complex call helper
   functions. Fixed in 0.6.9.6 already.

-  Plugins: Fix, the dill-compat code needs to follow API change. Fixed
   in 0.6.9.7 already.

-  Windows: Fixup for multiprocessing module and complex call helpers
   that could crash the program. Fixed in 0.6.9.7 already.

-  Fix, the frame caching could leak memory when using caching for
   functions and generators used in multiple threads.

-  Python3: Fix, importing an extension module below a compiled module
   was not possible in accelerated mode.

-  Python3: Fix, keyword arguments for ``open`` built-in were not fully
   compatible.

-  Fix, the scons python check should also not accept directories,
   otherwise strange misleading error will occur later.

-  Windows: When Python is installed through a symbolic link, MinGW64
   and Scons were having issues, added a workaround to resolve it even
   on Python2.

-  Compatibility: Added support for ``co_freevars`` in code objects,
   e.g. newer matplotlib needs this.

-  Standalone: Add needed data files for gooey. Fixed in 0.6.9.4
   already.

-  Scons: Fix, was not respecting ``--quiet`` option when running Scons.
   Fixed in 0.6.9.3 already.

-  Scons: Fix, wasn't automatically detecting Scons from promised paths.
   Fixed in 0.6.9.2 already.

-  Scons: Fix, the clcache output parsing wasn't robust enough. Fixed in
   0.6.9.1 already.

-  Python3.8: Ignore all non-strings provided in doc-string fashion,
   they are not to be considered.

-  Fix, ``getattr``, ``setattr`` and ``hasattr`` could not be used in
   finally clauses anymore. Fixed in 0.6.9.1 already.

-  Windows: For Python3 enhanced compatibility for Windows no console
   mode, they need a ``sys.stdin`` or else e.g. ``input`` will not be
   compatible and raise ``RuntimeError``.

New Features
------------

-  Added experimental support for Python 3.9, in such a way that the
   CPython3.8 test suite passes now, the 3.9 suite needs investigation
   still, so we might be missing new features.

-  Added experimental support for Onefile mode with ``--onefile`` that
   uses ``AppImage`` on Linux and our own bootstrap binary on Windows.
   Other platforms are not supported at this time. With this, the
   standalone folder is packed into a single binary. The Windows variant
   currently doesn't yet do any compression yet, but the Linux one does.

-  Windows: Added downloading of ``ccache.exe``, esp. as the other
   sources so far recommended were not working properly after updates.
   This is taken from the official project and should be good.

-  Windows: Added downloading of matching MinGW64 C compiler, if no
   other was found, or that was has the wrong architecture, e.g. 32 bits
   where we need 64 bits.

-  Windows: Added ability to copy icon resources from an existing binary
   with new option ``--windows-icon-from-exe``.

-  Windows: Added ability to provide multiple icon files for use with
   different desktop resolutions with new option
   ``--windows-icon-from-ico`` that got renamed to disambiguate from
   other icon options.

-  Windows: Added support for requesting UAC admin right with new option
   ``--windows-uac-admin``.

-  Windows: Added support for requesting "uiaccess" rights with yet
   another new option ``--windows-uac-uiaccess``.

-  Windows: Added ability to specify version info to the binary. New
   options ``--windows-company-name``, ``--windows-product-name``,
   ``--windows-file-version``, ``--windows-product-version``, and
   ``--windows-file-description`` have been added. Some of these have
   defaults.

-  Enhanced support for using the Win32 compiler of MinGW64, but it's
   not perfect yet and not recommended.

-  Windows: Added support for LTO mode for MSVC as well, this seems to
   allow more optimization.

-  Plugins: The numpy plugin now handles matplotlib3 config files
   correctly.

Optimization
------------

-  Use less C variables in dictionary created, not one per key/value
   pair. This improved scalability of C compilation.

-  Use common code for module variable access, leading to more compact
   code and enhanced scalability of C compilation.

-  Use error exit during dictionary creation to release the dictionary,
   list, tuple, and set in case of an error occurring while they are
   still under construction. That avoids releases of it in error exists,
   reducing the generated code size by a lot. This improves scalability
   of C compilation for generating these.

-  Annotate no exception raise for local variables of classes with know
   dict shape, to avoid useless error exits.

-  Annotate no exception exit for ``staticmethod`` and ``classmethod``
   as they do not check their arguments at all. This makes code
   generated for classes with these methods much more compact, mainly
   improving their scalability in C compilation.

-  In code generation, prefer ``bool`` over ``nuitka_bool`` which allows
   to annotate exception result, leading to more compact code. Also
   cleanup so that code generation always go through the C type objects,
   rather than doing cases locally, adding a C type for ``bool``.

-  Use common code for C code handling const ``None`` return only, to
   cases where there is any immutable constant value returned, avoid
   code generation for this common case. Currently mutable constants are
   not handled, this may be added in the future.

-  Annotate no exception for exception type checks in handlers for
   Python2 and no exception if the value has exception type shape for
   Python3. The exception type shape was newly added. This avoids
   useless exception handlers in most cases, where the provided
   exception is just a built-in exception name.

-  Improve speed of often used compile time methods on nodes
   representing constant values, by making their implementation type
   specific to improve frontend compile time speed, we check e.g.
   mutable and hashable a lot.

-  Provide truth value for variable references, enhancing loop
   optimization and merge value tracing, to also decide this correctly
   for values only read, and then changed through attribute, e.g.
   ``append`` on lists. This allows many more static optimization.

-  Use ``staticmethod`` for methods in Nuitka nodes to achieve faster
   frontend compile times where possible.

-  Use dedicated helper code for calls with single argument, avoiding
   the need have a call site local C array of size one, just to pass a
   pointer to it.

-  Added handling of ``hash`` slot, to predict hashable keys for
   dictionary and sets.

-  Share more slot provision for built-in type shapes from mixin
   classes, to get them more universally provided, even for special
   types, where their consideration is unusual.

-  Trace "user provided" flag only for constants where it really
   matters, i.e. for containers and generally potentially large values,
   but not for every number or boolean value.

-  Added lowering of ``bytearray`` constant values to ``bytes`` value
   iteration, while handling constant values for this optimization with
   dedicated code for improved frontend compilation speed.

-  The dict built-in now annotates the dictionary type shape of its
   result.

-  The wrapping side-effects node now passes on the type shape of the
   wrapped value, allowing for optimization of these too.

-  Split ``slice`` nodes into variants with 1, 2 or 3 arguments, to
   avoid the overhead of determining which case we have, as well as to
   save a bit of memory, since these are more frequently used on Python3
   for subscript operations. Also annotate their type shape, allowing
   more optimization.

-  Faster dictionary lookups, esp. in cases where errors occur, because
   we were manually recreating a ``KeyError`` that is already provided
   by the dict implementation. This should also be faster, as it avoids
   a CPython API call overhead on the DLL and they can provide a
   reference or not for the returned value, simplifying using code.

-  Faster dictionary containment checks, with our own dedicated helper,
   we can use code that won't create an exception when an item is not
   present at all.

-  Faster hash lookups with our own helper, separating cases where we
   want an exception for non-hashable values or not. These should also
   be faster to call.

-  Avoid acquiring thread state in exception handling that checks if a
   ``StopIteration`` occurred, to improved speed on Python3, where is
   involves locking, but this needs to be applied way more often.

-  Make sure checks to debug mode and full compatibility mode are done
   with the variables introduced, to avoid losing performance due to
   calls for Nuitka compile time enhancements. This was so far only done
   partially.

-  Split constant references into two base classes, only one of them
   tracking if the value was provided by the user. This saves compile
   time memory and avoids the overhead to check if sizes are exceeded in
   cases they cannot possibly be so.

-  The truth value of container creations is now statically known,
   because the empty container creation is no longer a possibility for
   these nodes, allowing more optimization for them.

-  Optimize the bool built-in with no arguments directory, allow to
   simplify the node for single argument form to avoid checks if an
   argument was given.

-  Added iteration handles for ``xrange`` values, and make them faster
   to create by being tied to the node type, avoiding shared types,
   instead using the mixin approach. This is in preparation to using
   them for standard iterator tracing as well. So far they are only used
   for ``any`` and ``all`` decision.

-  Added detection if a iterator next can raise, using existing iterator
   checking which allows to remove needless checks and exception traces.
   Adding a code variant for calls to next that cannot fail, while
   tuning the code used for ``next`` and unpacking next, to use faster
   exception checking in the C code. This will speed up unpacking
   performance for some forms of unpacking from known sizes.

-  Make sure to use the fastest tuple API possible in all of Nuitka,
   many place e.g. used ``PyTuple_Size``, and one was in a performance
   critical part, e.g. in code that used when compiled functions as
   called as a method.

-  Added optimized variant for ``_PyList_Extend`` for slightly faster
   unpacking code.

-  Added optimized variant for ``PyList_Append`` for faster list
   contractions code.

-  Avoid using ``RemoveFileSpec`` and instead provide our own code for
   that task, slightly reducing file size and avoiding to use the
   ``Shlapi`` link library.

Tests
-----

-  Made reflected test use common cleanup of test folder, which is more
   robust against Windows locking issues.

-  Only output changed CPython output after the forced update of cached
   value was done, avoiding duplicate or outdated outputs.

-  Avoid complaining about exceptions for in-place operations in case
   they are lowered to non-inplace operations and then raise
   unsupported, not worth the effort to retain original operator.

-  Added generated test for subscript operations, also expanding
   coverage in generated tests by making sure, conditional paths are
   both taken by varying the ``cond`` value.

-  Use our own code helper to check if an object has an attribute, which
   is faster, because it avoids creating exceptions in the first place,
   instead of removing them afterwards.

Cleanups
--------

-  Make sure that code generation always go through the C type objects
   rather than local ``elif`` casing of the type. This required cleaning
   up many of the methods and making code more abstract.

-  Added base class for C types without reference counting, so they can
   share the code that ignores their handling.

-  Remove ``getConstant`` for constant value nodes, use the more general
   ``getCompileTimeConstant`` instead, and provide quick methods that
   test for empty tuple or dict, to use for checking concrete values,
   e.g. with call operations.

-  Unified container creation into always using a factory function, to
   be sure that existing container creations are not empty.

-  Stop using ``@calledWithBuiltinArgumentNamesDecorator`` where
   possible, and instead make explicit wrapping or use correct names.
   This was used to allow e.g. an argument named ``list`` to be passed
   from built-in optimization, but that can be done in a cleaner
   fashion. Also aligned no attributes and the argument names, there was
   inconsistency there.

-  Name mangling was done differently for attribute names and normal
   names and with non-shared code, and later than necessary, removing
   this as a step from variable closure taking after initial tree build.

-  As part of the icon changes, now handled in Python code, we stop
   using the ``rc`` binary and handle all resources ourselves, allowing
   to remove that code from the Scons side of things.

-  Moved file comparison code of standalone mode into file utils
   function for use in plugins as well.

-  Unified how path concatenation is done in Nuitka helper code, there
   were more or less complete variants, this is making sure, the most
   capable form is used in all cases.

-  Massive cleanup to our scons file, by moving out util code that only
   scons uses, hacks we apply to speed up scons, and more to separate
   modules with dedicated interfaces.

-  When using ``enumerate`` we now provide start value of 1 where it is
   appropriate, e.g. when counting source code lines, rather than adding
   ``count+1`` on every usage, making code more readable.

Organisational
--------------

-  Do not recommend Anaconda on Windows anymore, it seems barely
   possible to get anything installed on it with a fresh download, due
   to the resolver literally working for days without finishing, and
   then reporting conflicts, it would only we usable when starting with
   Miniconda, but that seems less interesting to users, also gcc 5.2 is
   way too old these days.

-  The commit hook should be reinstalled, since it got improved and
   adapted for newer git versions.

-  Added link to donations to funding document, following a Github
   standard.

-  Bumped requirements for development to the latest versions, esp.
   newer isort.

-  Added a rough description of tests to do to add a new CPython test
   suite, to allow others to take this task in the future.

-  Updated the git hook so that Windows and newest git works.

-  Make it more clear in the documentation that Microsoft Appstore
   Python is not supported.

Summary
-------

This is the big release in terms of scalability. The optimization in
this release mostly focused on getting things that cause increased
compile times sorted out. A very important fix avoids loop optimization
to leak into global passes of all modules unnecessarily, but just as
important, generated code now is much better for the C compiler to
consume in observed problematic cases.

More optimization changes are geared towards reducing Nuitka frontend
compile time, which could also be a lot in some cases, ending up
specializing more constant nodes and how they expose themselves to
optimization.

Other optimization came from supporting Python 3.9 and things come
across during the implementation of that feature, e.g. to be able to
make differences with unpacking error messages, we provide more code to
handle it ourselves, and to manually optimize how to interact with e.g.
``list`` objects.

For Windows, the automatic download of ``ccache`` and a matching MinGW64
if none was found, is a new step, that should lower the barrier of entry
for people who have no clue what a C compiler is. More changes are bound
to come in this field with future releases, e.g. making a minimum
version requirement for gcc on Windows that excludes unfit C compilers.

All in all, this release should be taken as a major cleanup, resolving
many technical debts of Nuitka and preparing more optimization to come.


Nuitka Release 0.6.9
====================

This releases contains important bug fixes for regressions of the 0.6.8
series which had relatively many problems. Not all of these could be
addressed as hotfixes, and other issues were even very involved, causing
many changes to be necessary.

There are also many general improvements and performance work for
tracing and loops, but the full potential of this will not be unlocked
with this release yet.

Bug Fixes
---------

-  Fix, loop optimization sometimes didn't determinate, effectively
   making Nuitka run forever, with no indication why. This has been
   fixed and a mechanism to give up after too many attempts has been
   added.

-  Fix, closure taking object allowed a brief period where the garbage
   collector was exposed to uninitialized objects. Fixed in 0.6.8.1
   already.

-  Python3.6+: Fix corruption for exceptions thrown into asyncgen. Fixed
   in 0.6.8.1 already.

-  Fix, deleting variables detected as C type bool could raise an
   ``UnboundLocalError`` that was wrong. Fixed in 0.6.8.1 already.

-  Python3.8.3+: Fix, future annotations parsing was using hard coded
   values that were changed in CPython, leading to errors.

-  Windows: Avoid encoding issues for Python3 on more systems, by going
   from wide characters to unicode strings more directly, avoiding an
   encoding as UTF8 in the middle. Fixed in 0.6.8.2 already.

-  Windows: Do not crash when warning about uninstalled MSVC using
   Python3. This is a Scons bug that we fixed. Fixed in 0.6.8.3 already.

-  Standalone: The output of dependency walker should be considered as
   "latin1" rather than UTF8. Fixed in 0.6.8.3 already.

-  Standalone: Added missing hidden dependencies for ``flask``. Fixed in
   0.6.8.1 already.

-  Standalone: Fixed ``win32com.client`` on Windows. Fixed in 0.6.8.1
   already.

-  Standalone: Use ``pkgutil`` to scan encoding modules, properly
   ignoring the same files as Python does in case of garbage files being
   there. Fixed in 0.6.8.2 already.

-  Plugins: Enabling a plugin after the filename to compile was given,
   didn't allow for arguments to the passed, causing problems. Fixed in
   0.6.8.3 already.

-  Standalone: The ``certifi`` data file is now supported for all
   modules using it and not only some.

-  Standalone: The bytecode for the standard library had filenames
   pointing to the original installation attached. While these were not
   used, but replaced at runtime, they increased the size of the binary,
   and leaked information.

-  Standalone: The path of ``sys.executable`` was not None, but pointing
   to the original executable, which could also point to some temporary
   virtualenv directory and therefore not exist, also it was leaking
   information about the original install.

-  Windows: With the MSVC compiler, elimination of duplicate strings was
   not active, causing even unused strings to be present in the binary,
   some of which contained file paths of the Nuitka installation.

-  Standalone: Added support for pyglet.

-  Plugins: The command line handling for Pmw plugin was using wrong
   defaults, making it include more code than necessary, and to crash if
   it was not there.

New Features
------------

-  Windows: Added support for using Python 2.7 through a symlink too.
   This was already working for Python3, but a scons problem prevented
   this from working.

-  Caching of compiled C files is now checked with ccache and clcache,
   and added automatically where possible, plus a report of the success
   is made. This can accelerate the re-compile very much, even if you
   have to go through Nuitka compilation itself, which is not (yet)
   cached.

-  Added new ``--quiet`` option that will disable informational traces
   that are going to become more.

-  The Clang from MSVC installation is now picked up for both 32 and 64
   bits and follows the new location in latest Visual Studio 2019.

-  Windows: The ``ccache`` from Anaconda is now supported as well as the
   one from msys64.

Optimization
------------

-  The value tracing has become more correct with loops and in general
   less often inhibits optimization. Escaping of value traces is now a
   separate trace state allowing for more appropriate handling of actual
   unknowns.

-  Memory used for value tracing has been lowered by removing
   unnecessary states for traces, that we don't use anymore.

-  Windows: Prevent scons from scanning for MSVC when asked to use
