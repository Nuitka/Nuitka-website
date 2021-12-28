This is to inform you about the new stable release
of `Nuitka <https://nuitka.net>`_. It is the extremely
compatible Python compiler,  `"download now" </doc/download.html>`_.

This release breaks interface compatibility, therefore the major version
number change. Also "standalone mode" has seen significant improvements
on both Windows, and Linux. Should work much better now.

But consider that this part of Nuitka is still in its infancy. As it is
not the top priority of mine for Nuitka, which primarily is intended as
an super compatible accelerator of Python, it will continue to evolve
nearby.

There is also many new optimization based on structural improvements in
the direction of actual SSA.

Bug Fixes
=========

-  The "standalone mode" was not working on all Redhat, Fedora, and
   openSUSE platforms and gave warnings with older compilers. Fixed in
   0.4.7.1 already.

-  The "standalone mode" was not including all useful encodings. Fixed
   in 0.4.7.2 already.

-  The "standalone mode" was defaulting to ``--python-flag=-S`` which
   disables the parsing of "site" module. That unfortunately made it
   necessary to reach some modules without modifying ``PYTHONPATH``
   which conflicts with the "out-of-the-box" experience.

-  The "standalone mode" is now handling packages properly and generally
   working on Windows as well.

-  The syntax error of having an all catching except clause and then a
   more specific one wasn't causing a ``SyntaxError`` with Nuitka.

   .. code:: python

      try:
          something()
      except:
          somehandling()
      except TypeError:
          notallowed()

-  A corruption bug was identified, when re-raising exceptions, the top
   entry of the traceback was modified after usage. Depending on
   ``malloc`` this was potentially causing an endless loop when using it
   for output.

New Features
============

-  Windows: The "standalone" mode now properly detects used DLLs using
   `Dependency Walker <http://www.dependencywalker.com/>`__ which it
   offers to download and extra for you.

   It is used as a replacement to ``ldd`` on Linux when building the
   binary, and as a replacement of ``strace`` on Linux when running the
   tests to check that nothing is loaded from the outside.

Optimization
============

-  When iterating over ``list``, ``set``, this is now automatically
   lowered to ``tuples`` avoiding the mutable container types.

   So the following code is now equivalent:

   .. code:: python

      for x in [a, b, c]:
          ...

      # same as
      for x in (a, b, c):
          ...

   For constants, this is even more effective, because for mutable
   constants, no more is it necessary to make a copy.

-  Python2: The iteration of large ``range`` is now automatically
   lowered to ``xrange`` which is faster to loop over, and more memory
   efficient.

-  Added support for the ``xrange`` built-in.

-  The statement only expression optimization got generalized and now is
   capable of removing useless parts of operations, not only the whole
   thing when it has not side effects.

   .. code:: python

      [a, b]

      # same as
      a
      b

   This works for all container types.

   Another example is ``type`` built-in operation with single argument.
   When the result is not used, it need not be called.

   .. code:: python

      type(a)

      # same as
      a

   And another example ``is`` and ``is not`` have no effect of their own
   as well, therefore:

   .. code:: python

      a is b

      # same as
      a
      b

-  Added proper handling of conditional expression branches in SSA based
   optimization. So far these branches were ignored, which only
   acceptable for temporary variables as created by tree building, but
   not other variable types. This is preparatory for introducing SSA for
   local variables.

Organisational
==============

-  The option ``--exe`` is now ignored and creating an executable is the
   default behavior of ``nuitka``, a new option ``--module`` allows to
   produce extension modules.

-  The binary ``nuitka-python`` was removed, and is replaced by
   ``nuitka-run`` with now only implies ``--execute`` on top of what
   ``nuitka`` is.

-  Using dedicated `Buildbot <http://buildbot.net>`__ for continuous
   integration testing and release creation as well.

-  The `Downloads <https://nuitka.net/doc/download.html>`__ now offers
   MSI files for Win64 as well.

-  Discontinued the support for cross compilation to Win32. That was too
   limited and the design choice is to have a running CPython instance
   of matching architecture at Nuitka compile time.

New Tests
=========

-  Expanded test coverage for "standalone mode" demonstrating usage of
   "hex" encoding, and PySide package.

Summary
=======

The "executable by default" interface change improves on the already
high ease of use. The new optimization do not give all that much in
terms of numbers, but are all signs of structural improvements, and it
is steadily approaching the point, where the really interesting stuff
will happen.

The progress for standalone mode is of course significant. It is still
not quite there yet, but it is making quick progress now. This will
attract a lot of attention hopefully.

As for optimization, the focus for it has shifted to making exception
handlers work optimal by default (publish the exception to
``sys.exc_info()`` and create traceback only when necessary) and be
based on standard branches. Removing special handling of exception
handlers, will be the next big step. This release includes some
correctness fixes stemming from that work already.
