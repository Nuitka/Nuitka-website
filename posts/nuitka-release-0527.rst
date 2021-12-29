.. post:: 2017/07/23 17:42
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.5.27
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release comes a lot of bug fixes and improvements.

***********
 Bug Fixes
***********

-  Fix, need to add recursed modules immediately to the working set, or
   else they might first be processed in second pass, where global names
   that are locally assigned, are optimized to the built-in names
   although that should not happen. Fixed in 0.5.26.1 already.

-  Fix, the accelerated call of methods could crash for some special
   types. This had been a regress of 0.5.25, but only happens with
   custom extension types. Fixed in 0.5.26.1 already.

-  Python3.5: For ``async def`` functions parameter variables could fail
   to properly work with in-place assignments to them. Fixed in 0.5.26.4
   already.

-  Compatibility: Decorators that overload type checks didn't pass the
   checks for compiled types. Now ``isinstance`` and as a result
   ``inspect`` module work fine for them.

-  Compatibility: Fix, imports from ``__init__`` were crashing the
   compiler. You are not supposed to do them, because they duplicate the
   package code, but they work.

-  Compatibility: Fix, the ``super`` built-in on module level was
   crashing the compiler.

-  Standalone: For Linux, BSD and macOS extension modules and shared
   libraries using their own ``$ORIGIN`` to find loaded DLLs resulted in
   those not being included in the distribution.

-  Standalone: Added more missing implicit dependencies.

-  Standalone: Fix, implicit imports now also can be optional, as e.g.
   ``_tkinter`` if not installed. Only include those if available.

-  The ``--recompile-c-only`` was only working with C compiler as a
   backend, but not in the C++ compatibility fallback, where files get
   renamed. This prevented that edit and test debug approach with at
   least MSVC.

-  Plugins: The PyLint plug-in didn't consider the symbolic name
   ``import-error`` but only the code ``F0401``.

-  Implicit exception raises in conditional expressions would crash the
   compiler.

**************
 New Features
**************

-  Added support for Visual Studio 2017.

-  Added option ``--python2-for-scons`` to specify the Python2 execute
   to use for calling Scons. This should allow using Anaconda Python for
   that task.

**************
 Optimization
**************

-  References to known unassigned variables are now statically optimized
   to exception raises and warned about if the according option is
   enabled.

-  Unhashable keys in dictionaries are now statically optimized to
   exception raises and warned about if the according option is enabled.

-  Enable forward propagation for classes too, resulting in some classes
   to create only static dictionaries. Currently this never happens for
   Python3, but it will, once we can statically optimize ``__prepare__``
   too.

-  Enable inlining of class dictionary creations if they are mere return
   statements of the created dictionary. Currently this never happens
   for Python3, see above for why.

-  Python2: Selecting the metaclass is now visible in the tree and can
   be statically optimized.

-  For executables, we now also use a freelist for traceback objects,
   which also makes exception cases slightly faster.

-  Generator expressions no longer require the use of a function call
   with a ``.0`` argument value to carry the iterator value, instead
   their creation is directly inlined.

-  Remove "pass through" frames for Python2 list contractions, they are
   no longer needed. Minimal gain for generated code, but more
   lightweight at compile time.

-  When compiling Windows x64 with MinGW64 a link library needs to be
   created for linking against the Python DLL. This one is now cached
   and re-used if already done.

-  Use common code for ``NameError`` and ``UnboundLocalError`` exception
   code raises. In some cases it was creating the full string at compile
   time, in others at run time. Since the later is more efficient in
   terms of code size, we now use that everywhere, saving a bit of
   binary size.

-  Make sure to release unused functions from a module. This saves
   memory and can be decided after a full pass.

-  Avoid using ``OrderedDict`` in a couple of places, where they are not
   needed, but can be replaced with a later sorting, e.g. temporary
   variables by name, to achieve deterministic output. This saves memory
   at compile time.

-  Add specialized return nodes for the most frequent constant values,
   which are ``None``, ``True``, and ``False``. Also a general one, for
   constant value return, which avoids the constant references. This
   saves quite a bit of memory and makes traversal of the tree a lot
   faster, due to not having any child nodes for the new forms of return
   statements.

-  Previously the empty dictionary constant reference was specialized to
   save memory. Now we also specialize empty set, list, and tuple
   constants to the same end. Also the hack to make ``is`` not say that
   ``{} is {}`` was made more general, mutable constant references and
   now known to never alias.

-  The source references can be marked internal, which means that they
   should never be visible to the user, but that was tracked as a flag
   to each of the many source references attached to each node in the
   tree. Making a special class for internal references avoids storing
   this in the object, but instead it's now a class property.

-  The nodes for named variable reference, assignment, and deletion got
   split into separate nodes, one to be used before the actual variable
   can be determined during tree building, and one for use later on.
   This makes their API clearer and saves a tiny bit of memory at
   compile time.

