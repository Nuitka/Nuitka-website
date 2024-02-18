.. post:: 2023/06/09 15:41
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 1.6
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release bumps the much awaited 3.11 support to full level. This
means Nuitka is now expected to behave identical to CPython3.11 for the
largest part.

There is plenty of new features in Nuitka, e.g. a new testing approach
with reproducible compilation reports, support for including the
metadata if an distribution, and more.

In terms of bug fixes, it's also huge, and esp. macOS got a lot of
improvements that solve issues with prominent packages in our dependency
detection. And then for PySide we found a corruption issue, that got
workarounds.

***********
 Bug Fixes
***********

-  The new dict ``in`` optimization was compile time crashing on code
   where the dictionary shaped value checked for a key was actually an
   conditional expression

   .. code:: python

      # Was crashing
      "value" in some_dict if condition else other_dict

   Fixed in 1.5.1 already.

-  Standalone: Added support for ``openvino``. This also required to
   make sure to keep used DLLs and their dependencies in the same
   folder. Before they were put on the top level. Fixed in 1.5.1
   already.

-  Android: Convert ``RPATH`` to ``RUNPATH`` such that standalone
   binaries need no ``LD_LIBRARY_PATH`` guidance anymore. Fixed in 1.5.1
   already.

-  Standalone: Added support for newer ``skimage``. Fixed in 1.5.1
   already.

-  Standalone: Fix, new data file type ``.json`` needed to be added to
   the list of extensions used for the Qt plugin bindings. Fixed in
   1.5.2 already.

-  Standalone: Fix, the ``nuitka_types_patch`` module using during
   startup was released, which can have bad effects. Fixed in 1.5.2
   already.

-  Android: More reliable detection of the Android based Python Flavor.
   Fixed in 1.5.2 already.

-  Standalone: Added data files for ``pytorch_lightning`` and
   ``lightning_fabric`` packages. Added in 1.5.2 already.

-  Windows: Fix, the preservation of ``PATH`` didn't work on systems
   where this could lead to encoding issues due to reading a MBCS value
   and writing it as a unicode string. We now read and write the
   environment value as ``unicode`` both. Fixed in 1.5.3 already.

-  Plugins: Fix, the scons report values were not available in case of
   removed ``--remove-output`` deleting it before use. It is now read in
   case if will be used. Fixed in 1.5.3 already.

-  Python3.11: Added support for ``ExceptionGroup`` built-in type. Fixed
   in 1.5.4 already.

-  Anaconda: Fix, using ``numpy`` in a virtualenv and not from conda
   package was crashing. Fixed in 1.5.4 already.

-  Standalone: Added support for ``setuptools``. Due to the anti-bloat
   work, we didn't notice that if that was not sufficiently usable, the
   compiled result was not usable. Fixed in 1.5.4 already.

-  Distutils: Added support for pyproject with ``src`` folders. This
   supports now ``tool.setuptools.packages.find`` with a ``where`` value
   with pyproject files, where it typically is used like this:

   .. code:: toml

      [tool.setuptools.packages.find]
      where = ["src"]

-  Windows: Fix, the ``nuitka-run`` batch file was not working. Fixed in
   1.5.4 already.

-  Standalone: Add ``pymoo`` implicit dependencies. Fixed in 1.5.5
   already.

-  macOS: Avoid deprecated API, this should fix newer Xcode being used.
   Fixed in 1.5.5 already.

-  Fix, the ``multiprocessing`` in spawn mode didn't handle relative
   paths that become invalid after process start. Fixed in 1.5.5
   already.

-  Fix, spec ``%CACHE_DIR%`` was not given the correct folder on
   non-Windows. Fixed in 1.5.5 already.

-  Fix, special float values like ``nan`` and ``inf`` didn't properly
   generate code for C values. Fixed in 1.5.5 already.

-  Standalone: Add missing DLL for ``onnxruntime`` on Linux too. Fixed
   in 1.5.5 already.

-  UI: Fix, illegal python flags value could enable ``site`` mode. by
   mistake and were not caught. Fixed in 1.5.6 already.

-  Windows: Fix, user names with spaces failed with MinGW64 during
   linking. Fixed in 1.5.6 already.

-  Linux: Fix, was not excluding all libraries from glibc, which could
   cause crashes on newer systems. Fixed in 1.5.6 already.

-  Windows: Fix, could still pickup SxS libraries distributed by other
   software when found in PATH. Fixed in 1.5.6 already.

