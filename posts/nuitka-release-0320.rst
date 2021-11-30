This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This time there are a few bug fixes and some really major cleanups, lots
of new optimization and preparations for more. And then there is a new
compiler clang and a new platform supported. macOS X appears to work
mostly, thanks for the patches from Pete Hunt.

Bug fixes
=========

-  The use of a local variable name as an expression was not covered and
   lead to a compiler crash. Totally amazing, but true, nothing in the
   test suite of CPython covered this. `Issue#30
   <http://bugs.nuitka.net/issue30>`__. Fixed in release 0.3.19.1
   already.

-  The use of a closure variable name as an expression was not covered
   as well. And in this case corrupted the reference count. `Issue#31
   <http://bugs.nuitka.net/issue31>`__. Fixed in release 0.3.19.1
   already.

-  The ``from x import *`` attempted to respect ``__all__`` but failed
   to do so. `Issue#32 <http://bugs.nuitka.net/issue32>`__. Fixed in
   release 0.3.19.2 already.

-  The ``from x import *`` didn't give a ``SyntaxError`` when used on
   Python3. Fixed in release 0.3.19.2 already.

-  The syntax error messages for "global for function argument name" and
   "duplicate function argument name" are now identical as well.

-  Parameter values of generator function could cause compilation errors
   when used in the closure of list contractions. Fixed.

New Features
============

-  Added support for disabling the console for Windows binaries. Thanks
   for the patch go to Michael H Kent.

-  Enhanced Python3 support for syntax errors, these are now also
   compatible.

-  Support for macOS X was added.

-  Support for using the clang compiler was added, it can be enforced
   via ``--clang`` option. Currently this option is mainly intended to
   allow testing the "macOS X" support as good as possible under Linux.

Optimization
============

-  Enhanced all optimization that previously worked on "constants" to
   work on "compile time constants" instead. A "compile time constant"
   can currently also be any form of a built-in name or exception
   reference. It is intended to expand this in the future.

-  Added support for built-ins ``bin``, ``oct``, and ``hex``, which also
   can be computed at compile time, if their arguments are compile time
   constant.

-  Added support for the ``iter`` built-in in both forms, one and two
   arguments. These cannot be computed at compile time, but now will
   execute faster.

-  Added support for the ``next`` built-in, also in its both forms, one
   and two arguments. These also cannot be computed at compile time, but
   now will execute faster as well.

-  Added support for the ``open`` built-in in all its form. We intend
   for future releases to be able to track file opens for including them
   into the executable if data files.

-  Optimize the ``__debug__`` built-in constant as well. It cannot be
   assigned, yet code can determine a mode of operation from it, and
   apparently some code does. When compiling the mode is decided.

-  Optimize the ``Ellipsis`` built-in constant as well. It falls in the
   same category as ``True``, ``False``, ``None``, i.e. names of
   built-in constants that a singletons.

-  Added support for anonymous built-in references, i.e. built-ins which
   have names that are not normally accessible. An example is
   ``type(None)`` which is not accessible from anywhere. Other examples
   of such names are ``compiled_method_or_function``.

   Having these as represented internally, and flagged as "compile time
   constants", allows the compiler to make more compile time
   optimization and to generate more efficient C++ code for it that
   won't e.g. call the ``type`` built-in with ``None`` as an argument.

-  All built-in names used in the program are now converted to "built-in
   name references" in a first step. Unsupported built-ins like e.g.
   ``zip``, for which Nuitka has no own code or understanding yet,
   remained as "module variables", which made access to them slow, and
   difficult to recognize.

-  Added optimization for module attributes ``__file__``, ``__doc__``
   and ``__package__`` if they are read only. It's the same as
   ``__name__``.

-  Added optimization for slices and subscripts of "compile time
   constant" values. These will play a more important role, once value
   propagation makes them more frequent.

Organisational
==============

-  Created a "change log" from the previous release announcements. It's
   as ReStructured Text and converted to PDF for the release as well,
   but I chose not to include that in Debian, because it's so easy to
   generate the PDF on that yourself.

-  The posting of release announcements is now prepared by a script that
   converts the ReStructured Text to HTML and adds it to Wordpress as a
   draft posting or updates it, until it's release time. Simple, sweet
   and elegant.

