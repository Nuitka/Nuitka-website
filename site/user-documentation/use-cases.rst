:orphan:

###########
 Use Cases
###########

This page discusses the various use cases of Nuitka, it is recommended
to be read entirely, since the cases build on each other. They will
inform your decision how to use Nuitka for your software.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

**************************************************************
 Program compilation with all modules embedded (acceleration)
**************************************************************

If you want to compile a whole program recursively, and not only the
single file that is the main program, do it like this:

.. code:: bash

   python -m nuitka --follow-imports program.py

.. note::

   There are more fine-grained controls than ``--follow-imports``
   available. Consider the output of ``nuitka --help``. Including fewer
   modules into the compilation, but instead using normal Python for it,
   will make it faster to compile.

In case you have a source directory with dynamically loaded files, i.e.
one which cannot be found by recursing after normal import statements
via the ``PYTHONPATH`` (which would be the recommended way), you can
always require that a given directory shall also be included in the
executable:

.. code:: bash

   python -m nuitka --follow-imports --include-plugin-directory=plugin_dir program.py

.. note::

   If you don't do any dynamic imports, simply setting your
   ``PYTHONPATH`` at compilation time is what you should do.

   Use ``--include-plugin-directory`` only if you make ``__import__()``
   calls that Nuitka cannot predict, and that come from a directory, for
   everything from your Python installation, use ``--include-module`` or
   ``--include-package``.

.. note::

   The resulting filename will be ``program.exe`` on Windows,
   ``program.bin`` on other platforms, but ``--output-filename`` allows
   changing that.

.. note::

   The resulting binary still depends on CPython and used C extension
   modules being installed.

   If you want to be able to copy it to another machine, use
   ``--mode=standalone`` and copy the created ``program.dist`` directory
   and execute the ``program.exe`` (Windows) or ``program`` (other
   platforms) put inside.

******************************
 Extension Module compilation
******************************

If you want to compile a single extension module, all you have to do is
this:

.. code:: bash

   python -m nuitka --module some_module.py

The resulting file ``some_module.so`` can then be used instead of
``some_module.py``.

.. important::

   The filename of the produced extension module must not be changed as
   Python insists on a module name derived function as an entry point,
   in this case ``PyInit_some_module`` and renaming the file will not
   change that. Match the filename of the source code to what the binary
   name should be.

.. note::

   If both the extension module and the source code of it are in the
   same directory, the extension module is loaded. Changes to the source
   code only have effect once you recompile.

.. note::

   The option ``--follow-import-to`` works as well, but the included
   modules will only become importable *after* you imported the
   ``some_module`` name. If these kinds of imports are invisible to
   Nuitka, e.g. dynamically created, you can use ``--include-module`` or
   ``--include-package`` in that case, but for static imports it should
   not be needed.

.. note::

   An extension module can never include other extension modules. You
   will have to create a wheel for this to be doable.

.. note::

   The resulting extension module can only be loaded into a CPython of
   the same version and doesn't include other extension modules.

*********************
 Package compilation
*********************

If you need to compile a whole package and embed all modules, that is
also feasible, use Nuitka like this:

.. code:: bash

   python -m nuitka --module some_package --include-package=some_package

.. note::

   The inclusion of the package contents needs to be provided manually;
   otherwise, the package is mostly empty. You can be more specific if
   you like, and only include part of it, or exclude part of it, e.g.
   with ``--nofollow-import-to='*.tests'`` you would not include the
   unused test part of your code.

.. note::

   Data files located inside the package will not be embedded by this
   process, you need to copy them yourself with this approach.
   Alternatively, you can use the `file embedding of Nuitka commercial
   <https://nuitka.net/doc/commercial/protect-data-files.html>`__.

*********************************
 Standalone Program Distribution
*********************************

For distribution to other systems, there is the standalone mode, which
produces a folder for which you can specify ``--mode=standalone``.

.. code:: bash

   python -m nuitka --mode=standalone program.py

Following all imports is default in this mode. You can selectively
exclude modules by specifically saying ``--nofollow-import-to``, but
then an ``ImportError`` will be raised when import of it is attempted at
program run time. This may cause different behavior, but it may also
improve your compile time if done wisely.

For data files to be included, use the option
``--include-data-files=<source>=<target>`` where the source is a file
system path, but the target has to be specified relative. For the
standalone mode, you can also copy them manually, but this can do extra
checks, and for the onefile mode, there is no manual copying possible.

