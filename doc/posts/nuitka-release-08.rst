.. post:: 2022/05/26 10:54
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 0.8
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release has a massive amount of bug fixes, builds on existing
features, and adds new ones.

***********
 Bug Fixes
***********

-  Windows: Fix, need to ignore cases where shorting in path for
   external use during compilation gives an permission error. Fixed in
   0.7.1 already.

-  Compatibility: Added workaround for ``scipy.stats`` function copying.
   Fixed in 0.7.1 already.

-  Windows: Fix, detect ARM64 arch of MSVC properly, such that we can
   give a proper mismatch for the Python architecture. Fixed in 0.7.1
   already.

-  Standalone: Fix, using ``importlib.metadata`` module failed to
   include ``email`` from standard library parts no longer included by
   default. Fixed in 0.7.1 already.

-  macOS: Fix, the dependency parser was using normalized paths where
   original paths must be used. Fixed in 0.7.1 already.

-  Standalone: Fix, using ``shiboken6`` module (mostly due to
   ``PySide6``) failed to include ``argparse`` from the standard library
   from standard library parts no longer included by default. Fixed in
   0.7.1 already.

-  Onefile: Fix, the detection of a usable Python for compression could
   crash. Fixed in 0.7.2 already.

-  Onefile: Adding the payload on Windows could run into locks still
   being held, need to wait in that case. Fixed in 0.7.2 already.

-  Fix, need to include ``pkg_resources`` as well, we need it for when
   we use Jinja2, which is more often now. For Python3 this was fixed in
   0.7.3 already. Later a version to use with Python2 was added as well.

-  Release: The wheels built for Nuitka when installed through URLs were
   not version specific, but due to different inline copies per OS and
   Python version, they must not be reused. Therefore we now pretend to
   contain an extension module, which handles that. Fixed in 0.7.3
   already.

-  Standalone: Fix, using ``urllib.requests`` module failed to include
   ``http.client`` from standard library parts no longer included by
   default. Fixed in 0.7.3 already. Later ``http.cookiejar`` was added
   too.

-  Standalone: Do not compress MSVC runtime library when using ``upx``
   plugin, that is not going to work. Fixed in 0.7.4 already.

-  Standalone: Fix, on Windows more files should be included for TkInter
   to work with all software. Fixed in 0.7.5 already.

-  Distutils: Added support for ``package_dir`` directive to specify
   where source code lives. Fixed in 0.7.6 already.

-  Standalone: Fix, using ``shelve`` module failed to include ``dbm``
   from standard library parts no longer included by default. Fixed in
   0.7.6 already.

-  Standalone: Added support for ``arcade`` data files. Fixed in 0.7.7
   already.

-  Standalone: Fix, bytecode demotions should use relative filenames
   rather than original ones. Fixed in 0.7.7 already.

-  Standalone: Fix, must remove extension module objects from
   ``sys.modules`` before executing an extension module that will create
   it. This fixes cases of cyclic dependencies from modules loaded by
   the extension module.

-  Windows: In case of an exception, ``clcache`` was itself triggering
   one during its handling, hiding the real exception behind a
   ``TypeError``.

-  Windows: Improved ``clcache`` locking behavior, avoiding a race. Also
   increase characters used for key from 2 to 3 chars, making collisions
   far more rare.

-  Standalone: Added support for ``persistent`` package.

-  Standalone: Added support for newer ``tensorflow`` package.

-  Module: Fix, need to restore the ``__file__`` and ``__spec__`` values
   of top level module. It is changed by CPython after import to an
   incompatible file name, and not our loader, preventing package
   resources to be found.

-  Standalone: Added support for ``Crpytodome.Cipher.PKCS1_v1_5``.

-  Fix, ``pkgutil.iter_modules`` without arguments was not working
   properly with our meta path based loader.

-  Windows: Fix, could crash on when the Scons report was written due to
   directories in ``PATH`` that failed to encode.

-  Compatibility: Fix, positive ``divmod`` and modulo ``%`` with
   negative remainders of positive floats was not correct.

-  Fix, ``str.encode`` with only ``errors`` value, but default value for
   encoding was crashing the compilation.

-  Python3.10+: Fix, ``match`` statement sliced values must be lists,
   not tuples.

-  Standalone: Added support for newer ``glfw`` and ``OpenGL`` packages.

-  Python3: Fix, failed to read bytecode only stdlib files. This affect
   mostly Fedora Python which does this for encodings.

-  Python3.5+: Fix, two phase loading of modules could release it
   immediately.

-  Standalone: Added missing dependency for ``pydantic``.

-  Fix, the ``str.split`` rejected default ``sep`` value with only
   ``maxsplit`` given as a keyword argument.

-  Standalone: Added missing dependency of ``wsgiref`` module.

-  Standalone: Added support for ``falcon`` module.

-  Standalone: Added support for ``eliot`` module.

