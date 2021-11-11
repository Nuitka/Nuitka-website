This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release includes progress on all fronts. The primary focus was to
advance SSA optimization over older optimization code that was already
in place. In this domain, there are mostly cleanups.

Another focus has been to enhance Scons with MSVC on Windows. Nuitka now
finds an installed MSVC compiler automatically, properly handles
architecture of Python and Windows. This improves usability a lot.

Then this is also very much about bug fixes. There have been several hot
fixes for the last release, but a complicated and major issue forced a
new release, and many other small issues.

And then there is performance. As can be seen in the `performance graph
<https://nuitka.net/pages/performance.html>`__, this release is the
fastest so far. This came mainly from examining the need for comparison
slots for compiled types.

And last, but not least, this also expands the base of supported
platforms, adding Gentoo, and self compiled Python to the mix.

***********
 Bug Fixes
***********

-  Support Nuitka being installed to a path that contains spaces and
   handle main programs with spaces in their paths. `Issue#106
   <http://bugs.nuitka.net/issue106>`__. Fixed in 0.4.5.1 already.

-  Support Python being installed to a path that contains spaces.
   `Issue#106 <http://bugs.nuitka.net/issue106>`__. Fixed in 0.4.5.2
   already.

-  Windows: User provided constants larger than 65k didn't work with
   MSVC. `Issue#108 <http://bugs.nuitka.net/issue108>`__. Fixed in
   0.4.5.3 already.

-  Windows: The option ``--windows-disable-console`` was not effective
   with MSVC. `Issue#107 <http://bugs.nuitka.net/issue107>`__. Fixed in
   0.4.5.3 already.

-  Windows: For some users, Scons was detecting their MSVC installation
   properly already from registry, but it didn't honor the target
   architecture. `Issue#99 <http://bugs.nuitka.net/issue99>`__. Fixed in
   0.4.5.3 already.

-  When creating Python modules, these were marked as executable ("x"
   bit), which they are of course not. Fixed in 0.4.5.3 already.

-  Python3.3: On architectures where ``Py_ssize_t`` is not the same as
   ``long`` this could lead to errors. Fixed in 0.4.5.3 already.

-  Code that was using nested mutable constants and changed the nested
   ones was not executing correctly. `Issue#112
   <http://bugs.nuitka.net/issue112>`__.

-  Python2: Due to list contractions being re-formulated as functions,
   ``del`` was rejected for the variables assigned in the contraction.
   `Issue#111 <http://bugs.nuitka.net/issue111>`__.

   .. code:: python

      [expr(x) for x in iterable()]

      del x  # Should work, was gave an unjustified SyntaxError.

**************
 New Features
**************

-  Compiled types when used in Python comparison now work. Code like
   this will work:

   .. code:: python

      def f():
          pass


      assert type(f) == types.FunctionType

   This of course also works for ``in`` operator, and is another step
   ahead in compatibility, and surprising too. And best of all, this
   works even if the checking code is not compiled with Nuitka.

-  Windows: Detecting MSVC installation from registry, if no compiler is
   already present in PATH.

-  Windows: New options ``--mingw64`` to force compilation with MinGW.

**************
 Optimization
**************

-  Rich comparisons (``==``, ``<``, and the like) are now faster than
   ever before due to a full implementation of its own in Nuitka that
   eliminates a bit of the overhead. In the future, we will aim at
   giving it type hints to make it even faster. This gives a minor speed
   boost to PyStone of ca. 0.7% overall.

-  Integer comparisons are now treated preferably, as they are in
   CPython, which gives 1.3% speed boost to CPython.

-  The SSA based analysis is now used to provide variable scopes for
   temporary variables as well as reference count needs.

**********
 Cleanups
**********

-  Replaced "value friend" based optimization code with SSA based
   optimization, which allowed to remove complicated and old code that
   was still used mainly in optimization of ``or`` and ``and``
   expressions.

-  Delayed declaration of temp variables and their reference type is now
   performed based on information from SSA, which may given more
   accurate results. Not using "variable usage" profiles for this
   anymore.

-  The Scons interface and related code got a massive overhaul, making
   it more consistent and better documented. Also updated the internal
   copy to 2.3.0 for the platforms that use it, mostly Windows.

-  Stop using ``os.system`` and ``subprocess.call(..., shell = True)``
   as it is not really portable at all, use ``subprocess.call(..., shell
   = False)`` instead.

-  As usual lots of cleanups related to line length issues and PyLint.

****************
 Organisational
****************

-  Added support for Gentoo Linux.

-  Added support for self compiled Python versions with and without
   debug enabled. `Issue#110 <http://bugs.nuitka.net/issue110>`__

-  Added use of Nuitka fonts for headers in manuals.

-  Does not install in-line copy of Scons only on systems where it is
   not going to be used, that is mostly non-Windows, and Linux where it
   is not already present. This makes for cleaner RPM packages.

*********
 Summary
*********

While the SSA stuff is not yet bearing performance fruits, it starts to
carry weight. Taking over the temporary variable handling now also means
we can apply the same stuff to local variables later.

To make up for the delay in SSA driven performance improvements, there
is more traditional code acceleration for rich comparisons, making it
significant, and the bug fixes make Nuitka more compatible than ever.

So give this a roll, it's worth it. And feel free to join the mailing
list (since closed) or `make a donation
<https://nuitka.net/pages/donations.html>`__ to support Nuitka.
