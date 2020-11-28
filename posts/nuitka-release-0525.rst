This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release contains a huge amount of bug fixes, lots of optimization
gains, and many new features. It also presents many organizational
improvements, and many cleanups.

***********
 Bug Fixes
***********

-  Python3.5: Coroutine methods using ``super`` were crashing the
   compiler. `Issue#340 <http://bugs.nuitka.net/issue340>`__. Fixed in
   0.5.24.2 already.

-  Python3.3: Generator return values were not properly transmitted in
   case of ``tuple`` or ``StopIteration`` values.

-  Python3.5: Better interoperability between compiled coroutines and
   uncompiled generator coroutines.

-  Python3.5: Added support to compile in Python debug mode under
   Windows too.

-  Generators with arguments were using two code objects, one with, and
   one without the ``CO_NOFREE`` flag, one for the generator object
   creating function, and one for the generator object.

-  Python3.5: The duplicate code objects for generators with arguments
   lead to interoperability issues with between such compiled generator
   coroutines and compiled coroutines. `Issue#341
   <http://bugs.nuitka.net/issue341>`__. Fixed in 0.5.24.2 already.

-  Standalone: On some Linux variants, e.g. Debian Stretch and Gentoo,
   the linker needs more flags to really compile to a binary with
   ``RPATH``.

-  Compatibility: For set literal values, insertion order is wrong on
   some versions of Python, we now detect the bug and emulate it if
   necessary, previous Nuitka was always correct, but incompatible.

   .. code:: python

      {1, 1.0}.pop()  # the only element of the set should be 1

-  Windows: Make the batch files detect where they live at run time,
   instead of during ``setup.py``, making it possible to use them for
   all cases.

-  Standalone: Added package paths to DLL scan for ``depends.exe``, as
   with wheels there now sometimes live important DLLs too.

-  Fix, the clang mode was regressed and didn't work anymore, breaking
   the macOS support entirely.

-  Compatibility: For imports, we were passing for ``locals`` argument a
   real dictionary with actual values. That is not what CPython does, so
   stopped doing it.

-  Fix, for raised exceptions not passing the validity tests, they could
   be used after free, causing crashes.

-  Fix, the environment ``CC`` wasn't working unless also specifying
   ``CXX``.

-  Windows: The value of ``__file__`` in module mode was wrong, and
   didn't point to the compiled module.

-  Windows: Better support for ``--python-debug`` for installations that
   have both variants, it is now possible to switch to the right
   variant.

**************
 New Features
**************

-  Added parsing for shebang to Nuitka. When compiling an executable,
   now Nuitka will check of the ``#!`` portion indicates a different
   Python version and ask the user to clarify with ``--python-version``
   in case of a mismatch.

-  Added support for Python flag ``--python-flag=-O``, which allows to
   disable assertions and remove doc strings.

**************
 Optimization
**************

-  Faster method calls, combining attribute lookup and method call into
   one, where order of evaluation with arguments doesn't matter. This
   gives really huge relative speedups for method calls with no
   arguments.

-  Faster attribute lookup in general for ``object`` descendants, which
   is all new style classes, and all built-in types.

-  Added dedicated ``xrange`` built-in implementation for Python2 and
   ``range`` for Python3. This makes those faster while also solving
   ordering problems when creating constants of these types.

-  Faster ``sum`` again, using quick iteration interface and specialized
   quick iteration code for typical standard type containers, ``tuple``
   and ``list``.

-  Compiled generators were making sure ``StopIteration`` was set after
   their iteration, although most users were only going to clear it. Now
   only the ``send`` method, which really needs that does it. This speed
   up the closing of generators quite a bit.

-  Compiled generators were preparing a ``throw`` into non-started
   compilers, to be checked for immediately after their start. This is
   now handled in a generic way for all generators, saving code and
   execution time in the normal case.

-  Compiled generators were applying checks only useful for manual
   ``send`` calls even during iteration, slowing them down.

-  Compiled generators could duplicate code objects due to handling a
   flag for closure variables differently.

-  For compiled frames, the ``f_trace`` is not writable, but was taking
   and releasing references to what must be ``None``, which is not
   useful.

-  Not passing ``locals`` to import calls make it less code and faster
   too.

****************
 Organizational
****************

-  This release also prepares Python 3.6 support, it includes full
   language support on the level of CPython 3.6.0 with the sole
   exception of the new generator coroutines.

-  The improved mode is now the default, and full compatibility is now
   the option, used by test suites. For syntax errors, improved mode is
   always used, and for test suites, now only the error message is
   compared, but not call stack or caret positioning anymore.

-  Removed long deprecated option "--no-optimization". Code generation
   too frequently depends on not seeing unoptimized code. This has been
   hidden and broken long enough to finally remove it.

-  Added support for Python3.5 numbers to Speedcenter. There are now
   also tags for speedcenter, indicating how well "develop" branch fares
   in comparison to master.

-  With a new tool, source code and developer manual contents can be
   kept in sync, so that descriptions can be quoted there. Eventually a
   full Sphinx documentation might become available, but for now this
   makes it workable.

-  Added repository for Ubuntu Yakkety (16.10) for download.

-  Added repository for Fedora 25 for download.

**********
 Cleanups
**********

-  Moved the tools to compare CPython output, to sort import statements
   (isort) to autoformat the source code (Redbaron usage), and to check
   with PyLint to a common new ``nuitka.tools`` package, runnable with
   ``__main__`` modules and dedicated runners in ``bin`` directory.

-  The tools now share code to find source files, or have it for the
   first time, and other things, e.g. finding needed binaries on Windows
   installations.

-  No longer patch traceback objects dealloc function. Should not be
   needed anymore, and most probably was only bug hiding.

-  Moved handling of ast nodes related to import handling to the proper
   reformulation module.

-  Moved statement generation code to helpers module, making it
   accessible without cyclic dependencies that require local imports.

-  Removed deprecated method for getting constant code objects in favor
   of the new way of doing it. Both methods were still used, making it
   harder to analyse.

-  Removed useless temporary variable initializations from complex call
   helper internal functions. They worked around code generation issues
   that have long been solved.

-  The ABI flags are no longer passed to Scons together with the
   version.

*******
 Tests
*******

-  Windows: Added support to detect and to switch debug Python where
   available to also be able to execute reference counting tests.

-  Added the CPython 3.3 test suite, after cleaning up the worst bits of
   it, and added the brandnew 3.6 test suite with a minimal set of
   changes.

-  Use the original 3.4 test suite instead of the one that comes from
   Debian as it has patched quite a few issues that never made it
   upstream, and might cause crashes.

-  More construct tests, making a difference between old style classes,
   which have instances and new style classes, with their objects.

-  It is now possible to run a test program with Python3 and Valgrind.

*********
 Summary
*********

The quick iteration is a precursor to generally faster iteration over
unknown object iterables. Expanding this to general code generation, and
not just the ``sum`` built-in, might yield significant gains for normal
code in the future, once we do code generation based on type inference.

The faster method calls complete work that was already prepared in this
domain and also will be expanded to more types than compiled functions.
More work will be needed to round this up.

Adding support for 3.6.0 in the early stages of its release, made sure
we pretty much have support for it ready right after release. This is
always a huge amount of work, and it's good to catch up.

This release is again a significant improvement in performance, and is
very important to clean up open ends. Now the focus of coming releases
will now be on both structural optimization, e.g. taking advantage of
the iterator tracing, and specialized code generation, e.g. for those
iterations really necessary to use quick iteration code.
