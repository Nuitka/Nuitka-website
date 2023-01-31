################
 Nuitka Roadmap
################

This is the Nuitka roadmap, broken down by features.

********************
 User Extensibility
********************

-  Data files, implicit imports, and DLL inclusion are specified in Yaml
   files now.

   A post series is currently going on and has been lauched at post: [Nuitka
   Package Config
   Kickoff](https://nuitka.net/posts/nuitka-package-config-kickoff.html) and it
   will continue to become the documentation that currently lives under [Nuitka
   Package Config](https://nuitka.net/doc/nuitka-package-config.html) on the web
   site only for rapid development independent of Nuitka releases.

   The long term plan is to also include in the Nuitka release as part of
   the documentation, much like User Manual and Developer Manual, that are
   being maintained inside Nuitka repo.

************
 Standalone
************

-  "Multidist" support (public)

   .. note::

      This is an experimental feature and available in the 1.4 release
      series, checkout the User Manual to see how it is used. This is
      only here until the things described are also perfectly documented
      there.

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
 Onefile speed (public)
************************

-  Use memory mapped files on Windows and Linux for performance in
   accessing the payload.

-  Generally use memory mapping for calculating the checksum of a file.
   This is for all OSes, and should make cached mode faster to use.

-  Use Windows NTFS and macOS HFS extended attributes to store caching
   status of a file inside of it. It might be possible to detect
   modification of the file in this way and spare us the checksum, which
   will then be used only in case of a fallback being necessary.

-  Restructure the payload data stream in cached mode, such that
   skipping a file content becomes easier and does not require
   decryption of the whole data.

-  One files are compressed individually, we might be able to cache the
   result of a specific file, such that files from the Python
   installation do not have to be redone over and over.

************
 Python 3.11
************

-  Basic tests appear to work mostly, but frame handling has still bugs that
   need to be resolved. The changes done for generator frames appear to not yet
   fully compatible with 3.10 therefore this is still blocked from release.

-  There is a lack of integration of compiled and uncompiled generators
   with each other, this needs porting still.

-  Execute Python 3.10 test suite in a compatible way with 3.11

-  And and execute Python 3.11 test suite in a compatible way with 3.11

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
 Features to be added for 1.5
******************************

[ ] Add download updating for standalone as well, onefile for windows works.

[ ] Document commercial file embedding publicly with examples.

[ ] Document commercial Windows Service usage with examples.

[ ] Tuple unpacking for values that support indexing should be
   optimized.

******************************
 Features to be added for 1.6
******************************

[ ] Update for MinGW64 on Windows to use gcc 12.x based on.

[ ] Initial support for ctypes based direct calls of C code.
