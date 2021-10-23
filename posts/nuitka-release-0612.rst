This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is yet again a massive improvement in many ways with lots
of bug fixes and new features.

***********
 Bug Fixes
***********

-  Windows: Icon group entries were not working properly in some cases,
   leading to no icon or too small icons being displayed.

-  Standalone: The PyQt implicit dependencies were broken. Fixed in
   0.6.11.1 already.

-  Standalone: The datafile collector plugin was broken. Fixed in
   0.6.11.3 already.

-  Standalone: Added support for newer forms of ``matplotlib`` which
   need a different file layout and config file format. Fixed in
   0.6.11.1 already.

-  Plugins: If there was an error during loading of the module or
   plugin, it could still be attempted for use. Fixed in 0.6.11.1
   already.

-  Disable notes given by gcc, these were treated as errors. Fixed in
   0.6.11.1 already.

-  Windows: Fix, spaces in gcc installation paths were not working.
   Partially fixed in 0.6.11.4 already.

-  Linux: Fix, missing onefile icon error message was not complete.
   Fixed in 0.6.11.4 already.

-  Standalone: Workaround ``zmq`` problem on Windows by duplicating a
   DLL in both expected places. Fixed in 0.6.11.4 already.

-  Standalone: The ``dill-compat`` plugin wasn't working anymore. Fixed
   in 0.6.11.4 already.

-  Windows: Fix mistaken usage of ``sizeof`` for wide character buffers.
   This caused Windows onefile mode in temporary directory. Fixed in
   0.6.11.4 already.

-  Windows: Fix, checking subfolder natured crashed with different
   drives on Windows. Fixed in 0.6.11.4 already.

-  Windows: Fix, usage from MSVC prompt was no longer working, detect
   used SDK properly. Fixed in 0.6.11.4 already.

-  Windows: Fix, old clcache installation uses pth files that prevented
   our inline copy from working, workaround was added.

-  Windows: Also specify stack size to be used when compiling with gcc
   or clang.

-  Fix, claim of Python 3.9 support also in PyPI metadata was missing.
   Fixed in 0.6.11.5 already.

-  Python3.9: Subscripting ``type`` for annotations wasn't yet
   implemented.

-  Python3.9: Better matching of types for metaclass selection, generic
   aliases were not yet working, breaking some forms of type annotations
   in base classes.

-  Windows: Allow selecting ``--msvc-version`` when a MSVC prompt is
   currently activated.

-  Windows: Do not fallback to using gcc when ``--msvc-version`` has
   been specified. Instead it's an error if that fails to work.

-  Python3.6+: Added support for ``del ()`` statements, these have no
   effect, but were crashing Nuitka.

   .. code:: python

      del a  # standard form
      del a, b  # same as del a; del b
      del (a, b)  # braces are allowed
      del ()  # allowed for consistency, but wasn't working.

-  Standalone: Added support for ``glfw`` through a dedicated plugin.

-  macOS: Added support for Python3 from system and CPython official
   download for latest OS version.

**************
 New Features
**************

-  UI: With ``tqdm`` installed alongside Nuitka, experimental progress
   bars are enabled. Do not use `` --show-progress`` or ``--verbose`` as
   these might have to disable it.

-  Plugins: Added APIs for final processing of the result and onefile
   post processing.

-  Onefile: On Windows, the Python process terminates with
   ``KeyboardInterrupt`` when the user sends CTRL-break, CTRL-C,
   shutdown or logoff signals.

-  Onefile: On Windows, in case of the launching process terminating
   unexpectedly, e.g. due to Taskmanager killing it, or a ``os.sigkill``
   resulting in that, the Python process still terminates with
   ``KeyboardInterrupt``.

-  Windows: Now can select icons by index from files with multiple
   icons.

**************
 Optimization
**************

-  Avoid global passes caused by module specific optimization. The
   variable completeness os now traced per module and function scope,
   allowing a sooner usage. Unused temporary variables and closure
   variables are remove immediately. Recognizing possible auto releases
   of parameter variables is also instantly.

   This should bring down current passes from 5-6 global passes to only
   2 global passes in the normal case, reducing frontend compile times
   in some cases massively.

-  Better unary node handling. Dedicated nodes per operation allow for
   more compact memory usage and faster optimization.

-  Detect flow control and value escape for the repr of node based on
   type shape.

-  Enhanced optimization of caught exception references, these never
   raise or have escapes of control flow.

-  Exception matching operations are more accurately annotated, and may
   be recognized to not raise in more cases.

-  Added optimization for the ``issubclass`` built-in.

-  Removed scons caching as used on Windows entirely. We should either
   be using ``clcache`` or ``ccache`` automatically now.

-  Make sure to use ``__slots__`` for all node classes. In some cases,
   mixins were preventing the feature from being it. We now enforce
   their correct specification of slots, which makes sure we can't miss
   it anymore. This should again gain more speed and save memory at
   frontend compile time.

-  Scons: Enhanced gcc version detection with improved caching behavior,
   this avoids querying the same gcc binary twice.

****************
 Organisational
****************

-  The description of Nuitka on PyPI was absent for a while. Added back
   by adding long description of the project derived from the README
   file.

-  Avoid terms ``blacklist``, ``whilelist`` and ``slave`` in the Nuitka
   code preferring ``blocklist``, ``ignorelist`` and ``child`` instead,
   which are actually more clear anyway. We follow a general trend to do
   this.

-  Configured the inline copy of Scons so pylance has an easier time to
   find it.

-  The git commit hook had stopped applying diffs with newest git,
   improved that.

-  Updated description for adding new CPython test suite.

-  Using https URLs for downloading dependency walker, for it to be more
   secure.

-  The commit hook can now be disabled, it's in the Developer Manual how
   to do it.

**********
 Cleanups
**********

-  Moved unary operations to their own module, the operators module was
   getting too crowded.

-  The scons files for Python C backend and Windows onefile got cleaned
   up some more and moved more common code to shared modules.

-  When calling external tools, make sure to provide null input where
   possible.

-  Unified calling ``install_name_tool`` into a single method for adding
   rpath and name changes both at the same time.

-  Unified how tools like ``readelf``, ``ldconfig`` etc. are called and
   error exits and outputs checked to make sure we don't miss anything
   as easily.

*******
 Tests
*******

-  Adapted for some openSUSE specific path usages in standalone tests.

-  Basic tests for onefile operation and with termination signal sent
   were added.

*********
 Summary
*********

The big changes in this release are the optimization changes to reduce
the global passes and the memory savings from other optimization. These
should again make Nuitka more scalable with large projects, but there
definitely is work remaining.

Adding nice stopping behaviour for the Onefile mode on Windows is
seemingly a first, and it wasn't easy, but it will make it more reliable
to users.

Also tooling of gcc and MSVC on Windows got a lot more robust, covering
more cases, and macOS support has been renewed and should be a lot
better now.

The progress bar is a nice touch and improves the overall feel of the
compilation process, but obviously we need to aim at getting faster
overall still. For projects using large dependencies, e.g. Pandas the
compilation is still far too slow and that will need work on caching
frontend results, and better optimization and C code generation for the
backend.
