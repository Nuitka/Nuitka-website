This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release comes after a long time and contains large amounts of
changes in all areas. The driving goal was to prepare generating C
specific code, which is still not the case, but this is very likely
going to change soon. However this release improves all aspects.

Bug Fixes
=========

-  Compatibility: Fix, for star imports didn't check the values from the
   ``__all__`` iterable, if they were string values which could cause
   problems at run time.

   .. code:: python

      # Module level
      __all__ = (1,)

      # ...
      # other module:
      from module import *

-  Fix, for star imports, also didn't check for values from ``__all__``
   if they actually exist in the original values.

-  Corner cases of imports should work a lot more precise, as the level
   of compatibility for calls to ``__import__`` went from absurd to
   insane.

-  Windows: Fixed detection of uninstalled Python versions (not for all
   users and DLL is not in system directory). This of course only
   affected the accelerated mode, not standalone mode.

-  Windows: Scan directories for ``.pyd`` files for used DLLs as well.
   This should make the PyQt5 wheel work.

-  Python3.5: Fix, coroutines could have different code objects for the
   object and the frame using by it.

-  Fix, slices with built-in names crashed the compiler.

   .. code:: python

      something[id:len:range]

-  Fix, the C11 via C++ compatibility uses symlinks tp C++ filenames
   where possible instead of making a copy from the C source. However,
   even on Linux that may not be allowed, e.g. on a DOS file system.
   Added fallback to using full copy in that case. `Issue#353
   <http://bugs.nuitka.net/issue353>`__.

-  Python3.5: Fix coroutines to close the "yield from" where an
   exception is thrown into them.

-  Python3: Fix, list contractions should have their own frame too.

-  Linux: Copy the "rpath" of compiling Python binary to the created
   binary. This will make compiled binaries using uninstalled Python
   versions transparently find the Python shared library.

-  Standalone: Add the "rpath" of the compiling Python binary to the
   search path when checking for DLL dependencies on Linux. This fixes
   standalone support for Travis and Anaconda on Linux.

-  Scons: When calling scons, also try to locate a Python2 binary to
   overcome a potential Python3 virtualenv in which Nuitka is running.

-  Standalone: Ignore more Windows only encodings on non-Windows.

New Features
============

-  Support for Python 3.6 with only few corner cases not supported yet.

-  Added options ``--python-arch`` to pick 32 or 64 bits Python target
   of the ``--python-version`` argument.

-  Added support for more kinds of virtualenv configurations.

-  Uninstalled Python versions such as Anaconda will work fine in
   accelerated mode, except on Windows.

Optimization
============

-  The node tree children are no longer stored in a separate dictionary,
   but in the instance dictionary as attributes, making the tree more
   lightweight and in principle faster to access. This also saved about
   6% of the memory usage.

-  The memory usage of Nuitka for the Python part has fallen by roughly
   40% due to the use of new style classes, and slots where that is
   possible (some classes use multiple inheritance, where they don't
   work), and generally by reducing useless members e.g. in source code
   references. This of course also will make things compiled faster (the
   C compilation of course is not affected by this.)

-  The code generation for frames was creating the dictionary for the
   raised exception by making a dictionary and then adding all
   variables, each tested to be set. This was a lot of code for each
   frame specific, and has been replaced by a generic "attach" mechanism
   which merely stores the values, and only takes a reference. When
   asked for frame locals, it only then builds the dictionary. So this
   is now only done, when that is absolutely necessary, which it
   normally never is. This of course makes the C code much less verbose,
   and actual handling of exceptions much more efficient.

-  For imports, we now detect for built-in modules, that their import
   cannot fail, and if name lookups can fail. This leads to less code
   generated for error handling of these. The following code now e.g.
   fully detects that no ``ImportError`` or ``AttributeError`` will
   occur.

   .. code:: python

      try:
          from __builtin__ import len
      except ImportError:
          from builtins import len

-  Added more type shapes for built-in type calls. These will improve
   type tracing.

-  Compiled frames now have a free list mechanism that should speed up
   frames that recurse and frames that exit with exceptions. In case of
   an exception, the frame ownership is immediately transferred to the
   exception making it easier to deal with.

-  The free list implementations have been merged into a new common one
   that can be used via macro expansion. It is now type agnostic and be
   slightly more efficient too.

-  Also optimize "true" division and "floor division", not only the
   default division of Python2.

