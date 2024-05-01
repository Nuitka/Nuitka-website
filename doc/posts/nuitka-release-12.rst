.. post:: 2022/11/26 09:23
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 1.2
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release contains a large amount of new compatibility features and a
few new optimization, while again consolidating what we have.
Scalability should be better in many cases.

***********
 Bug Fixes
***********

-  Standalone: Added implicit dependency of ``thinc`` backend. Fixed in
   1.1.1 already.

-  Python3.10: Fix, ``match`` statements with unnamed star matches could
   give incorrect results. Fixed in 1.1.1 already.

      .. code:: python

         match x:
            case [*_, y]:
                  ... # y had wrong value here.

-  Python3.9+: Fix, file reader objects must convert to ``str`` objects.
   Fixed in 1.1.1 already.

      .. code:: python

         # This was the `repr` rather than a path value, but it must be usable
         # like that too.
         str(importlib.resources.files("package_name").joinpath("lala"))

-  Standalone: Added data file of ``echopype`` package. Fixed in 1.1.1
   already.

-  Anti-Bloat: Remove non-sense warning of compiled ``pyscf``. Fixed in
   1.1.1 already.

-  macOS: Fix, in LTO mode using ``incbin`` can fail, switch to source
   mode for constants resources. Fixed in 1.1.2 already.

-  Standalone: Add support for ``sv_ttk`` module. Fixed in 1.1.2
   already.

-  macOS: Fix, was no longer correcting ``libpython`` path, this was a
   regression preventing CPython for creating properly portable binary.
   Fixed in 1.1.2 already.

-  macOS: Fix, main binary was not included in signing command. Fixed in
   1.1.3 already.

-  Standalone: Added implicit dependency of ``orjson``. Due to
   ``zoneinfo`` not being automatically included anymore, this was
   having a segfault. Fixed in 1.1.3 already.

-  Standalone: Added support for new ``shapely``. Fixed in 1.1.4
   already.

-  macOS: Ignore extension module of non-matching architecture. Some
   wheels contain extension modules for only ``x86_64`` arch, and others
   contain them only for ``arm64``, preventing the standalone build.
   Fixed in 1.1.4 already.

-  Standalone: Added missing ``sklearn`` dependencies. Fixed in 1.1.4
   already.

-  Fix, packages available through relative import paths could be
   confused with the same ones imported by absolute paths. This should
   be very hard to trigger, by normal users, but was seen during
   development. Fixed in 1.1.4 already.

-  Standalone: Apply import hacks for ``pywin32`` modules only on
   Windows, otherwise it can break e.g. macOS compilation. Fixed in
   1.1.4 already.

-  Windows: More robust DLL dependency caching, otherwise e.g. a Windows
   update can break things. Also consider plugin contribution, and
   Nuitka version, to be absolutely sure, much like we already do for
   bytecode caching. Fixed in 1.1.4 already.

-  Standalone: Fix, ``seaborn`` needs the same workaround as ``scipy``
   for corruption with MSVC. Fixed in 1.1.4 already.

-  UI: Fix, the ``options-nanny`` was no longer functional and therefore
   failed to warn about non working options and package usages. Fixed in
   1.1.5 already.

-  macOS: Do not use extension modules of non-matching architecture.
   Fixed in 1.1.5 already.

-  Windows: Fix, resolving symlinks could fail for spaces in paths.
   Fixed in 1.1.6 already.

-  Standalone: Added missing DLL for ``lightgbm`` module. Fixed in 1.1.6
   already.

-  Compatibility: Respect ``super`` module variable. It is now possible
   to have a module level change of ``super`` but still get compatible
   behavior with Nuitka. Fixed in 1.1.6 already.

-  Compatibility: Make sure we respect ``super`` overloads in the
   builtin module. Fixed in 1.1.6 already.

-  Fix, the anti-bloat replacement code for ``numpy.testing`` was
   missing a required function. Fixed in 1.1.6 already.

