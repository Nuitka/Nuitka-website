.. post:: 2021/12/11 17:21
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.6.18
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release has a focus on new features of all kinds, and then also new
kinds of performance improvements, some of which enable static
optimization of what normally would be dynamic imports, while also
polishing plugins and adding also many new features and a huge amount of
organizational changes.

***********
 Bug Fixes
***********

-  Python3.6+: Fixes to asyncgen, need to raise ``StopAsyncIteration``
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
   a warning, and run time fail on these. Fixed in 0.6.17.2 already.

-  Standalone: Prevent the inclusion of ``drm`` libraries on Linux, they
   have to come from the target OS at run time. Fixed in 0.6.17.2
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

**************
 New Features
**************

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
   ``pydantic``.

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

**************
 Optimization
**************

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
   common kind of nodes operate faster and don't have to check at run
   time what type they are during access.

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

****************
 Organizational
****************

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

**********
 Cleanups
**********

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

-  Apply Visual Code auto-format to our Yaml files. This is
   unfortunately not and automatic formatting yet.

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

*******
 Tests
*******

-  Added CPython 3.10 test suite, it needs more work though.

-  Added generated test that exercises dictionary methods in multiple
   variations.

-  Test suite names were specified wrongly in a few of them.

*********
 Summary
*********

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
