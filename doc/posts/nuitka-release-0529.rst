.. post:: 2018/03/28 00:45
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.5.29
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release comes with a lot of improvements across the board. A lot of
focus has been givevn to the packaging side of Nuitka, but also there is
a lot of compatibility work.

***********
 Bug Fixes
***********

-  Windows: When using Scons for Python3 and Scons for Python2 on the
   same build directory, a warning would be given about the need to
   migrate. Make the Scons cache directory use the Python ABI version as
   a key too, to avoid these issues. Fixed in 0.5.28.1 already.

-  Windows: Fixup for Python3 and Scons no more generating the MinGW64
   import library for Python anymore properly. Was only working if
   cached from a previous install of Nuitka. Fixed in 0.5.28.1 already.

-  Plugins: Made the data files plugin mandatory and added support for
   the scrapy package needs.

-  Fix, added implicit dependencies for ``pkg_resources.external``
   package. Fixed in 0.5.28.1 already.

-  Fix, an import of ``x.y`` where this was not a package didn't cause
   the package ``x`` to be included.

-  Standalone: Added support for ``six.moves`` and ``requests.packages``
   meta imports, these cause hidden implicit imports, that are now
   properly handled.

-  Standalone: Patch the ``__file__`` value for technical bytecode
   modules loaded during Python library initialization in a more
   compatible way.

-  Standalone: Extension modules when loaded might actually raise legit
   errors, e.g. ``ImportError`` of another module, don't make those into
   ``SystemError`` anymore.

-  Python3.2: The ``__package__`` of sub-packages was wrong, which could
   cause issues when doing relative imports in that sub-package.

-  Python3: Contractions in a finally clause could crash the compiler.

-  Fix, unused closure variables could lead to a crash in they were
   passed to a nested function.

-  Linux: Standalone dependency analysis could enter an endless
   recursion in case of cyclic dependencies.

-  Python3.6: Async generation expressions need to return a ``None``
   value too.

-  Python3.4: Fix, ``__spec__`` is a package attribute and not a
   built-in value.

**************
 New Features
**************

-  It is now possible to run Nuitka with ``some_python_you_choose -m
   nuitka ...`` and therefore know exactly which Python installation is
   going to be used. It does of course need Nuitka installed for this to
   work. This mechanism is going to replace the ``--python-version``
   mechanism in the future.

-  There are dedicated runners for Python3, simply use ``nuitka3`` or
   ``nuitka3-run`` to execute Nuitka if your code is Python3 code.

-  Added warning for implicit exception raises due to mismatch in
   unpacking length. These are statically detected, but so far were not
   warned about.

-  Added cache for ``depends.exe`` results. This speeds up standalone
   mode again as some of these calls were really slow.

-  The import tracer is more robust against recursion and works with
   Python3 now.

-  Added an option to assume yes for downloading questions. The
   currently only enables the download of ``depends.exe`` and is
   intended for CI servers.

-  There is now a report file for scons, which records the values used
   to run things, this could be useful for debugging.

-  Nuitka now registers with distutils and can be used with
   ``bdist_wheel`` directly, but this lacks documentation and tests.
   Many improvements in the distutils build.

**************
 Optimization
**************

-  Forward propagate compile time constants even if they are only
   potential usages. This is actually the case where this makes the most
   sense, as it might remove its use entirely from the branches that do
   not use it.

-  Avoid extra copy of ``finally`` code. The cloning operation takes
   time and memory, and this shaved of 0.3% of Nuitka memory usage, as
   these can also become dangling.

-  Class dictionaries are now proper dictionarties in optimization,
   using some dedicated code for name lookups that are transformed to
   dedicated locals dictionary or mapping (Python3) accesses. This
   currently does not fully optimize, but will in coming releases, and
   saves about 25% of memory compared to the old code.

-  Treating module attributes ``__package__``, ``__loader__``,
   ``__file__``, and ``__spec__`` with dedicated nodes, that allow or
   forbid optimization dependent on usage.

-  Python3.6: Async generator expressions were not working fully, become
   more compatible.

-  Fix, using ``super`` inside a contraction could crash the compiler.

-  Fix, also accept ``__new__`` as properly decorated in case it's a
   ``classmethod`` too.

-  Fix, removed obsolete ``--nofreeze-stdlib`` which only complicated
   using the ``--recurse-stdlib`` which should be used instead.

****************
 Organisational
****************

-  The ``nuitka`` Python package is now installed into the public
   namespace and used from there. There are distinct copies to be
   installed for both Python2 and Python3 on platforms where it is
   supported.

-  Using ``twine`` for upload to PyPI now as recommended on their site.

-  Running ``pylint`` on Windows became practical again.

-  Added RPM packages for Fedora 26 and 27, these used to fail due to
   packaging issues.

-  Added RPM packages for openSUSE Leap 42.2, 42.3 and 15.0 which were
   simply missing.

-  Added RPM packages for SLE 15.

-  Added support for PyLint 1.8 and its new warnings.

-  The RPM packages no longer contain ``nuitka-run3``, it will be
   replaced by the new ``nuitka3-run`` which is in all packages.

-  The runners used for installation are now easy install created, but
   patched to avoid overhead at run time.

-  Added repository for Ubuntu Artful (17.10) for download, removed
   support for Ubuntu Yakkety, Vivid and Zesty (no more supported by
   them).

-  Removed support for Debian Wheezy and Ubuntu Precise (they are too
   old for modern packaging used).

-  There is now a issue template for GitHub when used.

*******
 Tests
*******

-  Windows: Standalone tests were referencing an old path to
   ``depends.exe`` that wasn't populated on new installs.

-  Refinements for CPython test suites to become more stable in results.
   Some tests occasionally fail to clean up, or might do indeterministic
   outputs, or are not relevant at all.

-  The tests don't use the runners, but more often do ``-m nuitka`` to
   become executable without having to find the proper runner. This
   improves usage during the RPM builds and generally.

-  Travis: Do not test development versions of CPython, even for stable
   release, they break too often.

*********
 Summary
*********

This release consolidates a lot of what we already had, adding hopeful
stuff for distutils integration. This will need tests and documentation
though, but should make Nuitka really easy to use. A few features are
still missing to make it generally reliable in that mode, but they are
going to come.

Also the locals dictionary work is kind of incomplete without a proper
generic tracing of not only local variables, but also dictionary keys.
With that work in place, a lot of improvements will happen.
