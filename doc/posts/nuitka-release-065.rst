.. post:: 2019/07/30 21:52
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.6.5
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release contains many bug fixes all across the board. There is also
new optimization and many organisational improvements.

***********
 Bug Fixes
***********

-  Python3.4+: Fixed issues with modules that exited with an exception,
   that could lead to a crash, dealing with their ``__spec__`` value.

-  Python3.4+: The ``__loader__`` method ``is_package`` had the wrong
   signature.

-  Python3.6+: Fix for ``async with`` being broken with uncompiled
   generators.

-  Python3.5+: Fix for ``coroutines`` that got their awaited object
   closed behind their back, they were complaining with ``RuntimeError``
   should they be closed themselves.

-  Fix, constant values ``None`` in a bool target that could not be
   optimized away, lead to failure during code generation.

   .. code:: python

      if x() and None:
          ...

-  Standalone: Added support for sha224, sha384, sha512 in crypto
   package.

-  Windows: The icon wasn't properly attached with MinGW64 anymore, this
   was a regression.

-  Windows: For compiler outputs, also attempt preferred locale to
   interpret outputs, so we have a better chance to not crash over MSVC
   error messages that are not UTF-8 compatible.

-  macOS: Handle filename collisions for generated code too, Nuitka now
   treats all filesystems for all OS as case insensitive for this
   purpose.

-  Compatibility: Added support for tolerant ``del`` in class exception
   handlers.

   .. code:: python

      class C:

          try:
              ...
          except Exception as e:
              del e

              # At exception handler exit, "e" is deleted if still assigned

   We already were compatible for functions and modules here, but due to
   the special nature of class variables really living in dictionaries,
   this was delayed. But after some other changes, it was now possible
   to solve this TODO.

-  Standalone: Added support for Python3 variant of Pmw.

-  Fix, the NumPy plugin now handles more installation types.

-  Fix, the qt plugin now handles multiple library paths.

-  Fix, need ``libm`` for some Anaconda variants too.

-  Fix, left over bytecode from plugins could crash the plugin loader.

-  Fix, ``pkgutil.iter_packages`` is now working for loaded packages.

**************
 New Features
**************

-  Python3.8: Followed some of the changes and works with beta2 as a
   Python 3.7, but none of the new features are implemented yet.

-  Added support for Torch, Tensorflow, Gevent, Sklearn, with a new
   Nuitka plugin.

-  Added support for "hinted" compilation, where the used modules are
   determined through a test run.

-  Added support for including TCL on Linux too.

**************
 Optimization
**************

-  Added support for the ``any`` built-in. This handles a wide range of
   type shapes and constant values at compile time, while also having
   optimized C code.

-  Generate code for some ``CLONG`` operations in preparation of
   eventual per expression C type selection, it then will allow to avoid
   objects in many instances.

-  Windows: Avoid creating link libraries for MinGW64 as these have
   become unnecessary is the mean time.

-  Packages: Do not export entry points for all included packages, only
   for the main package name it is importable as.

****************
 Organisational
****************

-  Added support for Visual Studio 2019 as a C compiler backend.

-  Improved plugin documentation describing how to create plugins for
   Nuitka even better.

-  The is now a mode for running the tests called ``all`` which will
   execute all the tests and report their errors, and only fail at the
   very end. This doesn't avoid wasting CPU cycles to report that e.g.
   all tests are broken, but it allows to know all errors before fixing
   some.

-  Added repository for Fedora 30 for download.

-  Added repository for openSUSE 15.1 for download.

-  Ask people to compile hello world program in the GitHub issue
   template, because many times, they have setup problems only.

-  Visual Studio Code is now the recommended IDE and has integrated
   configuration to make it immediately useful.

-  Updated internal copy of Scons to 3.1.0 as it incorporates many of
   our patches.

-  Changed wordings for optimization to use "lowering" as the only term
   to describe an optimization that simplifies.

**********
 Cleanups
**********

-  Plugins: Major refactoring of Nuitka plugin API.

-  Plugins: To locate module kind, use core Nuitka code that handles
   more cases.

-  The test suite runners are also now auto-formatted and checked with
   PyLint.

-  The Scons file is now PyLint clean too.

-  Avoid ``build_definitions.h`` to be included everywhere, in that it's
   only used in the main program part. This makes C linter hate us much
   less for using a non-existent file.

*******
 Tests
*******

-  Run the tests using Travis on macOS for Python2 too.

-  More standalone tests have been properly whitelisting to cover
   openSSL usage from local system.

-  Disabled PySide2 test, it's not useful to fail and ignore it.

-  Tests: Fixups for coverage testing mode.

-  Tests: Temporarily disable some checks for constants code in
   reflected tests as it only exposes ``marshal`` not being
   deterministic.

*********
 Summary
*********

This release is huge again. Main points are compatibility fixes, esp. on
the coroutine side. These have become apparently very compatible now and
we might eventually focus on making them better.

Again, GSoC 2019 is also showing effects, and will definitely continue
to do soin the next release.

Many use cases have been improved, and on an organisational level, the
adoption of Visual Studio Code seems an huge improvement to have a well
configured IDE out of the box too.

In upcoming releases, more built-ins will be optimized, and hopefully
the specialization of operations will hit more and more code with more
of the infrastructure getting there.
