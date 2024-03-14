:orphan:

#############################
 Nuitka Changelog before 2.0
#############################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per version changes of 1.x and comments
of old Nuitka release before version 2.0 was released.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

********************
 Nuitka Release 1.9
********************

This release has had a focus on improved startup time and compatibility
with lazy loaders which has resulted in some optimization. There are
also the usual amounts of bug fixes. For macOS and Linux there are lots
of improvements that should make standalone mode for them robust with
many more configurations.

Bug Fixes
=========

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
   prefix, as it might be unicode path as well. Fixed in 1.8.4 already.

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

New Features
============

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

Optimization
============

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

Organisational
==============

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

Cleanups
========

-  Dedicated node for fixed and built-in imports were added, which allow
   the general import node to be cleaner code.

-  Scons: Removed remaining ``win_target`` mode, this is long obsolete.

-  Spelling improvements by newer codespell, and generally, partially
   ported to 1.8.4 already so the Actions pass again.

-  Plugins: Move python code of ``dill-compat`` run time hook to
   separate file.

Tests
=====

-  Run the distutils tests on macOS as well, so it's made sure wheel
   creation is working there too, which it was though.

-  Avoid relative URLs in use during ``pyproject.toml`` tests, these
   fail to work on macOS at least.

-  Add GI GTK/GDK/Cairo standalone test for use with MSYS2. Eventually
   this should be run inside Nuitka-Watch against MSYS2 on a regular
   basis, but it doesn't support this Python flavor yet.

-  Added test case with Chinese module names and identifiers that
   exposed issues.

-  Completed the PGO test case and actually verify it does what we want.

-  Added standalone test for setuptools. Since our anti-bloat works
   makes it not compiled with most packages, when it is, make sure it
   doesn't expose Nuitka to some sort of issue by explicitly covering
   it.

-  Show tracebacks made in report creations on GitHub Actions and during
   RPM builds.

Summary
=======

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

********************
 Nuitka Release 1.8
********************

Bug Fixes
=========

-  Standalone: Added support for ``opentelemetry`` package. Added in
   1.7.1 already.

-  Reports: Fix, do not report plugin influence when there are not
   ``no-auto-follow`` in an anti-bloat section. Fixed in 1.7.2 already.

-  Anti-Bloat: Add missing usage tag ``use_pytest`` for anti-bloat
   changes that remove ``pytest`` related codes. Fixed in 1.7.2 already.

-  Standalone: Added support for newer ``jsonschema`` package. Fixed in
   1.7.2 already.

-  Standalone: Fix, our ``iterdir`` implementation was crashing in
   ``files`` for packages that don't actually have a directory for data
   files to live in. Fixed in 1.7.2 already.

-  Fix, parent package imports could pick the wrong name internally and
   then collide with sub-packages of that package during collision.
   Fixed in 1.7.3 already.

-  Standalone: Added support for ``pymssql`` package. Fixed in 1.7.3
   already.

-  Standalone: Added support for ``cvxpy`` package. Fixed in 1.7.4
   already.

-  Standalone: Added missing dependencies of ``lib2to3.refactor``. Fixed
   in 1.7.4 already.

-  Standalone: Fix, data files for ``lib2to3.pgen`` were regressed.
   Fixed in 1.7.4 already.

-  Standalone: Added missing dependency of ``cairo`` package. Fixed in
   1.7.4 already.

-  Standalone: Added support for new ``trio`` package. Fixed in 1.7.4
   already.

-  Standalone: Added support for ``markdown`` package. Fixed in 1.7.4
   already.

-  Standalone: Added support to ``eventlet`` package. Fixed in 1.7.4
   already.

-  Standalone: Added support for more newer ``sklearn`` package. Fixed
   in 1.7.5 already.

-  Standalone: Added support for more newer ``skimage`` package. Fixed
   in 1.7.5 already.

-  Standalone: Added support for more newer ``transformers`` package.
   Fixed in 1.7.5 already.

-  Standalone: Added support for ``torch_scatter`` package. Fixed in
   1.7.6 already.

-  Standalone: Added missing DLL for ``wx.html2`` to work well on
   Windows. Fixed in 1.7.6 already.

-  Fix, the ``@pyqtSlot`` decoration could crash the compilation and was
   effective even if no pyqt plugin was active. Fixed in 1.7.6 already.

-  Python3.11: Fix, need to support ``BaseExceptionGroup`` for code
   generation too, otherwise the ``exceptiongroup`` backport was not
   working. Fixed in 1.7.7 already.

-  MSYS2: Fix usage of deprecated ``sysconfig`` variable with mingw.
   After their switch to Python 3.11, it is no longer available. Fixed
   in 1.7.7 already.

-  Distutils: Do not compile empty directories found in package scan as
   namespaces. Fixed in 1.7.7 already.

-  Python3.7+: Fix, need to follow dict internal structure more
   correctly, otherwise we over-allocate and copy more data than
   necessary. Fixed in 1.7.7 already.

-  Python3.8: Fix, the new pyqt plugin workaround requires 3.9 or higher
   and could causes compile time crashes with the ``@pyqtSlot``
   decorator. Fixed in 1.7.7 already.

-  Modules: Fix, the ``.pyi`` file created was using default encoding
   which can vary and potentially even crash on other systems. Enforcing
   ``utf-8`` now. Fixed in 1.7.8 already.

-  Fix, only failed relative imports should become package relative.
   This was giving wrong names for attempts imports in these cases.
   Mostly only affected dependency caching correctness and reporting at
   this time. Fixed in 1.7.8 already.

-  Standalone: Added missing metadata dependencies for ``transformers``
   package. Fixed in 1.7.9 already, but more added for release.

-  Fix, need to ignore folders that cannot be module names in stdlib.
   Could e.g. crash when encountering folders like ``.idea`` which
   cannot be module names. Fixed in 1.7.9 already.

-  Standalone: Added data files for ``langchain`` package. Fixed in
   1.7.10 already.

-  Fix, forced output paths didn't work without C11 mode. This mainly
   affected older MSVC users, with newer MSVC and good enough Windows
   SDK, it's not using C++ anymore. Fixed in 1.7.10 already.

-  Fix, was using int values for boolean returns, something that was
   giving warnings with at least older MSVC not in C11 mode. Fixed in
   1.7.10 already.

-  Fix, failed hard name imports could crash with segfault trying to
   release their value. Fixed in 1.7.10 already.

-  Standalone: Added missing implicit dependency for ``xml.sax`` in
   stdlib. Fixed in 1.7.10 already.

-  Windows: Fix, ``--mingw64`` mode was not working if MSVC was
   installed, but not acceptable for use. Fixed in 1.7.10 already.

-  Standalone: Fix, ``onnxruntime`` had too few DLLs included. Fixed in
   1.7.10 already.

-  Standalone: Added support for ``moviepy``. Fixed in 1.7.10 already.

-  Python3.10+: Fix, matching empty sequences was not considering
   length, leading to incorrect code execution for that case.

   .. code:: python

      match x:
         case []:
               ... # non-empty sequences matched here

-  UI: Fix, some error outputs didn't work nicely with progress bars,
   need to use our own print function that temporarily disables them or
   else outputs get corrupted.

-  Linux: Sync output for data composer. This is to avoid race
   conditions that we might have been seeing occasionally.

-  Compatibility: Fix, the ``sys.flags.optimize`` value for
   ``--python-flag=-OO`` didn't match what Python does.

-  Standalone: Fix, packages have no ``__file__`` if imported from
   frozen, these was causing issues for some packages that scan all
   modules and expect those to be there.

-  Fix, the ``dict`` built-in could crash if its argument self-destructs
   during usage.

-  Fix, the ``PySide2/PySide6`` workaround for connecting compiled class
   methods without crashing were not handling its optional ``type``
   argument.

-  Enhanced non-commercial PySide2 support by adding yet another class
   to be hooked. This was ironically contributed by a commercial user.

-  Standalone: Added support for newer ``delvewheel`` version as used in
   newest ``scipy`` and probably more packages in the future.

-  Compatibility: The ``pkgutil.iter_modules`` function now works
   without importing the module first. The makes ``Faker`` work on
   Windows as well.

-  Reports: Detect top level packages even with broken packaging. Some
   packages will not reveal through installed files or top level what
   package they are for, and as a result, they cannot be uninstalled,
   but we need to still be able guess what package they are responsible
   for, so we go by their PyPI name, which works for ``tensorflow``.

-  Compatibility: More robust way of allowing iteration of compiled
   packages via file path.

   Rather than pre-populating the cache, we should provide the hook
   function to check if we are responsible for a given path. With this,
   the ``Faker`` package works on Windows as well now, and probably
   other packages benefit too. This then works on paths rather than
   strings, which due to short paths, etc. can be non-unique on Windows
   easily.

-  Standalone: Added support for the ``opencc`` package.

-  Compatibility: Fix, import name resolving done for things like
   ``six`` and others should be done as soon as possible, and not just
   during optimization, or else some imports can become just wrong as a
   result.

-  Python3.11: Added support for the new ``closure`` keyword only
   argument in ``exec`` built-in.

-  Standalone: Added support for ``pythonnet`` on Linux as well.

-  Debian: Fix, do not give false alarms for root pip installed
   packages, they get a similar path component, but are not actually
   Debian packages of course, this was mostly affecting builds inside
   containers of course.

-  Compatibility: Added support for comparing results from our resource
   reader file interfaces. This is needed for when people want to e.g.
   sort the the file list.

-  Python3.6+: Fix, didn't catch ``await`` on module level as a syntax
   error.

-  Compatibility: Added support for ``joblib`` with ``loky`` backend as
   well.

-  Standalone: Added support for newer ``chromadb`` adding missing
   dependencies and data files.

-  Python3.9+: Fix, ``importlib.resources.files()`` was not fully
   compatible

   Need to provide basename for ``.name`` attribute rather than an
   absolute path. And in some cases, a leading trailing slashes was
   produced for the full path, which caused trouble for file iteration
   of filenames.

-  Standalone: Added support for newer ``importlib_resources`` as well.
   We now need to expose the ``files`` functionality even before Python
   3.9 for this to be possible.

-  Standalone: Added support for newer ``rapidfuzz`` package.

-  Added support for newer ``PyOpenGL`` package.

New Features
============

-  Plugins: Added support to specify embedding of metadata for given
   packages via the package configuration. With this, entry points,
   version, etc. can even be resolved if not currently possible at
   compile time to so through the code with static optimization. Added
   in 1.7.1 already.

   .. code:: yaml

      - module-name: 'opentelemetry.propagate'
        data-files:
          include-metadata:
            - 'opentelemetry-api'

-  Distutils: Add PEP 660 editable install support. With this ``pdm``
   can be used for building wheels with Nuitka compilation. Added in
   1.7.8 already.

-  Haiku: Added support for accelerated mode, standalone will need more
   work, also recognize its form of the ``site-packages`` folder, named
   ``vendor-packages``.

-  Disable misleading initial import exception handling in ``numpy``,
   all what it says detracts only.

-  Added python flags given for ``no_asserts``, ``no_docstrings`` and
   ``no_annotations`` to the ``__compiled__`` attribute values of
   modules and functions to fully expose the information.

-  Watch: Added capability to specify what ``nuitka`` binary to use in
   ``nuitka-watch`` so we can use enhanced ``nuitka-watch`` from develop
   branch with older versions of Nuitka with no issues.

-  Watch: Now evaluates the minimum version needed for Nuitka, and skips
   test cases, allowing ``nuitka-watch`` to be run with versions that do
   not yet handle cases that e.g. develop already can, i.e. next Nuitka
   version.

-  Watch: Now evaluates if a compilation with Nuitka needs to be done at
   all, as it's only necessary if the PyPI config changed, or if Nuitka
   version changed.

-  Reports: Added source path for modules, so it's easier to tell where
   something came from, and esp. in case of bugs in the import location
   of Nuitka.

-  Reports: In case of a crash, always write report file for use in bug
   reporting. This is now done even if no report was asked for.

-  Reports: Include error exit message from Nuitka in case of explicit
   exits.

-  UI: Added new ``--deployment`` and ``--no-deployment-flag`` that
   disables certain debugging helpers.

   Right now, we use this to control a hook that prevents execution of
   itself with ``-c`` which is used by e.g. ``joblib`` and that
   potentially can turns Nuitka created programs into a fork bombs, when
   they use ``sys.executable -c ...``. This can be disabled with
   ``--no-deployment-flag=self-execution`` or ``--deployment``.

   The plan is to expand this to cover ``FileNotFoundError`` and similar
   exception exits pointing to compilation issues with helpful more
   annotations.

-  Catch attempts to exec compiled function bytecodes.

   This segfaults otherwise with at least Python3.11 and is probably a
   good idea to catch for all versions, as it doesn't do anything.

-  Windows: Remove unnecessary ``.\`` in CMD files generated, these will
   otherwise show up in ``sys.argv[0]`` too, making them more ugly than
   necessary.

-  Scons: Also respect ``CFLAGS`` setting. It's rarely used, but for
   completeness sake we should have that too. The effects are the same
   as ``CCFLAGS`` it seems.

Optimization
============

-  Added type shape for built-in hash operation, these must indeed be of
   ``int`` type either way.

-  Anti-Bloat: Avoid using ``unittest`` in ``future`` and
   ``multiprocessing`` package. Added in 1.7.3 already.

-  Anti-Bloat: Avoid using ``unittest`` in ``git`` package. Added in
   1.7.3 already.

-  Anti-Bloat: Avoid ``IPython`` in ``streamlit`` package.

-  Standalone: Make ``transformers`` work with ``no_docstrings`` mode.
   Added in 1.7.7 already.

-  Anti-Bloat: Avoid more ``IPython`` usage in ``transformers`` package.

-  Anti-Bloat: Avoid using ``pytest`` in ``polyfactory`` package.

-  Anti-Bloat: Expand the list of modules that are in the ``unittest``
   group by the ones Python provides itself, ``test.support``,
   ``test.test_support`` and ``future.moves.test.support``, so the
   culprits are more easily recognizable.

-  Anti-Bloat: Treat ``ipykernel`` and ``jupyter_client`` as equal to
   IPython for usage, so the bloat warning about IPython becomes more
   meaningful in that case too.

-  Anti-Bloat: Avoid using ``IPython`` in ``plumbum`` package.

-  Statically optimize the value of ``sys.byteorder`` as well.

-  Anti-Bloat: Added ``no-auto-follow`` for ``tornado`` in ``joblib``
   package. The user is informed of that happening if nothing else
   imports tornado in case he wants to enable it.

-  Standalone: Avoid including standard library ``zipapp`` or
   ``calendar`` automatically and remove their runners through
   ``anti-bloat`` configuration. This got rid of ``argparse`` for hello
   world compilation.

-  Standalone: Do not auto include standard library ``json.tool`` which
   is a binary only.

-  Standalone: Avoid automatic inclusion a ``_json`` extension module
   for the ``json`` module and do not automatically include it as part
   of stdlib anymore, this can reduce the size of standalone
   distributions.

-  Standalone: Avoid the standard library ``audioop`` extension module
   by making all audio related modules non-automatically included.

-  Standalone: Avoid the ``_contextvars`` standard library extension
   module. Explicit and implicit imports of ``contextvar`` module will
   continue to work and hopefully give proper errors until we do
   ourselves raise such errors.

-  Standalone: Avoid also the "_crypt" standard library extension
   module, and make the ``crypt`` module raise an error where we modify
   the message to not be as misleading.

-  Standalone: On macOS we also saw ``_bisect``, ``_opcode`` and more
   modules that are optional extension modules, that we no longer do
   automatically use if they are that way.

-  Standalone: Added more modules like ``mailbox``, ``grp``, etc. to
   exclusion from standard library when they trigger dependencies on
   other things, or are an extension themselves.

-  Anti-Bloat: Avoid using ``sqlalchmy.testing`` and therefore
   ``pytest`` in ``sqlalchemy`` package. Also added that testing package
   to be treated as using ``pytest``. Added in 1.7.10 already.

-  Anti-Bloat: Avoid IPython in ``distributed`` package. Added in 1.7.10
   already.

-  Anti-Bloat: Avoid ``dask`` usage in ``skimage``. Added in 1.7.10
   already.

-  Anti-Bloat: More changes needed for newer ``sympy`` to avoid
   ``IPython``. Added in 1.7.10 already.

-  Anti-Bloat: Enhanced handling of ``PIL.ImageQt`` even without the Qt
   binding plugins being active.

-  Anti-Bloat: Do not automatically follow ``matplotlib`` from ``scipy``
   as that is code that will only be used if other code using it exists
   too.

-  Anti-Bloat: Avoid ``pandas`` and ``matplotlib`` for ``sklearn``
   package. Availability checks of third party packages should be
   counted as real usage.

-  Anti-Bloat: Avoid ``IPython`` in newer ``keras`` module too.

-  Anti-Bloat: Updated for newer ``tensorflow`` package, also using more
   robust new form of ``no-auto-follow`` to achieve that.

-  Anti-Bloat: Avoid using Qt bindings for ``pandas.io.clipboard`` as
   it's only useful if one of our Qt plugins is active.

Organisational
==============

-  User Manual: Make it clear in the example that renaming created
   extension modules to change their name does not work, such that the
   user has to first rename the Python module properly.

-  macOS: Pronounce Homebrew as somewhat support but not recommended due
   to its limited results for portability.

-  UI: Added mnemonic for unsupported Windows store Python, so we have a
   place to give more information. Read more on `the info page
   <https://nuitka.net/info/unsupported-windows-app-store-python.html>`__
   for detailed information.

-  UI: Disable warning for ``numpy``/``scipy`` DLL non-identity
   conflicts. These are very common unfortunately and known to be
   harmless.

-  Stop creating PDFs for release. They are not really needed, but cause
   extra effort that makes no sense.

-  Quality: Updated to latest black which removes some leading new lines
   in blocks, changing a bunch of files. Bumped development requirements
   file Python version to 3.8, since black won't do 3.7 anymore.

-  Quality: Updated to latest PyLint, no changes from that.

-  Quality: Auto-format the markdown files used for GitHub templates as
   well.

-  Debugging: Catch errors during data composer phase cleaner. Added in
   1.7.1 already.

-  Plugins: More clear error messages for Yaml files checker. Added in
   1.7.5 already.

-  Release: Avoid DNS lookup by container, these sometimes failed.

-  UI: Catch user error of compiling in module mode with unknown file
   kinds, it needs to be Python code of course.

-  UI: In case of ``SyntaxError`` in main file, always suggest latest
   supported version. Previous it was toggling between Python2 and
   Python3, but that's no longer the main reason this happens.

-  UI: Fix typo in help output for ``--trademarks`` option. Added in
   1.7.8 already.

-  UI: Fix, need to enforce version information completeness only on
   Windows, other platforms can be more forgiving. Added in 1.7.8
   already.

-  Visual Code: Enable black formatter as default for Python.

-  UI: Disallow ``--follow-stdlib`` with ``--standalone`` mode. This is
   now the default, and just generally makes no sense anymore.

