:orphan:

######################################
 Unsupported Windows App Store Python
######################################

****************************
 The Problem in a few Words
****************************

Python on Windows can be installed via the Windows app store. While this
may be more convenient for the user, for compilation, this distribution
is missing essential bits and will not work.

************
 Background
************

Nuitka needs to be able to access all files, in order to inspect them
and to make them work on other machines. With Windows Store Python, when
Nuitka tries to even look at ``sys.executable`` (typically your
``python.exe`` on Windows), an ``OSError`` is given rather than the
needed look at e.g. Windows Resources to keep.

*************
 Consequence
*************

Because of these limitations, it was decided that this Python will not
be supported by Nuitka and you need to install a supported one. Check
out https://nuitka.net/doc/user-manual.html#requirements which lists
CPython and Anaconda as supported.

****************
 Recommendation
****************

Sticking with CPython which is best supported and should give best
portability. It will work as well as the Windows App Store Python for
you, under the hood it's the same code after all, but it's the official
Python form for Windows.
