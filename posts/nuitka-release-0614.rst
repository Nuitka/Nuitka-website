This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release has few, but important bug fixes. The main focus was on
expanding standalone support, esp. for PySide2, but also and in general
with plugins added that workaround ``pkg_resources`` usage for version
information.

Also an important new features was added, e.g. the project configuration
in the main file should prove to be very useful.

Bug Fixes
=========

-  Compatibility: Fix, modules that failed to import, should be retried
   on next import.

   So far we only ever executed the module body once, but that is not
   how it's supposed to be. Instead, only if it's in ``sys.modules``
   that should happen, which is the case after successful import.

-  Compatibility: Fix, constant ``False`` values in right hand side of
   ``and``/``or`` conditions were generating wrong code if the left side
   was of known ``bool`` shape too.

-  Standalone: Fix, add ``styles`` Qt plugins to list of sensible
   plugins.

   Otherwise no mouse hover events are generated on some platforms.

-  Compatibility: Fix, relative ``from`` imports beyond level 1 were not
   loadingg modules from packages if necessary. Fixed in 0.6.13.3
   already.

-  Standalone: The ``crypto`` DLL check for Qt bindings was wrong. Fixed
   in 0.6.13.2 already.

-  Standalone: Added experimental support for PySide6, but for good
   results, 6.1 will be needed.

-  Standalone: Added support for newer matplotlib. Fixed in 0.6.12.1
   already.

-  Standalone: Reverted changes related to ``pkg_resources`` that were
   causing regressions. Fixed in 0.6.13.1 already.

-  Standalone: Adding missing implicit dependency for ``cytoolz``
   package. Fixed in 0.6.13.1 already.

-  Standalone: Matching for package names to not suggest recompile for
   was broken and didn't match. Fixed in 0.6.13.1 already.

New Features
============

-  Added support for project options.

   When found in the filename provided, Nuitka will inject options to
   the commandline, such that it becomes possible to do a complex
   project with only using

   .. code:: bash

      python -m nuitka filename.py

   .. code:: python

      # Compilation mode, support OS specific.
      # nuitka-project-if: {OS} in ("Windows", "Linux"):
      #    nuitka-project: --onefile
      # nuitka-project-if: {OS} not in ("Windows", "Linux"):
      #    nuitka-project: --standalone

      # The PySide2 plugin covers qt-plugins
      # nuitka-project: --enable-plugin=pyside2
      # nuitka-project: --include-qt-plugins=sensible,qml

      # The pkg-resources plugin is not yet automatic
      # nuitka-project: --enable-plugin=pkg-resources

      # Nuitka Commercial only features follow:

      # Protect the constants from being readable.
      # nuitka-project: --enable-plugin=data-hiding

      # Include datafiles for Qt into the binary directory.
      # nuitka-project: --enable-plugin=datafile-inclusion
      # nuitka-project: --qt-datadir={MAIN_DIRECTORY}
      # nuitka-project: --qt-datafile-pattern=*.js
      # nuitka-project: --qt-datafile-pattern=*.qml
      # nuitka-project: --qt-datafile-pattern=*.svg
      # nuitka-project: --qt-datafile-pattern=*.png

   Refer to the User Manual for a table of directives and the variables
   allowed to be used.

-  Added option to include whole data directory structures in
   standalone.

   The new option ``--include-data-dir`` was added and is mostly
   required for onefile mode, but recommended for standalone too.

-  Added ``pkg-resources`` plugin.

   This one can resolve code like this at compile time without any need
   for pip metadata to be present or used.

   .. code:: python

      pkg_resources.get_distribution("module_name").version
      pkg_resources.get_distribution("module_name").parsed_version

-  Standalone: Also process early imports in optimization.

   Otherwise plugins cannot work on standard library modules. This makes
   it possible to handle them as well.

Optimization
============

