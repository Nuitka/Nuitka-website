.. post:: 2022/01/12 10:51
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.6.19
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release adds support for 3.10 while also adding very many new
optimization, and doing a lot of bug fixes.

***********
 Bug Fixes
***********

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

      # This large value was computed at run time and then if used, also
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
   ``setuptools_rust`` for which a two elements tuple form needs to be
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

**************
 New Features
**************

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

**************
 Optimization
**************

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

****************
 Organisational
****************

-  Migrated the Nuitka blog from Nikola to Sphinx based ABlog and made
   the whole site render with Sphinx, making it a lot more usable.

-  Added a small presentation about Nuitka on the Download page, to make
   sure people are aware of core features.

-  The ``gi`` plugin is now always on. The copying of the ``typelib``
   when ``gi`` is imported is harmless and people can disable the plugin
   if that's not needed.

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
   can not remove the usage, and no options related to following have
   been given.

-  Added Windows version to ``--version`` output of Nuitka. This is to
   more clearly recognize Windows 10 from Windows 11 report, and also
   the odd Windows 7 report, where tool chain will be different.

-  In Visual Code, the default Python used is now 3.9 in the "Linux" C
   configuration. This matches Debian Bullseye.

-  Nicer outputs from check mode of the auto-format as run for CI
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

**********
 Cleanups
**********

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

*******
 Tests
*******

-  Started test suite for Python PGO, not yet completely working though,
   it's not yet doing what is needed though.

-  Added generated test that exercises str methods in multiple
   variations.

-  Revived ``reflected`` test suite, that had been removed, because of
   Nuitka special needs. This one is not yet passing again though, due
   to a few details not yet being as compatible as needed.

-  Added test suite for CPython 3.10 and enable execution of tests with
   this version on GitHub actions.

*********
 Summary
*********

This release is another big step forward.

The amount of optimization added is again very large, some of which yet
again unlocks more static optimization of module imports, that
previously would have to be considered implicit. Now analyzing these on
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
