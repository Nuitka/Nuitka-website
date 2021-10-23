This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This is about the new release of Nuitka which some bug fixes and offers
a good speed improvement.

This new release is major milestone 2 work, enhancing practically all
areas of Nuitka. The main focus was on faster function calls, faster
class attributes (not instance), faster unpacking, and more built-ins
detected and more thoroughly optimizing them.

***********
 Bug fixes
***********

-  Exceptions raised inside with statements had references to the
   exception and traceback leaked.

-  On Windows the binaries ``sys.executable`` pointed to the binary
   itself instead of the Python interpreter. Changed, because some code
   uses ``sys.executable`` to know how to start Python scripts.

-  There is a bug (fixed in their repository) related to C++ raw strings
   and C++ "trigraphs" that affects Nuitka, added a workaround that
   makes Nuitka not emit "trigraphs" at all.

-  The check for mutable constants was erroneous for tuples, which could
   lead to assuming a tuple with only mutable elements to be not
   mutable, which is of course wrong.

******************
 New Optimization
******************

This time there are so many new optimization, it makes sense to group
them by the subject.

Exceptions
==========

-  The code to add a traceback is now our own, which made it possible to
   use frames that do not contain line numbers and a code object capable
   of lookups.

-  Raising exceptions or adding to tracebacks has been made way faster
   by reusing a cached frame objects for the task.

-  The class used for saving exceptions temporarily (e.g. used in
   ``try``/``finally`` code, or with statement) has been improved.

   It now doesn't make a copy of the exception with a C++ ``new`` call,
   but it simply stores the exception properties itself and creates the
   exception object only on demand, which is more efficient.

-  When catching exceptions, the addition of tracebacks is now done
   without exporting and re-importing the exception to Python, but
   directly on the exception objects traceback, this avoids a useless
   round trip.

Function Calls
==============

-  Uses of PyObject_Call provide ``NULL`` as the dictionary, instead of
   an empty dictionary, which is slightly faster for function calls.

-  There are now dedicated variants for complex function calls with
   ``*`` and ``**`` arguments in all forms.

   These can take advantage of easier cases. For example, a merge with
   star arguments is only needed if there actually were any of these.

-  The check for non-string values in the ``**`` arguments can now be
   completely short-cut for the case of a dictionary that has never had
   a string added. There is now code that detects this case and skips
   the check, eliminating it as a performance concern.

Parameter Parsing
=================

-  Reversed the order in which parameters are checked.

   Now the keyword dictionary is iterated first and only then the
   positional arguments after that is done. This iteration is not only
   much faster (avoiding repeated lookups for each possible parameter),
   it also can be more correct, in case the keyword argument is derived
   from a dictionary and its keys mutate it when being compared.

-  Comparing parameter names is now done with a fast path, in which the
   pointer values are compare first. This can avoid a call to the
   comparison at all, which has become very likely due to the interning
   of parameter name strings, see below.

-  Added a dedicated call to check for parameter equality with rich
   equality comparison, which doesn't raise an exception.

-  Unpacking of tuples is now using dedicated variants of the normal
   unpacking code instead of rolling out everything themselves.

Attribute Access
================

-  The class type (in executables, not yet for extension modules) is
   changed to a faster variant of our own making that doesn't consider
   the restricted mode a possibility. This avoids very expensive calls,
   and makes accessing class attributes in compiled code and in
   non-compiled code faster.

-  Access to attributes (but not of instances) got in-lined and
   therefore much faster. Due to other optimization, a specific step to
   intern the string used for attribute access is not necessary with
   Nuitka at all anymore. This made access to attributes about 50%
   faster which is big of course.

Constants
=========

-  The bug for mutable tuples also caused non-mutable tuples to be
   considered as mutable, which lead to less efficient code.

-  The constant creation with the g++ bug worked around, can now use raw
   strings to create string constants, without resorting to un-pickling
   them as a work around. This allows us to use
   ``PyString_FromStringAndSize`` to create strings again, which is
   obviously faster, and had not been done, because of the confusion
   caused by the g++ bug.

-  For string constants that are usable as attributes (i.e. match the
   identifier regular expression), these are now interned, directly
   after creation. With this, the check for identical value of pointers
   for parameters has a bigger chance to succeed, and this saves some
   memory too.

-  For empty containers (set, dict, list, tuple) the constants created
   are now are not unstreamed, but created with the dedicated API calls,
   saving a bit of code and being less ugly.

-  For mutable empty constant access (set, dict, list) the values are no
   longer made by copying the constant, but instead with the API
   functions to create new ones. This makes code like ``a = []`` a tiny
   bit faster.

