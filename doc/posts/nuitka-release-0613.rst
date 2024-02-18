.. post:: 2021/04/03 10:05
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.6.13
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release follows up with yet again massive improvement in many ways
with lots of bug fixes and new features.

***********
 Bug Fixes
***********

-  Windows: Icon group entries were not still not working properly in
   some cases, leading to no icon or too small icons being displayed.
   Fixed in 0.6.12.2 already.

-  Windows: Icons and version information were copied from the
   standalone executable to the onefile executable, but that failed due
   to race situations, sometimes reproducible. Instead we now apply
   things to both independently. Fixed in 0.6.12.2 already.

-  Standalone: Fixup scanning for DLLs with ``ldconfig`` on Linux and
   newer versions making unexpected outputs. Fixed in 0.6.12.2 already.

-  UI: When there is no standard input provided, prompts were crashing
   with ``EOFError`` when ``--assume-yes-for-downloads`` is not given,
   change that to defaulting to ``"no"`` instead. Fixed in 0.6.12.2
   already.

-  Windows: Detect empty strings for company name, product name, product
   and file versions rather than crashing on them later. Them being
   empty rather than not there can cause a lot of issues in other
   places. Fixed in 0.6.12.2 already.

-  Scons: Pass on exceptions during execution in worker threads and
   abort compilation immediately. Fixed in 0.6.12.2 already.

-  Python3.9: Still not fully compatible with typing subclasses, the
   enhanced check is now closely matching the CPython code. Fixed in
   0.6.12.2 already.

-  Linux: Nicer error message for missing ``libfuse`` requirement.

-  Compatibility: Lookups on dictionaries with ``None`` value giving a
   ``KeyError`` exception, but with no value, which is not what CPython
   does.

-  Python3.9: Fix, future annotations were crashing in debug mode. Fixed
   in 0.6.12.3 already.

-  Standalone: Corrections to the ``glfw`` were made. Fixed in 0.6.12.3
   already.

-  Standalone: Added missing ìmplicit dependency for ``py.test``. Fixed
   in 0.6.12.3 already.

-  Standalone: Adding missing implicit dependency for ``pyreadstat``.

-  Windows: Added workaround for common clcache locking problems. Since
   we use it only inside a single Scons process, we can avoiding using
   Windows mutexes, and use a process level lock instead.

-  Plugins: Fix plugin for support for ``eventlet``. Fixed in 0.6.12.3
   already.

-  Standalone: Added support for latest ``zmq`` on Windows.

-  Scons: the ``--quiet`` flag was not fully honored yet, with Scons
   still making a few outputs.

-  Standalone: Added support for alternative DLL name for newer
   ``PyGTK3`` on Windows. Fixed in 0.6.12.4 already.

-  Plugins: Fix plugin for support for ``gevent``. Fixed in 0.6.12.4
   already.

-  Standalone: Added yet another missing implicit dependency for
   ``pandas``.

-  Plugins: Fix, the ``qt-plugins`` plugin could stumble over ``.mesh``
   files.

-  Windows: Fix, dependency walker wasn't properly working with unicode
   ``%PATH%`` which could e.g. happen with a virtualenv in a home
   directory that requires them.

-  Python3: Fixed a few Python debug mode warnings about unclosed files
   that have sneaked into the codebase.

**************
 New Features
**************

-  Added new options ``--windows-force-stdout-spec`` and
   ``--windows-force-stderr-spec`` to force output to files. The paths
   provided at compile time can resolve symbolic paths, and are intended
   to e.g. place these files near the executable. Check the User Manual
   for a table of the currently supported values. At this time, the
   feature is limited to Windows, where the need arose first, but it
   will be ported to other supported OSes eventually. These are most
   useful for programs run as ``--windows-disable-console`` or with
   ``--enable-plugin=windows-service``.

   .. note::

      These options have since been renamed to ``--force-stdout`` and
      ``--force-stderr`` and have been made to work on all OSes.

-  Windows: Added option ``--windows-onefile-tempdir-spec`` (since
   renamed to ``--onefile-tempdir-spec``) to provide the temporary
   directory used with ``--windows-onefile-tempdir`` in onefile mode,
   you can now select your own pattern, and e.g. hardcode a base
   directory of your choice rather than ``%TEMP``.

-  Added experimental support for ``PySide2`` with workarounds for
   compiled methods not being accepted by its core. There are known
   issues with ``PySide2`` still, but it's working fine for some people
   now. Upstream patches will have to be created to remove the need for
   workarounds and full support.