Cleanups
========

-  Split out the ``nuitka.nodes.Nodes`` module into many topic nodes, so
   that there are now ``nuitka.nodes.BoolNodes`` or
   ``nuitka.nodes.LoopNodes`` to host nodes of similar kinds, so that it
   is now cleaner.

-  Split ``del`` statements into their own node kind, and use much
   simpler node structures for them. The following blocks are absolutely
   the same:

   .. code:: python

      del a, b.c, d

   .. code:: python

      del a
      del b.c
      del d

   So that's now represented in the node tree. And even more complex
   looking cases, like this one, also the same:

   .. code:: python

      del a, (b.c, d)

   This one gives a different parse tree, but the same bytecode. And so
   Nuitka need no longer concern itself with this at all, and can remove
   the tuple from the parse tree immediately. That makes them easy to
   handle. As you may have noted already, it also means, there is no way
   to enforce that two things are deleted or none at all.

-  Turned the function and class builder statements into mere assignment
   statements, where defaults and base classes are handled by wrapping
   expressions.

   Previously they are also kind of assignment statements too, which is
   not needed. Now they were reduced to only handle the ``bases`` for
   classes and the ``defaults`` for functions and make optional.

-  Refactored the decorator handling to the tree building stage,
   presenting them as function calls on "function body expression" or
   class body expression".

   This allowed to remove the special code for decorators from code
   generation and C++ templates, making decorations easy subjects for
   future optimization, as they practically are now just function calls.

   .. code:: python

      @some_classdecorator
      class C:
          @staticmethod
          def f():
              pass

   It's just a different form of writing things. Nothing requires the
   implementation of decorators, it's just functions calls with function
   bodies before the assignment.

   The following is only similar:

   .. code:: python

      class C:
          def f():
              pass

          f = staticmethod(f)


      C = some_classdecorator(C)

   It's only similar, because the assignment to an intermediate value of
   ``C`` and ``f`` is not done, and if an exception was raised by the
   decoration, that name could persist. For Nuitka, the function and
   class body, before having a name, are an expression, and so can of
   course be passed to decorators already.

-  The in-place assignments statements are now handled using temporary
   variable blocks

   Adding support for scoped temporary variables and references to them,
   it was possible to re-formulate in-place assignments expressions as
   normal look-ups, in-place operation call and then assignment
   statement. This allowed to remove static templates and will yield
   even better generated code in the future.

-  The for loop used to have has a "source" expression as child, and the
   iterator over it was only taken at the code generation level, so that
   step was therefore invisible to optimization. Moved it to tree
   building stage instead, where optimization can work on it then.

-  Tree building now generally allows statement sequences to be ``None``
   everywhere, and pass statements are immediately eliminated from them
   immediately. Empty statement sequences are now forbidden to exist.

-  Moved the optimization for ``__name__`` to compute node of variable
   references, where it doesn't need anything complex to replace with
   the constant value if it's only read.

-  Added new bases classes and mix-in classes dedicated to expressions,
   giving a place for some defaults.

-  Made the built-in code more reusable.

New Tests
=========

-  Added some more diagnostic tests about complex assignment and ``del``
   statements.

-  Added syntax test for star import on function level, that must fail
   on Python3.

-  Added syntax test for duplicate argument name.

-  Added syntax test for global on a function argument name.

Summary
=======

The decorator and building changes, the assignment changes, and the node
cleanups are all very important progress for the type inference work,
because they remove special casing the that previously would have been
required. Lambdas and functions now really are the same thing right
after tree building. The in-place assignments are now merely done using
standard assignment code, the built functions and classes are now
assigned to names in assignment statements, much *more* consistency
there.

Yet, even more work will be needed in the same direction. There may e.g.
be work required to cover ``with`` statements as well. And assignments
will become no more complex than unpacking from a temporary variable.

For this release, there is only minimal progress on the Python3 front,
despite the syntax support, which is only minuscule progress. The
remaining tasks appear all more or less difficult work that I don't want
to touch now.

There are still remaining steps, but we can foresee that a release may
be done that finally actually does type inference and becomes the
effective Python compiler this project is all about.
