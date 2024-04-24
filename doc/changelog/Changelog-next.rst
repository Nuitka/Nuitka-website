:orphan:

########################################
 Upcoming Release |NUITKA_VERSION_NEXT|
########################################

.. include:: ../changelog/changes-hub.inc

In this document, we track the per-version changes and comments for the
upcoming Nuitka |NUITKA_VERSION_NEXT| as a draft about hot-fixes of the
current stable release as |NUITKA_VERSION| as well.

****************************
 Nuitka Release 2.2 (Draft)
****************************

.. note::

   This a draft of the release notes for 2.2, which is supposed to
   contains the usual additions of new packages supported out of the box
   and will aim at scalability.

This release focused on compatibility and some important optimization
progress for loops. The main line of changes is to be able to support
Python 3.12 in the next release.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

Bug Fixes
=========

-  Standalone: Added support for ``pypdfium2`` package. Fixed in 2.1.1
   already.

-  Standalone: Make ``cefpython3`` work on Linux. Fixed in 2.1.1
   already.

-  ArchLinux: Added platform linker option for it to be usable with
   their current Arch Python package. Fixed in 2.1.1 already.

-  Fix, ``ctypes.CDLL`` optimization was using misspelled argument name
   for ``use_last_error``, such that keyword argument calls using it
   were statically optimized into ``TypeError`` at compile-time. Fixed
   in 2.1.1 already.

-  Fix, ``list.insert`` was not properly annotating exceptions. Raises
   by producing the inserted value raised or the index were not
   annotated, and therefore could fail to be caught locally. Fixed in
   2.1.1 already.

-  Standalone: Added support for ``selenium`` package. Fixed in 2.1.2
   already.

-  Standalone: Added support for ``hydra`` package. Fixed in 2.1.2
   already.

-  Standalone: Updated ``dotenv`` workaround for newer version. Fixed in
   2.1.3 already.

-  Fix, PySide6 slots were not moved between threads anymore. Need to
   make function renames visible in owning class as well. Fixed in 2.1.3
   already.

-  Standalone: Added support for ``win32com.server.register``. Fixed in
   2.1.3 already.

-  Standalone: Handle "string" import errors of ``uvicorn`` gracefully.
   Fixed in 2.1.3 already.

-  Fix, the ``dill-compat`` plugin needs to still expose the compiled
   type names as built-ins so pickle finds them.

-  Standalone: Added support for ``gruut`` package. Fixed in 2.1.3
   already.

-  Standalone: Added support for newer ``toga`` to also include
   ``toga_winforms`` metadata. Fixed in 2.1.3 already.

-  Standalone: Added support for newer ``tensorflow`` package. Fixed in
   2.1.4 already.

-  Standalone: Fix, ``matplotlib`` needs emit dependency on the backend
   included, otherwise it could be missing at run-time in some cases.
   Fixed in 2.1.4 already.

-  Onefile: Respect ``XDG_CACHE_HOME`` variable on non-Windows
   platforms. The cached location might not be configured to be
   ``~/.cache`` on some systems, respect that. Fixed in 2.1.4 already.

-  Python2: Some cases of ``list.insert`` were not properly handling all
   index types. Fixed in 2.1.4 already.

-  Fix, optimized ``list.remove`` failed to handle tuple arguments
   properly. Removing tuple values from lists, could give errors. Fixed
   in 2.1.4 already.

-  Standalone: Added missing implicit dependencies for
   ``pyarrow.datasets``. Fixed in 2.1.4 already.

-  Standalone: Added support for ``dask.dataframe`` module. Fixed in
   2.1.4 already.

-  Standalone: Added DLLs for ``tensorrt_libs`` package. Fixed in 2.1.4
   already.

-  Standalone: Added missing metadata of ``numpy`` for ``xarray``
   package. Fixed in 2.1.4 already.

-  Standalone: Added support for newer ``scipy``. Fixed in 2.1.5
   already.

-  Standalone: Fix, older gcc could give warning about C code to work
   with ``PYTHONPATH`` and that caused build errors on older systems.
   Fixed in 2.1.5 already.

-  Fix, ``locals`` representing nodes could not be cloned, and as a
   result, some code re-formulations failed to compile in ``try``
   constructs. Fixed in 2.1.5 already.

-  Standalone: Added data files for ``names`` package. Fixed in 2.1.5
   already.

-  Standalone: Added data files for ``randomname`` package. Fixed in
   2.1.5 already.

