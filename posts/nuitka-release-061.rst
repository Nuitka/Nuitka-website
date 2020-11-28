This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release comes after a relatively long time, and contains important
new optimization work, and even more bug fixes.

***********
 Bug Fixes
***********

-  Fix, the options ``--[no]follow-import-to=package_name`` was supposed
   to not follow into the given package, but the check was executed too
   broadly, so that e.g. ``package_name2`` was also affected. Fixed in
   0.6.0.1 already.

-  Fix, wasn't detecting multiple recursions into the same package in
   module mode, when attempting to compile a whole sub-package. Fixed in
   0.6.0.1 already.

-  Fix, constant values are used as C boolean values still for some of
   the cases. Fixed in 0.6.0.1 already.

-  Fix, referencing a function cannot raise an exception, but that was
   not annotated. Fixed in 0.6.0.2 already.

-  macOS: Use standard include of C bool type instead of rolling our
   own, which was not compatible with newest Clang. Fixed in 0.6.0.3
   already.

-  Python3: Fix, the ``bytes`` built-in type actually does have a
   ``__float__`` slot. Fixed in 0.6.0.4 already.

-  Python3.7: Types that are also sequences still need to call the
   method ``__class_getitem__`` for consideration. Fixed in 0.6.0.4
   already.

-  Python3.7: Error exits from program exit could get lost on Windows
   due to ``__spec__`` handling not preserving errors. Fixed in 0.6.0.4
   already.

-  Windows: Negative exit codes from Nuitka, e.g. due to a triggered
   assertion in debug mode were not working. Fixed in 0.6.0.4 already.

-  Fix, conditional ``and`` expressions were mis-optimized when not used
   to not execute the right hand side still. Fixed in 0.6.0.4 already.

-  Python3.6: Fix, generators, coroutines, and asyncgen were not
   properly supporting annotations for local variables. Fixed in 0.6.0.5
   already.

-  Python3.7: Fix, class declarations had memory leaks that were
   untestable before 3.7.1 fixed reference count issues in CPython.
   Fixed in 0.6.0.6 already.

-  Python3.7: Fix, asyncgen expressions can be created in normal
   functions without an immediate awaiting of the iterator. This new
   feature was not correctly supported.

-  Fix, star imports on the module level should disable built-in name
   optimization except for the most critical ones, otherwise e.g. names
   like ``all`` or ``pow`` can become wrong. Previous workarounds for
   ``pow`` were not good enough.

-  Fix, the scons for Python3 failed to properly report build errors due
   to a regression of the Scons version used for it. This would mask
   build errors on Windows.

-  Python3.4: Fix, packages didn't indicate that they are packages in
   their ``__spec__`` value, causing issues with ``importlib_resources``
   module.

-  Python3.4: The ``__spec__`` values of compiled modules didn't have
   compatible ``origin`` and ``has_location`` values preventing
   ``importlib_resources`` module from working to load data files.

-  Fix, packages created from ``.pth`` files were also considered when
   checking for sub-packages of a module.

-  Standalone: Handle cases of conflicting DLLs better. On Windows pick
   the newest file version if different, and otherwise just report and
   pick randomly because we cannot really decide which ought to be
   loaded.

-  Standalone: Warn about collisions of DLLs on non-Windows only as this
   can happen with wheels apparently.

-  Standalone: For Windows Python extension modules ``.pyd`` files,
   remove the SxS configuration for cases where it causes problems, not
   needed.

-  Fix: The ``exec`` statement on file handles was not using the proper
   filename when compiling, therefore breaking e.g.
   ``inspect.getsource`` on functions defined there.

-  Standalone: Added support for OpenGL platform plugins to be included
   automatically.

-  Standalone: Added missing implicit dependency for ``zmq`` module.

-  Python3.7: Fix, using the ``-X utf8`` flag on the calling
   interpreter, aka ``--python-flag=utf8_mode`` was not preserved in the
   compiled binary in all cases.

******************
 New Optimization
******************

-  Enabled C target type ``void`` which will catch creating unused stuff
   more immediately and give better code for expression only statements.

-  Enabled in-place optimization for module variables, avoiding write
   back to the module dict for unchanged values, accelerating these
   operations.

-  Compile time memory savings for the ``yield`` node of Python2, no
   need to track if it is in an exception handler, not relevant there.

-  Using the single child node for the ``yield`` nodes gives memory
   savings at compile time for these, while also making them operate
   faster.

-  More kinds of in-place operations are now optimized, e.g. ``int +=
   int`` and the ``bytes`` ones were specialized to perform real
   in-place extension where possible.

-  Loop variables no longer loose type information, but instead collect
   the set of possible type shapes allowing optimization for them.

****************
 Organizational
****************

-  Corrected download link for Arch AUR link of develop package.
-  Added repository for Ubuntu Cosmic (18.10) for download.
-  Added repository for Fedora 29 for download.
-  Describe the exact format used for ``clang-format`` in the Developer
   Manual.
-  Added description how to use CondaCC on Windows to the User Manual.

**********
 Cleanups
**********

-  The operations used for ``async for``, ``async with``, and ``await``
   were all doing a look-up of an awaitable, and then executing the
   ``yield from`` that awaitable as one thing. Now this is split into
   two parts, with a new ``ExpressionYieldFromAwaitable`` as a dedicated
   node.

-  The ``yield`` node types, now 3 share a base class and common
   computation for now, enhancing the one for awaitiable, which was not
   fully annotating everything that can happen.

-  In code generation avoid statement blocks that are not needed,
   because there are no local C variables declared, and properly indent
   them.

*******
 Tests
*******

-  Fixups for the manual Valgrind runner and the UI changes.
-  Test runner detects lock issue of ``clcache`` on Windows and
   considers it a permission problem that causes a retry.

*********
 Summary
*********

This addresses even more corner cases not working correctly, the out of
the box experience should be even better now.

The push towards C level performance for integer operation was held up
by the realization that loop SSA was not yet there really, and that it
had to be implemented, which of course now makes a huge difference for
the cases where e.g. ``bool`` are being used. There is no C type for
``int`` used yet, which limits the impact of optimization to only taking
shortcuts for the supported types. These are useful and faster of
course, but only building blocks for what is to come.

Most of the effort went into specialized helpers that e.g. add a
``float`` and and ``int`` value in a dedicated fashion, as well as
comparison operations, so we can fully operate some minimal examples
with specialized code. This is too limited still, and must be applied to
ever more operations.

What's more is that the benchmarking situation has not improved. Work
will be needed in this domain to make improvements more demonstrable. It
may well end up being the focus for the next release to improve Nuitka
speedcenter to give more fine grained insights across minor changes of
Nuitka and graphs with more history.
