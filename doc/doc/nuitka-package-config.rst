##############################
 Nuitka Package Configuration
##############################

**************
 Introduction
**************

To make it easier to deal with missing DLLs, implicit imports, data
files, bloat etc. we added a system with YAML files in Nuitka. These are
located under ``Plugins/Standard`` and can easily be extended. The
structure of the name is always ``*nuitka-package.config.yml``.
``standard`` includes all non-stdlib modules. In ``stdlib2`` and
``stdlib3`` there are entries for the standard library. In ``stdlib2``
there are only those for modules that are no longer available in Python
3.

If you want to use your own configuration, you can pass the path of your
YAML to ``--user-package-configuration-file``. If this could be
interesting for ``Nuitka`` itself, please do a PR on the main YAML
files.

*****************************
 The YAML Configuration File
*****************************

At the beginning you will find the following lines, which you can
ignore.

.. code:: yaml

   # yamllint disable rule:line-length
   # yamllint disable rule:indentation
   # yamllint disable rule:comments-indentation
   # too many spelling things, spell-checker: disable
   ---

An entry could look like this:

.. code:: yaml

   - module-name: 'pathlib'
     implicit-imports:
       - depends:
         - 'ntpath'
         - 'posixpath'

``module-name`` is the name of the affected module. We will show you
everything else in detail later.

It is also important to know that you do not have to worry about
formatting. We have programmed our own tool for this, which formats
everything automatically. This is executed via
``bin\autoformat-nuitka-source`` and automatically when pushing with
``git``. We also provide you with schemas that are automatically applied
to the YAML files and support you with auto-completion.

***************
 Documentation
***************

Data Files
==========

.. code:: yaml

   data-files:
     dest_path: '.'
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
|  ``when``: :ref:`jump to <when>`

Examples
--------

coming soon

.. _when:

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

If a module requires DLLs, they must be specified here

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
   |  ``setup_code``:
   |  ``filename_code``:

|  ``dest_path``: target directory
|     ``when``: :ref:`jump to <when>`

Examples
--------

coming soon

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
|  ``module_code``: replace the code of a module
|  ``replacements_plain``:
|  ``replacements_re``:
|  ``replacements``:
|  ``change_function``: replace the code of a function. ``un-callable``
   removes the function
|  ``append_result``:
|  ``append_plain``:
|  ``when``: :ref:`jump to <when>`

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
       when: 'version("nuitka") >= (1, 2, 1)'

If a module has imports that Nuitka can't find, you have to add them
here yourself.

Features
--------

|  ``depends``: modules that are required by this module
|  ``pre-import-code``:
|  ``post-import-code``:
|  ``when``: :ref:`jump to <when>`

Examples
--------

coming soon

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

If a module requires specific options, you can specify them here.

Features
--------

|  ``description``: description of what this does
|  ``console``: whether the console should be enabled. Choose between
   ``yes``, ``no``, ``recommend``
|  ``macos_bundle``: Choose between ``yes``, ``no``, ``recommend``
|  ``macos_bundle_as_onefile``: Choose between ``yes``, ``no``
|  ``support_info``: Choose between ``info``, ``warning``, ``error``
|  ``when``: :ref:`jump to <when>`

Examples
--------

coming soon

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

Examples
--------

coming soon

when
====

If this expression matches, the entry is executed, otherwise not. This
expression is a normal string evaluated by Python's eval function.
Nuitka provides variables for this.

Example of an expression:

.. code:: python

   if macos and python3_or_higher

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

There are also generated ones. For each Python version supported by
Nuitka there are the following:

|  ``python[big][major]_or_higher``: e.g. ``python39_or_higher``
|  ``before_python[big][major]``: e.g. ``before_python39``

The Anti-Bloat plugin provides you with additional variables. These are
only available in anti-bloat.

|  ``use_setuptools``: ``True`` if ``--noinclude-setuptools-mode`` not
   set to ``allow``
|  ``use_pytest``: ``True`` if ``--noinclude-pytest-mode`` not set to
   ``allow``
|  ``use_unittest``: ``True`` if ``--noinclude-unittest-mode`` not set
   to ``allow``
|  ``use_ipython``: ``True`` if ``--noinclude-IPython-mode`` not set to
   ``allow``
|  ``use_dask``: ``True`` if ``--noinclude-dask-mode`` not set to
   ``allow``

All these are bools.

To check the version of a package there is the ``version`` function,
which you simply pass the name to and you then get the version as a
tuple. An example:

.. code:: python

   version('shapely') < (1, 8, 1)
