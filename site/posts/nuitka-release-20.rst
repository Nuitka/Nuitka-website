.. post:: 2024/02/05
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 2.0
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release had focus on new features and new optimization. There is a
really large amount of compatibility with things newly added, but also
massive amounts of new features, and esp. for macOS and Windows, lot of
platform specified new abilities and corrections.

***********
 Bug Fixes
***********

-  Fix, workaround for private functions as Qt slots not having names
   mangled. Fixed in 1.9.1 already.

-  Fix, when using Nuitka with ``pdm`` it was not detected as using pip
   packages. Fixed in 1.9.1 already.

-  Fix, for ``pydantic`` our lazy loader parser didn't handle all cases
   properly yet. Fixed in 1.9.1 already.

-  Standalone: Added data files for ``pyocd`` package. Fixed in 1.9.1
   already.

-  Standalone: Added DLL for ``cmsis_pack_manager`` package. Fixed in
   1.9.1 already.

-  Standalone: Fix, the specs expanded at run time in some causes could
   contain random characters. Fixed in 1.9.2 already.

-  Fix, ``{"a":b, ...}.get("b")`` could crash at runtime. Fixed in 1.9.2
   already.

-  Standalone: Added data files for ``pyproj`` package. Fixed in 1.9.2
   already.

-  Standalone: Added more metadata requirements for ``transformers``
   package. Fixed in 1.9.2 already.

-  Plugins: Fix, could crash when including packages from the command
   line, if they had yaml configuration that requires checking the using
   module, e.g. anti-bloat work. Fixed in 1.9.3 already.

-  Standalone: Added support for ``delphifmx`` package. Fixed in 1.9.4
   already.

-  Android: Fix, cannot exclude ``libz`` on that platform, it's not a
   full Linux OS. Fixed in 1.9.3 already.

-  Standalone: Add needed DLLs for ``bitsandbytes`` package. Fixed in
   1.9.3 already.

-  Windows: Fix, newer ``joblib`` was not working anymore. Fixed in
   1.9.3 already.

-  Windows: Fix, could crash when working with junctions that switch
   drives. Fixed in 1.9.3 already.

-  Fix, was crashing with poetry installed environments. Fixed in 1.9.3
   already.

-  Standalone: Added support for newer ``chromadb`` package. Fixed in
   1.9.3 already.

-  Fix, could crash in report creation on modules excluded that were
   asked via command line for inclusion. Fixed in 1.9.3 already.

-  Anti-Bloat: Fix for newer ``streamlit``, it was causing
   ``SyntaxError`` for the compilation. Fixed in 1.9.4 already.

-  Arch: Added support for their OS release file location too. Fixed in
   1.9.4 already.

-  Windows: Fix, MinGW64 doesn't accept chinese module names a C source
   files. Use short paths for these instead. Fixed in 1.9.4 already.

-  Standalone: Added missing DLL for ``libusb_package`` package. Fixed
   in 1.9.4 already.

-  Fix, properly skip directories with non-module top level names when
   trying to find top level packages of distributions. Fixed in 1.9.4
   already.

-  Fix, avoid memory leak bug in triggered by ``rich`` package. Fixed in
   1.9.4 already.

-  Python3.11+: Fix, didn't detect non-keywords on star dict calls in
   some cases. Fixed in 1.9.4 already.

-  Fix, avoid crashes due to unrecognized installers on macOS and
   Windows, some packages that are built via legacy fallbacks of certain
   pip versions do not leave any indication of their origin at all.
   Fixed in 1.9.4 already.

-  Windows: Fix, need to indicate that the program is long path aware or
   else it cannot work with the paths. Fixed in 1.9.4 already.

-  Debian: The ``extern`` namespace might not exist in the
   ``pkg_resources`` module, make the code work with versions that
   remove it and use the proper external package names then. Fixed in
   1.9.6 already.

-  Compatibility: Fix, need to also have ``.exists`` method in our files
   reader objects. Fixed in 1.9.5 already.

