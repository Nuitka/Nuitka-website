:orphan:

################
 Nuitka Roadmap
################

.. include:: ../changelog/changes-hub.inc

This is the Nuitka roadmap, broken down by features.

.. contents:: Table of Contents
   :depth: 2
   :local:
   :class: page-toc

********************
 User Extensibility
********************

-  Data files, implicit imports, and DLL inclusion are specified in Yaml
   files now.

   A post series is currently going on and has been launched at post:
   `Nuitka Package Config Kickoff
   </posts/nuitka-package-config-kickoff.html>`__ and it will continue
   to improve the documentation that currently lives under `Nuitka
   Package Config </doc/nuitka-package-config.html>`__ on the web site
   only for rapid development independent of Nuitka releases.

   The long term plan is to also include in the Nuitka release as part
   of the documentation, much like User Manual and Developer Manual,
   that are being maintained inside Nuitka repo.

   The standard Yaml files (if modified) should be checked at runtime of
   Nuitka, for that we need to add some kind of checksum to it to detect
   modification and issue a warning, if ``jsonschema`` is not available
   for modification. Vendoring it seems unnecessarily much effort, and
   it's in ``requirements-devel.txt`` anyway.

   Currently the checksums are added in the commit hook, but they are
   not checked at runtime. We might want to limit checking to only used
   configuration entries.

**************************
 Onefile speed (standard)
**************************

-  Use Windows NTFS and macOS HFS extended attributes to store caching
   status of a file inside of it. It might be possible to detect
   modification of the file in this way and spare us the checksum, which
   will then be used only in case of a fallback being necessary.

   Example code for Windows can be found here:
   https://github.com/microsoft/Windows-classic-samples/blob/main/Samples/Win7Samples/winui/shell/appplatform/PropertyEdit/PropertyEdit.cpp

-  All files are compressed individually, we might then be able to cache
   the result of a specific file, such that files from the Python
   installation do not have to be redone over and over.

-  Write payload files as memory mapped too, that too should be faster.

*************
 Python 3.11
*************

-  Attribute lookups for types with a generic one need to update that
   code path, they will be much slower in 3.11 until we do that. That
   breaks the performance. We want to cleanup the code, potentially
   sharing improvements by generating code variants rather that
   duplicating stuff.

*************
 Python 3.12
*************

-  Use special code for 2 digits code in the long operation templates.
   Currently only single digit is optimized, but with Python 3.12, we
   can do better now.

-  Add support for generic classes, these are not yet implemented which is not
   acceptable mid-term.

*************
 Python 3.13
*************

-  The No-GIL variant of Python 3.13 is not currently working with
   Nuitka and needs more work. Right now it seems we cannot import
   ``inspect`` without crashing, we need to audit data structures for
   more issues like one we found with list data allocations.

**************************
 Nuitka-Python (standard)
**************************

This is currently under way and not yet described here. The current
Nuitka release has support for using it. Most work is focused on the aim
of getting it capable to statically compile, avoiding extension modules
and DLL usages.

************************
 Scalability (standard)
************************

-  More compact code objects handling

   Code objects and their creation is among the oldest code in Nuitka
   and lacks 2 features. First, their creation cannot be delayed, so
   they consume memory even if never used and module load time as well.

   We have since began to create constants from binary blobs. These too
   are also always created before use, but in some cases, we want to
   become able to delay this step.

   .. note::

      As of Nuitka 2.6, there is an experimental flag to enable these,
      and we need to switch over to using it.

-  Enhanced tracing of loop exit merges

   Tracing of exception exits is not done for function exits and module
   exits at this time, meaning that the most merge intensive form of
   tracing is not applied. However, with a for loop, and a bunch of code
   on the inside, even if the actual exception exit doesn't matter much
   more than if it happens at all, or for only very few variables
   (iterated, iterated value, etc.) causes a full blown tracing to be
   done. Experiments have shown, that this for some modules causing a
   40% increase of work to do, and providing the most complex merges to
   be done, which end up being used.

-  More scalable class creation

   For class creation, we have a bunch of complexity. We cannot decide
   easily if a class dictionary (while being in the class scope) is a
   normal dict, or at least well behaving like it, or if it's some sort
   of magic thing that changes all your assignments to something else,
   and won't allow reading them back, etc. as all of that happens
   potentially.

   This means that methods in classes, have a harder time to know
   anything for sure during their creation and assignment as well.

   This leads to massively more complex Python code internally
   re-formulating the class creation with all things that could happen
   by virtue of not knowing the base classes as exact as one would have
   to.

   The runtime impact is not so big, but a lot of merges and temporary
   variables are created and to be handled during optimization with no
   chance of getting rid of them really, although some helper functions
   used there could be inlined even today and give results that we can
   investigate, but that's never going to be completely workable.

   So, what we want to do here, is to check at runtime the actual value
   a class dictionary becomes, and as such generate simpler assign and
   access nodes that will not raise exceptions as much, even if we don't
   have dictionary tracing at this time, what we do is to change
   dictionaries over the local variables if the used of it is sane
   enough, i.e. no ``locals()`` and other strange things used.

