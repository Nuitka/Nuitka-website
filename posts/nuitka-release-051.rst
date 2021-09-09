This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release brings corrections and major improvements to how standalone
mode performs. Much of it was contributed via patches and bug reports.

***********
 Bug Fixes
***********

-  There was a crash when using ``next`` on a non-iterable. Fixed in
   0.5.0.1 already.

-  Module names with special characters not allowed in C identifiers
   were not fully supported. `Issue#118
   <http://bugs.nuitka.net/issue118>`__. Fixed in 0.5.0.1 already.

-  Name mangling for classes with leading underscores was not removing
   them from resulting attribute names. This broke at ``__slots__`` with
   private attributes for such classes. `Issue#119
   <http://bugs.nuitka.net/issue119>`__. Fixed in 0.5.0.1 already.

-  Standalone on Windows might need "cp430" encoding. `Issue#120
   <http://bugs.nuitka.net/issue120>`__. Fixed in 0.5.0.2 already.

-  Standalone mode didn't work with ``lxml.etree`` due to lack of hard
   coded dependencies. When a shared library imports things, Nuitka
   cannot detect it easily.

-  Wasn't working on macOS 64 bits due to using Linux 64 bits specific
   code. `Issue#123 <http://bugs.nuitka.net/issue123>`__. Fixed in
   0.5.0.2 already.

-  On MinGW the constants blob was not properly linked on some
   installations, this is now done differently (see below).

**************
 New Features
**************

-  Memory usages are now traced with ``--show-progress`` allowing us to
   trace where things go wrong.

******************
 New Optimization
******************

-  Standalone mode now includes standard library as bytecode by default.
   This is workaround scalability issues with many constants from many
   modules. Future releases are going to undo it.

-  On Windows the constants blob is now stored as a resource, avoiding
   compilation via C code for MSVC as well. MinGW was changed to use the
   same code.

***********
 New Tests
***********

-  Expanded test coverage for "standalone mode" demonstrating usage of
   "hex" encoding, PySide, and PyGtk packages.

*********
 Summary
*********

This release is mostly an interim maintenance release for standalone.
Major changes that provide optimization beyond that, termed "C-ish code
generation" are delayed for future releases.

This release makes standalone practical which is an important point.
Instead of hour long compilation, even for small programs, we are down
to less than a minute.

The solution of the scalability issues with many constants from many
modules will be top priority going forward. Since they are about how
even single use constants are created all in one place, this will be
easy, but as large changes are happening in "C-ish code generation", we
are waiting for these to complete.
