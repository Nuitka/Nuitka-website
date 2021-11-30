This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This has a focus on organisational improvements. With more and more
people joining Nuitka, normal developers as well as many GSoC 2019
students, the main focus was to open up the development tools and
processes, and to improve documentation.

That said, an impressive amount of bug fixes was contributed, but
optimization was on hold.

Bug Fixes
=========

-  Windows: Added support for running compiled binaries in unicode path
   names.

-  Standalone: Added support for crytodomex and pycparser packages.

-  Standalone: Added support for OpenSSL support in PyQt on Windows.

-  Standalone: Added support for OpenGL support with QML in PyQt on
   Windows.

-  Standalone: Added support for SciPy and extended the NumPy plugin to
   also handle it.

-  UI: The option ``--plugin-list`` still needed a positional argument
   to work.

-  Make sure ``sys.base_prefix`` is set correctly too.

-  Python3: Also make sure ``sys.exec_prefix`` and
   ``sys.base_exec_prefix`` are set correctly.

-  Standalone: Added platform plugins for PyQt to the default list of
   sensible plugins to include.

-  Fix detection of standard library paths that include ``..`` path
   elements.

Optimization
============

-  Avoid static C++ runtime library when using MinGW64.

New Features
============

-  Plugins: A plugin may now also generate data files on the fly for a
   given module.

-  Added support for FreeBSD/PowerPC arch which still uses ``gcc`` and
   not ``clang``.

Organisational
==============

-  Nuitka is participating in the GSoC 2019.

-  Added documentation on how to create or use Nuitka plugins.

-  Added more API doc to functions that were missing them as part of the
   ongoing effort to complete it.

-  Updated to latest PyLint 2.3.1 for checking the code.

-  Scons: Using newer Scons inline copy with Python 2.7 as, the old one
   remains only used with Python 2.6, making it easier to know the
   relevant code.

-  Autoformat was very much enhanced and handles C and ReST files too
   now. For Python code it does pylint comment formatting, import
   statement sorting, and blackening.

-  Added script ``misc/install-git-hooks.py`` that adds a commit hook
   that runs autoformat on commit. Currently it commits unstaged content
   and therefore is not yet ready for prime time.

-  Moved adapted CPython test suites to `Github repository under Nuitka
   Organisation <https://github.com/Nuitka/Nuitka-CPython-tests>`__.

-  Moved Nuitka-website repository to `Github repository under Nuitka
   Organisation <https://github.com/Nuitka/Nuitka-website>`__.

-  Moved Nuitka-speedcenter repository to `Github repository under
   Nuitka Organisation
   <https://github.com/Nuitka/Nuitka-speedcenter>`__.

-  There is now a `Gitter chat for Nuitka community
   <https://gitter.im/Nuitka-chat/community>`__.

-  Many typo and spelling corrections on all the documentation.

-  Added short installation guide for Nuitka on Windows.

Cleanups
========

-  Moved commandline parsing helper functions from common code helpers
   to the main program where of course their only usage is.

-  Moved post processing of the created standalone binary from main
   control to the freezer code.

-  Avoid using ``chmod`` binary to remove executable bit from created
   extension modules.

-  Windows: Avoid using ``rt.exe`` and ``mt.exe`` to deal with copying
   the manifest from the ``python.exe`` to created binaries. Instead use
   new code that extracts and adds Windows resources.

-  Fixed many ``ResourceWarnings`` on Python3 by improved ways of
   handling files.

-  Fixed deprecation warnings related to not using ``collections.abc``.

-  The runners in ``bin`` directory are now formatted with ``black``
   too.

Tests
=====

-  Detect Windows permission errors for two step execution of Nuitka as
   well, leading to retries should they occur.

-  The salt value for CPython cached results was improved to take more
   things into account.

-  Tests: Added more trick assignments and generally added more tests
   that were so far missing.

Summary
=======

With the many organisational changes in place, my normal work is
expected to resume for after and yield quicker improvements now.

It is also important that people are now enabled to contribute to the
Nuitka web site and the Nuitka speedcenter. Hope is to see more
improvements on this otherwise neglected areas.

And generally, it's great to see that a community of people is now
looking at this release in excitement and pride. Thanks to everybody who
contributed!
