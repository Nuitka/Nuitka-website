This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release is mostly the result of working towards compilation of a
real programs (Mercurial) and to merge and finalize the frame stack
work. Now Nuitka has a correct frame stack at all times, and supports
``func_code`` and ``gi_code`` objects, something previously thought to
be impossible.

Actually now it's only the "bytecode" objects that won't be there. And
not attributes of ``func_code`` are meaningful yet, but in theory can be
supported.

Due to the use of the "git flow" for Nuitka, most of the bugs listed
here were already fixed in on the stable release before this release.
This time there were 5 such hot fix releases, sometimes fixing multiple
bugs.

###########
 Bug fixes
###########

-  In case of syntax errors in the main program, an exception stack was
   giving that included Nuitka code. Changed to make the same output as
   CPython does. Fixed in 0.3.12a already.

-  The star import (``from x import *``) didn't work for submodules.
   Providing ``*`` as the import list to the respective code allowed to
   drop the complex lookups we were doing before, and to simply trust
   CPython C/API to do it correctly. Fixed in 0.3.12 already.

-  The absolute import is *not* the default of CPython 2.7 it seems. A
   local ``posix`` package shadows the standard library one. Fixed in
   0.3.12 already.

-  In ``--deep`` mode, a module may contain a syntax error. This is e.g.
   true of "PyQt" with ``port_v3`` included. These files contain Python3
   syntax and fail to be imported in Python2, but that is not to be
   considered an error. These modules are now skipped with a warning.
   Fixed in 0.3.12b already.

-  The code to import modules wasn't using the ``__import__`` built-in,
   which prevented ``__import__`` overriding code to work. Changed
   import to use the built-in. Fixed in 0.3.12c already.

-  The code generated for the ``__import__`` built-in with constant
   values was doing relative imports only. It needs to attempt relative
   and absolute imports. Fixed in 0.3.12c already.

-  The code of packages in "__init__.py" believed it was outside of the
   package, giving problems for package local imports. Fixed in 0.3.12d
   already.

-  It appears that "Scons", which Nuitka uses internally and transparent
   to you, to execute the compilation and linking tasks, was sometimes
   not building the binaries or shared libraries, due to a false
   caching. As a workaround, these are now erased before doing the
   build. Fixed in 0.3.12d already.

-  The use of ``in`` and ``not in`` in comparison chains (e.g. ``a < b <
   c`` is one), wasn't supported yet. The use of these in comparison
   chains ``a in b in c`` is very strange.

   Only in the ``test_grammar.py`` it was ever used I believe. Anyway,
   it's supported now, solving this ``TODO`` and reducing the
   difference. Fixed in 0.3.12e already.

-  The order of evaluation for ``in`` and ``not in`` operators wasn't
   enforced in a portable way. Now it is correct on "ARM" too. Fixed in
   0.3.12e already.

##############
 Optimization
##############

-  The built-ins ``GeneratorExit`` and ``StopIteration`` are optimized
   to their Python C/API names where possible as well.

##########
 Cleanups
##########

-  The ``__file__`` attribute of modules was the relative filename, but
   for absolute filenames these become a horrible mess at least on
   Linux.

-  Added assertion helpers for sane frame and code objects and use them.

-  Make use of ``assertObject`` in more places.

-  Instead of using ``os.path.sep`` all over, added a helper
   ``Utils.joinpath`` that hides this and using ``os.path.join``. This
   gives more readable code.

-  Added traces to the "unfreezer" guarded by a define. Helpful in
   analyzing import problems.

-  Some PyLint cleanups removing dead code, unused variables, useless
   pass statement, etc.

###########
 New Tests
###########

-  New tests to cover ``SyntaxError`` and ``IndentationError`` from
   ``--deep`` imports and in main program.

-  New test to cover evaluation order of ``in`` and ``not in``
   comparisons.

-  New test to cover package local imports made by the "__init__.py" of
   the package.

################
 Organisational
################

-  Drop "compile_itself.sh" in favor of the new "compile_itself.py",
   because the later is more portable.

-  The logging output is now nicer, and for failed recursions, outputs
   the line that is having the problem.

#########
 Summary
#########

The frame stack work and the ``func_code`` are big for compatibility.

The ``func_code`` was also needed for "hg" to work. For Mercurial to
pass all of its test suite, more work will be needed, esp. the
``inspect`` module needs to be run-time patched to accept compiled
functions and generators too.

Once real world programs like Mercurial work, we can use these as more
meaningful benchmarks and resume work on optimization.
