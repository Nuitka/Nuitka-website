.. post:: 2014/08/11 10:29
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.5.4
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release is aiming at preparatory changes to enable optimization
based on SSA analysis, introducing a variable registry, so that
variables no longer trace their references to themselves.

Otherwise, MinGW64 support has been added, and lots of bug fixes were
made to improve the compatibility.

**************
 Optimization
**************

-  Using new variable registry, now properly detecting actual need for
   sharing variables. Optimization may discover that it is unnecessary
   to share a variable, and then it no longer is. This also allows
   ``--debug`` without it reporting unused variable warnings on Python3.

-  Scons startup has been accelerated, removing scans for unused tools,
   and avoiding making more than one gcc version check.

***********
 Bug Fixes
***********

-  Compatibility: In case of unknown encodings, Nuitka was not giving
   the name of the problematic encoding in the error message. Fixed in
   0.5.3.3 already.

-  Submodules with the same name as built-in modules were wrongly
   shadowed. Fixed in 0.5.3.2 already.

-  Python3: Added implementations of ``is_package`` to the meta path
   based loader.

-  Python3.4: Added ``find_spec`` implementation to the meta path based
   loader for increased compatibility.

-  Python3: Corrections for ``--debug`` to work with Python3 and MSVC
   compiler more often.

-  Fixed crash with ``--show-scons`` when no compiler was found. Fixed
   in 0.5.3.5 already.

-  Standalone: Need to blacklist ``lib2to3`` from standard library as
   well. Fixed in 0.5.3.4 already.

-  Python3: Adapted to changes in ``SyntaxError`` on newer Python
   releases, there is now a ``msg`` that can override ``reason``.

-  Standalone Windows: Preserve ``sys.executable`` as it might be used
   to fork binaries.

-  Windows: The caching of Scons was not arch specific, and files could
   be used again, even if changing the arch from ``x86`` to ``x86_64``
   or back.

-  Windows: On 32 bit Python it can happen that with large number of
   generators running concurrently (>1500), one cannot be started
   anymore. Raising an ``MemoryError`` now.

****************
 Organisational
****************

-  Added support for MinGW64. Currently needs to be run with ``PATH``
   environment properly set up.

-  Updated internal version of Scons to 2.3.2, which breaks support for
   VS 2008, but adds support for VS 2013 and VS 2012. The VS 2013 is now
   the recommended compiler.

-  Added RPM package and repository for RHEL 7.

-  The output of ``--show-scons`` now includes the used compiler,
   including the MSVC version.

-  Added option ``--msvc`` to select the MSVC compiler version to use,
   which overrides automatic selection of the latest.

-  Added option ``-python-flag=no_warnings`` to disable user and
   deprecation warnings at run time.

-  Repository for Ubuntu Raring was removed, no more supported by
   Ubuntu.

**********
 Cleanups
**********

-  Made technical and logical sharing decisions separate functions and
   implement them in a dedicated variable registry.

-  The Scons file has seen a major cleanup.

*********
 Summary
*********

This release is mostly a maintenance release. The Scons integrations has
been heavily visited, as has been Python3 and esp. Python3.4
compatibility, and results from the now possible debug test runs.

Standalone should be even more practical now, and MinGW64 is an option
for those cases, where MSVC is too slow.
