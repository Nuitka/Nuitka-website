.. post:: 2022/10/16 10:56
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 1.1
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release contains a large amount of new compatibility features,
while consolidating what we have. Scalability should be better in some
cases.

***********
 Bug Fixes
***********

-  Standalone: Enhanced dependency scan of dependent DLLs to forward the
   containing package, so it can be searched in as well. This fixed at
   least PySide on macOS. Fixed in 1.0.1 already.

-  macOS: Enhanced dependency detection to use normalized paths and
   therefore to be more stable. Fixed in 1.0.1 already.

-  Standalone: Added support for the ``networkx`` package which uses new
   support for a function decorator trying to copy function default
   values. Fixed in 1.0.1 already.

-  Standalone: Include data files for ``pandas.io.format`` package. This
   one has Jinja2 template files that will be needed when using this
   package.

-  Python3.10: Fix, could crash in case a class was not giving ``match``
   arguments, but the user did attempt to match them. This happened e.g.
   with ``range`` objects. Fixed in 1.0.2 already.

-  Standalone: Added data files needed for ``pyenchant`` package. Fixed
   in 1.0.2 already.

-  Python3.10: Fix, matching sequence with ``as`` assignments in them
   didn't check for sub-pattern given. Fixed in 1.0.2 already.

-  Standalone: Fix, do not attempt to list non-existent ``PATH`` entries
   on Windows, these can crash the dependency detection otherwise. Fixed
   in 1.0.2 already.

-  Standalone: Fix, on newer Linux, ``linux-vdso.so.1`` appears in
   output of ``ldd`` in a way that suggests it may exist, which of
   course it does not, this is a kernel virtual DLL. Fixed in 1.0.3
   already.

-  Fix, comparison expressions could give wrong results as a regression
   of the new release. Fixed in 1.0.3 already.

-  Fix, on older Python (before 3.6), it could crash on data files
   defined in the Yaml config. Fixed in 1.0.4 already.

-  Fix, binary operations could give wrong results as a regression of
   the new release. Fixed in 1.0.4 already.

-  Standalone: Added support for ``pyzbar`` package. Fixed in 1.0.5
   already.

-  Standalone: Fix, empty directory structures were not working anymore
   due to a regression in the last release. Fixed in 1.0.5 already.

-  Windows: Fix, detected Pythons from Windows registry may of course
   fail to execute, because they were e.g. manually deleted. This would
   show e.g. in onefile compression. Fixed in 1.0.5 already.

-  Onefile: Fix, using a too old ``zstandard`` without finding another
   Python with a suitable one, lead to run time unpacking errors. Fixed
   in 1.0.6 already.

-  Fix, the inline copy of Jinja2 imported ``logging`` for no good
   reason, which lead to errors for users who have a module of the same
   name, that it was then using instead. Fixed in 1.0.6 already.

-  Fix, disable LTO mode for Anaconda Python, it is known to not work.
   Fixed in 1.0.6 already.

-  Linux: Fix, no need to insist on icon path for onefile anymore. Fixed
   in 1.0.6 already.

-  Standalone: Fix, the new version ``certifi`` was not working on
   Windows and 3.10 anymore. Fixed in 1.0.7 already.

-  Standalone: Added support for more ``rapidfuzz`` implicit
   dependencies. Fixed in 1.0.8 already.

-  Standalone: Added support for ``vibora``. Fixed in 1.0.8 already.

-  Fix, must not expose module name objects to Python import hooks.
   Fixed in 1.0.8 already.

-  Fix, calls to bound methods of string values generated incorrect
   calls. Fixed in 1.0.8 already.

-  Fix, do not crash in version detection on ``gcc`` error exit querying
   of its version.

-  Standalone: Added back support for older versions of the ``pyzmq``
   package.

-  Standalone: Ignore ``PATH`` elements that fail to be listed as a
   directory. It appears e.g. on Windows, folders can exist, despite
   being unusable in fact. These can then cause errors in DLL dependency
   scan. Also avoid having ``PATH`` set when executing dependency
   walker, it appears to use it even if not asked to.