-  Standalone: Fix, the standalone standard library scan was not fully
   ignoring git folders, subfolders were still looked at and could cause
   issues. Fixed in 2.1.5 already.

-  Standalone: Added support for newer ``transformers``. Fixed in 2.1.5
   already.

-  Standalone: Add support for newer ``bitsandbytes``. Fixed in 2.1.5
   already.

-  Scons: Fix, when locating binaries, do not use directories but only
   files.

   A directory named ``gcc`` could be confused for being a ``gcc``
   binary, but that is of course non-sense. Fixed in 2.1.6 already.

-  Windows: Fix, by default, scan only for ``.bin`` and ``.exe``
   binaries for Nuitka package configuration EXE dependency patterns.
   This was the intended value, but it had not taken effect yet. Fixed
   in 2.1.6 already.

-  Fix, the ``__compiled__.containing_dir`` should be an absolute path.
   For it to be useful after a change of directory is done in the
   program that is necessary. Fixed in 2.1.6 already.

-  Standalone: Added support for more parts of ``networkx`` package.
   Fixed in 2.1.6 already.

-  Windows: Fix working with UNC paths and re-parse points at compile
   time.

   Now Nuitka should work with mapped and even unmapped to drive paths
   like ``\\some-hostname\unc-test`` as they are common in some VM
   setups.

-  Windows: Make sure the download path is an external use path in scons
   as well, otherwise the home directory could be an unusable path for
   MinGW64, causing it to not find files.

-  Standalone: Added missing dependency of ``sspilib`` that prevented
   ``requests-ntlm`` from working on Windows.

-  Python3.5+: Add support for using dictionary un-packings in class
   declarations. This is a rarely used feature, that will practically
   never be used in actual code, but was found missing by tests
   recently.

-  Python3.11: Fix, code objects ``co_qualname`` attribute was not
   actually the qualified name, but the name only.

-  Anaconda: Fix, must not consider Anaconda'S ``lib`` directory system
   DLLs that are not included.

-  Fix, cannot trust dynamic hard modules as much otherwise,
   ``huggingface_hub.utils.tqdm`` ended up being a module, and not the
   class it's supposed to be.

-  macOS: Fix, on newer macOS the ``libc++`` and ``libz`` DLLs cannot be
   found anymore, we need to actively ignore that.

-  Fix, support for newer ``zaber_motion`` was not really working.

New Features
============

-  Added experimental support for Python 3.12, this is passing basic
   tests, but known to crash a lot at runtime still, you are recommended
   to use pre-releases of Nuitka, as official support is not going to
   happen before 2.3 release.

-  Standalone: Added support for ``tensorflow.function`` JIT

   This adds support to preserve the source code of decorated functions
   and provide it at runtime to ``tensorflow`` JIT so it can do its
   tracing executions.

-  For Nuitka package configuration, we now have ``change_class``
   similar to ``change_function`` to replace a full class definition
   with something else, this can be used to modify classes to become
   stubs or even unusable.

-  For the experimental ``@pyqtSlot`` decorator, we also should handle
   the ``@asyncSlot`` just the same. Added in 2.1.1 already.

-  Added new kind of warning of ``plugin`` category and use it in the
   Nuitka Package configuration to inform ``matplotlib`` users to select
   a GUI backend via plugin selection. Added in 2.1.4 already.

-  Zig: Added support for ``zig`` as CC value. Due to it not supporting
   C11 fully yet, we need to use the C++ workaround, and cannot compile
   for Python 3.11 or higher yet.

Optimization
============

-  Use ``set`` specific API in contains tests, rather than generic
   sequence one.

-  Lower ``value in something`` tests for known ``set`` and ``list``
   values to use ``frozenset`` and ``tuple`` respectively.

-  Recognize exact type shapes on loop variables where possible. This
   enables appends to list to be optimized to their dedicated nodes
   among other things, with those often being a lot faster than generic
   code. This speeds up e.g. list append tests by a larger amount.

-  Optimization: Have dedicated helper for ``list.remove``, such that it
   is not using a Python DLL call where that is slow, also the code was
   causing problems previously, that cannot happen in this form, and our
   form does actually work faster in general too.

-  ArchLinux: Enable static libpython by default, it is usable indeed.
   Added in 2.1.2 already.

-  Anti-Bloat: Avoid ``unittest`` usage in ``antlr`` package.

-  Anti-Bloat: Avoid ``IPython`` in ``celery`` package. Added in 2.1.2
   already.

