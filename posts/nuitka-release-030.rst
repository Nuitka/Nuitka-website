This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release 0.3.0 is the first release to focus on performance. In the
0.2.x series Nuitka achieved feature parity with CPython 2.6 and that
was very important, but now it is time to make it really useful.

Optimization has been one of the main points, although I was also a bit
forward looking to Python 2.7 language constructs. This release is the
first where I really started to measure things and removed the most
important bottlenecks.

##############
 New Features
##############

-  Added option to control ``--debug``. With this option the C++ debug
   information is present in the file, otherwise it is not. This will
   give much smaller ".so" and ".exe" files than before.

-  Added option ``--no-optimization`` to disable all optimization.

   It enables C++ asserts and compiles with less aggressive C++ compiler
   optimization, so it can be used for debugging purposes.

-  Support for Python 2.7 set literals has been added.

##########################
 Performance Enhancements
##########################

-  Fast global variables: Reads of global variables were fast already.
   This was due to a trick that is now also used to check them and to do
   a much quicker update if they are already set.

-  Fast ``break``/``continue`` statements: To make sure these statements
   execute the finally handlers if inside a try, these used C++
   exceptions that were caught by ``try``/``finally`` in ``while`` or
   ``for`` loops.

   This was very slow and had very bad performance. Now it is checked if
   this is at all necessary and then it's only done for the rare case
   where a ``break``/``continue`` really is inside the tried block.
   Otherwise it is now translated to a C++ ``break``/``continue`` which
   the C++ compiler handles more efficiently.

-  Added ``unlikely()`` compiler hints to all errors handling cases to
   allow the C++ compiler to generate more efficient branch code.

-  The for loop code was using an exception handler to make sure the
   iterated value was released, using ``PyObjectTemporary`` for that
   instead now, which should lead to better generated code.

-  Using constant dictionaries and copy from them instead of building
   them at run time even when contents was constant.

###########
 New Tests
###########

-  Merged some bits from the CPython 2.7 test suite that do not harm
   2.6, but generally it's a lot due to some ``unittest`` module
   interface changes.

-  Added CPython 2.7 tests ``test_dictcomps.py`` and
   ``test_dictviews.py`` which both pass when using Python 2.7.

-  Added another benchmark extract from "PyStone" which uses a while
   loop with break.

#########
 Numbers
#########

python 2.6:

.. code::

   Pystone(1.1) time for 50000 passes = 0.65
   This machine benchmarks at 76923.1 pystones/second

Nuitka 0.3.0:

.. code::

   Pystone(1.1) time for 50000 passes = 0.52
   This machine benchmarks at 96153.8 pystones/second

That's a 25% speedup now and a good start clearly. It's not yet in the
range of where i want it to be, but there is always room for more. And
the ``break``/``continue`` exception was an important performance
regression fix.
