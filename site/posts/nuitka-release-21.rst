.. post:: 2024/03/23 15:11
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 2.1
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release had focus on new features and new optimization. There is a
also a large amount of compatibility with things newly added to support
anti-bloat better, and workaround problems with newer package versions
that would otherwise need source code at run-time.

***********
 Bug Fixes
***********

-  Windows: Using older MSVC before 14.3 was not working anymore. Fixed
   in 2.0.1 already.

-  Compatibility: The ``dill-compat`` plugin didn't work for functions
   with closure variables taken. Fixed in 2.0.1 already.

   .. code:: python

      def get_local_closure(b):
        def _local_multiply(x, y):
          return x * y + b
        return _local_multiply

      fn = get_local_closure(1)
      fn2 = dill.loads(dill.dumps(fn))
      print(fn2(2, 3))

-  Windows: Fix, sometimes ``kernel32.dll`` is actually reported as a
   dependency, remove assertion against that. Fixed in 2.0.1 already.

-  UI: The help output for ``--output-filename`` was not formatted
   properly. Fixed in 2.0.1 already.

-  Standalone: Added support for the ``scapy`` package. Fixed in 2.0.2
   already.

-  Standalone: Added ``PonyORM`` implicit dependencies. Fixed in 2.0.2
   already.

-  Standalone: Added support for ``cryptoauthlib``, ``betterproto``,
   ``tracerite``, ``sklearn.util``, and ``qt_material`` packages. Fixed
   in 2.0.2 already.

-  Standalone: Added missing data file for ``scipy`` package. Fixed in
   2.0.2 already.

-  Standalone: Added missing DLLs for ``speech_recognition`` package.
   Fixed in 2.0.2 already.

-  Standalone: Added missing DLL for ``gmsh`` package. Fixed in 2.0.2
   already.

-  UI: Using reporting path in macOS dependency scan error message,
   otherwise these contain home directory paths for no good reason.
   Fixed in 2.0.2 already.

-  UI: Fix, could crash when compiling directories with trailing slashes
   used. At least on Windows, this happened for the "/" slash value.
   Fixed in 2.0.2 already.

-  Module: Fix, convenience option ``--run`` was not considering
   ``--output-dir`` directory to load the result module. Without this,
   the check for un-replaced module was always triggering for module
   source in current directory, despite doing the right thing and
   putting it elsewhere. Fixed in 2.0.2 already.

-  Python2: Avoid values for ``__file__`` of modules that are unicode
   and solve a TODO that restores consistency over modules mode
   ``__file__`` values. Fixed in 2.0.2 already.

-  Windows: Fix, short paths with and without dir name cached wrongly,
   which could lead to shorted paths even where not asked for them.
   Fixed in 2.0.2 already.

-  Fix, comparing list values that changed could segfault. This is a bug
   fix Python did, that we didn't follow yet and that became apparent
   after using our dedicated list helpers more often. Fixed in 2.0.2
   already.

-  Standalone: Added support for ``tiktoken`` package. Fixed in 2.0.2
   already.

-  Standalone: Fix, namespace packages had wrong runtime ``__path__``
   value. Fixed in 2.0.2 already.

-  Python3.11: Fix, was using tuples from freelist of the wrong size

   -  CPython changed the index for the size, to not use zero, which was
      wasteful when introduced with 3.10, but to ``size-1`` but we did
      not follow that and then used a tuple one bit larger than
      necessary.

   -  As a result, code producing a lot short living tuples could end up
      creating new ones over and over, causing bad memory allocations
      and slow performance.

   Fixed in 2.0.2 already.

-  macOS: Fix, need to allow non-existent and versioned dependencies of
   DLLs to themselves. Fixed in 2.0.2 already.

-  Windows: Fix PGO (Profile Guided Optimization) build errors with
   MinGW64, this feature is not yet ready for general use, but these
   errors shouldn't happen. Fixed in 2.0.2 already.

-  Plugins: Fix, do not load ``importlib_metadata`` unless really
   necessary.

   The ``pkg_resources`` plugin used to load it, and that then had
   harmful effects for our handling of distribution information in some
   configurations. Fixed in 2.0.3 already.

