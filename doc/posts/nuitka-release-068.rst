.. post:: 2020/05/18 09:11
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.6.8
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This releases contains important general improvements and performance
improvements and enhanced optimization as well as many bug fixes that
enhance the Python 3.8 compatibility.

***********
 Bug Fixes
***********

-  Python3.5+: Fix, coroutines and asyncgen could continue iteration of
   awaited functions, even after their return, leading to wrong
   behaviour.

-  Python3.5+: Fix, absolute imports of names might also refer to
   modules and need to be handled for module loading as well.

-  Fix, the ``fromlist`` of imports could loose references, potentially
   leading to corruption of contained strings.

-  Python3.8: Fix, positional only arguments were not enforced to
   actually be that way.

-  Python3.8: Fix, complex calls with star arguments that yielded the
   same value twice, were not yet caught.

-  Python3.8: Fix, evaluation order for nested dictionary contractions
   was not followed yet.

-  Windows: Use short paths, these work much better to load extension
   modules and TCL parts of TkInter cannot handle unicode paths at all.
   This makes Nuitka work in locations, where normal Python cannot.

-  Windows: Fixup dependency walker in unicode input directories.

-  Standalone: Use frozen module loader only at ``libpython``
   initialisation and switch to built-in bytecode loader that is more
   compatible afterwards, increasing compatibility.

-  Standalone: Fix for ``pydantic`` support.

-  Standalone: Added missing hidden dependency of uvicorn.

-  Fix, the parser for ``.pyi`` files couldn't handle multiline imports.

-  Windows: Derive linker arch of Python from running binary, since it
   can happen that the Python binary is actually a script.

-  Fixup static linking with ``libpython.a`` that contains ``main.o`` by
   making our colliding symbols for ``Py_GetArgcArgv`` weak.

-  Python3.7: Fix misdetection as asyncgen for a normal generator, if
   the iterated value is async.

-  Distutils: Fix ``build_nuitka`` for modules under nested namespaces.

-  OpenBSD: Follow usage of clang and other corrections to make
   accelerated mode work.

-  macOS: Fixup for standalone mode library scan.

-  Fix, the logging of ``--show-modules`` was broken.

-  Windows: Enable ``/bigobj`` mode for MSVC for large compilations to
   work.

-  Windows: Fixup crash in warning with pefile dependency manager.

-  Windows: Fixup ``win32com`` standalone detection of other Python
   version ``win32com`` is in system ``PATH``.

-  Fix, the python flag for static hashes didn't have the intended
   effect.

-  Fix, generators may be resurrected in the cause of their destruction,
   and then must not be released.

-  Fix, method objects didn't implement the methods ``__reduce__`` and
   ``__reduce_ex__`` necessary for pickling them.

-  Windows: Fix, using a Python installation through a symlink was not
   working.

-  Windows: Fix, icon paths that were relative were not working anymore.

-  Python3.8: Detect duplicate keywords yielded from star arguments.

-  Fix, methods could not be pickled.

-  Fix, generators, coroutines and asyncgen might be resurrected during
   their release, allow for that.

-  Fix, frames need to traverse their attached locals to be released in
   some cases.

**************
 New Features
**************

-  Plugin command line handling now allows for proper ``optparse``
   options to be used, doing away with special parameter code for
   plugins. The arguments now also become automatically passed to the
   instantiations of plugins.

   Loading and creation of plugins are now two separate phases. They are
   loaded when they appear on the command line and can add options in
   their own group, even required ones, but also with default values.

-  Started using logging with name-spaces. Applying logging per plugin
   to make it easier to recognize which plugin said what. Warnings are
   now colored in red.

-  Python3.5+: Added support for two step module loading, making Nuitka
   loading even more compatible.

-  Enhanced import tracing to work on standalone binaries in a useful
   manner, allow to compare with normal binaries.

-  Fix, the ``setattr`` built-in was leaking a reference to the ``None``
   value.

**************
 Optimization
**************

