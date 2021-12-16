This is to inform you about the new stable release
of `Nuitka <https://nuitka.net>`_. It is the extremely
compatible Python compiler,  `"download now" </doc/download.html>`_.

This is to inform you about the new stable release of Nuitka. This time
it contains mostly organisational improvements, some bug fixes, improved
compatibility and cleanups.

It is again the result of working towards compilation of a real program
(Mercurial). This time, I have added support for proper handling of
compiled types by the ``inspect`` module.

Bug fixes
=========

-  Fix for "Missing checks in parameter parsing with star list, star
   dict and positional arguments". There was whole in the checks for
   argument counts, now the correct error is given. Fixed in 0.3.13a
   already.

-  The simple slice operations with 2 values, not extended with 3
   values, were not applying the correct order for evaluation. Fixed in
   0.3.13a already.

-  The simple slice operations couldn't handle ``None`` as the value for
   lower or upper index. Fixed in 0.3.11a already.

-  The in-place simple slice operations evaluated the slice index
   expressions twice, which could cause problems if they had side
   effects. Fixed in 0.3.11a already.

New Features
============

-  Run time patching the ``inspect`` module so it accepts compiled
   functions, compiled methods, and compiled generator objects. The
   ``test_inspect`` test of CPython is nearly working unchanged with
   this.

-  The generator functions didn't have ``CO_GENERATOR`` set in their
   code object, setting it made compatible with CPython in this regard
   too. The inspect module will therefore return correct value for
   ``inspect.isgeneratorfunction()`` too.

Optimization
============

-  Slice indexes that are ``None`` are now constant propagated as well.

-  Slightly more efficient code generation for dual star arg functions,
   removing useless checks.

Cleanups
========

-  Moved the Scons, static C++ files, and assembler files to new package
   ``nuitka.build`` where also now ``SconsInterface`` module lives.

-  Moved the Qt dialog files to ``nuitka.gui``

-  Moved the "unfreezer" code to its own static C++ file.

-  Some PyLint cleanups.

New Tests
=========

-  New test ``Recursion`` to cover recursive functions.

-  New test ``Inspection`` to cover the patching of ``inspect`` module.

-  Cover ``execfile`` on the class level as well in ``ExecEval`` test.

-  Cover evaluation order of simple slices in ``OrderCheck`` too.

Organisational
==============

-  There is a new issue tracker available under http://bugs.nuitka.net

   Please register and report issues you encounter with Nuitka. I have
   put all the known issues there and started to use it recently. It's
   Roundup based like http://bugs.python.org is, so people will find it
   familiar.

-  The ``setup.py`` is now apparently functional. The source releases
   for download are made it with, and it appears the binary
   distributions work too. We may now build a windows installer. It's
   currently in testing, we will make it available when finished.

Summary
=======

The new source organisation makes packaging Nuitka really easy now. From
here, we can likely provide "binary" package of Nuitka soon. A windows
installer will be nice.

The patching of ``inspect`` works wonders for compatibility for those
programs that insist on checking types, instead of doing duck typing.
The function call problem, was an issue found by the Mercurial test
suite.

For the "hg.exe" to pass all of its test suite, more work may be needed,
this is the overall goal I am currently striving for. Once real world
programs like Mercurial work, we can use these as more meaningful
benchmarks and resume work on optimization.