-  macOS: Fix, PyQt5 standalone can fail due to ``libqpdf`` too.

-  Compatibility: Make ``dill-compat`` plugin support module mode too,
   previously this only worked for executables only. Fixed in 1.9.6
   already.

-  Standalone: Added data file for ``curl_cffi`` package. Fixed in 1.9.6
   already.

-  Windows: Fix warnings given by MinGW64 in debug mode for onefile
   compilation. Fixed in 1.9.6 already.

-  Python2: The handling of DLL permission changes was not robust
   against using unicode filenames. Fixed in 1.9.7 already.

-  Python2: Fix, could crash on Debian packages when detecting their
   installer. Fixed in 1.9.7 already.

-  Standalone: Added required data file for ``astor`` package. Fixed in
   1.9.7 already.

-  Reports: Fix, in case of build crashes during optimization, the bug
   report creation could be crashing because the module is not in the
   list of done modules yet. Fixed in 1.9.7 already.

-  Python2: Fix, ``unittest.mock`` was not yet available, code
   attempting to use it was crashing the compilation. Fixed in 1.9.7
   already.

-  Accelerated: Fix, tensorflow configuration removing ``site`` usage
   needs to apply only to standalone mode. Fixed in 1.9.7 already.

-  Plugins: Fix, the ``get_dist_name`` Nuitka Package Configuration
   function could crash in some rare configurations. Fixed in 1.9.7
   already.

-  Standalone: Added necessary data file for ``pygame`` package. Added
   in 1.9.7 already.

-  Standalone: Fix, was not properly handling standard library
   overloading module names for decisions. Inclusion and compilation
   mode were made as if the module was part of the standard library,
   rather than user code. This is now properly checking if it's also an
   actual standard library module.

-  Plugins: Fix, crashing on missing absence message with no UPX binary
   was found.

-  Windows: Fix, couldn't load extension modules from UNC paths, so
   standalone distributions failed to launch from network drives. This
   now works again and was a regression from adding support for symlinks
   on Windows.

-  Standalone: Added support for non-legacy ``pillow`` in ``imageio``
   package.

-  Standalone: Added required ``easyOCR`` data file.

-  Nuitka-Python: Fix, do not demote to non-LTO for "too many" modules
   there in the default auto mode, it doesn't work without it.

-  Fix, ``python setup.py install`` could fail. Apparently it tries to
   lookup Nuitka during installation, which then could fail, due to
   hacks we due to make sure wheels are platform dependent. That hack is
   of course not really needed for install, since no collision is going
   to happen there.

-  macOS: Fix, the standard ``matplotlib`` plugin that uses native UI
   was not included yet, and it was also not working due to bindings
   requiring uncompiled functions, which is now worked around.

-  Compatibility: Add back PySide6 workaround for overloading names like
   ``update`` with slots.

-  Standalone: Added ``geopandas`` data files.

-  Python2: Fix, code objects must be made from ``str`` exactly,
   ``unicode`` however was used in some configurations after recent
   improvements to the run time path handling.

-  Standalone: Added missing data files for ``boto``, the predecessor of
   ``boto3`` as well.

-  Standalone: Added missing DLL for ``tensorflow`` factorization
   module.

-  Compatibility: Fix, PySide2 and PySide6 signal disconnection without
   arguments were not working yet.

-  Standalone: Added support for ``toga``.

-  Scons: Fix, need to Avoid picking up ``clang`` from PATH on Windows
   with ``--clang`` provided, as only our WinLibs version is really
   working.

-  Fix, version of ``setuptools`` when included (which we try to avoid
   very much) was ``None`` which breaks some users of it, now it's the
   correct version so checks of e.g. ``setuptools_scm`` can succeed.

-  Fix, icon options for platforms were conflated, so what should be
   windows only icon could get used on other platforms as well.

-  Fix, could not create compiled methods from compiled methods. Also
   now errors out for invalid types given properly.

