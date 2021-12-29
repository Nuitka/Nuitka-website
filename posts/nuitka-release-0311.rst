.. post:: 2011/09/17 02:41
   :tags: compiler, git, Nuitka, Python
   :author: Kay Hayen

#######################
 Nuitka Release 0.3.11
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This is to inform you about the new release of Nuitka with some bug
fixes and portability work.

This release is generally cleaning up things, and makes Nuitka portable
to ARM Linux. I used to host the Nuitka homepage on that machine, but
now that it's no longer so, I can run heavy compile jobs on it. To my
surprise, it found many portability problems. So I chose to fix that
first, the result being that Nuitka now works on ARM Linux too.

***********
 Bug fixes
***********

-  The order of slice expressions was not correct on x86 as well, and I
   found that with new tests only. So the porting to ARM revealed a bug
   category, I previously didn't consider.

-  The use of ``linux2`` in the Scons file is potentially incompatible
   with Linux 3.0, although it seems that at least on Debian the
   ``sys.platform`` was changed back to ``linux2``. Anyway, it's
   probably best to allow just anything that starts with ``linux`` these
   days.

-  The ``print`` statement worked like a ``print`` function, i.e. it
   first evaluated all printed expressions, and did the output only
   then. That is incompatible in case of exceptions, where partial
   outputs need to be done, and so that got fixed.

**************
 Optimization
**************

-  Function calls now each have a dedicated helper function, avoiding in
   some cases unnecessary work. We will may build further on this and
   in-line ``PyObject_Call`` differently for the special cases.

**********
 Cleanups
**********

-  Moved many C++ helper declarations and in-line implementations to
   dedicated header files for better organisation.

-  Some dependencies were removed and consolidated to make the
   dependency graph sane.

-  Multiple decorators were in reverse order in the node tree. The code
   generation reversed it back, so no bug, yet that was a distorted
   tree.

   Finding this came from the ARM work, because the "reversal" was in
   fact just the argument evaluation order of C++ under x86/x64, but on
   ARM that broke. Correcting it highlighted this issue.

-  The deletion of slices, was not using ``Py_ssize`` for indexes,
   disallowing some kinds of optimization, so that was harmonized.

-  The function call code generation got a general overhaul. It is now
   more consistent, has more helpers available, and creates more
   readable code.

-  PyLint is again happier than ever.

***********
 New Tests
***********

-  There is a new basic test ``OrderChecks`` that covers the order of
   expression evaluation. These problems were otherwise very hard to
   detect, and in some cases not previously covered at all.

-  Executing Nuitka with Python3 (it won't produce correct Python3 C/API
   code) is now part of the release tests, so non-portable code of
   Nuitka gets caught.

****************
 Organisational
****************

-  Support for ARM Linux. I will make a separate posting on the
   challenges of this. Suffice to say now, that C++ leaves way too much
   things unspecified.

-  The Nuitka git repository now uses "git flow". The new git policy
   will be detailed in another `separate posting
   <https://nuitka.net/posts/nuitka-git-flow.html>`__.

-  There is an unstable ``develop`` branch in which the development
   occurs. For this release ca. 40 commits were done to this branch,
   before merging it. I am also doing more fine grained commits now.

-  Unlike previously, there is ``master`` branch for the stable release.

-  There is a script "make-dependency-graph.sh" (Update: meanwhile it
   was renamed to "make-dependency-graph.py") to produce a dependency
   graphs of Nuitka. I detected a couple of strange things through this.

-  The Python3 ``__pycache__`` directories get removed too by the
   cleanup script.

*********
 Numbers
*********

We only have "PyStone" now, and on a new machine, so the numbers cannot
be compared to previous releases:

python 2.6:

.. code::

   Pystone(1.1) time for 50000 passes = 0.48
   This machine benchmarks at 104167 pystones/second

Nuitka 0.3.11 (driven by python 2.6):

.. code::

   Pystone(1.1) time for 50000 passes = 0.19
   This machine benchmarks at 263158 pystones/second

So this a speedup factor of 258%, last time on another machine it was
240%. Yet it only proves that the generated and compiled are more
efficient than bytecode, but Nuitka doesn't yet do the relevant
optimization. Only once it does, the factor will be significantly
higher.

*********
 Summary
*********

Overall, there is quite some progress. Nuitka is a lot cleaner now,
which will help us later only. I wanted to get this out, mostly because
of the bug fixes, and of course just in case somebody attempts to use it
on ARM.
