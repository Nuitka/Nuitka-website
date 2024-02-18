.. post:: 2010/09/17 19:42
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.2.3
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This new release is marking a closing in on feature parity to CPython
2.6 which is an important mile stone. Once this is reached, a "Nuitka
0.3.x" series will strive for performance.

***********
 Bug Fixes
***********

-  Generator functions no longer leak references when started, but not
   finished.

-  Yield can in fact be used as an expression and returns values that
   the generator user ``send()`` to it.

************************************
 Reduced Differences / New Features
************************************

-  Generator functions already worked quite fine, but now they have the
   ``throw()``, ``send()`` and ``close()`` methods.

-  Yield is now an expression as is ought to be, it returns values put
   in by ``send()`` on the generator user.

-  Support for extended slices:

   .. code:: python

      x = d[:42, ..., :24:, 24, 100]
      d[:42, ..., :24:, 24, 100] = "Strange"
      del d[:42, ..., :24:, 24, 100]

************
 Tests Work
************

-  The "test_contextlib" is now working perfectly due to the generator
   functions having a correct ``throw()``. Added that test back, so
   context managers are now fully covered.

-  Added a basic test for "overflow functions" has been added, these are
   the ones which have an unknown number of locals due to the use of
   language constructs ``exec`` or ``from bla import *`` on the function
   level. This one currently only highlights the failure to support it.

-  Reverted removals of extended slice syntax from some parts of the
   CPython test suite.

**********
 Cleanups
**********

-  The compiled generator types are using the new C++0x type safe enums
   feature.

-  Resolved a circular dependency between ``TreeBuilding`` and
   ``TreeTransforming`` modules.
