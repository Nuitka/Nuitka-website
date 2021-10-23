This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release contains huge amounts of crucial bug fixes all across the
board. There is also new optimization and many organisational
improvements.

***********
 Bug Fixes
***********

-  Fix, the top level module must not be bytecode. Otherwise we end up
   violating the requirement for an entry point on the C level.

-  Fix, avoid optimizing calls with default values used. This is not yet
   working and needed to be disabled for now.

-  Python3: Fix, missing keyword only arguments were not enforced to be
   provided keyword only, and were not giving the compatible error
   message when missing.

-  Windows: Find ``win32com`` DLLs too, even if they live in sub folders
   of site-packages, and otherwise not found. They are used by other
   DLLs that are found.

-  Standalone: Fixup for problem with standard library module in most
   recent Anaconda versions.

-  Scons: Fix, was using ``CXXFLAGS`` and ``CPPFLAGS`` even for the C
   compiler, which is wrong, and could lead to compilation errors.

-  Windows: Make ``--clang`` limited to ``clang-cl.exe`` as using it
   inside a MinGW64 is not currently supported.

-  Standalone: Added support for using ``lib2to2.pgen``.

-  Standalone: Added paths used by openSUSE to the Tcl/Tk plugin.

-  Python3.6+: Fix, the ``__main__`` package was ``None``, but should be
   ``""`` which allows relative imports from itself.

-  Python2: Fix, compile time optimization of floor division was using
   normal division.

-  Python3: Fix, some run time operations with known type shapes, were
   falsely reporting error message with ``unicode`` or ``long``, which
   is of course not compatible.

-  Fix, was caching parent package, but these could be replaced e.g. due
   to bytecode demotion later, causing crashes during their
   optimization.

-  Fix, the value of ``__compiled__`` could be corrupted when being
   deleted, which some modules wrappers do.

-  Fix, the value of ``__package__`` could be corrupted when being
   deleted.

-  Scons: Make sure we can always output the compiler output, even if it
   has a broken encoding. This should resolve MSVC issues on non-English
   systems, e.g. German or Chinese.

-  Standalone: Support for newest ``sklearn`` was added.

-  macOS: Added resolver for run time variables in ``otool`` output,
   that gets PyQt5 to work on it again.

-  Fix, floor division of run time calculations with float values should
   not result in ``int``, but ``float`` values instead.

-  Standalone: Enhanced support for ``boto3`` data files.

-  Standalone: Added support for ``osgeo`` and ``gdal``.

-  Windows: Fix, there were issues with spurious errors attaching the
   constants blob to the binary due to incorrect C types provided.

-  Distutils: Fix, need to allow ``/`` as separator for package names
   too.

-  Python3.6+: Fix reference losses in asyncgen when throwing exceptions
   into them.

-  Standalone: Added support for ``dill``.

-  Standalone: Added support for ``scikit-image`` and ``skimage``.

-  Standalone: Added support for ``weasyprint``.

-  Standalone: Added support for ``dask``.

-  Standalone: Added support for ``pendulum``.

-  Standalone: Added support for ``pytz`` and ``pytzdata``.

-  Fix, ``--python-flags=no_docstrings`` no longer implies disabling the
   assertions.

**************
 New Features
**************

-  Added experimental support for Python 3.8, there is only very few
   things missing for full support.

-  Distutils: Added support for packages that are in a namespace and not
   just top level.

-  Distutils: Added support for single modules, not only packages, by
   supporting ``py_modules`` as well.

-  Distutils: Added support for distinct namespaces.

-  Windows: Compare Python and C compiler architecture for MSVC too, and
   catch the most common user error of mixing 32 and 64 bits.

-  Scons: Output variables used from the outside, so the debugging is
   easier.

-  Windows: Detect if clang installed inside MSVC automatically and use
   it if requested via ``--clang`` option. This is only the 32 bits
   variant, but currently the easy way to use it on Windows with Nuitka.

**************
 Optimization
**************

-  Loop variables were analysed, but results were only available on the
   inside of the loop, preventing many optimization in these cases.

-  Added optimization for the ``abs`` built-in, which is also a
   numerical operator.

-  Added optimization for the ``all`` built-in, adding a new concept of
   iteration handle, for efficient checking that avoids looking at very
   large sequences, of which properties can still be known.

   .. code:: python

      all(range(1, 100000))  # no need to look at all of them

-  Added support for optimizing ``ImportError`` construction with
   keyword-only arguments. Previously only used without these were
   optimized.

   .. code:: python

      raise ImportError(path="lala", name="lele")  # now optimized

