.. post:: 2020/01/25 08:42
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.6.7
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release contains bug fixes and improvements to the packaging, for
the RPM side as well as for Debian, to cover Python3 only systems as
they are now becoming more common.

***********
 Bug Fixes
***********

-  Compatibility: The value of ``__module__`` for extension modules was
   not dependent into which package the module was loaded, it now is.

-  Anaconda: Enhanced detection of Anaconda for Python 3.6 and higher.

-  CentOS6: Detect gcc version to allow saving on macro memory usage,
   very old gcc didn't have that.

-  Include Python3 for all Fedora versions where it works as well as for
   openSUSE versions 15 and higher.

-  Windows: Using short path names to interact with Scons avoids
   problems with unicode paths in all cases.

-  macOS: The usage of ``install_name_tool`` could sometimes fail due to
   length limits, we now increase it at link time.

-  macOS: Do not link against ``libpython`` for module mode. This
   prevented extension modules from actually being usable.

-  Python3.6: Follow coroutine fixes in our asyncgen implementation as
   well.

-  Fix, our version number handling could overflow with minor versions
   past 10, so we limited it for now.

**************
 New Features
**************

-  Added support for Python 3.8, the experimental was already there and
   pretty good, but now added the last obscure features too.

-  Plugins can now provide C code to be included in the compilation.

-  Distutils: Added targets ``build_nuitka`` and ``install_nuitka`` to
   complement ``bdist_nuitka``, so we support software other than
   wheels, e.g. RPM packaging that compiles with Nuitka.

-  Added support for ``lldb`` the Clang debugger with the ``--debugger``
   mode.

**************
 Optimization
**************

-  Make the file prefix map actually work for gcc and clang, and compile
   files inside the build folder, unless we are running in debugger
   mode, so we use ``ccache`` caching across different compilations for
   at least the static parts.

-  Avoid compilation of ``__frozen.c`` in accelerated mode, it's not
   used.

-  Prefer using the inline copy of scons over systems scons. The later
   will only be slower. Use the fallback to external scons only from the
   Debian packages, since there we consider it forbidden to include
   software as a duplicate.

****************
 Organisational
****************

-  Added recommended plugins for Visual Code, replacing the list in the
   Developer Manual.

-  Added repository for Fedora 30 for download.

-  Added repository for CentOS 8 for download.

-  Updated inline copy of Scons used for Python3 to 3.1.2, which is said
   to be faster for large compilations.

-  Removed Eclipse setup from the manual, it's only infererior at this
   point and we do not use it ourselves.

-  Debian: Stop recommending PyQt5 in the package, we no longer use it
   for built-in GUI that was removed.

-  Debian: Bumped the standards version and modernized the packaging,
   solving a few warnings during the build.

**********
 Cleanups
**********

-  Scons: Avoid to add Unix only include paths on Windows.

-  Scons: Have the static source code in a dedicated folder for clarity.

*******
 Tests
*******

-  Added tests to Github Actions, for the supported Python versions for
   all of Linux, macOS and Windows, covering the later publicly for the
   first time. We use Anaconda on macOS for the tests now, rather than
   Homebrew.

-  Enable IO encoding to make sure we use UTF8 for more test suites that
   actually need it in case of problems.

-  Comparing module outputs now handles segfaults by running in the
   debugger too.

*********
 Summary
*********

This release adds full support for Python 3.8 finally, which took us a
while, and it cleans up a lot on the packaging side. There aren't that
many important bug fixes, but it's still nice to this cleaned up.

We have important actual optimization in the pipeline that will apply
specialization to target types and for comparison operations. We expect
to see actual performance improvements in the next release again.
