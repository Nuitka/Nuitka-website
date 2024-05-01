.. post:: 2021/06/05 17:18
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.6.15
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release polished previous work with bug fixes, but there are also
important new things that help make Nuitka more usable, with one
important performance improvement.

***********
 Bug Fixes
***********

-  Fix, hard imports were not automatically used in code generation
   leading to errors when used. Fixed in 0.6.14.2 already.

-  Windows: Fix, ``clcache`` was disabled by mistake. Fixed in 0.6.14.2
   already.

-  Standalone: Added data files for ``jsonschema`` to be copied
   automatically.

-  Standalone: Support for ``pendulum`` wasn't working anymore with the
   last release due to plugin interface issues.

-  Retry downloads without SSL if that fails, as some Python do not have
   working SSL. Fixed in 0.6.14.5 already.

-  Fix, the ``ccache`` path wasn't working if it contained spaces. Fixed
   in 0.6.14.5 already.

-  Onefile: For Linux and ARM using proper download off appimage. Fixed
   in 0.6.14.5 already.

-  Standalone: Added support for ``pyreadstat``. Fixed in 0.6.14.5
   already.

-  Standalone: Added missing dependencies for ``pandas``. Fixed in
   0.6.14.6 already.

-  Standalone: Some preloaded packages from ``.pth`` do not have a
   ``__path__``, these can and must be ignored.

-  Onefile: On Linux, the ``sys.argv[0]`` was not the original file as
   advertised.

-  Standalone: Do not consider ``.mesh`` and ``.frag`` files as DLls in
   the Qt bindings when including the qml support. This was causing
   errors on Linux, but was generally wasteful.

-  Fix, project options could be injected twice, which could lead to
   errors with options that were only allowed once, e.g.
   ``--linux-onefile-icon``.

-  Windows: When updating the resources in created binaries, treat all
   kinds of ``OSError`` with information output.

-  Onefile: Remove onefile target binary path at startup as well, so it
   cannot cause confusion after error exit.

-  Onefile: In case of error exit from ``AppImage``, preserve its
   outputs and attempt to detect if there was a locking issue.

-  Standalone: Scan package folders on Linux for DLLs too. This is
   necessary to properly handle ``PyQt5`` in case of Qt installed in the
   system as well.

-  Standalone: On Linux, standard QML files were not found.

-  Standalone: Enforce C locale when detecting DLLs on Linux, otherwise
   whitelisting messages didn't work properly on newer Linux.

-  Standalone: Added support for ``tzdata`` package data files.

-  Standalone: Added support for ``exchangelib``.

-  Python3.9: Fix, type subscripts could cause optimization errors.

-  UI: Project options didn't properly handle quoting of arguments,
   these are normally removed by the shell.

-  Linux: The default icon for Python in the system is now found with
   more version specific names and should work on more systems.

-  Standalone: Do not include ``libstdc++`` as it should come from the
   system rather.

**************
 New Features
**************

-  Added plugin ``anti-bloat`` plugin, intended to fight bloat. For now
   it can make including certain modules an error, a warning, or force
   ``ImportError``, e.g. ``--noinclude-setuptools-mode=nofollow`` is
   very much recommended to limit compilation size.

-  The ``pkg-resources`` builtin now covers ``metadata`` and
   importlib_metadata packages for compile time version resolution as
   well.

-  Added support for ``PySide2`` on Python version before 3.6, because
   the patched code needs no workarounds. Fixed in 0.6.14.3 already.

-  Windows: Convert images to icon files on the fly. So now you can
   specify multiple PNG files, and Nuitka will create an icon out of
   that automatically.

-  macOS: Automatically download ``ccache`` binary if not present.

-  Plugins: New interface to query the main script path. This allows
   plugins to look at its directory.

-  UI: Output the versions of Nuitka and Python during compilation.

-  UI: Added option to control static linking. So far this had been
   enabled only automatically for cases where we are certain, but this
   allows to force enable or disable it. Now an info is given, if Nuitka
   thinks it might be possible to enable it, but doesn't do it
   automatically.

-  UI: Added ``--no-onefile`` to disable ``--onefile`` from project
   options.

**************
 Optimization
**************

-  Much enhanced GIL interaction with Python3.9 giving a big speed boost
   and better threading behaviour.

-  Faster conversion of iterables to ``list``, if size can be know,
   allocation ahead saves a lot of effort.

-  Added support for ``GenericAlias`` objects as compile time constants.

****************
 Organizational
****************

-  Enhanced GitHub issue raising instructions.

-  Apply ``rstfmt`` to all documentation and make it part of the commit
   hook.

-  Make sure to check Scons files as well. This would have caught the
   code used to disable ``clcache`` temporarily.

-  Do not mention Travis in PR template anymore, we have stopped using
   it.

-  Updated requirements to latest versions.

-  Bump requirements for development to 3.7 at least, toosl like black
   do not work with 3.6 anymore.

-  Started work on Nuitka Python, a CPython fork intended for enhanced
   performance and standalone support with Nuitka.

**********
 Cleanups
**********

-  Determine system prefix without virtualenv outside of Scons, such
   that plugins can share the code. There was duplication with the
   ``numpy`` plugin, and this will only be more complete using all
   approaches. This also removes a lot of noise from the scons file
   moving it to shared code.

-  The Qt plugins now collect QML files with cleaner code.

*******
 Tests
*******

-  Nicer error message if a wrong search mode is given.

-  Windows: Added timeout for determining run time traces with
   dependency walker, sometimes this hangs.

-  Added test to cover the zip importer.

-  Making use of project options in onefile tests, making it easier to
   execute them manually.

*********
 Summary
*********

For Windows, it's now easier than ever to create an icon for your
deployment, because you can use PNG files, and need not produce ICO
files anymore, with Nuitka doing that for you.

The onefile for Linux had some more or less severe problems that got
addressed, esp. also when it came to QML applications with PySide.

On the side, we are preparing to greatly improve the caching of Nuitka,
starting with retaining modules that were demoted to bytecode. There are
changes in this release, to support that, but it's not yet complete. We
expect that scalability will then be possible to improve even further.

Generally this is mostly a maintenance release, which outside of the
threading performance improvement has very little to offer for faster
execution, but that actually does a lot. Unfortunately right now it's
limited to 3.9, but some of the newer Python's will also be supported in
later releases.
