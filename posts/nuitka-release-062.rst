This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release has a huge focus on organizational things. Nuitka is growing in
terms of contributors and supported platforms.

Bug Fixes
---------

- Fix, the Python flag ``--python-flag=-O`` was removing doc strings, but that
  should only be done with ``--python-flag=-OO`` which was added too.

- Fix, accelerated binaries failed to load packages from the ``virtualenv``
  (not ``venv``) that they were created and ran with, due to not propagating
  ``sys.prefix``.

- Standalone: Do not include ``plat-*`` directories as frozen code, and also
  on some platforms they can also contain code that fails to import without
  error.

- Standalone: Added missing implicit dependency needed for newer NumPy
  versions.

New Features
------------

- Added support for Alpine Linux.

- Added support for MSYS2 based Python on Windows.

- Added support for Python flag ``--python flag=-OO``, which allows to remove
  doc strings.

- Added experimental support for ``pefile`` based dependency scans on Windows,
  thanks to Orsiris for this contribution.

- Added plugin for proper Tkinter standalone support on Windows, thanks to
  Jorj for this contribution.

- There is now a ``__compiled__`` attribute for each module that Nuitka has
  compiled. Should be like this now, and contains Nuitka version information
  for you to use, similar to what ``sys.version_info`` gives as a
  ``namedtuple`` for your checks.

  .. code-block:: python

    __nuitka_version__(major=0, minor=6, micro=2, releaselevel='release')

Optimization
------------

- Experimental code  for variant types for ``int`` and ``long`` values,
  that can be plain C value, as well as the ``PyObject *``. This is not
  yet completed though.

- Minor refinements of specialized code variants reducing them more often
  the actual needed code.

Organisational
--------------

- The Nuitka Github Organisation that was created a while ago and owns the
  Nuitka repo now, has gained members. Check out https://github.com/orgs/Nuitka/people
  for their list. This is an exciting transformation for Nuitka.

- Nuitka is participating in the GSoC 2019 under the PSF umbrella. We hope to
  grow even further. Thanks to the mentors who volunteered for this important
  task. Check out the
  `GSoC 2019 page <http://nuitka.net/pages/gsoc2019.html#mentors>`__ and thanks
  to the students that are already helping out.

- Added Nuitka internal `API documentation <http://nuitka.net/apidoc>`__ that
  will receive more love in the future. It got some for this release, but a
  lot is missing.

- The Nuitka code has been ``black``-ened and is formatted with an automatic
  tool now all the way, which makes contributors lives easier.

- Added documentation for questions received as part of the GSoC applications
  and ideas work.

- Some proof reading pull requests were merged for the documentation, thanks
  to everybody who addresses these kinds of errors. Sometimes typos, sometimes
  broken links, etc.

- Updated inline copy of Scons used for Python3 to 3.0.4, which hopefully means
  more bugs are fixed.

Summary
-------

This release is a sign of increasing adoption of Nuitka. The GSoC 2019 is
showing early effects, as is more developers joining the effort. These are
great times for Nuitka.

This release has not much on the optimization side that is user visible, but
the work that has begun is capable of producing glorious benchmarks once it
will be finished.

The focus on this and coming releases is definitely to open up the Nuitka
development now that people are coming in as permanent or temporary
contributors in (relatively) high numbers.
