.. post:: 2022/02/21 13:10
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 0.7
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release is massively improving macOS support, esp. for M1 and the
latest OS releases, but it also has massive improvements for usability
and bug fixes in all areas.

***********
 Bug Fixes
***********

-  Fix, ``set`` creation wasn't annotating its possible exception exit
   from hashing values and is not as free of side effects as ``list``
   and ``tuple`` creations are. Fixed in 0.6.19.1 already.

-  Windows: Fix, ``--experimental`` option values got lost for the C
   compilation when switching from MSVC to MinGW64, making them have no
   effect. Fixed in 0.6.19.1 already.

-  Windows: Fix, Clang from MinGW64 doesn't support LTO at this time,
   therefore default to ``no`` for it. Fixed in 0.6.19.1 already.

-  Debian: Fix, failed to detect Debian unstable as suitable for
   linking, it doesn't have the release number. Fixed in 0.6.19.1
   already.

-  Standalone: Added data files for ``pygsheets`` package. Fixed in
   0.6.19.2 already.

-  Fix, paths from plugin related file paths need to be made absolute
   before used internally, otherwise the cache can fail to deduplicate
   them. Fixed in 0.6.19.2 already.

-  Python3: With gcc before version 5, e.g. on CentOS 7, where we switch
   to using ``g++`` instead, the gcc version checks could crash. Fixed
   in 0.6.19.2 already.

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

-  Windows: Caching of DLL dependencies for the main programs was not
   really working, requiring to detect them anew for every standalone
   compilation for no good reason. Fixed in 0.6.19.3 already.

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
   annotating an exception exit when being optimized away, causing
   consistency checks to complain. Fixed in 0.6.19.5 already.

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

-  Onefile: The onefile binary was locked during run time and could not
   be renamed, preventing in-place updates. This has been resolved and
   now on Windows, the standard trick for updating a running binary of
   renaming it, then placing the new file works.

-  Fix, wasn't checking the ``zstandard`` version and as a result could
   crash if too old versions of it. This is now checked.

-  macOS: Large amounts of bug fixes for the dependency scanner. It got
   cleaned up and now handles many more cases correctly.

-  Windows: Fix, was not properly detecting wrong ClangCL architecture
   mismatch with the Python architecture. This could result in strange
   errors during C compilation in this setup.

-  Standalone: Added implicit dependencies for the ``asyncpg`` module.

-  Linux: Detect Debian or Ubuntu base and distribution name more
   reliably. This helps esp. with static libpython optimization being
   recognized automatically.

**************
 New Features
**************

-  We now disallow options that take arguments to be provided without
   using ``=``.

-  Previously ``--lto no`` worked just as well as ``--lto=no`` did. And
   that was the cause of problems when ``--lto`` first became a choice.

   Recently similar, but worse problems were observed, where e.g.
   ``--include-module`` could swallow trailing other arguments when
   users forgot to specify the name by accident. Therefore this style of
   giving options is now explicitly rejected.

-  Compiled types of Nuitka now inherit from uncompiled types. This
   should allow easier and more complete compatibility, making even code
   in extension modules that uses ``PyObject_IsInstance`` work, e.g.
   ``pydantic``.

-  macOS: Added signing of application bundles and standalone binaries
   for deployment to newer macOS platforms and esp. M1 where these are
   mandatory for execution.

-  macOS: Added support for selecting the single macOS target arch to
   create a binary for. The ``universal`` architecture is not yet
   supported though, but will be added in a future release.

-  Added support for compression in onefile mode through the use of an
   other Python installation, that has the ``zstandard`` module
   installed. With this it will work with 2.6 or higher, but require a
   3.5 or higher Python with it installed in either ``PATH`` or on
   Windows in the registry alternatively.

-  Added UPX plugin to compress created extension modules and binaries
   and for standalone mode, the included DLLs. For onefile, the
   compression is not useful since it has the payload already
   compressed.

-  Added a more explicit way to list usable MSVC versions with
   ``--msvc=list`` rather than requiring an invalid value. Check values
   given in the same way that Scons will do.

-  Added support for ``--python-flag=-u`` which disabled outputs
   buffers, so that these outputs are written immediately.

-  Plugins: Always on plugins now can have command line options. We want
   this for the ``anti-bloat`` plugin that is enabled by default in this
   release.