To copy some or all file in a directory, use the option
``--include-data-files=/etc/*.txt=etc/`` where you get to specify shell
patterns for the files, and a subdirectory where to put them, indicated
by the trailing slash.

.. important::

   Nuitka does not consider data files code, do not include DLLs, or
   Python files as data files, and expect them to work, they will not,
   unless you really know what you are doing. Refer to
   :ref:`code-is-not-data-files` for more details.

Also some folders are ignored, these are ``site-packages``,
``dist-packages`` and ``vendor-packages`` which would otherwise include
a full virtualenv, which is never a good thing to happen. And the
``__pycache__`` folder is also always ignored. On non-MacOS the file
``.DS_Store`` is ignored too, and ``py.typed`` folders have only meaning
to IDEs, and are ignored like ``.pyi`` files .

To copy a whole folder with all non-code files, you can use
``--include-data-dir=/path/to/images=images`` which will place those in
the destination, and if you want to use the ``--noinclude-data-files``
option to remove them. Code files are as detailed above DLLs,
executables, Python files, etc. and will be ignored. For those you can
use the ``--include-data-files=/binaries/*.exe=binary/`` form to force
them, but that is not recommended and known to cause issues at run-time.

For package data, there is a better way, namely using
``--include-package-data``, which detects all non-code data files of
packages automatically and copies them over. It even accepts patterns in
a shell style. It spares you the need to find the package directory
yourself and should be preferred whenever available. Functionally it's
very similar to ``--include-data-dir`` but it has the benefit to locate
the correct folder for you.

With data files, you are largely on your own. Nuitka keeps track of ones
that are needed by popular packages, but it might be incomplete. Raise
issues if you encounter something in these. Even better, raise PRs with
enhancements to the Nuitka Package Configuration. We want 3rd-party
software to just work out of the box.

When that is working, you can use the onefile mode if you so desire.

.. code:: bash

   python -m nuitka --mode=onefile program.py

This will create a single binary, that extracts itself on the target,
before running the program. But notice, that accessing files relative to
your program is impacted, make sure to read the section
:ref:`onefile-finding-files` as well.

.. note::

   **Recommended workflow:** Always test with ``--mode=standalone``
   first to ensure your program works correctly, then switch to
   ``--mode=onefile`` once everything is working. Issues like missing
   data files are much easier to debug in standalone mode.

   ``--mode=onefile`` automatically combines with ``--mode=standalone``,
   so you don't need to specify both.

.. code:: bash

   # Create a binary that unpacks into a temporary folder
   python -m nuitka --mode=onefile program.py

.. note::

   There are more platform-specific options, e.g. related to icons,
   splash screen, and version information, consider the ``--help``
   output for the details of these and check the section :ref:`tweaks`.

For the unpacking, by default a unique user temporary path one is used,
and then deleted, however this default
``--onefile-tempdir-spec="{TEMP}/onefile_{PID}_{TIME}"`` can be
overridden with a path specification, then using a cached path, avoiding
repeated unpacking, e.g. with
``--onefile-tempdir-spec="{CACHE_DIR}/{COMPANY}/{PRODUCT}/{VERSION}"``
which uses version information, and user-specific cache directory.

.. note::

   Using cached paths will be relevant, e.g. when Windows Firewall comes
   into play because otherwise, the binary will be a different one to it
   each time it is run.

Currently, these expanded tokens are available:

+----------------+-----------------------------------------------------------+---------------------------------------+
| Token          | What this Expands to                                      | Example                               |
+================+===========================================================+=======================================+
| {TEMP}         | User temporary file directory                             | C:\\Users\\...\\AppData\\Locals\\Temp |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {PID}          | Process ID                                                | 2772                                  |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {TIME}         | Time in seconds since the epoch.                          | 1299852985                            |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {PROGRAM}      | Full program run-time filename of executable.             | C:\\SomeWhere\\YourOnefile.exe        |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {PROGRAM_BASE} | No-suffix of run-time filename of executable.             | C:\\SomeWhere\\YourOnefile            |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {CACHE_DIR}    | Cache directory for the user.                             | C:\\Users\\SomeBody\\AppData\\Local   |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {COMPANY}      | Value given as ``--company-name``                         | YourCompanyName                       |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {PRODUCT}      | Value given as ``--product-name``                         | YourProductName                       |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {VERSION}      | Combination of ``--file-version`` & ``--product-version`` | 3.0.0.0-1.0.0.0                       |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {HOME}         | Home directory for the user.                              | /home/somebody                        |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {NONE}         | When provided for file outputs, ``None`` is used          | see notice below                      |
+----------------+-----------------------------------------------------------+---------------------------------------+
| {NULL}         | When provided for file outputs, ``os.devnull`` is used    | see notice below                      |
+----------------+-----------------------------------------------------------+---------------------------------------+

.. important::

   It is your responsibility to make the path provided unique, on
   Windows a running program will be locked, and while using a fixed
   folder name is possible, it can cause locking issues in that case,
   where the program gets restarted.

   Usually, you need to use ``{TIME}`` or at least ``{PID}`` to make a
   path unique, and this is mainly intended for use cases, where e.g.
   you want things to reside in a place you choose or abide your naming
   conventions.

.. important::

   For disabling output and stderr with ``--force-stdout-spec`` and
   ``--force-stderr-spec`` the values ``{NONE}`` and ``{NULL}`` achieve
   it, but with different effect. With ``{NONE}``, the corresponding
   handle becomes ``None``. As a result, e.g. ``sys.stdout`` will be
   ``None``, which is different from ``{NULL}`` where it will be backed
   by a file pointing to ``os.devnull``, i.e. you can write to it.

   With ``{NONE}``, you may e.g. get ``RuntimeError: lost sys.stdout``
   in case it does get used; with ``{NULL}`` that never happens.
   However, some libraries handle this as input for their logging
   mechanism, and on Windows this is how you are compatible with
   ``pythonw.exe`` which is behaving like ``{NONE}``.

*******************
 Setuptools Wheels
*******************

If you have a ``setup.py``, ``setup.cfg`` or ``pyproject.toml`` driven
creation of wheels for your software in place, putting Nuitka to use is
extremely easy.

Let's start with the most common ``setuptools`` approach, you can,
having Nuitka installed of course, simply execute the target
``bdist_nuitka`` rather than the ``bdist_wheel``. It takes all the
options and allows you to specify some more, that are specific to
Nuitka.

.. code:: python

   # For setup.py if you don't use other build systems:
   setup(
      # Data files are to be handled by setuptools and not Nuitka
      package_data={"some_package": ["some_file.txt"]},
      ...,
      # This is to pass Nuitka options.
      command_options={
         'nuitka': {
            # boolean option, e.g. if you cared for C compilation commands
            '--show-scons': True,
            # options without value, e.g. enforce using Clang
            '--clang': None,
            # options with single values, e.g. enable a plugin of Nuitka
            '--enable-plugin': "pyside2",
            # options with several values, e.g. avoid including modules
            '--nofollow-import-to' : ["*.tests", "*.distutils"],
         },
      },
   )

   # For setup.py with other build systems:
   # The tuple nature of the arguments is required by the dark nature of
   # "setuptools" and plugins to it, that insist on full compatibility,
   # e.g. "setuptools_rust"

   setup(
      # Data files are to be handled by setuptools and not Nuitka
      package_data={"some_package": ["some_file.txt"]},
      ...,
      # This is to pass Nuitka options.
      ...,
      command_options={
         'nuitka': {
            # boolean option, e.g. if you cared for C compilation commands
            '--show-scons': ("setup.py", True),
            # options without value, e.g. enforce using Clang
            '--clang': ("setup.py", None),
            # options with single values, e.g. enable a plugin of Nuitka
            '--enable-plugin': ("setup.py", "pyside2"),
            # options with several values, e.g. avoid including modules
            '--nofollow-import-to' : ("setup.py", ["*.tests", "*.distutils"]),
         }
      },
   )

If for some reason, you cannot or do not want to change the target, you
can add this to your ``setup.py``.

.. code:: python

   # For setup.py
   setup(
      ...,
      build_with_nuitka=True
   )

.. note::

   To temporarily disable the compilation, you could the remove above
   line, or edit the value to ``False`` by or take its value from an
   environment variable if you so choose, e.g.
   ``bool(os.getenv("USE_NUITKA", "True"))``. This is up to you.

Or you could put it in your ``setup.cfg``

.. code:: toml

   [metadata]
   build_with_nuitka = true

And last, but not least, Nuitka also supports the new ``build`` meta, so
when you have a ``pyproject.toml`` already, simple replace or add this
value:

.. code:: toml

   [build-system]
   requires = ["setuptools>=42", "wheel", "nuitka", "toml"]
   build-backend = "nuitka.distutils.Build"

   # Data files are to be handled by setuptools and not Nuitka
   [tool.setuptools.package-data]
   some_package = ['data_file.txt']

   [tool.nuitka]
   # These are not recommended, but they make it obvious to have effect.

   # boolean option, e.g. if you cared for C compilation commands, leading
   # dashes are omitted
   show-scons = true

   # options with single values, e.g. enable a plugin of Nuitka
   enable-plugin = "pyside2"

   # options with several values, e.g. avoid including modules, accepts
   # list argument.
   nofollow-import-to = ["*.tests", "*.distutils"]

.. note::

   For the ``nuitka`` requirement above absolute paths like
   ``C:\Users\...\Nuitka`` will also work on Linux, use an absolute path
   with *two* leading slashes, e.g. ``//home/.../Nuitka``.

.. note::

   Whatever approach you take, data files in these wheels are not
   handled by Nuitka at all, but by setuptools. You can, however, use
   the data file embedding of Nuitka commercial. In that case, you
   actually would embed the files inside the extension module itself,
   and not as a file in the wheel.

***********
 Multidist
***********

If you have multiple programs, that each should be executable, in the
past you had to compile multiple times, and deploy all of these. With
standalone mode, this, of course, meant that you were fairly wasteful,
as sharing the folders could be done, but wasn't really supported by
Nuitka.

Enter ``Multidist``. There is an option ``--main`` that replaces or adds
to the positional argument given. And it can be given multiple times.
When given multiple times, Nuitka will create a binary that contains the
code of all the programs given, but sharing modules used in them. They
therefore do not have to be distributed multiple times.

Let's call the basename of the main path, and entry point. The names of
these must, of course, be different. Then the created binary can execute
either entry point, and will react to what ``sys.argv[0]`` appears to
it. So if executed in the right way (with something like ``subprocess``
or OS API you can control this name), or by renaming or copying the
binary, or symlinking to it, you can then achieve the miracle.

This allows to combine very different programs into one.

.. note::

   This feature is still experimental. Use with care and report your
   findings should you encounter anything that is undesirable behavior

This mode works with standalone, onefile, and mere acceleration. It does
not work with module mode.

********************************
 Building with GitHub Workflows
********************************

For integration with GitHub workflows there is this `Nuitka-Action
<https://github.com/Nuitka/Nuitka-Action>`__ that you should use that
makes it really easy to integrate. You ought to start with a local
compilation though, but this will be easiest for cross platform
compilation with Nuitka.

This is an example workflow that builds on all 3 OSes

.. code:: yaml

   jobs:
   build:
      strategy:
         matrix:
         os: [macos-latest, ubuntu-latest, windows-latest]

      runs-on: ${{ matrix.os }}

      steps:
         - name: Check-out repository
         uses: actions/checkout@v4

         - name: Setup Python
         uses: actions/setup-python@v5
         with:
            python-version: '3.10'
            cache: 'pip'
            cache-dependency-path: |
               **/requirements*.txt

         - name: Install your Dependencies
         run: |
            pip install -r requirements.txt -r requirements-dev.txt

         - name: Build Executable with Nuitka
         uses: Nuitka/Nuitka-Action@main
         with:
            nuitka-version: main
            script-name: your_main_program.py
            # many more Nuitka options available, see action doc, but it's best
            # to use nuitka-project: options in your code, so e.g. you can make
            # a difference for macOS and create an app bundle there.
            mode: app

         - name: Upload Artifacts
         uses: actions/upload-artifact@v4
         with:
            name: ${{ runner.os }} Build
            path: | # match what's created for the 3 OSes
               build/*.exe
               build/*.bin
               build/*.app/**/*
            include-hidden-files: true

If your app is a GUI, e.g. ``your_main_program.py`` should contain these
comments as explained in :ref:`nuitka-project-options` since on macOS
this should then be a bundle.

.. code:: python

   # Compilation mode, standalone everywhere, except on macOS there app bundle
   # nuitka-project: --mode=app
   #
   # Debugging options, controlled via environment variable at compile time.
   # nuitka-project-if: {OS} == "Windows" and os.getenv("DEBUG_COMPILATION", "no") == "yes"
   #     nuitka-project: --windows-console-mode=hide
   # nuitka-project-else:
   #     nuitka-project: --windows-console-mode=disabled
