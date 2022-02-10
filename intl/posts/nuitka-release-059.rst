.. post:: 2015/01/30 07:37
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.5.9
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release is mostly a maintenance release, bringing out minor
compatibility improvements, and some standalone improvements. Also new
options to control the recursion into modules are added.

***********
 Bug Fixes
***********

-  Compatibility: Checks for iterators were using ``PyIter_Check`` which
   is buggy when running outside of Python core, because it's comparing
   pointers we don't see. Replaced with ``HAS_ITERNEXT`` helper which
   compares against the pointer as extracting for a real non-iterator
   object.

   .. code:: python

      class Iterable:
          def __init__(self):
              self.consumed = 2

          def __iter__(self):
              return Iterable()


      iter(Iterable())  # This is suppose to raise, but didn't with Nuitka

-  Python3: Errors when creating class dictionaries raised by the
   ``__prepare__`` dictionary (e.g. ``enum`` classes with wrong
   identifiers) were not immediately raised, but only by the ``type``
   call.

   This was not observable, but might have caused issues potentially.

-  Standalone macOS: Shared libraries and extension modules didn't have
   their DLL load paths updated, but only the main binary. This is not
   sufficient for more complex programs.

-  Standalone Linux: Shared libraries copied into the ``.dist`` folder
   were read-only and executing ``chrpath`` could potentially then fail.
   This has not been observed, but is a conclusion of macOS fix.

-  Standalone: When freezing standard library, the path of Nuitka and
   the current directory remained in the search path, which could lead
   to looking at the wrong files.

****************
 Organisational
****************

-  The ``getattr`` built-in is now optimized for compile time constants
   if possible, even in the presence of a ``default`` argument. This is
   more a cleanup than actually useful yet.

-  The calling of ``PyCFunction`` from normal Python extension modules
   got accelerated, especially for the no or single argument cases where
   Nuitka now avoids building the tuple.

**************
 New Features
**************

-  Added the option ``--recurse-pattern`` to include modules per
   filename, which for Python3 is the only way to not have them in a
   package automatically.

-  Added the option ``--generate-c++-only`` to only generate the C++
   source code without starting the compiler.

   Mostly used for debugging and testing coverage. In the later case we
   do not want the C++ compiler to create any binary, but only to
   measure what would have been used.

****************
 Organisational
****************

-  Renamed the debug option ``--c++-only`` to ``--recompile-c++-only``
   to make its purpose more clear and there now is
   ``--generate-c++-only`` too.

*******
 Tests
*******

-  Added support for taking coverage of Nuitka in a test run on a given
   input file.

-  Added support for taking coverage for all Nuitka test runners,
   migrating them all to common code for searching.

-  Added uniform way of reporting skipped tests, not generally used yet.

*********
 Summary
*********

This release marks progress towards having coverage testing. Recent
releases had made it clear that not all code of Nuitka is actually used
at least once in our release tests. We aim at identifying these.

Another direction was to catch cases, where Nuitka leaks exceptions or
is subject to leaked exceptions, which revealed previously unnoticed
errors.

Important changes have been delayed, e.g. the closure variables will not
yet use C++ objects to share storage, but proper ``PyCellObject`` for
improved compatibility, and to approach a more "C-ish" status. These is
unfinished code that does this. And the forward propagation of values is
not enabled yet again either.

So this is an interim step to get the bug fixes and improvements
accumulated out. Expect more actual changes in the next releases.
