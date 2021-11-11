This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This is to inform you about the new release of Nuitka with some real
news and a slight performance increase. The significant news is added
"Windows Support". You can now hope to run Nuitka on Windows too and
have it produce working executables against either the standard Python
distribution or a MinGW compiled Python.

There are still some small things to iron out, and clearly documentation
needs to be created, and esp. the DLL hell problem of ``msvcr90.dll``
vs. ``msvcrt.dll``, is not yet fully resolved, but appears to be not as
harmful, at least not on native Windows.

I am thanking Khalid Abu Bakr for making this possible. I was surprised
to see this happen. I clearly didn't make it easy. He found a good way
around ``ucontext``, identifier clashes, and a very tricky symbol
problems where the CPython library under Windows exports less than under
Linux. Thanks a whole lot.

Currently the Windows support is considered experimental and works with
MinGW 4.5 or higher only.

Otherwise there have been the usual round of performance improvements
and more cleanups. This release is otherwise milestone 2 work only,
which will have to continue for some time more.

***********
 Bug fixes
***********

-  Lambda generators were not fully compatible, their simple form could
   yield an extra value. The behavior for Python 2.6 and 2.7 is also
   different and Nuitka now mimics both correctly, depending on the used
   Python version

-  The given parameter count cited in the error message in case of too
   many parameters, didn't include the given keyword parameters in the
   error message.

-  There was an ``assert False`` right after warning about not found
   modules in the ``--deep`` mode, which was of course unnecessary.

**************
 Optimization
**************

-  When unpacking variables in assignments, the temporary variables are
   now held in a new temporary class that is designed for the task
   specifically.

   This avoids the taking of a reference just because the
   ``PyObjectTemporary`` destructor insisted on releasing one. The new
   class ``PyObjectTempHolder`` hands the existing reference over and
   releases only in case of exceptions.

-  When unpacking variable in for loops, the value from the iterator may
   be directly assigned, if it's to a variable.

   In general this would be possible for every assignment target that
   cannot raise, but the infrastructure cannot tell yet, which these
   would be. This will improve with more milestone 3 work.

-  Branches with only ``pass`` inside are removed, ``pass`` statements
   are removed before the code generation stage. This makes it easier to
   achieve and decide empty branches.

-  There is now a global variable class per module. It appears that it
   is indeed faster to roll out a class per module accessing the
   ``module *`` rather than having one class and use a ``module **``,
   which is quite disappointing from the C++ compiler.

-  Also ``MAKE_LIST`` and ``MAKE_TUPLE`` have gained special cases for
   the 0 arguments case. Even when the size of the variadic template
   parameters should be known to the compiler, it seems, it wasn't
   eliminating the branch, so this was a speedup measured with valgrind.

-  Empty tried branches are now replaced when possible with
   ``try``/``except`` statements, ``try``/``finally`` is simplified in
   this case. This gives a cleaner tree structure and less verbose C++
   code which the compiler threw away, but was strange to have in the
   first place.

-  In conditions the ``or`` and ``and`` were evaluated with Python
   objects instead of with C++ bool, which was unnecessary overhead.

-  List contractions got more clever in how they assign from the
   iterator value.

   It now uses a ``PyObjectTemporary`` if it's assigned to multiple
   values, a ``PyObjectTempHolder`` if it's only assigned once, to
   something that could raise, or a ``PyObject *`` if an exception
   cannot be raised. This avoids temporary references completely for the
   common case.

**********
 Cleanups
**********

-  The ``if``, ``for``, and ``while`` statements had always empty
   ``else`` nodes which were then also in the generated C++ code as
   empty branches. No harm to performance, but this got cleaned up.

-  Some more generated code white space fixes.

***********
 New Tests
***********

-  The CPython 2.7 test suite now also has the ``doctests`` extracted to
   static tests, which improves test coverage for Nuitka again.

   This was previously only done for CPython 2.6 test suite, but the
   test suites are different enough to make this useful, e.g. to
   discover newly changed behavior like with the lambda generators.

-  Added Shed Skin 0.7.1 examples as benchmarks, so we can start to
   compare Nuitka performance in these tests. These will be the focus of
   numbers for the 0.4.x release series.

-  Added a micro benchmark to check unpacking behavior. Some of these
   are needed to prove that a change is an actual improvement, when its
   effect can go under in noise of in-line vs. no in-line behavior of
   the C++ compiler.

-  Added "pybench" benchmark which reveals that Nuitka is for some
   things much faster, but there are still fields to work on. This
   version needed changes to stand the speed of Nuitka. These will be
   subject of a later posting.

****************
 Organisational
****************

-  There is now a "tests/benchmarks/micro" directory to contain tiny
   benchmarks that just look at a single aspect, but have no other
   meaning, e.g. the "PyStone" extracts fall into this category.

-  There is now a ``--windows-target`` option that attempts a
   cross-platform build on Linux to Windows executable. This is using
   "MingGW-cross-env" cross compilation tool chain. It's not yet working
   fully correctly due to the DLL hell problem with the C runtime. I
   hope to get this right in subsequent releases.

-  The ``--execute`` option uses wine to execute the binary if it's a
   cross-compile for windows.

-  Native windows build is recognized and handled with MinGW 4.5, the
   VC++ is not supported yet due to missing C++0x support.

-  The basic test suite ran with Windows so far only and some
   adaptations were necessary. Windows new lines are now ignored in
   difference check, and addresses under Windows are upper case, small
   things.

*********
 Numbers
*********

python 2.6:

.. code::

   Pystone(1.1) time for 50000 passes = 0.65
   This machine benchmarks at 76923.1 pystones/second

Nuitka 0.3.8 (driven by python 2.6):

.. code::

   Pystone(1.1) time for 50000 passes = 0.27
   This machine benchmarks at 185185 pystones/second

This is a 140% speed increase of 0.3.8 compared to CPython, up from 132%
compared to the previous release.
