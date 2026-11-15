:orphan:

.. meta::
   :description: What Nuitka is, what it fixes, and how to try it: a Python program becomes a standalone executable with one command.
   :keywords: nuitka,python compiler,exe,standalone,onefile,deployment,ip protection

####################
 Introducing Nuitka
####################

Someone suggested Nuitka for your project, maybe a colleague, maybe an
AI assistant. This page shows what it does in under a minute, and what
it changes for your team.

.. nuitka-example-cast:: csvsum
   :poster: npt:0:2

.. grid:: 1 1 3 3
   :gutter: 3
   :class-container: step-cards

   .. grid-item-card:: 1. Your code

      An ordinary Python program, here a small tool that adds up a
      column of a CSV file. Nothing in it is written for Nuitka.

   .. grid-item-card:: 2. One command

      Nuitka translates it to C, compiles it, and bundles Python with
      it into a single file.

   .. grid-item-card:: 3. Your program

      ``csvsum.bin``, or ``csvsum.exe`` on Windows, runs on machines
      without Python and prints the same result.

********************************
 What problem does Nuitka solve
********************************

Python programs are usually shipped as source code. Whoever runs them
needs the right Python version and every package installed, and can read
every line. Nuitka removes that step:

-  **No Python needed.** The executable contains your compiled code, the
   Python runtime, and the packages it uses. Users just start it.

-  **One file or one folder.** Onefile mode creates a single executable,
   standalone mode creates a folder that you can copy or put into an
   installer.

-  **Your source stays yours.** Your code is translated to C and
   compiled to machine code, so you no longer ship readable ``.py``
   files. With **Nuitka Commercial**, data files, constants, and
   tracebacks are protected too.

-  **Usually faster.** Compiled programs often run and start faster, and
   they behave like they do with CPython.

******************
 Before and after
******************

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   -  -  What the user needs
      -  Sending ``csvsum.py``
      -  Sending ``csvsum.exe``

   -  -  Python
      -  Installed, in a compatible version
      -  Nothing, it is included

   -  -  Packages your program uses
      -  Installed with ``pip``
      -  Nothing, they are included

   -  -  Steps to start the program
      -  Install Python, install packages, run a command
      -  Run it

   -  -  Access to your source code
      -  Anyone with the file can read it
      -  Delivered as compiled machine code

********************************
 Will it work with what we use?
********************************

Nuitka is fully compatible with |SUPPORTED_PYTHONS|, and works on
**Windows**, **macOS**, **Linux**, and more.

Packages that need special handling, such as Qt bindings, NumPy, and
many others, are covered by built-in plugins and package configuration.
Most programs compile without changes. When one does not, Nuitka names
the problem and links to a page explaining the fix.

********************
 What does it cost?
********************

Nuitka is free and open source. It is AGPLv3 licensed, but that does not
apply to the software you compile with it. Your code, and the binaries
created from it, remain yours under your own license.

**Nuitka Commercial** is an optional subscription for businesses. It
adds protection for data files and program constants, encrypted
tracebacks, Windows services, automatic updates, legacy Windows support,
and direct support. See :doc:`/doc/commercial` for the full list.

************************
 Try it on your project
************************

Run this on the machine where your program already works:

.. code:: bash

   python -m pip install -U Nuitka
   python -m nuitka --mode=onefile your_program.py

The :doc:`/tours/beginner` goes through it step by step, with examples
for command-line tools, desktop programs, data files, data science, web
services, and compiled modules.

************
 Next Steps
************

-  :doc:`/tours/beginner` for your first build and examples.

-  :doc:`/tours/it-manager` for the business view, or
   :doc:`/tours/deployment` for the technical one.

-  :doc:`/doc/commercial` for the commercial features.

-  :doc:`/pages/support` if you get stuck.

.. include:: variables.inc