**************
 New Features
**************

-  Plugins: Added support for module decisions, these are ``parameters``
   provided by the user which can be used to influence the Nuitka per
   package configuration with a new ``get_parameter`` function. We are
   using these to control important choices in the user, sometimes
   warning it to make that decision, if the default can be considered
   problematic.

-  Plugins: Added support for ``variables`` in Nuitka package
   configurations. We can now query at compile time, values from
   installed packages and use them, e.g. to know what backend is to be
   used.

-  Standalone: Added module decision to disable Torch JIT. This is
   generally the right idea, but the decision is still asked for since
   some packages and programs want to do Torch Tracing, and that is then
   disabled as well. This makes a bunch of transformers programs work.

-  Standalone: Added module decision to disable Numba JIT. This makes
   ``numba`` work in some cases, but not all. Some packages go very deep
   with JIT integration, but simpler uses will now compile.

-  New option ``--include-onefile-external-data`` allows you to specify
   file patterns that you included by other data files others, but to
   put those files not inside, but on the outside of the onefile binary.
   This makes it easier to create deployments fully within Nuitka
   project configuration, and to change your mind back and forth without
   adding/removing the data file option.

-  macOS: Added new value ``auto`` for detecting signing identity, if
   only one is available in the system.

-  macOS: Added support for ``--copyright`` and ``--trademark``
   information to be in app bundles as well, this was previously Windows
   only.

-  Windows: Added support for using junctions in the Python environment,
   these are used e.g. when installing via ``scoop``. Added in 1.9.2
   already.

-  Added option ``--cf-protection`` to select the control flow
   protection mode for the GCC compiler and deviate from default values
   of some environments to less strict values.

-  Reports: Added output filename to report, mainly intended for
   automatically locating the compilation result independent of options
   used.

-  Plugins: Now provides a checksum for yaml files, but not yet verifies
   them at runtime, to ask the user to run the checker tool to update it
   when they make modifications.

-  Windows: Detect when we create too large compiled executables. There
   is a limit of 2GB that you might e.g. violate by attempting to embed
   very large files. This doesn't cover onefile yet.

-  Watch: The tool can now create PRs with the changes in Nuitka-Watch
   for merging, this is for using it in the CI.

-  Watch: Scanning for Python versions now requires ``pipenv`` to be
   installed in them to be found.

-  Watch: Added ability to create branch and PR from watch run results.

-  Plugins: Added ``overridden-environment-variables`` feature to
   package configuration. These are environment variable changes that
   only last during the import of that module and are undone later.

-  Plugins: Added ``force-environment-variables`` feature to package
   configuration. These are environment variable changes done on module
   import that are not undone.

-  Nuitka-Action: Nuitka options that can be given multiple times,
   cannot be specified multiple times in your workflow. As a workaround,
   Nuitka now allows in Actions, to use new lines as separator. This is
   best done with this kind of quoting a multiline string.

   .. code:: yaml

      include-data-dir: |
         a=b
         c=d

-  The Nuitka Package Configuration ``no-auto-follow`` now applies
   recursively, i.e. that a top level package can have it, and not every
   sub-package that uses a package but should not be automatically
   followed, does have to say this. With this e.g. ``networkx``
   configuration became simpler, and yet covered automatically older
   versions as well, and future changes too.

-  Windows: Added support for compiling in case sensitive folders. When
   this option is enabled, using ``os.path.normcase`` can make filenames
   not found, so with a few cleanups, for lazy code that wasn't really
   using the APIs designed for comparisons and filename suffix testing,
   this works now better.

-  The ``__compiled__`` value has a new attribute ``containing_dir``
   that allows to find where a module, accelerate executable, a
   standalone dist folder, a macOS app bundle, or the onefile binary
   lives in a consistent fashion. This allows esp. better use than
   ``sys.argv[0]`` which points deep into the ``.app`` bundle, and can
   be used cross platform.

