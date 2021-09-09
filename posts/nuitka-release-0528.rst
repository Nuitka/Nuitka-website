This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release has a focus on compatibility work and contains bug fixes
and work to enhance the usability of Nuitka by integrating with
distutils. The major improvement is that contractions no longer use
pseudo functions to achieve their own local scope, but that there is now
a dedicated structure for that representing an in-lined function.

***********
 Bug Fixes
***********

-  Python3.6: Fix, ``async for`` was not yet implemented for async
   generators.

-  Fix, functions with keyword arguments where the value was determined
   to be a static raise could crash the compiler.

-  Detect using MinGW64 32 bits C compiler being used with 64 bits
   Python with better error message.

-  Fix, when extracting side effects of a static raise, extract them
   more recursively to catch expressions that themselves have no code
   generation being used. This fixes at least static raises in keyword
   arguments of a function call.

-  Compatibility: Added support for proper operation of
   ```pkgutil.get_data`` by implementing ``get_data`` in our meta path
   based loader.

-  Compatibility: Added ``__spec__`` module attribute was previously
   missing, present on Python3.4 and higher.

-  Compatibility: Made ``__loader__`` module attribute set when the
   module is loading already.

-  Standalone: Resolve the ``@rpath`` and ``@loader_path`` from
   ``otool`` on macOS manually to actual paths, which adds support for
   libraries compiled with that.

-  Fix, nested functions calling ``super`` could crash the compiler.

-  Fix, could not use ``--recurse-directory`` with arguments that had a
   trailing slash.

-  Fix, using ``--recurse-directory`` on packages that are not in the
   search crashed the compiler.

-  Compatibility: Python2 ``set`` and ``dict`` contractions were using
   extra frames like Python3 does, but those are not needed.

-  Standalone: Fix, the way ``PYTHONHOME`` was set on Windows had no
   effect, which allowed the compiled binary to access the original
   installation still.

-  Standalone: Added some newly discovered missing hidden dependencies
   of extension modules.

-  Compatibility: The name mangling of private names (e.g. ``__var``) in
   classes was applied to variable names, and function declarations, but
   not to classes yet.

-  Python3.6: Fix, added support for list contractions with ``await``
   expressions in async generators.

-  Python3.6: Fix, ``async for`` was not working in async generators
   yet.

-  Fix, for module tracebacks, we output the module name ``<module
   name``> instead of merely ``<module>``, but if the module was in a
   package, that was not indicated. Now it is ``<module package.name>``.

-  Windows: The cache directory could be unicode which then failed to
   pass as an argument to scons. We now encode such names as UTF-8 and
   decode in Scons afterwards, solving the problem in a generic way.

-  Standalone: Need to recursively resolve shared libraries with
   ``ldd``, otherwise not all could be included.

-  Standalone: Make sure ``sys.path`` has no references to CPython
   compile time paths, or else things may work on the compiling machine,
   but not on another.

-  Standalone: Added various missing dependencies.

-  Standalone: Wasn't considering the DLLs directory for standard
   library extensions for freezing, which would leave out these.

-  Compatibility: For ``__future__`` imports the ``__import__`` function
   was called more than once.

**************
 Optimization
**************

-  Contractions are now all properly inlined and allow for optimization
   as if they were fully local. This should give better code in some
   cases.

-  Classes are now all building their locals dictionary inline to the
   using scope, allowing for more compact code.

-  The dictionary API was not used in module template code, although it
   helps to generate more compact code.

**************
 New Features
**************

-  Experimental support for building platform dependent wheel
   distribution.

   .. code:: sh

      python setup.py --command-packages=nuitka.distutils clean -a bdist_nuitka

   Use with caution, this is incomplete work.

-  Experimental support for running tests against compiled installation
   with ``nose`` and ``py.test``.

-  When specifying what to recurse to, now patterns can be used, e.g.
   like this ``--recurse-not-to=*.tests`` which will skip all tests in
   submodules from compilation.

-  By setting ``NUITKA_PACKAGE_packagename=/some/path`` the ``__path__``
   of packages can be extended automatically in order to allow and load
   uncompiled sources from another location. This can be e.g. a
   ``tests`` sub-package or other plug-ins.

-  By default when creating a module, now also a ``module.pyi`` file is
   created that contains all imported modules. This should be deployed
   alongside the extension module, so that standalone mode creation can
   benefit from knowing the dependencies of compiled code.

-  Added option ``--plugin-list`` that was mentioned in the help output,
   but still missing so far.

-  The import tracing of the ``hints`` module has achieved experimental
   status and can be used to test compatibility with regards to import
   behavior.

**********
 Cleanups
**********

-  Rename tree and codegen ``Helper`` modules to unique names, making
   them easier to work with.

-  Share the code that decides to not warn for standard library paths
   with more warnings.

-  Use the ``bool`` enum definition of Python2 which is more elegant
   than ours.

-  Move quality tools, autoformat, isort, etc. to the
   ``nuitka.tools.quality`` namespace.

-  Move output comparison tool to the ``nuitka.tools.testing``
   namespace.

-  Made frame code generation capable of using nested frames, allowing
   the real inline of classes and contraction bodies, instead of
   "direct" calls to pseudo functions being used.

-  Proper base classes for functions that are entry points, and
   functions that are merely a local expression using return statements.

*******
 Tests
*******

-  The search mode with pattern, was not working anymore.
-  Resume hash values now consider the Python version too.
-  Added test that covers using test runners like ``nose`` and
   ``py.test`` with Nuitka compiled extension modules.

****************
 Organizational
****************

-  Added support for Scons 3.0 and running Scons with Python3.5 or
   higher. The option to specify the Python to use for scons has been
   renamed to reflect that it may also be a Python3 now. Only for
   Python3.2 to Python3.4 we now need another Python installation.

-  Made recursion the default for ``--recurse-directory`` with packages.
   Before you also had to tell it to recurse into that package or else
   it would only include the top level package, but nothing below.

-  Updated the man pages, correct mentions of its C++ to C and don't use
   now deprecated options.

-  Updated the help output which still said that standalone mode implies
   recursion into standard library, which is no longer true and even not
   recommended.

-  Added option to disable the output of ``.pyi`` file when creating an
   extension module.

-  Removed Ubuntu Wily package download, no longer supported by Ubuntu.

*********
 Summary
*********

This release was done to get the fixes and new features out for testing.
There is work started that should make generators use an explicit extra
stack via pointer, and restore instruction state via goto dispatchers at
function entry, but that is not complete.

This feature, dubbed "goto generators" will remove the need for fibers
(which is itself a lot of code), reduce the memory footprint at run time
for anything that uses a lot of generators, or coroutines.

Integrating with ``distutils`` is also a new thing, and once completed
will make use of Nuitka for existing projects automatic and trivial to
do. There is a lot missing for that goal, but we will get there.

Also, documenting how to run tests against compiled code, if that test
code lives inside of that package, will make a huge difference, as that
will make it easier for people to torture Nuitka with their own test
cases.

And then of course, nested frames now mean that every function could be
inlined, which was previously not possible due to collisions of frames.
This will pave the route for better optimization in those cases in
future releases.

The experimental features will require more work, but should make it
easier to use Nuitka for existing projects. Future releases will make
integrating Nuitka dead simple, or that is the hope.

And last but not least, now that Scons works with Python3, chances are
that Nuitka will more often work out the of the box. The older Python3
versions that still retain the issue are not very widespread.
