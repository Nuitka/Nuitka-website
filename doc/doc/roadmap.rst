################
 Nuitka Roadmap
################

This is the Nuitka roadmap, broken down by features.

********************
 User Extensibility
********************

-  Data files, implicit imports, and DLL inclusion are specified in Yaml
   files now.

   In this way, it is easy to extend by third parties. We could imagine
   even supporting packages that provide their own configuration for
   compilation with Nuitka through such files.

   A schema was created and helps editing in Visual Code, user files can
   be provided.

   The next step is to document these file formats.

   Changes are under way and nearly complete now.

************
 Standalone
************

-  "Multidist" support (undecided)

   Allow combining multiple main programs into one, called "multidist".
   These will work with a dispatcher that decides from the binary name
   what it is. There will be one big binary with the ability to run each
   program.

   The CMD file for accelerated mode, demonstrates that it's possible to
   load the CPython Windows DLL from another directory. We can leverage
   that approach and produce CMD files that will call the binary in the
   right fashion.

   I believe we can make it so that all the scripts will still think of
   themselves as ``__main__`` for the ``__name__`` during their
   execution, so no code changes are needed. It's only that
   ``sys.argv[0]`` vs. ``__file__`` for location.

   Much like for onefile, you need to distinguish program location and
   package location in this way. Note shared stuff living near the CMD
   file will see that CMD file path in ``sys.argv[0]`` there, and shared
   stuff, e.g. ``xmlschema`` module will find its data files in a
   directory that is shared.

   And to top it off, the fat binary of "multidist" may be in standalone
   or onefile mode, at your choice. The disadvantage there being, that
   onefile will be slower to unpack with a larger binary.

-  "Sharedist" support (undecided)

   In this the programs are not combined, rather separate standalone
   compilations are combined, produced shared and non-shared parts of
   multiple distributions.

   The plugins in Nuitka are cleaned up entirely, when comes to copying
   DLLs and data files now.

-  Dejong Stacks: More robust parser that allows stdout and stderr in
   same file with mixed outputs.

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

-  Add support for ``list`` methods, things like ``append`` really
   should be optimized as well in the mostly existing operation nodes.

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

-  Duplicate DLLs are a unresolved issue. We need to identify, is DLLs
   in different paths should be considered colliding at all.

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

-  Add support for all of the new case syntax of 3.10

   Right now it is not clear what is missing, need to investigate it by
   attempting to manage the full test suite.

***********************************
 Traceback Encryption (commercial)
***********************************

-  Right now tracebacks are entirely encrypted. But in a future update,
   you can decide which information is transferred, and what information
   is part of the encryption, and which part is not, e.g. hostname,
   client name, etc. could be output in plain text, while the variable
   names and values would not be, depending on your choice!

******************************
 Features to be added for 1.1
******************************

[x] Get complex flask standalone examples to work.

[ ] Add download updating for onefile on at least Windows.

[ ] Document commercial file embedding publicly with examples.

[ ] Document commercial Windows Service usage with examples.

[x] Add support for executables in the onefile binary. Right now outside of
   Windows, the x-bit is lost.

******************************
 Features to be added for 1.2
******************************

[ ] Update for MinGW64 on Windows to use gcc 12.x based on.

[ ] Initial support for ctypes based direct calls of C code.

[ ] Add support for ``list`` methods, things like ``append`` really
   should be optimized as well in the mostly existing operation nodes.

[ ] Tuple unpacking for values that support indexing should be
   optimized.

[ ] Document Yaml format with a series of postings with examples.
