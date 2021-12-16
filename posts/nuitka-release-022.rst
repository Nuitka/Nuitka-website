This is to inform you about the new stable release
of `Nuitka <https://nuitka.net>`_. It is the extremely
compatible Python compiler,  `"download now" </doc/download.html>`_.

This is some significant progress, a lot of important things were
addressed.

Bug Fixes
=========

-  Scope analysis is now done during the tree building instead of
   sometimes during code generation, this fixed a few issues that didn't
   show up in tests previously.

-  Reference leaks of generator expressions that were not fishing, but
   then deleted are not more.

-  Inlining of exec is more correct now.

-  More accurate exception lines when iterator creation executes
   compiled code, e.g. in a for loop

-  The list of base classes of a class was evaluated in the context of
   the class, now it is done in the context of the containing scope.

-  The first iterated of a generator expression was evaluated in its own
   context, now it is done in the context of the containing scope.

Reduced Differences
===================

-  With the enhanced scope analysis, ``UnboundLocalError`` is now
   correctly supported.

-  Generator expressions (but not yet functions) have a ``throw()``,
   ``send()`` and ``close()`` method.

-  Exec can now write to local function namespace even if ``None`` is
   provided at run time.

-  Relative imports inside packages are now correctly resolved at
   compile time when using ``--deep``.

Cleanups
========

-  The compiled function type got further enhanced and cleaned up.

-  The compiled generator expression function type lead to a massive
   cleanup of the code for generator expressions.

-  Cleaned up namespaces, was still using old names, or "Py*" which is
   reserved to core CPython.

-  Overhaul of the code responsible for ``eval`` and ``exec``, it has
   been split, and it pushed the detection defaults to the C++ compiler
   which means, we can do it at run time or compile time, depending on
   circumstances.

-  Made ``PyTemporaryObject`` safer to use, disabling copy constructor
   it should be also a relief to the C++ compiler if it doesn't have to
   eliminate all its uses.

-  The way delayed work is handled in ``TreeBuilding`` step has been
   changed to use closured functions, should be more readable.

-  Some more code templates have been created, making the code
   generation more readable in some parts. More to come.

New Features
============

-  As I start to consider announcing Nuitka, I moved the version logic
   so that the version can now be queried with ``--version``.

Optimization
============

-  Name lookups for ``None``, ``True`` and ``False`` and now always
   detected as constants, eliminating many useless module variable
   lookups.

New Tests
=========

-  More complete test of generator expressions.

-  Added test program for packages with relative imports inside the
   package.

-  The built-in ``dir()`` in a function was not having fully
   deterministic output list, now it does.

Summary
=======

Overall, the amount of differences between CPython and Nuitka is heading
towards zero. Also most of the improvements done in this release were
very straightforward cleanups and not much work was required, mostly
things are about cleanups and then it becomes easily right. The new type
for the compiled generator expressions was simple to create, esp. as I
could check what CPython does in its source code.

For optimization purposes, I decided that generator expressions and
generator functions will be separate compiled types, as most of their
behavior will not be shared. I believe optimizing generator expressions
to run well is an important enough goal to warrant that they have their
own implementation. Now that this is done, I will repeat it with
generator functions.

Generator functions already work quite fine, but like generator
expressions did before this release, they can leak references if not
finished , and they don't have the ``throw()`` method, which seems very
important to the correct operation of ``contextlib``. So I will
introduce a decicated type for these too, possibly in the next release.