-  Removed the need for statement context during code generation making
   it less memory intensive and faster.

Cleanups
========

-  Now always uses the ``__import__`` built-in node for all kinds of
   imports and directly optimizes and recursion into other modules based
   on that kind of node, instead of a static variant. This removes
   duplication and some incompatibility regarding defaults usage when
   doing the actual imports at run time.

-  Split the expression node bases and mixin classes to a dedicated
   module, moving methods that only belong to expressions outside of the
   node base, making for a cleaner class hierarchy.

-  Cleaned up the class structure of nodes, added base classes for
   typical compositions, e.g. expression with and without children,
   computation based on built-in, etc. while also checking proper
   ordering of base classes in the metaclass.

-  Moved directory and file operations to dedicated module, making also
   sure it is more generally used. This makes it easier to make more
   error resilient deletions of directories on e.g. Windows, where locks
   tend to live for short times beyond program ends, requiring second
   attempts.

-  Code generation for existing supported types, ``PyObject *``,
   ``PyObject **``, and ``struct Nuitka_CellObject *`` is now done via a
   C type class hierarchy instead of ``elif`` sequences.

-  Closure taking is now always done immediately correctly and
   references are take for closure variables still needed, making sure
   the tree is correct and needs no finalization.

-  When doing variable traces, initialize more traces immediately so it
   can be more reliable.

-  Code to setup a function for local variables and clean it up has been
   made common code instead of many similar copies.

-  The code was treating the ``f_executing`` frame member as if it were
   a counter with increases and decreases. Turn it into a mere boolean
   value and hide its usage behind helper functions.

-  The "maybe local variables" are no more. They were replaced by a new
   locals dict access node with a fallback to a module or closure
   variable should the dictionary not contain the name. This avoids many
   ugly checks to not do certain things for that kind of variable.

-  We now detect "exec" and "unqualified exec" as well as "star import"
   ahead of time as flags of the function to be created. We no longer
   need to mark functions as we go.

-  Handle "true", "floor" and normal division properly by applying
   future flags to decide which one to use.

-  We now use symbolic identifiers in all PyLint annotations.

-  The release scripts started to move into ``nuitka.tools.release`` so
   they get PyLint checks, autoformat and proper code re-use.

-  The use of ``INCREASE_REFCOUNT_X`` was removed, it got replaced with
   proper ``Py_XINCREF`` usages.

-  The use of ``INCREASE_REFCOUNT`` got reduced further, e.g. no
   generated code uses it anymore, and only a few compiled types do. The
   function was once required before "C-ish" lifted the need to do
   everything in one single function call.

Tests
=====

-  More robust deletion of directories, temporary stages used by CPython
   test suites, and standalone directories during test execution.

-  Moved tests common code into ``nuitka.tools.testing`` namespace and
   use it from there. The code now is allowed to use ``nuitka.utils``
   and therefore often better implementations.

-  Made standalone binaries robust against GTK theme access, checking
   the Python binary (some site.py files do that),

Organisational
==============

-  Added repository for Ubuntu Zesty (17.04) for download.

-  Added support for testing with Travis to complement the internal
   Buildbot based infrastructure and have pull requests on Github
   automatically tested before merge.

-  The ``factory`` branch is now also on Github.

-  Removed MSI for Python3.4 32 bits. It seems impossible to co-install
   this one with the 64 bits variant. All other versions are provided
   for both bit sizes still.

Summary
=======

This release marks huge progress. The node tree is now absolutely clean,
the variable closure taking is fully represented, and code generation is
prepared to add another type, e.g. for ``bool`` for which work has
already started.

On a practical level, the scalability of the release will have increased
very much, as this uses so much less memory, generates simpler C code,
while at the same time getting faster for the exception cases.

Coming releases will expand on the work of this release.

Frame objects should be allowed to be nested inside a function for
better re-formulations of classes and contractions of all kinds, as well
as real inline of functions, even if they could raise.

The memory savings could be even larger, if we stopped doing multiple
inheritance for more node types. The ``__slots__`` were and the child
API change could potentially make things not only more compact, but
faster to use too.

And also once special C code generation for ``bool`` is done, it will
set the stage for more types to follow (``int``, ``float``, etc). Only
this will finally start to give the C type speed we are looking for.

Until then, this release marks a huge cleanup and progress to what we
already had, as well as preparing the big jump in speed.