-  Plugins: Warn if Qt qml plugins are not included, but qml files are.
   This has been a trap for first time users for a while now, that now
   have a way of knowing that they need to enable that Qt plugin
   feature.

-  Plugins: Enhanced Qt binding plugins selection by the various qt
   plugins

   Now can also ask to not include specified plugins with
   ``--noinclude-qt-plugins`` and by now include ``sensible`` by
   default, with the ``--include-qt-plugins=qml`` line not replacing it,
   but rather extending it. That makes it easier to handle and catches a
   common trap, where users would only specify the missing plugin, but
   remove required plugins like ``platform`` making it stop to work.

-  Plugins: Allow plugins provide ``None`` for flags not just by return
   value length, but also an explicit value, so plugin code can make a
   difference in a consistent way.

-  UI: Lets have the ``options-nanny`` output the failed condition, so
   it's more clear what the issue is.

-  Quality: Unified spell checker markers to same form in all files
   through auto-format for more consistency.

-  Quality: Always avoid attempting to format executables, much like we
   already do for bytecode, otherwise some attempts on them can crash.

-  Windows: Only change directory to short path during execution of
   Scons, we are otherwise leaking it to ``--run`` execution in tests,
   giving their output comparison a harder time than necessary.

-  Scons: Use report paths for outputs of filenames in slow compilation
   messages as well.

-  WinPython: Adapted detection of this flavor to changes made in that
   project.

Cleanups
========

-  Major Cleanup, do not treat technical modules special anymore

   Previously the immediate demotion of standard library to bytecode is
   not really needed and prevented dependency analysis. We have had
   plenty issues with that ever since not all stdlib modules were
   automatic anymore, there was a risk of missing some of them, just
   because this analysis was not done.

   Moved the import detection code to a dedicated module cleaning up the
   size of the standalone mechanics, as it also is not exclusive to it.

   Adding "reasons" to modules, different from "decision reasons" why
   something was allowed to be included, these give the technical reason
   why something is added. This is needed for anti-bloat to be able to
   ignore stdlib being added only for being frozen.

   Now we are correctly annotating why an extension module was included,
   e.g. is it technical or not, that solves a TODO we had.

   Removes a lot of code duplication for reading source and bytecode of
   modules and the separate handling of uncompiled modules as a category
   in the module registry is no more necessary.

   The detection logic for technical modules itself was apparently not
   robust and had bugs to be fixed that became visible now, and that
   make it unclear how it ever worked as well.

-  Refactor towards unification of statement and expression.

   Make sure Make existing statement operations, i.e. use the function
   intended for them so they are immediately closer to what expressions
   do, and don't visit their own children themselves anymore.

   Remove checks for expression or statement, we won't use that anymore,
   and it's only costing performance until we merge them.

-  The caching (currently only used when demoting to bytecode), was not
   keeping track of distributions attempted to be used, but then being
   not found. That could have led to errors when using the cached
   result.

-  Again some more spelling fixes in code were identified and fixed.

-  Removed now unused user provided flag from uncompiled module nodes.

-  Removed 3.3 support from test runner as well.

-  Avoid potential slur word from one of the tests.

Tests
=====

-  Sometimes the pickle from cached CPython executions cannot be read
   due to protocol version differences, then of course it's also not
   usable.

-  Added CPython311 test suite, but it is not yet completely integrated.

-  Tests: Salvage one test for ``dateutil`` from a GSoC 2019 PR, we can
   use that.

Summary
=======

This is massive in terms of new features supported. The deployment mode
being added, provides us with a framework to make new user experience
with e.g. the missing data files, much more generous and help them by
pointing to the right solution.

The technical debt of immediate bytecode demotion being removed, is huge
for reliability of Nuitka. We now really only have to deal with actual
hidden dependencies in stdlib, and not just ones caused by us trying to
exclude parts of it and missing internal dependencies.

********************
 Nuitka Release 1.7
********************

There release is focused on adding plenty of new features in Nuitka,
with the new isolated mode for standalone being headliners, but there
are beginnings for including functions as not compiled, and really a lot
of new anti-bloat new features for improved handling, and improving user
interaction.

Also many packages were improved specifically to use less unnecessary
stuff, some of which are commonly used. For some things, e.g. avoiding
tkinter, this got also down to polishing modules that have GUI plugins
to avoid those if another GUI toolkit is used.

In terms of bug fixes, it's also a lot, and macOS got again a lot of
improvements that solve issues in our dependency detection. But also a
long standing corruption for code generation of cell variables of
contractions in loops has finally been solved.

Bug Fixes
=========

-  Python3.11: The MSVC compiler for Windows will not work before 14.3
   (Visual Studio 2022) if used in conjunction with Python 3.11, point
   it out to the user an ignore older versions. Fixed in 1.6.1 already.

-  Standalone: Added support for the ``pint`` package. Fixed in 1.6.1
   already.

-  Standalone: Added missing standard library dependency for
   ``statistics``. Fixed in 1.6.1 already.

-  Compatibility: Fix, the ``transformers`` auto models were copying
   invalid bytecode from compiled functions. Added workaround to use
   compiled function ``.clone()`` method. Fixed in 1.6.1 already.

-  Compatibility: Added workaround for ``scipy.optimize.cobyla``
   package. Fixed in 1.6.1 already.

-  Anaconda: Detect Anaconda package from ``conda install`` vs. PyPI
   package from ``pip install``, the specifics should only be applied to
   those. Adapted our configurations to make the difference. Fixed in
   1.6.1 already.

-  Anaconda: Do not search DLLs for newer ``shapely`` versions. Fixed in
   1.6.1 already.

-  Standalone: Add new implicit dependencies for ``pycrytodome.ECC``
   module. Fixed in 1.6.1 already.

-  Standalone: Fix ``tls_client`` for Linux by not non-Linux DLLs. Fixed
   in 1.6.1 already.

-  MacOS: When using ``--macos-app-name``, the executable name of a
   bundle could become wrong and prevent the launch of the program. Now
   uses the actual executable name. Fixed in 1.6.1 already.

-  Multidist: The docs didn't properly state the option name to use
   which is ``--main`` and also it didn't show up in help output. Fixed
   in 1.6.2 already.

-  Standalone: Added support for ``polars`` package. Fixed in 1.6.3
   already.

-  Standalone: Added implicit imports for ``apscheduler`` triggers.
   Fixed in 1.6.3 already.

-  Standalone: Add data files to AXML parser packages. Added in 1.6.4
   already.

-  Fix, ``exec`` nodes didn't annotate their exception exit. Fixed in
   1.6.4 already.

-  Standalone: Added data files for ``open_clip`` package. Fixed in
   1.6.4 already.

-  Standalone: Avoid data files warning with old ``pendulum`` package.
   Fixed in 1.6.4 already.

-  Standalone: Added implicit dependencies for ``faker`` module. Fixed
   in 1.6.4 already.

-  Added workaround for ``opentele`` exception raising trying to look at
   the exception frame before its raised. Fixed in 1.6.4 already.

-  Nuitka-Python: Do not check for unknown built-in modules. Fixed in
   1.6.4 already.

-  Scons: Fix, the total ``ccache`` file number given could be wrong.
   Ignored messages were counted still as compiled, leading to larger
   sum of files than actually there was. Fixed in 1.6.5 already.

-  Fix, multiprocessing resource tracker was not properly initialized.
   On at least macOS this was causing it to work relatively badly,
   because it could fail to actually use it. Fixed in 1.6.5 already.

-  Standalone: Added support for ``cassandra-driver`` package. Fixed in
   1.6.5 already.

-  Onefile: Have Python process suicide when bootstrap surprisingly
   died, respecting the provided grace time for shutdown. Fixed in 1.6.5
   already.

-  Plugins: Fix, package versions for at least Ubuntu packages can be
   broken, such that at least ``pkg_resources`` rejects them. Handle
   that and use fallback to next version detection method. Fixed in
   1.6.5 already.

-  Onefile: Handle ``SIGTERM`` and ``SIGQUIT`` just like ``SIGINT`` on
   non-Windows. The Python code with see ``KeyboardInterrupt`` for all 3
   signals, so it's easier to implement. Previously onefile would exit
   without cleanup being performed. Fixed in 1.6.5 already.

-  Standalone: Fix, need to add more implicit dependencies for
   ``pydantic`` because we do no longer include e.g. ``decimal`` and
   ``uuid`` automatically.

-  Standalone: Added missing implicit dependencies for ``fiona``
   package. Added in 1.6.6 already.

-  Standalone: Added missing implicit dependencies for ``rasterio``
   package. Added in 1.6.6 already.

-  Standalone: Fix, need to add more implicit dependencies for
   ``pydantic``. Added in 1.6.6 already.

-  Fix, the data composer used a signed value for encoding constant blob
   sizes, limiting it needlessly to half the size possible.

-  Windows: Avoid dependency on API not available on all versions,
   specifically Windows 7 didn't work anymore. With this, symlinks are
   only resolved where they actually exist, and MinGW64 does it too now.

-  Standalone: Added support for ``.location`` attribute for
   ``pkg_resources`` distribution objects.

-  Anti-Bloat: Avoid using ``dask`` and ``numba`` in the ``tsfresh``
   package.

-  Fix, outline cell variables must be re-initialized on entry. The code
   would be crashing for for outlines used in a loop, since the cleanup
   code for these cell variables would release the cell that was created
   during containing scope setup.

-  Standalone: Added missing dependency of ``pygeos`` package.

-  Standalone: Added ``sqlalchemy`` implicit dependency.

-  Standalone: Added data files for ``mnemonic`` package.

-  Fix, attribute checks could cause corruption when used on objects
   that raise exceptions during ``__getattr__``.

-  Python2: Fix, wasn't making sure instance attribute lookups were
   actually only done with ``str`` attributes.

-  macOS: Fix, need to allow versioned DLL dependency from un-versioned
   DLLs packaged.

-  Standalone: Added DLLs for ``rtree`` package.

-  Standalone: Added support for newer ``skimage`` package.

-  Standalone: Added support for newer ``matplotlib`` package.

-  Standalone: Fix, our ``numpy.testing`` replacement, was lacking a
   function ``assert_array_almost_equal`` used in at least the
   ``pytransform3d`` package.

New Features
============

-  Added support for ``--python-flag=isolated`` mode. In this mode,
   packages are not expandable via environment variable provided paths
   and ``sys.path`` is emptied which makes imports from the file system
   not work.

-  The options for forcing outputs were renamed to
   ``--force-stdout-spec`` and ``force-stderr-spec`` to force output to
   files and now work on non-Windows as well. They kind of were before,
   but e.g. ``%PROGRAM%`` was not implemented for all OSes yet.

-  Capturing of all outputs now extends beyond the Python level outputs
   is now attempting to capture C level outputs as well. These can be
   traces of Nuitka itself, but also messages from C libraries. On
   Windows, with MinGW64 this does not work, and it still only captures
   MinGW64, due to limitations of using different C run-times. With MSVC
   it works for the compiled program and C, but DLLs can have their own
   C runtime outputs that are still not caught.

-  Added new spec value ``%PROGRAM_BASE%`` which will avoid the suffix
   ``.exe`` or ``.bin`` of binaries that ``%PROGRAM%`` will still give.

-  Plugins: Added ability to query if a package in an Anaconda package
   or not, with the new ``is_conda_package()`` function in Nuitka
   package configuration. Added in 1.6.1 already.

-  Plugins: Provide control tags during plugin startup with new
   interface, such that these become globally visible.

-  Plugins: Allow to give ``--include-qt-plugins`` options of Qt binding
   plugins to be given multiple times. This is for consistency with
   other options. These now expand the list of plugins rather than
   replacing it.

-  Added experimental code to include functions decorated in certain
   ways to be included as bytecode. Prepare the inclusion as source code
   in a similar fashion. This was used to make example PyQt5 code work
   properly with timers where it doesn't normally work, but is still in
   development before it will be generally useful. For that it reacts to
   ``@pyqtSlot`` decorators.

-  Plugins: Make anti-bloat not warn when bloating modules include their
   group. This helps when e.g. ``distributed`` is going to use ``dask``,
   then we warn about ``distributed``, but not anymore, when that then
   uses ``dask``. And that intention to avoid ``dask`` is now in the
   warning given for ``distributed``.

-  Plugins: Added ability to decide module inclusion based on using
   module name and not only the used name. This will be super useful to
   make some imports not count per se for inclusion.

-  Plugins: Added new ``no-auto-follow`` Yaml configuration for
   ``anti-bloat``, that makes imports from one module not automatically
   included. That can make optional import removal much easier.

-  Plugins: Added new function for when clauses, such that it now can be
   tested if this Python version has a certain built-in name, e.g.
   ``when: 'not has_builtin_module("_socket")'`` will not apply
   configuration ``_socket`` is an extension module rather than
   built-in. This can be used to avoid unnecessary changes.

Optimization
============

-  Optimization: Better ``hasattr`` handling. Added ability for
   generated expression base class to monitor the attribute name for
   becoming constant and then calling a new abstract method due to
   ``auto_compute_handling`` saying ``wait_constant:name``.

-  Optimization: Added type shapes for ``setattr`` and ``hasattr``
   built-ins as well as the attribute check node for better code
   generation.

-  Optimization: Added dedicated nodes for ``importlib.resources.files``
   to allow including the used package automatically.

-  Standalone: Include only platform DLLs for ``tls_client`` rather than
   all DLLs for all platforms. Added in 1.6.1 already.

-  Anti-Bloat: Avoid including ``sympy.testing`` for ``sympy`` package.
   Added in 1.6.3 already.

-  Anti-Bloat: Avoid ``IPython`` in ``transformers`` package. Added in
   1.6.3 already.

-  Anti-Bloat: Avoid ``transformers.testing_util`` inclusion for
   ``transformers`` package as it will trigger ``pytest`` inclusion.

-  Anti-Bloat: Added missing method to our ``numpy.testing`` stub, so it
   can be used with more packages. Added in 1.6.4 already.

-  Anti-Bloat: Avoid ``numba`` usage from parts of ``pandas``. Added in
   1.6.4 already.

-  Anti-Bloat: Avoid ``pytest`` usage in ``patsy`` more completely.
   Added in 1.6.4 already.

-  Standalone: Added data files needed for ``pycountry`` package. Added
   in 1.6.4 already.

-  Anti-Bloat: Avoid ``unittest`` usage in ``numpy`` package. Added in
   1.6.4 already.

-  Anti-Bloat: Avoid using ``pytest`` in ``statsmodels`` package. Added
   in 1.6.4 already.

-  Anti-Bloat: Avoid including ``PIL.ImageQt`` when ``no-qt`` plugin is
   used. Added in 1.6.4 already.

-  Anti-Bloat: Avoid ``IPython`` usage in ``dask``. We do not cover
   bloat with ``dask`` allowed well yet, more like this should be added.
   Added in 1.6.5 already.

-  Anti-Bloat: Avoid ``dask`` via ``distributed`` in ``fsspec`` package.
   Added in 1.6.5 already.

-  Anti-Bloat: Avoid ``IPython`` in ``patsy`` package. Added in 1.6.5
   already.

-  Anti-Bloat: Avoid ``setuptools`` in newer ``torch`` as well. Added in
   1.6.5 already.

-  Anti-Bloat: Avoid ``tkinter`` inclusion in ``PIL`` and ``matplotlib``
   if another GUI plugin is active. This is using the control tags made
   available by GUI plugins.

-  Anti-Bloat: Avoid warning for ``from unittest import mock`` imports.
   These are common, and not considered actual usage of ``unittest``
   anymore.

-  Anti-Bloat: Avoid ``pandas`` usage in ``tqdm``. This uses the new
   ``no-auto-follow`` feature that will enable the optional integration
   of ``tqdm`` if pandas is included by other means only.

-  Anti-Bloat: Better method of avoiding ``socket`` in ``email.utils``.
   With changing the source code to delay the import of ``socket`` to
   the only function using it. Socket is now included only if used
   elsewhere. These changes however, are only done if ``_socket`` if is
   not a built-in module, because only then they really matters. And
   using a simple ``--include-module=socket`` will restore this. This
   approach is more robust and less invasive.

Organisational
==============

-  Added ``run-inside-nuitka-container`` for use in CI scripts. With
   this, dependencies of package building and testing from correct
   system installation should go away.

-  Release: Add CI container for use with
   ``run-inside-nuitka-container`` to make Debian package releases. This
   provides a more stable and flexible environment rather than building
   through ansible maintained environments, since different branches can
   more easily use different versions, or new features for the container
   handling.

-  Release: Use upload tokens rather than PyPI password in uploads, and
   secure the account with 2FA.

-  UI: Avoid duplicate warnings for ``anti-bloat`` detected imports. In
   case of ``from unittest import mock`` there were 2 warnings given,
   for ``unittest`` and ``unittest.mock`` but that is superfluous.

-  macOS: More beginner friendly version of Apple Python standalone
   error. They won't know why it is, and where to get a working Python
   version, so we explain more and added a download link.

-  Scons: Consider only 5 minutes slow for a module compilation in
   backend. Many machines are busy or slow by nature, so don't warn that
   much.

-  GitHub: Actions no longer work (easily) with Python2, so we removed
   those and need to test it elsewhere.

-  UI: Output the filename of the XML node dump from ``--xml`` as well.

-  UI: Make ``--edit-module-code`` work with onefile outputs as well.

-  Debugging: Allow yaml condition traceback to go through in
   ``--debug`` mode, so exception causes are visible.

-  Plugins: Make more clear what is the forbidden module user, such that
   it is possible to debug it.

-  UI: Inform user about slow linking, and ``--lto=no`` choice in case
   ``auto`` was used. This should make this option more obvious for new
   users that somehow victim of not defaulting to ``no``, but still
   having a slow link.

-  Debugging: Include PDBs for DLLs in unstripped mode already.
   Previously this was only done for debug mode, but that's a bit high
   of a requirement, and we sometimes need to debug where things do not
   happen in debug mode.

-  User Manual: Added typical problem with ``python -m compiled_module``
   execution not working and why that is so.

-  Debian: Do not include PDF files in packages. These are probably not
   used that much, but they cause issues at times, that are likely not
   worth the effort.

Cleanups
========

-  Moved OS error reporting as done in onefile binary to common code for
   easier reuse in plugins.

-  Moved helper codes for expanding paths and for getting the path to
   the running executable to file path common code for clearer code
   structure.

-  Removed ``x-bits`` from files that do not need them. For ``__main__``
   files, they are not needed, and for some files they were outright
   wrong.

-  Python3.12: Avoid usage of ``distutils.utils`` which were using to
   disable bytecode compilation for things we expect to not work.

-  Solve TODO and use more modern git command ``git branch
   --show-current`` to detect branch, our CI will have this for sure.

-  In our Yaml configuration prefer the GUI toolkit control tags, e.g.
   ``use_pyside6`` over the ``plugin("pyside6")`` method.

Tests
=====

-  Release: Use CI container for linter checks, so different branches
   can use different versions with less pain involved.

-  macOS: Allow all system library frameworks to be used, not just a few
   selected ones, there is many of them and they should all exist on
   every system. Added in 1.6.1 already.