**************
 Optimization
**************

-  Scalability: Avoid variables that are not shared to be treated as if
   they were, marking their type shape as ``tshape_unknown`` in the
   first micro pass. These micro passes are not visible, but basically
   constitute a full visit of the module tree over and over, until no
   more optimization is changing it. This can lead to quicker
   resolution, as that unknown type shape effectively disallowed all
   optimization for variables and reduce the number of necessary micro
   passes by one.

-  Escaped variables did provide a type shape ``tshape_unknown`` and
   while a lot of optimization looks for value knowledge, and gets by
   the escaped nature of the value, sometimes, this was seriously
   inhibiting some of the type based optimization.

-  Loop type shape analysis now succeeds in detecting the types for this
   code example, which is sort of a break-through for future performance
   enhancements in generated code.

   .. code:: python

      # Initial the value of "i" is "NUITKA_NINT_UNASSIGNED" in its
      # indicator part. The C compiler will remove that assignment
      # as it's only checked in the assignment coming up.
      i = 0
      # Assignment from a constant, produces a value where both the C
      # and the object value are value. This is indicated by a value
      # of "NUITKA_NINT_BOTH_VALID". The code generation will assign
      # both the object member from a prepared value, and the clong
      # member to 0.

      # For the conditional check, "NUITKA_NINT_CLONG_VALID" will
      # always be set, and therefore function will resort to comparing
      # that clong member against 9 simply, that will always be very
      # fast. Depending on how well the C compiler can tell if an overflow
      # can even occur, such that an object might get created, it can even
      # optimize that statically. In this case it probably could, but we
      # do not rely on that to be fast.
      while i < 9:  # RICH_COMPARE_LT_CBOOL_NINT_CLONG
         # Here, we might change the type of the object. In Python2,
         # this can change from ``int`` to ``long``, and our type
         # analysis tells us that. We can consider another thing,
         # not "NINT", but "NINTLONG" or so, to special case that
         # code. We ignore Python2 here, but multiple possible types
         # will be an issue, e.g. list or tuple, float or complex.
         # So this calls a function, that returns a value of type
         # "NINT" (actually it will become an in-place operation
         # but lets ignore that too).
         # That function is "BINARY_OPERATION_ADD_NINT_NINT_CLONG"(i, 1)
         # and it is going to check if the CLONG is valid, add the one,
         # and set to result to a new int. It will reset the
         # "NUITKA_NINT_OBJECT_VALID" flag, since the object will not be
         # bothered to create.
         i = i + 1

      # Since "NUITKA_INT_OBJECT_VALID" not given, need to create the
      # PyObject and return it.
      return i

-  Python3.11+: Use ``tomllib`` from standard library for our distutils
   integration into pyproject based builds.

-  Avoid late specialization for ``None`` returns in generators and do
   it during tree building already, to remove noise.

-  Added successful detection of static libpython for self compiled
   Python Linux and macOS. This makes it work with ``pyenv`` as well.

-  Standalone: Avoid including ``.pyx`` files when scanning for data
   files, these are code files too, in this case source files that are
   definitely unused most of the time.

-  macOS: Make static libpython default with CPython for more compact
   standalone distribution and faster binaries.

-  Remove non-existent entries from ``sys.path``, avoiding many file
   system lookups during import scans.

-  Anti-Bloat: Avoid using ``triton`` in ``torch`` package in more
   cases. Added in 1.9.2 already.

-  Anti-Bloat: Avoid using ``pytest`` in ``knetworkx`` package in more
   cases. Added in 1.9.2 already.

-  Anti-Bloat: Avoid using ``IPython`` in ``distributed`` package. Added
   in 1.9.3 already.

-  Anti-Bloat: Avoid using ``dask`` in ``skimage``. Added in 1.9.3
   already.

-  Anti-Bloat: Avoid using ``triton`` in the ``bitsandbytes`` package.
   Added in 1.9.3 already.

