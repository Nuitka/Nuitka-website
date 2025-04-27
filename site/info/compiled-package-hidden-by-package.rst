:orphan:

#############################################
 Compiled package hidden by existing package
#############################################

****************************
 The Problem in a Few Words
****************************

The way Nuitka produced the module/package output, it will not load the
compiled code, if imported from there before copying it to a different
place.

************
 Background
************

Python has a priority system that will prefer a directory ``something``
with ``__init__.py`` of the proper name over an extension module
``something.pyd`` / ``something.so`` located in the same place.

So what Nuitka replaced just now, cannot replace the source code until
you take further action. What's confusing about this, is that for plain
Python files, the priority is not an issue, so ``something.py`` can be
replaced with an extension module ``something.pyd`` / ``something.so``
located in the same place.

*********
 Example
*********

..
   code: shell

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

..
   code

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

Use ``--output-dir`` and place the output into a dedicated folder, say
``build`` and then make sure to import from there. You can verify by
checking your extension module ``__compiled__`` attribute, it should be
present.
