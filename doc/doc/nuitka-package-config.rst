##############################
 Nuitka Package Configuration
##############################

.. contents:: Table of Contents
   :depth: 3
   :local:
   :class: page-toc

**************
 Introduction
**************

For packaging, and compatibility, or some Python packages need to have
special considerations in Nuitka. Some will not work without certain
data files, sometimes modules depend on other modules in a hidden way,
and for standalone DLLs might have to be included, that are loaded
dynamically and therefore also invisible.

Another are is compatibility hacks, and removing bloat from code or just
making sure, you are not using an unsupported version or wrong options
for a package.

To make it easier to deal with missing DLLs, implicit imports, data
files, bloat etc. Nuitka has a system with Yaml files. These ship inside
of it and are located under ``plugins/standard`` and are designed to be
easily be extended.

The structure of the filename is always ``*nuitka-package.config.yml``.
The ``standard`` file includes all things that are not in the standard
library (``stdlib``) of Python. In ``stdlib2`` and ``stdlib3`` there are
entries for the standard library. In ``stdlib2`` there are only those
for modules that are no longer available in Python3.

If you want to use your own configuration, you can do so by passing the
filename of your Yaml file via the
``--user-package-configuration-file=my.nuitka-package.config.yml``
option.

If it could be interesting for the other parts of the user base of
Nuitka, please do a PR that adds it to the general files. In this way,
not every user has to repeat what you just did, and we can collectively
maintain it.

*****************************
 The YAML Configuration File
*****************************

At the beginning of the file you will find the following lines, which
you can ignore, they are basically only there to silence checkers about
problems that are too hard to avoid.

.. code:: yaml

   # yamllint disable rule:line-length
   # yamllint disable rule:indentation
   # yamllint disable rule:comments-indentation
   # too many spelling things, spell-checker: disable
   ---

An entry in the file look like this:

.. code:: yaml

   - module-name: 'pandas._libs'
     implicit-imports:
       - depends:
         - 'pandas._libs.tslibs.np_datetime'
         - 'pandas._libs.tslibs.nattype'
         - 'pandas._libs.tslibs.base'

The ``module-name`` value is the name of the affected module. We will
show and explain to you everything the other things in detail later. But
the key principle is that a declaration always references a module by
name.

It is also important to know that you do not have to worry about
formatting. We have programmed our own tool for this, which formats
everything automatically. This is executed via
``bin\autoformat-nuitka-source`` and automatically when pushing with
``git`` if you install the git hook (see Developer Manual for that).

There is also a Yaml schema file to check your files against and that in
Visual Code is automatically applied to the Yaml files and that then
supports you with auto-completion in Visual Code. So actually doing the
change in PR form can be easier than not.

***************
 Documentation
***************

Data Files
==========

.. code:: yaml

   data-files:
     dest_path: '.' # default, relative to package directory, normally not needed
     dirs:
       - 'dir1'

     patterns:
       - 'file1'
       - '*.dat'

     empty_dirs:
       - 'empty_dir'

     empty_dir_structures:
       - 'empty_dir_structure'

     when: 'win32'

If a module needs data files, you can get Nuitka to copy them into the
output with the following features.

Features
--------

|  ``dest_path``: target directory
|  ``dirs``: all directories that should be copied
|  ``patterns``: all files that should be copied (filename can be a
   `glob pattern
   <https://docs.python.org/3/library/glob.html#glob.glob>`_)
|  ``empty_dirs``: all empty directories that should be copied
|  ``empty_dir_structures``: all empty directory structures that should
   be copied
|  ``when``: when_ is documented in a separate section

Examples
--------

Example 1
^^^^^^^^^

The most simple form just adds a data folder. The data files are in a
folder and lives inside the package directory.

.. code:: yaml

   - module-name: 'customtkinter'
     data-files:
        dirs:
          - 'assets'

.. note::

   A ``dest_path`` is very unlikely necessary. It defaults to the ``.``
   relative path. It would have to be a strange package or some code
   modification on top, that would require data files to live in another
   spot in the standalone distribution.

Example 2
^^^^^^^^^

This example includes a complete folder with data files in a package.

