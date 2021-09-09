This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release has improvements in all areas. Many bug fixes are
accompanied with optimization changes towards value tracing.

***********
 Bug Fixes
***********

-  Fix, the new setuptools runners were not used by ``pip`` breaking the
   use of Nuitka from PyPI.

-  Fix, imports of ``six.moves`` could crash the compiler for built-in
   names. Fixed in 0.5.29.2 already.

-  Windows: Make the ``nuitka-run`` not a symlink as these work really
   bad on that platform, instead make it a full copy just like we did
   for ``nuitka3-run`` already. Fixed in 0.5.29.2 already.

-  Python3.5: In module mode, ``types.coroutine`` was monkey patched
   into an endless recursion if including more than one module, e.g. for
   a package. Fixed in 0.5.29.3 already.

-  Python3.5: Dictionary unpackings with both star arguments and non
   star arguments could leak memory. Fixed in 0.5.29.3 already.

   .. code:: python

      c = {a: 1, **d}

-  Fix, distutils usage was not working for Python2 anymore, due to
   using ``super`` for what are old style classes on that version.

-  Fix, some method calls to C function members could leak references.

   .. code:: python

      class C:
          for_call = functools.partial

          def m(self):
              self.for_call()  # This leaked a reference to the descriptor.

-  Python3.5: The bases classes should be treated as an unpacking too.

   .. code:: python

      class C(*D):  # Allowed syntax that was not supported.
          pass

-  Windows: Added back batch files to run Nuitka from the command line.
   Fixed in 0.5.29.5 already.

**************
 New Features
**************

-  Added option ``--include-package`` to force inclusion of a whole
   package with the submodules in a compilation result.

-  Added options ``--include-module`` to force inclusion of a single
   module in a compilation result.

-  The ```multiprocessing`` plug-in got adapted to Python 3.4 changes
   and will now also work in accelerated mode on Windows.

-  It is now possible to specify the Qt plugin directories with e.g.
   ``--plugin-enable-=qt_plugins=imageformats`` and have only those
   included. This should avoid dependency creep for shared libraries.

-  Plugins can now make the decision about recursing to a module or not.

-  Plugins now can get their own options passed.

**************
 Optimization
**************

-  The re-raising of exceptions has gotten its own special node type.
   This aims at more readability (XML output) and avoiding the overhead
   of checking potential attributes during optimization.

-  Changed built-in ``int``, ``long``, and ``float`` to using a slot
   mechanism that also analyses the type shape and detects and warns
   about errors at compile time.

-  Changed the variable tracing to value tracing. This meant to cleanup
   all the places that were using it to find the variable.

-  Enable must have / must not value value optimization for all kinds of
   variables including module and closure variables. This often avoids
   error exits and leads to smaller and faster generated code.

*******
 Tests
*******

-  Added burn test with local install of pip distribution to virtualenv
   before making any PyPI upload. It seems pip got its specific error
   sources too.

-  Avoid calling ``2to3`` and prefer ``<python> -m lib2to3`` instead, as
   it seems at least Debian Testing stopped to provide the binary by
   default. For Python 2.6 and 3.2 we continue to rely on it, as the
   don't support that mode of operation.

-  The PyLint checks have been made more robust and even more Python3
   portable.

-  Added PyLint to Travis builds, so PRs are automatically checked too.

-  Added test for distutils usage with Nuitka that should prevent
   regressions for this new feature and to document how it can be used.

-  Make coverage taking work on Windows and provide the full information
   needed, the rendering stage is not there working yet though.

-  Expanded the trick assignment test cases to cover more slots to find
   bugs introduced with more aggressive optimization of closure
   variables.

-  New test to cover multiprocessing usage.

-  Generating more code tests out of doctests for increased coverage of
   Nuitka.

**********
 Cleanups
**********

-  Stop using ``--python-version`` in tests where they still remained.

-  Split the forms of ``int`` and ``long`` into two different nodes,
   they share nothing except the name. Create the constants for the zero
   arg variant more immediately.

-  Split the output comparison part into a dedicated testing module so
   it can be re-used, e.g. when doing distutils tests.

-  Removed dead code from variable closure taking.

-  Have a dedicated module for the metaclass of nodes in the tree, so it
   is easier to find, and doesn't clutter the node base classes module
   as much.

-  Have a dedicated node for reraise statements instead of checking for
   all the arguments to be non-present.

****************
 Organizational
****************

-  There is now a pull request template for Github when used.

-  Deprecating the ``--python-version`` argument which should be
   replaced by using ``-m nuitka`` with the correct Python version.
   Outputs have been updated to recommend this one instead.

-  Make automatic import sorting and autoformat tools properly
   executable on Windows without them changing new lines.

-  The documentation was updated to prefer the call method with ``-m
   nuitka`` and manually providing the Python binary to use.

*********
 Summary
*********

This release continued the distutils integration adding first tests, but
more features and documentation will be needed.

Also, for the locals dictionary work, the variable tracing was made
generic, but not yet put to use. If we use this to also trace dictionary
keys, we can expect a lot of improvements for class code again.

The locals dictionary tracing will be the focus before resuming the work
on C types, where the ultimate performance boost lies. However,
currently, not the full compatibility has been achieved even with
currently using dictionaries for classes, and we would like to be able
to statically optimize those better anyway.
