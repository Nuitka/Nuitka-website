.. post:: 2013/12/05 01:45
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.4.7
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release includes important new features, lots of polishing
cleanups, and some important performance improvements as well.

***********
 Bug Fixes
***********

-  The RPM packages didn't build due to missing in-line copy of Scons.
   Fixed in 0.4.6.1 already.

-  The recursion into modules and unfreezing them was not working for
   packages and modules anymore. Fixed in 0.4.6.2 already.

-  The Windows installer was not including Scons. Fixed in 0.4.6.3
   already.

-  Windows: The immediate execution as performed by ``nuitka --execute``
   was not preserving the exit code.

-  Python3.3: Packages without ``__init.py__`` were not properly
   embedding the name-space package as well.

-  Python3: Fix, modules and packages didn't add themselves to
   ``sys.modules`` which they should, happened only for programs.

-  Python3.3: Packages should set ``__package`` to their own name, not
   the one of their parents.

-  Python3.3: The ``__qualname__`` of nested classes was corrected.

-  For modules that recursed to other modules, an infinite loop could be
   triggered when comparing types with rich comparisons.

**************
 New Features
**************

-  The "standalone" mode allows to compile standalone binaries for
   programs and run them without Python installation. The DLLs loaded by
   extension modules on Windows need to be added manually, on Linux
   these are determined automatically already.

   To achieve running without Python installation, Nuitka learned to
   freeze bytecode as an alternative to compiling modules, as some
   modules need to be present when the CPython library is initialized.

-  New option ``--python-flag`` allows to specify flags to the compiler
   that the "python" binary normally would. So far ``-S`` and ``-v`` are
   supported, with sane aliases ``no_site`` and ``trace_imports``.

   The recommended use of ``--python-flag=-S`` is to avoid dependency
   creep in standalone mode compilations, because the ``site`` module
   often imports many useless things that often don't apply to target
   systems.

**************
 Optimization
**************

-  Faster frame stack handling for functions without ``try``/``except``
   (or ``try``/``finally`` in Python3). This gives a speed boost to
   "PyStone" of ca. 2.5% overall.

-  Python2: Faster attribute getting and setting, handling special cases
   at compile time. This gives a minor speed boost to "PyStone" of ca.
   0.5% overall.

-  Python2: Much quicker calls of ``__getattr__`` and ``__setattr__`` as
   this is now using the quicker call method avoiding temporary tuples.

-  Don't treat variables usages used in functions called directly by
   their owner as shared. This leads to more efficient code generation
   for contractions and class bodies.

-  Create ``unicode`` constants directly from their UTF-8 string
   representation for Python2 as well instead of un-streaming. So far
   this was only done for Python3. Affects only program start-up.

-  Directly create ``int`` and ``long`` constants outside of ``2**31``
   and ``2**32-1``, but only limited according to actual platform
   values. Affects only program start-up.

-  When creating ``set`` values, no longer use a temporary ``tuple``
   value, but use a properly generated helper functions instead. This
   makes creating sets much faster.

-  Directly create ``set`` constants instead of un-streaming them.
   Affects only program start-up.

-  For correct line numbers in traceback, the current frame line number
   must be updated during execution. This was done more often than
   necessary, e.g. loops set the line number before loop entry, and at
   first statement.

-  Module variables are now accessed even faster, the gain for "PyStone"
   is only 0.1% and mostly the result of leaner code.

****************
 Organisational
****************

-  The "standalone mode" code (formerly known as "portable mode" has
   been redone and activated. This is a feature that a lot of people
   expect from a compiler naturally. And although the overall goal for
   Nuitka is of course acceleration, this kind of packaging is one of
   the areas where CPython needs improvement.

-  Added package for Ubuntu 13.10 for download, removed packages for
   Ubuntu 11.04 and 11.10, no more supported.

-  Added package for openSUSE 13.1 for download.

-  Nuitka is now part of Arch and can be installed with ``pacman -S
   nuitka``.

-  Using dedicated `Buildbot <http://buildbot.net>`__ for continuous
   integration testing. Not yet public.

-  Windows: In order to speed up repeated compilation on a platform
   without ``ccache``, added Scons level caching in the build directory.

-  Disabled hash randomization for inside Nuitka (but not in ultimately
   created binaries) for a more stable output, because dictionary
   constants will not change around. This makes the build results
   possible to cache for ``ccache`` and Scons as well.

*******
 Tests
*******

-  The ``programs`` tests cases now fail if module or directory
   recursion is not working, being executed in another directory.

-  Added test runner for packages, with initial test case for package
   with recursion and sub-packages.

-  Made some test cases more strict by reducing ``PYTHONPATH``
   provision.

-  Detect use of extra flags in tests that don't get consumed avoiding
   ineffective flags.

-  Use ``--execute`` on Windows as well, the issue that prevented it has
   been solved after all.

**********
 Cleanups
**********

-  The generated code uses ``const_``, ``var_``, ``par_`` prefixes in
   the generated code and centralized the decision about these into
   single place.

-  Module variables no longer use C++ classes for their access, but
   instead accessor functions, leading to much less code generated per
   module variable and removing the need to trace their usage during
   code generation.

-  The test runners now share common code in a dedicated module,
   previously they replicated it all, but that turned out to be too
   tedious.

-  Massive general cleanups, many of which came from new contributor
   Juan Carlos Paco.

-  Moved standalone and freezer related codes to dedicated package
   ``nuitka.freezer`` to not pollute the ``nuitka`` package name space.

-  The code generation use variable identifiers and their accesses was
   cleaned up.

-  Removed several not-so-special case identifier classes because they
   now behave more identical and all work the same way, so a parameters
   can be used to distinguish them.

-  Moved main program, function object, set related code generation to
   dedicated modules.

*********
 Summary
*********

This release marks major technological progress with the introduction of
the much sought standalone mode and performance improvements from
improved code generation.

The major break through for SSA optimization was not yet achieved, but
this is again making progress in the direction of it. Harmonizing
variables of different kinds was an important step ahead.

Also very nice is the packaging progress, Nuitka was accepted into Arch
after being in Debian Testing for a while already. Hope is to see more
of this kind of integration in the future.