.. code:: yaml

   - module-name: 'tkinterweb'
     data-files:
       dirs:
         - 'tkhtml'

.. note::

   The example is actually an imperfect solution, since dependent on
   architecture, files can be omitted. We are going to address this in
   an update later.

Example 3
^^^^^^^^^

This example will make sure an empty folder is created relative to a
package.

.. code:: yaml

   - module-name: 'Crypto.Util._raw_api'
     data-files:
       empty_dirs:
         - '.'

.. note::

   The reason this is necessary is that some packages expect to have
   their directory as derived from ``__file__`` to exist. But for
   compiled packages, unless there is extension packages or data files
   copied into them, these directories do not exist.

DLLs
====

.. code:: yaml

   dlls:
     - from_filenames:
         relative_path: 'dlls'
         prefixes:
           - 'dll1'
           - 'mydll*'

         suffixes:
           - 'pyd'

       dest_path: 'output_dir'
       when: 'win32'

     - by_code:
       setup_code: ''
       filename_code: ''
       dest_path: 'output_dir'
       when: 'linux'

If a module dynamically requires DLLs, i.e. there is not an extension
module is not linked against them, they must be specified in this way.

Features
--------

``from_filenames``
   |  ``relative_path``: directory where the DLLs can be found relative
      to the module
   |  ``prefixes``: all DLLs that should be copied (filename can be a
      `glob pattern
      <https://docs.python.org/3/library/glob.html#glob.glob>`_)
   |  ``suffixes``: can be used to force the file extension

``by_code``
   |  ``setup_code``: code needed to prepare the filename_code
   |  ``filename_code``: code that outputs a the DLL filename from
      installation

|  ``dest_path``: target directory
|     ``when``: when_ is documented in a separate section

The recommended way goes by filename. The ``by_code`` version is still
in flux and depends on compile time importing code, making it vulernable
to compile time issues in many ways.

Examples
--------

Example 1
^^^^^^^^^

Very simple example, the normal case, include a DLL with a known prefix
from its package directory.

.. code:: yaml

   - module-name: 'vosk'
     dlls:
       - from_filenames:
           prefixes:
             - 'libvosk'

Example 2
^^^^^^^^^

Another more complex example, in which the DLL lives in a subfolder, and
is even architecture dependant.

.. code:: yaml

   - module-name: 'tkinterweb'

     dlls:
       - from_filenames:
           relative_path: 'tkhtml/Windows/32-bit'
           prefixes:
             - 'Tkhtml'
         when: 'win32 and arch_x86'
       - from_filenames:
           relative_path: 'tkhtml/Windows/64-bit'
           prefixes:
             - 'Tkhtml'
         when: 'win32 and arch_amd64'

Example 3
^^^^^^^^^

Yet another example with architecture dependent DLLs all in one package,
that we do not want to include all, and in fact, must not include all at
the same time. This one selected by platform suffixes for DLLs.

.. code:: yaml

   - module-name: 'tls_client.cffi'

   dlls:
      - from_filenames:
         relative_path: 'dependencies'
         prefixes:
            - 'tls-client'
         suffixes:
            - 'dll'
         when: 'win32'
      - from_filenames:
         relative_path: 'dependencies'
         prefixes:
            - 'tls-client'
         suffixes:
            - 'so'
         when: 'linux'
      - from_filenames:
         relative_path: 'dependencies'
         prefixes:
            - 'tls-client'
         suffixes:
            - 'dylib'
         when: 'macos'

EXEs
====

To Nuitka, an "EXEs" *are* like DLLs_. Basically only a DLL with the
executable bit set. So, for a given selector, you can just add
``executable: yes`` with the default for a DLL configuration being
``executable: no``.

Examples
--------

.. code:: yaml

   dlls:
     - from_filenames:
         prefixes:
           - 'subprocess'
         executable: 'yes'
     - from_filenames:
         prefixes:
           - ''  # first match decides

Anti-Bloat
==========

.. code:: yaml

   anti-bloat:
     - description: 'remove tests'
       context: ''
       module_code: 'from hello import world'
       replacements_plain: ''
       replacements_re: ''
       replacements: ''
       change_function:
          'get_extension': 'un-callable'

       append_result: ''
       append_plain: ''
       when: ''

