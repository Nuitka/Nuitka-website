:orphan:

#############################################
 Compiled package hidden by existing package
#############################################

****************************
 The Problem in a Few Words
****************************

When Nuitka produces a compiled package right next to its source code,
might not be loaded. This happens when a directory with the same name as
the package exists alongside the compiled package. place.

************
 Background
************

Python has a priority system that will prefer a directory ``something``
with ``__init__.py`` of the proper name over an extension module
``something.pyd`` / ``something.so`` located in the same place.

This means that if you have a directory named ``kitty`` and Nuitka
compiles a package (with Python 3.10 on Windows for example) named
``kitty`` into ``kitty.cp310-win_amd64.pyd``, Python will prioritize the
``kitty`` directory over the compiled ``kitty.cp310-win_amd64.pyd``.
Therefore, the compiled code will not be used. This is different from
plain Python files, where ``something.py`` can be replaced by
``something.pyd`` / ``something.so`` in the same location. In that case,
the compiled code will be used.

*********
 Example
*********

.. code:: bash

   cd tests/packages/sub_package
   python -m nuitka --mode=package --remove-output --no-pyi-file kitty

.. code::

   ...
   Nuitka:WARNING: The compilation result is hidden by package directory 'kitty'.
   Nuitka:WARNING: Importing will not use compiled code while it exists because it
   Nuitka:WARNING: has precedence while both exist, out e.g. '--output-dir=output' to
   Nuitka:WARNING: sure is importable.
   Nuitka:WARNING:     Complex topic! More information can be found at
   Nuitka:WARNING: https://nuitka.net/info/compiled-package-hidden-by-package.html
   Nuitka: Successfully created
   Nuitka: '~\repos\Py2C\tests\packages\sub_package\kitty.cp310-win_amd64.pyd'.

.. code::

   $ ls
   kitty/  kitty.cp310-win_amd64.pyd*

.. code::

   python3.10
   >>> import kitty
   ...
   >>> kitty.__compiled__
   Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
   AttributeError: module 'kitty' has no attribute '__compiled__'

*************
 Consequence
*************

When compiling packages, replacing source code with its compiled form is
more complex in package mode.

****************
 Recommendation
****************

To avoid this issue, use the ``--output-dir`` option to place the
compiled package into a dedicated folder, such as ``build``. Then,
ensure you import the package from this directory.

For example, if you compile the ``kitty`` package with
``--output-dir=build``, you should import it from the ``build``
directory.

You can verify that the compiled code is being used by checking for the
``__compiled__`` attribute on the imported module. If it's present, the
compiled code is being used.