-  Fix, need to mark assigned from variables as escaped. Without it,
   some aliased loop variables could be misunderstood and falsely
   statically optimized.

-  Standalone: Added support for newer ``uvicorn`` package.

-  Standalone: Added data files for the ``accessible_output2``,
   ``babel``, ``frozendict``, and ``sound_lib`` package.

-  Standalone: Added support for newer ``sklearn`` package.

-  Standalone: Added support for ``tkinterdnd2`` package.

-  Python3.7+: Fix, the error message wasn't fully compatible for
   unsubscriptable type exception messages.

-  Standalone: Fix, ``idlelib`` from stdlib was always ignored.

-  Python3.4+: Fix, the ``__spec__.origin`` as produced by ``find_spec``
   of our meta path based loader, didn't have the correct ``origin``
   attribute value.

-  Standalone: Disable QtPDF plugin of PySide 6.3.0, because it's
   failing dependency checks. On macOS this was blocking, we will change
   it to detection if that is necessary in a future release.

-  Standalone: Added support for ``orderedmultidict``.

-  Standalone: Added support for ``clr`` module.

-  Standalone: Added support for newer ``cv2`` package.

**************
 New Features
**************

-  Added new option ``--module-name-choice`` to select what value
   ``__name__`` and ``__package__`` are going to be. With
   ``--module-name-choice=runtime`` (default for ``--module`` mode), the
   created module uses the parent package to deduce the value of
   ``__package__``, to be fully compatible. The value
   ``--module-name-choice=original`` (default for other modes) allows
   for more static optimization to happen.

-  Added support for ``get_resource_reader`` to our meta path based
   loader. This allows to avoid useless temporary files in case
   ``importlib.resources.path`` is used, due to a bad interaction with
   the fallback implementation used without it.

-  Added support for ``--force-stdout-spec```and ``--force-stderr-spec``
   on all platforms, this was previously limited to Windows.

-  Added support for requiring and suggesting modes. In part this was
   added to 0.7.3 already, and is used e.g. to enforce that on macOS the
   ``wx`` will only work as a GUI program and crash unless
   ``--disable-console`` is specified. These will warn the user or
   outright error the compilation if something is known to be needed or
   useful.

-  Debian: Detect version information for "Debian Sid". Added in 0.7.4
   already, and also improved how Debian/Ubuntu versions are output.

-  Added new option ``--noinclude-data-files`` to instruct Nuitka to not
   include data files matching patterns given. Also attached loggers and
   tags to included data file and include them in the compilation
   report.

-  Distutils: When using ``pyproject.toml`` without ``setup.py`` so far
   it was not possible to pass arguments. This is now possible by adding
   a section like this.

   .. code:: toml

      [nuitka]
      # options without an argument are passed as boolean value
      show-scons = true

      # options with single values, e.g. enable a plugin of Nuitka
      enable-plugin = pyside2

      # options with several values, e.g. avoiding including modules, accepts
      # list argument.
      nofollow-import-to = ["*.tests", "*.distutils"]

   The option names are the same, but without leading dashes. Lists are
   only needed when passing multiple values with the same option.

-  macOS: Add support for specifying signing identity with
   ``--macos-sign-identity`` and access to protected resources
   ``--macos-app-protected-resource``.

-  Included data files are now reported in the compilation report XML as
   well.

-  Accept absolute paths for searching paths of binaries. This allows
   e.g. the ``upx`` plugin to accept both a folder path and the full
   path including the binary name to work when you specify the binary
   location with ``--upx-binary`` making it more user friendly.

-  Python3.10: Added support for positional matching of classes, so far
   only keyword matching was working.

-  Added support for path spec values ``%CACHE_DIR``, ``%COMPANY%``,
   ``%PRODUCT%``, ``%VERSION%``, and ``%HOME`` in preparation of onefile
   once again being able to be cached and not unpacked repeatedly for
   each execution.

-  Standalone: Detect missing ``tk-inter`` plugin at runtime. When TCL
   fails to load, it then outputs a more helpful error. This ought to be
   done for all plugins, where it's not clear if they are needed.

-  Anti-bloat: Added support for plain replacements in the
   ``anti-bloat.yml`` file. Before with ``replacement```, the new value
   had to be produced by an ``eval``, which makes for less readable
   values due to extra quoting. for plain values.

**************
 Optimization
**************

-  Python3.10+: Added support for ``ordered-set`` PyPI package to speed
   up compilation on these versions too, adding a warning if no
   accelerated form of ``OrderedSet`` is used, but believed to be
   usable.

-  Optimization: Added ``bytes.decode`` operations. This is only a start
   and we needed this for internal usage, more should follow later.

-  Much more ``anti-bloat`` work was added. Avoiding ``ipython``,
   ``unittest``, and sometimes even ``doctest`` usage for some more
   packages.

