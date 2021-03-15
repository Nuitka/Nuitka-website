This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is a massive improvement in many ways with lots of bug
fixes and new features.

***********
 Bug Fixes
***********

-  Fix, the ``.pyi`` file parser didn't handle relative imports. Fixed
   in 0.6.10.1 already.

-  Windows: Fix, multiprocessing plugin was not working reliable
   following of imports from the additional entry point. Fixed in
   0.6.10.1 already.

-  Pipenv: Workaround parsing issue with our ``setup.py`` to allow
   installation from Github. Fixed in 0.6.10.1 already.

-  Merging of branches in optimization could give indetermistic results
   leading to more iterations than necessary. Fixed in 0.6.10.1 already.

-  Windows: Avoid profile powershell when attempting to resolve
   symlinks. Fixed in 0.6.10.1 already.

-  Windows: Fix, always check for stdin, stdout, and stderr presence.
   This was so far restricted to gui mode applications, but it seems to
   be necessary in other situations too. Fixed in 0.6.10.1 already.

-  Python2: Fix, ``--trace-execution`` was not working for standalone
   mode but can be useful for debugging. Fixed in 0.6.10.1 already.

-  Windows: Onefile could run into path length limits. Fixed in 0.6.10.3
   already.

-  Windows: The winlib gcc download link became broken and was updated.
   Fixed in 0.6.10.3 already.

-  Plugins: The "__main__" module was not triggering all plugin hooks,
   but it needs to for completeness.

-  Standalone: Fix, symlinked Python installations on Windows were not
   working, with dependency walker being unable to look into these.
   Fixed in 0.6.10.4 already.

-  Standalone: Fix support for numpy on Windows and macOS, the plugin
   failed to copy important DLLs. Fixed in 0.6.10.4 already.

-  Python3: For versions before 3.7, the symlink resolution also needs
   to be done, but wasn't handling the bytes output yet. Fixed in
   0.6.10.4 already.

-  Fix, folder based inclusion would both pick up namespace folders and
   modules of the same name, crashing the compilation due to conflicts.
   Fixed in 0.6.10.4 already.

-  Fix, the ``--lto`` wasn't used for clang on non-Windows yet.

-  Fix, the order of locals dict releases wasn't enforced, which could
   lead to differences that break caching of C files potentially. Fixed
   in 0.6.10.5 already.

-  Fix, ``hash`` nodes didn't consider if their argument was raising,
   even if the type of the argument was ``str`` and therefore the
   operation should not. Fixed in 0.6.10.5 already.

-  Fix, need to copy type shape and escape description for the
   replacement inverted comparisons when used with ``not``, otherwise
   the compilation can crash as these are expected to be present at all
   times. Fixed in 0.6.10.5 already.

-  Fix, some complex constant values could be confused, e.g. ``-0j`` and
   ``0j``. These corner cases were not properly considered in the
   constant loading code, only for ``float`` so far.

-  Standalone: Fix, bytecode only standard library modules were not
   working. This is at least used with Fedora 33.

-  Linux: Fix, extension modules compiled with ``--lto`` were not
   working.

-  Windows: Retry if updating resources fails due to Virus checkers
   keeping files locked.

-  Plugins: Pre- and postload code of modules should not be allowed to
   cause ``ImportError``, as these will be invisible to the other parts
   of optimization, instead make them unraisable error traces.

-  Standalone: Adding missing import for SciPy 1.6 support.

-  Windows: Fix, only export required symbols when using MinGW64 in
   module mode.

**************
 New Features
**************

-  Python3.9: Added official support for this version.

-  Onefile: Added command line options to include data files. These are
   ``--include-package-data`` which will copy all non-DLLs and
   non-Python files of package names matching the pattern given. And
   ``--include-data-file`` takes source and relative target file paths
   and copies them. For onefile this is the only way to include files,
   for standalone mode they are mostly a convenience function.

-  Onefile: Added mode where the file is unpacked to a temporary folder
   before running instead of doing it to appdata.

-  Onefile: Added linux specific options ``--linux-onefile-icon`` to
   allow provision of an icon to use in onefile mode on Linux, so far
   this was only available as the hard coded path to a Python icon,
   which also didn't exist on all platforms.

-  UI: Major logging cleanup. Everything is now using our tracing
   classes and even error exits go through there and are therefore
   colored if possible.

-  Plugins: Make it easier to integrate commercial plugins, now only an
   environment variable needs to point to them.

-  UI: Enhanced option parsing gives notes. This complains about options
   that conflict or that are implied in others. Trying to catch more
   usage errors sooner.

-  Plugins: Ignore exceptions in buggy plugin code, only warn about them
   unless in debug mode, where they still crash Nuitka.

-  Scons: More complete scons report files, includes list values as well
   and more modes used.

-  Windows: The ``clcache`` is now included and no longer used from the
   system.

-  Output for ``clcache`` and ``ccache`` results got improved.

-  Enhanced support for ``clang``, on Windows if present near a
   ``gcc.exe`` like it is the case for some winlibs downloads, it will
   be used. To use it provide ``--mingw64 --clang`` both. Without the
   first one, it will mean ``clangcl.exe`` which uses the MSVC compiler
   as a host.

**************
 Optimization
**************

-  Some modules had very slow load times, e.g. if they used many list
   objects due to linear searches for memory deduplication of objects.
   We now have dictionaries of practically all constant objects loaded,
   making these more instant.

