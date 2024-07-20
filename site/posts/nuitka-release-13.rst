.. post:: 2022/12/28 09:58
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 1.3
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release contains a large amount of performance work, that should
specifically be useful on Windows, but also generally. A bit of
scalability work has been applied, and as usual many bug fixes and small
improvements, many of which have been in hotfixes.

***********
 Bug Fixes
***********

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

**************
 New Features
**************

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

-  Plugins: In the Nuitka Package Configuration files, the ``when``
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

**************
 Optimization
**************

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

****************
 Organizational
****************

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

**********
 Cleanups
**********

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

*******
 Tests
*******

-  Added construct test that demonstrates the mutable constant argument
   passing for lists to see the performance gains in this area too.

-  Made construct runner ``--diff`` output usable for interactive usage.

-  Repaired Nuitka Speedcenter, but it's not yet too usable for general
   consumption. More work will be needed there, esp. to make comparisons
   more accessible for the general public.

*********
 Summary
*********

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
