This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release contains progress on many fronts, except performance.

The extended coverage from running the CPython 2.7 and CPython 3.2 (partially)
test suites shows in a couple of bug fixes and general improvements in
compatibility.

Then there is a promised new feature that allows to compile whole packages.

Also there is more Python3 compatibility, the CPython 3.2 test suite now
succeeds up to "test_builtin.py", where it finds that ``str`` doesn't support
the new parameters it has gained, future releases will improve on this.

And then of course, more re-formulation work, in this case, class definitions
are now mere simple functions. This and later function references, is the
important and only progress towards type inference.

Bug fixes
---------

- The compiled method type can now be used with ``copy`` module. That means,
  instances with methods can now be copied too. `Issue#40
  <http://bugs.nuitka.net/issue40>`__. Fixed in 0.3.23.1 already.

- The ``assert`` statement as of Python2.7 creates the ``AssertionError``
  object from a given value immediately, instead of delayed as it was with
  Python2.6. This makes a difference for the form with 2 arguments, and if the
  value is a tuple. `Issue#41 <http://bugs.nuitka.net/issue41>`__. Fixed in
  0.3.23.1 already.

- Sets written like this didn't work unless they were predicted at compile
  time:

  .. code-block:: python

     {value}

  This apparently rarely used Python2.7 syntax didn't have code generation yet
  and crashed the compiler. `Issue#42 <http://bugs.nuitka.net/issue42>`__. Fixed
  in 0.3.23.1 already.

- For Python2, the default encoding for source files is ``ascii``, and it is
  now enforced by Nuitka as well, with the same ``SyntaxError``.

- Corner cases of ``exec`` statements with nested functions now give proper
  ``SyntaxError`` exceptions under Python2.

- The ``exec`` statement with a tuple of length 1 as argument, now also gives a
  ``TypeError`` exception under Python2.

- For Python2, the ``del`` of a closure variable is a ``SyntaxError``.

New Features
------------

- Added support creating compiled packages. If you give Nuitka a directory with
  an "__init__.py" file, it will compile that package into a ".so" file. Adding
  the package contents with ``--recurse-dir`` allows to compile complete
  packages now. Later there will be a cleaner interface likely, where the later
  is automatic.

- Added support for providing directories as main programs. It's OK if they
  contain a "__main__.py" file, then it's used instead, otherwise give
  compatible error message.

- Added support for optimizing the ``super`` built-in. It was already working
  correctly, but not optimized on CPython2. But for CPython3, the variant
  without any arguments required dedicated code.

- Added support for optimizing the ``unicode`` built-in under Python2. It was
  already working, but will become the basis for the ``str`` built-in of
  Python3 in future releases.

- For Python3, lots of compatibility work has been done. The Unicode issues
  appear to be ironed out now. The ``del`` of closure variables is allowed and
  supported now. Built-ins like ``ord`` and ``chr`` work more correctly and
  attributes are now interned strings, so that monkey patching classes works.

Organizational
--------------

- Migrated "bin/benchmark.sh" to Python as "misc/run-valgrind.py" and made it a
  bit more portable that way. Prefers "/var/tmp" if it exists and creates
  temporary files in a secure manner. Triggered by the Debian "insecure temp
  file" bug.

- Migrated "bin/make-dependency-graph.sh" to Python as
  "misc/make-dependency-graph.py" and made a more portable and powerful that
  way.

  The filtering is done a more robust way. Also it creates temporary files in a
  secure manner, also triggered by the Debian "insecure temp file" bug.

  And it creates SVG files and no longer PostScript as the first one is more
  easily rendered these days.

- Removed the "misc/gist" git sub-module, which was previously used by
  "misc/make-doc.py" to generate HTML from "`User Manual
  <https://nuitka.net/doc/user-manual.html>`__" and "`Developer Manual
  <https://nuitka.net/doc/developer-manual.html>`__".

  These are now done with Nikola, which is much better at it and it integrates
  with the web site.

- Lots of formatting improvements to the change log, and manuals:

  * Marking identifiers with better suited ReStructured Text markup.
  * Added links to the bug tracker all Issues.
  * Unified wordings, quotation, across the documents.

Cleanups
--------

- The creation of the class dictionaries is now done with normal function
  bodies, that only needed to learn how to throw an exception when directly
  called, instead of returning ``NULL``.

  Also the assignment of ``__module__`` and ``__doc__`` in these has become
  visible in the node tree, allowing their proper optimization.

  These re-formulation changes allowed to remove all sorts of special treatment
  of ``class`` code in the code generation phase, making things a lot simpler.

- There was still a declaration of ``PRINT_ITEMS`` and uses of it, but no
  definition of it.

- Code generation for "main" module and "other" modules are now merged, and no
  longer special.

- The use of raw strings was found unnecessary and potentially still buggy and
  has been removed. The dependence on C++11 is getting less and less.

New Tests
---------

- Updated CPython2.6 test suite "tests/CPython26" to 2.6.8, adding tests for
  recent bug fixes in CPython. No changes to Nuitka were needed in order to
  pass, which is always good news.

- Added CPython2.7 test suite as "tests/CPython27" from 2.7.3, making it public
  for the first time. Previously a private copy of some age, with many no
  longer needed changes had been used by me. Now it is up to par with what was
  done before for "tests/CPython26", so this pending action is finally done.

- Added test to cover Python2 syntax error of having a function with closure
  variables nested inside a function that is an overflow function.

- Added test "BuiltinSuper" to cover ``super`` usage details.

- Added test to cover ``del`` on nested scope as syntax error.

- Added test to cover ``exec`` with a tuple argument of length 1.

- Added test to cover ``barry_as_FLUFL`` future import to work.

- Removed "Unicode" from known error cases for CPython3.2, it's now working.

Summary
-------

This release brought forward the most important remaining re-formulation
changes needed for Nuitka. Removing class bodies, makes optimization yet again
simpler. Still, making function references, so they can be copied, is missing
for value propagation to progress.

Generally, as usual, a focus has been laid on correctness. This is also the
first time, I am release with a known bug though: That is `Issue#39
<http://bugs.nuitka.net/issue39>`__ which I believe now, may be the root cause
of the mercurial tests not yet passing.

The solution will be involved and take a bit of time. It will be about
"compiled frames" and be a (invasive) solution. It likely will make Nuitka
faster too. But this release includes lots of tiny improvements, for Python3
and also for Python2. So I wanted to get this out now.

As usual, please check it out, and let me know how you fare.
