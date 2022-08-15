.. post:: 2022/07/02 08:17
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 0.9
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release has a many optimization improvements, and scalability
improvements, while also adding new features, with also some important
bug fixes.

***********
 Bug Fixes
***********

-  Fix, hard module name lookups leaked a reference to that object.
   Fixed in 0.8.1 already.

-  Python2: Fix, ``str.decode`` with ``errors`` as the only argument
   wasn't working. Fixed in 0.8.1 already.

-  Fix, could corrupt created uncompiled class objects ``__init__``
   functions in case of descriptors being used.

-  Standalone: Added support for newer ``torch``. Fixed in 0.8.1
   already.

-  Standalone: Added support for newer ``torchvision``. Fixed in 0.8.1
   already.

-  Fix, could compile time crash during initial parsing phase on
   constant dictionary literals with non-hashable keys.

   .. code:: python

      { {}:1, }

-  Fix, hard imported sub-modules of hard imports were falsely resolved
   to their parent. Fixed in 0.8.3 already.

   .. code:: python

      importlib.resources.read_bytes() # gave importlib has no attribute...

-  Windows: Fix, outputs with ``--force-stdout-spec`` or
   ``--force-stderr-spec`` were created with the file system encoding on
   Python3, but they nee to be ``utf-8``.

-  Fix, didn't allow zero spaces in Nuitka project options, which is not
   expected.

-  Modules: Fix, the ``del __file__`` in the top level module in module
   mode caused crashes at runtime, when trying to restore the original
   ``__file__`` value, after the loading CPython corrupted it.

-  Python2.6: Fixes for installations without ``pkg_resources``.

-  Windows: Fix for very old Python 2.6 versions, these didn't have a
   language assigned that could be used.

-  Security: Fix for `CVE-2022-2054
   <https://security-tracker.debian.org/tracker/CVE-2022-2054>`__ where
   environment variables used for transfer of information between Nuitka
   restarting itself, could be used to execute arbitrary code at compile
   time.

-  Anaconda: Fix, the torch plugin was not working on Linux due to
   missing DLL dependencies.

-  Fix, static optimization of ``importlib.import_module`` with a
   package given, for an absolute import was optimized into the wrong
   import, package was not ignored as it should be.

-  Windows: Installed Python scan could crash on trying installation
   paths from registry that were manually removed in the mean time, but
   not through an uninstaller.

-  Standalone: Added missing implicit dependency for ``pyreadstat``
   because parts of standard library it uses are no more automatically
   included.

-  Windows: Could still crash when no ``powershell`` is available with
   symlinks, handle this more gracefully.

-  Standalone: Added more missing Plotly dependencies, but more work
   will be needed to complete this.

-  Standalone: Add missing stdlib dependency on ``multiprocessing`` by
   ``concurrent.futures.process``.

-  Standalone: Fix, implicit dependencies assigned to ``imageio`` on PIL
   plugins should actually be assigned to ``PIL.Image`` that actually
   loads them, so it works outside of ``imageio`` too.

**************
 New Features
**************

-  UI: Added new option ``--user-package-configuration-file`` to allow
   users to provide extra Yaml configuration files for the Nuitka plugin
   mechanism to add hidden dependencies, anti-bloat, or data files, for
   packages. This will be useful for developing PRs to the standard file
   of Nuitka. Currently the schema is available, but it is not
   documented very well yet, so not really ready for end users just yet.

-  Standalone: Added new ``no-qt`` plugin as an easy way to prevent all
   of the Qt bindings from being included in a compilation.

-  Include module search path in compilation report.

**************
 Optimization
**************

-  Faster dictionary iteration with our own replacement for
   ``PyDict_Next`` that avoids the DLL call overhead (in case of
   non-static libpython) and does less unnecessary checks.

-  Added optimization for ``str.count`` and ``str.format`` methods as
   well, this should help in some cases with compile time optimization.

-  The node for ``dict.update`` with only an iterable argument, but no
   keyword arguments, was in fact unused due to wrongly generated code.
   Also the form with no arguments wasn't yet handled properly.

-  Scalability: Use specialized nodes for pair values, i.e. the
   representation of ``x = y`` in e.g. dictionary creations. With
   constant keys, and values, these avoid full constant value nodes, and
   therefore save memory and compile time for a lot of code.

-  Anti-bloat: Added more scalability work to avoid including modules
   that make compilation unnecessarily big.

-  Python3.9+: Faster calls in case of mixed code, i.e. compiled code
   calling uncompiled code.

-  Removing duplicates and non-existent entries from modules search path
   should improve performance when locating modules.

