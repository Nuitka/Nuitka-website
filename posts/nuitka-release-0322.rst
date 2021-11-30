This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is a continuation of the trend of previous releases, and
added more re-formulations of Python that lower the burden on code
generation and optimization.

It also improves Python3 support substantially. In fact this is the
first release to not only run itself under Python3, but for Nuitka to
*compile itself* with Nuitka under Python3, which previously only worked
for Python2. For the common language subset, it's quite fine now.

Bug fixes
=========

-  List contractions produced extra entries on the call stack, after
   they became functions, these are no more existent. That was made
   possible my making frame stack entries an optional element in the
   node tree, left out for list contractions.

-  Calling a compiled function in an exception handler cleared the
   exception on return, it no longer does that.

-  Reference counter handling with generator ``throw`` method is now
   correct.

-  A module "builtins" conflicted with the handling of the Python
   ``builtins`` module. Those now use different identifiers.

New Features
============

-  New ``metaclass`` syntax for the ``class`` statement works, and the
   old ``__metaclass__`` attribute is properly ignored.

   .. code:: python

      # Metaclass syntax in Python3, illegal in Python2
      class X(metaclass=Y):
          pass

   .. code:: python

      # Metaclass syntax in Python2, no effect in Python3
      class X:
          __metaclass__ = Y

   .. note::

      The way to make a use of a metaclass in a portable way, is to
      create a based class that has it and then inherit from it. Sad,
      isn' it. Surely, the support for ``__metaclass__`` could still
      live.

      .. code:: python

         # For Python2/3 compatible source, we create a base class that has the
         # metaclass used and doesn't require making a choice.

         CPythonNodeMetaClassBase = NodeCheckMetaClass("CPythonNodeMetaClassBase", (object,), {})

-  The ``--dump-xml`` option works with Nuitka running under Python3.
   This was not previously supported.

-  Python3 now also has compatible parameter errors and compatible
   exception error messages.

-  Python3 has changed scope rules for list contractions (assignments
   don't affect outside values) and this is now respected as well.

-  Python3 has gained support for recursive programs and stand alone
   extension modules, these are now both possible as well.

Optimization
============

-  Avoid frame stack entries for functions that cannot raise exceptions,
   i.e. where they would not be used.

   This avoids overhead for the very simple functions. And example of
   this can be seen here:

   .. code:: python

      def simple():
          return 7

-  Optimize ``len`` built-in for non-constant, but known length values.

   An example can be seen here:

   .. code:: python

      # The range isn't constructed at compile time, but we still know its
      # length.
      len(range(10000000))

      # The string isn't constructed at compile time, but we still know its
      # length.
      len("*" * 1000)

      # The tuple isn't constructed, instead it's known length is used, and
      # side effects are maintained.
      len((a(), b()))

   This new optimization applies to all kinds of container creations and
   the ``range`` built-in initially.

-  Optimize conditions for non-constant, but known truth values.

   At this time, known truth values of non-constants means ``range``
   built-in calls with know size and container creations.

   An example can be seen here:

   .. code:: python

      if (a,):
          print "In Branch"

   It's clear, that the tuple will be true, we just need to maintain the
   side effect, which we do.

-  Optimize ``or`` and ``and`` operators for known truth values.

   See above for what has known truth values currently. This will be
   most useful to predict conditions that need not be evaluated at all
   due to short circuit nature, and to avoid checking against constant
   values. Previously this could not be optimized, but now it can:

   .. code:: python

      # The access and call to "something()" cannot possibly happen
      0 and something()

      # Can be replaced with "something()", as "1" is true. If it had a side
      # effect, it would be maintained.
      1 and something()

      # The access and call to "something()" cannot possibly happen, the value
      # is already decided, it's "1".
      1 or something()

      # Can be replaced with "something()", as "0" is false. If it had a side
      # effect, it would be maintained.
      0 or something()

-  Optimize print arguments to become strings.

   The arguments to ``print`` statements are now converted to strings at
   compile time if possible.

   .. code:: python

      print 1

   becomes:

   .. code:: python

      print "1"

-  Combine print arguments to single ones.

   When multiple strings are printed, these are now combined.

   .. code:: python

      print "1+1=", 1 + 1

   becomes:

   .. code:: python

      print "1+1= 2"

Organisational
==============

-  Enhanced Python3 support, enabling support for most basic tests.

-  Check files with PyLint in deterministic (alphabetical) order.

Cleanups
========

-  Frame stack entries are now part of the node tree instead of part of
   the template for every function, generator, class or module.

-  The ``try``/``except``/``else`` has been re-formulated to use an
   indicator variable visible in the node tree, that tells if a handler
   has been executed or not.

-  Side effects are now a dedicated node, used in several optimization
   to maintain the effect of an expression with known value.

New Tests
=========

-  Expanded and adapted basic tests to work for Python3 as well.

-  Added reference count tests for generator functions ``throw``,
   ``send``, and ``close`` methods.

-  Cover calling a function with ``try``/``except`` in an exception
   handler twice. No test was previously doing that.

Summary
=======

This release offers enhanced compatibility with Python3, as well as the
solution to many structural problems. Calculating lengths of large
non-constant values at compile time, is technically a break through, as
is avoiding lengthy calculations. The frame guards as nodes is a huge
improvement, making that costly operational possible to be optimized
away.

There still is more work ahead, before value propagation will be safe
enough to enable, but we are seeing the glimpse of it already. Not for
long, and looking at numbers will make sense.