-  Windows: Fix, do not use cache DLL dependencies if one the files
   listed there went missing. Fixed in 1.5.6 already.

-  Onefile: Reject path spec that points to a system folder. We do not
   want to delete those when cleaning up clearly. Added in 1.5.6
   already.

-  Plugins: Fix, the ``dill-compat`` was broken by code object changes.
   Fixed in 1.5.6 already.

-  Standalone: Added workaround for ``networkx`` decorator issues. Fixed
   in 1.5.7 already.

-  Standalone: Added workaround for PySide6 problem with disconnecting
   signals from methods. Fixed in 1.5.7 already.

-  Standalone: Added workaround for PySide2 problem with disconnecting
   signals.

-  Fix, need to make sure the yaml package is located absolutely or else
   case insensitive file systems can confuse things. Fixed in 1.5.7
   already.

-  Standalone: Fix, extra scan paths were not considered in caching of
   module imports, breaking the feature in many cases. Fixed in 1.5.7
   already.

-  Windows: Fix, avoid system installed ``appdirs`` package as it is
   frequently broken. Fixed in 1.5.7 already.

-  Standalone: The bytecode cache check needs to handle re-checking
   relative imports found in the cache better. Otherwise some standard
   library modules were always recompiled due to apparent import
   changes. Fixed in 1.5.7 already.

-  Nuitka-Python: Fix, do not insist on ``PYTHONHOME`` making it to
   ``os.environ`` in order to delete it again. Fixed in 1.5.7 already.

-  Nuitka-Python: Allow builtin modules of all names. This is of course
   what it does. Fixed in 1.5.7 already.

-  Nuitka-Python: Ignore empty extension module suffix. Was confusing
   Nuitka to consider every file an extension module potentially. Fixed
   in 1.5.7 already.

-  Plugins: Properly merge code coming from distinct plugins. The
   ``__future__`` imports need to be moved to the start. Added in 1.5.7
   already.

-  Standalone: Added support for ``opentele`` package. Fixed in 1.5.7
   already.

-  Standalone: Added support for newer ``pandas`` and ``pyarrow`` usage.
   Fixed in 1.5.7 already.

-  Standalone: Added missing implicit dependency for PySide6. Fixed in
   1.5.7 already.

-  Fix, the pyi-file parser didn't handle doc strings, and could be
   crash for comment contents not conforming to be import statement
   code. Fixed in 1.5.8 already.

-  Standalone: Added support for ``pyqtlet2`` data files.

-  Python2: Fix, ``PermissionError`` doesn't exist on that version,
   which could lead to issues with retries for locked files e.g. but was
   also observed with symlinks.

-  Plugins: Recognize the error given by with ``upx`` if a file is
   already compressed.

-  Fix, so called "fixed" imports were not properly tracking their use,
   such that they then didn't show up in reports, and didn't cause
   dependencies on the module, which could e.g. impact ``importlib`` to
   not be included even if still being used.

-  Windows: Fix, retries for payload attachment were crashing when
   maximum number of retries were reached. Using the common code for
   retries solves that, since that code handles it just fine.

-  Standalone: Added support for the ``av`` module.

-  Distutils: Fix, should build from files in ``build`` folder rather
   than ``source`` files. This allows tools like ``versioneer`` that
   integrate with setuptools to do their thing, and get the result of
   that to compilation rather than the original source files.

-  Standalone: Added support for the ``Equation`` module.

-  Windows/macOS: Avoid problems with case insensitive file systems. The
   ``nuitka.Constants`` module and ``nuitka.constants`` package could
   collide, so we now avoid that package, there was only what is now
   ``nuitka.Serialization`` in there anyway. Also similar problem with
   ``nuitka.utils.Json`` and ``json`` standard library module.

-  Standalone: Added support ``transformers`` package.

-  Standalone: Fix for ``PyQt5`` which needs a directory to exist.

-  macOS: Fix, was crashing with PyQt6 in standalone mode when trying to
   register plugins to non-default path. We now try to skip the need,
   which also makes it work.

-  Fix, recursion error for complex code that doesn't happen in ``ast``
   module, but during conversion of the node tree it gives to our own
   tree, were not handled, and crashed with ``RecursionError``. This is
   now also handled, just like the error from ``ast``.

-  Standalone: Added support for ``sqlfluff``.

-  Standalone: Added support for PySide 6.5 on macOS solving DLL
   dependency issues.

