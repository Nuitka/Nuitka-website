:orphan:

##########################
 Tutorial Setup and Build
##########################

This is basic steps if you have nothing installed, of course if you have
any of the parts, just skip it.

*******
 Setup
*******

Install Python
==============

-  Download and install Python from
   https://www.python.org/downloads/windows

-  Select one of ``Windows x86-64 web-based installer`` (64 bits Python,
   recommended) or ``x86 executable`` (32 bits Python) installer.

-  Verify it's working using command ``python --version``.

Install Nuitka
==============

-  ``python -m pip install Nuitka``

-  Verify using command ``python -m nuitka --version``

**************************
 Write some code and test
**************************

Create a folder for the Python code
===================================

-  ``mkdir`` HelloWorld

-  make a python file named **hello.py**

.. code:: python

   def talk(message):
       return "Talk " + message


   def main():
       print(talk("Hello World"))


   if __name__ == "__main__":
       main()

Test your program
=================

Do as you normally would. Running Nuitka on code that works incorrectly
is not easier to debug.

.. code:: bash

   python hello.py

----

Build it using
==============

.. code:: bash

   python -m nuitka hello.py

.. note::

   This will prompt you to download a C caching tool (to speed up
   repeated compilation of generated C code) and a MinGW64 based C
   compiler, unless you have a suitable MSVC installed. Say ``yes`` to
   both those questions.

Run it
======

Execute the ``hello.exe`` created near ``hello.py``.

Distribute
==========

To distribute, build with ``--mode=standalone`` option, which will not
output a single executable, but a whole folder. Copy the resulting
``hello.dist`` folder to the other machine and run it.

You may also try ``--mode=onefile`` which creates a single executable
file. However, we recommend first ensuring your program works correctly
with ``--mode=standalone`` before using ``--mode=onefile``, as any
issues (such as missing data files) are easier to diagnose and fix in
standalone mode.

.. note::

   ``--mode=onefile`` automatically includes ``--mode=standalone``
   behavior, so you do not need to pass both options together.