-  Proper loop SSA capable of detecting shapes with an incremental
   initial phase and a final result of alternatives for variables
   written in the loop. This detects shapes of manual integer
   incrementing loops correctly now, it doesn't see through iterators
   yet, but this will come too.

-  Added type shapes for all operations and all important built-in types
   to allow more compile time optimization and better target type
   selection.

-  Target type code generation was expanded from manual usage with
   conditions to all operations allowing to get at bool target values
   more directly.

-  For in-place operations, there is the infrastructure to generate them
   for improved performance, but so far it's only used for Python2 int,
   and not for the many types normal operations are supported.

-  Force usage of C boolean type for all indicator variables from the
   re-formulation. In some cases, we are not yet there with detections,
   and this gives instant benefit.

-  Complex constants didn't annotate their type shape, preventing
   compile time optimization for them.

-  Python3.8: Also support vectorcall for compiled method objects. These
   are rarely used in new Python, but can make a difference.

-  Remove loops that have only a final break. This happens in static
   optimization in some cases, and allows more optimization to be done.

-  Avoid using a preparing a constant tuple value for calls with only
   constant arguments.

-  Avoid using ``PyErr_Format`` where it's not necessary by adding
   specialized helpers for common cases.

-  Detect ``del`` statements that will raise an exception and replace
   with that.

-  Exception matching is boolean shape, allowing for faster code
   generation.

-  Disable recursion checks outside of full compat mode.

-  Avoid large blocks for conditional statements that only need to
   enclose the condition evaluation.

-  Added shortcuts for interactions between compiled generator variants,
   to avoid calls to their C methods with argument passing, etc.

****************
 Organisational
****************

-  Updated Developer Manual with changes that happened, removing the
   obsolete language choice section.

-  Added 3.8 support mentions in even more places.

-  The mailing list has been deleted. We now prefer Gitter chat and
   GitHub issues for discussions.

-  Visual Code recommended extensions are now defined as such in the
   project configuration and you will be prompted to install them.

-  Visual Code environments for ``Py38`` and ``Py27`` were added for
   easier switch.

-  Catch usage of Python from the Microsoft App Store, it is not
   supported and seems to limit access to the Python installation for
   security reasons that make support impossible.

-  Make it clear that ``--full-compat`` should not be used in help
   output.

-  Added instructions for MSVC runtimes and standalone compilation to
   support Windows 7.

-  More complete listing of copyright holders for Debian.

-  Updated to newer black and PyLint.

-  Enhanced gcc version check, properly works with gcc 10 and higher.

*******
 Tests
*******

-  Pylint cleanups for some of the tests.

-  Added test for loading of user plugins.

-  Removed useless outputs for ``search`` mode skipping non-matches.

**********
 Cleanups
**********

-  Limit command line handling for multiprocessing module to when the
   plugin is actually used, avoiding useless code of Windows binaries.

-  Pylint cleanup also foreign code like ``oset`` and ``odict``.

-  In preparation of deprecating the alternative, ``--enable-plugin``
   has become the only form used in documentation and tests.

-  Avoid numeric pylint symbols more often.

-  Distutils: Cleanup module name for distutils commands, these are not
   actually enforced by distutils, but very ugly in our coding
   conventions.

-  The "cannot get here" code to mark unreachable code has been improved
   and no longer needs an identifier passed, but uses the standard C
   mechanism for that.

-  Removed accessors for lookup sources from nodes, allowing for faster
   usage and making sure, lookups are only done where needed.

*********
 Summary
*********

This release is huge in terms of bugs fixed, but also extremely
important, because the new loop SSA and type tracing, allows for many
more specialized code usages. We now can trace the type for some loops
to be specifically an integer or long value only, and will become able
to generate code that avoids using Python objects, in these cases.

Once that happens, the performance will make a big jump. Future releases
will have to consolidate the current state, but it is expected that at
least an experimental addition of C type ``float`` or ``C long`` can be
added, add to that ``iterator`` type shape and value analsis, and an
actual jump in performance can be expected.
