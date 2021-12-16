This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This is to inform you about the new stable release of Nuitka. This time
there are a few bug fixes, and the important step that triggered the
release: Nuitka has entered Debian Unstable. So you if want, you will
get stable Nuitka releases from now on via ``apt-get install nuitka``.

The release cycle was too short to have much focus. It merely includes
fixes, which were available as hot fixes, and some additional
optimization and node tree cleanups, as well as source cleanups. But not
much else.

Bug fixes
=========

-  Conditional statements with both branches empty were not optimized
   away in all cases, triggering an assertion of code generation.
   `Issue#16 <http://bugs.nuitka.net/issue16>`__. Released as 0.3.17a
   hot fix already.

-  Nuitka was considering directories to contain packages that had no
   "__init__.py" which could lead to errors when it couldn't find the
   package later in the compilation process. Released as 0.3.17a hot fix
   already.

-  When providing ``locals()`` to ``exec`` statements, this was not
   making the ``locals()`` writable. The logic to detect the case that
   default value is used (``None``) and be pessimistic about it, didn't
   consider the actual value ``locals()``. Released as 0.3.17b hot fix
   already.

-  Compatibility Fix: When no defaults are given, CPython uses ``None``
   for ``func.func_defaults``, but Nuitka had been using ``None``.

Optimization
============

-  If the condition of assert statements can be predicted, these are now
   optimized in a static raise or removed.

-  For built-in name references, there is now dedicated code to look
   them up, that doesn't check the module level at all. Currently these
   are used in only a few cases though.

-  Cleaner code is generated for the simple case of ``print``
   statements. This is not only faster code, it's also more readable.

Cleanups
========

-  Removed the ``CPythonStatementAssert`` node.

   It's not needed, instead at tree building, assert statements are
   converted to conditional statements with the asserted condition
   result inverted and a raise statement with ``AssertionError`` and the
   assertion argument.

   This allowed to remove code and complexity from the subsequent steps
   of Nuitka, and enabled existing optimization to work on assert
   statements as well.

-  Moved built-in exception names and built-in names to a new module
   ``nuitka.Builtins`` instead of having in other places. This was
   previously a bit spread-out and misplaced.

-  Added cumulative ``tags`` to node classes for use in checks. Use it
   annotate which node kinds to visit in e.g. per scope finalization
   steps. That avoids kinds and class checks.

-  New node for built-in name lookups

   This allowed to remove tricks played with adding module variable
   lookups for ``staticmethod`` when adding them for ``__new__`` or
   module variable lookups for ``str`` when predicting the result of
   ``type('a')``, which was unlikely to cause a problem, but an
   important ``TODO`` item still.

Organisational
==============

-  The `"Download" <https://nuitka.net/doc/download.html>`__ page is now
   finally updated for releases automatically.

   This closes `Issue#7 <http://bugs.nuitka.net/issue7>`__ completely.
   Up to this release, I had to manually edit that page, but now
   mastered the art of upload via XMLRCP and a Python script, so that
   don't loose as much time with editing, checking it, etc.

-  The Debian package is backportable to Ubuntu Natty, Maverick,
   Oneiric, I expect to make a separate announcement with links to
   packages.

-  Made sure the test runners worth with bare ``python2.6`` as well.

New Tests
=========

-  Added some tests intended for type inference development.

Summary
=======

This releases contains not as much changes as others, mostly because
it's the intended base for a Debian upload.

The ``exec`` fix was detected by continued work on the branch
``feature/minimize_CPython26_tests_diff`` branch, but that work is now
complete.

It is being made pretty (many git rebase iterations) with lots of Issues
being added to the bug tracker and referenced for each change. The
intention is to have a clean commits repository with the changed made.

But of course, the real excitement is the "type inference" work. It will
give a huge boost to Nuitka. With this in place, new benchmarks may make
sense. I am working on getting it off the ground, but also to make us
more efficient.

So when I learn something. e.g. ``assert`` is not special, I apply it to
the ``develop`` branch immediately, to keep the differences as small as
possible, and to immediately benefit from such improvements.
