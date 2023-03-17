################
 Nuitka Roadmap
################

This is the Nuitka roadmap, broken down by features.

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

************************
 Onefile speed (public)
************************

-  Use Windows NTFS and macOS HFS extended attributes to store caching
   status of a file inside of it. It might be possible to detect
   modification of the file in this way and spare us the checksum, which
   will then be used only in case of a fallback being necessary.

-  Restructure the payload data stream in cached mode, such that
   skipping a file content becomes easier and does not require
   decryption of the whole data.

-  All files are compressed individually, we might then be able to cache
   the result of a specific file, such that files from the Python
   installation do not have to be redone over and over.

-  Directly pass the memory mapped data to decompression to spare the
   use of ``memcpy``.

-  Write payload files as memory mapped too, that too should be faster.

*************
 Python 3.11
*************

-  Basic tests appear all work now.

-  Execute Python 3.10 test suite in a compatible way with 3.11, so far
   we got almost through, with only very few, and probably unimportant
   errors.

-  There is a lack of integration of compiled and uncompiled generators
   with each other, this needs porting still.

-  Attribute lookups for types with a generic one need to update that
   code path, they will be much slower in 3.11 until we do that. That
   breaks the performance. Probably not happening before 1.6 though as
   we want to cleanup the code, potentially sharing improvements by
   generating code variants rather that duplicating stuff.

-  And and execute Python 3.11 test suite in a compatible way with 3.11

-  MSVC in debug mode hates the Python headers, probably because they
   can not longer be used outside of C11 mode, and C++0x is not
   compatible enough for it. We might have to require newer MSVC and
   implement C11 mode for the new enough Windows SDK that allows it.

************************
 Nuitka-Python (public)
************************

This is currently under way and not yet described here. The current
Nuitka release has support for using it. Most work is focused on Linux
with Python 2.7 as well as Windows with Python 3.9 now with the aim of
getting it capable to statically compile, avoiding extension modules and
DLL usages.

**********************
 Performance (public)
**********************

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

-  Loop trace analysis fails to deliver ``int`` types shapes. We would
   need that for optimizing loops.

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

*******************************
 Container Builds (commercial)
*******************************

Providing containers with old Linux, and optimally compiled CPython with
``podman`` such that building with Nuitka on Fedora latest and Ubuntu
latest can be done fully automatically and still run on very old Linux.

*******************
 Automatic Updates
*******************

The running application needs to check for updates, and update itself
automatically, optionally after user prompt, on a restart, or after
successful update.

These are the steps needed to take.

[x] Add path spec identifiers that are suitable for caching, like
``%CACHE_DIR%``

[x] Detect caching ability for a spec, and add a onefile mode modifier
that will make it overwrite. Ideally volatile path elements are
detected.

[ ] Add download URL spec.

[ ] Actually download the file in a thread of the onefile bootstrap
binary and move it over the running binary, e.g. during restart.

********************************************
 Complete Support for Python Version (3.10)
********************************************

-  Add support for remaining ``match`` case syntax of 3.10

   When mixing keyword and positional arguments in catching a type,
   Nuitka asserts this. It is the last remaining cases missing to
   execute ``test_patma.py`` completely.

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

******************************
 Features to be added for 1.6
******************************

[ ] Full support of Python 3.11 version.

[ ] Update for MinGW64 on Windows to use gcc 12.x based on.

[ ] Add download updating for standalone as well, onefile for windows
works.

[ ] Document commercial file embedding publicly with examples.

[ ] Document commercial Windows Service usage with examples.

******************************
 Features to be added for 1.7
******************************

[ ] Initial support for ctypes based direct calls of C code.

[ ] Tuple unpacking for values that support indexing should be
   optimized.