**************
 Optimization
**************

-  Use binary operation code for their in-place variants too, giving
   substantial performance improvements in all cases that were not dealt
   with manually already, but were covered in standard binary
   operations. Until now only some string, some float operations were
   caught sped up, most often due to findings of Nuitka being terribly
   slower, e.g. not reusing string memory for inplace concatenation, but
   now all operations have code that avoids a generic code path, that is
   also very slow on Windows due calling to using the embedded Python
   via API being slow.

-  For mixed type operations, there was only one direction provided,
   which caused fallbacks to slower forms, e.g. with ``long`` and
   ``float`` values leading to inconsistent results, such that ``a - 1``
   and ``1 - a`` being accelerated or not.

-  Added C boolean optimization for a few operations that didn't have
   it, as these allow to avoid doing full computation of what the object
   result would have to do. This is not exhausted fully yet.

-  Python3: Faster ``+``/``-``/``+=``/``-=`` binary and in-place
   operations with ``int`` values providing specialized code helpers
   that are much faster, esp. in cases where no new storage is allocated
   for in-place results and where not a lot of digits are involved.

-  Python2: The Python3 ``int`` code is the Python2 ``long`` type and
   benefits from the optimization of ``+``/``-``/``+=``/``-=`` code as
   well, but of course its use is relatively rare.

-  Improved ``__future__`` imports to become hard imports, so more
   efficient code is generated for them.

-  Counting of instances had a run time impact by providing a
   ``__del__`` that was still needed to be executed and limits garbage
   collection on types with older Python versions.

-  UI: Avoid loading ``tqdm`` module before it's actually used if at all
   (it may get disabled by the user), speeding up the start of Nuitka.

-  Make sure to optimize internal helpers only once and immediately,
   avoiding extra global passes that were slowing down Python level
   compilation by of large programs by a lot.

-  Make sure to recognize the case where a module optimization can
   provide no immediate change, but only after a next run, avoiding
   extra global passes originating from these, that were slowing down
   compilation of large programs by a lot. Together with the other
   change, this can improve scalability by a lot.

-  Plugins: Remove implicit dependencies for ``pkg_resources.extern``
   and use aliases instead. Using one of the packages, was causing all
   that might be used, to be considered as used, with some being
   relatively large. This was kind of a mistake in how we supported this
   so far.

-  Plugins: Revamped the ``eventlet`` plugin, include needed DNS modules
   as bytecode rather than as source code, scanning them with
   ``pkgutil`` rather than filesystem, with much cleaner code in the
   plugin. The plugin is also now enabled by default.

****************
 Organisational
****************

-  Removed support for ``pefile`` dependency walker choice and inline
   copy of the code. It was never as good giving incomplete results, and
   after later improvements, slower, and therefore has lost the original
   benefit over using Dependency Walker that is faster and more correct.

-  Added example for onefile on Windows with the version information and
   with the temporary directory mode.

-  Describe difference in file access with onefile on Windows, where
   ``sys.argv[0]`` and ``os.path.dirname(__file__)`` will be different
   things.

-  Added inline copy of ``tqdm`` to make sure it's available for
   progress bar output for 2.7 or higher. Recommend having it in the
   Debian package.

-  Added inline copy of ``colorama`` for use on Windows, where on some
   terminals it will give better results with the progress bar.

-  Stop using old PyLint for Python2, while it would be nice to catch
   errors, the burden of false alarms seems to high now.

-  UI: Added even more checks on options that make no sense, made sure
   to do this only after a possible restart in proper environment, so
   warnings are not duplicated.

-  For Linux onefile, keep appimage outputs in case of an error, that
   should help debugging it in case of issues.

-  UI: Added traces for plugin provided implicit dependencies leading to
   inclusions.

-  Added inline copy of ``zstd`` C code for use in decompression for the
   Windows onefile bootstrap, not yet used though.

-  Added checks to options that accept package names for obvious
   mistakes, such that ``--include-package-data --mingw64`` will not
   swallow an option, as that is clearly not a package name, that would
   hide that option, while also not having any intended effect.

-  Added ignore list for decision to recompile extension modules with
   available source too. For now, Nuitka will not propose to recompile
   ``Cython`` modules that are very likely not used by the program
   anyway, and also not for ``lxml`` until it's clear if there's any
   benefit in that. More will be added in the future, this is mostly for
   cases, where Cython causes incompatibilities.

