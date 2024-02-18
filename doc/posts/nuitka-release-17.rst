.. post:: 2023/07/15 09:21
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 1.7
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

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

***********
 Bug Fixes
***********

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

**************
 New Features
**************

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

**************
 Optimization
**************

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

****************
 Organisational
****************

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

**********
 Cleanups
**********

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

*******
 Tests
*******

-  Release: Use CI container for linter checks, so different branches
   can use different versions with less pain involved.

-  macOS: Allow all system library frameworks to be used, not just a few
   selected ones, there is many of them and they should all exist on
   every system. Added in 1.6.1 already.

-  Made the ``pendulum`` test actually useful to cover new and old
   pendulum actually working properly.

*********
 Summary
*********

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