-  Faster binary operations.

   Applying lessons learnt during the enhancements for in-place
   operations that initially gave worse results than some manual code,
   we apply the same tricks for all binary operations, which speeds them
   up by significant margins, e.g. 30% for float addition, 25% for
   Python int addition, and still 6% for Python int addition.

-  More direct optimization of unary operations on constant value.

   Without this, ``-1`` was not directly a constant value, but had to go
   through the unary ``-`` operation, which it still does, but now it's
   done at tree building time.

-  More direct optimization for ``not`` in branches.

   Invertible comparisons, i.e. ``is``/``is not`` and ``in``/``not in``
   do not have do be done during optimization. This mainly avoids noise
   during optimization from such unimportant steps.

-  More direct optimization for constant slices.

   These are used in Python3 for all subscripts, e.g. ``a[1:2]`` will
   use ``slice(1,2)`` effectively. For Python2 they are used less often,
   but still. This also avoids a lot of noise during optimization,
   mostly on Python3

-  Scons: Avoid writing database to disk entirely.

   This saves a bit of disk churn and makes it unnecessary to specify
   the location such that it doesn't collide between Python versions.

-  For optimization passes, use previous max total as minimum for next
   pass. That will usually be a more accurate result, rather than
   starting from 1 again. Part of 0.6.13.1 already.

-  Enhancements to the branch merging improve the scalability of Nuitka
   somewhat, although the merging itself is still not very scalable,
   there are some modules that are very slow to optimize still.

-  Use ``orderset`` if available over the inline copy for ``OrderedSet``
   which is much faster and improves Nuitka compile times.

-  Make ``pkgutil`` a hard import too, this is in preparation of more
   optimization for its functions.

Organisational
==============

-  Upstream patches for ``PySide6`` have been contributed and merged
   into the development branch ``dev``. Full support should be available
   once this is released as part of 6.1 which is waiting for Qt 6.1
   naturally.

-  Patches for ``PySide2`` are available to commercial customers, see
   `PySide2 support <https://nuitka.net/pages/pyside2.html>`__ page.

-  Formatted all documents with ``rstfmt`` and made that part of the
   commit hook for Nuitka. It now works for all documents we have.

-  Updated inline copy of ``tqdm`` to 4.59.0 which ought to address
   spurious errors given.

-  User Manual: Remove ``--show-progress`` from the tutoral. The default
   progress bar is then disabled, and is actually much nicer to use.

-  Developer Manual: Added description of how context managers should be
   named.

-  Cleanup language for some warnings and outputs.

   It was still using obsolete "recursion" language rather than talking
   about "following imports", which is the new one.

Cleanups
========

-  Remove dead code related to constants marshal, the data composer has
   replaced this.

-  Avoid internal API usage for loading extension modules on Linux,
   there is a function in ``sys`` module to get the ld flags.

Tests
=====

-  Fix, the ``only`` mode wasn't working properly.

-  Use new project options feature for specific options in basic tests
   allowing to remove them from the test runner.

Summary
=======

For PySide2 things became more perfect, but it takes upstream patches
unfortunately such that only PySide6.1 will be working out of the box
outside of the commercial offering. We will also attempt to provide
workarounds, but there are some things that cannot be done that way.

This release added some more scalability to the optimization process,
however there will be more work needed to make efficient branch merges.

For onefile, a feature to include whole directories had been missing,
and could not easily be achieved with the existing options. This further
rounds this up, now what's considered missing is compression and macOS
support, both of which should be coming in a future release.

For the performance side of things, the binary operator work can
actually yield pretty good gains, with double digit improvements, but
this covers only so much. Much more C types and better type tracing
would be needed, but there was no progress on this front. Future
releases will have to revisit the type tracing to make sure, we know
more about loop variables, etc. so we can achieve the near C speed we
are looking for, at least in the field of ``int`` performance.

This release has largely been driven by the `Nuitka Commercial
</doc/commercial.html>`__ offering and needs for compatibility with more
code, which is of course always a good thing.