-  Made the ``pendulum`` test actually useful to cover new and old
   pendulum actually working properly.

Summary
=======

This release really polished ``anti-bloat`` to the point where we now
have all the tools needed. Also ``torch`` in newest version is now
working nicely again with it, and a few rough edges of what we did with
1.6 for not including extension modules were removed. This polishing
will go on, but has reached really high levels. More and more people are
capable of helping with PRs here.

The optimization work outside of ``anti-bloat`` was really minor, with
only the two attribute built-in nodes being worked on, and only
``hasattr`` seeing real improvements. However, this was more of a
structural thing. The ``wait_constant`` technique will not get applied
more often, but it also will need a ``wait_all_constant`` companion,
before we can expect scalability improvements.

Restoring Windows 7 is important to many people deploying to old
systems, and the like.

However, in the coming release, we need to attack loop tracing. The only
bugs currently remaining are related to wrong tracing of items, and it
also is a limitation for hard imports to work. So scalability from doing
more of the ``wait_constant`` work, and from more clever loop tracing
shall be the focus of the 1.8 release.

********************
 Nuitka Release 1.6
********************

This release bumps the much awaited 3.11 support to full level. This
means Nuitka is now expected to behave identical to CPython3.11 for the
largest part.

There is plenty of new features in Nuitka, e.g. a new testing approach
with reproducible compilation reports, support for including the
metadata if an distribution, and more.

In terms of bug fixes, it's also huge, and esp. macOS got a lot of
improvements that solve issues with prominent packages in our dependency
detection. And then for PySide we found a corruption issue, that got
workarounds.

Bug Fixes
=========

-  The new dict ``in`` optimization was compile time crashing on code
   where the dictionary shaped value checked for a key was actually an
   conditional expression

   .. code:: python

      # Was crashing
      "value" in some_dict if condition else other_dict

   Fixed in 1.5.1 already.

-  Standalone: Added support for ``openvino``. This also required to
   make sure to keep used DLLs and their dependencies in the same
   folder. Before they were put on the top level. Fixed in 1.5.1
   already.

-  Android: Convert ``RPATH`` to ``RUNPATH`` such that standalone
   binaries need no ``LD_LIBRARY_PATH`` guidance anymore. Fixed in 1.5.1
   already.

-  Standalone: Added support for newer ``skimage``. Fixed in 1.5.1
   already.

-  Standalone: Fix, new data file type ``.json`` needed to be added to
   the list of extensions used for the Qt plugin bindings. Fixed in
   1.5.2 already.

-  Standalone: Fix, the ``nuitka_types_patch`` module using during
   startup was released, which can have bad effects. Fixed in 1.5.2
   already.

-  Android: More reliable detection of the Android based Python Flavor.
   Fixed in 1.5.2 already.

-  Standalone: Added data files for ``pytorch_lightning`` and
   ``lightning_fabric`` packages. Added in 1.5.2 already.

-  Windows: Fix, the preservation of ``PATH`` didn't work on systems
   where this could lead to encoding issues due to reading a MBCS value
   and writing it as a unicode string. We now read and write the
   environment value as ``unicode`` both. Fixed in 1.5.3 already.

-  Plugins: Fix, the scons report values were not available in case of
   removed ``--remove-output`` deleting it before use. It is now read in
   case if will be used. Fixed in 1.5.3 already.

-  Python3.11: Added support for ``ExceptionGroup`` built-in type. Fixed
   in 1.5.4 already.

-  Anaconda: Fix, using ``numpy`` in a virtualenv and not from conda
   package was crashing. Fixed in 1.5.4 already.

-  Standalone: Added support for ``setuptools``. Due to the anti-bloat
   work, we didn't notice that if that was not sufficiently usable, the
   compiled result was not usable. Fixed in 1.5.4 already.

-  Distutils: Added support for pyproject with ``src`` folders. This
   supports now ``tool.setuptools.packages.find`` with a ``where`` value
   with pyproject files, where it typically is used like this:

   .. code:: toml

      [tool.setuptools.packages.find]
      where = ["src"]

-  Windows: Fix, the ``nuitka-run`` batch file was not working. Fixed in
   1.5.4 already.

-  Standalone: Add ``pymoo`` implicit dependencies. Fixed in 1.5.5
   already.

-  macOS: Avoid deprecated API, this should fix newer Xcode being used.
   Fixed in 1.5.5 already.

-  Fix, the ``multiprocessing`` in spawn mode didn't handle relative
   paths that become invalid after process start. Fixed in 1.5.5
   already.

-  Fix, spec ``%CACHE_DIR%`` was not given the correct folder on
   non-Windows. Fixed in 1.5.5 already.

-  Fix, special float values like ``nan`` and ``inf`` didn't properly
   generate code for C values. Fixed in 1.5.5 already.

-  Standalone: Add missing DLL for ``onnxruntime`` on Linux too. Fixed
   in 1.5.5 already.

-  UI: Fix, illegal python flags value could enable ``site`` mode. by
   mistake and were not caught. Fixed in 1.5.6 already.

-  Windows: Fix, user names with spaces failed with MinGW64 during
   linking. Fixed in 1.5.6 already.

-  Linux: Fix, was not excluding all libraries from glibc, which could
   cause crashes on newer systems. Fixed in 1.5.6 already.

-  Windows: Fix, could still pickup SxS libraries distributed by other
   software when found in PATH. Fixed in 1.5.6 already.

-  Windows: Fix, do not use cache DLL dependencies if one the files
   listed there went missing. Fixed in 1.5.6 already.

-  Onefile: Reject path spec that points to a system folder. We do not
   want to delete those when cleaning up clearly. Added in 1.5.6
   already.

-  Plugins: Fix, the ``dill-compat`` was broken by code object changes.
   Fixed in 1.5.6 already.

-  Standalone: Added workaround for ``networkx`` decorator issues. Fixed
   in 1.5.7 already.

-  Standalone: Added workaround for PySide6 problem with disconnecting
   signals from methods. Fixed in 1.5.7 already.

-  Standalone: Added workaround for PySide2 problem with disconnecting
   signals.

-  Fix, need to make sure the yaml package is located absolutely or else
   case insensitive file systems can confuse things. Fixed in 1.5.7
   already.

-  Standalone: Fix, extra scan paths were not considered in caching of
   module imports, breaking the feature in many cases. Fixed in 1.5.7
   already.

-  Windows: Fix, avoid system installed ``appdirs`` package as it is
   frequently broken. Fixed in 1.5.7 already.

-  Standalone: The bytecode cache check needs to handle re-checking
   relative imports found in the cache better. Otherwise some standard
   library modules were always recompiled due to apparent import
   changes. Fixed in 1.5.7 already.

-  Nuitka-Python: Fix, do not insist on ``PYTHONHOME`` making it to
   ``os.environ`` in order to delete it again. Fixed in 1.5.7 already.

-  Nuitka-Python: Allow builtin modules of all names. This is of course
   what it does. Fixed in 1.5.7 already.

-  Nuitka-Python: Ignore empty extension module suffix. Was confusing
   Nuitka to consider every file an extension module potentially. Fixed
   in 1.5.7 already.

-  Plugins: Properly merge code coming from distinct plugins. The
   ``__future__`` imports need to be moved to the start. Added in 1.5.7
   already.

-  Standalone: Added support for ``opentele`` package. Fixed in 1.5.7
   already.

-  Standalone: Added support for newer ``pandas`` and ``pyarrow`` usage.
   Fixed in 1.5.7 already.

-  Standalone: Added missing implicit dependency for PySide6. Fixed in
   1.5.7 already.

-  Fix, the pyi-file parser didn't handle doc strings, and could be
   crash for comment contents not conforming to be import statement
   code. Fixed in 1.5.8 already.

-  Standalone: Added support for ``pyqtlet2`` data files.

-  Python2: Fix, ``PermissionError`` doesn't exist on that version,
   which could lead to issues with retries for locked files e.g. but was
   also observed with symlinks.

-  Plugins: Recognize the error given by with ``upx`` if a file is
   already compressed.

-  Fix, so called "fixed" imports were not properly tracking their use,
   such that they then didn't show up in reports, and didn't cause
   dependencies on the module, which could e.g. impact ``importlib`` to
   not be included even if still being used.

-  Windows: Fix, retries for payload attachment were crashing when
   maximum number of retries were reached. Using the common code for
   retries solves that, since that code handles it just fine.

-  Standalone: Added support for the ``av`` module.

-  Distutils: Fix, should build from files in ``build`` folder rather
   than ``source`` files. This allows tools like ``versioneer`` that
   integrate with setuptools to do their thing, and get the result of
   that to compilation rather than the original source files.

-  Standalone: Added support for the ``Equation`` module.

-  Windows/macOS: Avoid problems with case insensitive file systems. The
   ``nuitka.Constants`` module and ``nuitka.constants`` package could
   collide, so we now avoid that package, there was only what is now
   ``nuitka.Serialization`` in there anyway. Also similar problem with
   ``nuitka.utils.Json`` and ``json`` standard library module.

-  Standalone: Added support ``transformers`` package.

-  Standalone: Fix for ``PyQt5`` which needs a directory to exist.

-  macOS: Fix, was crashing with PyQt6 in standalone mode when trying to
   register plugins to non-default path. We now try to skip the need,
   which also makes it work.

-  Fix, recursion error for complex code that doesn't happen in ``ast``
   module, but during conversion of the node tree it gives to our own
   tree, were not handled, and crashed with ``RecursionError``. This is
   now also handled, just like the error from ``ast``.

-  Standalone: Added support for ``sqlfluff``.

-  Standalone: Added support for PySide 6.5 on macOS solving DLL
   dependency issues.

-  Scons: Recognize more ``ccache`` outputs properly, their logging
   changed and provided irrelevant states, and ones not associated so
   far.

-  Onefile: Fix, could do random exit codes when failing to fork for
   whatever reason.

-  Standalone: Added support for ``pysnmp`` package.

-  Standalone: Added support for ``torchaudio`` and ``tensorflow`` on
   macOS. These contain broken DLL dependencies as relative paths, that
   are apparently ignored by macOS, so we do that too now.

-  Onefile: Use actual rather than guessed standalone binary name for
   ``multiprocessing`` spawns. Without this, a renamed onefile binary,
   didn't work.

-  Fix, side effect nodes, that are typically created when an expression
   raises, were use in optimization contexts, where they do not work.

-  Standalone: Added missing implicit dependency for
   ``sentence_transformers`` package.

-  macOS: Fix, added missing dependency for ``platform`` module.

New Features
============

-  Support for Python 3.11 is finally there. This took very long,
   because there were way more core changes than with previous releases.
   Nuitka integrates close to that core, and is as such very affected by
   this. Also a lot of missed opportunities to improve 3.7 or higher,
   3.9 or higher, and 3.10 or higher were implemented right away, as
   they were discovered on the way. Those had core changes not yet taken
   advantage of and as a result got faster with Nuitka too.

-  Reports: Added option ``--report-diffable`` to make the XML report
   created with ``--report`` become usable for comparison across
   different machine installations, users compiling, etc. so it can be
   used to compare versions of Nuitka and versions of packages being
   compiled for changes. Also avoid short names in reports, and resolve
   them back to long names, so they become more portable too.

-  Reports: Added option to provide custom data from the user. We use it
   in out testing to record the pipenv state used with things like
   ``--report-user-provided=pipenv-lock-hash=64a5e4`` with this data
   ending up inside of reports, where tools like the new testing tool
   ``nuitka-watch`` can use it to decide if upstream packages changed or
   not. These are free form, just needs to fit XML rules.

-  Plugins: Added ``include-pyi-file`` flag to data-files section. If
   provided, the ``.pyi`` file belonging to a specific module is
   included. Some packages, e.g. ``skimage`` depend at runtime on them.
   For data file options and configuration, these files are excluded,
   but this is now the way to force their inclusion. Added in 1.5.1
   already.

-  Compatibility: Added support for including distribution metadata with
   new option ``--include-distribution-metadata``.

   This allows generic walks over distributions and their entry points
   to succeed, as well as version checks with the metadata packages that
   are not compile time optimized.

-  Distutils: Handle extension modules in build tasks. Also recognize if
   we built it ourselves, in which case we remove it for rebuild. Added
   in 1.5.7 already.

-  Linux: Detect DLL like filenames that are Python extension modules,
   and ignore them when listing DLLs of a package with
   ``--list-package-dlls`` option. So far, this was a manual task to
   figure out actual DLLs. This will of course improve the Yaml package
   configuration tooling .

-  Onefile: Allow forcing to use no compression for the onefile payload,
   useful for debugging, to avoid long compression times and for test
   coverage of the rare case of not compressing if the bootstrap handles
   that correctly too.

-  Need to resolve symlinks that were used to call the application
   binary in some places on macOS at least. We therefore implemented the
   previously experimental and Windows only feature for all platforms.

-  Standalone: Added support including symlinks on non-Windows in
   standalone distribution, if they still point to a path that is inside
   the distribution. This can save a bunch of disk space used for some
   packages that e.g. distribute DLL links on Linux.

-  Onefile: Added support for including symlinks from the standalone
   distribution as such on non-Windows. Previously they were resolved to
   complete copies.

-  UI: Respect code suffixes in package data patterns. With this e.g.
   ``--include-package-data=package_name:*.py`` is doing what you say,
   even if of course, that might not be working.

-  UI: Added option ``--edit-module-code`` option.

   To avoid manually locating code to open it in Visual Code replaced
   old ``find-module`` helper to be a main Nuitka option, where it is
   more accessible. This also goes beyond it it, such that it resolves
   standalone file paths to module names to make debugging easier, and
   that it opens the file right away.

-  Standalone: Added support for handling missing DLLs. Needed for macOS
   PySide6.5.0 from PyPI, which contains DLL references that are broken.
   With this feature, we can exclude DLLs that wouldn't work anyway.

Optimization
============

-  Anti-Bloat: Remove ``IPython`` usage in ``huggingface_hub`` package
   versions. Added in 1.5.2 already.

-  Anti-Bloat: Avoid ``IPython`` usage in ``tokenizers`` module. Added
   in 1.5.4 already.

-  Added support for module type as a constant value. We want to add all
   types we have shapes for to allow better ``type(x)`` optimization.
   This is only the start.

-  Onefile: During payload unpacking the memory mapped data was copied
   to an input buffer. Removing that avoids memory copying and reduces
   usage.

-  Onefile: Avoid repeated directory creations. Without it, the
   bootstrap was creating already existing directories up to the root
   over and over, making many unnecessary file system checks. Added in
   1.5.5 already.

-  Anti-Bloat: Remove usage of ``IPython`` in ``trio`` package. Added in
   1.5.6 already.

-  Onefile: Use resource for payload on Win32 rather than overlay. This
   integrates better with signatures, removing the need to check for
   original file size. Changed in 1.5.6 already.

-  Onefile: Avoid using zstd input buffer, but using the memory mapped
   contents directly avoiding to copy uncompressed payload data. Changed
   in 1.5.6 already.

-  Onefile: Avoid double slashes in expanded onefile temp spec paths,
   they are just ugly.

-  Anti-Bloat: Remove usage of ``pytest`` and ``IPython`` for some
   packages used by newer ``torch``. Added in 1.5.7 already.

-  Anti-Bloat: Avoid ``triton`` to use setuptools. Added in 1.5.7
   already.

-  Anti-Bloat: Avoid ``pytest`` in newer ``networkx`` package. Added in
   1.5.7 already.

-  Prepare optimization for more built-in types with experimental code,
   but we need to disable it for now as it requires more completeness in
   code generation to cover them all. We did some, e.g. module type, but
   many more will be missing still.

-  Prepare optimization of class selection at compile time, by having a
   helper function rather than a dedicated node. This work is not
   complete though, and cannot be activated yet.

-  Windows: Cache short path name resolutions. Esp. for reporting, we
   now do a lot more of these than before, and this avoids they can
   become too time consuming.

-  Faster constant value handling for float value checks by avoiding
   module lookups per value.

-  Minimize size for hello world distribution such that no unused
   extension modules are included, by excluding even more modules and
   using modules from automatic inclusion of standard library.

-  Anti-Bloat: Catch ``pytest`` namespaces ``py`` and ``_pytest``
   sooner, to point to the actual uses more directly.

-  Anti-Bloat: Usage of ``doctest`` equals usage of "unittest" so cover
   it too, to point to the actual uses more directly.

-  Ever more spelling fixes in code and tests were identified and fixed.

-  Make sure side effect nodes indicate properly that they are raising,
   allowing exceptions to fully bubble up. This should lead to more dead
   code being recognized as such.

Organisational
==============

-  GitHub: Added marketplace action designed to cross platform build
   with Nuitka on GitHub directly. Usable with both standard and
   commercial Nuitka versions, and pronouncing it as officially
   supported.

   Check out out at `Nuitka-Action
   <https://github.com/Nuitka/Nuitka-Action>`__ repository.

-  Windows: When MSVC doesn't have WindowsSDK, just don't use it, and
   proceed, to e.g. allow fallback to winlibs gcc.

-  User Manual: The code to update benchmark numbers as giving was
   actually wrong. Fixed in 1.5.1 already.

-  UI: Make it clear that partially supported versions are considered
   experimental, not unsupported. Fixed in 1.5.2 already.

-  Plugins: Do not list deprecated plugins with ``plugin-list``, they do
   not have any effect, but listing them, makes people use them still.
   Fixed in 1.5.4 already.

-  Plugins: Make sure all plugins have descriptions. Some didn't have
   any yet, and sometimes the wording was improved. Fixed in 1.5.4
   already.

-  UI: Accept ``y`` as a shortcut for ``yes`` in prompts. Added in 1.5.5
   already.

-  Reports: Make sure the DLL dependencies for Linux are in a stable
   order. Added in 1.5.6 already.

-  Plugins: Check for latest fixes in PySide6. Added in 1.5.6 already.

-  Windows XP: For Python3.4 make using Python2 scons work again, we
   cannot have 3.5 or higher there. Added in 1.5.6 already.

-  Quality: Updated to latest PyLint. With Python 3.11 the older one,
   was not really working, and it was about time. Due to its many
   changes, we included it in the hotfix, so those can still be done.
   Changed in 1.5.7 already.

-  Release: Avoid broken ``requires.txt`` in source distribution. This
   apparently breaks poetry. Changed in 1.5.7 already.

-  GitHub: Enhanced issue template for more clarity, esp. to avoid
   unnecessary options, e.g. using ``--onefile`` for issues that show up
   with ``--standalone`` already, to report factory branch issues rather
   on Discord, and give a quick tip for a likely reproducer if a package
   fails to import.

-  User Manual: Added instructions on how to add a DLL or executable to
   a standalone distribution.

-  User Manual: Example paths in the table for path specs, meant for
   Windows were not properly escaping the backslashes and therefore
   rendered incorrectly.

-  Visual Code: Python3.11 is now the default configuration for C code
   editing.

-  Developer Manual: Updated descriptions for adding test suite. While
   added the Python 3.11 test suite, these instructions were further
   improved.

-  Debugging: Make it easier to fully deactivate free lists. Now only
   need to set max size to 0 and the free list will not be used.