-  Also eliminated target variable references, which were pseudo
   children of assignments and deletion nodes for variable names, that
   didn't really do much, but consume processing time and memory.

-  Added optimization for calls to ``staticmethod`` and ``classmethod``
   built-in methods along with type shapes.

-  Added optimization for ``open`` built-in on Python3, also adding the
   type shape ``file`` for the result.

-  Added optimization for ``bytearray`` built-in and constant values.
   These mutable constants can now be compile time computed as well.

-  Added optimization for ``frozenset`` built-in and constant values.
   These mutable constants can now be compile time computed as well.

-  Added optimization for ``divmod`` built-in.

-  Treat all built-in constant types, e.g. ``type`` itself as a
   constant. So far we did this only for constant values types, but of
   course this applies to all types, giving slightly more compact code
   for their uses.

-  Detect static raises if iterating over non-iterables and warn about
   them if the option is enabled.

-  Split of ``locals`` node into different types, one which needs the
   updated value, and one which just makes a copy. Properly track if a
   functions needs an updated locals dict, and if it doesn't, don't use
   that. This gives more efficient code for Python2 classes, and
   ``exec`` using functions in Python2.

-  Build all constant values without use of the ``pickle`` module which
   has a lot more overhead than ``marshal``, instead use that for too
   large ``long`` values, non-UTF8 ``unicode`` values, ``nan`` float,
   etc.

-  Detect the linker arch for all Linux platforms using ``objdump``
   instead of only a hand few hard coded ones.

**********
 Cleanups
**********

-  The use of ``INCREASE_REFCOUNT`` got fully eliminated.

-  Use functions not vulenerable for buffer overflow. This is generally
   good and avoids warnings given on OpenBSD during linking.

-  Variable closure for classes is different from all functions, don't
   handle the difference in the base class, but for class nodes only.

-  Make sure ``mayBeNone`` doesn't return ``None`` which means normally
   "unclear", but ``False`` instead, since it's always clear for those
   cases.

-  Comparison nodes were using the general comparison node as a base
   class, but now a proper base class was added instead, allowing for
   cleaner code.

-  Valgrind test runners got changed to using proper tool namespace for
   their code and share it.

-  Made construct case generation code common testing code for re-use in
   the speedcenter web site. The code also has minor beauty bugs which
   will then become fixable.

-  Use ``appdirs`` package to determine place to store the downloaded
   copy of ``depends.exe``.

-  The code still mentioned C++ in a lot of places, in comments or
   identifiers, which might be confusing readers of the code.

-  Code objects now carry all information necessary for their creation,
   and no longer need to access their parent to determine flag values.
   That parent is subject to change in the future.

-  Our import sorting wrapper automatically detects imports that could
   be local and makes them so, removing a few existing ones and
   preventing further ones on the future.

-  Cleanups and annotations to become Python3 PyLint clean as well. This
   found e.g. that source code references only had ``__cmp__`` and need
   rich comparison to be fully portable.

*******
 Tests
*******

-  The test runner for construct tests got cleaned up and the constructs
   now avoid using ``xrange`` so as to not need conversion for Python3
   execution as much.

-  The main test runner got cleaned up and uses common code making it
   more versatile and robust.

-  Do not run test in debugger if CPython also segfaulted executing the
   test, then it's not a Nuitka issue, so we can ignore that.

-  Improve the way the Python to test with is found in the main test
   runner, prefer the running interpreter, then ``PATH`` and registry on
   Windows, this will find the interesting version more often.

-  Added support for "Landscape.io" to ignore the inline copies of code,
   they are not under our control.

-  The test runner for Valgrind got merged with the usage for constructs
   and uses common code now.

-  Construct generation is now common code, intended for sharing it with
   the Speedcenter web site generation.

-  Rebased Python 3.6 test suite to 3.6.1 as that is the Python
   generally used now.

****************
 Organisational
****************

-  Added inline copy of ``appdirs`` package from PyPI.

-  Added credits for RedBaron and isort.

-  The ``--experimental`` flag is now creating a list of indications and
   more than one can be used that way.

-  The PyLint runner can also work with Python3 pylint.

-  The Nuitka Speedcenter got more fine tuning and produces more tags to
   more easily identify trends in results. This needs to become more
   visible though.

-  The MSI files are also built on AppVeyor, where their building will
   not depend on me booting Windows. Getting these artifacts as
   downloads will be the next step.

*********
 Summary
*********

This release improves many areas. The variable closure taking is now
fully transparent due to different node types, the memory usage dropped
again, a few obvious missing static optimizations were added, and many
built-ins were completed.

This release again improves the scalability of Nuitka, which again uses
less memory than before, although not an as big jump as before.

This does not extend or use special C code generation for ``bool`` or
any type yet, which still needs design decisions to proceed and will
come in a later release.
