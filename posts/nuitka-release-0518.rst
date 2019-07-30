This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release mainly has a scalability focus. While there are few compatibility
improvements, the larger goal has been to make Nuitka compilation and the final
C compilation faster.

Bug Fixes
---------

- Compatibility: The nested arguments functions can now be called using their
  keyword arguments.

  .. code-block:: python

    def someFunction(a,(b,c)):
        return a, b, c

    someFunction(a = 1, **{".1" : (2,3)})

- Compatibility: Generators with Python3.4 or higher now also have a
  ``__del__`` attribute, and therefore properly participate in finalization.
  This should improve their interactions with garbage collection reference
  cycles, although no issues had been observed so far.

- Windows: Was outputting command line arguments debug information at program
  start. `Issue#284 <http://bugs.nuitka.net/issue284>`__. Fixed in 0.5.17.1
  already.

Optimization
------------

- Code generated for parameter parsing is now a *lot* less verbose. Python
  level loops and conditionals to generate code for each variable has been
  replaced with C level generic code. This will speed up the backend
  compilation by a lot.

- Function calls with constant arguments were speed up specifically, as their
  call is now fully prepared, and yet using less code. Variable arguments are
  also faster, and all defaulted arguments are also much faster. Method calls
  are not affected by these improvements though.

- Nested argument functions now have a quick call entry point as well, making
  them faster to call too.

- The ``slice`` built-in, and internal creation of slices (e.g. in
  re-formulations of Python3 slices as subscripts) cannot raise. `Issue#262
  <http://bugs.nuitka.net/issue262>`__.

- Standalone: Avoid inclusion of bytecode of ``unittest.test``,
  ``sqlite3.test``, ``distutils.test``, and ``ensurepip``. These are not
  needed, but simply bloat the amount of bytecode used on e.g. macOS.
  `Issue#272 <http://bugs.nuitka.net/issue272>`__.

- Speed up compilation with Nuitka itself by avoid to copying and constructing
  variable lists as much as possible using an always accurate variable
  registry.

Cleanups
--------

- Nested argument functions of Python2 are now re-formulated into a wrapping
  function that directly calls the actual function body with the unpacking of
  nested arguments done in nodes explicitly. This allows for better
  optimization and checks of these steps and potential in-lining of these
  functions too.

- Unified slice object creation and built-in ``slice`` nodes, these were two
  distinct nodes before.

- The code generation for all statement kinds is now done via dispatching from
  a dictionary instead of long ``elif`` chains.

- Named nodes more often consistently, e.g. all loop related nodes start with
  ``Loop`` now, making them easier to group.

- Parameter specifications got simplified to work without variables where it is
  possible.

Organizational
--------------

- Nuitka is now available on the social code platforms gitlab as well.

Summary
-------

Long standing weaknesses have been addressed in this release, also quite a few
structural cleanups have been performed, e.g. strengthening the role of the
variable registry to always be accurate, is groundlaying to further improvement
of optimization.

However, this release cycle was mostly dedicated to performance of the actual
compilation, and more accurate information was needed to e.g. not search for
information that should be instant.

Upcoming releases will focus on usability issues and further optimization, it
was nice however to see speedups of created code even from these scalability
improvements.