-  Debugging: Added more assertions, added corrections to feature
   disables, check args after function calls for validity, check more
   types to be as expected.

-  Plugins: Enhanced plugin error messages generally, with ``--debug``
   exceptions become warning messages with the original exception being
   raised instead, making debugging during development much easier.

-  UI: Make it clear what not using ``ccache`` actually means. Not
   everybody is familiar with the design of Nuitka there or what the
   tool can actually do.

-  UI: Do not warn about not found distributions but merely inform of
   them.

   Since Nuitka is fully compatible with these, no need to consider
   those a warning, for some packages they also are given really a lot.

-  UI: Catch user error of wrong cases plugin names

   This now points out the proper name rather than denying the existence
   outright. We do not want to accept wrong case names silently.

Cleanups
========

-  Use proper API for setting ``PyConfig`` values during interpreter
   initialization. There is otherwise always the risk of crashes, should
   these values change during runtime. Fixed in 1.5.2 already.

-  For our reformulations have a helper function that build release
   statements for multiple variables at once. This removed a bunch of
   repetitve code from re-formulations.

-  Move the pyi-file parser code out of the module nodes and to source
   handling, where it is more closely related.

Tests
=====

-  Adding a ``nuitka-watch`` tool, which is still experimental and for
   use with the `Nuitka-Watch
   <https://github.com/Nuitka/Nuitka-Watch>`__ repository.

-  Refined macOS standalone exceptions further to cover more normal
   usages of files on that OS and for frameworks that applications
   typically use from the system.

-  Detect and consider onefile mode if given in project options as well.

-  Was not really applying import check in programs tests. Added in
   1.5.6 already.

-  Added coverage of testing the signing of Windows binaries with the
   commercial plugin.

-  Added coverage of version information to hello world onefile test, so
   we can use it for Virus tools checks.

-  Added tests to cover PyQt6 and PySide6 plugin availability, we so far
   only had that for PyQt5, which is of course not relevant, and totally
   different code anyway.

-  Cleanup distutils tests case to use common test case scanning. We now
   decide version skips based on names, and had to get away from number
   suffixes, so they are now in the middle.

Summary
=======

The class bodies optimization has made some progress in this release,
going to a re-formulation of the metaclass selection, so as to allow its
future optimization. We are not yet at "compiled objects", but this is a
promising road. We need to make some optimization improvements for
inlining constant value calls, then this can become really important,
but by itself these changes do not yield a lot of improvement.

For macOS again a bunch of time was spent to improve and complete the
detection of DLL dependencies. More corner cases are covered now and
more packages just work fine as a result.

The most important is to become Python3.11 compatible, even if attribute
lookups, and other things, and not yet optimized. We will get to that in
future releases. For now, compatibility is the first step to take.

For GitHub users, the Nuitka-Action will be interesting. But it's still
in develop. We keep adding missing options of Nuitka for a while it
seems, but for most people it should be usable already.

The new ``nuitka-watch`` ability, should allow us to detect breaking
PyPI releases, that need a new tweak in Nuitka sooner. But it will
probably grow in the coming releases to full value only. For now the
tool itself is not yet finished.

From here, a few open ends in the CPython 3.11 test suite will have to
be addressed, and maybe some of the performance tricks that it now will
enable, e.g. with repeated attribute lookups.

********************
 Nuitka Release 1.5
********************

This release contains the long awaited 3.11 support, even if only on an
experimental level. This means where 3.10 code is used, it is expected
to work equally well, but the Python 3.11 specific new features have yet
been done.

There is plenty of new features in Nuitka, e.g. much enhanced reports,
Windows ARM native compilation support, and the usual slew of anti-bloat
updates, and newly supported packages.

Bug Fixes
=========

-  Standalone: Added implicit dependencies for ``charset_normalizer``
   package. Fixed in 1.4.1 already.

-  Standalone: Added platform DLLs for ``sounddevice`` package. Fixed in
   1.4.1 already.

-  Plugins: The info from Qt bindings about other Qt bindings being
   suppressed for import, was spawning multiple lines, breaking tests.
   Merged to a single line until we do text wrap for info messages as
   well. Fixed in 1.4.1 already.

-  Plugins: Fix ``removeDllDependencies`` was broken and could not
   longer be used to remove DLLs from inclusion. Fixed in 1.4.1 already.

-  Fix, assigning methods of lists and calling them that way could crash
   at runtime. The same was true of dict methods, but had never been
   observed. Fixed in 1.4.2 already.

-  Standalone: Added DLL dependencies for ``onnxruntime``. Fixed in
   1.4.2 already.

-  Standalone: Added implicit dependencies for ``textual`` package.
   Fixed in 1.4.2 already.

-  Fix, boolean tests of lists could be optimized to wrong result when
   list methods got recognized, due to not annotating the escape during
   that pass properly. Fixed in 1.4.3 already.

-  Standalone: Added missing implicit dependency of ``apsw``. Fixed in
   1.4.3 already.

   .. note::

      Currently ``apsw`` only works with manual workarounds and only in
      limited ways, there is an import level incompatible with
      ``__init__`` being an extension module, that Nuitka does not yet
      handle.

-  Python3: Fix, for range arguments that fail to divide there
   difference, the code would have crashed. Fixed in 1.4.3 already.

-  Standalone: Fix, added support for newer ``pkg_resources`` with
   another vendored package. Fixed in 1.4.4 already.

-  Standalone: Fix, added support for newer ``shapely`` 2.0 versions.
   Fixed in 1.4.4 already.

-  Plugins: Fix, some yaml package configurations with DLLs by code
   didn't work anymore, notably old ``shapely`` 1.7.x versions were
   affected. Fixed in 1.4.4 already.

-  Fix, for onefile final result the "--output-dir" option was ignored.
   Fixed in 1.4.4 already.

-  Standalone: Added ``mozilla-ca`` package data file. Fixed in 1.4.4
   already.

-  Standalone: Fix, added missing implicit dependency for newer
   ``gevent``. Fixed in 1.4.4 already.

-  Scons: Accept an installed Python 3.11 for Scons execution as well.
   Fixed in 1.4.4 already.

-  Python3.7: Some ``importlib.resource`` nodes asserted against use in
   3.7, expecting it to be 3.8 or higher, but this interface is present
   in 3.7 already. Fixed in 1.4.5 already.

-  Standalone: Fix, Python DLLs installed to the Windows system folder
   were not included, causing the result to be not portable. Fixed in
   1.4.5 already.

-  Python3.9+: Fix, ``metadata.resources`` files method ``joinpath`` is
   some contexts is expected to accept variable number of arguments.
   Fixed in 1.4.5 already.

-  Standalone: Workaround for ``customtkinter`` data files on
   non-Windows. Fixed in 1.4.5 already.

-  Standalone: Added support for ``overrides`` package. Fixed in 1.4.6
   already.

-  Standalone: Added data files for ``strawberry`` package. Fixed in
   1.4.7 already.

-  Fix, anti-bloat plugin caused crashes when attempting to warn about
   packages coming from ``--include-package`` by the user. Fixed in
   1.4.7 already.

-  Windows: Fix, main program filenames with an extra dot apart from the
   ``.py`` suffix, had the part beyond that wrongly trimmed. Fixed in
   1.4.7 already.

-  Fix, list methods didn't properly annotated value escape during their
   optimization, which could lead to wrong optimization for boolean
   tests. Fixed in 1.4.7 already.

-  Standalone: Added support for ``imagej``, ``scyjava``, ``jpype``
   packages. Fixed in 1.4.8 already.

-  Fix, using ``--include-package`` on extension module names was not
   working. Fixed in 1.4.8 already.

-  Standalone: Added support for ``tensorflow.keras`` namespace as well.

-  Distutils: Fix namespace packages were not including their contained
   modules properly with regards to ``__file__`` properties, making
   relative file access impossible.

-  Onefile: On Windows the onefile binary did lock itself, which could
   fail with certain types of AV software. This is now avoided.

-  Accessing files using the top level ``metadata.resources`` files
   object was not working properly, this is now supported too.

-  MSYS2: Make sure mixing POSIX and Windows slashes causes no issues by
   hard-coding the onefile archive to use the subsystem slash rather
   than what MSYS prefers to use internally.

-  Standalone: Added missing dependencies of newer ``imageio``.

-  Fix, side effect nodes didn't annotate their non-exception raising
   nature properly, if that was the case.

New Features
============

-  Added experimental support for Python 3.11, for 3.10 language level
   code it should be fully usable, but the ``CPython311`` test suite has
   not even been started to check newly added or changed features.

-  Windows: Support for native Python on Windows ARM64, which needs 3.11
   or higher, but standalone and therefore onefile do not yet work, due
   to lack of any form of binary dependency analysis tool.

   This platform is relatively new in Python and generally. For the time
   being standalone and onefile should be done with Intel based Python,
   they would also be ARM64 only, whereas 32/64 Bit binaries can be run
   on all Windows ARM platforms.

-  Reports: Write compilation report even in case of Nuitka being
   interrupted or crashing. This then includes the exception, and a
   status like ``completed`` or ``interrupted``. At this time this
   happens only when ``--report=`` was specified, but in the future we
   will likely write one in case of Nuitka crashes.

-  Reports: Now the details of the used Python version, its flavor, the
   OS and the architecture are included. This is crucial information for
   analysis and can make ``--version`` output unnecessary.

-  Reports: License reports now handle ``UNKNOWN`` license by falling
   back to checking the classifiers, and therefore include the correct
   license e.g. with ``setuptools``. Also in case no license text is
   found, do not create an empty block. Added in 1.4.4 already.

-  Reports: In case the distribution name and the contained package
   names differ, output the list of packages included from a
   distribution. Added in 1.4.4 already.

-  Reports: Include data file sizes in report. Added in 1.4.7 already.

-  Reports: Include memory usage into the compilation report as well.

-  macOS: Add support for downloading ``ccache`` on arm64 (M1/M2) too.
   Added in 1.4.4 already.

-  UI: Allow ``--output-filename`` for standalone mode again. Added in
   1.4.3 already.

-  Standalone: Improved isolation with Python 3.8 or higher. Using new
   init mechanisms of Python, we now achieve that the scan for
   ``pyvenv.cfg`` on in current directory and above is not done, using
   it will be unwanted.

-  Python2: Expose ``__loader__`` for modules and register with
   ``pkg_resources`` too which expects these to be present for custom
   resource handling.

-  Python3.9+: The ``metadata.resources`` files objects method
   ``iterdir`` was not implemented yet. Fixed in 1.4.5 already.

-  Python3.9+: The ``metadata.resources`` files objects method
   ``absolute`` was not implemented yet.

-  Added experimental ability to create virtualenv from an existing
   compilation report with new ``--create-environment-from-report``
   option. It attempts to create a requirements file with the used
   packages and their versions. However, sometimes it seems not to be
   possible to due to conflicts.

Optimization
============

-  Onefile: Use memory mapping for calculating the checksum of files on
   all platforms. This is faster and simpler code. So far it had only be
   done this way on Windows, but other platforms also benefit a lot from
   it.

-  Onefile: Use memory mapping for accessing the payload rather than
   file operations. This avoids differences to macOS payload handling
   and is much faster too.

-  Anti-Bloat: Avoid using ``dask`` in ``joblib``.

   .. note::

      Newer versions of ``joblib`` do not currently work yet due to
      their own form of multiprocessing spawn not being supported yet.

-  Anti-Bloat: Adapt for newer ``pandas`` package.

-  Anti-Bloat: Remove more ``IPython`` usages in newer tensorflow.

-  Use dedicated class bodies for Python2 and Python3, with the former
   has a static dict type shape, and with Python3 this needs to be
   traced in order to tell what the meta class put in there.

-  Compile time optimize dict ``in``/``not in`` and ``dict.has_key``
   operations statically where the keys of a dict are known. As a
   result, the class declarations of Python3 no longer created code for
   both branches, the one with ``metaclass =`` in the class declaration
   and without. That means also a big scalability improvement.

-  For the Python3 class bodies, the usage of ``locals()`` was not
   recognized as not locally escaping all the variables, leading to
   variable traces where each class variable was marked as escaped for
   no good reason.

-  Added support for ``dict.fromkeys`` method, making the code
   generation understand and handle static methods as well.

-  Added support for ``os.listdir`` and ``os.path.basename``. Added in
   1.4.5 already for use in implementing the ``iterdir`` method, but
   they are also now optimized by themselves.

-  Added support for trusted constant values of the ``os`` module. These
   are ``curdir``, ``pardir``, ``sep``, ``extsep``, ``altsep``,
   ``pathsep``, ``linesep`` which may enable some minor compile time
   optimization to happen and completes this aspect of the ``os``
   module.

-  Faster ``digit`` size checks during ``float`` code generation for
   better compile time performance.

-  Faster ``list`` operations due to using ``PyList_CheckExact``
   everywhere this is applicable, this mostly makes debug operations
   faster, but also deep copying list values, or extending lists with
   iterables, etc.

-  Optimization: Collect module usages of the given module during its
   abstract execution. This avoids a full tree visit afterwards only to
   find them. It is much cheaper to collect them while we go over the
   tree. This enhances the scalability of large compilations by ca. 5%.

-  Optimization: Faster determination of loop variables. Rather than
   using a generic visitor, we use the children having generator codes
   to add traversal code that emits relevant variables to the user
   directly.

-  Cache extra search paths in order to avoid repeated directory
   operations as these are known to be slow at times.

-  Standalone: Do not include ``py.typed`` data files, these indicator
   files are for IDEs, but not needed at run time ever.

-  Make sure that the generic attribute code optimization is also
   effective in cases where a Python DLL is used. Previously this was
   only guaranteed to be used with static libpython.

-  Faster list constant usage

   Small immutable constants get their own code that is much faster for
   small sizes.

   Medium sized lists get code that just is hinted the size, but takes
   items from a source list, still a lot faster.

   For repeated lists where all elements are the same, we use a
   dedicated helper for all sizes, that is even faster except for small
   ones with LTO enabled, where the C compiler may already do that
   effectively.

-  Added optimization for ``os.path.abspath`` and ``os.path.isabs``
   which of course have not as much potential for compile time
   optimization, but we needed them for providing ``.absolute()`` for
   the meta path loader files implementation.

-  Faster class dictionary propagation decision. Instead of checking for
   trace types, let the trace object decide. Also abort immediately on
   first inhibit, rather than checking all variables. This improves
   Python2 compile time, and Python3 where this code is now starting to
   get used when the class dictionary is shown to have ``dict`` type.

-  Specialize type method ``__prepare__`` which is used in the Python3
   re-formation of class bodies to initialize the class dictionary.
   Where the metaclass is resolved, we can use this to decide that the
   standard empty dictionary is used statically, enabling class
   dictionary propagation for best scalability.

   At this time this only happens with classes without bases, but we
   expect to soon do this with all compile time known base classes. At
   this time, these optimization to become effective, we need to
   optimize meta class selection from bases classes, as well as
   modification of base classes with ``__mro_entries__`` methods.

-  The ``bool`` built-in on boolean values is now optimized away.

   Since it's used also for conditions being extracted, this is actually
   somewhat relevant, since it could keep code alive in side effects at
   least for no good reason and this allows a proper reduction.

Organisational
==============

-  Project: Require the useful stuff for installation of Nuitka already.
   These are things we cannot inline really, but otherwise will
   frequently be warned about, e.g. ``zstandard`` for onefile and
   ``ordered-set`` for fast operation, but we do not require packages
   that might fail to install.

-  User Manual: Added section about virus scanners and how to avoid
   false reports.

-  User Manual: Enhanced description for plugin module loading, the old
   code was too complicated and actually working only for a mode of
   including plugin code that is discouraged.

-  User Manual: Fix section for standalone finding files on wrong level.

-  Windows: Using the console on Python 3.4 to 3.7 is not working very
   well with e.g. many Asian systems. Nuitka fails to setup the encoding
   for stdin and stdout or this platform. It can then produce exceptions
   on input or output of unicode data, that doesn't overlap with UTF-8.

   We now inform the user of these older Python with a warning and
   mnemonic, to either disable the console or to upgrade to Python 3.8
   or higher, which normally won't be much of an issue for most users.

   Read more on `the info page
   <https://nuitka.net/info/old-python-windows-console.html>`__ for
   detailed information. Added in 1.4.1 already.

-  Debugging: Fixup debugging reference count output with Python3.4. For
   Python 3.11 compatibility tests, actually it was useful to compare
   with a version that doesn't have coroutines yet. Never tell me,
   supporting old versions is not good.

-  Deprecating support for Python 3.3, there is no apparent use of this
   version, and it has gained specific bugs, that are indeed not worth
   our time. Python 2.6 and Python 2.7 will continue to be supported
   probably indefinitely.

-  Recommend ``ordered-set`` for Python 3.7 to 3.9 as well, as not only
   for 3.10+ because on Windows, to install ``orderset`` MSVC needs to
   be installed, whereas ``ordered-set`` has a wheel for ready use.

-  Actually zstandard requirement is for a minimal version, added that
   to the requirement files.

-  Debugging: Lets not reexecute Nuitka in case if we are debugging it
   from Visual Code.

-  Debugging: Include the ``.pdb`` files in Windows standalone mode for
   proper C tracebacks should that be necessary.

-  UI: Detect the GitHub flavor of Python as well.

-  Quality: Check the ``clang-format`` version to avoid older ones with
   bugs that made it switch whitespace for one file. Using the one from
   Visual Code C extension is a good idea, since it will often be
   available. Running the checks on newer Ubuntu GitHub Actions runner
   to have the correct version available.

-  Quality: Updated the version of ``rstfmt`` and ``isort`` to the
   latest versions.

-  GitHub: Added commented out section for enabling ``ssh`` login, which
   we occasionally need to git bisect problems specific to GitHub Python
   flavor.

-  Plugins: Report problematic plugin name with module name or DLL name
   when these raise exceptions.

-  Use ``ordered-set`` package for Python3.7+ rather than only
   Python3.10+ because it doesn't need any build dependency on Windows.

-  UI: When showing source changes, also display the module name with
   the changed code.

-  UI: Use function intended for user query when asking about downloads
   too.

-  UI: Do not report usage of ``ccache`` for linking from newer version,
   that is not relevant.

-  Onefile: Make sure we have proper error codes when reporting IO
   errors.

-  MSVC: Detect a version for developer prompts too. This version is
   needed for use in enabling version specific features.

-  Started UML diagrams with ``plantuml`` that will need to be completed
   before using them in then new and more visual parts of Nuitka
   documentation.

-  UI: Check icon conversion capability at start of compilation rather
   than error exiting at the very end informing the user about required
   ``imageio`` packages to convert to native icons.

-  Quality: Enhanced autoformat on Windows, which was susceptible to
   tools introducing Windows new lines before other steps were
   performed, that then could be confused, also enforcing use of UTF-8
   encoding when working with Nuitka source code for formatting.

Cleanups
========

-  The ``delvewheel`` plugin was still using a ``zmq`` class name from
   its original implementation, adapted that.

-  Use common template for generator frames as well. This made them also
   work with 3.11, by avoiding duplication.

