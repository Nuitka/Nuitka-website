This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This new release is major milestone 2 work, enhancing practically all
areas of Nuitka. The focus was roundup and breaking new grounds with
structural optimization enhancements.

***********
 Bug fixes
***********

-  Exceptions now correctly stack.

   When you catch an exception, there always was the exception set, but
   calling a new function, and it catching the exception, the values of
   ``sys.exc_info()`` didn't get reset after the function returned.

   This was a small difference (of which there are nearly none left now)
   but one that might effect existing code, which affects code that
   calls functions in exception handling to check something about it.

   So it's good this is resolved now too. Also because it is difficult
   to understand, and now it's just like CPython behaves, which means
   that we don't have to document anything at all about it.

-  Using ``exec`` in generator functions got fixed up. I realized that
   this wouldn't work while working on other things. It's obscure yes,
   but it ought to work.

-  Lambda generator functions can now be nested and in generator
   functions. There were some problems here with the allocation of
   closure variables that got resolved.

-  List contractions could not be returned by lambda functions. Also a
   closure issue.

-  When using a mapping for globals to ``exec`` or ``eval`` that had a
   side effect on lookup, it was evident that the lookup was made twice.
   Correcting this also improves the performance for the normal case.

**************
 Optimization
**************

-  Statically raised as well as predicted exceptions are propagated
   upwards, leading to code and block removal where possible, while
   maintaining the side effects.

   This is brand new and doesn't do everything possible yet. Most
   notable, the matching of raised exception to handlers is not yet
   performed.

-  Built-in exception name references and creation of instances of them
   are now optimized as well, which leads to faster exception
   raising/catching for these cases.

-  More kinds of calls to built-ins are handled, positional parameters
   are checked and more built-ins are covered.

   Notable is that now checks are performed if you didn't potentially
   overload e.g. the ``len`` with your own version in the module.
   Locally it was always detected already. So it's now also safe.

-  All operations and comparisons are now simulated if possible and
   replaced with their result.

-  In the case of predictable true or false conditions, not taken
   branches are removed.

-  Empty branches are now removed from most constructs, leading to
   sometimes cleaner code generated.

**********
 Cleanups
**********

-  Removed the lambda body node and replaced it with function body. This
   is a great win for the split into body and builder. Regular functions
   and lambda functions now only differ in how the created body is used.

-  Large cleanup of the operation/comparison code. There is now only use
   of a simulator function, which exists for every operator and
   comparison. This one is then used in a prediction call, shared with
   the built-in predictions.

-  Added a ``Tracing`` module to avoid future imports of
   ``print_function``, which annoyed me many times by causing syntax
   failures for when I quickly added a print statement, not noting it
   must have the braces.

-  PyLint is happier than ever.

***********
 New Tests
***********

-  Enhanced ``OverflowFunctions`` test to cover even deeper nesting of
   overflow functions taking closure from each level. While it's not yet
   working, this makes clearer what will be needed. Even if this code is
   obscure, I would like to be that correct here.

-  Made ``Operators`` test to cover the `` operator as well.

-  Added to ``ListContractions`` the case where a contraction is
   returned by a lambda function, but still needs to leak its loop
   variable.

-  Enhanced ``GeneratorExpressions`` test to cover lambda generators,
   which is really crazy code:

   .. code:: python

      def y():
          yield ((yield 1), (yield 2))

-  Added to ``ExecEval`` a case where the ``exec`` is inside a
   generator, to cover that too.

-  Activated the testing of ``sys.exc_info()`` in ``ExceptionRaising``
   test.

   This was previously commented out, and now I added stuff to
   illustrate all of the behavior of CPython there.

-  Enhanced ``ComparisonChains`` test to demonstrate that the order of
   evaluations is done right and that side effects are maintained.

-  Added ``BuiltinOverload`` test to show that overloaded built-ins are
   actually called and not the optimized version. So code like this has
   to print 2 lines:

   .. code:: python

      from __builtin__ import len as _len


      def len(x):
          print x


      return _len(x)

      print len(range(9))

****************
 Organisational
****************

-  Changed "README.txt" to no longer say that "Scons" is a requirement.
   Now that it's included (patched up to work with ``ctypes`` on
   Windows), we don't have to say that anymore.

-  Documented the status of optimization and added some more ideas.

-  There is now an option to dump the node tree after optimization as
   XML. Not currently use, but is for regression testing, to identify
   where new optimization and changes have an impact. This make it more
   feasible to be sure that Nuitka is only becoming better.

-  Executable with Python3 again, although it won't do anything, the
   necessary code changes were done.

*********
 Summary
*********

It's nice to see, that I some long standing issues were resolved, and
that structural optimization has become almost a reality.

The difficult parts of exception propagation are all in place, now it's
only details. With that we can eliminate and predict even more of the
stupid code of "pybench" at compile time, achieving more infinite
speedups.