-  Plugins: Added ability for plugin to provide fake dependencies for a
   module. We want the this for the ``multiprocessing`` plugin, that is
   now enabled by default in this release too.

-  Plugins: Added ability for plugins to modify DLLs after copy for
   standalone. We will be using this in the new ``upx`` plugin.

-  Added retry for file copies that fail due to still running program.
   This can happen on Windows with DLLs in standalone mode. For
   interactive compilation, this allows a retry to happen after
   prompting the user.

-  UI: Added ability to list MSVC versions with ``--msvc=list``, and
   detect illegal values given to ``--msvc=`` before Scons sees them, it
   also crashes with a relative unhelpful error message.

-  UI: When linking, close the C compilation progress bar and state that
   that linking is going on. For some very large LTO compilations, it
   was otherwise at 100% and still taking a long time, confusing users.

-  Plugins: Added new plugin that is designed to handle DLL dependencies
   through a configuration file that can both handle filename patterns
   as well as code provided DLL locations.

-  Optimization: Exclude parts of the standard library by default. This
   allows for much smaller standalone distributions on modules, that can
   be expected to never be an implicit dependency of anything, e.g.
   ``argparse`` or ``pydoc``.

**************
 Optimization
**************

-  Standalone: Do not include ``encodings.bz2_codec`` and
   ``encodings.idna`` anymore, these are not file system encodings, but
   require extension modules.

-  Make sure we use proper ``(void)`` arguments for C functions without
   arguments, as for C functions, that makes a real difference, they are
   variable args functions and more expensive to call otherwise.

-  For standalone, default to using ``--python-flag=no_site`` to avoid
   the overhead that the typically unused ``site`` module incurs. It
   often includes large parts of the standard library, which we now want
   to be more selective about. There is new Python flag added called
   ``--python-flag=site`` that restores the inclusion of ``site``
   module.

-  Standalone: Exclude non-critical codec modules from being technical,
   i.e. have to be available at program startup. This removes the need
   for e.g. ``bz2`` related extension modules previously included.

-  In reformulations, use dictionary methods directly, we have since
   introduced dictionary specific methods, and avoid the unnecessary
   churn during optimization.

-  The complex call helper could trigger unnecessary passes in some
   cases. The pure functions were immediately optimized, but usages in
   other modules inside loops sometimes left them in incomplete states.

-  Windows: Avoid repeated hashing of the same files over and over for
   ``clcache``.

-  Cache dependencies of bytecode demoted modules in first compile and
   reuse that information in subsequent compilations.

-  Linux: Added option for switching compression method for onefile
   created with ``AppImage``. The default is also now ``gzip`` and not
   ``xz`` which has been observed to cause much slower startup for
   little size gains.

-  Standalone: For failed relative imports, during compiled time
   absolute imports were attempted still and included if successful, the
   imports would not be use them at run time, but lead to more modules
   being included than necessary.

****************
 Organisational
****************

-  There is now a `Discord server for Nuitka community
   <https://discord.gg/nZ9hr9tUck>`__ where you can hang out with the
   developers and ask questions. It is mirrored with the Gitter
   community chat, but offers more features.

-  The ``anti-bloat`` is now on by default. It helps scalability by
   changing popular packages to not provide test frameworks,
   installation tools etc. in the resulting binary. This oftentimes
   reduces the compilation by thousands of modules.

-  Also the ``multiprocessing`` plugin is now on by default. Detecting
   its need automatically removes a source of problems for first time
   users, that didn't know to enable it, but had all kinds of strange
   crashes from multiprocessing malfunctioning. This should enhance the
   out of the box experience by a lot.

-  With this release, the version numbering scheme will be changed. For
   a long time we have used 4 digits, where one is a leading zero. That
   was initially done to indicate that it's not yet ready. However, that
   is just untrue these days. Therefore, we switch to 3 digits, and a
   first hotfix with now be 0.7.1 rather than 0.6.19.1, which is too
   long.

   It has been observed that people disregard differences in the third
   digit, but actually for Nuitka these have oftentimes been very
   important updates. This change is to rectify it, and a new release
   will be ``0.8``, and there will be a ``1.0`` release after ``0.9``.

-  Added a new section to User Manual that explains how to manually load
   files, such that it is cleaner and compatible code. Using paths
   relative to current directory is not the right way, but there are
   nice helpers that make it very simple and correct with all kinds of
   contexts.

