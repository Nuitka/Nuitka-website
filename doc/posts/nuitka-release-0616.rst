.. post:: 2021/09/09 11:01
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.6.16
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release is mostly polishing and new features. Optimization looked
only at threading performance, and LTO improvements on Windows.

***********
 Bug Fixes
***********

-  Fix, the ``pkg-resources`` failed to resolve versions for
   ``importlib.metadata`` from its standard library at compile time.
   Fixed in 0.6.15.1 already.

-  Standalone: Fix, ``--include-module`` was not including the module if
   it was an extension modules, but only for Python modules. Fixed in
   0.6.15.1 already.

-  Standalone: Added missing implicit dependencies for ``gi.overrides``.
   Fixed in 0.6.15.1 already.

-  Python3.9: Fix, could crash when using generic aliases in certain
   configurations. Fixed in 0.6.15.2 already.

-  Fix, the tensorflow plugin needed an update due to changed API. Fixed
   in 0.6.15.3 already.

-  When error exiting Nuitka, it now closes any open progress bar for
   cleaner display.

-  Standalone: Added missing dependency for ``skimage``.

-  Standalone: The ``numpy`` plugin now automatically includes Qt
   backend if any of the Qt binding plugins is active.

**************
 New Features
**************

-  Python3.5+: Added support for onefile compression. This is using
   ``zstd`` which is known to give very good compression with very high
   decompression, much better than e.g. ``zlib``.

-  macOS: Added onefile support.

-  FreeBSD: Added onefile support.

-  Linux: Added method to use tempdir onefile support as used on other
   platforms as an alternative to ``AppImage`` based.

-  Added support for recursive addition of files from directories with
   patterns.

-  Attaching the payload to onefile now has a progress bar too.

-  Windows: Prelimary support for the yet unfinished Nuitka-Python that
   allows static linking and higher performance on Windows, esp. with
   Nuitka.

-  Windows: In acceleration mode, for uninstalled Python, now a CMD file
   is created rather than copying the DLL to the binary directory. That
   avoids conflicts with architectures and of course useless file
   copies.

-  New abilities for plugin ``anti-bloat`` allow to make it an error
   when certain modules are imported. Added more specific options for
   usual trouble makes, esp. ``setuptools``, ``pytest`` are causing an
   explosion for some programs, while being unused code. This makes it
   now easier to oversee this.

-  It's now possible to override ``appdirs`` decision for where cache
   files live with an environment variable ``NUITKA_CACHE_DIR``.

-  The ``-o`` option now also works with onefile mode, it previously
   rejected anything but acceleration mode. Fixed in 0.6.15.3 already.

-  Plugins: It's now possible for multiple plugins to provide pre or
   post load code for the same module.

-  Added indications for compilation modes ``standalone`` and
   ``onefile`` to the ``__compiled__`` attribute.

-  Plugins: Give nicer error message in case of colliding command line
   options.

**************
 Optimization
**************

-  Faster threading code is now using for Python3.8 or higher and not
   only 3.9, giving a performance boost, esp. on Windows.

-  Using ``--lto`` is now the default with MSVC 2019 or higher. This
   will given smaller and faster binaries. It has been available for
   some time, but not been the default yet.

**********
 Cleanups
**********

-  Using different progress bar titles for C compilation of Python code
   and C compilation of onefile bootstrap.

-  Moved platform specific detections, for FreeBSD/OpenBSD/macOS out of
   the Scons file and to common Nuitka code, sometimes eliminating
   duplications with one version being more correct than the other.

-  Massive cleanup of datafile plugin, using pattern descriptions, so
   more code duplication can be removed.

-  More cleanup of the scons files, sharing more common code.

****************
 Organizational
****************

-  Under the name Nuitka-Python we are now also developing a fork of
   CPython with enhancements, you can follow and joint it at
   https://github.com/Nuitka/Nuitka-Python but at this time it is not
   yet ready for prime time.

-  Onefile under Windows now only is temporary file mode. Until we
   figure out how to solve the problems with locking and caching, the
   mode where it installs to the AppData of the user is no longer
   available.

-  Renamed the plugin responsible for PyQt5 support to match the names
   of others. Note however, that at this time, PySide2 or PySide6 are to
   be recommended.

-  Make it clear that PySide 6.1.2 is actually going to be the supported
   version of PySide6.

-  Use MSVC in GitHub actions.

*********
 Summary
*********

This release had a massive focus on expanding existing features, esp.
for onefile, and plugins API, such that we can now configure
``anti-bloat`` with yaml, have really nice datafile handling options,
and have onefile on all OSes practically.
