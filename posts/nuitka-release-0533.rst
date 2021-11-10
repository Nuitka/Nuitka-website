This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release contains a bunch of fixes, most of which were previously
released as part of hotfixes, and important new optimization for
generators.

***********
 Bug Fixes
***********

-  Fix, nested functions with local classes using outside function
   closure variables were not registering their usage, which could lead
   to errors at C compile time. Fixed in 0.5.32.1 already.

-  Fix, usage of built-in calls in a class level could crash the
   compiler if a class variable was updated with its result. Fixed in
   0.5.32.1 already.

-  Python 3.7: The handling of non-type bases classes was not fully
   compatible and wrong usages were giving ``AttributeError`` instead of
   ``TypeError``. Fixed in 0.5.32.2 already.

-  Python 3.5: Fix, ``await`` expressions didn't annotate their
   exception exit. Fixed in 0.5.32.2 already.

-  Python3: The ``enum`` module usages with ``__new__`` in derived
   classes were not working, due to our automatic ``staticmethod``
   decoration. Turns out, that was only needed for Python2 and can be
   removed, making enum work all the way. Fixed in 0.5.32.3 already.

-  Fix, recursion into ``__main__`` was done and could lead to compiler
   crashes if the main module was named like that. This is not
   prevented. Fixed in 0.5.32.3 already.

-  Python3: The name for list contraction's frames was wrong all along
   and not just changed for 3.7, so drop that version check on it. Fixed
   in 0.5.32.3 already.

-  Fix, the hashing of code objects has creating a key that could
   produce more overlaps for the hash than necessary. Using a ``C1`` on
   line 29 and ``C`` on line 129, was considered the same. And that is
   what actually happened. Fixed in 0.5.32.3 already.

-  macOS: Various fixes for newer Xcode versions to work as well. Fixed
   in 0.5.32.4 already.

-  Python3: Fix, the default ``__annotations__`` was the empty dict and
   could be modified, leading to severe corruption potentially. Fixed in
   0.5.32.4 already.

-  Python3: When an exception is thrown into a generator that currently
   does a ``yield from`` is not to be normalized.

-  Python3: Some exception handling cases of ``yield from`` were leaking
   references to objects. Fixed in 0.5.32.5 already.

-  Python3: Nested namespace packages were not working unless the
   directory continued to exist on disk. Fixed in 0.5.32.5 already.

-  Standalone: Do not include ``icuuc.dll`` which is a system DLL. Fixed
   in 0.5.32.5 already.

-  Standalone: Added hidden dependency of newer version of ``sip``.
   Fixed in 0.5.32.5 already.

-  Standalone: Do not copy file permissions of DLLs and extension
   modules as that makes deleting and modifying them only harder. Fixed
   in 0.5.32.6 already.

-  Windows: The multiprocessing plugin was not always properly patching
   the run time for all module loads, made it more robust. Fixed in
   0.5.32.6 already.

-  Standalone: Do not preserve permissions of copied DLLs, which can
   cause issues with read-only files on Windows when later trying to
   overwrite or remove files.

-  Python3.4: Make sure to disconnect finished generators from their
   frames to avoid potential data corruption. Fixed in 0.5.32.6 already.

-  Python3.5: Make sure to disconnect finished coroutines from their
   frames to avoid potential data corruption. Fixed in 0.5.32.6 already.

-  Python3.6: Make sure to disconnect finished asyncgen from their
   frames to avoid potential data corruption. Fixed in 0.5.32.6 already.

-  Python3.5: Explicit frame closes of frames owned by coroutines could
   corrupt data. Fixed in 0.5.32.7 already.

-  Python3.6: Explicit frame closes of frames owned by asyncgen could
   corrupt data. Fixed in 0.5.32.7 already.

-  Python 3.4: Fix threaded imports by properly handling
   ``_initializing`` in compiled modules ``__spec__`` attributes. Before
   it happen that another thread attempts to use an unfinished module.
   Fixed in 0.5.32.8 already.

-  Fix, the options ``--include-module`` and ``--include-package`` were
   present but not visible in the help output. Fixed in 0.5.32.8
   already.

-  Windows: The multiprocessing plugin failed to properly pass compiled
   functions. Fixed in 0.5.32.8 already.

-  Python3: Fix, optimization for in-place operations on mapping values
   are not allowed and had to be disabled. Fixed in 0.5.32.8 already.

-  Python 3.5: Fixed exception handling with coroutines and asyncgen
   ``throw`` to not corrupt exception objects.