-  Added support for using abstract base classes in plugins. These are
   not considered for loading, and allow nicer implementation of shared
   code, e.g. between ``PyQt5`` and ``PySide2`` plugins, but allow e.g.
   to enforce the provision of certain overloads.

-  User Manual: Remove the instruction to install ``clcache``, since
   it's an inline copy, this makes no sense anymore and that was
   obsolete.

-  Updated PyLint to latest versions, and our requirements in general.

**********
 Cleanups
**********

-  Started removal of PyLint annotations used for old Python2 only. This
   will be a continuous action to remove these.

-  Jinja2 based static code generation for operations was cleaned up, to
   avoid code for static mismatches in the result C, avoiding language
   constructs like ``if (1 && 0)`` with sometimes larger branches,
   replacing it with Jinja2 branches of the ``{% if ... %}`` form.

-  Jinja2 based Python2 ``int`` code was pioniering the use of macros,
   but this was expanded to allow kinds of types for binary operations,
   allow their reuse for in-place operation, with these macros making
   returns via goto exits rather than return statements in a function.
   Landing pads for these exits can then assign target values for
   in-place different from what those for binary operation result return
   do.

-  Changed the interfacing of plugins with DLL dependency detection,
   cleaning up the interactions considerably with more unified code, and
   faster executing due to cached plugin decisions.

-  Integrate manually provided slot function for ``unicode`` and ``str``
   into the standard static code generation. Previously parts were
   generated and parts could be generated, but also provided with manual
   code. The later is now all gone.

-  Use a less verbose progress bar format with less useless infos,
   making it less likely to overflow.

-  Cleanup how payload data is accessed in Windows onefile bootstrap,
   preparing the addition of decompression, doing the reading from the
   file in only one dedicated function.

-  When Jinja2 generated exceptions in the static code, it is now done
   via proper Jinja2 macros rather than Python code, and these now avoid
   useless Python version branches where possible, e.g. because a type
   like ``bytes`` is already Python version specific, with the goal to
   get rid of ``PyErr_Format`` usage in our generated static code. That
   goal is future work though.

-  Move safe strings helpers (cannot overflow) to a dedicated file, and
   remove the partial duplication on the Windows onefile bootstrap code.

-  The Jinja2 static code generation was enhanced to track the usage of
   labels used as goto targets, so that error exits, and value typed
   exits from operations code no longer emitted when not used, and
   therefore labels that are not used are not present.

-  For implicit dependencies, the parsing of the ``.pyi`` file of a
   module no longer emits a dependency on the module itself. Also from
   plugins, these are now filtered away.

*******
 Tests
*******

-  Detect if onefile mode has required downloads and if there is user
   consent, otherwise skip onefile tests in the test runner.

-  Need to also allow accesses to files via short paths on Windows if
   these are allowed long paths.

-  The standalone tests on Windows didn't actually take run time traces
   and therefore were ineffective.

-  Added standalone test for ``glfw`` coverage.

-  Construct based tests for in-place operations are now using a value
   for the first time, and then a couple more times, allowing for real
   in-place usage, so we are sure we measure correctly if that's
   happening.

*********
 Summary
*********

Where the big change of the last release were optimization changes to
reduce the global passes, this release addresses remaining causes for
extra passes, that could cause these to still happen. That makes sure,
Nuitka scalability is very much enhanced in this field again.

The new features for forced outputs are at this time Windows only and
make a huge difference when it comes to providing a way to debug Windows
Services or programs in general without a console, i.e. a GUI program.
These will need even more specifiers, e.g. to cover program directory,
rather than exe filename only, but it's a very good start.

On the tooling side, not a lot has happened, with the clcache fix, it
seems that locking issues on Windows are gone.

The plugin changes from previous releases had left a few of them in a
state where they were not working, but this should be restored.
Interaction with the plugins is being refined constantly, and this
releases improved again on their interfaces. It will be a while until
this becomes stable.

Adding support for PySide2 is a headline feature actually, but not as
perfect as we are used to in other fields. More work will be needed,
also in part with upstream changes, to get this to be fully supported.

For the performance side of things, the in-place work and the binary
operations work has taken proof of concept stuff done for Python2 and
applied it more universally to Python3. Until we cover all long
operations, esp. ``*`` seems extremely important and is lacking, this
cannot be considered complete, but it gives amazing speedups in some
cases now.

Future releases will revisit the type tracing to make sure, we know more
about loop variables, to apply specific code helpers more often, so we
can achieve the near C speed we are looking for in the field of ``int``
performance.
