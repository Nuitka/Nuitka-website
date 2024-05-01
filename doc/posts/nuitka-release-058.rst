.. post:: 2015/01/16 05:04
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

######################
 Nuitka Release 0.5.8
######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release has mainly a focus on cleanups and compatibility
improvements. It also advances standalone support, and a few
optimization improvements, but it mostly is a maintenance release,
attacking long standing issues.

***********
 Bug Fixes
***********

-  Compatibility Windows macOS: Fix importing on case insensitive
   systems.

   It was not always working properly, if there was both a package
   ``Something`` and ``something``, by merit of having files
   ``Something/__init__.py`` and ``something.py``.

-  Standalone: The search path was preferring system directories and
   therefore could have conflicting DLLs.

-  Fix, the optimization of ``getattr`` with predictable result was
   crashing the compilation. This was a regression, fixed in 0.5.7.1
   already.

-  Compatibility: The name mangling inside classes also needs to be
   applied to global variables.

-  Fix, providing ``clang++`` for ``CXX`` was mistakenly thinking of it
   as a ``g++`` and making version checks on it.

-  Python3: Declaring ``__class__`` global is now a ``SyntaxError``
   before Python3.4.

-  Standalone Python3: Making use of module state in extension modules
   was not working properly.

**************
 New Features
**************

-  The filenames of source files as found in the ``__file__`` attribute
   are now made relative in standalone mode.

   This should make it more apparent if things outside of the
   distribution folder are used, at the cost of tracebacks. Expect the
   default ability to copy the source code along in an upcoming release.

-  Added experimental standalone mode support for PyQt5. At least
   headless mode should be working, plugins (needed for anything
   graphical) are not yet copied and will need more work.

*********
 Cleanup
*********

-  No longer using ``imp.find_module`` anymore. To solve the casing
   issues we needed to make our own module finding implementation
   finally.

-  The name mangling was handled during code generation only. Moved to
   tree building instead.

-  More code generation cleanups. The compatible line numbers are now
   attached during tree building and therefore better preserved, as well
   as that code no longer polluting code generation as much.

****************
 Organizational
****************

-  No more packages for openSUSE 12.1/12.2/12.3 and Fedora 17/18/19 as
   requested by the openSUSE Build Service.

-  Added RPM packages for Fedora 21 and CentOS 7 on openSUSE Build
   Service.

*******
 Tests
*******

-  Lots of test refinements for the CPython test suites to be run
   continuously in Buildbot for both Windows and Linux.

*********
 Summary
*********

This release brings about two major changes, each with the risk to break
things.

One is that we finally started to have our own import logic, which has
the risk to cause breakage, but apparently currently rather improved
compatibility. The case issues were not fixable with standard library
code.

The second one is that the ``__file__`` attributes for standalone mode
is now no longer pointing to the original install and therefore will
expose missing stuff sooner. This will have to be followed up with code
to scan for missing "data" files later on.

For SSA based optimization, there are cleanups in here, esp. the one
removing the name mangling, allowing to remove special code for class
variables. This makes the SSA tree more reliable. Hope is that the big
step (forward propagation through variables) can be made in one of the
next releases.
