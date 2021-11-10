This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release brings massive progress on all fronts. The big highlight is
of course: Full Python3.2 support. With this release, the test suite of
CPython3.2 is considered passing when compiled with Nuitka.

Then lots of work on optimization and infrastructure. The major goal of
this release was to get in shape for actual optimization. This is also
why for the first time, it is tested that some things are indeed compile
time optimized to spot regressions easier. And we are having performance
diagrams, `even if weak ones
<https://nuitka.net/pages/performance.html>`__:

**************
 New Features
**************

-  Python3.2 is now fully supported.

-  Fully correct ``metaclass =`` semantics now correctly supported. It
   had been working somewhat previously, but now all the corner cases
   are covered too.

   -  Keyword only parameters.
   -  Annotations of functions return value and their arguments.
   -  Exception causes, chaining, automatic deletion of exception
      handlers ``as`` values.
   -  Added support for starred assigns.
   -  Unicode variable names are also supported, although it's of course
      ugly, to find a way to translate these to C++ ones.

***********
 Bug fixes
***********

-  Checking compiled code with ``instance(some_function,
   types.FunctionType)`` as "zope.interfaces" does, was causing
   compatibility problems. Now this kind of check passes for compiled
   functions too. `Issue#53 <http://bugs.nuitka.net/issue53>`__

-  The frame of modules had an empty locals dictionary, which is not
   compatible to CPython which puts the globals dictionary there too.
   Also discussed in `Issue#53 <http://bugs.nuitka.net/issue53>`__

-  For nested exceptions and interactions with generator objects, the
   exceptions in ``sys.exc_info()`` were not always fully compatible.
   They now are.

-  The ``range`` builtin was not raising exceptions if given arguments
   appeared to not have side effects, but were still illegal, e.g.
   ``range([], 1, -1)`` was optimized away if the value was not used.

-  Don't crash on imported modules with syntax errors. Instead, the
   attempted recursion is simply not done.

-  Doing a ``del`` on ``__defaults`` and ``__module__`` of compiled
   functions was crashing. This was noticed by a Python3 test for
   ``__kwdefaults__`` that exposed this compiled functions weakness.

-  Wasn't detecting duplicate arguments, if one of them was not a plain
   arguments. Star arguments could collide with normal ones.

-  The ``__doc__`` of classes is now only set, where it was in fact
   specified. Otherwise it only polluted the name space of ``locals()``.

-  When ``return`` from the tried statements of a ``try/finally`` block,
   was overridden, by the final block, a reference was leaked. Example
   code:

   .. code:: python

      try:
          return 1
      finally:
          return 2

-  Raising exception instances with value, was leaking references, and
   not raising the ``TypeError`` error it is supposed to do.

-  When raising with multiple arguments, the evaluation order of them
   was not enforced, it now is. This fixes a reference leak when raising
   exceptions, where building the exception was raising an exception.

******************
 New Optimization
******************

-  Optimizing attribute access to compile time constants for the first
   time. The old registry had no actual user yet.

-  Optimizing subscript and slices for all compile time constants beyond
   constant values, made easy by using inheritance.

-  Built-in references now convert to strings directly, e.g. when used
   in a print statement. Needed for the testing approach "compiled file
   contains only prints with constant value".

-  Optimizing calls to constant nodes directly into exceptions.

-  Optimizing built-in ``bool`` for arguments with known truth value.
   This would be creations of tuples, lists, and dictionaries.

-  Optimizing ``a is b`` and ``a is not b`` based on aliasing interface,
   which at this time effectively is limited to telling that ``a is a``
   is true and ``a is not a`` is false, but this will expand.

-  Added support for optimizing ``hasattr``, ``getattr``, and
   ``setattr`` built-ins as well. The ``hasattr`` was needed for the
   ``class`` re-formulation of Python3 anyway.

-  Optimizing ``getattr`` with string argument and no default to simple
   attribute access.

-  Added support for optimizing ``isinstance`` built-in.

-  Was handling "BreakException" and "ContinueException" in all loops
   that used ``break`` or ``continue`` instead of only where necessary.

-  When catching "ReturnValueException", was raising an exception where
   a normal return was sufficient. Raising them now only where needed,
   which also means, function need not catch them ever.

**********
 Cleanups
**********

-  The handling of classes for Python2 and Python3 have been
   re-formulated in Python more completely.

   -  The calling of the determined "metaclass" is now in the node tree,
      so this call may possible to in-line in the future. This
      eliminated some static C++ code.

   -  Passing of values into dictionary creation function is no longer
      using hard coded special parameters, but temporary variables can
      now have closure references, making this normal and visible to the
      optimization.

   -  Class dictionary creation functions are therefore no longer as
      special as they used to be.

   -  There is no class creation node anymore, it's merely a call to
      ``type`` or the metaclass detected.