-  Fix, ``importlib.import_module`` static optimization was mishandling
   a module name of ``.`` with a package name given. Fixed in 1.1.6
   already.

-  macOS: Fix, some extension modules use wrong suffixes in self
   references, we need to not complain about this kind of error. Fixed
   in 1.1.6 already.

-  Fix, do not make ``ctypes.wintypes`` a hard import on non-Windows.
   Nuitka asserted against it failing, where some code handles it
   failing on non-Windows platforms. Fixed in 1.1.6 already.

-  Standalone: Added data files for ``vedo`` package. Fixed in 1.1.7
   already.

-  Plugins: Fix, the ``gi`` plugin did always set ``GI_TYPELIB_PATH``
   even if already present from user code. Also it did not handle errors
   to detect its value during compile time. Fixed in 1.1.7 already.

-  Standalone: Added missing dependencies for ``sqlalchemy`` to have all
   SQL backends working. Fixed in 1.1.7 already.

-  Added support Nixpkgs's default non-writable ``HOME`` directory.
   Fixed in 1.1.8 already.

-  Fix, distribution metadata name and package name need not align, need
   to preserve the original looked up name from
   ``importlib.metadata.distribution`` call. Fixed in 1.1.8 already.

-  Windows: Fix, catch usage of unsupported ``CLCACHE_MEMCACHED`` mode
   with MSVC compilation. It is just unsupported.

-  Windows: Fix, file version was spoiled from product version if it was
   the only version given.

-  Windows: The default for file description in version information was
   not as intended.

-  Plugins: Workaround for PyQt5 as contained in Anaconda providing
   wrong paths from the build machine.

-  macOS: After signing a binary with a certificate, compiling the next
   one was crashing on a warning about initially creating an ad-hoc
   binary.

-  Fix, detect case of non-writable cache path, make explaining error
   exit rather than crashing attempting to write to the cache.

-  macOS: Added support for ``pyobjc`` in version 9.0 or higher.

**************
 New Features
**************

-  Python3.11: For now prevent the execution with 3.11 and give a
   warning to the user for a not yet supported version. This can be
   overridden with ``--experimental=python311`` but at this times will
   not compile anything yet due to required and at this time missing
   core changes.

-  macOS: Added option ``--macos-sign-notarization`` that signs with
   runtime signature, but requires a developer certificate from Apple.
   As its name implies, this is for use with notarization for their App
   store.

-  DLLs used via ``delvewheel`` were so far only handled in the ``zmq``
   plugin, but this has been generalized to cover any package using it.
   With that, e.g. ``shapely`` just works. This probably helps many
   other packages as well.

-  Added ``__compiled__`` and ``__compiled_constant__`` attributes to
   compiled functions.

   With this, it can be decided per function what it is and bridges like
   ``pyobjc`` can use it to create better code on their side for
   constant value returning functions.

-  Added ``support_info`` check to Nuitka package format. Make it clear
   that ``pyobjc`` is only supported after ``9.0`` by erroring out if it
   has a too low version. It will not work at all before that version
   added support in upstream. Also using this to make it clear that
   ``opencv-python`` is best supported in version 4.6 or higher. It
   seems e.g. that video capture is not working with 4.5 at this time.

-  Added ``--report-template`` which can be used to provide Jinja2
   templates to create custom reports, and refer to built-in reports, at
   this time e.g. a license reports.

**************
 Optimization
**************

-  Trust the absence of a few selected hard modules and convert those to
   static raises of import errors.

-  For conditional nodes where only one branch exits, and the other does
   not, no merging of the trace collection should happen. This should
   enhance the scalability and leads to more static optimization being
   done after these kinds of branches on variables assigned in such
   branches.

   .. code:: python

      if condition1:
         a = 1
      else:
         raise KeyError

      if condition2:
         b = 1

      # Here, "a" is known to be assigned, but before it was only "maybe"
      # assigned, like "b" would have to be since, the branch may or may
      # not have been taken.

