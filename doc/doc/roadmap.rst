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

   The next step is to document these file formats, potentially define a
   schema for them and check it. We might have to change the format to
   make this possible.

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

   In this the programs are not combined, rather standalone compilations
   are resumed, produced shared and non-shared parts of multiple
   distributions.

   The plugins in Nuitka are still somewhat wild west when it comes to
   copying DLLs and data files as they see fit, sometimes, but not
   always, reporting to the core, so it could scan dependencies. Work is
   being done to clean them up. Some, most recently numpy, have been
   changed to make them yield objects describing tasks and executing
   them in the core. This way there is a chance to know what the program
   does and make this kind of change. This transition is almost
   complete, but the Qt plugins are still missing.

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
   static libpython it can linked though, but we still might want to
   make our own replacement.

-  Better code for ``+= 1`` constructs with no lack of type knowledge.
   There is a long standing todo, to add the ``CLONG`` support for
   binary operations. It requires the code generation of Jinja to be
   abstract, but that should have been close to being reached in last
   releases.

-  Better code for ``+= 1`` constructs even with lack of type knowledge.

   It should be possible to introduce prepared constants of
   ``nuitka_int`` type that have the object ready for use, as well as
   the integer value, and indicate so with the enum setting. This type,
   that is intended for use with local variables later on, could also be
   supported in binary operations and in-place operations, esp. for
   ``int``, ``float`` and ``long`` values.

-  Make module variable traces available to functions. This will be
   needed to optimize import of ``sys`` on module level and then
   attribute access on function level at compile time.

-  Implement the ``partial`` built-in and make it work with compiled
   functions. It could prepare calls much better, such that they do not
   come through keyword arguments unnecessarily.

-  Add support for ``list`` methods, things like ``append`` really
   should be optimized as well in the mostly existing operation nodes.

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

[ ] Detect caching ability for a spec, and add a onefile mode modifier
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
 Features to be added for 0.8
******************************

[x] Add ability to inhibit data files from the command line, so that
   things coming from a plugin can be suppressed.

[x] Forcing output and stderr to files should be supported for all OSes.

******************************
 Features to be added for 0.9
******************************

[ ] Onefile should support keeping cached binaries and then not requires
   to overwrite. Then we can drop ``AppImage`` usage on Linux.
