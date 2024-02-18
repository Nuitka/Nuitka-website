.. post:: 2012/11/11 16:29
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.3.25
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release brings about changes on all fronts, bug fixes, new
features. Also very importantly Nuitka no longer uses C++11 for its
code, but mere C++03. There is new re-formulation work, and re-factoring
of functions.

But the most important part is this: Mercurial unit tests are working.
Nearly. With the usual disclaimer of me being wrong, all remaining
errors are errors of the test, or minor things. Hope is that these unit
tests can be added as release tests to Nuitka. And once that is done,
the next big Python application can come.

***********
 Bug Fixes
***********

-  Local variables were released when an exception was raised that
   escaped the local function. They should only be released, after
   another exception was raised somewhere.

-  Identifiers of nested tuples and lists could collide.

   .. code:: python

      a = ((1, 2), 3)
      b = ((1,), 2, 3)

   Both tuples had the same name previously, not the end of the tuple is
   marked too. Fixed in 0.3.24.1 already.

-  The ``__name__`` when used read-only in modules in packages was
   optimized to a string value that didn't contain the package name.

-  Exceptions set when entering compiled functions were unset at
   function exit.

**************
 New Features
**************

-  Compiled frames support. Before, Nuitka was creating frames with the
   standard CPython C/API functions, and tried its best to cache them.
   This involved some difficulties, but as it turns out, it is actually
   possible to instead provide a compatible type of our own, that we
   have full control over.

   This will become the base of enhanced compatibility. Keeping
   references to local variables attached to exception tracebacks is
   something we may be able to solve now.

-  Enhanced Python3 support, added support for ``nonlocal`` declarations
   and many small corrections for it.

-  Writable ``__defaults__`` attribute for compiled functions, actually
   changes the default value used at call time. Not supported is
   changing the amount of default parameters.

**********
 Cleanups
**********

-  Keep the functions along with the module and added "FunctionRef" node
   kind to point to them.

-  Reformulated ``or`` and ``and`` operators with the conditional
   expression construct which makes the "short-circuit" branch.

-  Access ``self`` in methods from the compiled function object instead
   of pointer to context object, making it possible to access the
   function object.

-  Removed "OverflowCheck" module and its usage, avoids one useless scan
   per function to determine the need for "locals dictionary".

-  Make "compileTree" of "MainControl" module to only do what the name
   says and moved the rest out, making the top level control clearer.

-  Don't export module entry points when building executable and not
   modules. These exports cause MinGW and MSVC compilers to create
   export libraries.

**************
 Optimization
**************

-  More efficient code for conditional expressions in conditions:

   .. code:: python

      if a if b else c:
          ...

   See above, this code is now the typical pattern for each ``or`` and
   ``and``, so this was much needed now.

****************
 Organisational
****************

-  The remaining uses of C++11 have been removed. Code generated with
   Nuitka and complementary C++ code now compile with standard C++03
   compilers. This lowers the Nuitka requirements and enables at least
   g++ 4.4 to work with Nuitka.

-  The usages of the GNU extension operation ``a ?: b`` have replaced
   with standard C++ constructs. This is needed to support MSVC which
   doesn't have this.

-  Added examples for the typical use cases to the `User Manual
   <https://nuitka.net/doc/user-manual.html>`__.

-  The "compare_with_cpython" script has gained an option to immediately
   remove the Nuitka outputs (build directory and binary) if successful.
   Also the temporary files are now put under "/var/tmp" if available.

-  Debian package improvements, registering with ``doc-base`` the `User
   Manual <https://nuitka.net/doc/user-manual.html>`__ so it is easier
   to discover. Also suggest ``mingw32`` package which provides the
   cross compiler to Windows.

-  Partial support for MSVC (Visual Studio 2008 to be exact, the version
   that works with CPython2.6 and CPython2.7).

   All basic tests that do not use generators are working now, but those
   will currently cause crashes.

-  Renamed the ``--g++-only`` option to ``--c++-only``.

   The old name is no longer correct after clang and MSVC have gained
   support, and it could be misunderstood to influence compiler
   selection, rather than causing the C++ source code to not be updated,
   so manual changes will the used.

-  Catch exceptions for ``continue``, ``break``, and ``return`` only
   where needed for ``try``/``finally`` and loop constructs.

***********
 New Tests
***********

-  Added CPython3.2 test suite as "tests/CPython32" from 3.2.3 and run
   it with CPython2.7 to check that Nuitka gives compatible error
   messages. It is not expected to pass yet on Python3.2, but work will
   be done towards this goal.

-  Make CPython2.7 test suite runner also execute the generated
   "doctest" modules.

-  Enabled tests for default parameters and their reference counts.

*********
 Summary
*********

This release marks an important point. The compiled frames are exciting
new technology, that will allow even better integration with CPython,
while improving speed. Lowering the requirements to C++03 means, we will
become usable on Android and with MSVC, which will make adoption of
Nuitka on Windows easier for many.

Structurally the outstanding part is the function as references cleanup.
This was a blocker for value propagation, because now functions
references can be copied, whereas previously this was duplicating the
whole function body, which didn't work, and wasn't acceptable. Now, work
can resume in this domain.

Also very exciting when it comes to optimization is the remove of
special code for ``or`` and ``and`` operators, as these are now only
mere conditional expressions. Again, this will make value propagation
easier with two special cases less.

And then of course, with Mercurial unit tests running compiled with
Nuitka, an important milestone has been hit.

For a while now, the focus will be on completing Python3 support, XML
based optimization regression tests, benchmarks, and other open ends.
Once that is done, and more certainty about Mercurial tests support, I
may call it a 0.4 and start with local type inference for actual speed
gains.