-  Do not merge tried blocks that are aborting with an exception handler
   that is not aborting. This is very similar to the change for
   conditional statements, again there is a control flow branch, that
   may have to be merged with an optional part, but sometimes that part
   is not optional from the perspective of the code following.

   .. code:: python

      try:
         ... # potentially raising, but not aborting code
         return something() # this aborts
      except Exception:
         a = 1

      try:
         ... # potentially raising, but not aborting code
      except Exception:
         b = 1

      # Here, "a" is known to be assigned, but before it was only "maybe"
      # assigned, like "b" would have to be since, the branch may or may
      # not have been taken.

-  Exception matches were annotating a control flow escape and an
   exception exit, even when it is known that no error is possible to be
   happening that comparison.

   .. code:: python

      try:
         ...
      except ImportError: # an exception match is done here, that cannot raise
         ...

-  Trust ``importlib.metadata.PackageNotFoundError`` to exist, with this
   some more metadata usages are statically optimized. Added in 1.1.4
   already.

-  Handle constant values from trusted imports as trusted values. So
   far, trusted import values were on equal footing to regular
   variables, which on the module level could mean that no optimization
   was done, due to control flow escapes happening.

   .. code:: python

      # Known to be False at compile time.
      from typing import TYPE_CHECKING
      ...

      if TYPE_CHECKING:
         from something import normally_unused_unless_type_checking

   In this code example above, the static optimization was not done
   because the value may be changed on the outside. However, for trusted
   constants, this is no longer assumed to be happening. So far only
   ``if typing.TYPE_CHECKING:`` using code had been optimized.

-  macOS: Use sections for main binary constants binary blob rather than
   C source code (which we started in a recent hotfix due to LTO issues
   with incbin) and onefile payload. The latter enables notarization of
   the onefile binary as well and makes it faster to unpack as well.

-  Windows: Do not include DLLs from SxS. For PyPI packages these are
   generally unused, and self compiled modules won't be SxS
   installations either. We can add it back where it turns out needed.
   This avoids including ``comctl32`` and similar DLLs, which ought to
   come from the OS, and might impede backward compatibility only.

-  Disabled C compilation of very large ``azure`` modules.

-  The per module usage information of other modules was only updated in
   first pass was used in later passes. But since they can get optimized
   away, we have to update every time, avoiding to still include unused
   modules.

-  Anti-Bloat: Fight the use of ``dask`` in ``xarray`` and ``pint``,
   adding a mode controlling its use. This is however still incomplete
   and needs more work.

-  Fix, the anti-bloat configuration for ``rich.pretty`` introduced a
   ``SyntaxError`` that went unnoticed. In the future compilation will
   abort when this happens.

-  Standalone: Added support for including DLLs of ``llvmlite.binding``
   package.

-  Anti-Bloat: Avoid using ``pywin32`` through ``pkg_resources`` import.
   This seems rather pointless and follows an optimization done for the
   inline copy of Nuitka already, the ``ctypes`` code path works just
   fine, and this may well be the only reason why ``pywin32`` is
   included, which is by itself relatively large.

-  Cache directory contents when scanning for modules. The ``sys.path``
   and package directories were listed over and over, wasting time
   during the import analysis.

-  Optimization: Was not caching not found modules, but retrying every
   time for each usage, potentially wasting time during import analysis.

-  Anti-Bloat: Initial work to avoid ``pytest`` in patsy, it is however
   incomplete.

****************
 Organizational
****************

-  User Manual: Explain how to create 64/32 bits binaries on Windows,
   with there being no option to control it, this can otherwise be a bit
   unobvious that you have to just use the matching Python binary.

-  UI: Added an example for a cached onefile temporary location spec to
   the help output of ``--onefile-tempdir-spec`` to make cached more
   easy to achieve in the proper way.

-  UI: Quote command line options with space in value better, no need to
   quote an affected command line option in its entirety, and it looks
   strange.

-  macOS: Catch user error of disabling the console without using the
   bundle mode, as it otherwise it has no effect.

