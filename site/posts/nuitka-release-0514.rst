.. post:: 2015/08/28 07:03
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.5.14
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release is an intermediate step towards value propagation, which is
not considered ready for stable release yet. The major point is the
elimination of the ``try``/``finally`` expressions, as they are problems
to SSA. The ``try``/``finally`` statement change is delayed.

There are also a lot of bug fixes, and enhancements to code generation,
as well as major cleanups of code base.

***********
 Bug Fixes
***********

-  Python3: Added support assignments trailing star assignment.

   .. code:: python

      *a, b = 1, 2

   This raised ``ValueError`` before.

-  Python3: Properly detect illegal double star assignments.

   .. code:: python

      *a, *b = c

-  Python3: Properly detect the syntax error to star assign from
   non-tuple/list.

   .. code:: python

      *a = 1

-  Python3.4: Fixed a crash of the binary when copying dictionaries with
   split tables received as star arguments.

-  Python3: Fixed reference loss, when using ``raise a from b`` where
   ``b`` was an exception instance. Fixed in 0.5.13.8 already.

-  Windows: Fix, the flag ``--disable-windows-console`` was not properly
   handled for MinGW32 run time resulting in a crash.

-  Python2.7.10: Was not recognizing this as a 2.7.x variant and
   therefore not applying minor version compatibility levels properly.

-  Fix, when choosing to have frozen source references, code objects
   were not use the same value as ``__file__`` did for its filename.

-  Fix, when re-executing itself to drop the ``site`` module, make sure
   we find the same file again, and not according to the ``PYTHONPATH``
   changes coming from it. Fixed in 0.5.13.4 already.

-  Enhanced code generation for ``del variable`` statements, where it's
   clear that the value must be assigned.

-  When pressing CTRL-C, the stack traces from both Nuitka and Scons
   were given, we now avoid the one from Scons.

-  Fix, the dump from ``--xml`` no longer contains functions that have
   become unused during analysis.

-  Standalone: Creating or running programs from inside unicode paths
   was not working on Windows. Fixed in 0.5.13.7 already.

-  Namespace package support was not yet complete, importing the parent
   of a package was still failing. Fixed in 0.5.13.7 already.

-  Python2.6: Compatibility for exception check messages enhanced with
   newest minor releases.

-  Compatibility: The ``NameError`` in classes needs to say ``global
   name`` and not just ``name`` too.

-  Python3: Fixed creation of XML representation, now done without
   ``lxml`` as it doesn't support needed features on that version. Fixed
   in 0.5.13.5 already.

-  Python2: Fix, when creating code for the largest negative constant to
   still fit into ``int``, that was only working in the main module.
   Fixed in 0.5.13.5 already.

-  Compatibility: The ``print`` statement raised an assertion on unicode
   objects that could not be encoded with ``ascii`` codec.

**************
 New Features
**************

-  Added support for Windows 10.

-  Followed changes for Python 3.5 beta 2. Still only usable as a Python
   3.4 replacement, no new features.

-  Using a self compiled Python running from the source tree is now
   supported.

-  Added support for Anaconda Python distribution. As it doesn't install
   the Python DLL, we copy it along for acceleration mode.

-  Added support for Visual Studio 2015. Fixed in 0.5.13.3 already.

-  Added support for self compiled Python versions running from build
   tree, this is intended to help debug things on Windows.

**************
 Optimization
**************

-  Function in-lining is now present in the code, but still disabled,
   because it needs more changes in other areas, before we can generally
   do it.

-  Trivial outlines, result of re-formulations or function in-lining,
   are now in-lined, in case they just return an expression.

-  The re-formulation for ``or`` and ``and`` has been giving up,
   eliminating the use of a ``try``/``finally`` expression, at the cost
   of dedicated boolean nodes and code generation for these.

   This saves around 8% of compile time memory for Nuitka, and allows
   for faster and more complete optimization, and gets rid of a
   complicated structure for analysis.

-  When a frame is used in an exception, its locals are detached. This
   was done more often than necessary and even for frames that are not
   necessary our own ones. This will speed up some exception cases.

-  When the default arguments, or the keyword default arguments
   (Python3) or the annotations (Python3) were raising an exception, the
   function definition is now replaced with the exception, saving a code
   generation. This happens frequently with Python2/Python3 compatible
   code guarded by version checks.

-  The SSA analysis for loops now properly traces "break" statement
   situations and merges the post-loop situation from all of them. This
   significantly allows for and improves optimization of code following
   the loop.

-  The SSA analysis of ``try``/``finally`` statements has been greatly
   enhanced. The handler for ``finally`` is now optimized for exception
   raise and no exception raise individually, as well as for ``break``,
   ``continue`` and ``return`` in the tried code. The SSA analysis for
   after the statement is now the result of merging these different
   cases, should they not abort.

