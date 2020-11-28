This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

The major point this for this release is cleanup work, and generally bug
fixes, esp. in the field of importing. This release cleans up many small
open ends of Nuitka, closing quite a bunch of consistency ``TODO``
items, and then aims at cleaner structures internally, so optimization
analysis shall become "easy". It is a correctness and framework release,
not a performance improvement at all.

***********
 Bug fixes
***********

-  Imports were not respecting the ``level`` yet. Code like this was not
   working, now it is:

   .. code:: python

      from .. import something

-  Absolute and relative imports were e.g. both tried all the time, now
   if you specify absolute or relative imports, it will be attempted in
   the same way than CPython does. This can make a difference with
   compatibility.

-  Functions with a "locals dict" (using ``locals`` built-in or ``exec``
   statement) were not 100% compatible in the way the locals dictionary
   was updated, this got fixed. It seems that directly updating a dict
   is not what CPython does at all, instead it only pushes things to the
   dictionary, when it believes it has to. Nuitka now does the same
   thing, making it faster and more compatible at the same time with
   these kind of corner cases.

-  Nested packages didn't work, they do now. Nuitka itself is now
   successfully using nested packages (e.g.
   ``nuitka.transform.optimizations``)

**************
 New Features
**************

-  The ``--lto`` option becomes usable. It's not measurably faster
   immediately, and it requires g++ 4.6 to be available, but then it at
   least creates smaller binaries and may provide more optimization in
   the future.

******************
 New Optimization
******************

-  Exceptions raised by pre-computed built-ins, unpacking, etc. are now
   transformed to raising the exception statically.

**********
 Cleanups
**********

-  There is now a ``getVariableForClosure`` that a variable provider can
   use. Before that it guessed from ``getVariableForReference`` or
   ``getVariableForAssignment`` what might be the intention. This makes
   some corner cases easier.

-  Classes, functions and lambdas now also have separate builder and
   body nodes, which enabled to make getSameScopeNodes() really simple.
   Either something has children which are all in a new scope or it has
   them in the same scope.

-  Twisted workarounds like ``TransitiveProvider`` are no longer needed,
   because class builder and class body were separated.

-  New packages ``nuitka.transform.optimizations`` and
   ``nuitka.transform.finalizations``, where the first was
   ``nuitka.optimizations`` before. There is also code in
   ``nuitka.transform`` that was previously in a dedicated module. This
   allowed to move a lot of displaced code.

-  ``TreeBuilding`` now has fast paths for all 3 forms, things that need
   a "provider", "node", and "source_ref"; things that need "node" and
   "source_ref"; things that need nothing at all, e.g. pass.

-  Variables now avoid building duplicated instances, but instead share
   one. Better for analysis of them.

***********
 New Tests
***********

-  The Python 2.7 test suite is no longer run with Python 2.6 as it will
   just crash with the same exception all the time, there is no
   ``importlib`` in 2.6, but every test is using that through
   test_support.

-  Nested packages are now covered with tests too.

-  Imports of upper level packages are covered now too.

****************
 Organizational
****************

-  Updated the "README.txt" with the current plan on optimization.

*********
 Numbers
*********

python 2.6::

   Pystone(1.1) time for 50000 passes = 0.65
   This machine benchmarks at 76923.1 pystones/second

Nuitka 0.3.6 (driven by python 2.6)::

   Pystone(1.1) time for 50000 passes = 0.31
   This machine benchmarks at 161290 pystones/second

This is 109% for 0.3.6, but no change from the previous release. No
surprise, because no new effective new optimization means have been
implemented. Stay tuned for future release for actual progress.
