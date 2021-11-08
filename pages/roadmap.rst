This is the Nuitka roadmap, broken down by features.

####################
 User Extensibility
####################

-  Data files, implicit imports, even DLL inclusion, and plugins
   location should be specified in yaml format.

   In this way, it becomes easier to extend by third parties. We could
   imagine even supporting packages that provide their own configuration
   for compilation with Nuitka through such files.

   This is started with yaml config of the ``anti-bloat`` plugin, and
   will probably grow from there. The implicit imports is a natural next
   target to include there, as is the ``data-files`` plugin.

############
 Standalone
############

-  "Multidist" support (undecided)

   Allow combinining multiple main programs into one, called
   "multidist". These will work with a dispatcher that decides from the
   binary name what it is. There will be one big binary with the ability
   to run each program.

   The CMD file for accelerated mode, demonstrates that it's possible to
   load the CPython DLL from another directory. We can leverage that
   approach and produce CMD files that will call the binary in the right
   fashion.

   I believe we can make it so that all the scripts will still think of
   themselves as ``__main__`` for the ``__name__`` during their
   execution, so no code changes are needed. It's only that
   ``sys.argv[0]`` vs. ``__file__`` for location.

   Much like for onefile, you need to distinguish program location and
   package location in this way. Note shared stuff living near the CMD
   file will see that CMD file path in ``sys.argv[0]`` there, and shared
   stuff, e.g. ``xmlschema`` module will find its datafiles directory
   that is shared.

   And to top it off, the fat binary of "multidist" may be in standalone
   or onefile mode, at your choice. The disadvantage there being, that
   onefile will be slower to unpack with a larger binary.

-  "Sharedist" support (undecided)

   In this the programs are not combined, rather standalone compilations
   are resumed, produced shared and non-shared parts of multiple
   distributions.

   The plugins in Nuitka are still somewhat wild west when it comes to
   copying DLLs and data files as they see fit, sometimes, but not
   always, reporting to the core, so it could scan dependencies. Work
   is being done to clean them up. Some, most recently numpy, have been
   changed to make them yield objects describing tasks and
   executing them in the core. This way there is a chance to know what
   the program does and make this kind of change. This transition is
   almost complete, but the Qt plugins are still missing.

   My goal here is to say that e.g. a datafile should be what Nuitka
   commercial currently calls "trusted" independent of it being a
   datafile, right now that is not the case, but Nuitka is much closer
   to that now. This is of course the same with multiple distributions.

   For data files, this plugin could hook the data file copying process
   in much the same way, and put data files near the executable or in
   the shared area.

-  Windows: Provide builds of CPython that will allow static linking,
   avoiding the CPython DLL.

-  Forcing output and stderr to files should be supported for all OSes.

-  Dejong Stacks: More robust parser that allows stdout and stderr in
   same file with mixed outputs.

-  Add ability to inhibit datafiles from the command line, so that
   things coming from a plugin can be suppressed.

-  Add support for upx (public feature)

The UPX cannot compress payloads, which is why we can't use it and
expect it to solve the onefile compression issue. However, a post
processing of binaries, even from CPython extension modules, seems to
work and reduce the uncompressed sizes of binaries already.

########################
 Nuitka-Python (public)
########################

This is currently under way and not yet described here. The current Nuitka
release has support for using it. Most work is focused on Linux and Python2.7
now with the aim of getting it capable to statically compile numpy for speed.

######################
 Performance (public)
######################

-  Caching of demoted to bytecode modules. Some of these, e.g.
   ``pkg_resources`` take very long to analyse in Nuitka, just to find
   out the imports. There is no point in repeating this, a caching of
   Python compilation is a separate line of action, but it should start
   with this.

-  Faster attribute setting.

   For Python3 we still use ``_PyObjectDict_SetItem`` which is very hard
   to replace, as it's forking shared dictionary as necessary. With static
   libpython it can linked though, but we still might want to make our
   own replacement.

-  Support for static libpython together with LTO for Python3

   This gives an enormouse speed bump for Python2 with Debian package Python
   and of course for any properly self compiled Python, and to the Nuitka
   Python there will be. For Python3, this has not yet been achieved,
   but ought to be doable too. And in some cases, it can be known to not
   work and should not be suggested.

-  Support for keyword argument calls to use faster calling code.

   Esp. for the for the compiled functions, we currently go in these cases
   through the the ``tp_call`` slot, taking dictionary, and esp. when there
   is a mixture of dictionary and keyword arguments, this is causing Nuitka
   to be even slower.

-  Faster Object creation for compiled ``__init__`` and/or ``__new__``

   Right now, these are called through the ``tp_call`` slow, which makes
   argument passing unnecessarily slow.

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

####################
 macOS enhancements
####################

-  The macOS bundle mode and onefile are not yet working together, which
   needs mainly just internal changes for where to put files. Also for
   accelerated programs, bundle mode is not usable, so they couldn't be
   GUI programs yet.

-  Apple Python must be detected and rejected for standalone mode.

###############################
 Container Builds (commercial)
###############################

Providing docker images like manylinux does with Nuitka installed into
all of them and ready to use. Might make this a free feature once it's
done and supports --commercial download of the plugins nicely.

Providing containers with old Linux, and optimally compiled CPython with
podman such that building with Nuitka on Fedora latest and Ubuntu latest
can be done fully automatically and still run on very old Linux. Right
now this is implemented, but works mostly locally and needs more work
than it should.

########################################
 Support for Next Python Version (3.10)
########################################

-  Get it to work for 3.9 test suite.

   This will usually mean it's safe to use for most people over 3.9, but
   it's not supporting the 3.10 features yet. Currently stuck at some
   changes for asyncgen.

-  Add support for new case syntax of 3.10

   This is partially done, but recursive matching needs more work, guards
   are missing, it's done with a reformulation, and needs a bunch of new
   type comparisons, but many use cases ought to work now.

-  Get it to work for 3.10 test suite.

   This will amount to fully compatibility in support.

#################################
 Features to be added for 0.6.18
#################################

List of things, we are aiming for to be included in that release.

[ ] Caching for bytecode demoted modules so no optimization needs to be
run.

[ ] Add version information for macOS bundles.

[x] Building on new macOS works for old macOS deployment.


#################################
 Features to be added for 0.6.19
#################################

[ ] Compression of onefile with bootstrap before Python3.5, so far it's
   there for 3.5 or higher only.

[ ] Better scalability