-  Scons: Recognize more ``ccache`` outputs properly, their logging
   changed and provided irrelevant states, and ones not associated so
   far.

-  Onefile: Fix, could do random exit codes when failing to fork for
   whatever reason.

-  Standalone: Added support for ``pysnmp`` package.

-  Standalone: Added support for ``torchaudio`` and ``tensorflow`` on
   macOS. These contain broken DLL dependencies as relative paths, that
   are apparently ignored by macOS, so we do that too now.

-  Onefile: Use actual rather than guessed standalone binary name for
   ``multiprocessing`` spawns. Without this, a renamed onefile binary,
   didn't work.

-  Fix, side effect nodes, that are typically created when an expression
   raises, were use in optimization contexts, where they do not work.

-  Standalone: Added missing implicit dependency for
   ``sentence_transformers`` package.

-  macOS: Fix, added missing dependency for ``platform`` module.

**************
 New Features
**************

-  Support for Python 3.11 is finally there. This took very long,
   because there were way more core changes than with previous releases.
   Nuitka integrates close to that core, and is as such very affected by
   this. Also a lot of missed opportunities to improve 3.7 or higher,
   3.9 or higher, and 3.10 or higher were implemented right away, as
   they were discovered on the way. Those had core changes not yet taken
   advantage of and as a result got faster with Nuitka too.

-  Reports: Added option ``--report-diffable`` to make the XML report
   created with ``--report`` become usable for comparison across
   different machine installations, users compiling, etc. so it can be
   used to compare versions of Nuitka and versions of packages being
   compiled for changes. Also avoid short names in reports, and resolve
   them back to long names, so they become more portable too.

-  Reports: Added option to provide custom data from the user. We use it
   in out testing to record the pipenv state used with things like
   ``--report-user-provided=pipenv-lock-hash=64a5e4`` with this data
   ending up inside of reports, where tools like the new testing tool
   ``nuitka-watch`` can use it to decide if upstream packages changed or
   not. These are free form, just needs to fit XML rules.

-  Plugins: Added ``include-pyi-file`` flag to data-files section. If
   provided, the ``.pyi`` file belonging to a specific module is
   included. Some packages, e.g. ``skimage`` depend at runtime on them.
   For data file options and configuration, these files are excluded,
   but this is now the way to force their inclusion. Added in 1.5.1
   already.

-  Compatibility: Added support for including distribution metadata with
   new option ``--include-distribution-metadata``.

   This allows generic walks over distributions and their entry points
   to succeed, as well as version checks with the metadata packages that
   are not compile time optimized.

-  Distutils: Handle extension modules in build tasks. Also recognize if
   we built it ourselves, in which case we remove it for rebuild. Added
   in 1.5.7 already.

-  Linux: Detect DLL like filenames that are Python extension modules,
   and ignore them when listing DLLs of a package with
   ``--list-package-dlls`` option. So far, this was a manual task to
   figure out actual DLLs. This will of course improve the Yaml package
   configuration tooling .

-  Onefile: Allow forcing to use no compression for the onefile payload,
   useful for debugging, to avoid long compression times and for test
   coverage of the rare case of not compressing if the bootstrap handles
   that correctly too.

-  Need to resolve symlinks that were used to call the application
   binary in some places on macOS at least. We therefore implemented the
   previously experimental and Windows only feature for all platforms.

-  Standalone: Added support including symlinks on non-Windows in
   standalone distribution, if they still point to a path that is inside
   the distribution. This can save a bunch of disk space used for some
   packages that e.g. distribute DLL links on Linux.

-  Onefile: Added support for including symlinks from the standalone
   distribution as such on non-Windows. Previously they were resolved to
   complete copies.

-  UI: Respect code suffixes in package data patterns. With this e.g.
   ``--include-package-data=package_name:*.py`` is doing what you say,
   even if of course, that might not be working.

-  UI: Added option ``--edit-module-code`` option.

   To avoid manually locating code to open it in Visual Code replaced
   old ``find-module`` helper to be a main Nuitka option, where it is
   more accessible. This also goes beyond it it, such that it resolves
   standalone file paths to module names to make debugging easier, and
   that it opens the file right away.

-  Standalone: Added support for handling missing DLLs. Needed for macOS
   PySide6.5.0 from PyPI, which contains DLL references that are broken.
   With this feature, we can exclude DLLs that wouldn't work anyway.

**************
 Optimization
