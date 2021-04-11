This is the Nuitka roadmap, broken down by features.

#########
 Onefile
#########

-  Add support for macOS (public feature)

   The initial goal here is to make the temp directory mode work on
   Linux too, that is going to be largely what it takes. The ``%TEMP%``
   etc notations might be a bit of research to find out the proper
   values.

-  Add zstd compression (public feature)

   The file reading is already somewhat abstracted. After adding support
   for Linux with the bootstrap code (Linux works without it, and in a
   better way), it should be more easy for me to develop this, as
   Windows is kind of a hostile environment for me in terms of the
   debugging.

-  Add support for upx (public feature)

   The UPX cannot compress payloads, which is why we can't use it.
   However, a post processing of binaries, even from CPython extension
   modules, seems to work and reduce the uncompressed sizes of binaries
   already.

############
 Standalone
############

-  The main binary will be separated from the dist folder. (undecided)

   Allowing a common place for the binary to load from, with some sort
   of repository to load from.

-  Windows: Attempt to avoid need to copy the DLL by using a ".cmd" file
   that sets the PATH to make it find the CPython DLL, which otherwise
   would have to be exempted. Also a minor bootstrap approach could be
   considered, where we to what this does in an executable to the launch
   an attached binary with that configuration.

-  Include data files directly in the standalone binary (commercial)

   Making them accessible via standard API such as ``pkgutil.get_data``
   and having them covered by data hiding.

-  Include Qt data files directly in the standalone binary (commercial)

   These cannot be done from constant values, but there is a Qt
   mechanism that is fed from constant values that we can use.

######################
 Performance (public)
######################

-  Caching of demoted to bytecode modules. Some of these, e.g.
   ``pkg_resources`` take very long to analyse in Nuitka, just to find
   out the imports. There is no point in repeating this, a caching of
   Python compilation is a separate line of action, but it should start
   with this.

-  Better Python3 threading on 3.8 or higher.

   There is now a better way to yield the GIL than whatN Nuitka does.
   Older Python3 versions allowed no interactions, but newer ones do.

-  Better code for ``+= 1`` constructs with lack of type knowledge.

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

#################################
 Features to be added for 0.6.14
#################################

[x] Apply lessons learn from in-place operations to binary operations

   -  Move generic algorithm for fallback into separate function force
      to not inline as they otherwise slow down.

   -  Instead of calling specialized function when checking type to be
      the same, directly call the binary_operation template and generate
      code forced inline.

[x] Fix importing issue, where a module after having raises can never be
   loaded again.

[x] Improve data hiding to cover module names.

[x] Add file inclusion for data files and Qt files.

#################################
 Features to be added for 0.6.15
#################################

[ ] Attempt to avoid need to copy the DLL by using a .cmd file that sets
   the PATH to make it find the CPython DLL.

[ ] Compression of onefile for Windows

[ ] Add onefile for macOS

[ ] Better Python3 threading on 3.8 or higher.

#################################
 Features to be added for 0.6.16
#################################

   [ ] Better scalability
