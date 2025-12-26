.. post:: 2024/06/12
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 2.3
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release bumps the long-awaited 3.12 support to a complete level.
Now, Nuitka behaves identically to CPython 3.12 for the most part.

In terms of bug fixes, it's also huge. Especially for Unicode paths and
software with Unicode extension module names and Unicode program names,
and even non-UTF8 code names, there have been massive amounts of
improvements.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

***********
 Bug Fixes
***********

-  Standalone: Added support for ``python-magic-bin`` package. Fixed in
   2.2.1 already.

-  Fix: The cache directory creation could fail when multiple
   compilations started simultaneously. Fixed in 2.2.1 already.

-  macOS: For ``arm64`` builds, DLLs can also have an architecture
   dependent suffix; check that as well. Makes the ``soundfile``
   dependency scan work. Fixed in 2.2.1 already.

-  Fix: Modules where lazy loaders handling adds hard imports when a
   module is first processed did not affect the current module,
   potentially causing it not to resolve hidden imports. Fixed in 2.2.1
   already.

-  macOS: The use of ``libomp`` in ``numba`` needs to cause the
   extension module not to be included and not to look elsewhere. Fixed
   in 2.2.1 already.

-  Python3.6+: Fix, added support for keyword arguments of
   ``ModuleNotFoundError``. Fixed in 2.2.1 already.

-  macOS: Detect more versioned DLLs and ``arm64`` specific filenames.
   Fixed in 2.2.1 already.

-  Fix, was not annotating exception exit when converting an import to a
   hard submodule import. Fixed in 2.2.2 already.

-  Fix, branches that became empty can still have traces that need to be
   merged.

   Otherwise, usages outside the branch will not see propagated
   assignment statements. As a result, these falsely became unassigned
   instead. Fixed in 2.2.2 already.

-  Windows: Fix, uninstalled self-compiled Python didn't have proper
   installation prefix added for DLL scan, resulting in runtime DLLs not
   picked up from there. Fixed in 2.2.2 already.

-  Standalone: Added support for newer ``PySide6`` version 6.7. It
   needed correction on macOS and has a new data file type. Fixed in
   2.2.3 already.

-  Standalone: Complete support for ``pyocd`` package. Fixed in 2.2.3
   already.

-  Module: Fix, the created ``.pyi`` files were incomplete.

   The list of imported modules created in the finalization step was
   incomplete, we now go over the actual done modules and mark all
   non-included modules as dependencies.

-  Scons: Fix, need to avoid using Unicode paths towards the linker on
   Windows. Instead, use a temporary output filename and rename it to
   the actual filename after Scons has completed.

-  Windows: Avoid passing Unicode paths to the dependency walker on
   Windows, as it cannot handle those. Also, the temporary filenames in
   the build folder must be in short paths, as it cannot handle them in
   case that is a Unicode path.

-  Scons: For ``ccache`` on Windows, the log filename must be a short
   path too, if the build folder is a Unicode path.

-  Windows: Make sure the Scons build executes inside a short path as
   well, so that a potential Unicode path is visible to the C compiler
   when resolving the current directory.

-  Windows: The encoding of Unicode paths for accelerated mode values of
   ``__file__`` was not making sure that hex sequences were correctly
   terminated, so in some cases, it produced ambiguous C literals.

-  Windows: Execute binaries created with ``--windows-uac-admin`` with
   and ``--run`` options with proper UAC prompt.

-  Fix, need to allow for non-UTF8 Unicode in variable names, function
   names, class names, and method names.

-  Python3.10+: Fix, ``match`` statements that captured the rest of
   mapping checks were not working yet.

   .. code:: python

      match value:
         case {"key1": 5, **rest}:
            ... # rest was not assigned here

-  Windows: When deleting build folders, make sure the retries leading
   to a complete deletion always.

-  Python2: Fix, could crash with non-``unicode`` program paths on
   Windows.

-  Avoid giving ``SyntaxWarning`` from reading source code

   For example, the standard ``site`` module of Python 3.12 gives
   warnings about illegal escape sequences that nobody cares about
   apparently.

-  Fix, the ``matplotlib`` warnings by ``options-nanny`` were still
   given even if the ``no-qt`` plugin was used, since the variable name
   referenced there was not actually set yet by that plugin.

-  Windows: Fix, when using the uninstalled self-compiled Python, we
   need ``python.exe`` to find DLL dependencies. Otherwise it doesn't
   locate the MSVC runtime and Python DLL properly.

-  Standalone: Added support for ``freetype`` package.

**************
 New Features
**************

-  Support for Python 3.12 is finally there. We focused on scalability
   first and because we did things the correct way immediately, rather
   than rushing to get it working and improving only later.

   As a result, the correctness and performance of **Nuitka** with
   previous Python releases are improved as well.

   Some things got delayed, though. We need to do more work to take
   advantage of other core changes. Concerning exceptions normalized at
   creation time, the created module code doesn't yet take advantage.
   Also, more efficient two-digit long handling is possible with Python
   3.12, but not implemented. It will take more time before we have
   these changes completed.