-  Plugins: Avoid warnings from plugin evaluated code, it could happen
   that a ``UserWarning`` would be displayed during compilation. Fixed
   in 2.0.3 already.

-  Fix, loading pickles with compiled functions in module mode was not
   working. Fixed in 2.0.3 already.

-  Standalone: Added data files for ``h2o`` package. Fixed in 2.0.3
   already.

-  Fix, variable assignment from variables that started to raise were
   not recognized.

   When a variable assignment from a variable became a raise expression,
   that wasn't caught and propagated as it should have been. Fixed in
   2.0.3 already.

-  Make the ``NUITKA_PYTHONPATH`` usage more robust. Fixed in 2.0.3
   already.

-  Fix, PySide2/6 argument name for slot connection and disconnect
   should be ``slot``, wasn't working with keyword argument calls. Fixed
   in 2.0.3 already.

-  Standalone: Added support for ``paddle`` and ``paddleocr`` packages.
   Fixed in 2.0.4 already.

-  Standalone: Added support for ``diatheke``. Fixed in 2.0.4 already.

-  Standalone: Added support for ``zaber-motion`` package. Fixed in
   2.0.4 already.

-  Standalone: Added support for ``plyer`` package. Fixed in 2.0.4
   already.

-  Fix, added handling of ``OSError`` for metadata read, otherwise
   corrupt packages can have Nuitka crashing. Fixed in 2.0.4 already.

-  Fix, need to annotate potential exception exit when making a fixed
   import from hard module attribute. Fixed in 2.0.4 already.

-  Fix, didn't consider Nuitka project options with ``--main`` and
   ``--script-path``. This is of course the only way Nuitka-Action does
   call it, so they didn't work there at all. Fixed in 2.0.4 already.

-  Scons: Fix, need to close progress bar when about to error exit.
   Otherwise error outputs will be garbled by incomplete progress bar.
   Fixed in 2.0.4 already.

-  Fix, need to convert relative from imports to hard imports too, or
   else packages needed to be followed are not included. Fixed in 2.0.5
   already.

-  Standalone: Added ``pygame_menu`` data files. Fixed in 2.0.6 already.

-  Windows: Fix, wasn't working when compiling on network mounted drive
   letters. Fixed in 2.0.6 already.

-  Fix, the ``.pyi`` parser was crashing on some comments with a leading
   ``from`` in the line, recognize these better. Fixed in 2.0.6 already.

-  Actions: Fix, some yaml configs could fail to load plugins. Fixed in
   2.0.6 already.

-  Standalone: Added support for newer ``torch`` packages that otherwise
   require source code.

-  Fix, inline copies of ``tqdm`` etc. left sub-modules behind, removing
   only the top level ``sys.modules`` entry may not be enough.

**************
 New Features
**************

-  Plugins: Added support for ``constants`` in Nuitka package
   configurations. We can now using ``when`` clauses, define variable
   values to be defined, e.g. to specify the DLL suffix, or the DLL
   path, based on platform dependent properties.

-  Plugins: Make ``relative_path``, ``suffix``, ``prefix`` in DLL Nuitka
   package configurations allowed to be an expression rather than just a
   constant value.

-  Plugins: Make not only booleans related to the python version
   available, but also strings ``python_version_str`` and
   ``python_version_full_str``, to use them when constructing e.g. DLL
   paths in Nuitka Package Configuration.

-  Plugins: Added helper function ``iterate_modules`` for producing the
   submodules of a given package, for using in expressions of Nuitka
   package configuration.

-  macOS: Added support for Tcl/Tk detection on Homebrew Python.

-  Added ``module`` attribute to ``__compiled__`` values

   So far it was impossible to distinguish non-standalone, i.e.
   accelerated mode and module compilation by looking at the
   ``__compiled__`` attribute, so we add an indicator for module mode
   that closes this gap.

-  Plugins: Added ``appdirs`` and ``importlib`` for use in Nuitka
   package config expressions.

