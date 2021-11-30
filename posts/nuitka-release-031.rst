This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release of Nuitka continues the focus on performance and contains
only cleanups and optimization. Most go into the direction of more
readable code, some aim at making the basic things faster, with good
results as to performance as you can see below.

Optimization
============

-  Constants in conditions of conditional expressions (``a if cond else
   d``), ``if``/``elif`` or ``while`` are now evaluated to ``true`` or
   ``false`` directly. Before there would be temporary python object
   created from it which was then checked if it had a truth value.

   All of that is obviously overhead only. And it hurts the typically
   ``while 1:`` infinite loop case badly.

-  Do not generate code to catch ``BreakException`` or
   ``ContinueException`` unless a ``break`` or ``continue`` statement
   being in a ``try: finally:`` block inside that loop actually require
   this.

   Even while uncaught exceptions are cheap, it is still an improvement
   worthwhile and it clearly improves the readability for the normal
   case.

-  The compiler more aggressively prepares tuples, lists and dicts from
   the source code as constants if their contents is "immutable" instead
   of building at run time. An example of a "mutable" tuple would be
   ``({},)`` which is not safe to share, and therefore will still be
   built at run time.

   For dictionaries and lists, copies will be made, under the assumption
   that copying a dictionary will always be faster, than making it from
   scratch.

-  The parameter parsing code was dynamically building the tuple of
   argument names to check if an argument name was allowed by checking
   the equivalent of ``name in argument_names``. This was of course
   wasteful and now a pre-built constant is used for this, so it should
   be much faster to call functions with keyword arguments.

-  There are new templates files and also actual templates now for the
   ``while`` and ``for`` loop code generation. And I started work on
   having a template for assignments.

Cleanups
========

-  Do not generate code for the else of ``while`` and ``for`` loops if
   there is no such branch. This uncluttered the generated code
   somewhat.

-  The indentation of the generated C++ was not very good and whitespace
   was often trailing, or e.g. a real tab was used instead of "\t". Some
   things didn't play well together here.

   Now much of the generated C++ code is much more readable and white
   space cleaner. For optimization to be done, the humans need to be
   able to read the generated code too. Mind you, the aim is not to
   produce usable C++, but on the other hand, it must be possible to
   understand it.

-  To the same end of readability, the empty ``else {}`` branches are
   avoided for ``if``, ``while`` and ``for`` loops. While the C++
   compiler can be expected to remove these, they seriously cluttered up
   things.

-  The constant management code in ``Context`` was largely simplified.
   Now the code is using the ``Constant`` class to find its way around
   the problem that dicts, sets, etc. are not hashable, or that
   ``complex`` is not being ordered; this was necessary to allow deeply
   nested constants, but it is also a simpler code now.

-  The C++ code generated for functions now has two entry points, one
   for Python calls (arguments as a list and dictionary for parsing) and
   one where this has happened successfully. In the future this should
   allow for faster function calls avoiding the building of argument
   tuples and dictionaries all-together.

-  For every function there was a "traceback adder" which was only used
   in the C++ exception handling before exit to CPython to add to the
   traceback object. This was now in-lined, as it won't be shared ever.

Numbers
=======

python 2.6:

.. code::

   Pystone(1.1) time for 50000 passes = 0.65
   This machine benchmarks at 76923.1 pystones/second

Nuitka 0.3.1:

.. code::

   Pystone(1.1) time for 50000 passes = 0.41
   This machine benchmarks at 121951 pystones/second

This is 58% for 0.3.1, up from the 25% before. So it's getting
somewhere. As always you will find its latest version here.
