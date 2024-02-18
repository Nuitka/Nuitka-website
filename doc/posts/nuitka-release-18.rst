.. post:: 2023/09/30 07:59
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 1.8
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

***********
 Bug Fixes
***********

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

**************
 New Features
**************

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

**************
 Optimization
**************

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

****************
 Organisational
****************

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

**********
 Cleanups
**********

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

*******
 Tests
*******

-  Sometimes the pickle from cached CPython executions cannot be read
   due to protocol version differences, then of course it's also not
   usable.

-  Added CPython311 test suite, but it is not yet completely integrated.

-  Tests: Salvage one test for ``dateutil`` from a GSoC 2019 PR, we can
   use that.

*********
 Summary
*********

This is massive in terms of new features supported. The deployment mode
being added, provides us with a framework to make new user experience
with e.g. the missing data files, much more generous and help them by
pointing to the right solution.

The technical debt of immediate bytecode demotion being removed, is huge
for reliability of Nuitka. We now really only have to deal with actual
hidden dependencies in stdlib, and not just ones caused by us trying to
exclude parts of it and missing internal dependencies.
