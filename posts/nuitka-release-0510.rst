This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release has a focus on code generation optimization. Doing major
changes away from "C++-ish" code to "C-ish" code, many constructs are
now faster or got looked at and optimized.

Bug Fixes
=========

-  Compatibility: The variable name in locals for the iterator provided
   to the generator expression should be ``.0``, now it is.

-  Generators could leak frames until program exit, these are now
   properly freed immediately.

Optimization
============

-  Faster exception save and restore functions that might be in-lined by
   the backend C compiler.

-  Faster error checks for many operations, where these errors are
   expected, e.g. instance attribute lookups.

-  Do not create traceback and locals dictionary for frame when
   ``StopIteration`` or ``GeneratorExit`` are raised. These tracebacks
   were wasted, as they were immediately released afterwards.

-  Closure variables to functions and parameters of generator functions
   are now attached to the function and generator objects.

-  The creation of functions with closure taking was accelerated.

-  The creation and destruction of generator objects was accelerated.

-  The re-formulation for in-place assignments got simplified and got
   faster doing so.

-  In-place operations of ``str`` were always copying the string, even
   if was not necessary. This corrects `Issue#124
   <http://bugs.nuitka.net/issue124>`__.

   .. code:: python

      a += b  # Was not re-using the storage of "a" in case of strings

-  Python2: Additions of ``int`` for Python2 are now even faster.

-  Access to local variable values got slightly accelerated at the
   expense of closure variables.

-  Added support for optimizing the ``complex`` built-in.

-  Removing unused temporary and local variables as a result of
   optimization, these previously still allocated storage.

Cleanup
=======

-  The use of C++ classes for variable objects was removed. Closure
   variables are now attached as ``PyCellObject`` to the function
   objects owning them.

-  The use of C++ context classes for closure taking and generator
   parameters has been replaced with attaching values directly to
   functions and generator objects.

-  The indentation of code template instantiations spanning multiple was
   not in all cases proper. We were using emission objects that handle
   it new lines in code and mere ``list`` objects, that don't handle
   them in mixed forms. Now only the emission objects are used.

-  Some templates with C++ helper functions that had no variables got
   changed to be properly formatted templates.

-  The internal API for handling of exceptions is now more consistent
   and used more efficiently.

-  The printing helpers got cleaned up and moved to static code,
   removing any need for forward declaration.

-  The use of ``INCREASE_REFCOUNT_X`` was removed, it got replaced with
   proper ``Py_XINCREF`` usages. The function was once required before
   "C-ish" lifted the need to do everything in one function call.

-  The use of ``INCREASE_REFCOUNT`` got reduced. See above for why that
   is any good. The idea is that ``Py_INCREF`` must be good enough, and
   that we want to avoid the C function it was, even if in-lined.

-  The ``assertObject`` function that checks if an object is not
   ``NULL`` and has positive reference count, i.e. is sane, got turned
   into a preprocessor macro.

-  Deep hashes of constant values created in ``--debug`` mode, which
   cover also mutable values, and attempt to depend on actual content.
   These are checked at program exit for corruption. This may help
   uncover bugs.

Organisational
==============

-  Speedcenter has been enhanced with better graphing and has more
   benchmarks now. More work will be needed to make it useful.

-  Updates to the Developer Manual, reflecting the current near finished
   state of "C-ish" code generation.

Tests
=====

-  New reference count tests to cover generator expressions and their
   usage got added.

-  Many new construct based tests got added, these will be used for
   performance graphing, and serve as micro benchmarks now.

-  Again, more basic tests are directly executable with Python3.

Summary
=======

This is the next evolution of "C-ish" coming to pass. The use of C++ has
for all practical purposes vanished. It will remain an ongoing activity
to clear that up and become real C. The C++ classes were a huge road
block to many things, that now will become simpler. One example of these
were in-place operations, which now can be dealt with easily.

Also, lots of polishing and tweaking was done while adding construct
benchmarks that were made to check the impact of these changes. Here,
generators probably stand out the most, as some of the missed
optimization got revealed and then addressed.

Their speed increases will be visible to some programs that depend a lot
on generators.

This release is clearly major in that the most important issues got
addressed, future releases will provide more tuning and completeness,
but structurally the "C-ish" migration has succeeded, and now we can
reap the benefits in the coming releases. More work will be needed for
all in-place operations to be accelerated.

More work will be needed to complete this, but it's good that this is
coming to an end, so we can focus on SSA based optimization for the
major gains to be had.
