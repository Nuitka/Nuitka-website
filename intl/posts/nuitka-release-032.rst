.. post:: 2010/10/10 21:10
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.3.2
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release of Nuitka continues the focus on performance. But this
release also revisits the topic of feature parity. Before, feature
parity had been reached "only" with Python 2.6. This is of course a big
thing, but you know there is always more, e.g. Python 2.7.

With the addition of set contractions and dict contractions in this very
release, Nuitka is approaching Python support for 2.7, and then there
are some bug fixes.

***********
 Bug fixes
***********

-  Calling a function with ``**`` and using a non-dict for it was
   leading to wrong behavior.

   Now a mapping is good enough as input for the ``**`` parameter and
   it's checked.

-  Deeply nested packages "package.subpackage.module" were not found and
   gave a warning from Nuitka, with the consequence that they were not
   embedded in the executable. They now are.

-  Some error messages for wrong parameters didn't match literally. For
   example "function got multiple..." as opposed to "function() got
   multiple..." and alike.

-  Files that ended in line with a "#" but without a new line gave an
   error from "ast.parse". As a workaround, a new line is added to the
   end of the file if it's "missing".

-  More correct exception locations for complex code lines. I noted that
   the current line indication should not only be restored when the call
   at hand failed, but in any case. Otherwise sometimes the exception
   stack would not be correct. It now is - more often. Right now, this
   has no systematic test.

-  Re-raised exceptions didn't appear on the stack if caught inside the
   same function, these are now correct.

-  For ``exec`` the globals argument needs to have "__builtins__" added,
   but the check was performed with the mapping interface.

   That is not how CPython does it, and so e.g. the mapping could use a
   default value for "__builtins__" which could lead to incorrect
   behavior. Clearly a corner case, but one that works fully compatible
   now.

**************
 Optimization
**************

-  The local and shared local variable C++ classes have a flag
   "free_value" to indicate if an "PY_DECREF" needs to be done when
   releasing the object. But still the code used "Py_XDECREF" (which
   allows for "NULL" values to be ignored.) when the releasing of the
   object was done. Now the inconsistency of using "NULL" as "object"
   value with "free_value" set to true was removed.

-  Tuple constants were copied before using them without a point. They
   are immutable anyway.

**********
 Cleanups
**********

-  Improved more of the indentation of the generated C++ which was not
   very good for contractions so far. Now it is. Also assignments should
   be better now.

-  The generation of code for contractions was made more general and
   templates split into multiple parts. This enabled reuse of the code
   for list contractions in dictionary and set contractions.

-  The with statement has its own template now and got cleaned up
   regarding indentation.

***********
 New Tests
***********

-  There is now a script to extract the "doctests" from the CPython test
   suite and it generates Python source code from them. This can be
   compiled with Nuitka and output compared to CPython. Without this,
   the doctest parts of the CPython test suite is mostly useless.
   Solving this improved test coverage, leading to many small fixes. I
   will dedicate a later posting to the tool, maybe it is useful in
   other contexts as well.

-  Reference count tests have been expanded to cover assignment to
   multiple assignment targets, and to attributes.

-  The deep program test case, now also have a module in a sub-package
   to cover this case as well.

****************
 Organisational
****************

-  The `gitweb interface <https://nuitka.net/gitweb>`__ (since disabled)
   might be considered an alternative to downloading the source if you
   want to provide a pointer, or want to take a quick glance at the
   source code. You can already download with git, follow the link below
   to the page explaining it.

-  The "README.txt" has documented more of the differences and I
   consequently updated the Differences page. There is now a distinction
   between generally missing functionality and things that don't work in
   ``--deep`` mode, where Nuitka is supposed to create one executable.

   I will make it a priority to remove the (minor) issues of ``--deep``
   mode in the next release, as this is only relatively little work, and
   not a good difference to have. We want these to be empty, right? But
   for the time being, I document the known differences there.

*********
 Numbers
*********

python 2.6:

.. code::

   Pystone(1.1) time for 50000 passes = 0.65
   This machine benchmarks at 76923.1 pystones/second

Nuitka 0.3.2:

.. code::

   Pystone(1.1) time for 50000 passes = 0.39
   This machine benchmarks at 128205 pystones/second

This is 66% for 0.3.2, slightly up from the 58% of 0.3.1 before. The
optimization done were somewhat fruitful, but as you can see, they were
also more cleanups, not the big things.