-  Standalone: Added support for ``tzlocal`` package.

-  Python3.10: Fix, ``complex`` literals were not working for mappings
   in ``match`` statements.

-  Fix, ``bool`` built-in expressions were not properly annotating
   exception raises, where the value cannot raise on truth check.

-  Standalone: Added support for the ``agscheduler`` package. Plugins
   must be done manually still with explicit ``--include-module`` calls.

-  Standalone: Added support for using ``shapely`` in Anaconda as well.

-  Debian: Fix, versioned dependency for ``libzstd`` should also be in
   package, this should restore Nuitka package builds for Debian Jessie.

-  Standalone: Added support for ``vtk`` package.

-  Windows: Fix, avoid using ``pywin32`` in our appdirs usage, it might
   be a broken installation and is optional to ``appdirs`` anyway, which
   then will fallback to using ``ctypes`` to make the lookups.

-  Standalone: Added support for more ``pandas`` versions.

-  Standalone: Adding support for ``mkl`` implicit DLL usage in
   Anaconda.

-  Standalone: Added support for ``jsonschema`` with Python 3.10.

-  Standalone: Added support for ``pyfiglet`` fonts data files.

-  Scons: Avoid gcc linker command line length limits for module mode
   too.

-  Standalone: Added data file of ``distributed.config``.

-  Standalone: Add support for ``cv2`` GUI on Linux, the Qt platform
   plugin is now included.

-  Fix, the anti-bloat configuration for ``numpy.testing`` tools exposed
   an incomplete ``suppress_warnings`` replacement that could lead to
   errors in some functions of ``numpy``.

-  Standalone: Fix DLL dependency caching on Windows, need to consider
   DLL content of course too.

-  Standalone: Added missing dependency for ``torchvision``.

-  Standalone: Added support for ``torchvision`` on Anaconda as well.

-  Standalone: Added support for ``panda3d``.

-  Windows: Fix, need to make sure to use UTF-8 encoding for define
   values like company name. Otherwise the local system encoding is
   used, but the C compiler expects UTF-8 in wide literals. This may
   crash of give wrong results.

-  Standalone: Added ``facenet_torch`` data files.

-  Anaconda: Include ``libstdc++.so`` on Linux or else e.g. ``cv2`` will
   not work with system library.

-  Windows: Fix, can have file version without a company name.

**************
 New Features
**************

-  Python3.10: Added support for assignments in ``match`` alternatives
   ``|`` syntax.

-  Compatibility: Register Nuitka meta path based loader with
   ``pkg_resources`` such that checking resource presence with
   ``has_resource`` works too. This should also add support for using
   ``jinja2.PackageLoader``, previously only ``jinja2.FileSystemLoader``
   worked. Fixed in 1.0.1 already.

-  Compatibility: Make function ``__defaults__`` attribute size
   changeable. For a long time, this was a relatively big issue for some
   packages, but now this is supported as well.

-  Compatibility: Added support for ``importlib.metadata.distribution``
   and ``importlib_metadata.distribution`` functions as well
   ``importlib.metadata.metadata`` and ``importlib_metadata.metadata``
   functions.

-  Onefile: Added support for including other binaries than the main
   executable in the payload. So far on non-Windows, we only made the
   main binary executable, hard coded, and nothing else. But Some
   things, e.g. Qt web engine, do require binaries to be used, and these
   no longer have the issue of missing x-bit on macOS and Linux now.

-  Standalone: Resolve executable path when called through symbolic
   link, which makes file resolutions work properly for it, for this
   type of installing it in ``%PATH%``.

-  Python3.9+: Added support for ``importlib.resources.files`` with
   compiled modules.

   It returns traversable objects, which can be used to opens files,
   checks them, etc. and this e.g. allows ``jsonschema`` to work with
   Python 3.10, despite bugs in CPython's compatibility layer.

