:orphan:

###################################
 Old Python Windows console issues
###################################

****************************
 The Problem in a few Words
****************************

Windows versions Python 3.4-3.7 compilation results share a problem with
determining the proper encoding to use for inputs and outputs to the
terminal. They default to UTF8, which is good for most of the world, but
not for most of Asia. There on any print, it can crash the program.

************
 Background
************

For these versions, there is a circular dependency in Python, where to
determine the encoding to use, requires an initialized run time, but to
initialize the run time, the encoding must be had, or dedicated code
must be produced to handle the lookup from locale to encoding.

This code would be very complex, but newer Python versions do not
require this and just do the right thing. Therefore it was decided to
not do it. If a commercial user requires it, this can be implemented on
a time basis, i.e. paying for the days it takes.

*************
 Consequence
*************

Using these older version for terminal programs is therefore highly
discouraged. If you disable the console, which you should do for the
final deployment of a GUI program anyway, the warning goes away. Using
these older version is not by itself a problem when there is no terminal
available.

****************
 Recommendation
****************

If you really need this, you can determine the required encodings and
re-create ``sys.stdin``, ``sys.stdout``, and ``sys.stderr`` with proper
ones after the program launched.

If you do not care, e.g. because you do a GUI program, but will
temporarily for debugging have the console, you can disable the mnemonic
with ``--nowarn-mnemonic=old-python-windows-console`` and carry on, the
warning will no longer show itself.

If you know the encoding to use, you can workaround the issue with
``PYTHONIOENCODING`` being set to the proper value other that ``utf-8``.

Everybody else ought to update to at least Python 3.8 where this problem
does not exist.
