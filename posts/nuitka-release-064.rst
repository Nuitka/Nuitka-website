This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release contains many bug fixes all across the board. There is also
new optimization and many organisational improvements.

Bug Fixes
---------

- When linking very large programs or packages, with gcc compiler, Scons can
  produce commands that are too large for the OS. This happens sooner on the
  Windows OS, but also on Linux. We now have a workaround that avoids long
  command lines by using ``@sources.tmp`` syntax.

- Standalone: Remove temporary module after its use, instead of keeping it
  in ``sys.modules`` where e.g. ``Quart`` code tripped over its ``__file__``
  value that is illegal on Windows.

- Fixed non-usage of our enhanced detection of ``gcc`` version for compilers
  if given as a full path.

- Fixed non-detection of ``gnu-cc`` as a form of gcc compiler.

- Python3.4: The ``__spec__`` value corrections for compiled modules was not
  taking into account that there was a ``__spec__`` value, which can happen
  if something is wrapping imported modules.

- Standalone: Added implicit dependencies for ``passlib``.

- Windows: Added workaround for OS command line length limit in compilation
  with MinGW64.

- Python2: Revive the ``enum`` plugin, there are backports of the buggy code
  it tries to patch up.

- Windows: Fixup handling of SxS with non zero language id, these occur e.g.
  in Anaconda.

- Plugins: Handle multiple PyQt plugin paths, e.g. on openSUSE this is done,
  also enhanced finding that path with Anaconda on Windows.

- Plugins: For ``multiprocessing`` on Windows, allow the ``.exe`` suffix to
  not be present, which can happen when ran from command line.

- Windows: Better version checks for DLLs on Python3, the ``ctypes`` helper
  code needs more definitions to work properly.

- Standalone: Added support for both ``pycryptodome`` and ``pycryptodomex``.

- Fix, the ``chr`` built-in was not giving fully compatible error on non
  number input.

- Fix, the ``id`` built-in doesn't raise an exception, but said otherwise.

- Python3: Proper C identifiers for names that fit into ``latin-1``, but are
  not ``ascii`` encodings.

New Features
------------

- Windows: Catch most common user error of using compiler from one architecture
  against Python from another. We now check those and compare it, and if they
  do not match, inform the user directly. Previously the compilation could
  fail, or the linking, with cryptic errors.

- Distutils: Using setuptools and its runners works now too, not merely only
  pure distutils.

- Distutils: Added more ways to pass Nuitka specific options via distutils.

- Python3.8: Initial compatibility changes to get basic tests to work.

Organisational
--------------

- Nuitka is participating in the GSoC 2019 with 2 students, Batakrishna and
  Tommy.

- Point people creating PRs to using the ``pre-commit`` hook in the template.
  Due to making the style issues automatic, we can hope to encounter less noise
  and resulting merge problems.

- Many improvements to the ``pre-commit`` hook were done, hopefully completing
  its development.

- Updated to latest ``pylint``, ``black``, and ``isort`` versions, also
  added ``codespell`` to check for typos in the source code, but that is not
  automated yet.

- Added description of how to use experimental flags for your PRs.

- Removed mirroring from Bitbucket and Gitlab, as we use the Github organisation
  features.

- Added support for Ubuntu Disco, removed support for Ubuntu Artful packages.

Optimization
------------

- Windows: Attach data blobs as Windows resource files directly for programs
  and avoid using C data files for modules or MinGW64, which can be slow.

- Specialization of helper codes for ``+`` is being done for more types and
  more thoroughly and fully automatic with Jinja2 templating code. This does
  replace previously manual code.

- Added specialization of helper codes for ``*`` operation which is entirely
  new.

- Added specialization of helper codes for ``-`` operation which is entirely
  new.

- Dedicated nodes for specialized operations now allow to save memory and all
  use type shape based analysis to predict result types and exception control
  flow.

- Better code generation for boolean type values, removing error checks when
  possible.

- Better static analysis for even more type operations.

Cleanups
--------

- Fixed many kinds of typos in the code base with ``codespell``.

- Apply automatic formatting to more test runner code, these were previously
  not done.

- Avoid using ``shutil.copytree`` which fails to work when directory already
  exists, instead provide ``nuitka.util.FileOperations.copyTree`` and use that
  exclusively.

Tests
-----

- Added new mode of operation to test runners, ``only`` that executes just
  one test and stops, useful during development.

- Added new mechanism for standalone tests to expression modules that need
  to be importable, or else to skip the test by a special comment in the
  file, instead of by coded checks in the test runner.

- Added also for more complex cases, another form of special comment, that can
  be any expression, that decides if the test makes sense.

- Cover also setuptools in our distutils tests and made the execution more
  robust against variable behavior of distutils and setuptools.

- Added standalone test for Urllib3.

- Added standalone test for rsa.

- Added standalone test for Pmw.

- Added standalone test for passlib.

Summary
-------

Again this release is a sign of increasing adoption of Nuitka. The GSoC
2019 is also showing effects, definitely will in the next release.

This release has a lot of new optimization, called specialization, but for
it to really used, in many instances, we need to get away from working on
C types for variables only, and get to them beig used for expressions more
often. Otherwise much of the new special code is not used for most code.

The focus of this release has been again to open up development further
and to incorporate findings from users. The number of fixes or new use
cases working is astounding.

In upcoming releases, new built-ins will be optimized, and specialization
of operations will hit more and more code now that the infrastructure for
it is in place.
