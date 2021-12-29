.. post:: 2012/01/26 20:49
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.3.19
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This time there are a few bug fixes, major cleanups, more Python3
support, and even new features. A lot things in this are justifying a
new release.

***********
 Bug fixes
***********

-  The man pages of ``nuitka`` and ``nuitka-python`` had no special
   layout for the option groups and broken whitespace for
   ``--recurse-to`` option. Also ``--g++-only`` was only partially bold.
   Released as 0.3.18.1 hot fix already.

-  The command line length improvement we made to Scons for Windows was
   not portable to Python2.6. Released as 0.3.18.2 hot fix already.

-  Code to detect already considered packages detection was not portable
   to Windows, for one case, there was still a use of ``/`` instead of
   using a ``joinpath`` call. Released as 0.3.18.3 already.

-  A call to the range built-in with no arguments would crash the
   compiler, see Released as 0.3.18.4 already.

-  Compatibility Fix: When rich comparison operators returned false
   value other ``False``, for comparison chains, these would not be
   used, but ``False`` instead, see .

-  The support for ``__import__`` didn't cover keyword arguments, these
   were simply ignored. Fixed, but no warning is given yet.

**************
 New Features
**************

-  A new option has been added, one can now specify
   ``--recurse-directory`` and Nuitka will attempt to embed these
   modules even if not obviously imported. This is not yet working
   perfect yet, but will receive future improvements.

-  Added support for the ``exec`` built-in of Python3, this enables us
   to run one more basic test, ``GlobalStatement.py`` with Python3. The
   test ``ExecEval.py`` nearly works now.

**************
 Optimization
**************

-  The no arguments ``range()`` call now optimized into the static
   CPython exception it raises.

-  Parts of comparison chains with constant arguments are now optimized
   away.

**********
 Cleanups
**********

-  Simplified the ``CPythonExpressionComparison`` node, it now always
   has only 2 operands.

   If there are more, the so called "comparison chain", it's done via
   ``and`` with assignments to temporary variables, which are expressed
   by a new node type ``CPythonExpressionTempVariableRef``. This allowed
   to remove ``expression_temps`` from C++ code templates and
   generation, reducing the overall complexity.

-  When executing a module (``--execute`` but not ``--exe``), no longer
   does Nuitka import it into itself, instead a new interpreter is
   launched with a fresh environment.

-  The calls to the variadic ``MAKE_TUPLE`` were replaced with calls the
   ``MAKE_TUPLExx`` (where ``xx`` is the number of arguments), that are
   generated on a as-needed basis. This gives more readable code,
   because no ``EVAL_ORDERED_xx`` is needed at call site anymore.

-  Many node classes have moved to new modules in ``nuitka.nodes`` and
   grouped by theme. That makes them more accessible.

-  The choosing of the debug python has moved from Scons to Nuitka
   itself. That way it can respect the ``sys.abiflags`` and works with
   Python3.

-  The replacing of ``.py`` in filenames was made more robust. No longer
   is ``str.replace`` used, but instead proper means to assure that
   having ``.py`` as other parts of the filenames won't be a trouble.

-  Module recursion was changed into its own module, instead of being
   hidden in the optimization that considers import statements.

-  As always, some PyLint work, and some minor ``TODO`` were solved.

****************
 Organisational
****************

-  Added more information to the `Developer Manual
   <https://nuitka.net/doc/developer-manual.html>`__, e.g. documenting
   the tree changes for ``assert`` to become a conditional statement
   with a raise statement, etc.

-  The Debian package is as of this version verified to be installable
   and functional on to Ubuntu Natty, Maverick, Oneiric, and Precise.

-  Added support to specify the binary under test with a ``NUITKA``
   environment, so the test framework can run with installed version of
   Nuitka too.

-  Made sure the test runners work under Windows as well. Required
   making them more portable. And a workaround for ``os.execl`` not
   propagating exit codes under Windows.

-  For windows target the MinGW library is now linked statically. That
   means there is no requirement for MinGW to be in the ``PATH`` or even
   installed to execute the binary.

***********
 New Tests
***********

-  The ``basic``, ``programs``, ``syntax``, and ``reflected`` were made
   executable under Windows. Occasionally this meant to make the test
   runners more portable, or to work around limitations.

-  Added test to cover return values of rich comparisons in comparison
   chains, and order of argument evaluation for comparison chains.

-  The ``Referencing.py`` test was made portable to Python3.

-  Cover no arguments ``range()`` exception as well.

-  Added test to demonstrate that ``--recurse-directory`` actually
   works. This is using an ``__import__`` that cannot be predicted at
   run time (yet).

-  The created source package is now tested on pbuilder chroots to be
   pass installation and the basic tests, in addition to the full tests
   during package build time on these chroots. This will make sure, that
   Nuitka works fine on Ubuntu Natty and doesn't break without notice.

*********
 Summary
*********

This releases contains many changes. The "temporary variable ref" and
"assignment expression" work is ground breaking. I foresee that it will
lead to even more simplifications of code generation in the future, when
e.g. in-place assignments can be reduced to assignments to temporary
variables and conditional statements.

While there were many improvements related to Windows support and fixing
portability bugs, or the Debian package, the real focus is the
optimization work, which will ultimately end with "value propagation"
working.

These are the real focus. The old comparison chain handling was a big
wart. Working, but no way understood by any form of analysis in Nuitka.
Now they have a structure which makes their code generation based on
semantics and allows for future optimization to see through them.

Going down this route is an important preparatory step. And there will
be more work like this needed. Consider e.g. handling of in-place
assignments. With an "assignment expression" to a "temporary variable
ref", these become the same as user code using such a variable. There
will be more of these to find.

So, that is where the focus is. The release now was mostly aiming at
getting involved fixes out. The bug fixed by comparison chain reworking,
and the ``__import__`` related one, were not suitable for hot fix
releases, so that is why the 0.3.19 release had to occur now. But with
plugin support, with this comparison chain cleanup, with improved
Python3 support, and so on, there was plenty of good stuff already, also
worth to get out.