-  Report the MSVC version in Scons output during compilation. The 2022
   version is required, but we support everything back to 2008, to work
   on very old systems as well. This will help identifying differences
   that arise from there.

-  Quality: Find Clang format from MSVC 2022 too. We use in auto format
   of Nuitka source code, but need to also search that as a new path.

-  Added a spellchecker extension for Visual Code, resulting in many
   spelling fixes in all kinds of documentation and code. This finds
   more things than ``codespell``, but also has a lot of false alarms.

-  Check value of ``--onefile-tempdir-spec`` for typical user errors. It
   cannot be ``.`` as that would require to overwrite the onefile binary
   on Windows, and will generally behave very confusing. Warn about
   absolute or relative paths going outside of where the binary lives.
   Can be useful in controlled setups, but not generally. Also warn
   about using no variables, making non-unique paths.

-  macOS: Flavor detection was largely expanded. The ``Apple`` flavor is
   recognized on more systems. ``Homebrew`` was newly added, and we
   actually can detect ``CPython`` reliably as a first.

-  Added a tool from leo project to create better ``.pyi`` files for
   modules. We will make use of it in the future to enhance the files
   created by Nuitka to not only contain hidden dependencies, but
   optionally also module signatures.

-  Plugins: Clearer information from ``pyside2`` that patched wheels
   might be mandatory and workarounds only patches cannot be done for
   older Python.

-  Added progress bars for DLL dependency detection and DLL copying for
   standalone. These both can end up using take a fair bit of time
   depending on project size, and it's nice to know what's going on.

-  macOS: Added support for using both ``--onefile`` and
   ``--macos-create-app-bundle`` as it is needed for PySide2 due to
   issues with signing code now.

-  Added warning when attempting to include extension modules in an
   accelerated compilation.

-  Modules: Catch the user error of following all imports when creating
   a module. This is very unlikely to produce usable results.

-  Start integrating `Sourcery <https://sourcery.ai>`__ for improved
   Nuitka code. It will comment on PRs and automatically improve Nuitka
   code as we develop it.

-  Debugging: Added command line tool ``find-module`` that outputs how
   Nuitka locates a module in the Python environment it's ran with. That
   removes the need to use Python prompt to dump ``__file__`` of
   imported modules. Some modules even hide parts of their namespace
   actively during run-time, the tool will not be affected by that.

**********
 Cleanups
**********

-  Refactored Python scan previously used for Scons usage on versions
   that need to run in with another Python to be more generally usable.

-  Use explicit ``nuitka.utils.Hashing`` module that allows the core to
   perform these operations with simpler code.

-  macOS: Use ``isPathBelow`` for checking if something is a system
   library for enhanced robustness and code clarity.

-  macOS: Make sure to use our proper error checking wrappers for
   command execution when using tools like ``otool`` or ``codesign``.

-  Standalone: Avoid a temporary file with a script during technical
   import detection. These have been observed to potentially become
   corrupted, and this avoids any chance of that happening, while also
   being simpler code.

-  Avoid naming things ``shlib`` and call them ``extension`` instead.
   Inspired by the spell checker disliking the former term, which is
   also less precise.

-  Removed the dead architecture selection option for Windows, it was
   unused for a long time.

-  Moved Windows ``SxS`` handling of DLLs to a more general place where
   also macOS specific tasks are applied, to host standard modification
   of DLLs during their copying.

*******
 Tests
*******

-  Better matching of relative filenames for search modes of the
   individual test suite runners.

-  Debugger outputs on segfaults were no longer visible and have been
   restored.

*********
 Summary
*********

This release is tremendous progress for macOS. Finally biting the bullet
and paying obscene amounts of money to rent an M1 machine, it was
possible to enhance the support for this platform. Currently typical
packages for macOS are being made compatible as well, so it can now be
expected to perform equally well.

On the quality side, the spell checker has had some positive effects,
finding typos and generally misspelled code, that ``codespell`` does
not, due to it being very conservative.

The trend to enhance plugins has continued. The copying of DLLs is very
nearly finalized. Making more plugins enabled by default is seeing a lot
of progress, with 2 important ones addressed.

Work on the size of distributions has seen a lot of positive results, in
that now standalone distributions are often very minimal, with many
extension modules from standard library no longer being present.
