This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This new release of Nuitka has a focus on re-organizing the Nuitka
generated source code and a modest improvement on the performance side.

For a long time now, Nuitka has generated a single C++ file and asked
the C++ compiler to translate it to an executable or shared library for
CPython to load. This was done even when embedding many modules into one
(the "deep" compilation mode, option ``--deep``).

This was simple to do and in theory ought to allow the compiler to do
the most optimization. But for large programs, the resulting source code
could have exponential compile time behavior in the C++ compiler. At
least for the GNU g++ this was the case, others probably as well. This
is of course at the end a scalability issue of Nuitka, which now has
been addressed.

So the major advancement of this release is to make the ``--deep``
option useful. But also there have been a performance improvements,
which end up giving us another boost for the "PyStone" benchmark.

***********
 Bug fixes
***********

-  Imports of modules local to packages now work correctly, closing the
   small compatibility gap that was there.

-  Modules with a "-" in their name are allowed in CPython through
   dynamic imports. This lead to wrong C++ code created. (Thanks to Li
   Xuan Ji for reporting and submitting a patch to fix it.)

-  There were warnings about wrong format used for ``Ssize_t`` type of
   CPython. (Again, thanks to Li Xuan Ji for reporting and submitting
   the patch to fix it.)

-  When a wrong exception type is raised, the traceback should still be
   the one of the original one.

-  Set and dict contractions (Python 2.7 features) declared local
   variables for global variables used. This went unnoticed, because
   list contractions don't generate code for local variables at all, as
   they cannot have such.

-  Using the ``type()`` built-in to create a new class could attribute
   it to the wrong module, this is now corrected.

**************
 New Features
**************

-  Uses Scons to execute the actual C++ build, giving some immediate
   improvements.

-  Now caches build results and Scons will only rebuild as needed.

-  The direct use of ``__import__()`` with a constant module name as
   parameter is also followed in "deep" mode. With time, non-constants
   may still become predictable, right now it must be a real CPython
   constant string.

**************
 Optimization
**************

-  Added optimization for the built-ins ``ord()`` and ``chr()``, these
   require a module and built-in module lookup, then parameter parsing.
   Now these are really quick with Nuitka.

-  Added optimization for the ``type()`` built-in with one parameter. As
   above, using from builtin module can be very slow. Now it is
   instantaneous.

-  Added optimization for the ``type()`` built-in with three parameters.
   It's rarely used, but providing our own variant, allowed to fix the
   bug mentioned above.

**********
 Cleanups
**********

-  Using scons is a big cleanup for the way how C++ compiler related
   options are applied. It also makes it easier to re-build without
   Nuitka, e.g. if you were using Nuitka in your packages, you can
   easily build in the same way than Nuitka does.

-  Static helpers source code has been moved to ".hpp" and ".cpp" files,
   instead of being in ".py" files. This makes C++ compiler messages
   more readable and allows us to use C++ mode in Emacs etc., making it
   easier to write things.

-  Generated code for each module ends up in a separate file per module
   or package.

-  Constants etc. go to their own file (although not named sensible yet,
   likely going to change too)

-  Module variables are now created by the ``CPythonModule`` node only
   and are unique, this is to make optimization of these feasible. This
   is a pre-step to module variable optimization.

***********
 New Tests
***********

-  Added "ExtremeClosure" from my Python quiz, it was not covered by
   existing tests.

-  Added test case for program that imports a module with a dash in its
   name.

-  Added test case for main program that starts with a dash.

-  Extended the built-in tests to cover ``type()`` as well.

****************
 Organisational
****************

-  There is now a new environment variable ``NUITKA_SCONS`` which should
   point to the directory with the ``SingleExe.scons`` file for Nuitka.
   The scons file could be named better, because it is actually one and
   the same who builds extension modules and executables.

-  There is now a new environment variable ``NUITKA_CPP`` which should
   point to the directory with the C++ helper code of Nuitka.

-  The script "create-environment.sh" can now be sourced (if you are in
   the top level directory of Nuitka) or be used with eval. In either
   case it also reports what it does.

   .. admonition:: Update

      The script has become obsolete now, as the environment variables
      are no longer necessary.

-  To cleanup the many "Program.build" directories, there is now a
   "clean-up.sh" script for your use. Can be handy, but if you use git,
   you may prefer its clean command.

   .. admonition:: Update

      The script has become obsolete now, as Nuitka test executions now
      by default delete the build results.

*********
 Numbers
*********

python 2.6::

   Pystone(1.1) time for 50000 passes = 0.65
   This machine benchmarks at 76923.1 pystones/second

Nuitka 0.3.4::

   Pystone(1.1) time for 50000 passes = 0.34
   This machine benchmarks at 147059 pystones/second

This is 91% for 0.3.4, up from 80% before.
