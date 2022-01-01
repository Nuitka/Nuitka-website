.. post:: 2013/03/05 22:13
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.4.1
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release is the first follow-up with a focus on optimization. The
major highlight is progress towards SSA form in the node tree.

Also a lot of cleanups have been performed, for both the tree building,
which is now considered mostly finished, and will be only reviewed. And
for the optimization part there have been large amounts of changes.

**************
 New Features
**************

-  Python 3.3 experimental support

   -  Now compiles many basic tests. Ported the dictionary quick access
      and update code to a more generic and useful interface.
   -  Added support for ``__qualname__`` to classes and functions.
   -  Small compatibility changes. Some exceptions changed, absolute
      imports are now default, etc.
   -  For comparison tests, the hash randomization is disabled.

-  Python 3.2 support has been expanded.

   The Python 3.2 on Ubuntu is not providing a helper function that was
   used by Nuitka, replaced it with out own code.

***********
 Bug fixes
***********

-  Default values were not "is" identical.

   .. code:: python

      def defaultKeepsIdentity(arg="str_value"):
          print arg is "str_value"


      defaultKeepsIdentity()

   This now prints "True" as it does with CPython. The solution is
   actually a general code optimization, see below.

-  Usage of ``unicode`` built-in with more than one argument could
   corrupt the encoding argument string.

   An implementation error of the ``unicode`` was releasing references
   to arguments converted to default encoding, which could corrupt it.

-  Assigning Python3 function annotations could cause a segmentation
   fault.

**************
 Optimization
**************

-  Improved propagation of exception raise statements, eliminating more
   code. They are now also propagated from all kinds of expressions.
   Previously this was more limited. An assertion added will make sure
   that all raises are propagated. Also finally, raise expressions are
   converted into raise statements, but without any normalization.

   .. code:: python

      # Now optimizing:
      raise TypeError, 1 / 0
      # into (minus normalization):
      raise ZeroDivisionError, "integer division or modulo by zero"

      # Now optimizing:
      (1 / 0).something
      # into (minus normalization):
      raise ZeroDivisionError, "integer division or modulo by zero"

      # Now optimizing:
      function(a, 1 / 0).something
      # into (minus normalization), notice the side effects of first checking
      # function and a as names to be defined, these may be removed only if
      # they can be demonstrated to have no effect.
      function
      a
      raise ZeroDivisionError, "integer division or modulo by zero"

   There is more examples, where the raise propagation is new, but you
   get the idea.

-  Conditional expression nodes are now optimized according to the truth
   value of the condition, and not only for compile time constants. This
   covers e.g. container creations, and other things.

   .. code:: python

      # This was already optimized, as it's a compile time constant.
      a if ("a",) else b
      a if True else b

      # These are now optimized, as their truth value is known.
      a if (c,) else b
      a if not (c,) else b

   This is simply taking advantage of infrastructure that now exists.
   Each node kind can overload "getTruthValue" and benefit from it. Help
   would be welcome to review which ones can be added.

-  Function creations only have side effects, when their defaults or
   annotations (Python3) do. This allows to remove them entirely, should
   they be found to be unused.

-  Code generation for constants now shares element values used in
   tuples.

   The general case is currently too complex to solve, but we now make
   sure constant tuples (as e.g. used in the default value for the
   compiled function), and string constants share the value. This should
   reduce memory usage and speed up program start-up.

**********
 Cleanups
**********

-  Optimization was initially designed around visitors that each did one
   thing, and did it well. It turns out though, that this approach is
   unnecessary, and constraint collection, allows for the most
   consistent results. All remaining optimization has been merged into
   constraint collection.

-  The names of modules containing node classes were harmonized to
   always be plural. In the beginning, this was used to convey the
   information that only a single node kind would be contained, but that
   has long changed, and is unimportant information.

-  The class names of nodes were stripped from the "CPython" prefix.
   Originally the intent was to express strict correlation to CPython,
   but with increasing amounts of re-formulations, this was not used at
   all, and it's also not important enough to dominate the class name.

-  The re-formulations performed in tree building have moved out of the
   "Building" module, into names "ReformulationClasses" e.g., so they
   are easier to locate and review. Helpers for node building are now in
   a separate module, and generally it's much easier to find the content
   of interest now.

-  Added new re-formulation of ``print`` statements. The conversion to
   strings is now made explicit in the node tree.

***********
 New Tests
***********

-  Added test to cover default value identity.

****************
 Organisational
****************

-  The upload of `Nuitka to PyPI
   <http://pypi.python.org/pypi/Nuitka/>`__ has been repaired and now
   properly displays project information again.

*********
 Summary
*********

The quicker release is mostly a consolidation effort, without much
actual performance progress. The progress towards SSA form matter a lot
on the outlook front. Once this is finished, standard compiler
algorithms can be added to Nuitka which go beyond the current peephole
optimization.