************************
 Performance (standard)
************************

-  Dual types

   After recent improvements, loop analysis became strong enough to
   trace the types of loop variables, when integer operations are used
   to increment them, but not if they come out of iterators. That should
   be added.

   For range and enumerate, we should have code generation capable of
   producing dual types as well and the dual type generation should be
   made generally usable for all code creation, which is not too far
   away.

-  Function inlining.

   There is dead code in Nuitka capable of inlining functions, but it is
   not used. It should be used on the complex call helpers when
   arguments are constant, maybe even with hints towards loop unrolling,
   where there are loops e.g. over dictionaries. And generally for
   functions that have code that is not too complex, say ``return a+b``.
   For this, we could have a generated tree visitor, that checks if the
   cost exceeds a specific value.

   Overall this would remove some code in local functions, and then it
   would also make class creations of at least Python3 more compact and
   compile time optimizable, due to e.g. knowing the meta class and
   therefore class dictionary type more often.

-  Static metaclass and class dictionaries for Python3

   Changes in 1.5 allow this for the case of no base class being
   specified. But if even only ``object`` is given a base class, then it
   changes to not being compile time resolved, leading to not having an
   idea what the ``__prepare__`` call is going to give for the class
   dictionary, it could be something very strange, so all the things
   become and remain untrusted.

   The way forward, is to inline the helpers that select the metaclass
   in Python3, and the 3.7+ iteration over all bases to build a new set
   of bases, through potential ``__mro_entries__`` calls.

   For these helpers, inlining can of course be done with compile time
   knowledge of these bases, e.g. ``(object,)``, and we could write
   Python code, that will attempt to resolve this where possible. The
   other solution, is to inline the code when we know it will go away
   through compile time optimization automatically.

   Right now, these re-formulation have loops that using an iterator,
   and then take out of it. This ties is with incomplete optimization
   for known indexable types. In case of a tuple, as we have here (but
   of course also list, etc.) the iteration can be replaced with
   indexing operations, and the indexing can then be done from that
   loop.

   After a replacement, the loop will be driven by increases to that
   index variable for the ``base = next(bases_iter)`` operation having
   become ``base = bases[base_index]; base_index += 1``. The loop break
   will be that the end of the tuple is reached, which is then a
   comparison to the length of the tuple.

   This optimization is a separate point and has been implemented on
   streams before. I am getting ready to make new ones these weeks. Only
   the releases are not yet replaced, i.e. it is working correctly, but
   it was leaking references. That will be solvable. Once that finished,
   there will be an a desire of course to specialize type and list index
   lookups for generated code, but for this part of the plan, that is
   not relevant, because for that we aim at full compile time resolution
   of the help code to the metaclass and the list of actual bases (most
   bases classes have no ``__mro_entries__`` only data classes might
   pose work there).

   But based on doing this first, the remaining issue is that loop
   unrolling must be solved. For these helpers, we can force it. Since
   the index integer is done with what will be very predictable things,
   we will have during loop unrolling, a chance to know the iteration
   count, since we know the length of the tuple, and not only the shape.

   The function inlining of these helpers will be maybe instrumented to
   do the loop unrolling instantly.

   Once we know the meta class, we can actually consider the effect it
   it on the class, and try to optimize the call to it with the
   ``meta_class(name, bases, **kw_from_declarations)`` just type.
   Specifically ``type`` but maybe even ``enum`` and things will be
   something to handle pretty nicely, to the point that we have a
   perfect understanding of the resulting class.

   The gains from this will be mostly related to startup time. Class
   creation code runs there a lot. Avoiding interactions with dictionary
   through mapping methods can only be faster as well, and it will be a
   lot of code. Already in 1.5 a lot of code is avoided before this even
   happens generally.

-  Compiled classes / objects

   We might dare and replace the implementation of some metaclass like
   ``type`` with improved variants, esp. where ``__slots__`` are used,
   then we may just be faster to resolve these and interact with
   compiled code and methods. It would e.g. no longer be a compiled
   ``__init__`` being called, but potentially things like assigning
   arguments to the slot values, will be implicitly done.

   This is somewhat in the dark at this point, what can be done. First
   step of