-  Applied code formatting to many more files in ``tests``, etc.

-  Removed a few micro benchmarks that are instead to be covered by
   construct based tests now.

-  Enhanced code generation for specialized in-place operations to avoid
   unused code for operations that do not have any shortcuts where the
   operation would be actual in-place of a reference count 1 object.

-  Better code generation for module variable in-place operations with
   proper indentation and no repeated calls.

-  Plugins: Use the ``namedtuple`` factory that we created for
   informational tuples from plugins as well.

-  Make details of download utils module more accessible for better
   reuse.

-  Remove last remaining Python 3.2 version check in C code, for us this
   is just Python3 with 3.2 being unsupported.

-  Cleanup, name generated call helper file properly, indicating that it
   is a generated file.

Tests
=====

-  Made the CPython3.10 test suite largely executable with Python 3.11
   and running that with CI now.

-  Allow measuring constructs without writing the code diff again. Was
   crashing when no filename was given.

-  Make Python3.11 test execution recognized by generally accepting
   partially supported versions to execute the tests with.

-  Handle also ``newfstat`` directory checks in file usage scan. This
   are used on newer Linux systems.

-  GitHub: In actions use ``--report`` for coverage and upload the
   reports as artifacts.

-  Use ``no-qt`` plugin to avoid warnings in ``matplotlib`` test rather
   than disabling the warnings about Qt bindings.

-  macOS: Detect if the machine can take runtime traces, which on Apple
   Silicon by default it cannot.

-  macOS: Cover all APIs for file tracing, rather than just one for
   extended coverage.

-  Fix, distutils test was not installing the built wheels, but source
   archive and therefore compiling that second time.

-  For the ``pyproject.toml`` using tests, Nuitka was always downloaded
   from PyPI rather than using the version under test.

-  Ignore ``ld`` info output about mismatching architecture libraries
   being ignored. Fixed in 1.4.1 already.

Summary
=======

With this release an important new avenue for scalability has been
started. While for Python2 class bodies were very often reduced to just
that dictionary creation, with Python3 that was not the case, due to the
many new complexities, and while this release makes a start, we will be
able to continue this path towards much more scalable class creation
codes. And while the performance does not really matter all that much
for these, knowing these, will ultimately lead us to "compiled classes"
as our own type, and "compiled objects" that may well perform much
faster.

Already now, the enhancements to class creation codes will result in
smaller binaries, but much more is expected the more this is completed.

The majority of the work was of course to become Python3.11 compatible,
and unfortunately the attribute lookups are not as optimized as for 3.10
yet, which may cause disappointing results for performance initially. We
will need to complete that before benchmarks will make much sense.

For the next release, full Python 3.11 support is planned. I believe it
should be usable. Problems with 3.11 may get hotfixes, but ultimately
the develop version is probably the one to recommend when using 3.11
with Nuitka, as there will be the whole set of fixes, since not
everything will be ported back.

The new reports should be used in bug reporting soon. We foresee that
for issue reports, these may well become mandatory. Together with the
ability to create a virtualenv from the reports, this may make
reproducing issues a breeze, but first tries on complex projects were
also highlighting that it may not be as simple.

********************
 Nuitka Release 1.4
********************

This release contains a large amount of performance work, where
specifically Python versions 3.7 or higher see regressions in relative
performance to CPython fixed. Many cases of macros turned to functions
have been found and resolved. For 3.10 specifically we take advantage of
new opportunities for optimization. And generally avoiding DLL calls
will benefit execution times on platform where the Python DLL is used,
most prominently Windows.

Then this also adds new features, specifically custom reports. Also
tools to aid with adding Nuitka package configuration input data, to
list DLLs and data files.

With multidist we see a brand new ability to combine several programs
into one, that will become very useful for packaging multiple binaries
without the overhead of multiple distributions.

Bug Fixes
=========

-  Standalone: Added implicit dependencies for ``dependency_injector``
   package. Fixed in 1.3.1 already.

-  Fix, the generated metadata nodes for distribution queries had an
   error in their generated children handling that could cause crashes
   at compile time. Fixed in 1.3.2 already.

-  Standalone: Added implicit dependencies for ``passlib.apache``
   package. Fixed in 1.3.2 already.

-  Windows: Fix, our shortcut to find DLLs by analyzing loaded DLLs
   stumbled in a case of a DLL loaded into the compiling Python that had
   no filename associated, while strange, we need to handle this as
   well. Fixed in 1.3.3 already.

-  Standalone: Also need to workaround more decorator tricks for
   ``networkx``. Fixed in 1.3.3 already.

-  Scons: Fix, was not updating ``PATH`` environment variable anymore,
   which could lead to externally provided compilers and internal
   winlibs gcc clashing on Windows, but should be a general problem.
   Fixed in 1.3.4 already.

-  Standalone: Added support for ``cefpython3`` package. Fixed in 1.3.4
   already.

-  Standalone: Added support for newer ``webview`` package versions.
   Fixed in 1.3.4 already.

-  Standalone: Fix, some extension modules set their ``__file__`` to
   ``None`` during multi phase imports, which we then didn't update
   anymore, however that is necessary. Fixed in 1.3.4 already.

-  Python3.10+: Fix, was not supporting ``match`` cases where an
   alternative had no condition associated. Fixed in 1.3.5 already.

-  Windows: Identify Windows ARM architecture Python properly. We do not
   yet support it, but we should report it properly and some package
   configurations are already taking it already into account. Fixed in
   1.3.5 already.

-  Fix, the Nuitka meta path based loader, needs to expose a
   ``__module__`` attribute because there is code out there, that
   identifies standard loaders through looking at this value, but
   crashes without it. Fixed in 1.3.5 already.

-  Fix, very old versions of the ``importlib_metadata`` backport were
   using themselves to load their ``__version__`` attribute. Added a
   workaround for it, since in Nuitka it doesn't work until after
   loading the module.

-  Fix, value escapes for attribute and subscript assignments sources
   were not properly annotated. This could cause incorrect code
   execution. Fixed in 1.3.6 already.

-  Fix, "pure" functions, which are currently only our complex call
   helper functions, were not visited in all cases. This lead to a crash
   in code generation after modules using them got demoted to bytecode.
   After use from cache, this didn't happen again. Fixed in 1.3.6
   already.

-  Standalone: Added more implicit dependencies of crypto packages.
   Fixed in 1.3.6 already.

-  Standalone: Added implicit dependencies of ``pygments.styles``
   module. Fixed in 1.3.6 already.

-  Fix, was falsely encoding ``Ellipsis`` too soon during tree building.
   It is not quite like ``True`` and ``False``. Fixed in 1.3.6 already.

-  Standalone: Fix, ``numpy`` on macOS didn't work inside an application
   bundle anymore. Fixed in 1.3.7 already.

-  Python3.8+: Fix, need to follow change for extension module handling,
   otherwise some uses of ``os.add_dll_directory`` fail to work. Fixed
   in 1.3.8 already.

-  Standalone: Added missing implicit dependencies of ``sqlalchemy``.
   Fixed in 1.3.8 already.

-  Python3.9+: Fix, resource reader files was not fully compatible and
   needed to register with ``importlib.resources.as_file`` to work well
   with it. Fixed in 1.3.8 already.

-  Fix, the version check for ``cv2`` was not working with the
   ``opencv-python-headless`` variant. Package name and distribution
   name is not a 1:1 mapping for all things. Fixed in 1.3.8 already.

-  Standalone: Added DLLs needed for ``tls_client`` package.

-  Fix, imports of resolved names should be modified for runtime too.
   Where Nuitka recognizes aliases, as e.g. the ``requests`` module
   does, it only adding a dependency on the resolved name, but not
   ``requests`` itself. The import however was still done at runtime on
   ``requests`` which then didn't work. This was only visible if only
   these aliases to other modules were used.

-  Onefile: Fix, do not send duplicate CTRL-C to child process. Our test
   only send it to the bootstrap process, rather than the process group,
   as it normally is working, therefore misleading us into sending it to
   the child even if not needed.

-  Onefile: When not using cached mode, on Windows the temporary folder
   used sometimes failed to delete after the executable stopped with
   CTRL-C. This is due to races in releasing of locks and process
   termination and AV tools, so we now retry for some time, to make sure
   it is always deleted.

-  Standalone: Fix, was not ignoring ``.dylib`` when scanning for data
   files unlike all other DLL suffixes.

-  Standalone: Added missing implicit dependency of ``mplcairo``.

-  Standalone: The main binary name on non-Windows didn't have a suffix
   ``.bin`` unlike in accelerated mode. However, this didn't work well
   for packages which have binaries colliding with the package name.
   Therefore now the suffix is added in this case too.

-  macOS: Workaround bug in ``platform_utils.paths``. It is guessing the
   wrong path for included data files with Nuitka.

-  Standalone: Added DLLs of ``sound_lib``, selecting by OS and
   architecture.

-  Fix, for package metadata as from ``importlib.metadata.metadata`` for
   use at runtime we need to use both package name and distribution name
   to create it, or else it failed to work. Packages like
   ``opencv-python-headless`` can now with this too.

-  Standalone: Added support for ``tkinterweb`` on Windows. Other
   platforms will need work to be done later.

New Features
============

-  UI: Added new option to listing package data files. This is for use
   with analyzing standalone issues. And will output all files that are
   data files for a given package name.

   .. code:: shell

      python -m nuitka --list-package-data=tkinterweb

-  UI: Added new option to listing package DLL files. This is also for
   use with analyzing standalone issues.

   .. code:: shell

      python -m nuitka --list-package-dlls=tkinterweb

-  Reports: The usages of modules, successful or not, are now included
   in the compilation report. Checking out which ones are ``not-found``
   might help recognition of issues.

-  Multidist: You can now experimentally create binaries with multiple
   entry points. At runtime one of multiple ``__main__`` will be
   executed. The option to use is multiple ``--main=some_main.py``
   arguments. If then the binary name is changed, on execution you get a
   different variant being executed.

   .. note::

      Using it with only one replaces the previous use of the positional
      argument given and is not using multidist at all.

   .. note::

      Multidist is compatible with onefile, standalone, and mere
      acceleration. It cannot be used for module mode obviously.

   For deployment this can solve duplication.

   .. note::

      For wheels, we will probably change those with multiple entry
      points to compiling multidist executables, so we do avoid Python
      script entry points there. But this has not yet been done.

-  Onefile: Kill non-cooperating child processes on CTRL-C after a grace
   period, that can be controlled at compile time with
   ``--onefile-child-grace-time`` the hard way. This avoids hangs of
   processes that fail to properly shutdown.

-  Plugins: Add support for extra global search paths to mimic
   ``sys.path`` manipulations in the Yaml configuration with new
   ``global-sys-path`` import hack.

-  Reports: Include used distributions of compiled packages and their
   versions.

-  Reports: Added ability to generate custom reports with
   ``--report-template`` where the user can provide a Jinja2 template to
   make his own reports.

-  Anti-Bloat: Added support for checking python flags. There are
   ``no_asserts``, ``no_docstrings`` and ``no_annotations`` now. These
   can be used to limit rules to be only applied when these optional
   modes are active.

   Not all packages will work in these modes, but often can be enhanced
   to work with relatively little patching. This allows to limit these
   patches to only where they are necessary.

Optimization
============

-  Anti-Bloat: Avoid using ``sparse`` and through that Numba in the
   ``scipy`` package, reducing its distribution footprint. Part of 1.3.3
   already.

-  Anti-Bloat: Avoid IPython and Numba in ``trimesh`` package. Part of
   1.3.3 already.

-  Anti-Bloat: Avoid Numba in ``shap`` package. Part of 1.3.8 already.

-  Anti-bloat: Removed ``xgboost`` docstring dependencies, such that
   ``--python-flag=no_docstrings`` can be used with this package.

-  For guided deep copy ``frozenset`` and empty ``tuple`` need no copies

   This also speeds up copies of non-empty tuples by avoiding that size
   checking branch in construction with Python 3.10 or higher.

-  For node construction, avoid keyword argument style calls of the base
   class, where there is only a single argument. They don't really help
   readability, but cost compile time.

-  Determine guard mode of frames dynamically and avoid frame
   preservation checks where they are not needed.

   For Python2 this is necessary, but not for Python3, so make the
   function avoid finding the parent frame for that version entirely,
   which should speed up compilation as well.

   By not hard coding frame guard mode at creation time, and instead
   determine it at compile time, after optimization, so this now allows
   to use the "once" mode more often. This affects contractions and also
   classes on the module level right now. They do not need a cached
   frame, since their code is only executed once.

   By avoiding that useless code, the C compiler also has a slightly
   better scalability, since the classes are all created in one function
   that then has less code.

-  The bytecode cache is now checking if the used modules or attempted
   to be used modules are available or not in just the same way.
   Previously it was very dependent on the file system to contain the
   same things, which was not giving cache hits even after only creating
   a new folder near a binary, since that affected importable modules.
   With the new check it should be much more directly hitting even
   across different virtual environments, but with same code.

-  Generate base classes or mixins for all kinds of expression,
   statements and statement sequences. The previous code had a dedicated
   variant for single child, to allow faster operation in a common case,
   but still a lot of ``hasattr/getattr/setattr`` on dynamic attribute
   names were done. This was making the tree traversal during
   optimization slower than necessary.

   Another shortcoming was that for some nodes, some values are
   optional, where for others, they are not. Some values are a ``tuple``
   actually, while most are nodes only. However, dealing with this
   generically was also slower than necessary.

   The new code now enforces children types during creation and updated,
   it rejects unexpected ``None`` values for non-optional children, and
   it provides generated code to do this in the fastest way possible,
   although surely some more improvements will come here.

   Also when abstract executing the tree, rather than generically
   visiting all children, this now just unrolls this, and there are even
   some modes added, where a node can indicate properties, e.g.
   ``auto_compute_handling = "final,no_raise"`` will tell the code
   generator that this expression never raises in the computation, and
   is final, i.e. doesn't have any code to evaluate, because it cannot
   be optimized any further.

   Also the way ``checkers`` previously worked, for every node creation,
   for every child update, a dictionary lookup had to be done. This is
   now hard coded for the few nodes that actually want to convert values
   on the fly and we might make a difference in the future for optional
   checkers, such that these are only run in debug mode.

   These changes brought about much faster compilation, however the big
   elephant in the room will still be merging value traces, and
   scalability problems remain there.

-  Attribute node generation for method specs like ``dict.update``, etc.
   now provide type shapes. From these type shapes, mixins for the
   result value type are picked automatically. Previously these shapes
   were added manually. In some cases, they were even missing. In a few
   cases, where the type is dependent on the Python version, we do not
   currently do this though, so this needs more work, but expanding the
   coverage got easier in this way.

-  Determining the used modules of a module requires a tree visit
   operations, that then asked for node types and used different APIs.
   This has been unified to be able to call a virtual method instead,
   which saves some compile time.

-  After scanning for a module, we then determined the module kind even
   after we previously knew it during the scan. Also, this was checking
   ``os.path.isdir`` which was making it relatively slow and wasting 5%
   compile time on the IO being done. The check got enhanced and most
   often replaced with using the knowledge from the original import scan
   eliminating this time.

-  Already most helper code of Nuitka was included from ``.c`` files,
   but compiled generators and compiled cells codes were not yet done
   like this, making life unnecessarily harder for the compiler and
   linker. This should also allow more optimization for some codes.

-  Cache the plugin decisions about recursion for a module name. When a
   module is imported multiple times plugins were each asked again and
   again, which is not a good thing to do.

-  Avoid usage of ``PyObject_RichCompareBool`` API, as we have our own
   comparison functions that are faster and faster to call without
   crossing of DLL barrier.

-  Python3.8+: Avoid usage of ``PyIndex_Check`` which has become an API
   in 3.8, and was as a result not inlined anymore with a DLL barrier
   was to be crossed, making all kinds of multiplication and
   subscript/index operations slower.

-  Replace ``PyNumber_Index`` API with our own code. As of 3.10 it
   enforces a conversion to ``long`` that for Nuitka is not a good thing
   to do in all places. But also due to DLL barrier it was potentially
   slow to call, and is used a lot, and we can drop the checks that are
   useless for Nuitka.

-  Python3.7+: Avoid the use of ``PyImport_GetModule`` for looking up
   imported modules from ``sys.modules``, rather look it up from
   interpreter internals, also this was using subscript functions, when
   this is always a dictionary.

-  Avoid using ``PyImport_GetModuleDict`` and instead have our own API
   to get this quicker.

-  Faster exception match checks and sub type checks.

   This solves a ``TODO`` about inlining the API function used, so we
   can be faster in a relatively common operation. For every exception
   handler, we had to do one API call there.

-  Faster subtype checks.

   These are common in binary operations on non-identical types, but
   also needed for the exception checks, and object creation through
   class type calls. With our own ``PyType_IsSubType`` replacement these
   faster to use and avoid the API call.

-  Faster Python3 ``int`` value startup initialization.

   On Python 3.9 or higher we can get small int values directly from the
   interpreter, and with 3.11 they are accessible as global values.

   Also we no longer de-duplicate small int values through our cache,
   since there is no use in this, saving a bunch of startup time. And we
   can create the values with our own API replacement, that will work
   during startup already and save API calls as these can be relatively
   slow. And esp. for the small values, this benefits from not having to
   create them.

-  Faster Python3 ``bytes`` value startup initialization.

   On Python 3.10 or higher, we can create these values ourselves
   without an API call, avoiding its overhead.

   Also we no longer de-duplicate small bytes values through our cache,
   because that is already done by the API and our replacement, so this
   was just wasting time.

-  Faster ``slice`` object values with Python 3.10 or higher

   On Python 3.10 or higher, we can create these values ourselves
   without an API call, avoiding its overhead.

   These are important for Python3, because ``a[x:y]`` in the general
   case has to use ``a[slice(x,y)]`` on that version, making this
   somewhat relevant to performance in some cases.

-  Faster ``str`` built-in with API calls

   For common cases, this avoids API calls. We mostly have this such
   that ``print`` style tests do not have this as API calls where we
   strive to remove all API calls for given programs.

-  Faster exception normalization.

   For the common case, we have our own variant of
   ``PyErr_NormalizeException`` that will avoid the API call. It may
   still call the ``PyObject_IsSubclass`` API, for which we only have
   started replacement work, but this is already a step ahead in the
   right direction.

-  Faster object releases

   For Python3.8 or higher when our code released objects, it was doing
   that with an API call, due to a macro change in Python headers. We
   revert that and do it still on our own which avoids the performance
   penalty.

-  Enable Python threading during extension module DLL loading

   We now release the GIL for Python3.8 or higher when loading the DLL,
   following a change in that version.

-  Faster variable handling in trace collection. The code was doing
   checks for variable types, to decide what to do e.g. when control
   flow escapes for a variable. However, this is faster if solved with a
   virtual method in those variable classes, shifting the responsibility
   to inside there.

-  For call codes the need to check the return value was not perfectly
   annotated in all cases. This is now driven by the expression rather
   than passed, and will result in better code generated in some corner
   cases.

Organisational
==============

