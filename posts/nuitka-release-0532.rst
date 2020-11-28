This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release contains substantial new optimization, bug fixes, and
already the full support for Python 3.7. Among the fixes, the enhanced
coroutine work for compatibility with uncompiled ones is most important.

***********
 Bug Fixes
***********

-  Fix, was optimizing write backs of attribute in-place assignments
   falsely.

-  Fix, generator stop future was not properly supported. It is now the
   default for Python 3.7 which showed some of the flaws.

-  Python3.5: The ``__qualname__`` of coroutines and asyncgen was wrong.

-  Python3.5: Fix, for dictionary unpackings to calls, check the keys if
   they are string values, and raise an exception if not.

-  Python3.6: Fix, need to check assignment unpacking for too short
   sequences, we were giving ``IndexError`` instead of ``ValueError``
   for these. Also the error messages need to consider if they should
   refer to "at least" in their wording.

-  Fix, outline nodes were cloned more than necessary, which would
   corrupt the code generation if they later got removed, leading to a
   crash.

-  Python3.5: Compiled coroutines awaiting uncompiled coroutines was not
   working properly for finishing the uncompiled ones. Also the other
   way around was raising a ``RuntimeError`` when trying to pass an
   exception to them when they were already finished. This should
   resolve issues with ``asyncio`` module.

-  Fix, side effects of a detected exception raise, when they had an
   exception detected inside of them, lead to an infinite loop in
   optimization. They are now optimized in-place, avoiding an extra step
   later on.

**************
 New Features
**************

-  Support for Python 3.7 with only some corner cases not supported yet.

**************
 Optimization
**************

-  Delay creation of ``StopIteration`` exception in generator code for
   as long as possible. This gives more compact code for generations,
   which now pass the return values via compiled generator attribute for
   Python 3.3 or higher.

-  Python3: More immediate re-formulation of classes with no bases.
   Avoids noise during optimization.

-  Python2: For class dictionaries that are only assigned from values
   without side effects, they are not converted to temporary variable
   usages, allowing the normal SSA based optimization to work on them.
   This leads to constant values for class dictionaries of simple
   classes.

-  Explicit cleanup of nodes, variables, and local scopes that become
   unused, has been added, allowing for breaking of cyclic dependencies
   that prevented memory release.

*******
 Tests
*******

-  Adapted 3.5 tests to work with 3.7 coroutine changes.
-  Added CPython 3.7 test suite.

**********
 Cleanups
**********

-  Removed remaining code that was there for 3.2 support. All uses of
   version comparisons with 3.2 have been adapted. For us, Python3 now
   means 3.3, and we will not work with 3.2 at all. This removed a fair
   bit of complexity for some things, but not all that much.

-  Have dedicated file for import released helpers, so they are easier
   to find if necessary. Also do not have code for importing a name in
   the header file anymore, not performance relevant.

-  Disable Python warnings when running scons. These are particularly
   given when using a Python debug binary, which is happening when
   Nuitka is run with ``--python-debug`` option and the inline copy of
   Scons is used.

-  Have a factory function for all conditional statement nodes created.
   This solved a TODO and handles the creation of statement sequences
   for the branches as necessary.

-  Split class reformulation into two files, one for Python2 and one for
   Python3 variant. They share no code really, and are too confusing in
   a single file, for the huge code bodies.

-  Locals scopes now have a registry, where functions and classes
   register their locals type, and then it is created from that.

-  Have a dedicated helper function for single argument calls in static
   code that does not require an array of objects as an argument.

****************
 Organizational
****************

-  There are now ``requirements-devel.txt`` and ``requirements.txt``
   files aimed at usage with scons and by users, but they are not used
   in installation.

*********
 Summary
*********

This releases has this important step to add conversion of locals
dictionary usages to temporary variables. It is not yet done everywhere
it is possible, and the resulting temporary variables are not yet
propagated in the all the cases, where it clearly is possible. Upcoming
releases ought to achieve that most Python2 classes will become to use a
direct dictionary creation.

Adding support for Python 3.7 is of course also a huge step. And also
this happened fairly quickly and soon after its release. The generic
classes it adds were the only real major new feature. It breaking the
internals for exception handling was what was holding back initially,
but past that, it was really easy.

Expect more optimization to come in the next releases, aiming at both
the ability to predict Python3 metaclasses ``__prepare__`` results, and
at more optimization applied to variables after they became temporary
variables.