-  Use less memory at compile time due using ``__slots__`` for all node
   types, finally figured out, how to achieve this with multiple
   inheritance.

-  Use hedley for compiler macros like ``unlikely`` as they know best
   how to do these.

-  Special case the merging of 2 branches avoiding generic code and
   being much faster.

-  Hard imports have better code generated, and are being optimized into
   for the few standard library modules and builtin modules we handle,
   they also now annotate the type shape to be module.

-  No longer annotate hard module import attribute lookups as control
   flow escapes. Not present attributes are changed into static raises.
   Trust for values is configured for a few values, and experimental.

-  Avoid preloaded packages for modules that have no side effects and
   are in the standard library, typically ``.pth`` files will use e.g.
   ``os`` but that's not needed to be preserved.

-  Use ``incbin`` for including binary data through inline assemly of
   the C compiler. This covers many more platforms than our previous
   linker option hacks, and the fallback to generated C code. In fact
   everything but Windows uses this now.

****************
 Organisational
****************

-  Windows: For Scons we now require a Python 3.5 or higher to be
   installed to use it.

-  Windows: Removed support for gcc older than version 8. This
   specifically affects CondaCC and older MinGW64 installations. Since
   Nuitka can now download the MinGW64 10, there is no point in having
   these and they cause issues.

-  We took over the maintenance of clcache as Nuitka/clcache which is
   not yet ready for public consumption, but should become the new
   source of clache in the future.

-  Include an inline copy of clcache in Nuitka and use it on Windows for
   MSVC and ClangCL.

-  Removed compatibility older aliases of follow option, ``--recurse-*``
   and require ``--follow-*`` options to be used instead.

-  For pylint checking, the tool now supports a ``--diff`` mode where
   only the changed files get checked. This is much faster and allows to
   do it more often before commit.

-  Check the versions of isort and black when doing the autoformat to
   avoid using outdated versions.

-  Handling missing pylint more gracefully when checking source code
   quality.

-  Make sure to use the codespell tool with Python3 and make sure to
   error exit when spelling problems were found, so we can use this in
   Github actions too.

-  Removed Travis config, we now only use Github actions.

-  Removed landscape config, it doesn't really exist anymore.

-  Bumped all PyPI dependnecies to their latest versions.

-  Recommend ccache on Debian, as we now consider the absence of ccache
   something to warn about.

-  Plugins: The DLLs asked for by plugins that are not found are no
   longer warned about.

-  Allow our checker and format tools to run on outside of tree code. We
   are using that for Nuitka/clcache.

-  Added support for Fedora 33 and openSUSE 15.3, as well as Ubuntu
   Groovy.

-  Windows: Check if Windows SDK is installed for MSVC and ClangCL.

-  Windows: Enhanced wording in case no compiler was found. No longer
   tell people how to manually install MinGW64, that is no longer
   necessary and ``pywin32`` is not needed to detect MSVC, so it's not
   installed if not found.

-  Detect "embeddable Python" by missing include files, and reject it
   with proper error message.

-  Added onefile and standalone as a use case to the manual and put also
   the DLL and data files problems as typically issues.

**********
 Cleanups
**********

-  Avoid decimal and string comparisons for Python versions checks,
   these were lazy and are going to break once 3.10 surfaces. In testing
   we now use tuples, in Nuitka core hexacimal values much like CPython
   itself does.

-  Stop using subnode child getters and setters, and instead only use
   subnode attributes. This was gradually changed so far, but in this
   release all remaining uses have migrated. This should also make the
   optimization stage go faster.

-  Change node constructors to not use a decorator to resolve conflicts
   with builtin names, rather handle these with manual call changes, the
   decorator only made it difficult to read and less performant.

-  Move safe string helpers to their own dedicated helper file, allowing
   for reuse in plugin code that doesn't want to use all of Nuitka C
   helpers.

-  Added utils code for inline copy imports, as we use that for quite a
   few things now.

-  Further restructured the Scons files to use more common code.

-  Plugins: The module name objects now reject many ``str`` specific
   APIs that ought to not be used, and the code got changed to use these
   instead, leading to cleaner and more correct usages.

-  Using named tuples to specify included data files and entry points.

-  Use ``pkgutil`` in plugins to scan for modules rather than listing
   directories.

*******
 Tests
*******

-  New option to display executed commands during comparisons.

-  Added test suite for onefile testing.

*********
 Summary
*********

This release has seen Python3.9 and Onefile both being completed. The
later needs compression added on Windows, but that can be added in a
coming release, for now it's fully functional.

The focus clearly has been on massive cleanups, some of which will
affect compile time performance. There is relatively little new
optimization otherwise.

The adoption of clcache enables a very fast caching, as it's now loaded
directly into the Scons process, avoiding a separate process fork.

Generally a lot of polishing has been applied with many cleanups
lowering the technical debt. It will be interesting to see where the
hard module imports can lead us in terms of more optimization. Static
optimization of the Python version comparisons and checks is needed to
lower the amount of imports to be processed.

Important fixes are also included, e.g. the constants loading
performance was too slow in some cases. The ``multiprocessing`` on
Windows and ``numpy`` plugins were regressed and finally everything
ought to be back to working fine.

Future work will have to aim at enhanced scalability. In some cases,
Nuitka still takes too much time to compile if projects like Pandas
include virtually everything installed as an option for it to use.
