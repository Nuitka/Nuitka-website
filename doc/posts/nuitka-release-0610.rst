.. post:: 2020/12/22 15:38
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.6.10
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release comes with many new features, e.g. onefile support, as well
as many new optimization and bug fixes.

***********
 Bug Fixes
***********

-  Fix, was memory leaking arguments of all complex call helper
   functions. Fixed in 0.6.9.6 already.

-  Plugins: Fix, the dill-compat code needs to follow API change. Fixed
   in 0.6.9.7 already.

-  Windows: Fixup for multiprocessing module and complex call helpers
   that could crash the program. Fixed in 0.6.9.7 already.

-  Fix, the frame caching could leak memory when using caching for
   functions and generators used in multiple threads.

-  Python3: Fix, importing an extension module below a compiled module
   was not possible in accelerated mode.

-  Python3: Fix, keyword arguments for ``open`` built-in were not fully
   compatible.

-  Fix, the scons python check should also not accept directories,
   otherwise strange misleading error will occur later.

-  Windows: When Python is installed through a symbolic link, MinGW64
   and Scons were having issues, added a workaround to resolve it even
   on Python2.

-  Compatibility: Added support for ``co_freevars`` in code objects,
   e.g. newer matplotlib needs this.

-  Standalone: Add needed data files for gooey. Fixed in 0.6.9.4
   already.

-  Scons: Fix, was not respecting ``--quiet`` option when running Scons.
   Fixed in 0.6.9.3 already.

-  Scons: Fix, wasn't automatically detecting Scons from promised paths.
   Fixed in 0.6.9.2 already.

-  Scons: Fix, the clcache output parsing wasn't robust enough. Fixed in
   0.6.9.1 already.

-  Python3.8: Ignore all non-strings provided in doc-string fashion,
   they are not to be considered.

-  Fix, ``getattr``, ``setattr`` and ``hasattr`` could not be used in
   finally clauses anymore. Fixed in 0.6.9.1 already.

-  Windows: For Python3 enhanced compatibility for Windows no console
   mode, they need a ``sys.stdin`` or else e.g. ``input`` will not be
   compatible and raise ``RuntimeError``.

**************
 New Features
**************

-  Added experimental support for Python 3.9, in such a way that the
   CPython3.8 test suite passes now, the 3.9 suite needs investigation
   still, so we might be missing new features.

-  Added experimental support for Onefile mode with ``--onefile`` that
   uses ``AppImage`` on Linux and our own bootstrap binary on Windows.
   Other platforms are not supported at this time. With this, the
   standalone folder is packed into a single binary. The Windows variant
   currently doesn't yet do any compression yet, but the Linux one does.

-  Windows: Added downloading of ``ccache.exe``, esp. as the other
   sources so far recommended were not working properly after updates.
   This is taken from the official project and should be good.

-  Windows: Added downloading of matching MinGW64 C compiler, if no
   other was found, or that was has the wrong architecture, e.g. 32 bits
   where we need 64 bits.

-  Windows: Added ability to copy icon resources from an existing binary
   with new option ``--windows-icon-from-exe``.

-  Windows: Added ability to provide multiple icon files for use with
   different desktop resolutions with new option
   ``--windows-icon-from-ico`` that got renamed to disambiguate from
   other icon options.

-  Windows: Added support for requesting UAC admin right with new option
   ``--windows-uac-admin``.

-  Windows: Added support for requesting "uiaccess" rights with yet
   another new option ``--windows-uac-uiaccess``.

-  Windows: Added ability to specify version info to the binary. New
   options ``--windows-company-name``, ``--windows-product-name``,
   ``--windows-file-version``, ``--windows-product-version``, and
   ``--windows-file-description`` have been added. Some of these have
   defaults.

-  Enhanced support for using the Win32 compiler of MinGW64, but it's
   not perfect yet and not recommended.

-  Windows: Added support for LTO mode for MSVC as well, this seems to
   allow more optimization.

-  Plugins: The numpy plugin now handles matplotlib3 config files
   correctly.

**************
 Optimization
**************

-  Use less C variables in dictionary created, not one per key/value
   pair. This improved scalability of C compilation.

-  Use common code for module variable access, leading to more compact
   code and enhanced scalability of C compilation.

-  Use error exit during dictionary creation to release the dictionary,
   list, tuple, and set in case of an error occurring while they are
   still under construction. That avoids releases of it in error exists,
   reducing the generated code size by a lot. This improves scalability
   of C compilation for generating these.

-  Annotate no exception raise for local variables of classes with know
   dict shape, to avoid useless error exits.

