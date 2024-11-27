.. post:: 2023/12/17 14:25
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 1.9
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release has focused on improved startup time and compatibility with
lazy loaders which has resulted in some optimization. There are also the
usual amounts of bug fixes. For macOS and Linux there are lots of
improvements that should make standalone mode for them robust with many
more configurations.

***********
 Bug Fixes
***********

-  Nuitka Action: Fix, the parsing code intended for the github action
   was not working as advertised. Fixed in 1.8.1 already.

-  Standalone: Follow ``soundfile`` change for their DLL names. Fixed in
   1.8.1 already.

-  MSYS: Fix, the recent change to detect their Python flavor with 3.11
   was done wrong. Fixed in 1.8.1 already.

-  Windows: Ignore MS API DLLs found from ``%PATH%``. We only ignored
   them because they come from the Windows system folder, but if any
   program has them, then we did include them. Fixed in 1.8.1 already.

-  Standalone: Fix, ``calendar`` is used by ``time`` built-in module
   actually and therefore must be included. Fixed in 1.8.1 already.

-  Standalone: Added data file for ``unstructured`` package. Fixed in
   1.8.1 already.

-  Standalone: Added data file for ``grpc`` package. Fixed in 1.8.1
   already.

-  Standalone: Added missing dependency for ``skimage``. Fixed in 1.8.1
   already.

-  Python3.11: The dictionary copy code could crash on special kinds of
   dictionaries. Fixed in 1.8.2 already.

-  Standalone: Added data file required by ``ens`` of ``web3`` package.
   Fixed in 1.8.2 already.

-  Fix, ``multiprocessing`` could not access attributes living in
   ``__main__`` module, but only things elsewhere, breaking minimal
   examples. Fixed in 1.8.2 already.

-  Reports: Fix, the license of some packages in case it is ``UNKNOWN``
   was not handling all the cases that wheels expose. Fixed in 1.8.2
   already.

-  Fix, using ``--include-module`` and ``--include-package`` was
   behaving identical for packages. Made the former not include all of
   the package, but only the top level and what that uses.

-  Standalone: Added support for the ``lightning`` package. Fixed in
   1.8.3 already.

-  Distutils: Fix, the platform tag was sometimes incorrect for wheels
   built. Fixed in 1.8.3 already.

-  Compatibility: Make the PySide2/PySide6 signal connection workaround
   more robust. It was not handling reuse of the same method properly
   and insisted on changing ``__name__`` which some objects apparently
   dislike a lot. Fixed in 1.8.4 already.

-  Windows: Fix, need to use short path for the Python installation
   prefix, as it might be Unicode path as well. Fixed in 1.8.4 already.

-  Fix, output spec ``%NONE%`` was not compiling anymore. Fixed in 1.8.4
   already.

-  Reports: Avoid having short paths for DLL sources on Windows. Fixed
   in 1.8.4 already.

-  Fix, catch provided metadata from command line
   ``--include-distribution-metadata`` without including the package at
   runtime. Fixed in 1.8.4 already.

-  Python3.10+: Fix, was not properly initializing indicator variable
   used in the ``match`` re-formulation. The generated code still work,
   but this was an error on the logical level to use a variable
   un-initialized. Fixed in 1.8.4 already.

-  Standalone: Added missing DLLs for ``rlottie-python``. Fixed in 1.8.4
   already.

-  Standalone: Added missing implicit dependencies and also avoid
   duplication of DLLs for the ``av`` package. Fixed in 1.8.4 already.

-  Fix, was not handling errors when creating distribution objects.
   Fixed in 1.8.4 already.

-  macOS: Remove extended attributes from DLLs, e.g. ``finder`` can add
   them and it prevents code signing. Fixed in 1.8.4 already.

-  macOS: Workaround for signing tkinter data files properly, we just
   exclude the problematic ones, as they are going to be unused. Fixed
   in 1.8.4 already.

-  Standalone: Added hidden dependency of ``curl_cffi`` package. Fixed
   in 1.8.5 already.

