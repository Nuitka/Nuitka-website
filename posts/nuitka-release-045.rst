This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release incorporates very many bug fixes, most of which were already part
of hot fixes, usability improvements, documentation improvements, new logo,
simpler Python3 on Windows, warnings for recursion options, and so on. So it's
mostly a consolidation release.

Bug Fixes
---------

- When targeting Python 3.x, Nuitka was using "python" to run Scons to run it
  under Python 2.x, which is not good enough on systems, where that is already
  Python3. Improved to only do the guessing where necessary (i.e. when using
  the in-line copy of Scons) and then to prefer "python2". `Issue#95
  <http://bugs.nuitka.net/issue95>`__. Fixed in 0.4.4.1 already.

- When using Nuitka created binaries inside a "virtualenv", created programs
  would instantly crash. The attempt to load and patch ``inspect`` module was
  not making sure that ``site`` module was already imported, but inside the
  "virtualenv", it cannot be found unless. `Issue#96
  <http://bugs.nuitka.net/issue96>`__. Fixed in 0.4.4.1 already.

- The option ``--recurse-directory`` to include plugin directories was
  broken. `Issue#97 <http://bugs.nuitka.net/issue97>`__. Fixed in 0.4.4.2
  already.

- Python3: Files with "BOM" marker causes the compiler to crash. `Issue#98
  <http://bugs.nuitka.net/issue98>`__. Fixed in 0.4.4.2 already.

- Windows: The generated code for ``try``/``return``/``finally`` was working
  with gcc (and therefore MinGW), but not with MSVC, causing crashes.
  `Issue#102 <http://bugs.nuitka.net/issue102>`__. Fixed in 0.4.4.2 already.

- The option ``--recurse-all`` did not recurse to package ``__init__.py`` files
  in case ``from x.y import z`` syntax was used. `Issue#100
  <http://bugs.nuitka.net/issue100>`__. Fixed in 0.4.4.2 already.

- Python3 on macOS: Corrected link time error. Fixed in 0.4.4.2 already.

- Python3.3 on Windows: Fixed crash with too many arguments to a kwonly
  argument using function. Fixed in 0.4.4.2 already.

- Python3.3 on Windows: Using "yield from" resulted in a link time error. Fixed
  in 0.4.4.2 already.

- Windows: Added back XML manifest, found a case where it is needed to prevent
  clashes with binary modules.

- Windows: Generators only worked in the main Python threads. Some unusual
  threading modules therefore failed.

- Using ``sys.prefix`` to find the Python installation instead of hard coded
  paths. `Issue#103 <http://bugs.nuitka.net/issue103>`__.

New Features
------------

- Windows: Python3 finds Python2 installation to run Scons automatically now.

  Nuitka itself runs under Python3 just fine, but in order to build the
  generated C++ code into binaries, it uses Scons which still needs Python2.

  Nuitka will now find the Python2 installation searching Windows registry
  instead of requiring hard coded paths.

- Windows: Python2 and Python3 find their headers now even if Python is not
  installed to specific paths.

  The installation path now is passed on to Scons which then uses it.

- Better error checking for ``--recurse-to`` and ``--recurse-not-to``
  arguments, tell the user not to use directory paths.

- Added a warning for ``--recurse-to`` arguments that end up having no effect
  to the final result.

Cleanups
--------

- Import mechanism got cleaned up, stopped using "PyImport_ExtendInittab". It
  does not handle packages, and the ``sys.meta_path`` based importer is now
  well proven.

- Moved some of the constraint collection code mess into proper places. It
  still remains a mess.

Organizational
--------------

- Added ``LICENSE.txt`` file with Apache License 2.0 text to make it more
  immediately obvious which license Nuitka is under.

- Added section about Nuitka license to the "`User Manual
  <https://nuitka.net/doc/user-manual.html#license>`__".

- Added `Nuitka Logo <https://nuitka.net/doc/images/Nuitka-Logo-Symbol.png>`__
  to the distribution.

- Use Nuitka Logo as the bitmap in the Windows installer.

- Use Nuitka Logo in the documentation ("`User Manual
  <https://nuitka.net/doc/user-manual.html>`__" and "`Developer Manual
  <https://nuitka.net/doc/developer-manual.html>`__").

- Enhanced documentation to number page numbers starting after table of
  contents, removed header/footer from cover pages.

Summary
-------

This release is mostly the result of improvements made based on the surge of
users after Europython 2013. Some people went to extents and reported their
experience very detailed, and so I could aim at making e.g. their
misconceptions about how recursion options work, more obvious through warnings
and errors.

This release is not addressing performance improvements. The next release will
be able to focus on that. I am taking my claim of full compatibility very
serious, so any time it's broken, it's the highest priority to restore it.
