This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release brings bug fixes, important new optimization, newly
supported platforms, and important compatibility improvements. Progress
on all fronts.

###########
 Bug Fixes
###########

-  Closure taking of global variables in member functions of classes
   that had a class variable of the same name was binding to the class
   variable as opposed to the module variable.

-  Overwriting compiled function's ``__doc__`` attribute more than once
   could corrupt the old value, leading to crashes. Fixed in 0.5.5.2
   already.

-  Compatibility Python2: The ``exec`` statement ``execfile`` were
   changing ``locals()`` was given as an argument.

   .. code:: python

      def function():
          a = 1

          exec code in locals()  # Cannot change local "a".
          exec code in None  # Can change local "a"
          exec code

   Previously Nuitka treated all 3 variants the same.

-  Compatibility: Empty branches with a condition were reduced to only
   the condition, but they need in fact to also check the truth value:

   .. code:: python

      if condition:
          pass
      # must be treated as
      bool(condition)
      # and not (bug)
      condition

-  Detection of Windows virtualenv was not working properly. Fixed in
   0.5.5.2 already.

-  Large enough constants structures are now unstreamed via ``marshal``
   module, avoiding large codes being generated with no point. Fixed in
   0.5.5.2 already.

-  Windows: Pressing CTRL-C gave two stack traces, one from the
   re-execution of Nuitka which was rather pointless. Fixed in 0.5.5.1
   already.

-  Windows: Searching for virtualenv environments didn't terminate in
   all cases. Fixed in 0.5.5.1 already.

-  During installation from PyPI with Python3 versions, there were
   errors given for the Python2 only scons files. Fixed in 0.5.5.3
   already.

-  Fix, the arguments of ``yield from`` expressions could be leaked.

-  Fix, closure taking of a class variable could have in a sub class
   where the module variable was meant.

   .. code:: python

      var = 1


      class C:
          var = 2

          class D:
              def f():
                  # was C.var, now correctly addressed top level var
                  return var

-  Fix, setting ``CXX`` environment variable because the installed gcc
   has too low version, wasn't affecting the version check at all.

-  Fix, on Debian/Ubuntu with ``hardening-wrapper`` installed the
   version check was always failing, because these report a shortened
   version number to Scons.

##############
 Optimization
##############

-  Local variables that must be assigned also have no side effects,
   making use of SSA. This allows for a host of optimization to be
   applied to them as well, often yielding simpler access/assign code,
   and discovering in more cases that frames are not necessary.

-  Micro optimization to ``dict`` built-in for simpler code generation.

################
 Organisational
################

-  Added support for ARM "hard float" architecture.

-  Added package for Ubuntu 14.10 for download.

-  Added package for openSUSE 13.2 for download.

-  Donations were used to buy a Cubox-i4 Pro. It got Debian Jessie
   installed on it, and will be used to run an even larger amount of
   tests.

-  Made it more clear in the user documentation that the ``.exe`` suffix
   is used for all platforms, and why.

-  Generally updated information in User Manual and Developer Manual
   about the optimization status.

-  Using Nikola 7.1 with external filters instead of our own, outdated
   branch for the web site.

##########
 Cleanups
##########

-  PyLint clean for the first time ever. We now have a Buildbot driven
   test that this stays that way.

-  Massive indentation cleanup of keyword argument calls. We have a rule
   to align the keywords, but as this was done manually, it could easily
   get out of touch. Now with a "autoformat" tool based on RedBaron,
   it's correct. Also, spacing around arguments is now automatically
   corrected. More to come.

-  For ``exec`` statements, the coping back to local variables is now an
   explicit node in the tree, leader to cleaner code generation, as it
   now uses normal variable assignment code generation.

-  The ``MaybeLocalVariables`` became explicit about which variable they
   might be, and contribute to its SSA trace as well, which was
   incomplete before.

-  Removed some cases of code duplication that were marked as TODO
   items. This often resulted in cleanups.

-  Do not use ``replaceWith`` on child nodes, that potentially were
   re-used during their computation.

#########
 Summary
#########

The release is mainly the result of consolidation work. While the
previous release contained many important enhancements, this is another
important step towards full SSA, closing one loop whole (class variables
and ``exec`` functions), as well as applying it to local variables,
largely extending its use.

The amount of cleanups is tremendous, in huge part due to infrastructure
problems that prevented release repeatedly. This reduces the
technological debt very much.

More importantly, it would appear that now eliminating local and
temporary variables that are not necessary is only a small step away.
But as usual, while this may be easy to implement now, it will uncover
more bugs in existing code, that we need to address before we continue.
