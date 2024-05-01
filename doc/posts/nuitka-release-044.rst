.. post:: 2013/06/27 00:16
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.4.4
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release marks the point, where Nuitka for the first time supports
all major current Python versions and all major features. It adds Python
3.3 support and it adds support for threading. And then there is a
massive amount of fixes that improve compatibility even further.

Aside of that, there is major performance work. One side is the
optimization of call performance (to CPython non-compiled functions) and
to compiled functions, both. This gave a serious improvement to
performance.

Then of course, we are making other, long term performance progress, as
in "--experimental" mode, the SSA code starts to optimize unused code
away. That code is not yet ready for prime time yet, but the trace
structure will hold.

**************
 New Features
**************

-  Python3.3 support.

   The test suite of CPython3.3 passes now too. The ``yield from`` is
   now supported, but the improved argument parsing error messages are
   not implemented yet.

-  Tracing user provided constants, now Nuitka warns about too large
   constants produced during optimization.

-  Line numbers of expressions are now updates as evaluation progresses.
   This almost corrects.

   Now only expression parts that cannot raise, do not update, which can
   still cause difference, but much less often, and then definitely
   useless.

-  Experimental support for threads.

   Threading appears to work just fine in the most cases. It's not as
   optimal as I wanted it to be, but that's going to change with time.

**************
 Optimization
**************

-  Previous corrections for ``==``, ``!=``, and ``<=``, caused a
   performance regression for these operations in case of handling
   identical objects.

   For built-in objects of sane types (not ``float``), these operations
   are now accelerated again. The overreaching acceleration of ``>=``
   was still there (bug, see below) and has been adapted too.

-  Calling non-compiled Python functions from compiled functions was
   slower than in CPython. It is now just as fast.

-  Calling compiled functions without keyword arguments has been
   accelerated with a dedicated entry point that may call the
   implementation directly and avoid parameter parsing almost entirely.

-  Making calls to compiled and non-compiled Python functions no longer
   requires to build a temporary tuple and therefore is much faster.

-  Parameter parsing code is now more compact, and re-uses error raises,
   or creates them on the fly, instead of hard coding it. Saves binary
   size and should be more cache friendly.

***********
 Bug Fixes
***********

-  Corrected false optimization of ``a >= a`` on C++ level.

   When it's not done during Nuitka compile time optimization, the rich
   comparison helper still contained short cuts for ``>=``. This is now
   the same for all the comparison operators.

-  Calling a function with default values, not providing it, and not
   providing a value for a value without default, was not properly
   detecting the error, and instead causing a run time crash.

   .. code:: python

      def f(a, b=2):
          pass


      f(b=2)

   This now properly raises the ``TypeError`` exception.

-  Constants created with ``+`` could become larger than the normally
   enforced limits. Not as likely to become huge, but still potentially
   an issue.

-  The ``vars`` built-in, when used on something without ``__dict__``
   attribute, was giving ``AttributeError`` instead of ``TypeError``.

-  When re-cursing to modules at compile time, script directory and
   current directory were used last, while at run time, it was the other
   way around, which caused overloaded standard library modules to not
   be embedded.

   Thanks for the patch to James Michael DuPont.

-  Super without arguments was not raising the correct ``RuntimeError``
   exception in functions that cannot be methods, but
   ``UnboundLocalError`` instead.

   .. code:: python

      def f():
          super()  # Error, cannot refer to first argument of f

-  Generators no longer use ``raise StopIteration`` for return
   statements, because that one is not properly handled in
   ``try``/``except`` clauses, where it's not supposed to trigger, while
   ``try``/``finally`` should be honored.

-  Exception error message when throwing non-exceptions into generators
   was not compatible.

-  The use of ``return`` with value in generators is a ``SyntaxError``
   before Python3.3, but that was not raised.

-  Variable names of the "__var" style need to be mangled. This was only
   done for classes, but not for functions contained in classes, there
   they are now mangled too.

-  Python3: Exceptions raised with causes were not properly chaining.

-  Python3: Specifying the file encoding corrupted line numbers, making
   them all of by one.

**********
 Cleanups
**********

-  For containers (``tuple``, ``list``, ``set``, ``dict``) defined on
   the source code level, Nuitka immediately created constant references
   from them.

   For function calls, class creations, slice objects, this code is now
   re-used, and its dictionaries and tuples, may now become constants
   immediately, reducing noise in optimization steps.

-  The parameter parsing code got cleaned up. There were a lot of relics
   from previously explored paths. And error raises were part of the
   templates, but now are external code.

-  Global variable management moved to module objects and out of
   "Variables" module.

-  Make sure, nodes in the tree are not shared by accident.

   This helped to find a case of duplicate use in the complex call
   helpers functions. Code generation will now notice this kind of
   duplication in debug mode.

-  The complex call helper functions were manually taking variable
   closure, which made these functions inconsistent to other functions,
   e.g. no variable version was allocated to assignments.

   Removing the manual setting of variables allowed a huge reduction of
   code volume, as it became more generic code.

-  Converting user provided constants to create containers into
   constants immediately, to avoid noise from doing this in
   optimization.

-  The ``site`` module is now imported explicitly in the ``__main__``
   module, so it can be handled by the recursion code as well. This will
   help portable mode.

-  Many line length 80 changes, improved comments.

***********
 New Tests
***********

-  The CPython3.3 test suite was added, and run with both Python3.2 and
   Python3.3, finding new bugs.

-  The ``doctest`` to code generation didn't successfully handle all
   tests, most notably, "test_generators.py" was giving a
   ``SyntaxError`` and therefore not actually active. Correcting that
   improved the coverage of generator testing.

****************
 Organizational
****************

-  The portable code is still delayed.

   Support for Python3.3 was a higher priority, but the intention is to
   get it into shape for Europython still.

   Added notes about it being disabled it in the `User Manual
   <https://nuitka.net/doc/user-manual.html>`__ documentation.

*********
 Summary
*********

This release is in preparation for Europython 2013. Wanted to get this
much out, as it changes the status slides quite a bit, and all of that
was mostly done in my Cyprus holiday a while ago.

The portable code has not seen progress. The idea here is to get this
into a development version later.
