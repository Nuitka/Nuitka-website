This is to inform you about the new stable release
of `Nuitka <https://nuitka.net>`_. It is the extremely
compatible Python compiler,  `"download now" </doc/download.html>`_.

This releases contains some really major enhancements, all heading
towards enabling value propagation inside Nuitka. Assignments of all
forms are now all simple and explicit, and as a result, now it will be
easy to start tracking them.

Contractions have become functions internally, with statements use
temporary variables, complex unpacking statement were reduced to more
simple ones, etc.

Also there are the usual few small bug fixes, and a bunch of
organisational improvements, that make the release complete.

Bug fixes
=========

-  The built-in ``next`` could causes a program crash when iterating
   past the end of an iterator. Fixed in 0.3.20.1 already.

-  The ``set`` constants could cause a compiler error, as that type was
   not considered in the "mutable" check yet. Fixed in 0.3.20.2 already.

-  Performance regression. Optimize expression for exception types
   caught as well again, this was lost in last release.

-  Functions that contain ``exec``, are supposed to have a writable
   locals. But when removing that ``exec`` statement as part of
   optimization, this property of the function could get lost.

-  The so called "overflow functions" are once again correctly handled.
   These once were left behind in some refactoring and had not been
   repaired until now. An overflow function is a nested function with an
   ``exec`` or a star import.

-  The syntax error for ``return`` outside of a function, was not given,
   instead the code returned at run time. Fixed to raise a
   ``SyntaxError`` at compile time.

Optimization
============

-  Avoid ``tuple`` objects to be created when catching multiple
   exception types, instead call exception match check function multiple
   times.

-  Removal of dead code following ``break``, ``continue``, ``return``,
   and ``raise``. Code that follows these statements, or conditional
   statements, where all branches end with it.

   .. note::

      These may not actually occur often in actual code, but future
      optimization may produce them more frequently, and their removal
      may in turn make other possible optimization.

-  Detect module variables as "read only" after all writes have been
   detected to not be executed as removed. Previously the "read only
   indicator" was determined only once and then stayed the same.

-  Expanded conditional statement optimization to detect cases, where
   condition is a compile time constant, not just a constant value.

-  Optimize away assignments from a variable to the same variable, they
   have no effect. The potential side effect of accessing the variable
   is left intact though, so exceptions will be raised still.

   .. note::

      An exception is where ``len = len`` actually does have an impact,
      because that variable becomes assignable. The "compile itself"
      test of Nuitka found that to happen with ``long`` from the
      ``nuitka.__past__`` module.

-  Created Python3 variant of quick ``unicode`` string access, there was
   no such thing in the CPython C/API, but we make the distinction in
   the source code, so it makes sense to have it.

-  Created an optimized implementation for the built-in ``iter`` with 2
   parameters as well. This allows for slightly more efficient code to
   be created with regards to reference handling, rather than using the
   CPython C/API.

-  For all types of variable assigned in the generated code, there are
   now methods that accept already taken references or not, and the code
   generator picks the optimal variant. This avoids the drop of
   references, that e.g. the local variable will insist to take.

-  Don't use a "context" object for generator functions (and generator
   expressions) that don't need one. And even if it does to store e.g.
   the given parameter values, avoid to have a "common context" if there
   is no closure taken. This avoids useless ``malloc`` calls and speeds
   up repeated generator object creation.

Organisational
==============

-  Changed the Scons build file database to reside in the build
   directory as opposed to the current directory, not polluting it
   anymore. Thanks for the patch go to Michael H Kent, very much
   appreciated.

-  The ``--experimental`` option is no longer available outside of
   checkouts of git, and even there not on stable branches (``master``,
   ``hotfix/...``). It only pollutes ``--help`` output as stable
   releases have no experimental code options, not even development
   version will make a difference.

-  The binary "bin/Nuitka.py" has been removed from the git repository.
   It was deprecated a while ago, not part of the distribution and
   served no good use, as it was a symbolic link only anyway.

-  The ``--python-version`` option is applied at Nuitka start time to
   re-launch Nuitka with the given Python version, to make sure that the
   Python run time used for computations and link time Python versions
   are the same. The allowed values are now checked (2.6, 2.7 and 3.2)
   and the user gets a nice error with wrong values.

