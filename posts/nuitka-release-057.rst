This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is brings a newly supported platform, bug fixes, and again
lots of cleanups.

***********
 Bug Fixes
***********

-  Fix, creation of dictionary and set literals with non-hashable
   indexes did not raise an exception.

   .. code:: python

      {[]: None}  # This is now a TypeError

******************
 New Optimization
******************

-  Calls to the ``dict`` built-in with only keyword arguments are now
   optimized to mere dictionary creations. This is new for the case of
   non-constant arguments only of course.

   .. code:: python

      dict(a=b, c=d)
      # equivalent to
      {"a": b, "c": d}

-  Slice ``del`` with indexable arguments are now using optimized code
   that avoids Python objects too. This was already done for slice
   look-ups.

-  Added support for ``bytearray`` built-in.

****************
 Organizational
****************

-  Added support for OpenBSD with fiber implementation from library, as
   it has no context support.

**********
 Cleanups
**********

-  Moved slicing solutions for Python3 to the re-formulation stage. So
   far the slice nodes were used, but only at code generation time,
   there was made a distinction between Python2 and Python3 for them.
   Now these nodes are purely Python2 and slice objects are used
   universally for Python3.

*******
 Tests
*******

-  The test runners now have common code to scan for the first file to
   compile, an implementation of the ``search`` mode. This will allow to
   introduce the ability to search for pattern matches, etc.

-  More tests are directly executable with Python3.

-  Added ``recurse_none`` mode to test comparison, making using extra
   options for that purpose unnecessary.

*********
 Summary
*********

This solves long standing issues with slicing and subscript not being
properly distinguished in the Nuitka code. It also contains major bug
fixes that really problematic. Due to the involved nature of these fixes
they are made in this new release.
