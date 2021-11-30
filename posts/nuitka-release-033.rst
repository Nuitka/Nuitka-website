This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release of Nuitka continues the focus on performance. It also
cleans up a few open topics. One is "doctests", these are now extracted
from the CPython 2.6 test suite more completely. The other is that the
CPython 2.7 test suite is now passed completely. There is some more work
ahead though, to extract all of the "doctests" and to do that for both
versions of the tests.

This means an even higher level of compatibility has been achieved, then
there is performance improvements, and ever cleaner structure.

Bug fixes
=========

Generators
----------

-  Generator functions tracked references to the common and the instance
   context independently, now the common context is not released before
   the instance contexts are.

-  Generator functions didn't check the arguments to ``throw()`` the way
   they are in CPython, now they do.

-  Generator functions didn't trace exceptions to "stderr" if they
   occurred while closing unfinished ones in "del".

-  Generator functions used the slightly different wordings for some
   error messages.

Function Calls
--------------

-  Extended call syntax with ``**`` allows that to use a mapping, and it
   is now checked if it really is a mapping and if the contents has
   string keys.

-  Similarly, extended call syntax with ``*`` allows a sequence, it is
   now checked if it really is a sequence.

-  Error message for duplicate keyword arguments or too little arguments
   now describe the duplicate parameter and the callable the same way
   CPython does.

-  Now checks to the keyword argument list first before considering the
   parameter counts. This is slower in the error case, but more
   compatible with CPython.

Classes
-------

-  The "locals()" built-in when used in the class scope (not in a
   method) now is correctly writable and writes to it change the
   resulting class.

-  Name mangling for private identifiers was not always done entirely
   correct.

Others
------

-  Exceptions didn't always have the correct stack reported.

-  The pickling of some tuples showed that "cPickle" can have
   non-reproducible results, using "pickle" to stream constants now

Optimization
============

-  Access to instance attributes has become faster by writing specific
   code for the case. This is done in JIT way, attempting at run time to
   optimize attribute access for instances.

-  Assignments now often consider what's cheaper for the other side,
   instead of taking a reference to a global variable, just to have to
   release it.

-  The function call code built argument tuples and dictionaries as
   constants, now that is true for every tuple usage.

Cleanups
========

-  The static helper classes, and the prelude code needed have been
   moved to separate C++ files and are now accessed "#include". This
   makes the code inside C++ files as opposed to a Python string and
   therefore easier to read and or change.

New Features
============

-  The generator functions and generator expressions have the attribute
   "gi_running" now. These indicate if they are currently running.

New Tests
=========

-  The script to extract the "doctests" from the CPython test suite has
   been rewritten entirely and works with more doctests now. Running
   these tests created increased the test coverage a lot.

-  The Python 2.7 test suite has been added.

Organisational
==============

-  One can now run multiple "compare_with_cpython" instances in
   parallel, which enables background test runs.

-  There is now a new environment variable "NUITKA_INCLUDE" which needs
   to point to the directory Nuitka's C++ includes live in. Of course
   the "create-environment.sh" script generates that for you easily.

Numbers
=======

python 2.6:

.. code::

   Pystone(1.1) time for 50000 passes = 0.65
   This machine benchmarks at 76923.1 pystones/second

Nuitka 0.3.3:

.. code::

   Pystone(1.1) time for 50000 passes = 0.36
   This machine benchmarks at 138889 pystones/second

This is 80% for 0.3.3, up from 66% before.