**************

-  Anti-Bloat: Remove ``IPython`` usage in ``huggingface_hub`` package
   versions. Added in 1.5.2 already.

-  Anti-Bloat: Avoid ``IPython`` usage in ``tokenizers`` module. Added
   in 1.5.4 already.

-  Added support for module type as a constant value. We want to add all
   types we have shapes for to allow better ``type(x)`` optimization.
   This is only the start.

-  Onefile: During payload unpacking the memory mapped data was copied
   to an input buffer. Removing that avoids memory copying and reduces
   usage.

-  Onefile: Avoid repeated directory creations. Without it, the
   bootstrap was creating already existing directories up to the root
   over and over, making many unnecessary file system checks. Added in
   1.5.5 already.

-  Anti-Bloat: Remove usage of ``IPython`` in ``trio`` package. Added in
   1.5.6 already.

-  Onefile: Use resource for payload on Win32 rather than overlay. This
   integrates better with signatures, removing the need to check for
   original file size. Changed in 1.5.6 already.

-  Onefile: Avoid using zstd input buffer, but using the memory mapped
   contents directly avoiding to copy uncompressed payload data. Changed
   in 1.5.6 already.

-  Onefile: Avoid double slashes in expanded onefile temp spec paths,
   they are just ugly.

-  Anti-Bloat: Remove usage of ``pytest`` and ``IPython`` for some
   packages used by newer ``torch``. Added in 1.5.7 already.

-  Anti-Bloat: Avoid ``triton`` to use setuptools. Added in 1.5.7
   already.

-  Anti-Bloat: Avoid ``pytest`` in newer ``networkx`` package. Added in
   1.5.7 already.

-  Prepare optimization for more built-in types with experimental code,
   but we need to disable it for now as it requires more completeness in
   code generation to cover them all. We did some, e.g. module type, but
   many more will be missing still.

-  Prepare optimization of class selection at compile time, by having a
   helper function rather than a dedicated node. This work is not
   complete though, and cannot be activated yet.

-  Windows: Cache short path name resolutions. Esp. for reporting, we
   now do a lot more of these than before, and this avoids they can
   become too time consuming.

-  Faster constant value handling for float value checks by avoiding
   module lookups per value.

-  Minimize size for hello world distribution such that no unused
   extension modules are included, by excluding even more modules and
   using modules from automatic inclusion of standard library.

-  Anti-Bloat: Catch ``pytest`` namespaces ``py`` and ``_pytest``
   sooner, to point to the actual uses more directly.

-  Anti-Bloat: Usage of ``doctest`` equals usage of "unittest" so cover
   it too, to point to the actual uses more directly.

-  Ever more spelling fixes in code and tests were identified and fixed.

-  Make sure side effect nodes indicate properly that they are raising,
   allowing exceptions to fully bubble up. This should lead to more dead
   code being recognized as such.

****************
 Organisational
****************

-  GitHub: Added marketplace action designed to cross platform build
   with Nuitka on GitHub directly. Usable with both standard and
   commercial Nuitka versions, and pronouncing it as officially
   supported.

   Check out out at `Nuitka-Action
   <https://github.com/Nuitka/Nuitka-Action>`__ repository.

-  Windows: When MSVC doesn't have WindowsSDK, just don't use it, and
   proceed, to e.g. allow fallback to winlibs gcc.

-  User Manual: The code to update benchmark numbers as giving was
   actually wrong. Fixed in 1.5.1 already.

-  UI: Make it clear that partially supported versions are considered
   experimental, not unsupported. Fixed in 1.5.2 already.

-  Plugins: Do not list deprecated plugins with ``plugin-list``, they do
   not have any effect, but listing them, makes people use them still.
   Fixed in 1.5.4 already.

-  Plugins: Make sure all plugins have descriptions. Some didn't have
   any yet, and sometimes the wording was improved. Fixed in 1.5.4
   already.

-  UI: Accept ``y`` as a shortcut for ``yes`` in prompts. Added in 1.5.5
   already.

-  Reports: Make sure the DLL dependencies for Linux are in a stable
   order. Added in 1.5.6 already.

-  Plugins: Check for latest fixes in PySide6. Added in 1.5.6 already.

-  Windows XP: For Python3.4 make using Python2 scons work again, we
   cannot have 3.5 or higher there. Added in 1.5.6 already.

