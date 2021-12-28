This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

The last release represented a significant change and introduced a few
regressions, which got addressed with hot fix releases. But it also had
a focus on cleaning up open optimization issues that were postponed in
the last release.

##############
 New Features
##############

-  The filenames of source files as found in the ``__file__`` attribute
   are now made relative for all modes, not just standalone mode.

   This makes it possible to put data files along side compiled modules
   in a deployment.

###########
 Bug Fixes
###########

-  Local functions that reference themselves were not released. They now
   are.

   .. code:: python

      def someFunction():
          def f():
              f()  # referencing 'f' in 'f' caused the garbage collection to fail.

   Recent changes to code generation attached closure variable values to
   the function object, so now they can be properly visited. Fixed in
   0.5.10.1 already.

-  Python2.6: The complex constants with real or imaginary parts
   ``-0.0`` were collapsed with constants of value ``0.0``. This became
   more evident after we started to optimize the ``complex`` built-in.
   Fixed in 0.5.10.1 already.

   .. code:: python

      complex(0.0, 0.0)
      complex(-0.0, -0.0)  # Could be confused with the above.

-  Complex call helpers could leak references to their arguments. This
   was a regression. Fixed in 0.5.10.1 already.

-  Parameter variables offered as closure variables were not properly
   released, only the cell object was, but not the value. This was a
   regression. Fixed in 0.5.10.1 already.

-  Compatibility: The exception type given when accessing local variable
   values not initialized in a closure taking function, needs to be
   ``NameError`` and ``UnboundLocalError`` for accesses in the providing
   function. Fixed in 0.5.10.1 already.

-  Fix support for "venv" on systems, where the system Python uses
   symbolic links too. This is the case on at least on Mageia Linux.
   Fixed in 0.5.10.2 already.

-  Python3.4: On systems where ``long`` and ``Py_ssize_t`` are different
   (e.g. Win64) iterators could be corrupted if used by uncompiled
   Python code. Fixed in 0.5.10.2 already.

-  Fix, generator objects didn't release weak references to them
   properly. Fixed in 0.5.10.2 already.

-  Compatibility: The ``__closure__`` attributes of functions was so far
   not supported, and rarely missing. Recent changes made it easy to
   expose, so now it was added.

-  macOS: A linker warning about deprecated linker option ``-s`` was
   solved by removing the option.

-  Compatibility: Nuitka was enforcing that the ``__doc__`` attribute to
   be a string object, and gave a misleading error message. This check
   must not be done though, ``__doc__`` can be any type in Python.

##############
 Optimization
##############

-  Variables that need not be shared, because the uses in closure taking
   functions were eliminated, no longer use cell objects.

-  The ``try``/``except`` and ``try``/``finally`` statements now both
   have actual merging for SSA, allowing for better optimization of code
   behind it.

   .. code:: python

      def f():

          try:
              a = something()
          except:
              return 2

          # Since the above exception handling cannot continue the code flow,
          # we do not have to invalidate the trace of "a", and e.g. do not have
          # to generate code to check if it's assigned.
          return a

   Since ``try``/``finally`` is used in almost all re-formulations of
   complex Python constructs this is improving SSA application widely.
   The uses of ``try``/``except`` in user code will no longer degrade
   optimization and code generation efficiency as much as they did.

-  The ``try``/``except`` statement now reduces the scope of tried block
   if possible. When no statement raised, already the handling was
   removed, but leading and trailing statements that cannot raise, were
   not considered.

   .. code:: python

      def f():

          try:
              b = 1
              a = something()
              c = 1
          except:
              return 2

   This is now optimized to.

   .. code:: python

      def f():

          b = 1
          try:
              a = something()
          except:
              return 2
          c = 1

   The impact may on execution speed may be marginal, but it is
   definitely going to improve the branch merging to be added later.
   Note that ``c`` can only be optimized, because the exception handler
   is aborting, otherwise it would change behaviour.

-  The creation of code objects for standalone mode and now all code
   objects was creating a distinct filename object for every function in
   a module, despite them being same content. This was wasteful for
   module loading. Now it's done only once.

   Also, when having multiple modules, the code to build the run time
   filename used for code objects, was calling import logic, and doing
   lookups to find ``os.path.join`` again and again. These are now
   cached, speeding up the use of many modules as well.

##########
 Cleanups
##########

-  Nuitka used to have "variable usage profiles" and still used them to
   decide if a global variable is written to, in which case, it stays
   away from doing optimization of it to built-in lookups, and later
   calls.

   The have been replaced by "global variable traces", which collect the
   traces to a variable across all modules and functions. While this is
   now only a replacement, and getting rid of old code, and basing on
   SSA, later it will also allow to become more correct and more
   optimized.

-  The standalone now queries its hidden dependencies from a plugin
   framework, which will become an interface to Nuitka internals in the
   future.

#########
 Testing
#########

-  The use of deep hashing of constants allows us to check if constants
   become mutated during the run-time of a program. This allows to
   discover corruption should we encounter it.

-  The tests of CPython are now also run with Python in debug mode, but
   only on Linux, enhancing reference leak coverage.

-  The CPython test parts which had been disabled due to reference
   cycles involving compiled functions, or usage of ``__closure__``
   attribute, were reactivated.

################
 Organisational
################

-  Since Google Code has shutdown, it has been removed from the Nuitka
   git mirrors.

#########
 Summary
#########

This release brings exciting new optimization with the focus on the
``try`` constructs, now being done more optimal. It is also a
maintenance release, bringing out compatibility improvements, and
important bug fixes, and important usability features for the deployment
of modules and packages, that further expand the use cases of Nuitka.

The git flow had to be applied this time to get out fixes for regression
bug fixes, that the big change of the last release brought, so this is
also to consolidate these and the other corrections into a full release
before making more invasive changes.

The cleanups are leading the way to expanded SSA applied to global
variable and shared variable values as well. Already the built-in detect
is now based on global SSA information, which was an important step
ahead.
