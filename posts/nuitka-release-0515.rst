This is to inform you about the new stable release
of `Nuitka <https://nuitka.net>`_. It is the extremely
compatible Python compiler,  `"download now" </doc/download.html>`_.

This release enables SSA based optimization, the huge leap, not so much
in terms of actual performance increase, but for now making the things
possible that will allow it.

This has been in the making literally for years. Over and over, there
was just "one more thing" needed. But now it's there.

The release includes much stuff, and there is a perspective on the open
tasks in the summary, but first out to the many details.

Bug Fixes
=========

-  Standalone: Added implicit import for ``reportlab`` package
   configuration dynamic import. Fixed in 0.5.14.1 already.

-  Standalone: Fix, compilation of the ``ctypes`` module could happen
   for some import patterns, and then prevented the distribution to
   contain all necessary libraries. Now it is made sure to not include
   compiled and frozen form both. `Issue#241
   <http://bugs.nuitka.net/issue241>`__. Fixed in 0.5.14.1 already.

-  Fix, compilation for conditional statements where the boolean check
   on the condition cannot raise, could fail compilation. `Issue#240
   <http://bugs.nuitka.net/issue240>`__. Fixed in 0.5.14.2 already.

-  Fix, the ``__import__`` built-in was making static optimization
   assuming compile time constants to be strings, which in the error
   case they are not, which was crashing the compiler. `Issue#240
   <http://bugs.nuitka.net/issue245>`__.

   .. code:: python

      __import__(("some.module",))  # tuples don't work

   This error became only apparent, because now in some cases, Nuitka
   forward propagates values.

-  Windows: Fix, when installing Python2 only for the user, the
   detection of it via registry failed as it was only searching system
   key. This was `a github pull request
   <https://github.com/kayhayen/Nuitka/pull/8>`__. Fixed in 0.5.14.3
   already.

-  Some modules have extremely complex expressions requiring too deep
   recursion to work on all platforms. These modules are now included
   entirely as bytecode fallback. `Issue#240
   <http://bugs.nuitka.net/issue240>`__.

-  The standard library may contain broken code due to installation
   mistakes. We have to ignore their ``SyntaxError``. `Issue#244
   <http://bugs.nuitka.net/issue244>`__.

-  Fix, pickling compiled methods was failing with the wrong kind of
   error, because they should not implement ``__reduce__``, but only
   ``__deepcopy__``. `Issue#219 <http://bugs.nuitka.net/issue219>`__.

-  Fix, when running under ``wine``, the check for scons binary was
   fooled by existence of ``/usr/bin/scons``. `Issue#251
   <http://bugs.nuitka.net/issue251>`__.

New Features
============

-  Added experimental support for Python3.5, coroutines don't work yet,
   but it works perfectly as a 3.4 replacement.

-  Added experimental Nuitka plug-in framework, and use it for the
   packaging of Qt plugins in standalone mode. The API is not yet stable
   nor polished.

-  New option ``--debugger`` that makes ``--run`` execute directly in
   ``gdb`` and gives a stack trace on crash.

-  New option ``--profile`` executes compiled binary and outputs
   measured performance with ``vmprof``. This is work in progress and
   not functional yet.

-  Started work on ``--graph`` to render the SSA state into diagrams.
   This is work in progress and not functional yet.

-  Plug-in framework added. Not yet ready for users. Working ``PyQt4``
   and ``PyQt5`` plug-in support. Experimental Windows
   ``multiprocessing`` support. Experimental PyLint warnings disable
   support. More to come.

-  Added support for Anaconda accelerated mode on macOS by modifying the
   rpath to the Python DLL.

-  Added experimental support for ``multiprocessing`` on Windows, which
   needs monkey patching of the module to support compiled methods.

Optimization
============

-  The SSA analysis is now enabled by default, eliminating variables
   that are not shared, and can be forward propagated. This is currently
   limited mostly to compile time constants, but things won't remain
   that way.

-  Code generation for many constructs now takes into account if a
   specific operation can raise or not. If e.g. an attribute look-up is
   known to not raise, then that is now decided by the node the looked
   is done to, and then more often can determine this, or even directly
   the value.

-  Calls to C-API that we know cannot raise, no longer check, but merely
   assert the result.

-  For attribute look-up and other operations that might be known to not
   raise, we now only assert that it succeeds.

-  Built-in loop-ups cannot fail, merely assert that.

-  Creation of built-in exceptions never raises, merely assert that too.

-  More Python operation slots now have their own computations and some
   of these gained overloads for more compile time constant
   optimization.

-  When taking an iterator cannot raise, this is now detected more
   often.

-  The ``try``/``finally`` construct is now represented by duplicating
   the final block into all kinds of handlers (``break``, ``continue``,
   ``return``, or ``except``) and optimized separately. This allows for
   SSA to trace values more correctly.

-  The ``hash`` built-in now has dedicated node and code generation too.
   This is mostly intended to represent the side effects of dictionary
   look-up, but gives more compact and faster code too.

-  Type ``type`` built-in cannot raise and has no side effect.

-  Speed improvement for in-place float operations for ``+=`` and
   ``*=``, as these will be common cases.

Tests
=====

-  Made the construct based testing executable with Python3.

-  Removed warnings using the new PyLint warnings plug-in for the
   reflected test. Nuitka now uses the PyLint annotations to not warn.
   Also do not go into PyQt for reflected test, not needed. Many Python3
   improvements for cases where there are differences to report.

-  The optimization tests no longer use 2to3 anymore, made the tests
   portable to all versions.

-  Checked more in-place operations for speed.

Organisational
==============

-  Many improvements to the coverage taking. We can hope to see public
   data from this, some improvements were triggered from this already,
   but full runs of the test suite with coverage data collection are yet
   to be done.

Summary
=======

The release includes many important new directions. Coverage analysis
will be important to remain certain of test coverage of Nuitka itself.
This is mostly done, but needs more work to complete.

Then the graphing surely will help us to debug and understand code
examples. So instead of tracing, and reading stuff, we should visualize
things, to more clearly see, how things evolve under optimization
iteration, and where exactly one thing goes wrong. This will be improved
as it proves necessary to do just that. So far, this has been rare.
Expect this to become end user capable with time. If only to allow you
to understand why Nuitka won't optimize code of yours, and what change
of Nuitka it will need to improve.

The comparative performance benchmarking is clearly the most important
thing to have for users. It deserves to be the top priority. Thanks to
the PyPy tool ``vmprof``, we may already be there on the data taking
side, but the presenting and correlation part, is still open and a fair
bit of work. It will be most important to empower users to make
competent performance bug reports, now that Nuitka enters the phase,
where these things matter.

As this is a lot of ground to cover. More than ever. We can make this
compiler, but only if you help, it will arrive in your life time.