-  Faster attribute setting.

   For Python3 we still use ``_PyObjectDict_SetItem`` which is very hard
   to replace, as it's forking shared dictionary as necessary. With
   static libpython it can be linked though, but we still might want to
   make our own replacement.

-  Better code for ``+= 1`` constructs with no lack of type knowledge.

   We have this for ``INT``, ``LONG``, and ``FLOAT`` now. Actually for
   all in-place operations, except for ``LONG`` we only cover ``+=`` and
   ``-=``.

-  Better code for ``+= 1`` constructs even with lack of type knowledge.

   It should be possible to introduce prepared constants of
   ``nuitka_int`` type that have the object ready for use, as well as
   the integer value, and indicate so with the enum setting. This type,
   that is intended for use with local variables later on, could also be
   supported in binary operations and in-place operations, esp. for
   ``int``, ``float`` and ``long`` values.

-  Implement the ``partial`` built-in and make it work with compiled
   functions. It could prepare calls much better, such that they do not
   come through keyword arguments unnecessarily.

-  Cover all built-ins of Python

   Currently a few built-ins, even as important as ``enumerate`` are not
   yet implemented. We need to revisit this once we got integer type
   specialization and loop iteration specialization both.

********************
 macOS enhancements
********************

-  While ``arm64`` (M1) only builds and ``x86_64`` (Intel) only builds
   work, the value ``universal`` which of course implies twice the size,
   and as such has other disadvantages, is not yet supported.

   It will require two distinct compilations, and on the Python level,
   some values, e.g. architecture, cannot be compile time decided on
   macOS, which currently is even a potential weakness of the current
   code.

   So far we use macOS tools to split binaries that are universal, and
   in this case we need to merge binaries into one with the same tools.

****************************************
 Container Builds (public + commercial)
****************************************

Providing containers with old Linux, and optimally compiled CPython with
``podman`` such that building with Nuitka on Fedora latest and Ubuntu
latest can be done fully automatically and still run on very old Linux.

The ``run-inside-nuitka-container`` kind of duplicates the effort, so we
can provide more container files in the future, some of which can e.g.
be geared towards making e.g. Nuitka-Python easy to use with Nuitka, and
Nuitka optimized CPython that is portable for Linux easier to access.

*******************
 Automatic Updates
*******************

The running application needs to check for updates, and update itself
automatically, optionally after user prompt, on a restart, or after
successful update.

This has been implemented for onefile mode only. Unfortunately that is
not good for macOS which often require app mode, i.e. standalone mode
effectively with more than a single file.

***********************************
 Traceback Encryption (commercial)
***********************************

-  Right now tracebacks are entirely encrypted. But in a future update,
   you can decide which information is transferred, and what information
   is part of the encryption, and which part is not, e.g. hostname,
   client name, etc. could be output in plain text, while the variable
   names and values would not be, depending on your choice!

-  Dejong Stacks: More robust parser that allows stdout and stderr in
   same file with mixed outputs.

*************************************
 Regression Testing User Compilation
*************************************

-  Creating more content in `Nuitka-Watch
   <https://github.com/Nuitka/Nuitka-Watch>`_ and fine tuning the tools
   to detect changes in the compilation due to upstream changes, as well
   as changes due to newer Nuitka separately.

-  We should teach our users to have this in place for doing it with
   their own code base, allowing them to see changes due to new Nuitka
   or new PyPI packages individually.

**************************
 Plugin API documentation
**************************

-  The API for plugins should be documented in Sphinx and be accessible
   on the website.

**********
 Coverage
**********

-  The test runner is prepared to take coverage of Nuitka during
   execution, and we have as job for it, but we don't yet render the
   results anywhere.

*************************************
 Features to be added for Nuitka 2.7
*************************************

[x] Activate more scalable code objects handling

[ ] Enhanced tracing of loop exit merges

[ ] More scalable class creation

*************************************
 Features to be added for Nuitka 2.8
*************************************

[ ] Use performance potential for attribute access with Python 3.11
version.

[ ] Document commercial file embedding publicly with examples.

[ ] Document commercial Windows Service usage with examples.

[ ] Document traceback encryption usage with examples.

*************************************
 Features to be added for Nuitka 3.0
*************************************

[ ] Initial support for ctypes based direct calls of C code.

[ ] Tuple unpacking for values that support indexing should be
   optimized.

[ ] Add download updating for standalone as well, onefile for windows
works.
