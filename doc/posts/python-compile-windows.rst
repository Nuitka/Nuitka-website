.. post:: 2022/05/15 07:46:50
   :tags: Python, Windows, Nuitka, HowTo
   :author: Kay Hayen

###########################
 Compile Python on Windows
###########################

Looking to create an executable from Python script? Let me show you the
full steps to achieve it on *Windows*.

************************************************************************
 Steps to create a Windows executable from a Python script using Nuitka
************************************************************************

Step 1: Add Python to Windows Path
==================================

The simple way to add Python to the ``PATH`` do this is to check the box
during installation of CPython. You just `download python
<https://www.python.org/downloads/>`__ and install or modify Python by
checking the box in the installer:

.. image:: images/Python-Installation-Screen-Windows.png
   :alt: check modify PATH when you install python

This box is not enabled by default. You can also manually add the Python
installation path to ``PATH`` environment variable.

.. note::

   You do not strictly have to execute this step, you can also replace
   ``python`` with just the absolute path, e.g.
   ``C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe``
   but that can become inconvenient.

Step 2: Open a Windows Prompt
=============================

This can be ``cmd.exe`` or Windows Terminal, or from an IDE like Visual
Code or PyCharm. And then type ``python`` to verify the correct
installation, and ``exit`` to leave the Python prompt again.

.. image:: images/Python-Installation-CMD.png
   :alt: Launch Python in Windows prompt to verify

Step 3: Install the Nuitka Python Compiler package
==================================================

Now install Nuitka with the following command.

.. code:: bash

   python -m pip install nuitka

.. image:: images/Nuitka-Installation-CMD.png
   :alt: Install Nuitka in Python

Step 4: Run your Program
========================

Now run your program from the terminal. Convince yourself that
everything is working.

.. code:: bash

   python fancy-program.py

.. note::

   If it's a GUI program, make sure it has a ``.pyw`` suffix. That is
   going to make Python know it's one.

Step 5: Create the Executable using Nuitka
==========================================

.. code:: bash

   python -m nuitka --onefile fancy-program.py

In case of a terminal program, add one of many options that Nuitka has
to adapt for platform specifics, e.g. program icon, and so on.

.. code:: bash

   python -m nuitka --onefile --windows-disable-console fancy-program.py

This will create ``fancy-program.exe``.

Step 6: Run the Executable
==========================

Your executable should appear right near ``fancy-program.py`` and
opening the explorer or running ``fancy-program.exe`` from the Terminal
should be good.

.. code:: bash

   fancy-program.exe
