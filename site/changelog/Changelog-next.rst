:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

This document outlines the changes for the upcoming **Nuitka**
|NUITKA_VERSION_NEXT| release, serving as a draft changelog. It also
includes details on hot-fixes applied to the current stable release,
|NUITKA_VERSION|.

It currently covers changes up to version **4.3rc2**.

**************************************************
 **Nuitka** Release |NUITKA_VERSION_NEXT| (Draft)
**************************************************

.. note::

   These are the draft release notes for the upcoming **Nuitka**
   |NUITKA_VERSION_NEXT| release. A primary goal for this version is to
   improve Python 3.15 support, with work planned on frame locals
   proxies as in Python 3.13, optimization of iterator unpacking, and
   inlining of generator expressions. Development is ongoing, and this
   documentation might lag slightly behind the latest code changes.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  Fix, comparisons and add or subtract operations of Python ``long``
   values with C ``long`` operands could produce wrong results. (Fixed
   in 4.2.1 already.)

-  **Python 3.14:** Fix, deferred annotations did not work with hard
   import names, e.g. ``io.BytesIO``, since those were unnecessarily
   generated as ``__import__`` calls. (Fixed in 4.2.1 already.)

-  **Python 3.14:** Fix, the
   ``--devel-no-bytecode-to-compiled-fallback`` option was not honored
   when source generation for an ``__annotate__`` function failed, where
   the fallback to compiled code happened anyway. (Fixed in 4.2.1
   already.)

-  **Python 3.14:** Fix, source generation for ``__annotate__``
   functions did not handle closures, constants, and calls correctly.
   Closure variables were then rejected to fall back to compiled code,
   and values like non-finite floats, empty sets, and types from modules
   are rendered as valid source. (Fixed in 4.2.1 already.)

-  **Plugins:** Fix, nested uses of the ``forkserver`` context were not
   working. (Fixed in 4.2.1 already.)

-  **Compatibility:** Fix, conditional expressions did not decide their
   type shapes from the branches properly, which could lead to wrong
   optimization of list appends and subscript operations. (Fixed in
   4.2.2 already.)

-  **Compatibility:** Fix, keyword arguments created from ``str``
   subclass instances were rejected, since the check compared the exact
   type instead of allowing subclasses. (Fixed in 4.2.2 already.)

-  **Windows:** Fix, MSYS2 builds now link the compiler runtime
   statically, avoiding a runtime dependency on e.g.
   ``libwinpthread-1.dll``, which also fixes module mode requiring that
   DLL. (Fixed in 4.2.2 already.)

-  **MSYS2:** Fix, adapting Python header files did not work on that
   flavor yet. (Fixed in 4.2.2 already.)

-  **macOS:** Fix, newer Xcode versions only ship tools like
   ``install_name_tool``, ``lipo``, ``nm``, and ``otool`` as ARM64
   binaries, which fail to run in an ``x86_64`` translated process.
   These are now invoked with ``arch -arm64`` as needed, and the same
   for the C compiler and ``ccache``. (Fixed in 4.2.2 already.)

-  **Debian:** Fix, onefile mode was no longer usable when the ``zstd``
   inline copy is absent, e.g. in the official Debian package, since the
   system ``zstd`` and ``zlib`` are now linked statically instead.
   (Fixed in 4.2.2 already.)

-  **Installer:** Fix, Linux installer creation crashed in onefile mode,
   now informs the user that ``--mode=app-dist`` (or
   ``--mode=standalone``) mode is required. (Fixed in 4.2.2 already.)

-  Fix, when outline functions were removed, e.g. class bodies that
   raise, the variable tracing was not undone, so the value traces could
   be inconsistent, this is now reversed properly.

-  Fix, cloned outline functions did not copy the variables they take
   from the enclosing scope, so the clones could lack closure variables.

-  Fix, the context manager for directory changes only restored the
   previous directory on success, now it does so also on errors, which
   the ``nuitka-watch`` tool depends on.

-  **Python 3.12+:** Fix, the ``__bound__`` of type variables was always
   ``None``, since the bound was not used when creating them.

-  **Python 3.15:** Fix, the ``_math_integer`` extension module was
   missing from the standard library modules known to never raise on
   import, which prevented optimizing its imports.

-  **Python 3.15:** Fix, the ``Py_GetPath`` API was no longer available,
   requiring an explicit declaration again.

-  **Python 3.15:** Fix, the older inline copy of Scons no longer works
   there, now all Python 3.7+ versions use the newer copy that was
   previously only used on Windows.

-  **Python 3.15:** Fix, creating ``long`` objects triggered assertions
   there, since the tag field needs initialization before setting the
   sign and digit count.

-  **Standalone:** Fix, the source package ``__init__.py`` is now
   preferred over a C extension ``__init__.so`` or ``__init__.pyd``
   file, respecting the recompile decisions of the user, whose plugin
   queries are now also cached.

-  **Windows:** Fix, the experimental MinGW64 usage with Python 3.13 and
   higher did not work in Python debug mode, as the internal structure
   offsets for debug builds were missing.

