This is to inform you about the new stable release
of `Nuitka <https://nuitka.net>`_. It is the extremely
compatible Python compiler,  `"download now" </doc/download.html>`_.

This release 0.2.4 is likely the last 0.2.x release, as it's the one
that achieved feature parity with CPython 2.6, which was the whole point
of the release series, so time to celebrate. I have stayed away (mostly)
from any optimization, so as to not be premature.

From now on speed optimization is going to be the focus though. Because
right now, frankly, there is not much of a point to use Nuitka yet, with
only a minor run time speed gain in trade for a long compile time. But
hopefully we can change that quickly now.

New Features
============

-  The use of exec in a local function now adds local variables to scope
   it is in.

-  The same applies to ``from module_name import *`` which is now
   compiled correctly and adds variables to the local variables.

Bug Fixes
=========

-  Raises ``UnboundLocalError`` when deleting a local variable with
   ``del`` twice.

-  Raises ``NameError`` when deleting a global variable with ``del``
   twice.

-  Read of to uninitialized closure variables gave ``NameError``, but
   ``UnboundLocalError`` is correct and raised now.

Cleanups
========

-  There is now a dedicated pass over the node tree right before code
   generation starts, so that some analysis can be done as late as that.
   Currently this is used for determining which functions should have a
   dictionary of locals.

-  Checking the exported symbols list, fixed all the cases where a
   ``static`` was missing. This reduces the "module.so" sizes.

-  With gcc the "visibility=hidden" is used to avoid exporting the
   helper classes. Also reduces the "module.so" sizes, because classes
   cannot be made static otherwise.

New Tests
=========

-  Added "DoubleDeletions" to cover behaviour of ``del``. It seems that
   this is not part of the CPython test suite.

-  The "OverflowFunctions" (those with dynamic local variables) now has
   an interesting test, exec on a local scope, effectively adding a
   local variable while a closure variable is still accessible, and a
   module variable too. This is also not in the CPython test suite.

-  Restored the parts of the CPython test suite that did local star
   imports or exec to provide new variables. Previously these have been
   removed.

-  Also "test_with.py" which covers PEP 343 has been reactivated, the
   with statement works as expected.