-  Added ``--keep-pythonpath`` alias for ``--execute-with-pythonpath``
   option, probably easier to remember.

-  Support ``--debug`` with clang, so it can also be used to check the
   generated code for all warnings, and perform assertions. Didn't
   report anything new.

-  The contents environment variable ``CXX`` determines the default C++
   compiler when set, so that checking with ``CXX=g++-4.7 nuitka-python
   ...`` has become supported.

-  The ``check-with-pylint`` script now has a real command line option
   to control the display of ``TODO`` items.

Cleanups
========

-  Changed complex assignments, i.e. assignments with multiple targets
   to such using a temporary variable and multiple simple assignments
   instead.

   .. code:: python

      a = b = c

   .. code:: python

      _tmp = c
      b = _tmp
      a = _tmp

   In CPython, when one assignment raises an exception, the whole thing
   is aborted, so the complexity of having multiple targets is no more
   needed, now that we have temporary variables in a block.

   All that was really needed, was to evaluate the complete source
   expression only once, but that made code generation contain ugly
   loops that are no more needed.

-  Changed unpacking assignments to use temporary variables. Code like
   this:

   .. code:: python

      a, b = c

   Is handled more like this:

   .. code:: python

      _tmp_iter = iter(c)
      _tmp1 = next(_tmp_iter)
      _tmp2 = next(_tmp_iter)
      if not finished(_tmp_iter):
          raise ValueError("too many values to unpack")
      a = _tmp1
      b = _tmp2

   In reality, not really ``next`` is used, as it wouldn't raise the
   correct exception for unpacking, and the ``finished`` check is more
   condensed into it.

   Generally this cleanup allowed that the ``AssignTargetTuple`` and
   associated code generation was removed, and in the future value
   propagation may optimize these ``next`` and ``iter`` calls away where
   possible. At this time, this is not done yet.

-  Exception handlers assign caught exception value through assignment
   statement.

   Previously the code generated for assigning from the caught exception
   was not considered part of the handler. It now is the first statement
   of an exception handler or not present, this way it may be optimized
   as well.

-  Exception handlers now explicitly catch more than one type.

   Catching multiple types worked by merits of the created tuple object
   working with the Python C/API function called, but that was not
   explicit at all. Now every handler has a tuple of exceptions it
   catches, which may only be one, or if None, it's all.

-  Contractions are now functions as well.

   Contractions (list, dict, and set) are now re-formulated as function
   bodies that contain for loops and conditional statements. This
   allowed to remove a lot of special code that dealt with them and will
   make these easier to understand for optimization and value
   propagation.

-  Global is handled during tree building.

   Previously the global statement was its own node, which got removed
   during the optimization phase in a dedicated early optimization that
   applied its effect, and then removed the node.

   It was determined, that there is no reason to not immediately apply
   the effect of the global variable and take closure variables and add
   them to the provider of that ``global`` statement, allowing to remove
   the node class.

-  Read only module variable detection integrated to constraint
   collection.

   The detection of read only module variables was so far done as a
   separate step, which is no more necessary as the constraint
   collection tracks the usages of module variables anyway, so this
   separate and slow step could be removed.

New Tests
=========

-  Added test to cover order of calls for complex assignments that
   unpack, to see that they make a fresh iterator for each part of a
   complex assignment.

-  Added test that unpacks in an exception catch. It worked, due to the
   generic handling of assignment targets by Nuitka, and I didn't even
   know it can be done, example:

   .. code:: python

      try:
          raise ValueError(1, 2)
      except ValueError as (a, b):
          print "Unpacking caught exception and unpacked", a, b

   Will assign ``a=1`` and ``b=2``.

-  Added test to cover return statements on module level and class
   level, they both must give syntax errors.

-  Cover exceptions from accessing unassigned global names.

-  Added syntax test to show that star imports do not allow other names
   to be imported at the same time as well.

-  Python3 is now also running the compile itself test successfully.

Summary
=======

The progress made towards value propagation and type inference is *very*
significant, and makes those appears as if they are achievable.