-  UI: Added interface method to specify filename patterns with package
   data inclusion option, making ``--include-package-data`` usable in
   many more cases, picking the only files or file types you want. You
   can now use ``--include-package-data=package_name=*.txt`` and select
   only a subset of package data files in this way. Before this, it
   included everything and ``--noinclude-data-files`` would have to be
   used.

-  macOS: Make ``runtime`` signing an experimental option.

-  Consistently allow ``when`` conditions for all package configuration
   elements, e.g. also DLLs.

-  Plugins: Added method to overload to work on standalone binary
   specifically. This makes it easier to only modify that specific
   binary.

-  Plugins: Added support for regular expressions in anti-bloat
   replacements, with new ``replacements_re`` code.

**************
 Optimization
**************

-  Add support for ``os.path`` hard module imports along with
   specialized nodes for file tests ``os.path.exists``,
   ``os.path.isfile``, and ``os.path.isdir`` aiming at tracking used
   files, producing warnings about missing files in the future.

-  Standalone: Do not include ``concurrent`` standard library package
   automatically. This avoids the inclusion of ``multiprocessing`` which
   we essentially had reverted during last release cycle.

-  Standalone: Do not include ``zoneinfo`` standard library package
   automatically. It has many data files and is often not used (yet).

-  Standalone: Do not include ``asyncio`` standard library package
   automatically anymore.

-  Avoid compilation of large generated codes in the ``asyncua``
   package.

-  Compile time optimize ``pkg_resources.iter_entry_points`` too, such
   that these can be used to resolve plugin modules, which helps with
   adding support for ``agscheduler`` package plugins. Note that these
   still need to be manually included with ``--include-module`` but now
   that works.

-  For known truth values of the right hand side of ``and`` or ``or``
   conditions, reduce the expression as far as possible.

-  Added dedicated assignment node for hard imports, which then are
   propagated in classes as well, allowing for more static optimization
   for code on the class level.

-  Added linker options to make static ``--static-libpython`` work with
   clang on Linux as well.

-  macOS: Make sure ``libpython`` is loaded relative to the executable.
   This is needed for at least Anaconda Python.

-  macOS: Fix, need to search environment specific DLL paths and only
   then global paths, otherwise mixed Python versions will not work
   correctly.

-  Anti-Bloat: Remove IPython usage in ``rich`` package.

-  Anti-Bloat: Avoid ``doctest`` dependency when using ``pyrect``.

-  Anti-Bloat: Some ``unittest`` removals from ``pytorch`` using
   libraries.

-  Keep the Scons report items sorted, or else it varies for the hashing
   of dependencies with Python versions before 3.6, causing cache misses
   without need.

****************
 Organizational
****************

-  UI: Output the ``.cmd`` file created (if any) on Windows, e.g. when
   run in a virtualenv or for uninstalled Python versions, it will
   otherwise not run in accelerated mode, but previously the output
   suggested to run the executable directly.

-  UI: Enhanced command line option description of
   ``--include-plugin-directory`` which is frequently misunderstood.
   That option barely does what people want it to do. Point them to
   using the other options that are easy to use and will work.

-  UI: Specified needed Python version for use in ``--python-for-scons``
   so users can know ahead of time what versions are suitable.

-  Reports: Added information about data files including, optimization
   times per module, active plugins.

-  Debugging: Repaired offline DLL dependency listing tool, such that it
   can be used during Windows DLL analysis.

-  Make ``--xml`` accept a filename for the node tree dump, and change
   it so it can be executed in addition to actual compilation. This way
   we need not be super-robust about keeping stdout clean, to not break
   XML parsing.

-  Plugins: Avoid useless warning about PySide2 plugin usage if another
   Qt plugin is actually selected.

-  UI: Catch error of directories being used as data files where plain
   files are expected and point out that other options must be used.

-  User Manual: Added section about accessing files in standalone mode
   too, so people can make sure it works properly.

