This is to inform you about the new stable release
of `Nuitka <https://nuitka.net>`_. It is the extremely
compatible Python compiler,  `"download now" </doc/download.html>`_.

This releases contains important bug fixes for regressions of the 0.6.8
series which had relatively many problems. Not all of these could be
addressed as hotfixes, and other issues were even very involved, causing
many changes to be necessary.

There are also many general improvements and performance work for
tracing and loops, but the full potential of this will not be unlocked
with this release yet.

Bug Fixes
=========

-  Fix, loop optimization sometimes didn't determinate, effectively
   making Nuitka run forever, with no indication why. This has been
   fixed and a mechanism to give up after too many attempts has been
   added.

-  Fix, closure taking object allowed a brief period where the garbage
   collector was exposed to uninitialized objects. Fixed in 0.6.8.1
   already.

-  Python3.6+: Fix corruption for exceptions thrown into asyncgen. Fixed
   in 0.6.8.1 already.

-  Fix, deleting variables detected as C type bool could raise an
   ``UnboundLocalError`` that was wrong. Fixed in 0.6.8.1 already.

-  Python3.8.3+: Fix, future annotations parsing was using hard coded
   values that were changed in CPython, leading to errors.

-  Windows: Avoid encoding issues for Python3 on more systems, by going
   from wide characters to unicode strings more directly, avoiding an
   encoding as UTF8 in the middle. Fixed in 0.6.8.2 already.

-  Windows: Do not crash when warning about uninstalled MSVC using
   Python3. This is a Scons bug that we fixed. Fixed in 0.6.8.3 already.

-  Standalone: The output of dependency walker should be considered as
   "latin1" rather than UTF8. Fixed in 0.6.8.3 already.

-  Standalone: Added missing hidden dependencies for ``flask``. Fixed in
   0.6.8.1 already.

-  Standalone: Fixed ``win32com.client`` on Windows. Fixed in 0.6.8.1
   already.

-  Standalone: Use ``pkgutil`` to scan encoding modules, properly
   ignoring the same files as Python does in case of garbage files being
   there. Fixed in 0.6.8.2 already.

-  Plugins: Enabling a plugin after the filename to compile was given,
   didn't allow for arguments to the passed, causing problems. Fixed in
   0.6.8.3 already.

-  Standalone: The ``certifi`` data file is now supported for all
   modules using it and not only some.

-  Standalone: The bytecode for the standard library had filenames
   pointing to the original installation attached. While these were not
   used, but replaced at runtime, they increased the size of the binary,
   and leaked information.

-  Standalone: The path of ``sys.executable`` was not None, but pointing
   to the original executable, which could also point to some temporary
   virtualenv directory and therefore not exist, also it was leaking
   information about the original install.

-  Windows: With the MSVC compiler, elimination of duplicate strings was
   not active, causing even unused strings to be present in the binary,
   some of which contained file paths of the Nuitka installation.

-  Standalone: Added support for pyglet.

-  Plugins: The command line handling for Pmw plugin was using wrong
   defaults, making it include more code than necessary, and to crash if
   it was not there.

New Features
============

-  Windows: Added support for using Python 2.7 through a symlink too.
   This was already working for Python3, but a scons problem prevented
   this from working.

-  Caching of compiled C files is now checked with ccache and clcache,
   and added automatically where possible, plus a report of the success
   is made. This can accelerate the re-compile very much, even if you
   have to go through Nuitka compilation itself, which is not (yet)
   cached.

-  Added new ``--quiet`` option that will disable informational traces
   that are going to become more.

-  The Clang from MSVC installation is now picked up for both 32 and 64
   bits and follows the new location in latest Visual Studio 2019.

-  Windows: The ``ccache`` from Anaconda is now supported as well as the
   one from msys64.

Optimization
============

-  The value tracing has become more correct with loops and in general
   less often inhibits optimization. Escaping of value traces is now a
   separate trace state allowing for more appropriate handling of actual
   unknowns.

-  Memory used for value tracing has been lowered by removing
   unnecessary states for traces, that we don't use anymore.

-  Windows: Prevent scons from scanning for MSVC when asked to use
   MinGW64. This avoids a performance loss doing something that will
   then end up being unused.

-  Windows: Use function level linking with MSVC, this will allow for
   smaller binaries to be created, that don't have to include unused
   helper functions.

Cleanups
========

-  The scons file now uses Nuitka utils functions and is itself split up
   into several modules for enhanced readability.

-  Plugin interfaces for providing extra entry points have been cleaned
   up and now named tuples are used. Backward compatibility is
   maintained though.

Organisational
==============

-  The use of the logging module was replaced with more of our custom
   tracing and we now have the ability to write the optimization log to
   a separate file.

-  Old style plugin options are now detected and reported as a usage
   error rather than unknown plugin.

-  Changed submodules to use git over https, so as to not require ssh
   which requires a key registered and causes problems with firewalls
   too.

-  More correct Debian copyright file, made formatting of emails in
   source code consistent.

-  Added repository for Ubuntu focal.

Summary
=======

The main focus of this release has been bug fixes with only a little
performance work due to the large amount of regressions and other
findings from the last release.

The new constants loading for removes a major scalability problem. The
checked and now consistently possible use of ``ccache`` and ``clcache``
allows for much quicker recompilation. Nuitka itself can still be slow
in some cases, but should have seen some improvements too. Scalability
will have to remain a focus for the next releases too.

The other focus, was to make the binaries contain no original path
location, which is interesting for standalone mode. Nuitka should be
very good in this area now.

For optimization, the new loop code is again better. But it was also
very time consuming, to redo it, yet again. This has prevented other
optimization to be added.

And then for correctness, the locals scope work, while very invasive,
was necessary, to handle the usage of locals inside of contractions, but
also will be instrumental for function inlining to become generally
available.

So, ultimately, this release is a necessary intermediate step. Upcoming
releases will be able to focus more clearly on run time performance
again as well as on scalability for generated C code.