-  Annotate no exception exit for ``staticmethod`` and ``classmethod``
   as they do not check their arguments at all. This makes code
   generated for classes with these methods much more compact, mainly
   improving their scalability in C compilation.

-  In code generation, prefer ``bool`` over ``nuitka_bool`` which allows
   to annotate exception result, leading to more compact code. Also
   cleanup so that code generation always go through the C type objects,
   rather than doing cases locally, adding a C type for ``bool``.

-  Use common code for C code handling const ``None`` return only, to
   cases where there is any immutable constant value returned, avoid
   code generation for this common case. Currently mutable constants are
   not handled, this may be added in the future.

-  Annotate no exception for exception type checks in handlers for
   Python2 and no exception if the value has exception type shape for
   Python3. The exception type shape was newly added. This avoids
   useless exception handlers in most cases, where the provided
   exception is just a built-in exception name.

-  Improve speed of often used compile time methods on nodes
   representing constant values, by making their implementation type
   specific to improve frontend compile time speed, we check e.g.
   mutable and hashable a lot.

-  Provide truth value for variable references, enhancing loop
   optimization and merge value tracing, to also decide this correctly
   for values only read, and then changed through attribute, e.g.
   ``append`` on lists. This allows many more static optimization.

-  Use ``staticmethod`` for methods in Nuitka nodes to achieve faster
   frontend compile times where possible.

-  Use dedicated helper code for calls with single argument, avoiding
   the need have a call site local C array of size one, just to pass a
   pointer to it.

-  Added handling of ``hash`` slot, to predict hashable keys for
   dictionary and sets.

-  Share more slot provision for built-in type shapes from mixin
   classes, to get them more universally provided, even for special
   types, where their consideration is unusual.

-  Trace "user provided" flag only for constants where it really
   matters, i.e. for containers and generally potentially large values,
   but not for every number or boolean value.

-  Added lowering of ``bytearray`` constant values to ``bytes`` value
   iteration, while handling constant values for this optimization with
   dedicated code for improved frontend compilation speed.

-  The dict built-in now annotates the dictionary type shape of its
   result.

-  The wrapping side-effects node now passes on the type shape of the
   wrapped value, allowing for optimization of these too.

-  Split ``slice`` nodes into variants with 1, 2 or 3 arguments, to
   avoid the overhead of determining which case we have, as well as to
   save a bit of memory, since these are more frequently used on Python3
   for subscript operations. Also annotate their type shape, allowing
   more optimization.

-  Faster dictionary lookups, esp. in cases where errors occur, because
   we were manually recreating a ``KeyError`` that is already provided
   by the dict implementation. This should also be faster, as it avoids
   a CPython API call overhead on the DLL and they can provide a
   reference or not for the returned value, simplifying using code.

-  Faster dictionary containment checks, with our own dedicated helper,
   we can use code that won't create an exception when an item is not
   present at all.

-  Faster hash lookups with our own helper, separating cases where we
   want an exception for non-hashable values or not. These should also
   be faster to call.

-  Avoid acquiring thread state in exception handling that checks if a
   ``StopIteration`` occurred, to improved speed on Python3, where is
   involves locking, but this needs to be applied way more often.

-  Make sure checks to debug mode and full compatibility mode are done
   with the variables introduced, to avoid losing performance due to
   calls for Nuitka compile time enhancements. This was so far only done
   partially.

-  Split constant references into two base classes, only one of them
   tracking if the value was provided by the user. This saves compile
   time memory and avoids the overhead to check if sizes are exceeded in
   cases they cannot possibly be so.

-  The truth value of container creations is now statically known,
   because the empty container creation is no longer a possibility for
   these nodes, allowing more optimization for them.

-  Optimize the bool built-in with no arguments directory, allow to
   simplify the node for single argument form to avoid checks if an
   argument was given.

-  Added iteration handles for ``xrange`` values, and make them faster
   to create by being tied to the node type, avoiding shared types,
   instead using the mixin approach. This is in preparation to using
   them for standard iterator tracing as well. So far they are only used
   for ``any`` and ``all`` decision.

-  Added detection if a iterator next can raise, using existing iterator
   checking which allows to remove needless checks and exception traces.
   Adding a code variant for calls to next that cannot fail, while
   tuning the code used for ``next`` and unpacking next, to use faster
   exception checking in the C code. This will speed up unpacking
   performance for some forms of unpacking from known sizes.

-  Make sure to use the fastest tuple API possible in all of Nuitka,
   many place e.g. used ``PyTuple_Size``, and one was in a performance
   critical part, e.g. in code that used when compiled functions as
   called as a method.

-  Added optimized variant for ``_PyList_Extend`` for slightly faster
   unpacking code.

