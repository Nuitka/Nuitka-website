:orphan:

######################################
 Unsupported Windows App Store Python
######################################

****************************
 The Problem in a Few Words
****************************

Python on Windows can be installed via the Windows app store. While this
may be more convenient for the user, for compilation, this distribution
is missing essential bits and will not work.

.. note::

   As of Nuitka 4.0, only accelerated mode (which is not commonly what
   you use) does not work. Standalone and onefile modes are supported.

************
 Background
************

Nuitka needs to be able to access all files, in order to inspect them
and to make them work on other machines. With Windows Store Python, when
Nuitka tries to even look at ``sys.executable`` (typically your
``python.exe`` on Windows), an ``OSError`` is raised, preventing Nuitka
from inspecting e.g. Windows Resources that it needs.

*************
 Consequence
*************

Because of these limitations, it was decided that this Python will not
be supported by Nuitka and you need to install a supported one. Check
out https://nuitka.net/user-documentation/user-manual.html#requirements
which lists CPython and Anaconda as supported.

****************
 Recommendation
****************

Use CPython, which is best supported and should give the best
portability. It will work as well as the Windows App Store Python for
you — under the hood it is the same code — but it is the official Python
distribution for Windows.