-  Quality: Updated to latest PyLint. With Python 3.11 the older one,
   was not really working, and it was about time. Due to its many
   changes, we included it in the hotfix, so those can still be done.
   Changed in 1.5.7 already.

-  Release: Avoid broken ``requires.txt`` in source distribution. This
   apparently breaks poetry. Changed in 1.5.7 already.

-  GitHub: Enhanced issue template for more clarity, esp. to avoid
   unnecessary options, e.g. using ``--onefile`` for issues that show up
   with ``--standalone`` already, to report factory branch issues rather
   on Discord, and give a quick tip for a likely reproducer if a package
   fails to import.

-  User Manual: Added instructions on how to add a DLL or executable to
   a standalone distribution.

-  User Manual: Example paths in the table for path specs, meant for
   Windows were not properly escaping the backslashes and therefore
   rendered incorrectly.

-  Visual Code: Python3.11 is now the default configuration for C code
   editing.

-  Developer Manual: Updated descriptions for adding test suite. While
   added the Python 3.11 test suite, these instructions were further
   improved.

-  Debugging: Make it easier to fully deactivate free lists. Now only
   need to set max size to 0 and the free list will not be used.

-  Debugging: Added more assertions, added corrections to feature
   disables, check args after function calls for validity, check more
   types to be as expected.

-  Plugins: Enhanced plugin error messages generally, with ``--debug``
   exceptions become warning messages with the original exception being
   raised instead, making debugging during development much easier.

-  UI: Make it clear what not using ``ccache`` actually means. Not
   everybody is familiar with the design of Nuitka there or what the
   tool can actually do.

-  UI: Do not warn about not found distributions but merely inform of
   them.

   Since Nuitka is fully compatible with these, no need to consider
   those a warning, for some packages they also are given really a lot.

-  UI: Catch user error of wrong cases plugin names

   This now points out the proper name rather than denying the existence
   outright. We do not want to accept wrong case names silently.

**********
 Cleanups
**********

-  Use proper API for setting ``PyConfig`` values during interpreter
   initialization. There is otherwise always the risk of crashes, should
   these values change during runtime. Fixed in 1.5.2 already.

-  For our reformulations have a helper function that build release
   statements for multiple variables at once. This removed a bunch of
   repetitve code from re-formulations.

-  Move the pyi-file parser code out of the module nodes and to source
   handling, where it is more closely related.

*******
 Tests
*******

-  Adding a ``nuitka-watch`` tool, which is still experimental and for
   use with the `Nuitka-Watch
   <https://github.com/Nuitka/Nuitka-Watch>`__ repository.

-  Refined macOS standalone exceptions further to cover more normal
   usages of files on that OS and for frameworks that applications
   typically use from the system.

-  Detect and consider onefile mode if given in project options as well.

-  Was not really applying import check in programs tests. Added in
   1.5.6 already.

-  Added coverage of testing the signing of Windows binaries with the
   commercial plugin.

-  Added coverage of version information to hello world onefile test, so
   we can use it for Virus tools checks.

-  Added tests to cover PyQt6 and PySide6 plugin availability, we so far
   only had that for PyQt5, which is of course not relevant, and totally
   different code anyway.

-  Cleanup distutils tests case to use common test case scanning. We now
   decide version skips based on names, and had to get away from number
   suffixes, so they are now in the middle.

*********
 Summary
*********

The class bodies optimization has made some progress in this release,
going to a re-formulation of the metaclass selection, so as to allow its
future optimization. We are not yet at "compiled objects", but this is a
promising road. We need to make some optimization improvements for
inlining constant value calls, then this can become really important,
but by itself these changes do not yield a lot of improvement.

For macOS again a bunch of time was spent to improve and complete the
detection of DLL dependencies. More corner cases are covered now and
more packages just work fine as a result.

The most important is to become Python3.11 compatible, even if attribute
lookups, and other things, and not yet optimized. We will get to that in
future releases. For now, compatibility is the first step to take.

For GitHub users, the Nuitka-Action will be interesting. But it's still
in develop. We keep adding missing options of Nuitka for a while it
seems, but for most people it should be usable already.

The new ``nuitka-watch`` ability, should allow us to detect breaking
PyPI releases, that need a new tweak in Nuitka sooner. But it will
probably grow in the coming releases to full value only. For now the
tool itself is not yet finished.

From here, a few open ends in the CPython 3.11 test suite will have to
be addressed, and maybe some of the performance tricks that it now will
enable, e.g. with repeated attribute lookups.
