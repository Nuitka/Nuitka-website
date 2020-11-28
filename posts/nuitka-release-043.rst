This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release expands the reach of Nuitka substantially, as new platforms
and compilers are now supported. A lot of polish has been applied. Under
the hood there is the continued and in-progress effort to implement SSA
form in Nuitka.

**************
 New Features
**************

-  Support for new compiler: Microsoft Visual C++.

   You can now use Visual Studio 2008 or Visual Studio 2010 for
   compiling under Windows.

-  Support for NetBSD.

   Nuitka works for at least NetBSD 6.0, older versions may or may not
   work. This required fixing bugs in the generic "fibers"
   implementation.

-  Support for Python3 under Windows too.

   Nuitka uses Scons to build the generated C++ files. Unfortunately it
   requires Python2 to execute, which is not readily available to call
   from Python3. It now guesses the default installation paths of
   CPython 2.7 or CPython 2.6 and it will use it for running Scons
   instead. You have to install it to ``C:\Python26`` or ``C:\Python27``
   for Nuitka to be able to find it.

-  Enhanced Python 3.3 compatibility.

   The support the newest version of Python has been extended, improving
   compatibility for many minor corner cases.

-  Added warning when a user compiles a module and executes it
   immediately when that references ``__name__``.

   Because very likely the intention was to create an executable. And
   esp. if there is code like this:

   .. code:: python

      if __name__ == "__main__":
          main()

   In module mode, Nuitka will optimize it away, and nothing will happen
   on execution. This is because the command

   .. code:: sh

      nuitka --execute module

   is behavioral more like

      python -c "import module"

   and that was a trap for new users.

-  All Linux architectures are now supported. Due to changes in how
   evaluation order is enforced, we don't have to implement for specific
   architectures anymore.

***********
 Bug Fixes
***********

-  Dictionary creation was not fully compatible.

   As revealed by using Nuitka with CPython3.3, the order in which
   dictionaries are to be populated needs to be reversed, i.e. CPython
   adds the last item first. We didn't observe this before, and it's
   likely the new dictionary implementation that finds it.

   Given that hash randomization makes dictionaries item order
   undetermined anyway, this is more an issue of testing.

-  Evaluation order for arguments of calls was not effectively enforced.
   It is now done in a standards compliant and therefore fully portable
   way. The compilers and platforms so far supported were not affected,
   but the newly supported Visual Studio C++ compiler was.

-  Using a ``__future__`` import inside a function was giving an
   assertion, instead of the proper syntax error.

-  Python3: Do not set the attributes ``sys.exc_type``,
   ``sys.exc_value``, ``sys.exc_traceback``.

-  Python3: Annotations of function worked only as long as their
   definition was not referring to local variables.

******************
 New Optimization
******************

-  Calls with no positional arguments are now using the faster call
   methods.

   The generated C++ code was using the ``()`` constant at call site,
   when doing calls that use no positional arguments, which is of course
   useless.

-  For Windows now uses OS "Fibers" for Nuitka "Fibers".

   Using threads for fibers was causing only overhead and with this API,
   MSVC had less issues too.

****************
 Organizational
****************

-  Accepting `Donations <https://nuitka.net/pages/donations.html>`__ via
   Paypal, please support funding travels, website, etc.

-  The "`User Manual <https://nuitka.net/doc/user-manual.html>`__" has
   been updated with new content. We now do support Visual Studio,
   documented the required LLVM version for clang, Win64 and modules may
   include modules too, etc. Lots of information was no longer accurate
   and has been updated.

-  The Changelog has been improved for consistency, wordings, and
   styles.

-  Nuitka is now available on the social code platforms as well

   -  `Bitbucket <https://bitbucket.org/kayhayen/nuitka>`__
   -  `Github <https://github.com/kayhayen/Nuitka>`__
   -  `Gitorious <https://gitorious.org/nuitka/nuitka>`__
   -  `Google Code <https://code.google.com/p/nuitka/>`__

-  Removed "clean-up.sh", which is practically useless, as tests now
   clean up after themselves reasonably, and with ``git clean -dfx``
   working better.

-  Removed "create-environment.sh" script, which was only setting the
   ``PATH`` variable, which is not necessary.

-  Added ``check-with-pylint --emacs`` option to make output its work
   with Emacs compilation mode, to allow easier fixing of warnings from
   PyLint.

-  Documentation is formatted for 80 columns now, source code will
   gradually aim at it too. So far 90 columns were used, and up to 100
   tolerated.

**********
 Cleanups
**********

-  Removed useless manifest and resource file creation under Windows.

   Turns out this is no longer needed at all. Either CPython, MinGW, or
   Windows improved to no longer need it.

-  PyLint massive cleanups and annotations bringing down the number of
   warnings by a lot.

-  Avoid use of strings and built-ins as run time pre-computed constants
   that are not needed for specific Python versions, or Nuitka modes.

-  Do not track needed tuple, list, and dict creation code variants in
   context, but e.g. in ``nuitka.codegen.TupleCodes`` module instead.

-  Introduced an "internal" module to host the complex call helper
   functions, instead of just adding it to any module that first uses
   it.

***********
 New Tests
***********

-  Added basic tests for order evaluation, where there currently were
   None.
-  Added support for "2to3" execution under Windows too, so we can run
   tests for Python3 installations too.

*********
 Summary
*********

The release is clearly major step ahead. The new platform support
triggered a whole range of improvements, and means this is truly
complete now.

Also there is very much polish in this release, reducing the number of
warnings, updated documentation, the only thing really missing is
visible progress with optimization.
