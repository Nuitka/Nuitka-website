.. post:: 2011/01/22 14:52
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.3.5
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This new release of Nuitka is an overall improvement on many fronts,
there is no real focus this time, likely due to the long time it was in
the making.

The major points are more optimization work, largely enhanced import
handling and another improvement on the performance side. But there are
also many bug fixes, more test coverage, usability and compatibility.

Something esp. noteworthy to me and valued is that many important
changes were performed or at least triggered by Nicolas Dumazet, who
contributed a lot of high quality commits as you can see from the gitweb
history. He appears to try and compile Mercurial and Nuitka, and this
resulted in important contributions.

***********
 Bug fixes
***********

-  Nicolas found a reference counting bug with nested parameter calls.
   Where a function had parameters of the form ``a, (b,c)`` it could
   crash. This got fixed and covered with a reference count test.

-  Another reference count problem when accessing the locals dictionary
   was corrected.

-  Values ``0.0`` and ``-0.0`` were treated as the same. They are not
   though, they have a different sign that should not get lost.

-  Nested contractions didn't work correctly, when the contraction was
   to iterate over another contraction which needs a closure. The
   problem was addressing by splitting the building of a contraction
   from the body of the contraction, so that these are now 2 nodes,
   making it easy for the closure handling to get things right.

-  Global statements in function with local ``exec()`` would still use
   the value from the locals dictionary. Nuitka is now compatible to
   CPython with this too.

-  Nicolas fixed problems with modules of the same name inside different
   packages. We now use the full name including parent package names for
   code generation and look-ups.

-  The ``__module__`` attribute of classes was only set after the class
   was created. Now it is already available in the class body.

-  The ``__doc__`` attribute of classes was not set at all. Now it is.

-  The relative import inside nested packages now works correctly. With
   Nicolas moving all of Nuitka to a package, the compile itself exposed
   many weaknesses.

-  A local re-raise of an exception didn't have the original line
   attached but the re-raise statement line.

**************
 New Features
**************

-  Modules and packages have been unified. Packages can now also have
   code in "__init__.py" and then it will be executed when the package
   is imported.

-  Nicolas added the ability to create deep output directory structures
   without having to create them beforehand. This makes
   ``--output-dir=some/deep/path`` usable.

-  Parallel build by Scons was added as an option and enabled by
   default, which enhances scalability for ``--deep`` compilations a
   lot.

-  Nicolas enhanced the CPU count detection used for the parallel build.
   Turned out that ``multithreading.cpu_count()`` doesn't give us the
   number of available cores, so he contributed code to determine that.

-  Support for upcoming g++ 4.6 has been added. The use of the new
   option ``--lto`` has been been prepared, but right now it appears
   that the C++ compiler will need more fixes, before we can this
   feature with Nuitka.

-  The ``--display-tree`` feature got an overhaul and now displays the
   node tree along with the source code. It puts the cursor on the line
   of the node you selected. Unfortunately I cannot get it to work
   two-way yet. I will ask for help with this in a separate posting as
   we can really use a "python-qt" expert it seems.

-  Added meaningful error messages in the "file not found" case.
   Previously I just didn't care, but we sort of approach end user
   usability with this.

**************
 Optimization
**************

-  Added optimization for the built-in ``range()`` which otherwise
   requires a module and ``builtin`` module lookup, then parameter
   parsing. Now this is much faster with Nuitka and small ranges (less
   than 256 values) are converted to constants directly, avoiding run
   time overhead entirely.

-  Code for re-raise statements now use a simple re-throw of the
   exception where possible, and only do the hard work where the
   re-throw is not inside an exception handler.

-  Constant folding of operations and comparisons is now performed if
   the operands are constants.

-  Values of some built-ins are pre-computed if the operands are
   constants.

-  The value of module attribute ``__name__`` is replaced by a constant
   unless it is assigned to. This is the first sign of upcoming constant
   propagation, even if only a weak one.

-  Conditional statement and/or their branches are eliminated where
   constant conditions allow it.

**********
 Cleanups
**********

-  Nicolas moved the Nuitka source code to its own ``nuitka`` package.
   That is going to make packaging it a lot easier and allows cleaner
   code.

-  Nicolas introduced a fast path in the tree building which often
   delegates (or should do that) to a function. This reduced a lot of
   the dispatching code and highlights more clearly where such is
   missing right now.

-  Together we worked on the line length issues of Nuitka. We agreed on
   a style and very long lines will vanish from Nuitka with time. Thanks
   for pushing me there.