-  Release: Make clear we require ``wheel`` and ``setuptools`` to
   install by adding a ``pyproject.toml`` that addresses a warning of
   ``pip``. Part of 1.3.6 release already.

-  Debugging: When plugins evaluate ``when`` conditions that raise,
   output which it was exactly. Part of 1.3.3 already.

-  Anti-Bloat: Added a mnemonic and more clear message for the case of
   unwanted imports being encountered. Also do not warn about IPython
   itself using IPython packages, that must of course be considered
   normal. Now it also lists the module that does the unwanted usage
   immediately. Previously this was not as clear.

-  UI: More clear output for not yet supported Python version. Make it
   more clear in the message, what is the highest supported version, and
   what version is Nuitka and what is Python in this.

-  UI: Make sure data files have normalized paths. Specifically on
   Windows, otherwise a mix of slashes could appear. Part of 1.3.6
   release already.

-  UI: Make it clear that disabling the console harms your debugging
   when we suggest the ``--disable-console`` for GUI packages. Otherwise
   using that, they just deprive themselves of ways to get error
   information.

-  UI: The ordering of scons ``ccache`` report was not enforced. Part of
   1.3.7 release already.

-  Quality: Use proper temporary filename during autoformat, so as to
   avoid flicker in Visual Code, e.g. search results.

-  User Manual: Was still using old option name for
   ``--onefile-tempdir-spec`` that has since been made not OS specific,
   with even the OS specific name being removed.