-  Added optimized variant for ``PyList_Append`` for faster list
   contractions code.

-  Avoid using ``RemoveFileSpec`` and instead provide our own code for
   that task, slightly reducing file size and avoiding to use the
   ``Shlapi`` link library.

*******
 Tests
*******

-  Made reflected test use common cleanup of test folder, which is more
   robust against Windows locking issues.

-  Only output changed CPython output after the forced update of cached
   value was done, avoiding duplicate or outdated outputs.

-  Avoid complaining about exceptions for in-place operations in case
   they are lowered to non-inplace operations and then raise
   unsupported, not worth the effort to retain original operator.

-  Added generated test for subscript operations, also expanding
   coverage in generated tests by making sure, conditional paths are
   both taken by varying the ``cond`` value.

-  Use our own code helper to check if an object has an attribute, which
   is faster, because it avoids creating exceptions in the first place,
   instead of removing them afterwards.

**********
 Cleanups
**********

-  Make sure that code generation always go through the C type objects
   rather than local ``elif`` casing of the type. This required cleaning
   up many of the methods and making code more abstract.

-  Added base class for C types without reference counting, so they can
   share the code that ignores their handling.

-  Remove ``getConstant`` for constant value nodes, use the more general
   ``getCompileTimeConstant`` instead, and provide quick methods that
   test for empty tuple or dict, to use for checking concrete values,
   e.g. with call operations.

-  Unified container creation into always using a factory function, to
   be sure that existing container creations are not empty.

-  Stop using ``@calledWithBuiltinArgumentNamesDecorator`` where
   possible, and instead make explicit wrapping or use correct names.
   This was used to allow e.g. an argument named ``list`` to be passed
   from built-in optimization, but that can be done in a cleaner
   fashion. Also aligned no attributes and the argument names, there was
   inconsistency there.

-  Name mangling was done differently for attribute names and normal
   names and with non-shared code, and later than necessary, removing
   this as a step from variable closure taking after initial tree build.

-  As part of the icon changes, now handled in Python code, we stop
   using the ``rc`` binary and handle all resources ourselves, allowing
   to remove that code from the Scons side of things.

-  Moved file comparison code of standalone mode into file utils
   function for use in plugins as well.

-  Unified how path concatenation is done in Nuitka helper code, there
   were more or less complete variants, this is making sure, the most
   capable form is used in all cases.

-  Massive cleanup to our scons file, by moving out util code that only
   scons uses, hacks we apply to speed up scons, and more to separate
   modules with dedicated interfaces.

-  When using ``enumerate`` we now provide start value of 1 where it is
   appropriate, e.g. when counting source code lines, rather than adding
   ``count+1`` on every usage, making code more readable.

****************
 Organisational
****************

-  Do not recommend Anaconda on Windows anymore, it seems barely
   possible to get anything installed on it with a fresh download, due
   to the resolver literally working for days without finishing, and
   then reporting conflicts, it would only we usable when starting with
   Miniconda, but that seems less interesting to users, also gcc 5.2 is
   way too old these days.

-  The commit hook should be reinstalled, since it got improved and
   adapted for newer git versions.

-  Added link to donations to funding document, following a GitHub
   standard.

-  Bumped requirements for development to the latest versions, esp.
   newer isort.

-  Added a rough description of tests to do to add a new CPython test
   suite, to allow others to take this task in the future.

-  Updated the git hook so that Windows and newest git works.

-  Make it more clear in the documentation that Microsoft Appstore
   Python is not supported.

*********
 Summary
*********

This is the big release in terms of scalability. The optimization in
this release mostly focused on getting things that cause increased
compile times sorted out. A very important fix avoids loop optimization
to leak into global passes of all modules unnecessarily, but just as
important, generated code now is much better for the C compiler to
consume in observed problematic cases.

More optimization changes are geared towards reducing Nuitka frontend
compile time, which could also be a lot in some cases, ending up
specializing more constant nodes and how they expose themselves to
optimization.

Other optimization came from supporting Python 3.9 and things come
across during the implementation of that feature, e.g. to be able to
make differences with unpacking error messages, we provide more code to
handle it ourselves, and to manually optimize how to interact with e.g.
``list`` objects.

For Windows, the automatic download of ``ccache`` and a matching MinGW64
if none was found, is a new step, that should lower the barrier of entry
for people who have no clue what a C compiler is. More changes are bound
to come in this field with future releases, e.g. making a minimum
version requirement for gcc on Windows that excludes unfit C compilers.

All in all, this release should be taken as a major cleanup, resolving
many technical debts of Nuitka and preparing more optimization to come.