-  Nicolas also did provide many style fixes and general improvements,
   e.g. using ``PyObjectTemporary`` in more places in the C++ code, or
   not using ``str.find`` where ``x in y`` is a better choice.

-  The node structure got cleaned up towards the direction that
   assignments always have an assignment as a child.

   A function definition, or a class definition, are effectively
   assignments, and in order to not have to treat this as special cases
   everywhere, they need to have assignment targets as child nodes.

   Without such changes, optimization will have to take too many things
   into account. This is not yet completed.

-  Nicolas merged some node tree building functions that previously
   handled deletion and assigning differently, giving us better code
   reuse.

-  The constants code generation was moved to a ``__constants.cpp``
   where it doesn't make __main__.cpp so much harder to read anymore.

-  The module declarations have been moved to their own header files.

-  Nicolas cleaned up the scripts used to test Nuitka big time, removing
   repetitive code and improving the logic. Very much appreciated.

-  Nicolas also documented a things in the Nuitka source code or got me
   to document things that looked strange, but have reasons behind it.

-  Nicolas solved the ``TODO`` related to built-in module accesses.
   These will now be way faster than before.

-  Nicolas also solved the ``TODO`` related to the performance of
   "locals dict" variable accesses.

-  Generator.py no longer contains classes. The Contexts objects are
   supposed to contain the state, and as such the generator objects
   never made much sense.

-  Also with the help of Scons community, I figured out how to avoid
   having object files inside the ``src`` directory of Nuitka. That
   should also help packaging, now all build products go to the .build
   directory as they should.

-  The vertical white space of the generated C++ got a few cleanups,
   trailing/leading new line is more consistent now, and there were some
   assertions added that it doesn't happen.

***********
 New Tests
***********

-  The CPython 2.6 tests are now also run by CPython 2.7 and the other
   way around and need to report the same test failure reports, which
   found a couple of issues.

-  Now the test suite is run with and without ``--debug`` mode.

-  Basic tests got extended to cover more topics and catch more issues.

-  Program tests got extended to cover code in packages.

-  Added more exec scope tests. Currently inlining of exec statements is
   disabled though, because it requires entirely different rules to be
   done right, it has been pushed back to the next release.

****************
 Organisational
****************

-  The ``g++-nuitka`` script is no more. With the help of the Scons
   community, this is now performed inside the scons and only once
   instead of each time for every C++ file.

-  When using ``--debug``, the generated C++ is compiled with ``-Wall``
   and ``-Werror`` so that some form of bugs in the generated C++ code
   will be detected immediately. This found a few issues already.

-  There is a new git merge policy in place. Basically it says, that if
   you submit me a pull request, that I will deal with it before
   publishing anything new, so you can rely on the current git to
   provide you a good base to work on. I am doing more frequent
   pre-releases already and I would like to merge from your git.

-  The "README.txt" was updated to reflect current optimization status
   and plans. There is still a lot to do before constant propagation can
   work, but this explains things a bit better now. I hope to expand
   this more and more with time.

-  There is now a "misc/clean-up.sh" script that prints the commands to
   erase all the temporary files sticking around in the source tree.

   That is for you if you like me, have other directories inside,
   ignored, that you don't want to delete.

-  Then there is now a script that prints all source filenames, so you
   can more easily open them all in your editor.

-  And very important, there is now a "check-release.sh" script that
   performs all the tests I think should be done before making a
   release.

-  Pylint got more happy with the current Nuitka source. In some places,
   I added comments where rules should be granted exceptions.

*********
 Numbers
*********

python 2.6:

.. code::

   Pystone(1.1) time for 50000 passes = 0.65
   This machine benchmarks at 76923.1 pystones/second

Nuitka 0.3.5 (driven by python 2.6):

.. code::

   Pystone(1.1) time for 50000 passes = 0.31
   This machine benchmarks at 161290 pystones/second

This is 109% for 0.3.5, up from 91% before.

Overall this release is primarily an improvement in the domain of
compatibility and contains important bug and feature fixes to the users.
The optimization framework only makes a first showing of with the
framework to organize them. There is still work to do to migrate
optimization previously present

It will take more time before we will see effect from these. I believe
that even more cleanups of ``TreeBuilding``, ``Nodes`` and
``CodeGeneration`` will be required, before everything is in place for
the big jump in performance numbers. But still, passing 100% feels good.
Time to rejoice.
