This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is finally making full use of SSA analysis knowledge for
code generation, leading to many enhancements over previous releases.

It also adds support for Python3.4, which has been longer in the making,
due to many rather subtle issues. In fact, even more work will be needed
to fully solve remaining minor issues, but these should affect no real
code.

And then there is much improved support for using standalone mode
together with virtualenv. This combination was not previously supported,
but should work now.

**************
 New Features
**************

-  Added support for Python3.4

   This means support for ``clear`` method of frames to close
   generators, dynamic ``__qualname__``, affected by ``global``
   statements, tuples as ``yield from`` arguments, improved error
   messages, additional checks, and many more detail changes.

******************
 New Optimization
******************

-  Using SSA knowledge, local variable assignments now no longer need to
   check if they need to release previous values, they know definitely
   for the most cases.

   .. code:: python

      def f():
          a = 1  # This used to check if old value of "a" needs a release
          ...

-  Using SSA knowledge, local variable references now no longer need to
   check for raising exceptions, let alone produce exceptions for cases,
   where that cannot be.

   .. code:: python

      def f():
          a = 1
          return a  # This used to check if "a" is assigned

-  Using SSA knowledge, local variable references now are known if they
   can raise the ``UnboundLocalError`` exception or not. This allows to
   eliminate frame usages for many cases. Including the above example.

-  Using less memory for keeping variable information.

-  Also using less memory for constant nodes.

***********
 Bug Fixes
***********

-  The standalone freezing code was reading Python source as UTF-8 and
   not using the code that handles the Python encoding properly. On some
   platforms there are files in standard library that are not encoded
   like that.

-  The fiber implementation for Linux amd64 was not working with glibc
   from RHEL 5. Fixed to use now multiple ``int`` to pass pointers as
   necessary. Also use ``uintptr_t`` instead of ``intprt_t`` to
   transport pointers, which may be more optimal.

-  Line numbers for exceptions were corrupted by ``with`` statements due
   to setting line numbers even for statements marked as internal.

-  Partial support for ``win32com`` by adding support for its hidden
   ``__path__`` change.

-  Python3: Finally figured out proper chaining of exceptions, given
   proper context messages for exception raised during the handling of
   exceptions.

-  Corrected C++ memory leak for each closure variable taken, each time
   a function object was created.

-  Python3: Raising exceptions with tracebacks already attached, wasn't
   using always them, but producing new ones instead.

-  Some constants could cause errors, as they cannot be handled with the
   ``marshal`` module as expected, e.g. ``(int,)``.

-  Standalone: Make sure to propagate ``sys.path`` to the Python
   instance used to check for standard library import dependencies. This
   is important for virtualenv environments, which need ``site.py`` to
   set the path, which is not executed in that mode.

-  Windows: Added support for different path layout there, so using
   virtualenv should work there too.

-  The code object flag "optimized" (fast locals as opposed to locals
   dictionary) for functions was set wrongly to value for the parent,
   but for frames inside it, one with the correct value. This lead to
   more code objects than necessary and false ``co_flags`` values
   attached to the function.

-  Options passed to ``nuitka-python`` could get lost.

   .. code:: sh

      nuitka-python program.py argument1 argument2 ...

   The above is supposed to compile program.py, execute it immediately
   and pass the arguments to it. But when Nuitka decides to restart
   itself, it would forget these options. It does so to e.g. disable
   hash randomization as it would affect code generation.

-  Raising tuples exception as exceptions was not compatible (Python2)
   or reference leaking (Python3).

*******
 Tests
*******

-  Running ``2to3`` is now avoided for tests that are already running on
   both Python2 and Python3.

-  Made XML based optimization tests work with Python3 too. Previously
   these were only working on Python2.

-  Added support for ignoring messages that come from linking against
   self compiled Pythons.

-  Added test case for threaded generators that tortures the fiber layer
   a bit and exposed issues on RHEL 5.

-  Made reference count test of compiled functions generic. No more code
   duplication, and automatic detection of shared stuff. Also a more
   clear interface for disabling test cases.

-  Added Python2 specific reference counting tests, so the other cases
   can be executed with Python3 directly, making debugging them less
   tedious.

**********
 Cleanups
**********

-  Really important removal of "variable references". They didn't solve
   any problem anymore, but their complexity was not helpful either.
   This allowed to make SSA usable finally, and removed a lot of code.

-  Removed special code generation for parameter variables, and their
   dedicated classes, no more needed, as every variable access code is
   now optimized like this.

-  Stop using C++ class methods at all. Now only the destructor of local
   variables is actually supposed to do anything, and their are no
   methods anymore. The unused ``var_name`` got removed,
   ``setVariableValue`` is now done manually.

-  Moved assertions for the fiber layer to a common place in the header,
   so they are executed on all platforms in debug mode.

-  As usual, also a bunch of cleanups for PyLint were applied.

-  The ``locals`` built-in code now uses code generation for accessing
   local variable values instead having its own stuff.

****************
 Organizational
****************

-  The Python version 3.4 is now officially supported. There are a few
   problems open, that will be addressed in future releases, none of
   which will affect normal people though.

-  Major cleanup of Nuitka options.

      -  Windows specific stuff is now in a dedicated option group. This
         includes options for icon, disabling console, etc.
      -  There is now a dedicated group for controlling backend compiler
         choices and options.

-  Also pickup ``g++44`` automatically, which makes using Nuitka on
   CentOS5 more automatic.

*********
 Summary
*********

This release represents a very important step ahead. Using SSA for real
stuff will allow us to build the trust necessary to take the next steps.
Using the SSA information, we could start implementing more
optimizations.