-  Standalone: Added hidden dependency of ``tensorflow`` package. Fixed
   in 1.8.5 already.

-  Standalone: Added more ``kivymd`` data files. Fixed in 1.8.5 already.

-  Standalone: Added implicit dependency for ``winloop`` package. Fixed
   in 1.8.6 already.

-  Windows: Fix, do not resolve main program executable filename to long
   filename. Fixed in 1.8.5 already.

-  Windows: Fix, ignore ``ucrtbase`` runtime DLLs found from ``%PATH%``
   as well. Fixed in 1.8.6 already.

-  Compatibility: Fix, the ``dill-compat`` plugin was regressed and
   support for ``dill`` version 0.3 was added.

-  Fix, need to include package name for ``joblib`` usage with
   ``--python-flag=-m`` to work properly.

-  Windows: Added support for newest ``joblib`` too, we no longer need
   to error for using the latest one.

-  Fix, attribute lookups becoming hard through node factories didn't
   annotate possible exceptions.

-  Standalone: Added support for ``huggingface_hub`` vendored lazy
   loader variant.

-  Standalone: Added support for ``datasets`` module.

-  Plugins: Handle default plugin of ``matplotlib`` a lot better. Be
   more graceful when the query of the default one fails, and point to
   ``MPLBACKEND`` usage. Otherwise inform the user of the backend used
   for ``matplotlib`` so it can be checked.

-  Fix, ``--include-module`` on a package was including all of it rather
   than just top level, which was what it should do. For including the
   full package, there is ``--include-package`` instead.

-  macOS: Fix, need to check dependencies for the selected target arch
   precisely, otherwise DLLs and extension modules for the other arch
   can cause errors for our dependency analysis in standalone mode.

      -  Also added support for getting DLL exported symbols on macOS
         which then allows to properly distinguish extension modules
         from mere DLLs on macOS, and not just Linux.

-  MSYS2: Fix, the GTK DLL name changed again.

-  Compatibility: Added support for ``.zip`` files being in python path
   as well.

-  Fix, when a sub-package module import is rejected for whatever
   reason, the programs attempt to import it, still implies an attempt
   to import the parent module. For extension modules in accelerated
   mode, this is of course common, but the containing package if any, is
   of course still to be included.

-  Fix, PySide6 in accelerated mode needs workarounds too, previously
   only standalone mode was avoiding the corruptions it was causing.

-  Fix, make the PySide2/PySide6 signal connection workaround also fix
   disconnection only. For signals that only ever got disconnected, but
   never connected, the workaround was not applied.

-  MSYS2: For standalone add more GI dlls.

-  Fix, inline copies of e.g. ``tqdm`` could be detected during
   compilation and even in place of the real package.

-  Standalone: Added proper support for ``timm`` without disabling JIT
   generally.

-  Python3.11: Fix, frozen stdlib modules must be turned off

   Otherwise the value of ``os.__file__`` becomes wrong, and maybe more
   issues, as Nuitka is more compatible to full modules than the frozen
   modules are for standalone mode at least.

-  Python2: Avoid RuntimeWarning when using inline copy of ``tqdm``.

-  Standalone: Added support for newer ``pydantic`` and its lazy loader.

-  Standalone: Add config for font data files of ``qtawesome`` package.

-  Plugins: Added workaround for PySide6 enums checking bytecode when
   some older enum values are used. The PySide6 means to detect method
   calls vs. type lookups to decide if to inject the default value for a
   flag value. With our workaround, enums behave as expected without
   that check being possible.

-  Standalone: Added support for ``gradio`` package.

-  Python3.6+: Added support for non-latin (for example Chinese) module
   names, these were not working correctly yet.

-  Python3: Fix, star importing from modules with non-UTF8 encodable
   names in the module dictionary crashed.

-  Python2: Fix, couldn't list directories with unicode filenames in
   them, so that e.g. a Python3 created build directory with unicode
   module names was not possible to fully delete.

