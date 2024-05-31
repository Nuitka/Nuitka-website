.. post:: 2023/03/26 19:38
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 1.5
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release contains the long awaited 3.11 support, even if only on an
experimental level. This means where 3.10 code is used, it is expected
to work equally well, but the Python 3.11 specific new features have yet
been done.

There is plenty of new features in Nuitka, e.g. much enhanced reports,
Windows ARM native compilation support, and the usual slew of anti-bloat
updates, and newly supported packages.

***********
 Bug Fixes
***********

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

**************
 New Features
**************

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

**************
 Optimization
**************

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

****************
 Organizational
****************

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

**********
 Cleanups
**********

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

*******
 Tests
*******

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

*********
 Summary
*********

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