-  The ``ccache`` was not always used, sometimes it believed to catch a
   potential race, that we need to tell it to ignore. This will speed up
   re-compilation of the C side in many cases.

-  Do not compile the meta path based loader separate, which allows us
   to not expose functions and values only used by it. Also spares the C
   compiler one file.

-  Added various dedicated nodes for querying package resources data,
   e.g. ``pkgutil.get_data``. This will make it easier to detect cases
   of missing data files in the future.

-  Added more hard imports, some of which help scalability in the
   compilation, because these are then known to exist in standalone
   mode, others are used for package resource specific operations.

-  Onefile: Releasing decompression buffers avoiding unnecessary high
   memory usage of bootstrap binary.

-  Standalone: Avoid proving directories with no DLLs (e.g. from
   packages) towards ``ldd``, this should avoid exceeding command line
   limits.

-  For ``clcache`` remove writing of the stats file before Scons has
   completed, which avoids IO and locking churn.

-  Standalone: Avoid including ``wsgiref`` from stdlib by default.

**********
 Cleanups
**********

-  Removed references to ``chrpath`` and dead code around it, it was
   still listed as a dependency, although we stopped using it a while
   ago.

-  Removed uses of ``anti-bloat`` in examples and tests, it is now
   enabled by default.

-  Made standard plugin file naming consistent, their name should be
   ``*Plugin.py``.

-  Cleaned up ``tensorflow`` plugin. The source modification was moved
   to ``anti-bloat`` where it is easy to do. The implicit dependencies
   are now in the config file of ``implicit-imports`` plugin.

-  Massive cleanups of data file handling in plugins. Adding methods for
   producing the now required objects.

-  The Scons file handling got further cleaned up and unified, doing
   more things in common code.

-  Avoid ``#ifdefs`` usages with new helper function
   ``Nuitka_String_FromFormat`` that implies them for more readable
   code.

-  Split the allowance check from the encountering. Allow plugins and
   options all to say if an import should be followed, and only when
   that is decided, to complain about it. Previously the attempt was
   causing an error, even if another plugin were to decide against it
   later.

-  Python2.6: Avoid warnings from MSVC for out specialized ``long``
   code. In testing it worked correctly, but this is more explicit and
   doesn't rely on C implementation specific behavior, although it
   appears to be universal.

****************
 Organisational
****************

-  UI: Warning tests are now wrapped to multiple lines if necessary.
   That makes it more accessible for larger messages that contain more
   guiding information.

-  Documented how to use local Nuitka checkout with ``pyproject.toml``
   files, this makes debugging Nuitka straightforward in these setups.

-  Added instructions on how to pass extra C and linker flags and to the
   User Manual.

-  Made our auto-format usable for the Nuitka website code too.

-  Removed dependencies on ``chrpath`` and the now dead code that would
   use it, we are happy with ``patchelf``.

-  Updated to latest versions of requirements for development, esp.
   ``black`` and ``pylint``.

-  Renamed ``--macos-onefile-icon`` to ``--macos-app-icon`` because that
   is what it is really used for.

-  Unified how dependencies are installed in GitHub actions.

-  Updated man page contents for option name changes from last releases.

-  Updated the MinGW64 winlibs download used on Windows to the latest
   version.

-  Updated the ``ccache`` binary used on Windows with MinGW64. This is
   in preparation of using it potentially for MSVC as well.

-  Updated Visual Code C config to use Python3.10 and MSVC 2022 include
   paths.

*******
 Tests
*******

-  Better outputs from standalone library compilation test, esp. when
   finding a problem, present the script to reproduce it immediately.

-  Enhanced generated tests to cover ``str`` methods to use keyword
   arguments.

-  Added automatic execution of ``pyproject.toml`` driven test case.

-  Enhanced output in case of ``optimization`` test failures, dumping
   what value is there that has not become compile-time not constant.

*********
 Summary
*********

This release has seen a lot of consolidation. The plugins layer for data
files is now all powerful, allowing much nicer handling of them by the
plugins, they are better reported in normal output, and they are also
part of the report file that Nuitka can create. You may now also inhibit
their inclusion from the command line, if you decide otherwise.

The ``pyproject.toml`` now supporting Nuitka arguments is closing an
important gap.

Generally many features got more polished, e.g. non-automatic inclusion
of stdlib modules has most problems fixed up.

An important area of improvement, are the hard imports. These will be
used to replace the source based resolution of package requirements with
ones that are proper nodes in the tree. Getting these hard imports to
still retain full compatibility with existing imports, that are more or
less ``__import__`` uses only, was revealing quite a bit of technical
debt, that has been addressed with this release.

For onefile, the cached mode is being prepared with the variables added,
but will only be in a later release.

Also a bunch of new or upgraded packages are working now, and the push
for ``anti-bloat`` work has increased, making many compilations even
more lean, but scalability is still an issue.