-  Compatibility: Added missing ``as_posix`` method to our resource
   reader objects.

-  Standalone: Added missing DLLs for ``PyAutoIt`` package.

-  Standalone: Added data files for the ``flask_restx`` package, for
   which ``--include-package-data`` also wouldn't work, due to its
   strange handling when running in frozen mode.

-  Standalone: Added more metadata requirements for ``transformers``
   package.

-  Standalone: Added support for newer ``transformers`` package.

-  Standalone: Added data files for ``yapf`` vendored ``lib2to3``
   package.

-  Plugins: Fix, was crashing on module patterns of submodules not
   existing in the yaml config implicit dependencies.

**************
 New Features
**************

-  Plugins: Introduce an explicit hard import registry, that now can be
   expanded at compile time by plugins.

-  Plugins: Added support for ``lazy`` delayed loading, which removes
   the need for ``include-pyi-file`` as we inline its effect at compile
   time. Also, the dependencies of these kinds of packages no longer
   need to be overreaching and can analyze the code again. This is using
   the hard import registry plugin interface.

-  Linux: Standalone builds with PyPI packages no longer include system
   DLLs unless a new Yaml configuration for DLLs called
   ``package-system-dlls`` is configured, which will be necessary for
   GTK bindings probably. With this the included DLLs will more often be
   only ones suitable for use on other OSes. This should make Linux
   standalone somewhat easier, but still need to compile on old OS.

-  Reports: For distributions include the ``installer`` name, so we can
   tell pip, conda or system packages apart better.

-  Reports: For included modules, we now also attribute the
   distributions it directly uses modules from and the distribution the
   module itself belongs to was added as an attribute as well.

-  Reports: Added excluded module reasons to reporting, so that it can
   be told directly, which imports were found, but not followed to. Also
   added report reader capable of providing information from a
   compilation report.

-  Added support for FIPS compliance, a US security standard by NIST,
   that caused parts of Python used by Nuitka to be flagged.

-  Watch: Added option to control the update mode, handles now rc
   versions, so it can be used before and after Nuitka releases easily.

-  Watch: Added timeout for how long programs are allow to run.

-  Watch: Added ability to recognize fork loops happening, so test cases
   of e.g. ``joblib`` do not suddenly go wild on a break change in that
   or other packages.

-  macOS: The ``--list-package-dlls`` now needs to check target arch
   options, so we now delay the non-compiling options execution until
   it's set, which also makes it cleaner code. Also, we can now
   distinguish real Python extension modules from mere DLLs on macOS
   too.

-  Standalone: Also ignore ``av`` and ``cv2`` DLL collisions, making it
   more generic.

-  Standalone: Make ``tk-inter`` plugin more robust. Detect the tkinter
   version used and scan for its paths. Use path used when compiling
   ``tcl`` from source and check data directory paths for ``tcl`` and
   ``tk`` for expected files, and error out if they are not found. With
   these changes self-compiled Python as e.g. used in our commercial
   Linux container is supported too now.

-  Enhanced support for self compiled Python by using link libraries
   needed for static linked extension modules. This allows a better
   commercial Linux container build mainly.

**************
 Optimization
**************

-  Optimization: Enhanced handling of aliased variables.

   Was not converting variable assignments from variables created during
   re-formulations to the dedicated nodes, potentially missing out on
   optimizations specific to that case, because it was then not
   recognized to be non-generic anymore later.

   Was not optimizing comparisons and truth checks for temporary
   variable references, missing out a lot of opportunities for
   optimization of code coming from re-formulations.

   When a variable is aliased, but the source variable is one that
   cannot escape or is even very hard value, we were not annotating that
   as well as possible, but now e.g. comparisons with constant values
   that are immutable are done even if aliased.

   Remove knowledge of variables assigned to other variables only if
   that value can actually escape, otherwise that has no real point.

-  Use variable length encoding for data blob size values. This removes
   size constraints in some cases, but also makes the representation of
   ``list``, ``tuple``, ``dict`` more compact, since they commonly have
   only a few elements, but we used 4 bytes for length, where the
   average should be close to one 1 byte per length item now.

