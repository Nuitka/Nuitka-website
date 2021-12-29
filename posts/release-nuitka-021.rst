.. post:: 2010/09/05 14:00
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.2.1
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

The march goes on, this is another minor release with a bunch of
substantial improvements:

***********
 Bug Fixes
***********

-  Packages now also can be embedded with the ``--deep`` option too,
   before they could not be imported from the executable.

-  In-lined exec with their own future statements leaked these to the
   surrounding code.

*********************
 Reduced Differences
*********************

-  The future print function import is now supported too.

**********
 Cleanups
**********

-  Independence of the compiled function type. When I started it was
   merely ``PyCFunction`` and then a copy of it patched at run time,
   using increasingly less code from CPython. Now it's nothing at all
   anymore.

-  This lead to major cleanup of run time compiled function creation
   code, no more ``methoddefs``, ``PyCObject`` holding context, etc.

-  PyLint was used to find the more important style issues and potential
   bugs, also helping to identify some dead code.

*********
 Summary
*********

The major difference now is the lack of a throw method for generator
functions. I will try to address that in a 0.2.2 release if possible.
The plan is that the 0.2.x series will complete these tasks, and 0.3
could aim at some basic optimization finally.
