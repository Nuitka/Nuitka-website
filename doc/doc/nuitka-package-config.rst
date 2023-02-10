##############################
 Nuitka Package Configuration
##############################

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
filename of your Yaml file to ``--user-package-configuration-file``.

.. note::

   If this could be interesting for the whole user base of Nuitka,
   please do a PR that adds it to the general files. In this way, not
   every user has to repeat what you just did, and we can collectively
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

Examples
--------

The most simple form just adds a data folder. The data files are in a
folder and lives inside the package directory.

.. code:: yaml

   - module-name: 'customtkinter'
     data-files:
        dirs:
          - 'assets'

.. note::

   The ``dest_path`` is very unlikely necessary. It defaults to the
   ``.`` relative path. It would have to be a strange package or some
   code modification on top, that would require data files to live in
   another spot in the standalone distribution.

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

Very simple example, the normal case, include a DLL with a known prefix
from its package directory.

.. code:: yaml

   - module-name: 'vosk'
     dlls:
       - from_filenames:
           prefixes:
             - 'libvosk'

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

when
====

If this expression matches, the entry is executed, otherwise not. This
expression is a normal string evaluated by Python's eval function.
Nuitka provides variables for this.

Example of an expression:

.. code:: python

   macos and python3_or_higher

These variables are currently available:

|  ``macos``: ``True`` if OS is MacOS
|  ``win32``: ``True`` if OS is Windows
|  ``linux``: ``True`` if OS is Linux
|  ``anaconda``: ``True`` if Anaconda Python used
|  ``debian_python``: ``True`` if Debian Python used
|  ``standalone``: ``True`` if standalone mode is activated
|  ``module_mode``: ``True`` if module mode is activated
|  ``before_python3``: ``True`` if Python 2 used
|  ``python3_or_higher``: ``True`` if Python 3 used

There are also more Python version specific ones. For each Python
version supported by Nuitka there are the following:

|  ``python[major][minor]_or_higher``: e.g. ``python310_or_higher``
|  ``before_python[major][minor]``: e.g. ``before_python310``

The Anti-Bloat plugin provides you with additional variables. These are
only available in anti-bloat.

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

All these are bools.

To check the version of a package there is the ``version`` function,
which you simply pass the name to and you then get the version as a
tuple. An example:

.. code:: python

   version('shapely') < (1, 8, 1)

It returns ``None`` if the package isn't installed.

Also, compilation modules, like ``no_asserts``, ``no_docstrings``, and
``no_annotations`` are available. These are for use in ``anti-bloat``
where packages sometimes will not work unless helped somewhat.

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