-  Anti-Bloat: Avoid using ``setuptools`` in ``transformers`` package
   for more modules. Added in 2.1.3 already.

-  Anti-Bloat: Avoid testing packages for newer ``tensorflow`` package
   as well. Added in 2.1.4 already.

-  Optimization: Avoid recompiling ``azure`` package which is not
   performance relevant. Added in 2.1.4 already.

-  Avoid GUI plugin owned packages from backend plugins unless the
   corresponding plugin is actually active. Added in 2.1.4 already.

-  Anti-Bloat: Avoid ``setuptools`` in ``deepspeed`` package. Added in
   2.1.4 already.

-  Anti-Bloat: Avoid ``setuptools`` in ``transformers`` package. Added
   in 2.1.4 already.

-  Anti-Bloat: Avoid ``scipy`` usage causing ``torch`` or ``cupy``
   usage. Added in 2.1.4 already.

-  Anti-Bloat: Recognize ``keras`` testing modules as ``unittest``
   bloat.

-  Faster code generation due to enhancements in how identifiers are
   cached for module names, and the indentation codes.

-  Optimization: Handle ``no_docstrings`` issue for ``torio`` package.

-  Anti-Bloat: Avoid ``IPython`` from ``imgui_bundle`` package.

-  Anti-Bloat: Remove testing module usage when ``dask`` is used.

Organisational
==============

-  UI: Catch conflicts between data files and EXE/DLLs/extension module
   filenames. Previously you could overwrite binaries with data files,
   this is now recognized.

-  Onefile: Avoid using program name without suffix inside the dist
   folder, as that avoids collisions with data file directories of the
   same name, e.g. if the package and main binary have the same name,
   they would clash previously, but adding a ``.bin`` suffix to the
   binary avoids that entirely.

-  UI: Don't force ``{VERSION}`` in specs to be resolved to four digits.

   That just makes it hard to use for users, who will be surprised to
   see ``1.0`` become ``1.0.0.0`` when that is only needed for Windows
   version information really.

-  UI: Catch wrong values for ``--jobs`` value sooner, negative and
   non-integer values error exit immediately. Added in 2.1.1 already.

-  UI: Nicer usage name when invoked with ``python -m nuitka``

   The recommended form of calling of Nuitka should not have an ugly
   invocation reference ``__main__.py`` instead put the ``python -m
   nuitka`` notion there.

-  UI: Reorder options for plugins group to be more useful.

-  Plugins: Remove obsolete plugins from standard plugin documentation.
   Removed in 2.1.4 already.

-  UI: For Python debug mode compilation, do not about static libpython
   at all, this is misleading, often it doesn't work for that
   configuration, and it's only a distraction, since debugging Python
   reference counts is not about performance. Changed in 2.1.4 already.

-  UI: Catch newlines in spec values. They break code C code generation
   potentially and they also are likely copy&paste mistakes, that won't
   do what the user expects. Added in 2.1.4 already.

-  Quality: Updated to latest version of black.

-  Quality: Fix, ``isort`` and ``black`` can corrupt outputs, catch
   that.

-  Debugging: Generate Scons debug script

   This can be used to quickly re-execute a Scons compilation without
   running Nuitka again, this is best used in cases, where there is no
   Python level change but only C changes and no expectation of
   producing a usable result.

   Because no post-processing is applied, and as a consequence this is
   not usable to produce binaries that work. In the future, we might
   expand this to be able to run post-processing still.

-  Debugging: Disabling all freelists is now honored for more code,
   tuples and empty dictionaries as well.

-  UI: Add macOS version to help output, that is actually making a lot
   of differences many times.

-  Reports: Add OS release to reports as well.

-  Watch: Reporting more problems, catching more errors, basic ability
   to create PRs from changes added, but not yet used automatically.

Tests
=====

-  Tests: Fix, cannot assume ``setuptools`` to be installed, some RPM
   based systems don't have it.

-  Run commercial code signing test only on Windows.

-  Allow the Azure agent folders for standalone file access tests as
   well, it's like a home directory for the purposes of those tests.

-  Make sure optimization tests are named to make it clear that they are
   tests.

Cleanups
========

-  Remove useless ``--execute-with-pythonpath`` option, we don't use
   that anymore at all.

Summary
=======

The JIT mechanism added for ``tensorflow`` should be possible to
generalize and will be applied to other JITs, like maybe ``numba`` in
the future as well.

.. include:: ../dynamic.inc