-  **macOS:** Fix, code signing no longer mutates the keychain file,
   since the ``security`` commands change it in place, a temporary copy
   is now used instead.

-  **Compatibility:** Fix, nested frames used the same exception line
   number storage, leading to corruption of either the inner or outer
   line numbers in exceptions, they now have separate storage.

-  **AIX:** Fix, COFF dump based dependency detection for archives now
   extracts object members to a temporary file before dumping them,
   since the direct member selection was not portable.

Package Support
===============

-  **Standalone:** Added support for newer ``PyAV``. (Added in 4.2.1
   already.)

-  **Standalone:** Fix, ``vtk8`` was no longer working, since the
   package path configuration was needlessly restricted to ``vtk``
   version 9 and higher. (Fixed in 4.2.1 already.)

-  **Standalone:** Added support for the latest ``toga`` on macOS, with
   the ``toga_cocoa.resources`` dependency now included. (Added in 4.2.1
   already.)

-  **Plugins:** Fix, the ``PySide6`` ``singleShot`` timer workaround
   protected the wrong argument when called with more arguments,
   allowing the issue it is meant to avoid to occur. (Fixed in 4.2.1
   already.)

New Features
============

-  **Python 3.14:** Added source generation for function calls and more
   hard import types for ``__annotate__`` functions. (Added in 4.2.1
   already.)

-  **Python 3.14:** Added source generation for more constant value
   types for ``__annotate__`` functions, e.g. ``bytes``, ``range``,
   ``slice``, ``bytearray``, and ``complex`` values, including
   non-finite components. (Added in 4.2.1 already.)

-  **Python 3.15:** Pronounced Python 3.15 as partially supported, with
   Python 3.16 now being the only not yet supported version.

-  **Python 3.15:** Added support for unpacking in comprehensions, e.g.
   ``[*i for i in values]`` and ``{**d for d in mappings}``, including
   the async variants.

-  **Python 3.15:** Added the internal structure offsets needed for
   Windows support.

Optimization
============

-  **Standalone:** Moved implicit import consideration from module
   recursion into the optimization pass, avoiding an unnecessary third
   pass for standard library modules using a cold bytecode cache. (Added
   in 4.2.2 already.)

-  **Standalone:** Enabled LTO for the "Python Build Standalone" flavor
   as well, since it is known to be supported. (Added in 4.2.2 already.)

-  Unpacking from values that are known to be indexable now uses direct
   subscript access instead of the iterator protocol, making e.g. ``a, b
   = some_tuple`` a lot faster, with starred unpacking to follow once
   this has proven stable.

-  The ``io.open`` built-in is now treated like ``open``, so that file
   tracing for embedded data files applies to it as well.

Anti-Bloat
==========

-  Avoided using ``pydoc`` in the official ``PySimpleGUI`` package as
   well, which so far was only done for the non-official one. (Fixed in
   4.2.1 already.)

Organizational
==============

-  **UI:** Made the ``--file-description`` help text clear that it is no
   longer Windows only, as it is also used as the summary of the
   AppStream metadata of Linux ``--mode=app`` mode. (Fixed in 4.2.1
   already.)

-  **Release:** Added ``clangd`` to the CI container to allow checking
   with it. (Added in 4.2.2 already.)

-  **Release:** Made it clear that on Python 3.14 and higher, the
   standard library ``compression.zstd`` is used instead of the
   ``zstandard`` package in the requirements.

-  **AI:** Added the ``setup-pr-branch`` skill for setting up fork pull
   request branches for pushing updates, pointed the
   ``module-not-found`` skill at the MRE workflow, and ignored the
   scratch folder used for AI work.

-  **Docs:** Made it clear in the Developer Manual that Python 3.14 is
   covered by feature parity.

-  **Docs:** Integrated the website documentation changes into the User
   Manual, including the report template data tables and the CPU
   architecture baseline section.

-  **Quality:** Disabled more ``ruff`` warnings that are not important
   for Nuitka, and enhanced the ``clangd`` and Visual Code configuration
   for correctness.

Tests
=====

-  Added support for the ``win32``, ``linux``, and ``macos`` variables
   in ``wait_for`` conditions of ``nuitka-watch`` test cases. (Added in
   4.2.1 already.)

-  Added ``--devel-no-bytecode-to-compiled-fallback`` to
   ``nuitka-watch`` compilations with Python 3.14 and higher, requiring
   that annotate functions do not fall back to compiled code for the
   packages we actively monitor.

-  The test runner now displays the full Python version string, which is
   useful for release candidate versions, where the numeric version
   alone is ambiguous.

-  Allowed to specify test names without their version specific suffixes
   in the test runner.

Cleanups
========

-  The temporary filename context manager now deletes the file itself,
   also on errors, simplifying its users such that don't have to do it.
   (Fixed in 4.2.1 already.)

-  **Quality:** Addressed the warnings reported by the ``clangd`` LSP,
   adding shared headers for the long digit, dictionary internal, power,
   and repeat helpers, and organizing the IDE only includes.

Summary
=======

This release is currently under active development and is not yet
feature-complete.

.. include:: ../dynamic.inc