-  Anti-Bloat: Avoid ``IPython`` in ``tf_keras`` package as well. Added
   in 1.9.6 already.

-  Anti-Bloat: Avoid ``unittest`` in ``mock.mock`` module. Added in
   1.9.7 already.

-  Avoid importing ``setuptools_scm`` during compilation when using the
   ``tqdm`` inline copy, this also avoids a warning on Ubuntu. Added in
   1.9.7 already.

-  Anti-Bloat: Avoid ``doctest`` in ``skimage`` in their ``tifffile``
   inline copy as well. Added in 1.9.7 already.

-  Anti-Bloat: Avoid ``h5py.tests`` with older ``h5py`` as well. Added
   in 1.9.7 already.

-  Anti-Bloat: Using ``distributed.utils_test`` is also considered using
   ``pytest``.

-  Anti-Bloat: Avoid ``IPython`` in the ``pip`` package.

-  Anti-Bloat: Avoid ``site`` module for older ``tensorflow`` versions
   too.

-  Anti-Bloat: Avoid more ``unittest`` usages in ``tensorflow``
   packages.

-  Anti-Bloat: Avoid ``nose`` in ``skimage`` package.

-  Anti-Bloat: Avoid ``nose`` in ``networkx`` package.

-  Anti-Bloat: Avoid ``nose`` in ``pywt`` package.

****************
 Organizational
****************

-  UI: Change template paths over from ``%VAR%`` to ``{VAR}``.

   The old spec values are migrated transparently and continue to work,
   but get a warning when used.

   The new code detects unknown variable names and more formatting
   issues than before.

   Using only the ``{PID}`` value for process ID, is now making it
   temporary value for onefile, that was previously a bug.

   The main benefit and reason of doing this, is that Windows
   ``CMD.EXE`` does expand those values before Nuitka sees them as even
   with quoting ``%TEMP%`` is the current one on the building machine, a
   recipe for disaster. As some people still use that, and e.g.
   ``os.system`` or ``subprocess`` with ``shell=True`` will use it too,
   this is just not sustainable for a good user experience.

   As a result, compile time and run time variables now clash, there is
   e.g. ``{VERSION}`` (program version information given) and
   ``{Version}`` (Nuitka version), and we should clean that up too.

-  Project: Added Code of Conduct. Adapted from the one used in the
   Linux kernel.

-  UI: Warnings given by Nuitka used to be in red color, changed those
   to be yellow for consistency.

-  User Manual: Added pointer for Nuitka-Action `Nuitka-Action
   <https://github.com/Nuitka/Nuitka-Action>`__ for users interested in
   using Nuitka in GitHub workflows.

-  Added ``.gitignore`` to build folder that just causes these folders
   to be ignored by git.

-  User Manual: Added information on how to debug fork bombs from
   created binaries.

-  Debugging: The output of ``--experimental=--report-refcounts`` that
   we use to show leaks of compiled time objects at program exit, now
   counts and reports on functions, generator objects and compiled cells
   as well.

-  Quality: Warnings from ``yamllint`` not disabled are errors. These
   were only output, but didn't cause the autoformat to error exit yet.

-  UI: Enhanced formatting of info traces, drop the ``:INFO`` part that
   shouts, and reserve that for errors and warnings. Also format info
   messages to make sure they fit into the line.

-  UI: Changed ``--show-source-changes`` to accept module pattern to
   make it easier to only see the ones currently being worked on. To get
   the old behavior of showing everything, use ``*`` as a pattern.

-  UI: Allow using ``~`` in data files source path for command line
   options and expand it properly.

-  Quality: Enhanced schema for our package configuration yaml files to
   detect suffixes with leading dots, that is not wanted. These now fail
   checks, but we also tolerate them now.

-  Quality: Check module names used in the package configuration yaml
   files for validity, this catches e.g. trailing dots.

-  Quality: Make sure to really prefer ``clang-format`` from Visual Code
   and MSVC for formatting C code, otherwise a system installed one
   could be used that gives slightly different outputs.

