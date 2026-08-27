:orphan:

.. meta::
   :description: The Nuitka deployment tour: turn your Python program into standalone executables and single files for distribution.
   :keywords: nuitka,deployment,standalone,onefile,distribution,executable

########################
 Nuitka Deployment Tour
########################

Dear deployment user,

you want to give your Python program to other people, and you have heard
Nuitka can help with that. This tour explains how to get from your
source code to something that runs on the machines of your users.

**********
 Overview
**********

Nuitka is a Python compiler. It turns your program into a compiled
binary that does not require a Python installation on the target
machine. That means your users get a program, not a software project.

For deployment, three modes matter:

-  **Accelerated**: compile for speed, but the Python installation is
   still needed on the target machine.

-  **Standalone**: a folder with your program, its dependencies, and the
   needed Python runtime. Copy the folder, run the program.

-  **Onefile**: everything bundled into a single executable file.

We recommend to start with **standalone** and only switch to **onefile**
once your program works there.

*************
 Quick Start
*************

Install Nuitka first:

.. code:: bash

   python -m pip install -U "Nuitka[app]"

Then compile your program:

.. code:: bash

   python -m nuitka --mode=standalone your_program.py

The result is a ``your_program.dist`` folder next to your script. Copy
that folder to another machine and run the executable inside it, no
Python needed there.

When you are ready for a single file:

.. code:: bash

   python -m nuitka --mode=onefile your_program.py

.. note::

   Onefile mode extracts itself to a temporary folder at startup, which
   makes launching slightly slower than standalone mode, and anti-virus
   software is more likely to be suspicious of it.

*************************************
 Data Files and Third Party Packages
*************************************

Most packages work out of the box. Nuitka follows your imports and
bundles what is used.

If your program loads data files, such as images or configuration files,
you need to tell Nuitka to include them:

.. code:: bash

   python -m nuitka --mode=standalone --include-data-files=config.json=. your_program.py

For larger projects, put these settings into ``nuitka-project:`` comment
directives at the top of your main program, so the build command stays
simple and reproducible. See :doc:`/user-documentation/user-manual` for
details.

If something goes wrong, check
:doc:`/user-documentation/common-issue-solutions` for the most common
situations first.

***************
 Going Further
***************

-  :doc:`/user-documentation/use-cases` covers many deployment scenarios
   in detail, including plugins for your program.

-  :doc:`/user-documentation/user-manual` is the complete reference for
   all options.

-  For protecting your program from reverse engineering, encrypted
   outputs, or automatic updates for your users, see
   :doc:`/doc/commercial`.

.. include:: ../variables.inc
