This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is mostly about catching up with issues. Most address standalone
problems with special modules, but there are also some general compatibility
corrections, as well as important fixes for Python3.5 and coroutines and to
improve compatibility with special Python variants like Anaconda under the
Windows system.

Bug Fixes
---------

- Standalone Python3.5: The ``_decimal`` module at least is using a
  ``__name__`` that doesn't match the name at load time, causing programs that
  use it to crash.

- Compatibility: For Python3.3 the ``__loader__`` attribute is now set in all
  cases, and it needs to have a ``__module__`` attribute. This makes inspection
  as done by e.g. ``flask`` working.

- Standalone: Added missing hidden dependencies for ``Tkinter`` module, adding
  support for this to work properly.

- Windows: Detecting the Python DLL and EXE used at compile time and preserving
  this information use during backend compilation. This should make sure we use
  the proper ones, and avoids hacks for specific Python variants, enhancing the
  support for Anaconda, WinPython, and CPython installations.

- Windows: The ``--python-debug`` flag now properly detects if the run time
  is supporting things and error exits if it's not available. For a CPython3.5
  installation, it will switch between debug and non-debug Python binaries and
  DLLs.

- Standalone: Added plug-in for the ``Pwm`` package to properly combine it into
  a single file, suitable for distribution.

- Standalone: Packages from standard library, e.g. ``xml`` now have proper
  ``__path__`` as a list and not as a string value, which breaks code of e.g.
  PyXML. `Issue#183 <http://bugs.nuitka.net/issue183>`__.

- Standalone: Added missing dependency of ``twisted.protocols.tls``. `Issue#288
  <http://bugs.nuitka.net/issue288>`__.

- Python3.5: When finalizing coroutines that were not finished, a corruption of
  its reference count could happen under some circumstances.

- Standalone: Added missing DLL dependency of the ``uuid`` module at run time,
  which uses ctypes to load it.

New Features
------------

- Added support for Anaconda Python on this Linux. Both accelerated and
  standalone mode work now. `Issue#295 <http://bugs.nuitka.net/issue295>`__.

- Added support for standalone mode on FreeBSD. `Issue#294
  <http://bugs.nuitka.net/issue294>`__.

- The plug-in framework was expanded with new features to allow addressing some
  specific issues.

Cleanups
--------

- Moved memory related stuff to dedicated utils package
  ``nuitka.utils.MemoryUsage`` as part of an effort to have more topical
  modules.

- Plug-ins how have a dedicated module through which the core accesses the API,
  which was partially cleaned up.

- No more "early" and "late" import detections for standalone mode. We now scan
  everything at the start.

Summary
-------

This release focused on expanding plugins. These were then used to enhance the
success of standalone compatibility. Eventually this should lead to a finished
and documented plug-in API, which will open up the Nuitka core to easier hacks
and more user contribution for these topics.