-  Standalone: Do not include data files scanned with ``site-packages``
   or ``__pycache__`` folders. This should make it easier to use
   ``--include-data-file=./**.qml:.`` when you have a virtualenv living
   in the same folder.

-  Onefile: Added check for compression ability before starting the
   compilation to inform the user immediately.

-  Release: Mark macOS as supported in PyPI categories. This is of
   course true for a long time already.

-  Release: Mark Android as supported in PyPI categories as well. With
   some extra work, it can be used.

-  User Manual: Added section pointing to and explaining compilation
   reports. This has become extremely useful even if still somewhat work
   in progress.

-  User Manual: Added table with included custom reports, at this time
   only the license reports, which is very rough shape and needs
   contributors for good looks and content.

Cleanups
========

-  Plugins: Moved parts of the ``pywebview`` plugin that pertain to the
   DLLs and data files to package configuration.

-  Made the user query code a dedicated function, so it can be reused
   and more consistent across its uses in Nuitka. With a default that is
   proposed to a user, and a default that applies if used
   non-interactively. We will switch all prompts to using this.

-  Code generation for module, class and function frames is now unified,
   removing duplication while also becoming more flexible. For
   generators this work has been started, but is not yet completed.

-  Nodes exposing used modules now implement the same virtual method
   providing a list of them.

-  Make sure to pass ``tuple`` values rather than ``list`` values from
   the tree building stage and node optimization creating new nodes.
   This allows us to drop conversions previously done inside of nodes.

Tests
=====

-  Do not enable deprecated plugins, the warnings about them break
   tests.

-  Ignore Qt binding warnings in tests, some are less supported than
   ``PySide6`` or commercial ``PySide2``.

Summary
=======

The focus of this release was first a major restructuring of how
children are handled in the node tree. The generated code opens up the
possibility of many more scalability improvements in the coming
releases. The pure iteration speed for the node tree will make compile
times for the Python part even shorter in coming releases. Scalability
will be a continuous focus for some releases.

Then the avoiding of API calls is a huge benefit for many platforms that
are otherwise at a disadvantage. This is also only started. We will aim
at getting more complex programs to do next to none of these, so far
only some tests are working after program start without them, which is
of course big progress. We will progress there with future releases as
well.

Catching up on problems that previous migrations have not discovered is
also a huge step forward to restoring the performance supremacy, that
was not there anymore in extreme cases.

The Yaml package configuration work is showing its fruits. More people
have been able to contribute changes for ``anti-bloat`` or missing
dependencies than ever before.

Some part of the Python 3.11 work have positively influenced things,
e.g. with the frame cleanup. THe focus of the next release cycle shall
be to add support for it. Right now, generator frames need a cleanup to
be finished, to also become better and working with 3.11 at the same
time. Where possible, work to support 3.11 was also conducted as a
cleanup action, or reduction of the technical debts.

All in all, it is fair to say that this release is a big leap forward in
all kinds of ways.

********************
 Nuitka Release 1.3
********************

This release contains a large amount of performance work, that should
specifically be useful on Windows, but also generally. A bit of
scalability work has been applied, and as usual many bug fixes and small
improvements, many of which have been in hotfixes.

Bug Fixes
=========

-  macOS: Framework build of PySide6 were not properly supporting the
   use of WebEngine. This requires including frameworks and resources in
   new ways, and actually some duplication of files, making the bundle
   big, but this seems to be unavoidable to keep the signature intact.

-  Standalone: Added workaround for ``dotenv``. Do not insist on
   compiled package directories that may not be there in case of no data
   files. Fixed in 1.2.1 already.

-  Python3.8+: Fix, the ``ctypes.CDLL`` node attributes the ``winmode``
   argument to Python2, which is wrong, it was actually added with 3.8.
   Fixed in 1.2.1 already.

-  Windows: Attempt to detect corrupt object file in MSVC linking. These
   might be produced by ``cl.exe`` crashes or ``clcache`` bugs. When
   these are reported by the linker, it now suggests to use the
   ``--clean-cache=ccache`` which will remove it, otherwise there would
   be no way to cure it. Added in 1.2.1 already.

-  Standalone: Added data files for ``folium`` package. Added in 1.2.1
   already.

-  Standalone: Added data files for ``branca`` package. Added in 1.2.1
   already.

-  Fix, some forms ``try`` that had exiting ``finally`` branches were
   tracing values only assigned in the ``try`` block incorrectly. Fixed
   in 1.2.2 already.

-  Alpine: Fix, Also include ``libstdc++`` for Alpine to not use the
   system one which is required by its other binaries, much like we
   already do for Anaconda. Fixed in 1.2.2 already.

-  Standalone: Added support for latest ``pytorch``. One of our
   workarounds no longer applies. Fixed in 1.2.2 already.

-  Standalone: Added support for webcam on Windows with
   ``opencv-python``. Fixed in 1.2.3 already.

-  Standalone: Added support for ``pytorch_lightning``, it was not
   finding metadata for ``rich`` package. Fixed in 1.2.4 already.

   For the release we found that ``pytorch_lightning`` may not find
   ``rich`` installed. Need to guard ``version()`` checks in our package
   configuration.

-  Standalone: Added data files for ``dash`` package. Fixed in 1.2.4
   already.

-  Windows: Retry replace ``clcache`` entry after a delay, this works
   around Virus scanners giving access denied while they are checking
   the file. Naturally you ought to disable those for your build space,
   but new users often don't have this. Fixed in 1.2.4 already.

-  Standalone: Added support for ``scipy`` 1.9.2 changes. Fixed in 1.2.4
   already.

-  Catch corrupt object file outputs from ``gcc`` as well and suggest to
   clean cache as well. This has been observed to happen at least on
   Windows and should help resolve the ``ccache`` situation there.

-  Windows: In case ``clcache`` fails to acquire the global lock, simply
   ignore that. This happens sporadically and barely is a real locking
   issue, since that would require two compilations at the same time and
   for that it largely works.

-  Compatibility: Classes should have the ``f_locals`` set to the actual
   mapping used in their frame. This makes Nuitka usable with the
   ``multidispatch`` package which tries to find methods there while the
   class is building.

-  Anaconda: Fix, newer Anaconda versions have TCL and Tk in new places,
   breaking the ``tk-inter`` automatic detection. This was fixed in
   1.2.6 already.

-  Windows 7: Fix, onefile was not working anymore, a new API usage was
   not done in a compatible fashion. Fixed in 1.2.6 already.

-  Standalone: Added data files for ``lark`` package. Fixed in 1.2.6
   already.

-  Fix, ``pkgutil.iter_modules`` without arguments was given wrong
   compiled package names. Fixed in 1.2.6 already.

-  Standalone: Added support for newer ``clr`` DLLs changes. Fixed in
   1.2.7 already.

-  Standalone: Added workarounds for ``tensorflow.compat`` namespace not
   being available. Fixed in 1.2.7 already.

-  Standalone: Added support for ``tkextrafont``. Fixed in 1.2.7
   already.

-  Python3: Fix, locals dict test code testing if a variable was present
   in a mapping could leak references. Fixed in 1.2.7 already.

-  Standalone: Added support for ``timm`` package. Fixed in 1.2.7
   already.

-  Plugins: Add ``tls`` to list of sensible plugins. This enables at
   least ``pyqt6`` plugin to do networking with SSL encryption.

-  Standalone: Added implicit dependencies of ``sklearn.cluster``.

-  FreeBSD: Fix, ``fcopyfile`` is no longer available on newest OS
   version, and include files for ``sendfile`` have changed.

-  MSYS2: Add back support for MSYS Posix variant. Now onefile works
   there too.

-  Fix, when picking up data files from command line and plugins,
   different exclusions were applied. This has been unified to get
   better coverage for avoiding to include DLLs and the like as data
   files. DLLs are not data files and must be dealt with differently
   after all.

New Features
============

-  UI: Added new option for cache disabling ``--disable-cache`` that
   accepts ``all`` and cache names like ``ccache``, ``bytecode`` and on
   Windows, ``dll-dependencies`` with selective values.

   .. note::

      The ``clcache`` is implied in ``ccache`` for simplicity.

-  UI: With the same values as ``--disable-cache`` Nuitka may now also
   be called with ``--clean-cache`` in a compilation or without a
   filename argument, and then it will erase those caches current data
   before making a compilation.

-  macOS: Added ``--macos-app-mode`` option for application bundles that
   should run in the background (``background``) or are only a UI
   element (``ui-element``).

-  Plugins: In the Nuitka package configuration files, the ``when``
   allows now to check if a plugin is active. This allowed us to limit
   console warnings to only packages whose plugin was activated.

-  Plugins: Can now mark a plugin as a GUI toolkit responsible with the
   consequence that other toolkit detector plugins are all disabled, so
   when using ``tk-inter`` no longer will you be asked about ``PySide6``
   plugin, as that is not what you are using apparently.

-  Plugins: Generalized the GUI toolkit detection to include
   ``tk-inter`` as well, so it will now point out that ``wx`` and the Qt
   bindings should be removed for best results, if they are included in
   the compilation.

-  Plugins: Added ability to provide data files for macOS ``Resources``
   folder of application bundles.

-  macOS: Fix, Qt WebEngine was not working for framework using Python
   builds, like the ones from PyPI. This adds support for both PySide2
   and PySide6 to distribute those as well.

-  MSYS2: When asking a CPython installation to compress from the POSIX
   Python, it crashed on the main filename being not the same.

-  Scons: Fix, need to preserve environment attached modes when
   switching to winlibs gcc on Windows. This was observed with MSYS2,
   but might have effects in other cases too.

Optimization
============

-  Python3.10+: When creating dictionaries, lists, and tuples, we use
   the newly exposed dictionary free list. This can speedup code that
   repeatedly allocates and releases dictionaries by a lot.

-  Python3.6+: Added fast path to dictionary copy. Compact dictionaries
   have their keys and values copied directly. This is inspired by a
   Python3.10 change, but it is applicable to older Python as well, and
   so we did.

-  Python3.9+: Faster compiled object creation, esp. on Python platforms
   that use a DLLs for libpython, which is a given on Windows. This
   makes up for core changes that went unnoticed so far and should
   regain relative speedups to standard Python.

-  Python3.10+: Faster float operations, we use the newly exposed float
   free list. This can speed up all kinds of float operations that are
   not doable in-place by a lot.

-  Python3.8+: On Windows, faster object tracking is now available, this
   previously had to go through a DLL call, that is now removed in this
   way as it was for non-Windows only so far.

-  Python3.7+: On non-Windows, faster object tracking is now used, this
   was regressed when adding support for this version, becoming equally
   bad as all of Windows at the time. However, we now managed to restore
   it.

-  Optimization: Faster deep copy of mutable tuples and list constants,
   these were already faster, but e.g. went up from 137% gain factor to
   201% on Python3.10 as a result. We now use guided a deep copy, which
   then has the information, what types it is going to copy, removing
   the need to check through a dictionary.

-  Optimization: Also have own allocator function for fixed size
   objects. This accelerates allocation of compiled cells, dictionaries,
   some iterators, and lists objects.

-  More efficient code for object initialization, avoiding one DLL calls
   to set up our compiled objects.

-  Have our own ``PyObject_Size`` variant, that will be slightly faster
   and avoids DLL usage for ``len`` and size hints, e.g. in container
   creations.

-  Avoid using non-optimal ``malloc`` related macros and functions of
   Python, and instead of the fasted form generally. This avoids Python
   DLL calls that on Windows can be particularly slow.

-  Scalability: Generated child mixins are now used for the generated
   package metadata hard import nodes calls, and for all instances of
   single child tuple containers. These are more efficient for creation
   and traversal of the tree, directly improving the Python compile
   time.

-  Scalability: Slightly more efficient compile time constant property
   detections. For ``frozenset`` there was not need to check for
   hashable values, and some branches could be replaced with e.g.
   defining our own ``EllipsisType`` for use in short paths.

-  Windows: When using MSVC and LTO, the linking stage was done with
   only one thread, we now use the proper options to use all cores. This
   is controlled by ``--jobs`` much like C compilation already is. For
   large programs this will give big savings in overall execution time.
   Added in 1.2.7 already.

-  Anti-Bloat: Remove the use of ``pytest`` for ``dash`` package
   compilation.

-  Anti-Bloat: Remove the use of IPython for ``dotenv``, ``pyvista``,
   ``python_utils``, and ``trimesh`` package compilation.

-  Anti-Bloat: Remove IPython usage in ``rdkit`` improving compile time
   for standalone by a lot. Fixed in 1.2.7 already.

-  Anti-Bloat: Avoid ``keras`` testing framework when using that
   package.

Organisational
==============

-  Plugins: The ``numpy`` plugin functionality was moved to Nuitka
   package configuration, and as a result, the plugin is now deprecated
   and devoid of functionality. On non-Windows, this removes unused
   duplications of the ``numpy.core`` DLLs.

-  User Manual: Added information about macOS entitlements and Windows
   console. These features are supported very well by Nuitka, but needed
   documentation.

-  UI: Remove alternative options from ``--help`` output. These are
   there often only for historic reasons, e.g. when an option was
   renamed. They should not bother users reading them.

-  Plugins: Expose the mnemonics option to plugin warnings function, and
   use it for ``pyside2`` and ``pyqt5`` plugins.

-  Quality: Detect trailing/leading spaces in Nuitka package
   configuration ``description`` values during their automatic check.

-  UI: Detect the CPython official flavor on Windows by comparing to
   registry paths and consider real prefixes, when being used in
   virtualenv more often, e.g. when checking for CPython on Apple.

-  UI: Enhanced ``--version`` output to include the C compiler
   selection. It is doing that respecting your other options, e.g.
   ``--clang``, etc. so it will be helpful in debugging setup issues.

   UI: Some error messages were using ``%r`` rather than ``'%s'`` to
   output file paths, but that escaped backslashes on Windows, making
   them look worse, so we changed away from this.

-  UI: Document more clearly what ``--output-dir`` actually controls.

-  macOS: Added options hint that the ``Foundation`` module requires
   bundle mode to be usable.

-  UI: Allow using both ``--follow-imports`` and ``--nofollow-imports``
   on command line rather than erroring out. Simply use what was given
   last, this allows overriding what was given in project options tests
   should the need arise.

-  Reports: Include plugin reasons for pre and post load modules
   provided. This solves a TODO and makes it easier to debug plugins.

-  UI: Handle ``--include-package-data`` before compilation, removing
   the ability to use pattern. This makes it easier to recognize
   mistakes without a long compilation and plugins can know them this
   way too.

-  GitHub: Migration workflows to using newer actions for Python and
   checkout. Also use newer Ubuntu LTS for Linux test runner.

-  UI: Catch user error of running Nuitka with the ``pythonw`` binary on
   Windows.

-  UI: Make it clear that MSYS2 defaults to ``--mingw64`` mode. It had
   been like this, but the ``--help`` output didn't say so.

-  GitHub: Updated contribution guidelines for better readability.

-  GitHub: Use organisation URLs everywhere, some were still pointing to
   the personal rather than the organisation one. While these are
   redirected, it is not good to have them like this.

-  Mastodon: Added link to https://fosstodon.org/@kayhayen to the PyPI
   package and User Manual.

Cleanups
========

-  Nodes for hard import calls of package meta data now have their base
   classes fully automatically created, replacing what was previously
   manual code. This aims at making them more consistent and easier to
   add.

-  When adding the new Scons file for C compiler version output, more
   values that are needed for both onefile and backend compilation were
   moved to centralized code, simplifying these somewhat again.

-  Remove unused ``main_module`` tag. It cannot happen that a module
   name matches, and still thinks of itself as ``__main__`` during
   compilation, so that idea was unnecessary.

-  Generate the dictionary copy variants from template code rather than
   having manual duplications. For ``dict.copy()``, for deep copy
   (needed e.g. when there are escaping mutable keyword argument
   constant values in say a function call), and for ``**kw`` value
   preparation in the called function (checking argument types), we have
   had diverged copies, that are now unified in a single Jinja2 template
   for optimization.

-  Plugins: Also allow providing generators for providing extra DLLs
   much like we already do for data files.

-  Naming of basic tests now makes sure to use a ``Test`` suffix, so in
   Visual Code selector they are more distinct from Nuitka code modules.

-  Rather than populating empty dictionaries, helper code now uses
   factory functions to create them, passing keys and values, and
   allowing values to be optional, removing noisy ``if`` branches at
   call side.

-  Removed remaining ``PyDev`` annotations, we don't need those anymore
   for a long time already.

-  Cleanup, avoid lists objects for ctypes defined functions and their
   ``arglist``, actually tuples are sufficient and naturally better to
   use.

-  Spelling cleanups were resumed, as an ongoing action.

Tests
=====

-  Added construct test that demonstrates the mutable constant argument
   passing for lists to see the performance gains in this area too.

-  Made construct runner ``--diff`` output usable for interactive usage.

-  Repaired Nuitka Speedcenter, but it's not yet too usable for general
   consumption. More work will be needed there, esp. to make comparisons
   more accessible for the general public.

Summary
=======

The major achievement of this release was the removal of the long lived
``numpy`` plug-in, replacing it with package based configuration, that
is even more optimal and works perfectly across all platforms on both
important package installation flavors.

This release has a lot of consolidation efforts, but also as a result of
3.11 investigations, addresses a lot of issues, that have crept in over
time with Python3 releases since 3.7, each time, something had not been
noticed. There will more need for investigation of relative performance
losses, but this should address the most crucial ones, and also takes
advantage of optimization that had become with 3.10 already.

There is also some initial results from cleanups with the composite node
tree structure, and how it is managed. Generated "child(ren) having"
mixins, allow for faster traversal of the node tree.

Some technical things also improved in Scons. Using multiple cores in
LTO with MSVC with help this a lot, although for big compilations
``--lto=no`` probably has to be recommended still.

More ``anti-bloat`` work on more packages rounds up the work.

For macOS specifically, the WebEngine support is crucial to some users,
and the new ``--macos-app-mode`` with more GUI friendly default resolves
long standing problems in this area.

And for MSYS2 and FreeBSD, support has been re-activated, so now 4 OSes
work extremely well (others too likely), and on those, most Python
flavors work well.

The performance and scalability improvements are going to be crucial.
It's a pity that 3.11 is not yet supported, but we will be getting
there.

********************
 Nuitka Release 1.2
********************

This release contains a large amount of new compatibility features and a
few new optimization, while again consolidating what we have.
Scalability should be better in many cases.

Bug Fixes
=========

-  Standalone: Added implicit dependency of ``thinc`` backend. Fixed in
   1.1.1 already.

-  Python3.10: Fix, ``match`` statements with unnamed star matches could
   give incorrect results. Fixed in 1.1.1 already.

      .. code:: python

         match x:
            case [*_, y]:
                  ... # y had wrong value here.

-  Python3.9+: Fix, file reader objects must convert to ``str`` objects.
   Fixed in 1.1.1 already.

      .. code:: python

         # This was the `repr` rather than a path value, but it must be usable
         # like that too.
         str(importlib.resources.files("package_name").joinpath("lala"))

-  Standalone: Added data file of ``echopype`` package. Fixed in 1.1.1
   already.

-  Anti-Bloat: Remove non-sense warning of compiled ``pyscf``. Fixed in
   1.1.1 already.

-  macOS: Fix, in LTO mode using ``incbin`` can fail, switch to source
   mode for constants resources. Fixed in 1.1.2 already.

-  Standalone: Add support for ``sv_ttk`` module. Fixed in 1.1.2
   already.

-  macOS: Fix, was no longer correcting ``libpython`` path, this was a
   regression preventing CPython for creating properly portable binary.
   Fixed in 1.1.2 already.

-  macOS: Fix, main binary was not included in signing command. Fixed in
   1.1.3 already.

-  Standalone: Added implicit dependency of ``orjson``. Due to
   ``zoneinfo`` not being automatically included anymore, this was
   having a segfault. Fixed in 1.1.3 already.

-  Standalone: Added support for new ``shapely``. Fixed in 1.1.4
   already.

-  macOS: Ignore extension module of non-matching architecture. Some
   wheels contain extension modules for only ``x86_64`` arch, and others
   contain them only for ``arm64``, preventing the standalone build.
   Fixed in 1.1.4 already.

-  Standalone: Added missing ``sklearn`` dependencies. Fixed in 1.1.4
   already.

-  Fix, packages available through relative import paths could be
   confused with the same ones imported by absolute paths. This should
   be very hard to trigger, by normal users, but was seen during
   development. Fixed in 1.1.4 already.

-  Standalone: Apply import hacks for ``pywin32`` modules only on
   Windows, otherwise it can break e.g. macOS compilation. Fixed in
   1.1.4 already.

-  Windows: More robust DLL dependency caching, otherwise e.g. a Windows
   update can break things. Also consider plugin contribution, and
   Nuitka version, to be absolutely sure, much like we already do for
   bytecode caching. Fixed in 1.1.4 already.

-  Standalone: Fix, ``seaborn`` needs the same workaround as ``scipy``
   for corruption with MSVC. Fixed in 1.1.4 already.

-  UI: Fix, the ``options-nanny`` was no longer functional and therefore
   failed to warn about non working options and package usages. Fixed in
   1.1.5 already.

-  macOS: Do not use extension modules of non-matching architecture.
   Fixed in 1.1.5 already.

-  Windows: Fix, resolving symlinks could fail for spaces in paths.
   Fixed in 1.1.6 already.

-  Standalone: Added missing DLL for ``lightgbm`` module. Fixed in 1.1.6
   already.

-  Compatibility: Respect ``super`` module variable. It is now possible
   to have a module level change of ``super`` but still get compatible
   behavior with Nuitka. Fixed in 1.1.6 already.

-  Compatibility: Make sure we respect ``super`` overloads in the
   builtin module. Fixed in 1.1.6 already.

-  Fix, the anti-bloat replacement code for ``numpy.testing`` was
   missing a required function. Fixed in 1.1.6 already.

-  Fix, ``importlib.import_module`` static optimization was mishandling
   a module name of ``.`` with a package name given. Fixed in 1.1.6
   already.

-  macOS: Fix, some extension modules use wrong suffixes in self
   references, we need to not complain about this kind of error. Fixed
   in 1.1.6 already.

-  Fix, do not make ``ctypes.wintypes`` a hard import on non-Windows.
   Nuitka asserted against it failing, where some code handles it
   failing on non-Windows platforms. Fixed in 1.1.6 already.

-  Standalone: Added data files for ``vedo`` package. Fixed in 1.1.7
   already.

-  Plugins: Fix, the ``gi`` plugin did always set ``GI_TYPELIB_PATH``
   even if already present from user code. Also it did not handle errors
   to detect its value during compile time. Fixed in 1.1.7 already.

-  Standalone: Added missing dependencies for ``sqlalchemy`` to have all
   SQL backends working. Fixed in 1.1.7 already.

-  Added support Nixpkgs's default non-writable ``HOME`` directory.
   Fixed in 1.1.8 already.

-  Fix, distribution metadata name and package name need not align, need
   to preserve the original looked up name from
   ``importlib.metadata.distribution`` call. Fixed in 1.1.8 already.

-  Windows: Fix, catch usage of unsupported ``CLCACHE_MEMCACHED`` mode
   with MSVC compilation. It is just unsupported.

-  Windows: Fix, file version was spoiled from product version if it was
   the only version given.

-  Windows: The default for file description in version information was
   not as intended.

-  Plugins: Workaround for PyQt5 as contained in Anaconda providing
   wrong paths from the build machine.

-  macOS: After signing a binary with a certificate, compiling the next
   one was crashing on a warning about initially creating an ad-hoc
   binary.

-  Fix, detect case of non-writable cache path, make explaining error
   exit rather than crashing attempting to write to the cache.

-  macOS: Added support for ``pyobjc`` in version 9.0 or higher.

New Features
============

-  Python3.11: For now prevent the execution with 3.11 and give a
   warning to the user for a not yet supported version. This can be
   overridden with ``--experimental=python311`` but at this times will
   not compile anything yet due to required and at this time missing
   core changes.

-  macOS: Added option ``--macos-sign-notarization`` that signs with
   runtime signature, but requires a developer certificate from Apple.
   As its name implies, this is for use with notarization for their App
   store.

-  DLLs used via ``delvewheel`` were so far only handled in the ``zmq``
   plugin, but this has been generalized to cover any package using it.
   With that, e.g. ``shapely`` just works. This probably helps many
   other packages as well.

-  Added ``__compiled__`` and ``__compiled_constant__`` attributes to
   compiled functions.

   With this, it can be decided per function what it is and bridges like
   ``pyobjc`` can use it to create better code on their side for
   constant value returning functions.

-  Added ``support_info`` check to Nuitka package format. Make it clear
   that ``pyobjc`` is only supported after ``9.0`` by erroring out if it
   has a too low version. It will not work at all before that version
   added support in upstream. Also using this to make it clear that
   ``opencv-python`` is best supported in version 4.6 or higher. It
   seems e.g. that video capture is not working with 4.5 at this time.

-  Added ``--report-template`` which can be used to provide Jinja2
   templates to create custom reports, and refer to built-in reports, at
   this time e.g. a license reports.

Optimization
============

-  Trust the absence of a few selected hard modules and convert those to
   static raises of import errors.

-  For conditional nodes where only one branch exits, and the other does
   not, no merging of the trace collection should happen. This should
   enhance the scalability and leads to more static optimization being
   done after these kinds of branches on variables assigned in such
   branches.

   .. code:: python

      if condition1:
         a = 1
      else:
         raise KeyError

      if condition2:
         b = 1

      # Here, "a" is known to be assigned, but before it was only "maybe"
      # assigned, like "b" would have to be since, the branch may or may
      # not have been taken.

-  Do not merge tried blocks that are aborting with an exception handler
   that is not aborting. This is very similar to the change for
   conditional statements, again there is a control flow branch, that
   may have to be merged with an optional part, but sometimes that part
   is not optional from the perspective of the code following.

   .. code:: python

      try:
         ... # potentially raising, but not aborting code
         return something() # this aborts
      except Exception:
         a = 1

      try:
         ... # potentially raising, but not aborting code
      except Exception:
         b = 1

      # Here, "a" is known to be assigned, but before it was only "maybe"
      # assigned, like "b" would have to be since, the branch may or may
      # not have been taken.

-  Exception matches were annotating a control flow escape and an
   exception exit, even when it is known that no error is possible to be
   happening that comparison.

   .. code:: python

      try:
         ...
      except ImportError: # an exception match is done here, that cannot raise
         ...

-  Trust ``importlib.metadata.PackageNotFoundError`` to exist, with this
   some more metadata usages are statically optimized. Added in 1.1.4
   already.

-  Handle constant values from trusted imports as trusted values. So
   far, trusted import values were on equal footing to regular
   variables, which on the module level could mean that no optimization
   was done, due to control flow escapes happening.

   .. code:: python

      # Known to be False at compile time.
      from typing import TYPE_CHECKING
      ...

      if TYPE_CHECKING:
         from something import normally_unused_unless_type_checking

   In this code example above, the static optimization was not done
   because the value may be changed on the outside. However, for trusted
   constants, this is no longer assumed to be happening. So far only
   ``if typing.TYPE_CHECKING:`` using code had been optimized.

-  macOS: Use sections for main binary constants binary blob rather than
   C source code (which we started in a recent hotfix due to LTO issues
   with incbin) and onefile payload. The latter enables notarization of
   the onefile binary as well and makes it faster to unpack as well.

-  Windows: Do not include DLLs from SxS. For PyPI packages these are
   generally unused, and self compiled modules won't be SxS
   installations either. We can add it back where it turns out needed.
   This avoids including ``comctl32`` and similar DLLs, which ought to
   come from the OS, and might impede backward compatibility only.

-  Disabled C compilation of very large ``azure`` modules.

-  The per module usage information of other modules was only updated in
   first pass was used in later passes. But since they can get optimized
   away, we have to update every time, avoiding to still include unused
   modules.

-  Anti-Bloat: Fight the use of ``dask`` in ``xarray`` and ``pint``,
   adding a mode controlling its use. This is however still incomplete
   and needs more work.

-  Fix, the anti-bloat configuration for ``rich.pretty`` introduced a
   ``SyntaxError`` that went unnoticed. In the future compilation will
   abort when this happens.

-  Standalone: Added support for including DLLs of ``llvmlite.binding``
   package.

-  Anti-Bloat: Avoid using ``pywin32`` through ``pkg_resources`` import.
   This seems rather pointless and follows an optimization done for the
   inline copy of Nuitka already, the ``ctypes`` code path works just
   fine, and this may well be the only reason why ``pywin32`` is
   included, which is by itself relatively large.

-  Cache directory contents when scanning for modules. The ``sys.path``
   and package directories were listed over and over, wasting time
   during the import analysis.

-  Optimization: Was not caching not found modules, but retrying every
   time for each usage, potentially wasting time during import analysis.

-  Anti-Bloat: Initial work to avoid ``pytest`` in patsy, it is however
   incomplete.

Organisational
==============

-  User Manual: Explain how to create 64/32 bits binaries on Windows,
   with there being no option to control it, this can otherwise be a bit
   unobvious that you have to just use the matching Python binary.

-  UI: Added an example for a cached onefile temporary location spec to
   the help output of ``--onefile-tempdir-spec`` to make cached more
   easy to achieve in the proper way.

-  UI: Quote command line options with space in value better, no need to
   quote an affected command line option in its entirety, and it looks
   strange.

-  macOS: Catch user error of disabling the console without using the
   bundle mode, as it otherwise it has no effect.

-  macOS: Warn about not providing an icon with disabled console,
   otherwise the dock icon is empty, which just looks bad.

-  Debian: Also need to depend on ``glob2`` packages which the yaml
   engine expects to use when searching for DLLs.

-  Debian: Pertain inline copies of modules in very old builds, there is
   e.g. no ``glob2`` for older releases, but only recent Debian releases
   need very pure packages, our backport doesn't have to do it right.

-  macOS: More reliable detection of Homebrew based Python. Rather than
   checking file system via its ``sitecustomize`` contents. The
   environment variables are only present to some usages.

-  Installations with pip did not include all license, README files,
   etc. which however was intended. Also the attempt to disable bytecode
   compilation for some inline copies was not effective yet.

-  Renamed ``pyzmq`` plugin to ``delvewheel`` as it is now absolutely
   generic and covers all uses of said packaging technique.

-  Caching: Use cache directory for cached downloads, rather than
   application directory, which is just wrong. This will cause all
   previously cached downloads to become unused and repeated.

-  Quality: Updated development requirements to latest ``black``,
   ``isort``, ``yamllint``, and ``tqdm``.

-  Visual Code: Added recommendation for extension for Debian packaging
   files.

-  Added warning for ``PyQt5`` usage, since its support is very
   incomplete. Made the ``PyQt6`` warning more concrete. It seems only
   Qt threading does not work, which is of course still significant.
   Instead PySide2 and PySide6 are recommended.

-  UI: Have dedicated options group for onefile, the spec for the
   temporary files is not a Windows option at all anymore. Also move the
   warnings group to the end, people need to see the inclusion related
   group first.

-  User Manual: Explain how to create 64/32 bits binaries on Windows,
   which is not too obvious.

Cleanups
========

-  Moved PySide plugins DLL search extra paths to the Yaml
   configuration. In this way it is not dependent on the plugin being
   active, avoiding cryptic errors on macOS when they are not found.

-  Plugins: Avoid duplicate link libraries due to casing. We are now
   normalizing the link library names, which avoids e.g. ``Shell32`` and
   ``shell32`` to be in the result.

-  Cleanups to prepare a PyLint update that so otherwise failed due to
   encountered issues.

-  Plugins: Pass so called build definitions for generically. Rather
   than having dedicated code for each, and plugins can now provide them
   and pass their index to the scons builds.

-  Onefile: Moved file handling code to common code reducing code
   duplication and heavily cleaning up the bootstrap code generally.

-  Onefile: The CRC32 checksum code was duplicated between constants
   blob and onefile, and has moved to shared code, with an actual
   interface to take the checksum.

-  Spelling cleanups resumed, e.g. this time more clearly distinguishing
   between ``run time`` and ``runtime``, the first is when the program
   executes, but the latter can be an environment provided by a C
   compiler.

Tests
=====

-  Tests: Added test that applies anti-bloat configuration to all found
   modules.

-  Tests: Tests: Avoid including unused ``nuitka.tools`` code in
   reflected test, which should make it faster. The compiler itself
   doesn't use that code.

Summary
=======

This release is again mainly a consolidation of previous release, as
well as finishing off existing features. Optimization added in previous
releases should have all regressions fixed now, again with a strong
series of hotfixes.

New optimization was focused around findings with static optimization
not being done, but still resulting in general improvements. Letting
static optimization drive the effort is still paying off.

Scalability has seen improvements through some of the optimization, this
time a lot less anti-bloat work has been done, and some things are only
started. The focus will clearly now shift to making this a community
effort. Expect postings that document the Yaml format we use.

For macOS specifically, with the sections work, onefile should launch
faster, should be more compatible with signing, and can now be used in
notarization, so for that platform, things are more round.

For Windows, a few issues with version information and onefile have been
addressed. We should be able to use memory mapped view on this platform
too, for faster unpacking of the payload, since it doesn't have to go
through the file anymore.

********************
 Nuitka Release 1.1
********************

This release contains a large amount of new compatibility features,
while consolidating what we have. Scalability should be better in some
cases.

Bug Fixes
=========

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

New Features
============

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

Optimization
============

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

Organisational
==============

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

Cleanups
========

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

Tests
=====

-  Added coverage for comparisons that need argument swaps.

-  Allow more time in onefile keyboard signal test, otherwise it can be
   a race on slow machines, e.g. emulated machines.

-  Tests: Added support for running a local web server.

Summary
=======

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

********************
 Nuitka Release 1.0
********************

This release contains a large amount of new features, while
consolidating what we have with many bug fixes. Scalability should be
dramatically better, as well as new optimization that will accelerate
some code quite a bit. See the summary, how this release is paving the
way forward.

Bug Fixes
=========

-  Python3: Fix, ``bytes.decode`` with only ``errors`` argument given
   was not working. Fixed in 0.9.1 already.

-  MSYS2: Fix, the accelerate mode ``.cmd`` file was not working
   correctly. Fixed in 0.9.1 already.

-  Onefile: Fix, the bootstrap when waiting for the child, didn't
   protect against signals that interrupt this call. This only affected
   users of the non-public ``--onefile-tempdir`` option on Linux, but
   with that becoming the default in 1.0, this was discovered. Fixed in
   0.9.1 already.

-  Fix, ``pkg_resources`` compile time generated ``Distribution`` values
   could cause issues with code that put it into calls, or in tried
   blocks. Fixed in 0.9.1 already.

-  Standalone: Added implicit dependencies of ``Xlib`` package. Fixed in
   0.9.1 already.

-  macOS: Fix, the package configuration for ``wx`` had become invalid
   when restructuring the Yaml with code and schema disagreeing on
   allowed values. Fixed in 0.9.1 already.

-  Fix: The ``str.format`` with a single positional argument didn't
   generate proper code and failed to compile on the C level. Fixed in
   0.9.1 already.

-  Fix, the type shape of ``str.count`` result was wrong. Fixed in 0.9.1
   already.

-  UI: Fix, the warning about collision of just compiled package and
   original package in the same folder hiding the compiled package
   should not apply to packages without an ``__init__.py`` file, as
   those do **not** take precedence. Fixed in 0.9.2 already.

-  Debugging: Fix, the fallback to ``lldb`` from ``gdb`` when using the
   option ``--debugger`` was broken on anything but Windows. Fixed in
   0.9.2 already.

-  Python3.8: The module ``importlib.metadata`` was not recognized
   before 3.9, but actually 3.8 already has it, causing the compile time
   resolution of package versions to not work there. Fixed in 0.9.3
   already.

-  Standalone: Fix, at least on macOS we should also scan from parent
   folders of DLLs, since they may contain sub-directories in their
   names. This is mostly the case, when using frameworks. Fixed in 0.9.2
   already.

-  Standalone: Added package configuration for ``PyQt5`` to require
   onefile bundle mode on macOS, and recommend to disable console for
   PyQt6. This is same as we already do for ``PySide2`` and ``PySide6``.
   Fixed in 0.9.2 already.

-  Standalone: Removed stray macOS onefile bundle package configuration
   for ``pickle`` module which must have been added in error. Fixed in
   0.9.2 already.

-  UI: Catch user error of attempting to compile the ``__init__.py``
   rather than the package directory. Fixed in 0.9.2 already.

-  Fix, hard name import nodes failed to clone, causing issues in
   optimization phase. Fixed in 0.9.2 already.

-  Fix, avoid warnings given with gcc 11. Fixed in 0.9.2 already.

-  Fix, dictionary nodes where the operation itself has no effect, e.g.
   ``dict.copy`` were not properly annotating that their dictionary
   argument could still cause a raise and have side effects, triggering
   an assertion violation in Nuitka. Fixed in 0.9.2 already.

-  Standalone: Added ``pynput`` implicit dependencies on Linux. Fixed in
   0.9.2 already.

-  Fix, boolean condition checks on variables converted immutable
   constant value assignments to boolean values, leading to incorrect
   code execution. Fixed in 0.9.2 already.

-  Python3.9: Fix, could crash on generic aliases with non-hashable
   values. Fixed in 0.9.3 already.

   .. code:: python

      dict[str:any]

-  Python3: Fix, an iteration over ``sys.version_info`` was falsely
   optimized into a tuple, which is not always compatible. Fixed in
   0.9.3 already.

-  Standalone: Added support for ``xgboost`` package. Fixed in 0.9.3
   already.

-  Standalone: Added data file for ``text_unidecode`` package. Fixed in
   0.9.4 already.

-  Standalone: Added data files for ``swagger_ui_bundle`` package. Fixed
   in 0.9.4 already.

-  Standalone: Added data files for ``connexion`` package. Fixed in
   0.9.4 already.

-  Standalone: Added implicit dependencies for ``sklearn.utils`` and
   ``rapidfuzz``. Fixed in 0.9.4 already.

-  Python3.10: Fix, the reformulation of ``match`` statements could
   create nodes that are used twice, causing code generation to assert.
   Fixed in 0.9.4 already.

-  Fix, module objects removed from ``sys.modules`` but still used could
   lack a reference to themselves, and therefore crash due to working on
   a released module variables dictionary. Fixed in 0.9.5 already.

-  Fix, the MSVC compiles code generated for SciPy 1.8 wrongly. Added a
   workaround for that code to avoid triggering it. Fixed in 0.9.6
   already.

-  Fix, calls to ``str.format`` where the result is not used, could
   crash the compiler during code generation. Fixed in 0.9.6 already.

-  Standalone: For DLLs on macOS and Anaconda, also consider the ``lib``
   directory of the root environment, as some DLLs are otherwise not
   found.

-  Fix, allow ``nonlocal`` and ``global`` for ``__class__`` to be used
   on the class level.

-  Fix, ``xrange`` with large values didn't work on all platforms. This
   affected at least Python2 on macOS, but potentially others as well.

-  Windows: When scanning for installed Pythons to e.g. run Scons or
   onefile compression, it was attempting to use installations that got
   deleted manually and could crash.

-  macOS: Fix, DLL conflicts are now resolved by checking the version
   information too, also all cases that previously errored out after a
   conflict was reported, will now work.

-  Fix, conditional expressions whose statically decided condition
   picking a branch will raise an exception could crash the compilation.

   .. code:: python

      # Would previously crash Nuitka during optimization.
      return 1/0 if os.name == "nt" else 1/0

-  Windows: Make sure we set C level standard file handles too

   At least newer subprocess was affected by this, being unable to
   provide working handles to child processes that pass their current
   handles through, and also this should help DLL code to use it as
   level.

-  Standalone: Added support for ``pyqtgraph`` data files.

-  Standalone: Added support for ``dipy`` by anti-bloat removal of its
   testing framework that wants to do unsupported stuff.

-  UI: Could still give warnings about modules not being followed, where
   that was not true.

-  Fix, ``--include-module`` was not working for non-automatic standard
   library paths.

New Features
============

-  Onefile: Recognize a non-changing path from
   ``--onefile-tempdir-spec`` and then use cached mode. By default a
   temporary folder is used in the spec value, make it delete the files
   afterwards.

   The cached mode is not necessarily faster, but it is not going to
   change files already there, leaving the binaries there intact. In the
   future it may also become faster to execute, but right now checking
   the validity of the file takes about as long as re-creating it,
   therefore no gain yet. The main point, is to not change where it runs
   from.

-  Standalone: Added option to exclude DLLs. You can npw use
   ``--noinclude-dlls`` to exclude DLLs by filename patterns.

   The may e.g. come from Qt plugins, where you know, or experimented,
   that it is not going to be used in your specific application. Use
   with care, removing DLLs will lead to very hard to recognize errors.

-  Anaconda: Use ``CondaCC`` from environment variables for Linux and
   macOS, in case it is installed. This can be done with e.g. ``conda
   install gcc_linux-64`` on Linux or ``conda install clang_osx-64`` on
   macOS.

-  Added new option ``--nowarn-mnemonic`` to disable warnings that use
   mnemonics, there is currently not that many yet, but it's going to
   expand. You can use this to acknowledge the ones you accept, and not
   get that warning with the information pointer anymore.

-  Added method for resolving DLL conflicts on macOS too. This is using
   version information and picks the newer one where possible.

-  Added option ``--user-package-configuration-file`` for user provided
   Yaml files, which can be used to provide package configuration to
   Nuitka, to e.g. add DLLs, data files, do some anti-bloat work, or add
   missing dependencies locally. The documentation for this does not yet
   exist though, but Nuitka contains a Yaml schema in the
   ``misc/nuitka-package-config-schema.json`` file.

-  Added ``nuitka-project-else`` to avoid repeating conditions in Nuitka
   project configuration, this can e.g. be used like this:

   .. code:: python

      # nuitka-project-if: os.getenv("TEST_VARIANT", "pyside2") == "pyside2":
      #   nuitka-project: --enable-plugin=no-qt
      # nuitka-project-else:
      #   nuitka-project: --enable-plugin=no-qt
      #   nuitka-project: --noinclude-data-file=*.svg

   Previously, the inverted condition had to be used in another
   ``nuitka-project-if`` which is no big deal, but less readable.

-  Added support for deep copying uncompiled functions. There is now a
   section in the User Manual that explains how to clone compiled
   functions. This allows a workaround like this:

   .. code:: python

      def binder(func, name):
         try:
            result = func.clone()
         except AttributeError:
            result = types.FunctionType(func.__code__, func.__globals__, name=func.__name__, argdefs=func.__defaults__, closure=func.__closure__)
            result = functools.update_wrapper(result, func)
            result.__kwdefaults__ = func.__kwdefaults__

         result.__name__ = name
         return result

-  Plugins: Added explicit deprecation status of a plugin. We now have a
   few that do nothing, and are just there for compatibility with
   existing users, and this now informs the user properly rather than
   just saying it is not relevant.

-  Fix, some Python installations crash when attempting to import
   modules, such as ``os`` with a ``ModuleName`` object, because we
   limit string operations done, and e.g. refuse to do ``.startswith``
   which of course, other loaders that your installation has added,
   might still use.

-  Windows: In case of not found DLLs, we can still examine the run time
   of the currently compiling Python process of Nuitka, and locate them
   that way, which helps for some Python configurations to support
   standalone, esp. to find CPython DLL in unusual spots.

-  Debian: Workaround for ``lib2to3`` data files. These are from stdlib
   and therefore the patched code from Debian needs to be undone, to
   make these portable again.

Optimization
============

-  Scalability: Avoid merge traces of initial variable versions, which
   came into play when merging a variable used in only one branch. These
   are useless and only made other optimization slower or impossible.

-  Scalability: Also avoid merge traces of merge traces, instead flatten
   merge traces and avoid the duplication doing so. There were
   pathological cases, where this reduced optimization time for
   functions from infinite to instant.

-  For comparison helpers, switch comparison where possible, such that
   there are only 3 variants, rather than 6. Instead the boolean result
   is inverted, e.g. changing ``>=`` into ``not <`` effectively. Of
   course this can only be done for types, where we know that nothing
   special, i.e. no method overloads of ``__gte__`` is going on.

-  For binary operations that are commutative with the selected types,
   in mixed type cases, swap the arguments during code generation, such
   that e.g. ``long_a + float_b`` is actually computed as ``float_b +
   long_a``. This again avoids many helpers. It also can be done for
   ``*`` with integers and container types.

-  In cases, where a comparison (or one of the few binary operation
   where we consider it useful), is used in a boolean context, but we
   know it is impossible to raise an exception, a C boolean result type
   is used rather than a ``nuitka_bool`` which is now only used when
   necessary, because it can indicate the exception result.

-  Anti-Bloat: More anti-bloat work was done for popular packages,
   covering also uses of ``setuptools_scm``, ``nose`` and ``nose2``
   package removals and warnings. There was also a focus on making
   ``mmvc``, ``tensorflow`` and ``tifffile`` compile well, removing e.g.
   the uses of the tensorflow testing framework.

-  Faster comparison of ``int`` values with constant values, this uses
   helpers that work with C ``long`` values that represent a single
   "digit" of a value, or ones that use the full value space of C
   ``long``.

-  Faster comparison of ``float`` values with constant values, this uses
   helpers that work with C ``float`` values, avoiding the useless
   Python level constant objects.

-  Python2: Comparison of ``int`` and ``long`` now has specialized
   helpers that avoids converting the ``int`` to a ``long`` through
   coercion. This takes advantage of code to compare C ``long`` values
   (which are at the core of Python2 ``int`` objects, with ``long``
   objects.

-  For binary operation on mixed types, e.g. ``int * bytes`` the slot of
   the first function was still considered, and called to give a
   ``Py_NotImplemented`` return value for no good reason. This also
   applies to mixed operations of ``int``, ``long``, and ``float``
   types, and for ``str`` and ``unicode`` values on Python2.

-  Added missing helper for ``**`` operation with floats, this had been
   overlooked so far.

-  Added dedicated nodes for ``ctypes.CDLL`` which aims to allow us to
   detect used DLLs at compile time in the future, and to move closer to
   support its bindings more efficiently.

-  Added specialized nodes for ``dict.popitem`` as well. With this, now
   all of the dictionary methods are specialized.

-  Added specialized nodes for ``str.expandtabs``, ``str.translate``,
   ``str.ljust``, ``str.rjust``, ``str.center``, ``str.zfill``, and
   ``str.splitlines``. While these are barely performance relevant, this
   completes all ``str`` methods, except ``removeprefix`` and
   ``removesuffix`` that are Python3.9 or higher.

-  Added type shape for result of ``str.index`` operation as well, this
   was missing so far.

-  Optimize ``str``, ``bytes`` and ``dict`` method calls through
   variables.

-  Optimize calls through variables containing e.g. mutable constant
   values, these will be rare, because they all become exceptions.

-  Optimize calls through variables containing built-in values,
   unlocking optimization of such calls, where it is assigned to a local
   variable.

-  For generated attribute nodes, avoid local doing import statements on
   the function level. While these were easier to generate, they can
   only be slow at run time.

-  For the ``str`` built-in annotate its value as derived from ``str``,
   which unfortunately does not allow much optimization, since that can
   still change many things, but it was still a missing attribute.

-  For variable value release nodes, specialize them by value type as
   well, enhancing the scalability, because e.g. parameter variable
   specific tests, need not be considered for all other variable types
   as well.

Organisational
==============

-  Plugins: Major changes to the Yaml file content, cleaning up some of
   the DLL configuration to more easy to use.

   The DLL configuration has two flavors, one from code and one from
   filename matching, and these got separated into distinct items in the
   Yaml configuration. Also how source and dest paths get provided got
   simplified, with a relative path now being used consistently and with
   sane defaults, deriving the destination path from where the module
   lives. Also what we called patterns, are actually prefixes, as there
   is still the platform specific DLL file naming appended.

-  Plugins: Move mode checks to dedicated plugin called
   ``options-nanny`` that is always enabled, giving also much cleaner
   Yaml configuration with a new section added specifically for these.
   It controls advice on the optional or required use of
   ``--disable-console`` and the like. Some packages, e.g. ``wx`` are
   known to crash on macOS when the console is enabled, so this advice
   is now done with saner configuration.

-  Plugins: Also for all Yaml configuration sub-items where is now a
   consistent ``when`` field, that allows checking Python version, OS,
   Nuitka modes such as standalone, and only apply configuration when
   matching this criterion, with that the anti-bloat options to allow
   certain bloat, should now have proper effect as well.

-  The use of ``AppImage`` on Linux is no more. The performance for
   startup was always slower, while having lost the main benefit of
   avoiding IO at startup, due to new cached mode, so now we always use
   the same bootstrap binary as on macOS and Windows.

-  UI: Do not display implicit reports reported by plugins by default
   anymore. These have become far too many, esp. with the recent stdlib
   work, and often do not add any value. The compilation report will
   become where to turn to find out why a module in included.

-  UI: Ask the user to install the ordered set package that will
   actually work for the specific Python version, rather than making him
   try one of two, where sometimes only one can work, esp. with Python
   3.10 allowing only one.

-  GitHub: More clear wording in the issue template that ``python -m
   nuitka --version`` output is really required for support to given.

-  Attempt to use Anaconda ``ccache`` binary if installed on
   non-Windows. This is esp. handy on macOS, where it is harder to get
   it.

-  Windows: Avoid byte-compiling the inline copy of Scons that uses
   Python3 when installing for Python2.

-  Added experimental switches to disable certain optimization in order
   to try out their impact, e.g. on corruption bugs.

-  Reports: Added included DLLs for standalone mode to compilation
   report.

-  Reports: Added control tags influencing plugin decisions to the
   compilation report.

-  Plugins: Make the ``implicit-imports`` dependency section in the Yaml
   package configuration a list, for consistency with other blocks.

-  Plugins: Added checking of tags such from the package configuration,
   so that for things dependent on python version (e.g.
   ``python39_or_higher``, ``before_python39``), the usage of Anaconda
   (``anaconda``) or certain OS (e.g. ``macos``), or modes (e.g.
   ``standalone``), expressions in ``when`` can limit a configuration
   item.

-  Quality: Re-enabled string normalization from black, the issues with
   changes that are breaking to Python2 have been worked around.

-  User Manual: Describe using a minimal virtualenv as a possible help
   low memory situations as well.

-  Quality: The yaml auto-format now properly preserves comments, being
   based on ``ruamel.yaml``.

-  Nuitka-Python: Added support for the Linux build with Nuitka-Python
   for our own CPython fork as well, previously only Windows was
   working, amd macOS will follow later.

-  The commit hook when installed from git bash was working, but doing
   so from ``cmd.exe`` didn't find a proper path for shell from the
   ``git`` location.

-  Debugging: A lot of experimental toggles were added, that allow
   control over the use of certain optimization, e.g. use of dict, list,
   iterators, subscripts, etc. internals, to aid in debugging in
   situations where it's not clear, if these are causing the issue or
   not.

-  Added support for Fedora 36, which requires some specific linker
   options, also recognize Fedora based distributions as such.

-  Removed long deprecated option ``--noinclude-matplotlib`` from numpy
   plugin, as it hasn't had an effect for a long time now.

-  Visual Code: Added extension for editing Jinja2 templates. This one
   even detects that we are editing C or Python and properly highlights
   accordingly.

Cleanups
========

-  Standalone: Major cleanup of the dependency analysis for standalone.
   There is no longer a distinction between entry points (main binary,
   extension modules) and DLLs that they depend on. The OS specific
   parts got broken out into dedicated modules as well and decisions are
   now taken immediately.

-  Plugins: Split the Yaml package configuration files into 3 files. One
   contains now Python2 only stdlib configuration, and another one
   general stdlib.

-  Plugins: Also cleanup the ``zmq`` plugin, which was one the last
   holdouts of now removed plugin method, moving parts to the Yaml
   configuration. We therefore no longer have ``considerExtraDlls``
   which used to work on the standalone folder, but instead only plugin
   code that provides included DLL or binary objects from
   ``getExtraDlls`` which gives Nuitka much needed control over DLL
   copying. This was a long lasting battle finally won, and will allow
   many new features to come.

-  UI: Avoid changing whitespace in warnings, where we have intended
   line breaks, e.g. in case of duplicate DLLs. Went over all warnings
   and made sure to either avoid new-lines or have them, depending on
   wanted output.

-  Iterator end check code now uses the same code as rich comparison
   expressions and can benefit from optimization being done there as
   well.

-  Solved TODO item about code generation time C types to specify if
   they have error checking or not, rather than hard coding it.

-  Production of binary helper function set was cleaned up massively,
   but still needs more work, comparison helper function set was also
   redesigned.

-  Changing the spelling of our container package to become more clear.

-  Used ``namedtuple`` objects for storing used DLL information for more
   clear code.

-  Added spellchecker ignores for all attribute and argument names of
   generated fixed attribute nodes.

-  In auto-format make sure the imports float to the top. That very much
   cleans up generated attribute nodes code, allowing also to combine
   the many ones it makes, but also cleans up some of our existing code.

-  The package configuration Yaml files are now sorted according to
   module names. This will help to avoid merge conflicts during hotfixes
   merge back to develop and automatically group related entries in a
   sane way.

-  Moved large amounts of code producing implicit imports to Yaml
   configuration files.

-  Changed the ``tensorflow`` plugin to Yaml based configuration, making
   it a deprecated do nothing plugin, that only remains there for a few
   releases, to not crash existing build scripts.

-  Lots of spelling cleanups, e.g. renaming ``nuitka.codegen`` to
   ``nuitka.code_generation`` for clarity.

Tests
=====

-  Added generated test to cover ``bytes`` method. This would have found
   the issue with ``decode`` potentially.

-  Enhanced standalone test for ``ctypes`` on Linux to actually have
   something to test.

Summary
=======

This release improves on many things at once. A lot of work has been put
into polishing the Yaml configuration that now only lacks documentation
and examples, such that the community as a whole should become capable
of adding missing dependencies, data files, DLLs, and even anti-bloat
patches.

Then a lot of new optimization has been done, to close the missing gaps
with ``dict`` and ``str`` methods, but before completing ``list`` which
is already a work in progress pull request, and ``bytes``, we want to
start and generate the node classes that form the link or basis of
dedicated nodes. This will be an area to work on more.

The many improvements to existing code helpers, and them being able to
pick target types for the arguments of comparisons and binary
operations, is a pre-cursor to universal optimization of this kind. What
is currently only done for constant values, will in the future be
interesting for picking specific C types for use. That will then be a
huge difference from what we are doing now, where most things still have
to use ``PyObject *`` based types.

Scalability has again seen very real improvements, memory usage of
Nuitka itself, as well as compile time inside Nuitka are down by a lot
for some cases, very noticeably. There is never enough of this, but it
appears, in many cases now, large compilations run much faster.

For macOS specifically, the new DLL dependency analysis, is much more
capable or resolving conflicts all by itself. Many of the more complex
packages with some variants of Python, specifically Anaconda will now be
working a lot better.

And then, of course there is the big improvement for Onefile, that
allows to use cached paths. This will make it more usable in the general
case, e.g. where the firewall of Windows hate binaries that change their
path each time they run.

Future directions will aim to make the compilation report more concise,
and given reasons and dependencies as they are known on the inside more
clearly, such that is can be a major tool for testing, bug reporting and
analysis of the compilation result.