-  Re-formulated complex calls through helper functions that process the
   star list and dict arguments and do merges, checks, etc.

   -  Moves much C++ code into the node tree visibility.
   -  Will allow optimization to eliminate checks and to compile time
      merge, once in-line functions and loop unrolling are supported.

-  Added "return None" to function bodies without a an aborting
   statement at the end, and removed the hard coded fallback from
   function templates. Makes it explicit in the node tree and available
   for optimization.

-  Merged C++ classes for frame exception keeper with frame guards.

   -  The exception is now saved in the compiled frame object, making it
      potentially more compatible to start with.

   -  Aligned module and function frame guard usage, now using the same
      class.

   -  There is now a clear difference in the frame guard classes. One is
      for generators and one is for functions, allowing to implement
      their different exception behavior there.

-  The optimization registries for calls, subscripts, slices, and
   attributes have been replaced with attaching them to nodes.

   -  The ensuing circular dependency has been resolved by more local
      imports for created nodes.
   -  The package "nuitka.transform.optimization.registries" is no more.
   -  New per node methods "computeNodeCall", "computeNodeSubscript",
      etc. dispatch the optimization process to the nodes directly.

-  Use the standard frame guard code generation for modules too.

   -  Added a variant "once", that avoids caching of frames entirely.

-  The variable closure taking has been cleaned up.

   -  Stages are now properly numbered.
   -  Python3 only stage is not executed for Python2 anymore.
   -  Added comments explaining things a bit better.
   -  Now an early step done directly after building a tree.

-  The special code generation used for unpacking from iterators and
   catching "StopIteration" was cleaned up.

   -  Now uses template, Generator functions, and proper identifiers.

-  The ``return`` statements in generators are now re-formulated into
   ``raise StopIteration`` for generators, because that's what they
   really are. Allowed to remove special handling of ``return`` nodes in
   generators.

-  The specialty of CPython2.6 yielding non-None values of lambda
   generators, was so far implemented in code generation. This was moved
   to tree building as a re-formulation, making it subject to normal
   optimization.

-  Mangling of attribute names in functions contained in classes, has
   been moved into the early tree building. So far it was done during
   code generation, making it invisible to the optimization stages.

-  Removed tags attribute from node classes. This was once intended to
   make up for non-inheritance of similar node kinds, but since we have
   function references, the structure got so clean, it's no more needed.

-  Introduced new package ``nuitka.tree``, where the building of node
   trees, and operations on them live, as well as recursion and variable
   closure.

-  Removed ``nuitka.transform`` and move its former children
   ``nuitka.optimization`` and ``nuitka.finalization`` one level up. The
   deeply nested structure turned out to have no advantage.

-  Checks for Python version was sometimes "> 300", where of course ">=
   300" is the only thing that makes sense.

-  Split out helper code for exception raising from the handling of
   exception objects.

***********
 New Tests
***********

-  The complete CPython3.2 test suite was adapted (no ``__code__``, no
   ``__closure__``, etc.) and is now passing, but only without
   "--debug", because otherwise some of the generated C++ triggers
   (harmless) warnings.

-  Added new test suite designed to prove that expressions that are
   known to be compile time constant are indeed so. This works using the
   XML output done with ``--dump-xml`` and then searching it to only
   have print statements with constant values.

-  Added new basic CPython3.2 test "Functions32" and "ParameterErrors32"
   to cover keyword only parameter handling.

-  Added tests to cover generator object and exception interactions.

-  Added tests to cover ``try/finally`` and ``return`` in one or both
   branches correctly handling the references.

-  Added tests to cover evaluation order of arguments when raising
   exceptions.

****************
 Organisational
****************

-  Changed my email from GMX over to Gmail, the old one will still
   continue to work. Updated the copyright notices accordingly.

-  Uploaded `Nuitka to PyPI <http://pypi.python.org/pypi/Nuitka/>`__ as
   well.

*********
 Summary
*********

This release marks a milestone. The support of Python3 is here. The
re-formulation of complex calls, and the code generation improvements
are quite huge. More re-formulation could be done for argument parsing,
but generally this is now mostly complete.

The 0.3.x series had a lot releases. Many of which brought progress with
re-formulations that aimed at making optimization easier or possible.
Sometimes small things like making "return None" explicit. Sometimes
bigger things, like making class creations normal functions, or getting
rid of ``or`` and ``and``. All of this was important ground work, to
make sure, that optimization doesn't deal with complex stuff.

So, the 0.4.x series begins with this. The focus from now on can be
almost purely optimization. This release contains already some of it,
with frames being optimized away, with the assignment keepers from the
``or`` and ``and`` re-formulation being optimized away. This will be
about achieving goals from the "ctypes" plan as discussed in the
developer manual.

Also the performance page will be expanded with more benchmarks and
diagrams as I go forward. I have finally given up on "codespeed", and do
my own diagrams.