-  The code generation for ``del`` statements is now taking advantage
   should there be definite knowledge of previous value. This speed them
   up slightly.

-  The SSA analysis of ``del`` statements now properly decided if the
   statement can raise or not, allowing for more optimization.

-  For list contractions, the re-formulation was enhanced using the new
   outline construct instead of a pseudo function, leading to better
   analysis and code generation.

-  Comparison chains are now re-formulated into outlines too, allowing
   for better analysis of them.

-  Exceptions raised in function creations, e.g. in default values, are
   now propagated, eliminating the function's code. This happens most
   often with Python2/Python3 in branches. On the other hand, function
   creations that cannot are also annotated now.

-  Closure variables that become unreferenced outside of the function
   become normal variables leading to better tracing and code generation
   for them.

-  Function creations cannot raise except their defaults, keyword
   defaults or annotations do.

-  Built-in references can now be converted to strings at compile time,
   e.g. when printed.

****************
 Organizational
****************

-  Removed gitorious mirror of the git repository, they shut down.

-  Make it more clear in the documentation that Python2 is needed at
   compile time to create Python3 executables.

**********
 Cleanups
**********

-  Moved more parts of code generation to their own modules, and used
   registry for code generation for more expression kinds.

-  Unified ``try``/``except`` and ``try``/``finally`` into a single
   construct that handles both through
   ``try``/``except``/``break``/``continue``/``return`` semantics.
   Finally is now solved via duplicating the handler into cases
   necessary.

   No longer are nodes annotated with information if they need to
   publish the exception or not, this is now all done with the dedicated
   nodes.

-  The ``try``/``finally`` expressions have been replaced with outline
   function bodies, that instead of side effect statements, are more
   like functions with return values, allowing for easier analysis and
   dedicated code generation of much lower complexity.

-  No more "tolerant" flag for release nodes, we now decide this fully
   based on SSA information.

-  Added helper for assertions that code flow does not reach certain
   positions, e.g. a function must return or raise, aborting statements
   do not continue and so on.

-  To keep cloning of code parts as simple as possible, the limited use
   of ``makeCloneAt`` has been changed to a new ``makeClone`` which
   produces identical copies, which is what we always do. And a generic
   cloning based on "details" has been added, requiring to make
   constructor arguments and details complete and consistent.

-  The re-formulation code helpers have been improved to be more
   convenient at creating nodes.

-  The old ``nuitka.codegen`` module ``Generator`` was still used for
   many things. These now all got moved to appropriate code generation
   modules, and their users got updated, also moving some code generator
   functions in the process.

-  The module ``nuitka.codegen.CodeTemplates`` got replaces with direct
   uses of the proper topic module from ``nuitka.codegen.templates``,
   with some more added, and their names harmonized to be more easily
   recognizable.

-  Added more assertions to the generated code, to aid bug finding.

-  The auto-format now sorts pylint markups for increased consistency.

-  Releases no longer have a ``tolerant`` flag, this was not needed
   anymore as we use SSA.

-  Handle CTRL-C in scons code preventing per job messages that are not
   helpful and avoid tracebacks from scons, also remove more unused
   tools like ``rpm`` from out in-line copy.

*******
 Tests
*******

-  Added the CPython3.4 test suite.

-  The CPython3.2, CPython3.3, and CPython3.4 test suite now run with
   Python2 giving the same errors. Previously there were a few specific
   errors, some with line numbers, some with different ``SyntaxError``
   be raised, due to different order of checks.

   This increases the coverage of the exception raising tests somewhat.

-  Also the CPython3.x test suites now all pass with debug Python, as
   does the CPython 2.6 test suite with 2.6 now.

-  Added tests to cover all forms of unpacking assignments supported in
   Python3, to be sure there are no other errors unknown to us.

-  Started to document the reference count tests, and to make it more
   robust against SSA optimization. This will take some time and is work
   in progress.

-  Made the compile library test robust against modules that raise a
   syntax error, checking that Nuitka does the same.

-  Refined more tests to be directly executable with Python3, this is an
   ongoing effort.

*********
 Summary
*********

This release is clearly major. It represents a huge step forward for
Nuitka as it improves nearly every aspect of code generation and
analysis. Removing the ``try``/``finally`` expression nodes proved to be
necessary in order to even have the correct SSA in their cases. Very
important optimization was blocked by it.

Going forward, the ``try``/``finally`` statements will be removed and
dead variable elimination will happen, which then will give function
inlining. This is expected to happen in one of the next releases.

This release is a consolidation of 8 hotfix releases, and many
refactorings needed towards the next big step, which might also break
things, and for that reason is going to get its own release cycle.