-  Added manual specialization for single argument calls, sovling a
   TODO, as these will be very frequent.

-  Memory: Use single child form of node class where possible, the
   general class now raises an error if used with used with only one
   child name, this will use less memory at compile time.

-  Memory: Avoid list for non-local declarations in every function,
   these are very rare, only have it if absolutely necessary.

-  Generate more compact code for potential ``NameError`` exceptions
   being raised. These are very frequent, so this improves scalability
   with large files.

-  Python2: Annotate comparison of ``None`` with ``int`` and ``str``
   types as not raising an exception.

-  Shared empty body functions and generators.

   One shared implementation for all empty functions removes that burden
   from the C compiler, and from the CPU instruction cache. All the
   shared C code does is to release its arguments, or to return an empty
   generator function in case of generator.

-  Memory: Added support for automatic releases of parameter variables
   from the node tree. These are normally released in a try finally
   block, however, this is now handled during code generation for much
   more compact C code generated.

-  Added specialization for ``int`` and ``long`` operations ``%``,
   ``<<``, ``>>``, ``|``, ``&``, ``^``, ``**``, ``@``.

-  Added dedicated nodes for representing and optimizing based on shapes
   for all binary operations.

-  Disable gcc macro tracing unless in debug mode, to save memory during
   the C compilation.

-  Restored Python2 fast path for ``int`` with unknown object types,
   restoring performance for these.

**********
 Cleanups
**********

-  Use dedicated ``ModuleName`` type that makes the tests that check if
   a given module name is inside a namespace as methods. This was hard
   to get right and as a result, adopting this fixed a few bugs and or
   inconsistent results.

-  Expand the use of ``nuitka.PostProcessing`` to cover all actions
   needed to get a runnable binary. This includes using
   ``install_name_tool`` on macOS standalone, as well copying the Python
   DLL for acceleration mode, cleaning the ``x`` bit for module mode.
   Previously only a part of these lived there.

-  Avoid including the definitions of dynamically created helper
   functions in the C code, instead just statically declare the ones
   expected to be there. This resolves Visual Code complaining about it,
   and should make life also easier for the compiler and caches like
   ``ccache``.

-  Create more helper code in closer form to what ``clang-format`` does,
   so they are easier to compare to the static forms. We often create
   hard coded variants for few arguments of call functions, and generate
   them for many argument variations.

-  Moved setter/getter methods for Nuitka nodes consistently to the
   start of the node class definitions.

-  Generate C code much closer to what ``clang-format`` would change it
   to be.

-  Unified calling ``install_name_tool`` on macOS into one function that
   takes care of all the things, including e.g. making the file
   writable.

-  Debug output from scons should be more consistent and complete now.

-  Sort files for compilation in scons for better reproducible results.

-  Create code objects version independent, avoiding python version
   checks by pre-processor, hiding new stuff behind macros, that ignore
   things on older Python versions.

*******
 Tests
*******

-  Added many more built-in tests for increased coverage of the newly
   covered ones, some of them being generic tests that allow to test all
   built-ins with typical uses.

-  Many tests have become more PyLint clean as a result of work with
   Visual Code and it complaining about them.

-  Added test to check PyPI health of top 50 packages. This is a major
   GSoC 2019 result.

-  Output the standalone directory contents for Windows too in case of a
   failure.

-  Added generated tests to fully cover operations on different type
   shapes and their errors as well as results for typical values.

-  Added support for testing against installed version of Nuitka.

-  Cleanup up tests, merging those for only Python 3.2 with 3.3 as we no
   longer support that version anyway.

-  Execute the Python3 tests for macOS on Travis too.

****************
 Organisational
****************

-  The donation sponsored machine called ``donatix`` had to be replaced
   due to hardware breakage. It was replaced with a Raspberry-Pi 4.

-  Enhanced plugin documentation.

-  Added description of the git workflow to the Developer Manual.

-  Added checker script ``check-nuitka-with-codespell`` that reports
   typos in the source code for easier use of ``codespell`` with Nuitka.

-  Use newest PyLint and clang-format.

-  Also check plugin documentation files for ReST errors.

-  Much enhanced support for Visual Code configuration.

-  Trigger module code is now written into the build directory in debug
   mode, to aid debugging.

-  Added deep check function that descends into tuples to check their
   elements too.

*********
 Summary
*********

This release comes after a long time of 4 months without a release, and
has accumulated massive amounts of changes. The work on CPython 3.8 is
not yet complete, and the performance work has yet to show actual fruit,
but has also progressed on all fronts. Connecting the dots and pieces
seems not far away.
