This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This is a maintenance release, largely intended to put out improved
support for new platforms and minor corrections. It should improve the
speed for standalone mode, and compilation in general for some use
cases, but this is mostly to clean up open ends.

Bug Fixes
=========

-  Fix, the ``len`` built-in could give false values for dictionary and
   set creations with the same element.

   .. code:: python

      # This was falsely optimized to 2 even if "a is b and a == b" was true.
      len({a, b})

-  Python: Fix, the ``gi_running`` attribute of generators is no longer
   an ``int``, but ``bool`` instead.

-  Python3: Fix, the ``int`` built-in with two arguments, value and
   base, raised ``UnicodeDecodeError`` instead of ``ValueError`` for
   illegal bytes given as value.

-  Python3: Using ``tokenize.open`` to read source code, instead of
   reading manually and decoding from ``tokenize.detect_encoding``, this
   handles corner cases more compatible.

-  Fix, the PyLint warnings plug-in could crash in some cases, make sure
   it's more robust.

-  Windows: Fix, the combination of Anaconda Python, MinGW 64 bits and
   mere acceleration was not working. `Issue#254
   <http://bugs.nuitka.net/issue254>`__.

-  Standalone: Preserve not only namespace packages created by ``.pth``
   files, but also make the imports done by them. This makes it more
   compatible with uses of it in Fedora 22.

-  Standalone: The extension modules could be duplicated, turned this
   into an error and cache finding them during compile time and during
   early import resolution to avoid duplication.

-  Standalone: Handle "not found" from ``ldd`` output, on some systems
   not all the libraries wanted are accessible for every library.

-  Python3.5: Fixed support for namespace packages, these were not yet
   working for that version yet.

-  Python3.5: Fixes lack of support for unpacking in normal ``tuple``,
   ``list``, and ``set`` creations.

   .. code:: python

      [*a]  # this has become legal in 3.5 and now works too.

   Now also gives compatible ``SyntaxError`` for earlier versions.
   Python2 was good already.

-  Python3.5: Fix, need to reduce compiled functions to ``__qualname__``
   value, rather than just ``__name__`` or else pickling methods doesn't
   work.

-  Python3.5: Fix, added ``gi_yieldfrom`` attribute to generator
   objects.

-  Windows: Fixed harmless warnings for Visual Studio 2015 in
   ``--debug`` mode.

Optimization
============

-  Re-formulate ``exec`` and ``eval`` to default to ``globals()`` as the
   default for the locals dictionary in modules.

-  The ``try`` node was making a description of nodes moved to the
   outside when shrinking its scope, which was using a lot of time, just
   to not be output, now these can be postponed.

-  Refactored how freezing of bytecode works. Uncompiled modules are now
   explicit nodes too, and in the registry. We only have one or the
   other of it, avoiding to compile both.

Tests
=====

-  When ``strace`` or ``dtruss`` are not found, given proper error
   message, so people know what to do.

-  The doc tests extracted and then generated for CPython3 test suites
   were not printing the expressions of the doc test, leading to largely
   decreased test coverage here.

-  The CPython 3.4 test suite is now also using common runner code, and
   avoids ignoring all Nuitka warnings, instead more white listing was
   added.

-  Started to run CPython 3.5 test suite almost completely, but
   coroutines are blocking some parts of that, so these tests that use
   this feature are currently skipped.

-  Removed more CPython tests that access the network and are generally
   useless to testing Nuitka.

-  When comparing outputs, normalize typical temporary file names used
   on posix systems.

-  Coverage tests have made some progress, and some changes were made
   due to its results.

-  Added test to cover too complex code module of ``idna`` module.

-  Added Python3.5 only test for unpacking variants.

Cleanups
========

-  Prepare plug-in interface to allow suppression of import warnings to
   access the node doing it, making the import node is accessible.

-  Have dedicated class function body object, which is a specialization
   of the function body node base class. This allowed removing class
   specific code from that class.

-  The use of "win_target" as a scons parameter was useless. Make more
   consistent use of it as a flag indicator in the scons file.

-  Compiled types were mixing uses of ``compiled_`` prefixes, something
   with a space, sometimes with an underscore.

Organisational
==============

-  Improved support for Python3.5 missing compatibility with new
   language features.

-  Updated the Developer Manual with changes that SSA is now a fact.

-  Added Python3.5 Windows MSI downloads.

-  Added repository for Ubuntu Wily (15.10) for download. Removed Ubuntu
   Utopic package download, no longer supported by Ubuntu.

-  Added repository with RPM packages for Fedora 22.

Summary
=======

So this release is mostly to lower the technical debt incurred that
holds it back from supporting making more interesting changes. Upcoming
releases may have continue that trend for some time.

This release is mostly about catching up with Python3.5, to make sure we
did not miss anything important. The new function body variants will
make it easier to implement coroutines, and help with optimization and
compatibility problems that remain for Python3 classes.

Ultimately it will be nice to require a lot less checks for when
function in-line is going to be acceptable. Also code generation will
need a continued push to use the new structure in preparation for making
type specific code generation a reality.
