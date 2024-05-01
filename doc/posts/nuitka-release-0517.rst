.. post:: 2015/12/28 21:56
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.5.17
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release is a major feature release, as it adds full support for
Python3.5 and its coroutines. In addition, in order to properly support
coroutines, the generator implementation got enhanced. On top of that,
there is the usual range of corrections.

***********
 Bug Fixes
***********

-  Windows: Command line arguments that are unicode strings were not
   properly working.

-  Compatibility: Fix, only the code object attached to exceptions
   contained all variable names, but not the one of the function object.

-  Python3: Support for virtualenv on Windows was using non-portable
   code and therefore failing.

-  The tree displayed with ``--display-tree`` duplicated all functions
   and did not resolve source lines for functions. It also displayed
   unused functions, which is not helpful.

-  Generators with parameters leaked C level memory for each instance of
   them leading to memory bloat for long running programs that use a lot
   of generators. Fixed in 0.5.16.1 already.

-  Don't drop positional arguments when called with ``--run``, also make
   it an error if they are present without that option.

**************
 New Features
**************

-  Added full support for Python3.5, coroutines work now too.

**************
 Optimization
**************

-  Optimized frame access of generators to not use both a local frame
   variable and the frame object stored in the generator object itself.
   This gave about 1% speed up to setting them up.

-  Avoid having multiple code objects for functions that can raise and
   have local variables. Previously one code object would be used to
   create the function (with parameter variable names only) and when
   raising an exception, another one would be used (with all local
   variable names). Creating them both at start-up was wasteful and also
   needed two tuples to be created, thus more constants setup code.

-  The entry point for generators is now shared code instead of being
   generated for each one over and over. This should make things more
   cache local and also results in less generated C code.

-  When creating frame codes, avoid working with strings, but use proper
   emission for less memory churn during code generation.

****************
 Organizational
****************

-  Updated the key for the Debian/Ubuntu repositories to remain valid
   for 2 more years.

-  Added support for Fedora 23.

-  MinGW32 is no more supported, use MinGW64 in the 32 bits variant,
   which has less issues.

**********
 Cleanups
**********

-  Detecting function type ahead of times, allows to handle generators
   different from normal functions immediately.

-  Massive removal of code duplication between normal functions and
   generator functions. The later are now normal functions creating
   generator objects, which makes them much more lightweight.

-  The ``return`` statement in generators is now immediately set to the
   proper node as opposed to doing this in variable closure phase only.
   We can now use the ahead knowledge of the function type.

-  The ``nonlocal`` statement is now immediately checked for syntax
   errors as opposed to doing that only in variable closure phase.

-  The name of contraction making functions is no longer skewed to
   empty, but the real thing instead. The code name is solved
   differently now.

-  The ``local_locals`` mode for function node was removed, it was
   always true ever since Python2 list contractions stop using pseudo
   functions.

-  The outline nodes allowed to provide a body when creating them,
   although creating that body required using the outline node already
   to create temporary variables. Removed that argument.

-  Removed PyLint false positive annotations no more needed for PyLint
   1.5 and solved some TODOs.

-  Code objects are now mostly created from specs (not yet complete)
   which are attached and shared between statement frames and function
   creations nodes, in order to have less guess work to do.

*******
 Tests
*******

-  Added the CPython3.5 test suite.

-  Updated generated doctests to fix typos and use common code in all
   CPython test suites.

*********
 Summary
*********

This release continues to address technical debt. Adding support for
Python3.5 was the major driving force, while at the same time removing
obstacles to the changes that were needed for coroutine support.

With Python3.5 sorted out, it will be time to focus on general
optimization again, but there is more technical debt related to classes,
so the cleanup has to continue.
