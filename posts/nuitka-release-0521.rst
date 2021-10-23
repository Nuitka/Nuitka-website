This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release focused on scalability work. Making Nuitka more usable in
the common case, and covering more standalone use cases.

***********
 Bug Fixes
***********

-  Windows: Support for newer MinGW64 was broken by a workaround for
   older MinGW64 versions.

-  Compatibility: Added support for the (unofficial) C-Python API
   ``Py_GetArgcArgv`` that was causing ``prctl`` module to fail loading
   on ARM platforms.

-  Compatibility: The proper error message template for complex call
   arguments is now detected as compile time. There are changes coming,
   that are already in some pre-releases of CPython.

-  Standalone: Wasn't properly ignoring ``Tools`` and other directories
   in the standard library.

**************
 New Features
**************

-  Windows: Detect the MinGW compiler arch and compare it to the Python
   arch. In case of a mismatch, the compiler is not used. Otherwise
   compilation or linking gives hard to understand errors. This also
   rules out MinGW32 as a compiler that can be used, as its arch doesn't
   match MinGW64 32 bits variant.

-  Compile modules in two passes with the option to specify which
   modules will be considered for a second pass at all (compiled without
   program optimization) or even become bytecode.

-  The developer mode installation of Nuitka in ``develop`` mode with
   the command ``pip install -e nuitka_git_checkout_dir`` is now
   supported too.

**************
 Optimization
**************

-  Popular modules known to not be performance relevant are no longer C
   compiled, e.g. ``numpy.distutils`` and many others frequently
   imported (from some other module), but mostly not used and definitely
   not performance relevant.

**********
 Cleanups
**********

-  The progress tracing and the memory tracing and now more clearly
   separate and therefore more readable.

-  Moved RPM related files to new ``rpm`` directory.

-  Moved documentation related files to ``doc`` directory.

-  Converted import sorting helper script to Python and made it run
   fast.

****************
 Organisational
****************

-  The Buildbot infrastructure for Nuitka was updated to Buildbot 0.8.12
   and is now maintained up to date with Ansible.

-  Upgraded the Nuitka bug tracker to Roundup 1.5.1 to which I had
   previously contributed security fixes already active.

-  Added SSL certificates from Let's Encrypt for the web server.

*********
 Summary
*********

This release advances the scalability of Nuitka somewhat. The two pass
approach does not yet carry all possible fruits. Caching of single pass
compiled modules should follow for it to become consistently fast.

More work will be needed to achieve fast and scalable compilation, and
that is going to remain the focus for some time.