-  Plugins: Added ability to specify modules to not follow when a module
   is used. This ``nofollow`` configuration is for rare use cases only.

-  Plugins: Added values ``extension_std_suffix`` and
   ``extension_suffix`` for use in expressions, to e.g. construct DLL
   suffix patterns from it.

-  UI: Added more control over caching with per cache category
   environment variables, as `documented in the User Manual.
   <https://nuitka.net/doc/user-manual.html#control-where-caches-live>`_.

-  Plugins: Added support for reporting module detections

   The ``delvewheel`` plugin now puts the version of that packaging tool
   used by a particular module in the report rather than tracing it to
   the user, that in the normal case won't care. This is more for
   debugging purposes of Nuitka.

**************
 Optimization
**************

-  Scalability: Do not make loop analysis at all for very trusted value
   traces, their point is to not change, and waiting for that to be
   confirmed has no point.

-  Use very trusted value traces in functions not just as mere assign
   traces or else expected optimization will not be done on them in many
   cases. With this a lot more cases of hard values are optimized
   leading also to generally more compact and correct results in terms
   of imports, metadata, code avoided on the wrong OS, etc.

-  Scalability: When specializing assignments, make sure to have the
   proper value trace immediately.

   When changing to a hard value, the value trace was still an assign
   trace and not very trusted for one for micro pass of the module.

   This had the effect to need one more micro pass to get to benefiting
   of the unescapable nature of those values, which meant more micro
   passes than necessary and those being more complex due to escaped
   traces, and therefore taking longer for affected modules.

-  Scalability: The code trying avoid merge traces of merge traces, and
   to instead flatten merge traces was only handling part of these
   correctly, and correcting it reduced optimization time for some
   functions from infinite to instant. Less memory usage should also
   come out of this, even where this was not affecting compile time as
   much. Added in 2.0.1 already.

-  Scalability: Some codes that checked for variables were testing for
   temporary variable and normal variable both one after another, making
   some optimization steps and code generation slower than necessary due
   to the extra calls.

-  Scalability: A variable assignment from variable that were later
   recognized to become a raise was not recognized as such, and this
   then wasn't caught and propagated as it should, preventing more
   optimization of the affected code. Make sure to convert more directly
   when observing things to change, rather than doing it one pass later.

-  The fix proper reuse of tuples released to the freelist with matching
   sizes causes less memory usage and faster performance for the 3.11
   version. Added in 2.0.2 already.

-  Statically optimize ``sys.exit`` into exception raise of
   ``SystemExit``.

   This should make a bunch of dead code obvious to Nuitka, it can now
   tell this aborts execution of a branch, potentially eliminating
   imports, etc.

-  macOS: Enable python static link library for Homebrew too. Added in
   2.0.1 already. Added in 2.0.3 already.

-  Avoid compiling bloated module namespace of ``altair`` package. Added
   in 2.0.3 already.

-  Anti-Bloat: Avoid including ``kubernetes`` for ``tensorflow`` unless
   used otherwise. Added in 2.0.3 already.

-  Anti-Bloat: Avoid including setuptools for ``tqdm``. Added in 2.0.3
   already.

-  Anti-Bloat: Avoid ``IPython`` in ``fire`` package. Added in 2.0.3
   already.

-  Anti-Bloat: Avoid including ``Cython`` for ``pydantic`` package.
   Added in 2.0.3 already.

-  Anti-Bloat: Changes to avoid ``triton`` in newer ``torch`` as well.
   Added in 2.0.5 already.

-  Anti-Bloat: Avoid ``setuptools`` via ``setuptools_scm`` in
   ``pyarrow``.

-  Anti-Bloat: Made more packages equivalent to using ``setuptools``
   which we want to avoid, all of ``Cython``, ``cython``, ``pyximport``,
   ``paddle.utils.cpp_extension``, ``torch.utils.cpp_extension`` were
   added for better reports of the actual causes.

****************
 Organizational
****************

-  Moved the changelog of Nuitka to the website, just point to there
   from Nuitka repo.