-  For slice indices the code generation now takes advantage of creating
   a C++ ``Py_ssize_t`` from constant value if possible. Before it was
   converting the integer constant at run time, which was of course
   wasteful even if not (very) slow.

Iteration
=========

-  The creation of iterators got our own code. This avoids a function
   call and is otherwise only a small gain for anything but sequence
   iterators. These may be much faster to create now, as it avoids
   another call and repeated checks.

-  The next on iterator got our own code too, which has simpler code
   flow, because it avoids the double check in case of NULL returned.

-  The unpack check got similar code to the next iterator, it also has
   simpler code flow now and avoids double checks.

Built-ins
=========

-  Added support for the ``list``, ``tuple``, ``dict``, ``str``,
   ``float`` and ``bool`` built-ins along with optimizing their use with
   constant parameter.

-  Added support for the ``int`` and ``long`` built-ins, based on a new
   "call spec" object, that detects parameter errors at compile time and
   raises appropriate exceptions as required, plus it deals with keyword
   arguments just as well.

   So, to Nuitka it doesn't matter now it you write ``int(value) ``or
   ``int(x = value)`` anymore. The ``base`` parameter of these built-ins
   is also supported.

   The use of this call spec mechanism will the expanded, currently it
   is not applied to the built-ins that take only one parameter. This is
   a work in progress as is the whole built-ins business as not all the
   built-ins are covered yet.

Cleanups
========

-  In 0.3.8 per module global classes were introduced, but the
   ``IMPORT_MODULE`` kept using the old universal class, this got
   resolved and the old class is now fully gone.

-  Using ``assertObject`` in more cases, and in more places at all,
   catches errors earlier on.

-  Moved the addition to tracebacks into the ``_PythonException`` class,
   where it works directly on the contained traceback. This is cleaner
   as it no longer requires to export exceptions to Python, just to add
   a traceback entry.

-  Some ``PyLint`` cleanups were done, reducing the number of reports a
   bit, but there is still a lot to do.

-  Added a ``DefaultValueIdentifier`` class that encapsulates the access
   to default values in the parameter parsing more cleanly.

-  The module ``CodeTemplatesListContractions`` was renamed to
   ``CodeTemplatesContractions`` to reflect the fact that it deals with
   all kinds of contractions (also set and dict contractions), not just
   list contractions.

-  Moved the with related template to its own module
   ``CodeTemplatesWith``, so its easier to find.

-  The options handling for g++ based compilers was cleaned up, so that
   g++ 4.6 and MinGW are better supported now.

-  Documented more aspects of the Scons build file.

-  Some more generated code white space fixes.

-  Moved some helpers to dedicated files. There is now ``calling.hpp``
   for function calls, an ``importing.cpp`` for import related stuff.

-  Moved the manifest generation to the scons file, which now produces
   ready to use executables.

***********
 New Tests
***********

-  Added a improved version of "pybench" that can cope with the "0 ms"
   execution time that Nuitka has for some if its sub-tests.

-  Reference counting test for with statement was added.

-  Micro benchmarks to demonstrate try finally performance when an
   exception travels through it.

-  Micro benchmark for with statement that eats up exceptions raised
   inside the block.

-  Micro benchmarks for the read and write access to class attributes.

-  Enhanced ``Printing`` test to cover the trigraphs constant bug case.
   Output is required to make the error detectable.

-  Enhanced ``Constants`` test to cover repeated mutation of mutable
   tuple constants, this covers the bug mentioned.

****************
 Organisational
****************

-  Added a credits section to the "README.txt" where I give credit to
   the people who contributed to Nuitka, and the projects it is using. I
   will make it a separate posting to cite these.

-  Documented the requirements on the compiler more clearly, document
   the fact that we require scons and which version of Python (2.6 or
   2.7).

-  The is now a codespeed implementation up and running with historical
   data for up to Nuitka 0.3.8 runs of "PyStone" and with pybench. It
   will be updated for 0.3.9 once I have the infrastructure in place to
   do that automatically.

-  The cleanup script now also removes .so files.

-  The handling of options for g++ got improved, so it's the same for
   g++ and MinGW compilers, plus adequate errors messages are given, if
   the compiler version is too low.

-  There is now a ``--unstriped`` option that just keeps the debug
   information in the file, but doesn't keep the assertions.

   This will be helpful when looking at generated assembler code from
   Nuitka to not have the distortions that ``--debug`` causes (reduced
   optimization level, assertions, etc.) and instead a clear view.