-  Scons: Allow disabling to enforce no warnings for C compilation

   Currently only for gcc, where we need it until loop tracing is
   better, we can now use ``--experimental=allow-c-warnings`` options to
   make ``--debug`` work for some known currently unavoidable warnings.

-  macOS: Make ``--macos-create-app-bundle`` imply standalone mode, it's
   not working or useful for accelerated mode anyway.

-  Standalone: Added support for using self-compiled Python versions
   that are not installed on Linux and macOS. This avoids having to do
   ``make install`` and can ease debugging with changes made in Python
   core itself. Added in 1.9.6 already.

-  Release: Added ability to simple re-date hotfixes. Previously the
   version bump commit needed to be dropped, now a fixup commit is easy
   to generate.

-  Release: Man pages are no longer built during package builds, but are
   available statically in the git, which should make it easier.

-  Release: Disable verbose output in package installation of Nuitka, it
   never was any use, and just makes things hard to read.

-  UI: Check user yaml file present immediately. Otherwise it was
   crashing when parsing yaml files first time with less comprehensible
   exceptions. Added in 1.9.7 already.

-  Quality: Updated to latest ``rstfmt``, ``black`` and ``isort``
   versions.

-  Debian: Remove references to PDF documentation that no longer exists.

-  Quality: Do not crash when collecting modified files due to deleted
   files.

-  UI: Detect the Alpine flavor of Python as well.

-  UI: Detect ``manylinux`` Pythons as a Python flavors as well.

-  UI: Detect self compiled uninstalled Python as a dedicated flavor.

**********
 Cleanups
**********

-  For the Nuitka-Action part of the available options is now generated
   from Nuitka option definitions itself, adding some previously missing
   options as a result. As a result, adding
   ``--include-onefile-external-data`` was automatic this time.

-  The warnings for onefile only options without onefile mode provided
   have been moved to common code, and in some cases were having wrong
   texts corrected.

-  Use enum definitions in the Nuitka Package Configuration schema
   rather than manual ``oneOf`` types.

-  The User Manual was proof read and had a bunch of wordings improved.

-  Cleanup, avoid "unused but set variable" warning from the C compiler
   for hard some forms of hard imports.

-  Prefer ``os.getenv`` over ``os.environ.get`` for readability.

-  Changed parts of the C codes that ``clang-format`` had a hard time
   with to something more normal.

*******
 Tests
*******

-  When locating the standalone binary created, use a compilation report
   and resolve the path specified there. This allows macOS app bundles
   to be used in these tests as well.

-  Made the PyQt tests executable on macOS too adding necessary options.

-  Added reference test case for unpacking into a list, this was not
   covered but under suspect of reference leaking which turns out to be
   wrong.

-  Much enhanced usage of ``virtualenv`` in the ``distutils`` test
   cases. We make more sure to delete them even in case of issues. We
   disable warnings during Nuitka package installation. The code to
   execute a case was factored out and became more clear. We now handle
   errors in execution with stating what case actually failed, this was
   a bit hard to tell previously. Also do not install Nuitka when a
   pyproject case is used, since the build tool installs Nuitka itself.

*********
 Summary
*********

This release deserves the 2.0 marker, as it is ground breaking in many
ways. The loop type analysis stands out on the optimization front. This
will open an avenue for much optimized code at least for some benchmark
examples this summer.

The new features for package configuration, demonstrate abilities to
avoid plugins for Nuitka, where those previously would have been used.
The new ``variables`` and ``parameters`` made it unnecessary to have
them, and still add compile time variable use and user decisions and
information, without them.

The scope of supported Python configurations got expanded a bit, and the
the usual slew of anti-bloat work and new packages supported, makes
Nuitka an ever more round package.

The improved user dialog with less noisy messages and slightly better
coloring, continues a trend, where Nuitka becomes more and more easy to
use.

.. include:: ../dynamic.inc