-  Faster CRC32 with zlib, leading to much faster program startup, and
   faster checksums for cached mode of onefile, improving that a lot as
   well.

-  Windows: Updated MinGW64 to latest winlibs package, should produce
   even faster code and show stopping bugs in its ``binutils`` have
   apparently been fixed. This should now link a lot faster with LTO,
   due to using multiple processes.

-  Added support for ``builtins.open`` as hard import to ``open``.

-  Scalability: Make sure we actually use ``__slots__`` for our classes.
   Variables, code generation context, iteration handles, and type
   shapes didn't really use those and that should speed their use up and
   therefore reduce Python compile time and memory usage.

-  Standalone: Removed one more automatic stdlib module ``textwrap`` as
   it otherwise uses a runner code with test code that is bloating with
   hello world code.

-  Fedora: Enabled LTO linking by default as well, it's working, but
   Fedora Python is still not really good to use, since it doesn't allow
   static linking of libpython.

-  Anti-Bloat: Avoid ``pytest`` usage in ``pooch`` package. Added in
   1.8.1 already.

-  Anti-Bloat: Remove ``pdb`` usage from ``pyparsing`` package. Added in
   1.8.2 already.

-  Anti-Bloat: Remove ``unittest`` usage in ``bitarray``. module. Added
   in 1.8.2 already.

-  Anti-Bloat: Avoid ``lightning`` to cause use of its
   ``lightning.testing`` framework.

-  Anti-Bloat: Added override that that ``torch`` but only it can use
   ``unittest``, it will not work otherwise.

-  Anti-Bloat: Avoid using ``IPython`` in ``gradio`` package.

-  Anti-Bloat: Avoid using ``IPython`` in ``altair`` package.

-  Anti-Bloat: Avoid using ``numba`` in ``pyqtgraph`` package.

-  Anti-Bloat: Avoid using ``triton`` in ``torch`` package.

-  Anti-Bloat: Avoid using ``unittest`` in ``multiprocess`` package.

-  Anti-Bloat: Avoid using ``setuptools`` with new ``mmcv`` package as
   well.

-  Anti-Bloat: Avoid URLs in numpy messages.

-  Code Generation: Dedicated helper function for fixed imports, that
   uses less C code for standard imports.

-  Standalone: Avoid including ``libz`` on Linux.

-  Quality: Use latest ``isort`` and ``rstchk`` versions.

****************
 Organizational
****************

-  Python3.12: Mark as unsupported for now, it does not yet compile on
   the C level again.

-  User Manual: Added description of deployment mode, this was not
   documented so far, but for some programs, dealing with them is now
   required.

-  User Manual: Improved ``--include-plugin-directory`` documentation to
   make it more clear what it is usable for and what not.

-  UI: Reject standard library paths for plugin directories given to
   ``--include-plugin-directory`` which is a frequent user error.

-  UI: When interrupting during Scons build with CTRL-C do not give a
   Nuitka call stack, there is no point in that one, rather just exit
   with a message saying the user interrupted the scons build.

-  UI: Make package data output from ``--list-package-data`` more
   understandable.

   We already had a count for DLLs too, and should not list directory
   name in case it's empty and has no data files, otherwise this can
   confuse people.

-  UI: Make the progress bar react to terminal resizes. This avoids many
   of the distortions seen in Visual Code that seems to do it a lot.

-  UI: Added a mnemonic warning for macOS architecture cross
   compilation, that it will only work as well as Python does when
   limited to that arch. Read more on `the info page
   <https://nuitka.net/info/macos-cross-compile.html>`__ for detailed
   information. Added in 1.8.4 already.

-  UI: Error exit for wrong/non-existent input files first. Otherwise
   e.g. complaints about not including anything can be given where
   project options were intended to solve that.

-  UI: Enhanced error message in case of not included ``imageio``
   plugins. Added in 1.8.4 already.