-  Python 3.7: Added more checks to class creations that were missing
   for full compatibility.

-  Python3: Smarter hashing of unicode values avoids increased memory
   usage from cached converted forms in debug mode.

****************
 Organisational
****************

-  The issue tracker on Github is now the one that should be used with
   Nuitka, winning due to easier issue templating and integration with
   pull requests.

-  Document the threading model and exception model to use for MinGW64.

-  Removed the ``enum`` plug-in which is no longer useful after the
   improvements to the ``staticmethod`` handling for Python3.

-  Added Python 3.7 testing for Travis.

-  Make it clear in the documentation that ``pyenv`` is not supported.

-  The version output includes more information now, OS and
   architecture, so issue reports should contain that now.

-  On PyPI we didn't yet indicated Python 3.7 as supported, which it of
   course is.

**************
 New Features
**************

-  Added support for MiniConda Python.

**************
 Optimization
**************

-  Using goto based generators that return from execution and resume
   based on heap storage. This makes tests using generators twice as
   fast and they no longer use a full C stack of 2MB, but only 1K
   instead.

-  Conditional ``a if cond else b``, ``a and b``, ``a or b`` expressions
   of which the result value is are now transformed into conditional
   statements allowing to apply further optimizations to the right and
   left side expressions as well.

-  Replace unused function creations with side effects from their
   default values with just those, removing more unused code.

-  Put all statement related code and declarations for it in a dedicated
   C block, making things slightly more easy for the C compiler to
   re-use the stack space.

-  Avoid linking against ``libpython`` in module mode on everything but
   Windows where it is really needed. No longer check for static Python,
   not needed anymore.

-  More compact function, generator, and asyncgen creation code for the
   normal cases, avoid qualname if identical to name for all of them.

-  Python2 class dictionaries are now indeed directly optimized, giving
   more compact code.

-  Module exception exits and thus its frames have become optional
   allowing to avoid some code for some special modules.

-  Uncompiled generator integration was backported to 3.4 as well,
   improving compatibility and speed there as well.

**********
 Cleanups
**********

-  Frame object and their cache declarations are now handled by the way
   of allocated variable descriptions, avoid special handling for them.

-  The interface to "forget" a temporary variable has been replaced with
   a new method that skips a number for it. This is done to keep
   expression use the same indexes for all their child expressions, but
   this is more explicit.

-  Instead of passing around C variables names for temporary values, we
   now have full descriptions, with C type, code name, storage location,
   and the init value to use. This makes the information more
   immediately available where it is needed.

-  Variable declarations are now created when needed and stored in
   dedicated variable storage objects, which then in can generate the
   code as necessary.

-  Module code generation has been enhanced to be closer to the pattern
   used by functions, generators, etc.

-  There is now only one spot that creates variable declaration, instead
   of previous code duplications.

-  Code objects are now attached to functions, generators, coroutines,
   and asyncgen bodies, and not anymore to the creation of these
   objects. This allows for simpler code generation.

-  Removed fiber implementations, no more needed.

*******
 Tests
*******

-  Finally the asyncgen tests can be enabled in the CPython 3.6 test
   suite as the corrupting crash has been identified.

-  Cover ever more cases of spurious permission problems on Windows.

-  Added the ability to specify specific modules a comparison test
   should recurse to, making some CPython tests follow into modules
   where actual test code lives.

*********
 Summary
*********

This release is huge in many ways.

First, finishing "goto generators" clears an old scalability problem of
Nuitka that needed to be addressed. No more do
generators/coroutines/asyncgen consume too much memory, but instead they
become as lightweight as they ought to be.

Second, the use of variable declarations carying type information all
through the code generation, is an important pre-condition for "C types"
work to resume and become possible, what will be 0.6.0 and the next
release.

Third, the improved generator performance will be removing a lot of
cases, where Nuitka wasn't as fast, as its current state not using "C
types" yet, should allow. It is now consistently faster than CPython for
everything related to generators.

Fourth, the fibers were a burden for the debugging and linking of Nuitka
on various platforms, as they provided deprecated interfaces or not. As
they are now gone, Nuitka ought to definitely work on any platform where
Python works.

From here on, C types work can take it, and produce the results we are
waiting for in the next major release cycle that is about to start.

Also the amount of fixes for this release has been incredibly high. Lots
of old bugs esp. for coroutines and asyncgen have been fixed, this is
not only faster, but way more correct. Mainly due to the easier
debugging and interface to the context code, bugs were far easier to
avoid and/or find.