-  UI: Proper error message from Nuitka when scons build fails with a
   detail mnemonic page. Read more on for detailed information.

-  Windows: Reject all MinGW64 that are not are not the ``WinLibs`` that
   Nuitka itself downloaded. As these packages break very easily, we
   need to control if it's a working set of ``ccache``, ``make``,
   ``binutils`` and gcc with all the necessary workarounds and features
   like ``LTO`` working on Windows properly.

-  Quality: Added auto-format of PNG and JPEG images. This aims at
   making it simpler to add images to our repositories, esp. Nuitka
   Website. This now makes ``optipng`` and ``jpegoptim`` calls as
   necessary. Previously this was manual steps for the website to be
   applied.

-  User Manual: Be more clear about compiler version needs on Windows
   for Python 3.11.

-  User Manual: Added examples for error message with low C compiler
   memory, such that maybe they can be found via search by users.

-  User Manual: Removed sections that are unnecessary or better
   maintained as separate pages on the website.

-  Quality: Avoid empty ``no-auto-follow`` values, for silently ignoring
   it there is a dedicated string ``ignore`` that must be used.

-  Quality: Enforce normalized paths for ``dest_path`` and
   ``relative_path``. Users were uncertain if a leading dot made sense,
   but we now disallow it for clarity.

-  Quality: Check more keys with expressions for syntax errors, to catch
   these mistakes in configuration sooner.

-  Quality: Scanning through all files with the auto-format tool should
   now be faster, and CPython test suite directories (test submodules)
   if present are ignored.

-  Release: Remove month from manpage generation, that's only noise in
   diffs.

-  Removed digital art folders, these were only making checkouts larger
   for no good reason. We will have better ones on the website in the
   future.

-  Scons: Allow C warnings when compiling for running in debugger
   automatically.

-  UI: The macOS app bundle option is not experimental at all. This has
   been untrue for years now, remove that cautioning.

-  macOS: Discontinue support for PyQt6.

   With newer PyQt6 we would have to package frameworks properly, and we
   don't have that yet and it will be a lot of developer time to get it.

   Instead point people to PySide6 which is the better choice and is
   perfectly supported by Qt company and Nuitka.

-  Removed version numbering, month of creation, etc. from the man pages
   generated.

-  Moved ``Credits.rst`` file to be on the website and maintain it there
   rather than syncing of from the Nuitka repository.

-  Bumped copyright year and split the license text such that it is now
   at the bottom of the files rather than eating up the first page, this
   is aimed at making the code more readable.

**********
 Cleanups
**********

-  With ``sys.exit`` being optimized, we were able to make our trick to
   avoid following ``nuitka`` because of accidentally finding the
   ``setup`` as an import more simple.

   .. code:: python

      # Don't allow importing this, and make recognizable that
      # the above imports are not to follow. Sometimes code imports
      # setup and then Nuitka ends up including itself.
      if __name__ != "__main__":
         sys.exit("Cannot import 'setup' module of Nuitka")

-  Scons: Don't scan for ``ccache`` on Windows, the ``WinLibs`` package
   contains it nowadays, and since it's now required to be used, there
   is no point for this code anymore.

-  Minor cleanups coming from trying out ``ruff`` as a linter on Nuitka,
   it found a few uses of not using ``not in``, but that was it.

*******
 Tests
*******

-  Removed test with chinese filenames, we need to avoid chinese names
   in the repo. These have been seen as preventing installation on some
   systems that are not capable of handling them in the git, zip, pip
   tooling, so lets avoid them entirely now that Nuitka handles these
   just fine.

-  Tests: More macOS standalone tests that need to be bundles were
   getting the project configuration to do it.

*********
 Summary
*********

This release added much needed tools for our Nuitka Package
configuration, but also cleans up scalability and optimization that was
supposed to work, but did not yet, or not anymore.

The usability improved again, as it does always, but the big
improvements for scalability that will implement existing algorithms
more efficient, are yet to come, this release was mainly driven by the
need to get ``torch`` to work in its latest version out of the box with
stable Nuitka, but this couldn't be done as a hotfix