-  UI: Enhanced messages from options nanny, showing the condition that
   was not passed.

-  UI: Improved download experience. When hitting CTRL-C during a
   download, delete the incomplete file immediately, otherwise it's
   causing an error next run. Also added progress for downloads as well,
   so they do not sit there silent without a way to know how much is
   remaining.

-  UI: Also report errors happening during plugin init nicely.

-  Visual Code: Added ignore paths code spell checking. This only adds
   the most obvious things, more to come later.

-  Visual Code: Use environment for C include path configurations, and
   add one for use on macOS, this cleaned up a lot of inconsistencies in
   paths for the various existing platforms.

-  Debugging: Added experimental switch to disable free lists, so memory
   corruption issues can become easier to debug.

-  UI: Output clang and gcc versions in ``--version`` output as well.

-  UI: Add hint how to disable the warning message that asks to disable
   the console during debugging by explicit ``--enable-console`` usage.

-  UI: Do not consider aliases of options for ambiguous option error.
   Without this ``--no-progressbar`` and ``--no-progress-bar`` being
   both accepted, forced long version of options for no good reason.

-  Debugging: With ``--debug`` output failed query command that a plugin
   made. In this way it is easier to check what is wrong about it for
   the user already.

-  UI: Check if metadata included has the actual distribution package
   included. Otherwise we error out, as this would result in a
   ``RuntimeError`` when the program is attempting to use it.

-  UI: Harmonized help text quoting. We will also need that in order to
   generate the help texts for Nuitka-Action in the future. Currently
   this is not perfect yet.

-  Debugging: Added trace that allows us to see how long ``Py_Exit``
   call takes, which might be a while in some cases.

-  User Manual: Made the Nuitka requirements top level chapter.

-  User Manual: Added promise to support newer Python versions as soon
   as possible.

-  User Manual: Added section about how Linux standalone is hard and
   needs special care.

-  Python3.11: Disallow to switch to g++ for too old gcc, with this
   Python version we have to use C11.

-  Quality: Remove inconsistencies with C python hex version literals in
   auto-format, which will also make searching code easier.

-  UI: More clear error message for asking package data of a module name
   that is not a package.

**********
 Cleanups
**********

-  Dedicated node for fixed and built-in imports were added, which allow
   the general import node to be cleaner code.

-  Scons: Removed remaining ``win_target`` mode, this is long obsolete.

-  Spelling improvements by newer codespell, and generally, partially
   ported to 1.8.4 already so the Actions pass again.

-  Plugins: Move python code of ``dill-compat`` run time hook to
   separate file.

*******
 Tests
*******

-  Run the distutils tests on macOS as well, so it's made sure wheel
   creation is working there too, which it was though.

-  Avoid relative URLs in use during ``pyproject.toml`` tests, these
   fail to work on macOS at least.

-  Add GI GTK/GDK/Cairo standalone test for use with **MSYS2**.
   Eventually this should be run inside Nuitka-Watch against **MSYS2**
   on a regular basis, but it doesn't support this Python flavor yet.

-  Added test case with Chinese module names and identifiers that
   exposed issues.

-  Completed the PGO test case and actually verify it does what we want.

-  Added standalone test for setuptools. Since our anti-bloat works
   makes it not compiled with most packages, when it is, make sure it
   doesn't expose Nuitka to some sort of issue by explicitly covering
   it.

-  Show tracebacks made in report creations on GitHub Actions and during
   RPM builds.

*********
 Summary
*********

This is again massive in terms of new features supported. The lazy
loader support is very important as it allows to handle more packages in
better ways than just including everything.

The new added optimization are nice, esp. startup time will make a huge
difference for many people, but mainly the focus was on supporting
packages properly, and getting Nuitka-Watch to be able to detect
breaking of packages from PyPI closer to when it happens.

And then of course, there is a tremendous amount of improvements for the
UI, with lots features become even more rounded.

For Python 3.12 work has begun, but there is more to do for it. At this
time it's not clear how long it takes to add it. Stay tuned.