-  Onefile: Using ``%TEMP%`` folder should not by itself prevent cached
   onefile mode, only really variable paths should. People may want to
   have this as some kind of temporary cache still.

-  UI: Catch user error of using elements, that resolve to absolute
   values in the middle of path specs, so using e.g.
   ``something/%PROGRAM%`` is now a mistake caught at compile time.
   These values can only be at the start of spec values naturally.

-  Quality: Updated to newer version of ``rstfmt``.

-  UI: Nicer error message when a forbidden import is requested as an
   implicit import by a plugin.

-  Python3.11: Adapted to allocator and exception state changes, but
   more will be needed to compile at all.

-  Visual Code: Find ``clang-format`` from the recommended C++ extension
   of Visual Code, which makes it finally available on macOS easily too.

-  UI: Quote command line argument values as necessary when stating them
   in the logging. Otherwise they are not directly usable on the shell
   and also less readable.

-  Debian: Do not list fake modules as used debian packages codes, which
   could e.g. happen with the pre-load code of ``pkg_resources`` if that
   is from a Debian package. Fake packages should not be mentioned for
   these lists though.

-  Nuitka-Python: Added support to set link time flags coming from
   statically included packages.

-  For our ``isort`` trick of splitting files in two parts (mostly to
   setup import paths for ``nuitka`` package), make sure the second
   parts starts with a new line.

-  Added more usable form ``--output-filename`` to specify the output
   filename, the short form has become barely usable after we switched
   to enforcing no space separation for command line arguments.

-  UI: Check if output filename's directory exists ahead of time, and
   error exit if not, otherwise compilation crashed only in the very
   end, trying to create the final result.

-  UI: When exiting with no error code, do not use red color or
   ``FATAL`` error annotation, that is not justified.

-  Quality: Make sure the Yaml auto-format does not change effective
   contents.

-  Quality: Added ability to limit autoformat by file type, which can be
   handy when e.g. only the yaml files should be scanned.

-  UI: Removed ``--windows-onefile-tempdir-spec`` alias of
   ``--onefile-tempdir-spec`` option, it is no longer Windows specific.

**********
 Cleanups
**********

-  Prefer single quotes rather than double quotes in our package
   configuration Yaml files, otherwise esp. regular expressions with
   escapes become very confusing.

-  Move import hacks to general mechanism in Yaml package configuration
   files. This is for extra paths from package names or from directory
   paths relative to the package. This removes special purpose code from
   core code paths and allows their reuse.

-  Again more spelling cleanups have been done, to make the code cleaner
   to read and search.

-  Unified how plugins treat iteration over their value list, and how
   the ``when`` condition is applied for the various kinds of sections.

-  Output compilation command that failed during coverage taking, which
   makes it unnecessary to attempt to reconstruct what happened from
   test modes.

*******
 Tests
*******

-  Added coverage for comparisons that need argument swaps.

-  Allow more time in onefile keyboard signal test, otherwise it can be
   a race on slow machines, e.g. emulated machines.

-  Tests: Added support for running a local web server.

*********
 Summary
*********

This release is mainly a consolidation of previous release. Optimization
added in previous release did in fact introduce regressions, that needed
to be addressed and were cause for relatively many hotfixes.

The Yaml nuitka package configuration feature is getting ever more
powerful, but is not one bit more documented, such that the community as
a whole is not yet capable of adding missing dependencies, data files,
DLLs, and even anti-bloat patches.

New optimization was focused around compatibility with very few
exceptions, where the non-automatic standard library work is standing
out, and allows for smaller binaries in many cases.

Scalability has seen improvements through a few optimization, but mainly
again with anti-bloat work being done. This is owed to the fact that
consolidation was the name of the game.

For Anaconda specifically, a lot more software is covered, and
generally, ``cv2`` and ``torch`` related tools are now working better,
but it seems DLL handling will remain problematic in many instances.

The compilation report contains much more information and is getting
there is terms of completeness. At some point, we should ask for it in
bug reports.
