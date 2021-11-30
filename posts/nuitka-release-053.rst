This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is mostly a follow up, resolving points that have become
possible to resolve after completing the C-ish evolution of Nuitka. So
this is more of a service release.

New Features
============

-  Improved mode ``--improved`` now sets error lines more properly than
   CPython does in many cases.

-  The ``-python-flag=-S`` mode now preserves ``PYTHONPATH`` and
   therefore became usable with virtualenv.

Optimization
============

-  Line numbers of frames no longer get set unless an exception occurs,
   speeding up the normal path of execution.

-  For standalone mode, using ``--python-flag-S`` is now always possible
   and yields less module usage, resulting in smaller binaries and
   faster compilation.

Bug Fixes
=========

-  Corrected an issue for frames being optimized away where in fact they
   are still necessary. `Issue#140 <http://bugs.nuitka.net/issue140>`__.
   Fixed in 0.5.2.1 already.

-  Fixed handling of exception tests as side effects. These could be
   remainders of optimization, but didn't have code generation. Fixed in
   0.5.2.1 already.

-  Previously Nuitka only ever used the statement line as the line
   number for all the expression, even if it spawned multiple lines.
   Usually nothing important, and often even more correct, but sometimes
   not. Now the line number is most often the same as CPython in full
   compatibility mode, or better, see above. `Issue#9
   <http://bugs.nuitka.net/issue9>`__.

-  Python3.4: Standalone mode for Windows is working now.

-  Standalone: Undo changes to ``PYTHONPATH`` or ``PYTHONHOME`` allowing
   potentially forked CPython programs to run properly.

-  Standalone: Fixed import error when using PyQt and Python3.

New Tests
=========

-  For our testing approach, the improved line number handling means we
   can undo lots of changes that are no more necessary.

-  The compile library test has been extended to cover a third potential
   location where modules may live, covering the ``matplotlib`` module
   as a result.

Cleanups
========

-  In Python2, the list contractions used to be re-formulated to be
   function calls that have no frame stack entry of their own right.
   This required some special handling, in e.g. closure taking, and
   determining variable sharing across functions.

   This now got cleaned up to be properly in-lined in a
   ``try``/``finally`` expression.

-  The line number handling got simplified by pushing it into error
   exits only, removing the need to micro manage a line number stack
   which got removed.

-  Use ``intptr_t`` over ``unsigned long`` to store fiber code pointers,
   increasing portability.

Organisational
==============

-  Providing own Debian/Ubuntu repositories for all relevant
   distributions.

-  Windows MSI files for Python 3.4 were added.

-  Hosting of the web site was moved to metal server with more RAM and
   performance.

Summary
=======

This release brings about structural simplification that is both a
follow-up to C-ish, as well as results from a failed attempt to remove
static "variable references" and be fully SSA based. It incorporates
changes aimed at making this next step in Nuitka evolution smaller.
