This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release contains the first use of SSA for value propagation and
massive amounts of bug fixes and optimization. Some of the bugs that
were delivered as hotfixes, were only revealed when doing the value
propagation as they still could apply to real code.

***********
 Bug Fixes
***********

-  Fix, relative imports in packages were not working with absolute
   imports enabled via future flags. Fixed in 0.5.12.1 already.

-  Loops were not properly degrading knowledge from inside the loop at
   loop exit, and therefore this could have lead missing checks and
   releases in code generation for cases, for ``del`` statements in the
   loop body. Fixed in 0.5.12.1 already.

-  The ``or`` and ``and`` re-formulation could trigger false assertions,
   due to early releases for compatibility. Fixed in 0.5.12.1 already.

-  Fix, optimizion of calls of constant objects (always an exception),
   crashed the compiler. This corrects `Issue#202
   <http://bugs.nuitka.net/issue202>`__. Fixed in 0.5.12.2 already.

-  Standalone: Added support for ``site.py`` installations with a
   leading ``def`` or ``class`` statement, which is defeating our
   attempt to patch ``__file__`` for it. This corrects `Issue#189
   <http://bugs.nuitka.net/issue189>`__.

-  Compatibility: In full compatibility mode, the tracebacks of ``or``
   and ``and`` expressions are now as wrong as they are in CPython. Does
   not apply to ``--improved`` mode.

-  Standalone: Added missing dependency on ``QtGui`` by ``QtWidgets``
   for PyQt5.

-  macOS: Improved parsing of ``otool`` output to avoid duplicate
   entries, which can also be entirely wrong in the case of Qt plugins
   at least.

-  Avoid relative paths for main program with file reference mode
   ``original``, as it otherwise changes as the file moves.

-  MinGW: The created modules depended on MinGW to be in ``PATH`` for
   their usage. This is no longer necessary, as we now link these
   libraries statically for modules too.

-  Windows: For modules, the option ``--run`` to immediately load the
   modules had been broken for a while.

-  Standalone: Ignore Windows DLLs that were attempted to be loaded, but
   then failed to load. This happens e.g. when both PySide and PyQt are
   installed, and could cause the dreaded conflicting DLLs message. The
   DLL loaded in error is now ignored, which avoids this.

-  MinGW: The resource file used might be empty, in which case it
   doesn't get created, avoiding an error due to that.

-  MinGW: Modules can now be created again. The run time relative code
   uses an API that is WinXP only, and MinGW failed to find it without
   guidance.

**************
 Optimization
**************

-  Make direct calls out of called function creations. Initially this
   applies to lambda functions only, but it's expected to become common
   place in coming releases. This is now 20x faster than CPython.

   .. code:: python

      # Nuitka avoids creating a function object, parsing function arguments:
      (lambda x: x)(something)

-  Propagate assignments from non-mutable constants forward based on SSA
   information. This is the first step of using SSA for real compile
   time optimization.

-  Specialized the creation of call nodes at creation, avoiding to have
   all kinds be the most flexible form (keyword and plain arguments),
   but instead only what kind of call they really are. This saves lots
   of memory, and makes the tree faster to visit.

-  Added support for optimizing the ``slice`` built-in with compile time
   constant arguments to constants. The re-formulation for slices in
   Python3 uses these a lot. And the lack of this optimization prevented
   a bunch of optimization in this area. For Python2 the built-in is
   optimized too, but not as important probably.

-  Added support for optimizing ``isinstance`` calls with compile time
   constant arguments. This avoids static exception raises in the
   ``exec`` re-formulation which tests for ``file`` type, and then
   optimization couldn't tell that a ``str`` is not a ``file`` instance.
   Now it can.

-  Lower in-place operations on immutable types to normal operations.
   This will allow to compile time compute these more accurately.

-  The re-formulation of loops puts the loop condition as a conditional
   statement with break. The ``not`` that needs to apply was only added
   in later optimization, leading to unnecessary compile time efforts.

-  Removed per variable trace visit from optimization, removing useless
   code and compile time overhead. We are going to optimize things by
   making decision in assignment and reference nodes based on forward
   looking statements using the last trace collection.

**************
 New Features
**************

-  Added experimental support for Python 3.5, which seems to be passing
   the test suites just fine. The new ``@`` matrix multiplicator
   operators are not yet supported though.

-  Added support for patching source on the fly. This is used to work
   around a (now fixed) issue with ``numexpr.cpuinfo`` making type
   checks with the ``is`` operation, about the only thing we cannot
   detect.

****************
 Organisational
****************

-  Added repository for Ubuntu Vivid (15.04) for download. Removed
   Ubuntu Saucy and Ubuntu Raring package downloads, these are no longer
   supported by Ubuntu.

-  Added repository for Debian Stretch, after Jessie release.

-  Make it more clear in the documentation that in order to compile
   Python3, a Python2 is needed to execute Scons, but that the end
   result is a Python3 binary.

-  The PyLint checker tool now can operate on directories given on the
   command line, and whitelists an error that is Windows only.

**********
 Cleanups
**********

-  Split up standalone code further, moving ``depends.exe`` handling to
   a separate module.

-  Reduced code complexity of scons interface.

-  Cleaned up where trace collection is being done. It was partially
   still done inside the collection itself instead in the owner.

-  In case of conflicting DLLs for standalone mode, these are now output
   with nicer formatting, that makes it easy to recognize what is going
   on.

-  Moved code to fetch ``depends.exe`` to dedicated module, so it's not
   as much in the way of standalone code.

*******
 Tests
*******

-  Made ``BuiltinsTest`` directly executable with Python3.

-  Added construct test to demonstrate the speed up of direct lambda
   calls.

-  The deletion of ``@test`` for the CPython test suite is more robust
   now, esp. on Windows, the symbolic links are now handled.

-  Added test to cover ``or`` usage with in-place assignment.

-  Cover local relative ``import from .`` with ``absolute_import``
   future flag enabled.

-  Again, more basic tests are now directly executable with Python3.

*********
 Summary
*********

This release is major due to amount of ground covered. The reduction in
memory usage of Nuitka itself (the C++ compiler will still use much
memory) is very massive and an important aspect of scalability too.

Then the SSA changes are truly the first sign of major improvements to
come. In their current form, without eliminating dead assignments, the
full advantage is not taken yet, but the next releases will do this, and
that's a major milestone to Nuitka.

The other optimization mostly stem from looking at things closer, and
trying to work towards function in-lining, for which we are making a lot
of progress now.