If you want to replace code, for example to remove dependencies, you can
do that here.

.. note::

   For avoiding optional modules imports, see the ``no-auto-follow``
   that is applicable in implict imports section.

Features
--------

|  ``description``: description of what this ``anti-bloat`` does
|  ``context``:
|  ``module_code``: replace the entire code of a module with it
|  ``replacements_plain``: search an replace plain strings
|  ``replacements_re``: search an replace regular expressions
|  ``replacements``: search a plain string and replace with an
   expression result
|  ``change_function``: replace the code of a function. ``un-callable``
   removes the function
|  ``append_result``: append the result of an expression to module code
|  ``append_plain``: append plain text to the module code
|  ``when``: when_ is documented in a separate section

Examples
--------

coming soon

Implicit-Imports
================

.. code:: yaml

   implicit-imports:
     - depends:
        - 'ctypes'

       pre-import-code: ''
       post-import-code: ''
       when: 'version("package_name") >= (1, 2, 1)'

Features
--------

|  ``depends``: modules that are required by this module
|  ``no-auto-follow``: list of modules not really required by this
   module
|  ``pre-import-code``: code to execute before a module is imported
|  ``post-import-code``: code to execute after a module is imported
|  ``when``: when_ is documented in a separate section

Examples
--------

In this example, environment variables needed to resolve the path of the
Qt plugins and the fonts directory are used. This is only needed on
Linux and on standalone, and here is how the standard configuration does
it. And there there more mundane implicit requirements, that come from
the package using an extension module and on the inside ``cv2``.

.. code:: yaml

   - module-name: 'cv2'
       - depends:
           - 'cv2.cv2'
           - 'numpy'
           - 'numpy.core'
       - pre-import-code:
           - |
             import os
             os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(__file__), 'qt/plugins')
             os.environ['QT_QPA_FONTDIR'] = os.path.join(os.path.dirname(__file__), 'qt/fonts')
         when: 'linux and standalone'

For the ``no-auto-follow`` this shows how to not follow to a module,
even with ``--follow-imports`` being given just because of this module
doing an import. If another one does the import, it will be followed
into still, but this particular modules not not cause it. The message
given is shown when that happens. If if is ``ignore``, nothing will be
displayed.

In this concrete example, ``tdqm`` would register with ``pandas``
methods if possible, but handles it not being found gracefully. No need
to include it just to do that, if ``pandas`` is otherwise unused.

.. code:: yaml

   - module-name: 'tqdm.std'
     anti-bloat:
       - no-auto-follow:
           'pandas': 'ignore'

Options
=======

.. code:: yaml

   options:
     checks:
       - description: 'fix crash'
         console: 'yes'
         macos_bundle: 'yes'
         macos_bundle_as_onefile: 'no'
         support_info: 'warning'
         when: 'macos'

If a module requires specific options, you can specify them here, to
make sure the user is informed of them.

Features
--------

|  ``description``: description of what this does
|  ``console``: whether the console should be enabled. Choose between
   ``yes``, ``no``, ``recommend``
|  ``macos_bundle``: Choose between ``yes``, ``no``, ``recommend``
|  ``macos_bundle_as_onefile``: Choose between ``yes``, ``no``
|  ``support_info``: Choose between ``info``, ``warning``, ``error``
|  ``when``: when_ is documented in a separate section

Examples
--------

On macOS, the popular ``wx`` toolkit will not work unless the
application is a GUI program. The result is a crash without any
information to the user. It also will not work unless it's in a macOS
bundle. So this configuration will make sure to warn or error out in
case these modes are not enabled.

.. code:: yaml

   - module-name: 'wx'
     options:
       checks:
         - description: 'wx will crash in console mode during startup'
           console: 'yes'
           when: 'macos'
         - description: 'wx requires program to be in bundle form'
           macos_bundle: 'yes'
           when: 'macos'

Import-Hacks
============