-  Experimental support for Python 3.13 beta 1 is also there, and
   potentially surprising, but we will try and follow its release cycle
   closely and aim to support it at the time of release.

   **Nuitka** has followed all of its core changes so far, and basic
   tests are passing; the accelerated, module, standalone, and onefile
   modes all work as expected. The only thing delayed is the uncompiled
   generator integration, where we need to replicate the exact CPython
   behavior. We need to have perfect integration only for working with
   the ``asyncio`` loop, so we wait with it until release candidates
   appear.

-  Plugins: Added support to include directories entirely unchanged by
   adding ``raw_dir`` values for ``data-files`` section, see .

-  UI: The new command line option ``--include-raw-dir`` was added to
   allow including directories entirely unchanged.

-  Module: Added support for creating modules with Unicode names. Needs
   a different DLL entry function name and to make use of two-phase
   initialization for the created extension module.

-  Added support for OpenBSD standalone mode.

**************
 Optimization
**************

-  Python3: Avoid API calls for allocators

   Most effective with Python 3.11 or higher but also many other types
   like ``bytes``, ``dict`` keys, ``float``, and ``list`` objects are
   faster to create with all Python3 versions.

-  Python3.5+: Directly use the **Python** allocator functions for
   object creation, avoiding the DLL API calls. The coverage is complete
   with Python3.11 or higher, but many object types like ``float``,
   ``dict``, ``list``, ``bytes`` benefit even before that version.

-  Python3: Faster creation of ``StopIteration`` objects.

   With Python 3.12, the object is created directly and set as the
   current exception without normalization checks.

   We also added a new specialized function to create the exception
   object and populate it directly, avoiding the overhead of calling of
   the ``StopIteration`` type.

-  Python3.10+: When accessing freelists, we were not passing for
   ``tstate`` but locally getting the interpreter object, which can be
   slower by a few percent in some configurations. We now use the free
   lists more efficient with ``tuple``, ``list``, and ``dict`` objects.

-  Python3.8+: Call uncompiled functions via vector calls.

   We avoid an API call that ends up being slower than using the same
   function via the vector call directly.

-  Python3.4+: Avoid using ``_PyObject_LengthHint`` API calls in
   ``list.extend`` and have our variant that is faster to call.

-  Added specialization for ``os.path.normpath``. We might benefit from
   compile time analysis of it once we want to detect file accesses.

-  Avoid using module constants accessor for global constant values

   For example, with ``()``, we used the module-level accessor for no
   reason, as it is already available as a global value. As a result,
   constant blobs shrink, and the compiled code becomes slightly smaller
   , too.

-  Anti-Bloat: Avoid using ``dask`` from the ``sparse`` module. Added in
   2.2.2 already.

****************
 Organizational
****************

-  UI: Major change in console handling.

   Compiled programs on Windows now have a third mode, besides console
   or not. You can now create GUI applications that attach to an
   available console and output there.

   The new option ``--console`` controls this and allows to enforce
   console with the ``force`` value and disable using it with the
   ``disable`` value, the ``attach`` value activates the new behavior.

   .. note::

      Redirection of outputs to a file in ``attach`` mode only works if
      it is launched correctly, for example, interactively in a shell,
      but some forms of invocation will not work; prominently,
      ``subprocess.call`` without inheritable outputs will still output
      to a terminal.

   On macOS, the distinction doesn't exist anymore; technically it
   wasn't valid for a while already; you need to use bundles for
   non-console applications, though, by default otherwise a console is
   forced by macOS itself.

-  Detect ``patchelf`` usage in buggy version ``0.18.0`` and ask the
   user to upgrade or downgrade it, as this specific version is known to
   be broken.

-  UI: Make clear that the ``--nofollow-import-to`` option accepts
   patters.

-  UI: Added warning for module mode and usage of the options to force
   outputs as they don't have any effect.

-  UI: Check the success of Scons in creating the expected binary
   immediately after running it and not only once we reach
   post-processing.

-  UI: Detect empty user package configuration files

-  UI: Do not output module ``ast`` when a plugin reports an error for
   the module, for example, a forbidden import.

-  Actions: Update from deprecated action versions to the latest
   versions.

*******
 Tests
*******

-  Use :ref:`Nuitka Project Options <nuitka-project-options>` for the
   user plugin test rather than passing by environment variables to the
   test runner.

-  Added a new search mode, ``skip``, to complement ``resume`` which
   resumes right after the last test ``resume`` stopped on. We can use
   that while support for a Python version is not complete.

**********
 Cleanups
**********

-  Solved a TODO about using unified code for setting the
   ``StopIteration``, coroutines, generators, and asyncgen used to be
   different.

-  Unified how the binary result filename is passed to Scons for modules
   and executables to use the same ``result_exe`` key.

*********
 Summary
*********

This release marks a huge step in catching up with compatibility of
Python. After being late with 3.12 support, we will now be early with
3.13 support if all goes well.

The many Unicode support related changes also enhanced Nuitka to
generate 2 phase loading extension modules, which also will be needed
for sub-interpreter support later on.

From here on, we need to re-visit compatibility. A few more obscured
3.10 features are missing, the 3.11 compatibility is not yet complete,
and we need to take advantage of the new caching possibilities to
enhance performance for example with attribute lookups to where it can
be with the core changes there.

For the coming releases until 3.13 is released, we hope to focus on
scalability a lot more and get a much needed big improvement there, and
complete these other tasks on the side.
