This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is massive in terms of fixes, but also adds a lot of refinement
to code generation, and more importantly adds experimental support for
Python 3.7, while enhancing support for Pyt5 in standalone mode by a lot.

Bug Fixes
---------

- Standalone: Added missing dependencies for ``PyQt5.Qt`` module.

- Plugins: Added support for ``PyQt5.Qt`` module and its ``qml`` plugins.

- Plugins: The sensible plugin list for PyQt now includes that platforms
  plugins on Windows too, as they are kind of mandatory.

- Python3: Fix, for uninstalled Python versions wheels that linked against
  the ``Python3`` library as opposed to ``Python3X``, it was not found.

- Standalone: Prefer DLLs used by main program binary over ones used by
  wheels.

- Standalone: For DLLs added by Nuitka plugins, add the package directory
  to the search path for dependencies where they might live.

- Fix, the ``vars`` built-in didn't annotate its exception exit.

- Python3: Fix, the ``bytes`` and ``complex`` built-ins needs to be treated as
  a slot too.

- Fix, consider if ``del`` variable must be assigned, in which case no
  exception exit should be created. This prevented ``Tkinter`` compilation.

- Python3.6: Added support for the following language construct:

  .. code-block:: python

    d = {"metaclass" : M}

    class C(**d):
       pass

- Python3.5: Added support for cyclic imports. Now a ``from`` import with
  a name can really cause an import to happen, not just a module attribute
  lookup.

- Fix, ``hasattr`` was never raising exceptions.

- Fix, ``bytearray`` constant values were considered to be non-iterable.

- Python3.6: Fix, now it is possible to ``del __annotations__`` in a class
  and behave compatible. Previously in this case we were falling back to the
  module variable for annotations used after that which is wrong.

- Fix, some built-in type conversions are allowed to return derived types,
  but Nuitka assumed the exact type, this affected ``bytes``, ``int``,
  ``long``, ``unicode``.

- Standalone: Fix, the ``_socket`` module was insisted on to be found, but
  can be compiled in.

New Features
------------

- Added experimental support for Python 3.7, more work will be needed
  though for full support. Basic tests are working, but there are are
  at least more coroutine changes to follow.

- Added support for building extension modules against statically linked
  Python. This aims at supporting manylinux containers, which are supposed
  to be used for creating widely usable binary wheels for Linux. Programs
  won't work with statically linked Python though.

- Added options to allow ignoring the Windows cache for DLL dependencies or
  force an update.

- Allow passing options from distutils to Nuitka compilation via setup
  options.

- Added option to disable the DLL dependency cache on Windows as it may
  become wrong after installing new software.

- Added experimental ability to provide extra options for Nuitka to setuptools.

- Python3: Remove frame preservation and restoration of exceptions. This is
  not needed, but leaked over from Python2 code.

Optimization
------------

- Apply value tracing to local dict variables too, enhancing the optimization
  for class bodies and function with ``exec`` statements by a lot.

- Better optimization for "must not have value", wasn't considering merge
  traces of uninitialized values, for which this is also the case.

- Use 10% less memory at compile time due to specialized base classes for
  statements with a single child only allowing ``__slots__`` usage by not
  having multiple inheritance for those.

- More immediately optimize branches with known truth values, so that merges
  are avoided and do not prevent trace based optimization before the pass after
  the next one. In some cases, optimization based on traces could fail to be
  done if there was no next pass caused by other things.

- Much faster handling for functions with a lot of ``eval`` and ``exec`` calls.

- Static optimization of ``type`` with known type shapes, the value is
  predicted at compile time.

- Optimize containers for all compile time constants into constant nodes. This
  also enables further compile time checks using them, e.g. with ``isinstance``
  or ``in`` checks.

- Standalone: Using threads when determining DLL dependencies. This will speed
  up the un-cached case on Windows by a fair bit.

- Also remove unused assignments for mutable constant values.

- Python3: Also optimize calls to ``bytes`` built-in, this was so far not done.

- Statically optimize iteration over constant values that are not iterable
  into errors.

- Removed Fortran, Java, LaTex, PDF, etc. stuff from the inline copies of
  Scons for faster startup and leaner code. Also updated to 3.0.1 which is
  no important difference over 3.0.0 for Nuitka however.

- Make sure to always release temporary objects before checking for error
  exits. When done the other way around, more C code than necessary will
  be created, releasing them in both normal case and error case after the
  check.

- Also remove unused assignments in case the value is a mutable constant.

Cleanups
--------

- Don't store "version" numbers of variable traces for code generation, instead
  directly use the references to the value traces instead, avoiding later
  lookups.

- Added dedicated module for ``complex`` built-in nodes.

- Moved C helpers for integer and complex types to dedicated files, solving the
  TODOs around them.

- Removed some Python 3.2 only codes.

Organizational
--------------

- For better bug reports, the ``--version`` output now contains also the Python
  version information and the binary path being used.

- Started using specialized exceptions for some types of errors, which will
  output the involved data for better debugging without having to reproduce
  anything. This does e.g. output XML dumps of problematic nodes.

- When encountering a problem (compiler crash) in optimization, output the
  source code line that is causing the issue.

- Added support for Fedora 28 RPM builds.

- Remove more instances of mentions of 3.2 as supported or usable.

- Renovated the graphing code and made it more useful.

Summary
-------

This release marks important progress, as the locals dictionary tracing is
a huge step ahead in terms of correctness and proper optimization. The actual
resulting dictionary is not yet optimized, but that ought to follow soon now.

The initial support of 3.7 is important. Right now it apparently works pretty
well as a 3.6 replacement already, but definitely a lot more work will be
needed to fully catch up.

For standalone, this accumulated a lot of improvements related to the plugin
side of Nuitka. Thanks to those involved in making this better. On Windows
things ought to be much faster now, due to parallel usage of dependency
walker.