-  macOS: Warn about not providing an icon with disabled console,
   otherwise the dock icon is empty, which just looks bad.

-  Debian: Also need to depend on ``glob2`` packages which the yaml
   engine expects to use when searching for DLLs.

-  Debian: Pertain inline copies of modules in very old builds, there is
   e.g. no ``glob2`` for older releases, but only recent Debian releases
   need very pure packages, our backport doesn't have to do it right.

-  macOS: More reliable detection of Homebrew based Python. Rather than
   checking file system via its ``sitecustomize`` contents. The
   environment variables are only present to some usages.

-  Installations with pip did not include all license, README files,
   etc. which however was intended. Also the attempt to disable bytecode
   compilation for some inline copies was not effective yet.

-  Renamed ``pyzmq`` plugin to ``delvewheel`` as it is now absolutely
   generic and covers all uses of said packaging technique.

-  Caching: Use cache directory for cached downloads, rather than
   application directory, which is just wrong. This will cause all
   previously cached downloads to become unused and repeated.

-  Quality: Updated development requirements to latest ``black``,
   ``isort``, ``yamllint``, and ``tqdm``.

-  Visual Code: Added recommendation for extension for Debian packaging
   files.

-  Added warning for ``PyQt5`` usage, since its support is very
   incomplete. Made the ``PyQt6`` warning more concrete. It seems only
   Qt threading does not work, which is of course still significant.
   Instead PySide2 and PySide6 are recommended.

-  UI: Have dedicated options group for onefile, the spec for the
   temporary files is not a Windows option at all anymore. Also move the
   warnings group to the end, people need to see the inclusion related
   group first.

-  User Manual: Explain how to create 64/32 bits binaries on Windows,
   which is not too obvious.

**********
 Cleanups
**********

-  Moved PySide plugins DLL search extra paths to the Yaml
   configuration. In this way it is not dependent on the plugin being
   active, avoiding cryptic errors on macOS when they are not found.

-  Plugins: Avoid duplicate link libraries due to casing. We are now
   normalizing the link library names, which avoids e.g. ``Shell32`` and
   ``shell32`` to be in the result.

-  Cleanups to prepare a PyLint update that so otherwise failed due to
   encountered issues.

-  Plugins: Pass so called build definitions for generically. Rather
   than having dedicated code for each, and plugins can now provide them
   and pass their index to the scons builds.

-  Onefile: Moved file handling code to common code reducing code
   duplication and heavily cleaning up the bootstrap code generally.

-  Onefile: The CRC32 checksum code was duplicated between constants
   blob and onefile, and has moved to shared code, with an actual
   interface to take the checksum.

-  Spelling cleanups resumed, e.g. this time more clearly distinguishing
   between ``run time`` and ``runtime``, the first is when the program
   executes, but the latter can be an environment provided by a C
   compiler.

*******
 Tests
*******

-  Tests: Added test that applies anti-bloat configuration to all found
   modules.

-  Tests: Tests: Avoid including unused ``nuitka.tools`` code in
   reflected test, which should make it faster. The compiler itself
   doesn't use that code.

*********
 Summary
*********

This release is again mainly a consolidation of previous release, as
well as finishing off existing features. Optimization added in previous
releases should have all regressions fixed now, again with a strong
series of hotfixes.

New optimization was focused around findings with static optimization
not being done, but still resulting in general improvements. Letting
static optimization drive the effort is still paying off.

Scalability has seen improvements through some of the optimization, this
time a lot less anti-bloat work has been done, and some things are only
started. The focus will clearly now shift to making this a community
effort. Expect postings that document the Yaml format we use.

For macOS specifically, with the sections work, onefile should launch
faster, should be more compatible with signing, and can now be used in
notarization, so for that platform, things are more round.

For Windows, a few issues with version information and onefile have been
addressed. We should be able to use memory mapped view on this platform
too, for faster unpacking of the payload, since it doesn't have to go
through the file anymore.