.. code:: yaml

   import-hacks:
     - package-paths:
        - 'vtkmodules'

       package-dirs:
         - 'win32comext'

       find-dlls-near-module:
         - 'shiboken2'

       when: "True"

Features
--------

|  ``package-paths``:
|  ``package-dirs``:
|  ``find-dlls-near-module``:
|  ``global-sys-path:``: for modules that manipulate ``sys.path``

Examples
--------

The module ``tkinterweb`` contains the following code, that Nuitka
doesn't yet understand well enough at compile time.

.. code:: python

   sys.path.append(os.path.dirname(os.path.realpath(__file__)))

What this does is to add the package directory, such that Python files
in the package directory are visible as global imports. To Nuitka these
will not be resolvable, unless we help it.

.. code:: yaml

   - module-name: 'tkinterweb'
     import-hacks:
       - global-sys-path:
           # This package forces itself into "sys.path" and expects absolute
           # imports to be available.
           - ''

This adds the relative path ``''`` during compile time to the import
resolution, making it work. This makes the ``sys.path`` modification
visible to Nuitka. Suffice to say that this is very unusual, thus it's
in the import hacks category.

Variables
=========

It is possible to use compile time package information in an expression
like the e.g. when_ clauses, but also for some other values. They are
then accessed via the ``get_variable`` function and reporting and
caching traces their usage.

.. note::

   Where they are not currently working, we might have to add support
   for that.

.. code:: yaml

   variables:
     setup_code: 'import whatever'
     declarations:
       'variable1_name': 'whatever.something()'
       'variable2_name': 'whatever.something2()'

Constants
=========

.. code:: yaml

   constants:
     - declarations:
         'suffix': '-Windows'
       when: "win32"
     - declarations:
         'suffix': '-Linux'
       when: "linux"
     - declarations:
         'suffix': '-MacOS'
       when: "macos"

It is possible to use compile time package information in an expression
like the e.g. when_ clauses, but also for some other values that allow
using an expression_, e.g. when constructing paths. They are then
accessed via the ``get_variable`` function and reporting and caching
traces their usage.

They are most useful to avoid repeated usage of OS specific values
without making using configuration repeated with different when_
clauses, as those and then only there for defined constants.

We do not yet have examples, we intend to use this to cleanup a few of
the configurations that we already have or use it in the future.

Expression
==========

Example of an expression:

.. code:: python

   macos and python3_or_higher

These variables are available for quick tests. The idea being that
actual code is never going to be necessary in these expressions.

OS Indications
--------------

To check what OS is selected, we got these.

|  ``macos``: ``True`` if OS is MacOS
|  ``win32``: ``True`` if OS is Windows
|  ``linux``: ``True`` if OS is Linux

Compilation modes
-----------------

|  ``standalone``: ``True`` if standalone mode is activated with
   ``--standalone`` or ``--onefile``
|  ``module_mode``: ``True`` if module mode is activated with
   ``--module``
|  ``deployment``: ``True`` if deployment mode is activated with
   ``--deployment``

.. note::

   For non-deployment changes, these can be annotated with the
   ``deployment`` annotation. We need to be careful with general doing
   changes in that way, because it makes testing harder, and changes
   e.g. to make numpy not hide bugs of our packaging of its DLLs behind
   a misleading error, are usually very good for deployment too.

Python Flavors
--------------

To check the Python flavor, we got these.

|  ``anaconda``: ``True`` if Anaconda Python used, but see
   ``is_conda_package`` below
|  ``debian_python``: ``True`` if Debian Python used

More could be added, but these are the trouble makers that sometimes
need special handling due to them modifying PyPI packages for themselves
to use.

Package Versions
----------------

To check the version of packages and distributions, we got these.

|  ``version``: ``tuple of int`` get version of distribution
|  ``get_dist_name``: ``str`` resolve package name to distribution

For packages, that have multiple distribution names potentially, it's
best to use it like this ``version(get_dist_name("cv2")) < (4,6)`` as
often this can be one of many different names.

.. note::

   In many cases, package name and distribution name align, but that is
   not always the case.

Python Versions
---------------

For limiting to certain Python versions, we got Python3 indicators and
more Python version specific ones:

|  ``before_python3``: ``True`` if Python 2 used
|  ``python3_or_higher``: ``True`` if Python 3 used
|  ``python[major][minor]_or_higher``: e.g. ``python310_or_higher``
|  ``before_python[major][minor]``: e.g. ``before_python310``

Anti-Bloat
----------

The Anti-Bloat plugin provides you with additional variables from
command line choices. These are mainly intended for the ``anti-bloat``
section, but work everywhere now.

|  ``use_setuptools``: ``True`` if ``--noinclude-setuptools-mode`` is
   not set to ``nofollow`` or ``error``
|  ``use_pytest``: ``True`` if ``--noinclude-pytest-mode`` is not set to
   ``nofollow`` or ``error``
|  ``use_unittest``: ``True`` if ``--noinclude-unittest-mode`` is not
   set to ``nofollow`` or ``error``
|  ``use_ipython``: ``True`` if ``--noinclude-IPython-mode`` is not set
   to ``nofollow`` or ``error``
|  ``use_dask``: ``True`` if ``--noinclude-dask-mode`` is not set to
   ``nofollow`` or ``error``

All these are bools as well.

Package Versions
----------------

To check the version of a package there is the ``version`` function,
which you simply pass the name to and you then get the version as a
tuple. An example:

.. code:: python

   version("rich") is not None and version("rich") >= (10, 2, 2)

It returns ``None`` if the package isn't installed, sometimes this need
handling, e.g. in the configuration of another package.s

Due to differences in DLL and data file layout, conda packages (from
Anaconda) will be different. But running ``anaconda`` is not sufficient,
in case the package from from ``pip install`` rather than ``conda
install``, so this allows to make a difference for this.

It returns a boolean value. No need to check for ``anaconda``, that is
implied of course, and probably should never be used, but this instead.

.. code:: python

   is_conda_package("shapely")

Python Flags
------------

Also, the global (or module local in the future) compilation modules,
like ``no_asserts``, ``no_docstrings``, and ``no_annotations`` are
available. These are for use in ``anti-bloat`` where packages sometimes
will not work unless helped somewhat.

Experimental Settings
---------------------

For development, there is a function ``experimental`` that you can use
to check for the presence of flags given on the command line. So you can
use that to toggle a change on or off until you are happy with it, or
attach it to an incomplete feature of Nuitka.

.. code:: python

   # bool, true if --experimental=some-flag-name given
   experimental('some-flag-name')

Variable/Constant Values
------------------------

For variables/constants to be used, they need to be defined within the
package configuration as constants_ or variables_. They then become
accessible, but variables are only evaluated if they are actually used.
That means, if e.g. the when_ clause causes a variable to be unused,
it's never evaluated.

.. note::

   Where an expression_ is not currently working, we might have to add
   support for that, this is an ongoing effort.

Examples
--------

The most simple form just picks up information from a package, in this
instance, we ask the package about the backend it would use with the
current configuration and all, and force the decision to be that by
changing the very same function to be compiled into producing just that
value without further investigation.

This is a simple solution to a common problem, namely to persist such
decisions from the original compiling environment to the target
environment.

Example 1
^^^^^^^^^

.. code:: yaml

   - module-name: 'toga.platform'
     variables:
       setup_code: 'import toga.platform'
       declarations:
         'toga_backend_module_name': 'toga.platform.get_platform_factory(). __name__'
     anti-bloat:
       - change_function:
           'get_platform_factory': "'importlib.import_module(%r)' % get_variable('toga_backend_module_name')"

when
====

In the ``when`` part an expression_ is given and if it matches, the
entry it is attached to is applied, otherwise not. This expression is a
normal string evaluated by Python's eval function. Nuitka provides
variables in the context for this.

********************
 Where else to look
********************

There is a post series under the tag ``package_config`` found
https://nuitka.net/blog/tag/package_config.html that explains some
things in more detail and is going to cover this and expand it for some
time.

Then of course, there is also the current package configuration file,
located at
https://github.com/Nuitka/Nuitka/blob/develop/nuitka/plugins/standard/standard.nuitka-package.config.yml
that is full of examples.