-  Optimize calls through variables as well. These are needed for the
   package resource nodes to properly resolve at compile time from their
   hard imports to the called function.

-  Hard imported names should also be considered very trusted
   themselves, so they are e.g. also optimized in calls.

-  Anti-bloat: Avoid more useless imports in Pandas, Numba, Plotly, and
   other packages, improving the scalability some more.

-  Added dedicated nodes for ``pkg_resources.require``,
   ``pkg_resources.get_distribution``, ``importlib.metadata.version``,
   and ``importlib_metadata.version``, so we can use compile time
   optimization to resolve their argument values where possible.

-  Avoid annotating control flow escape for all release statements.
   Sometimes we can tell that ``__del__`` will not execute outside code
   ever, so this then avoids marking values as escaped, and taking the
   time to do so.

-  Calls of methods through variables on ``str``, ``dict``, ``bytes``
   that have dedicated nodes are now also optimized through variables.

-  Boolean tests through variables now also are optimized when the
   original assignment is a compile time constant that is not mutable.
   This is only basic, but will allow tests on ``TYPE_CHECKING`` coming
   from a ``from typing import TYPE_CHECKING`` statement to be
   optimized, avoiding this overhead.

**********
 Cleanups
**********

-  Changed to ``torch`` plugin to Yaml based configuration, making it
   obsolete, it only remains there for a few releases, to not crash
   existing build scripts.

-  Moved older package specific hacks to the Yaml file. Some of these
   were from hotfixes where the Yaml file wasn't yet used by default,
   but now there is no need for them anymore.

-  Removed most of the ``pkg-resources`` plugin work. This is now done
   during optimization phase and rather than being based on source code
   matches, it uses actual value tracing, so it immediately covers many
   more cases.

-  Continued spelling improvements, renaming identifiers used in the
   source that the cspell based extension doesn't like. This aims at
   producing more readable and searchable code.

-  Generated attribute nodes no longer do local imports of the operation
   nodes they refer to. This also avoids compile time penalties during
   optimization that are not necessary.

-  Windows: Avoid useless bytecode of inline copy used by Python3 when
   installing for Python2, this spams just a lot of errors.

****************
 Organisational
****************

-  Removed MSI installers from the download page. The MSI installers are
   discontinued as Python has deprecated their support for them, as well
   as Windows 10 is making it harder for users to install them. Using
   the PyPI installation is recommended on Windows.

-  Merged our Yaml files into one and added schema description, for
   completion and checking in Visual Code while editing. Also check the
   schema in ``check-nuitka-with-yamllint`` which is now slightly
   misnamed. The schema is in no way final and will see improvements in
   future releases.

-  UI: Nicer progress bar layout that avoids flicker when optimizing
   modules.

-  UI: When linking, output the total number of object files used, to
   have that knowledge after the progress bar for C compilation is gone.

-  Quality: Auto-format the package configuration Yaml file for
   anti-bloat, implicit dependencies, etc.

-  GitHub: Point out the commit hook in the PR template.

-  UI: Nicer output in case of no commercial version is used.

-  Updated the MinGW64 winlibs download used on Windows to the latest
   version based on gcc 11, the gcc 12 is not yet ready.

-  Git: Make sure we are not affected by ``core.autocrlf`` setting, as
   it interferes with auto-format enforcing Unix newlines.

-  Removed the MSI downloads. Windows 10 has made them harder to install
   and Python itself is discontinuing support for them, while often it
   was only used by beginners, for which it was not intended.

-  Anaconda: Make it more clear how to install static libpython with
   precise command.

-  UI: Warn about using Debian package contents. These can be
   non-portable to other OSes.

-  Quality: The auto-format now floats imports to the top for
   consistency. With few exceptions, it was already done like this. But
   it makes things easier for generated code.

*******
 Tests
*******

-  The reflected test was adapted to preserve ``PYTHONPATH`` now that
   module presence influences optimization.

*********
 Summary
*********

This release marks a point, that will allow us to open up the
compatibility work for implicit dependencies and anti-bloat stuff even
further. The Yaml format will need documentation and potentially more
refinement, but will open up a future, where latest packages can be
supported with just updating this configuration.

The scalability improvements really make a difference for many libraries
and are a welcome improvement on both memory usage and compile time.
They are achieved by an accord of static optimization of

One optimization aimed at optimizing tuple unpacking, was not finished
in time for this release, but will be subject of a future release. It
has driven many other improvements though.

Generally, also from the UI, this is a huge step forward. With links to
the website for complex topics being started, and the progress bar
flicker being removed, the tool has yet again become more user friendly.
