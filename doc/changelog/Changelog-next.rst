:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per-version changes and comments for the
upcoming Nuitka |NUITKA_VERSION_NEXT| as a draft about hot-fixes of the
current stable release as |NUITKA_VERSION| as well.

****************************
 Nuitka Release 2.3 (Draft)
****************************

.. note::

   This a draft of the release notes for 2.3, which is supposed to add
   Python 3.12 support, and the usual additions of new packages
   supported out of the box and will also aim at scalability if
   possible.

This release bumps the long-awaited 3.12 support to a complete level.
This means Nuitka now behaves identically to CPython 3.12 for the
largest part.

In terms of bug fixes, it's also huge. Especially for Unicode paths and
software with Unicode extension module names and Unicode program names,
and even non-UTF8 code names, there have been massive amounts of
improvements.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

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

-  Fix, was not annotating exception exit when converting import to hard
   submodule import. Fixed in 2.2.2 already.

-  Fix, branches that became empty still need to be merged.

   Otherwise, propagated assignment statements will not be seen by
   usages outside the branch and become unassigned instead. Fixed in
   2.2.2 already.

-  Windows: Fix, uninstalled self-compiled Python didn't have proper
   installation prefix added for DLL scan, resulting in runtime DLLs not
   picked up from there. Fixed in 2.2.2 already.

-  Standalone: Added support for newer ``PySide6`` version 6.7, needed
   correction on macOS and has new kind of data files. Fixed in 2.2.3
   already.

-  Standalone: More complete support for ``pyocd`` package. Fixed in
   2.2.3 already.

-  Module: Fix, the create ``.pyi`` files were incomplete.

   The list of imported modules created in the finalization step was
   incomplete, we now go over the actual done modules and mark all
   non-included modules as dependencies.

-  Scons: Fix, need to avoid using Unicode paths towards the linker on
   Windows. Instead, use a temporary output filename and correct it by
   renaming after Scons has completed.

-  Windows: Avoid passing Unicode paths to the dependency walker on
   Windows, as it cannot handle those. Also, the temporary filenames in
   the build folder must be short filenames, as it cannot handle them in
   case that is a Unicode path.

-  Scons: For ``ccache`` on Windows, the log filename must be short path
   too, if the build folder is a Unicode path.

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

New Features
============

-  Support for Python 3.12 is finally there. We focused on scalability
   first and because we did things the correct way immediately, rather
   than rushing to get it working and improving only later.

   As a result, the correctness and performance with previous Python
   releases is improved as well.

   Some things got delayed, though. We need to do more work to take
   advantage of other core changes. Concerning exceptions normalized at
   creation time, the created module code doesn't take advantage at all
   yet. Also, more efficient two-digit long handling is possible with
   Python 3.12, but not implemented. These are both changes that will
   take some time, but they are still before we have them.

-  Plugins: Added support to include directories entirely unchanged by
   adding ``raw_dir`` values for ``data-files`` section, see
   :doc:`Nuitka Package Configuration
   </user-documentation/nuitka-package-config>`.

-  UI: The new command line option ``--include-raw-dir`` was added to
   allow including directories entirely unchanged.

-  Module: Added support for creating modules with Unicode names. Needs
   a different DLL entry function name and to make use of two phase
   initialization for the created extension module.

Optimization
============

-  Python3: Avoid API calls for allocators

   This is most effective with Python 3.11 or higher but also many other
   types like ``bytes``, ``dict`` keys, ``float`` objects, and ``list``
   are faster to create with all Python3 versions.

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

-  Python3.8+: Call uncompiled functions via vector calls.

   We avoid an API call that ends up being slower than using the same
   function via the vector call directly.

-  Added specialization for ``os.path.normpath``. We might benefit from
   compile time analysis of it once we want to detect file accesses.

-  Avoid using module constants accessor for global constant values

   For example, with ``()`` we used the module-level accessor for no
   reason, as it is already available as a global value. As a result
   constant blobs shrink, and the compiled code becomes slightly smaller
   as well.

-  Anti-Bloat: Avoid using ``dask`` from the ``sparse`` module. Added in
   2.2.2 already.

Organizational
==============

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
   non-console applications though, by default otherwise a console is
   forced by macOS itself.

-  Detect ``patchelf`` usage in buggy version ``0.18.0`` and ask the
   user to upgrade or downgrade it, as this specific version is known to
   be broken.

-  UI: Make clear that the ``--nofollow-import-to`` option accepts
   patters.

-  UI: Added warning for module mode and usage of the options to force
   outputs as they don't have any effect.

-  UI: Check the success of Scons in creating the expected binary
   immediately after running it and not only in post-processing which is
   late.

Tests
=====

-  Use :ref:`Nuitka Project Options <nuitka-project-options>` for the
   user plugin test rather than passing by environment variables to the
   test runner.

Cleanups
========

-  Solved a TODO about using unified code for setting the
   ``StopIteration``, coroutines, generators and asyncgen used to be
   different.

-  Unified how the result filename is passed to Scons for modules and
   executables to use the same ``result_exe`` key.

Summary
=======

This release is not yet done.

.. include:: ../dynamic.inc
