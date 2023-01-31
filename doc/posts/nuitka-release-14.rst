.. post:: 2023/02/02 01:11
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

####################
 Nuitka Release 1.4
####################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release contains a large amount of performance work, where
specifically Python versions 3.7 or higher see regressions in relative
performance to CPython fixed. Many cases of macros turned to functions
have been found and resolved. For 3.10 specifically we take advantage of
new opportunities for optimization. And generally avoiding DLL calls
will benefit execution times on platform where the Python DLL is used,
most prominently Windows.

Then this also adds new features, specifically custom reports. Also
tools to aid with adding Nuitka package configuration input data, to
list DLLs and data files.

With multidist we see a brand new ability to combine several programs
into one, that will become very useful for packaging multiple binaries
without the overhead of multiple distributions.

***********
 Bug Fixes
***********

-  Standalone: Added implicit dependencies for ``dependency_injector``
   package. Fixed in 1.3.1 already.

-  Fix, the generated metadata nodes for distribution queries had an
   error in their generated children handling that could cause crashes
   at compile time. Fixed in 1.3.2 already.

-  Standalone: Added implicit dependencies for ``passlib.apache``
   package. Fixed in 1.3.2 already.

-  Windows: Fix, our shortcut to find DLLs by analyzing loaded DLLs
   stumbled in a case of a DLL loaded into the compiling Python that had
   no filename associated, while strange, we need to handle this as
   well. Fixed in 1.3.3 already.

-  Standalone: Also need to workaround more decorator tricks for
   ``networkx``. Fixed in 1.3.3 already.

-  Scons: Fix, was not updating ``PATH`` environment variable anymore,
   which could lead to externally provided compilers and internal
   winlibs gcc clashing on Windows, but should be a general problem.
   Fixed in 1.3.4 already.

-  Standalone: Added support for ``cefpython3`` package. Fixed in 1.3.4
   already.

-  Standalone: Added support for newer ``webview`` package versions.
   Fixed in 1.3.4 already.

-  Standalone: Fix, some extension modules set their ``__file__`` to
   ``None`` during multi phase imports, which we then didn't update
   anymore, however that is necessary. Fixed in 1.3.4 already.

-  Python3.10+: Fix, was not supporting ``match`` cases where an
   alternative had no condition associated. Fixed in 1.3.5 already.

-  Windows: Identify ARM64 architecture Python properly. We do not yet
   support it, but we should report it properly and some package
   configurations are already taking it already into account. Fixed in
   1.3.5 already.

-  Fix, the Nuitka meta path based loader, needs to expose a
   ``__module__`` attribute because there is code out there, that
   identifies standard loaders through looking at this value, but
   crashes without it. Fixed in 1.3.5 already.

-  Fix, very old versions of the ``importlib_metadata`` backport were
   using themselves to load their ``__version__`` attribute. Added a
   workaround for it, since in Nuitka it doesn't work until after
   loading the module.

-  Fix, value escapes for attribute and subscript assignments sources
   were not properly annotated. This could cause incorrect code
   execution. Fixed in 1.3.6 already.

-  Fix, "pure" functions, which are currently only our complex call
   helper functions, were not visited in all cases. This lead to a crash
   in code generation after modules using them got demoted to bytecode.
   After use from cache, this didn't happen again. Fixed in 1.3.6
   already.

-  Standalone: Added more implicit dependencies of crypto packages.
   Fixed in 1.3.6 already.

-  Standalone: Added implicit dependencies of ``pygments.styles``
   module. Fixed in 1.3.6 already.

-  Fix, was falsely encoding ``Ellipsis`` too soon during tree building.
   It is not quite like ``True`` and ``False``. Fixed in 1.3.6 already.

-  Standalone: Fix, ``numpy`` on macOS didn't work inside an application
   bundle anymore. Fixed in 1.3.7 already.

-  Python3.8+: Fix, need to follow change for extension module handling,
   otherwise some uses of ``os.add_dll_directory`` fail to work. Fixed
   in 1.3.8 already.

-  Standalone: Added missing implicit dependencies of ``sqlalchemy``.
   Fixed in 1.3.8 already.

-  Python3.9+: Fix, resource reader files was not fully compatible and
   needed to register with ``importlib.resources.as_file`` to work well
   with it. Fixed in 1.3.8 already.

-  Fix, the version check for ``cv2`` was not working with the
   ``opencv-python-headless`` variant. Package name and distribution
   name is not a 1:1 mapping for all things. Fixed in 1.3.8 already.

-  Standalone: Added DLLs needed for ``tls_client`` package.

-  Fix, imports of resolved names should be modified for runtime too.
   Where Nuitka recognizes aliases, as e.g. the ``requests`` module
   does, it only adding a dependency on the resolved name, but not
   ``requests`` itself. The import however was still done at runtime on
   ``requests`` which then didn't work. This was only visible if only
   these aliases to other modules were used.

-  Onefile: Fix, do not send duplicate CTRL-C to child process. Our test
   only send it to the bootstrap process, rather than the process group,
   as it normally is working, therefore misleading us into sending it to
   the child even if not needed.

-  Onefile: When not using cached mode, on Windows the temporary folder
   used sometimes failed to delete after the executable stopped with
   CTRL-C. This is due to races in releasing of locks and process
   termination and AV tools, so we now retry for some time, to make sure
   it is always deleted.

-  Standalone: Fix, was not ignoring ``.dylib`` when scanning for data
   files unlike all other DLL suffixes.

-  Standalone: Added missing implicit dependency of ``mplcairo``.

-  Standalone: The main binary name on non-Windows didn't have a suffix
   ``.bin`` unlike in accelerated mode. However, this didn't work well
   for packages which have binaries colliding with the package name.
   Therefore now the suffix is added in this case too.

-  macOS: Workaround bug in ``platform_utils.paths``. It is guessing the
   wrong path for included data files with Nuitka.

-  Standalone: Added DLLs of ``sound_lib``, selecting by OS and
   architecture.

**************
 New Features
**************

-  UI: Added new option to listing package data files. This is for use
   with analyzing standalone issues. And will output all files that are
   data files for a given package name.

   .. code:: shell

      python -m nuitka --list-package-data=tkinterweb

-  UI: Added new option to listing package DLL files. This is also for
   use with analyzing standalone issues.

   .. code:: shell

      python -m nuitka --list-package-dlls=tkinterweb

-  Reports: The usages of modules, successful or not, are now included
   in the compilation report. Checking out which ones are ``not-found``
   might help recognition of issues.

-  Multidist: You can now experimentally create binaries with multiple
   entry points. At runtime one of multiple ``__main__`` will be
   executed. The option to use is multiple ``--main=some_main.py``
   arguments. If then the binary name is changed, on execution you get a
   different variant being executed.

   .. note::

      Using it with only one replaces the previous use of the positional
      argument given and is not using multidist at all.

   .. note::

      Multidist is compatible with onefile, standalone, and mere
      acceleration. It cannot be used for module mode obviously.

   For deployment this can solve duplication.

   .. note::

      For wheels, we will probably change those with multiple entry
      points to compiling multidist executables, so we do avoid Python
      script entry points there. But this has not yet been done.

-  Onefile: Kill non-cooperating child processes on CTRL-C after a grace
   period, that can be controlled at compile time with
   ``--onefile-child-grace-time`` the hard way. This avoids hangs of
   processes that fail to properly shutdown.

-  Plugins: Add support for extra global search paths to mimic
   ``sys.path`` manipulations in the Yaml configuration with new
   ``global-sys-path`` import hack.

-  Standalone: Added support for ``tkinterweb`` on Windows. Other
   platforms will need work to be done later.

-  Fix, for package metadata as from ``importlib.metadata.metadata`` for
   use at runtime we need to use both package name and distribution name
   to create it, or else it failed to work. Packages like
   ``opencv-python-headless`` can now with this too.

-  Reports: Include used distributions of compiled packages and their
   versions.

-  Reports: Added ability to generate custom reports with
   ``--report-template`` where the user can provide a Jinja2 template to
   make his own reports.

-  Anti-Bloat: Added support for checking python flags. There are
   ``no_asserts``, ``no_docstrings`` and ``no_annotations`` now. These
   can be used to limit rules to be only applied when these optional
   modes are active.

   Not all packages will work in these modes, but often can be enhanced
   to work with relatively little patching. This allows to limit these
   patches to only where they are necessary.

**************
 Optimization
**************

-  Anti-Bloat: Avoid using ``sparse`` and through that Numba in the
   ``scipy`` package, reducing its distribution footprint. Part of 1.3.3
   already.

-  Anti-Bloat: Avoid IPython and Numba in ``trimesh`` package. Part of
   1.3.3 already.

-  Anti-Bloat: Avoid Numba in ``shap`` package. Part of 1.3.8 already.

-  Anti-bloat: Removed ``xgboost`` docstring dependencies, such that
   ``--python-flag=no_docstrings`` can be used with this package.

-  For guided deep copy ``frozenset`` and empty ``tuple`` need no copies

   This also speeds up copies of non-empty tuples by avoiding that size
   checking branch in construction with Python 3.10 or higher.

-  For node construction, avoid keyword argument style calls of the base
   class, where there is only a single argument. They don't really help
   readability, but cost compile time.

-  Determine guard mode of frames dynamically and avoid frame
   preservation checks where they are not needed.

   For Python2 this is necessary, but not for Python3, so make the
   function avoid finding the parent frame for that version entirely,
   which should speed up compilation as well.

   By not hard coding frame guard mode at creation time, and instead
   determine it at compile time, after optimization, so this now allows
   to use the "once" mode more often. This affects contractions and also
   classes on the module level right now. They do not need a cached
   frame, since their code is only executed once.

   By avoiding that useless code, the C compiler also has a slightly
   better scalability, since the classes are all created in one function
   that then has less code.

-  The bytecode cache is now checking if the used modules or attempted
   to be used modules are available or not in just the same way.
   Previously it was very dependent on the file system to contain the
   same things, which was not giving cache hits even after only creating
   a new folder near a binary, since that affected importable modules.
   With the new check it should be much more directly hitting even
   across different virtual environments, but with same code.

-  Generate base classes or mixins for all kinds of expression,
   statements and statement sequences. The previous code had a dedicated
   variant for single child, to allow faster operation in a common case,
   but still a lot of ``hasattr/getattr/setattr`` on dynamic attribute
   names were done. This was making the tree traversal during
   optimization slower than necessary.

   Another shortcoming was that for some nodes, some values are
   optional, where for others, they are not. Some values are a ``tuple``
   actually, while most are nodes only. However, dealing with this
   generically was also slower than necessary.

   The new code now enforces children types during creation and updated,
   it rejects unexpected ``None`` values for non-optional children, and
   it provides generated code to do this in the fastest way possible,
   although surely some more improvements will come here.

   Also when abstract executing the tree, rather than generically
   visiting all children, this now just unrolls this, and there are even
   some modes added, where a node can indicate properties, e.g.
   ``auto_compute_handling = "final,no_raise"`` will tell the code
   generator that this expression never raises in the computation, and
   is final, i.e. doesn't have any code to evaluate, because it cannot
   be optimized any further.

   Also the way ``checkers`` previously worked, for every node creation,
   for every child update, a dictionary lookup had to be done. This is
   now hard coded for the few nodes that actually want to convert values
   on the fly and we might make a difference in the future for optional
   checkers, such that these are only run in debug mode.

   These changes brought about much faster compilation, however the big
   elephant in the room will still be merging value traces, and
   scalability problems remain there.

-  Attribute node generation for method specs like ``dict.update``, etc.
   now provide type shapes. From these type shapes, mixins for the
   result value type are picked automatically. Previously these shapes
   were added manually. In some cases, they were even missing. In a few
   cases, where the type is dependent on the Python version, we do not
   currently do this though, so this needs more work, but expanding the
   coverage got easier in this way.

-  Determining the used modules of a module requires a tree visit
   operations, that then asked for node types and used different APIs.
   This has been unified to be able to call a virtual method instead,
   which saves some compile time.

-  After scanning for a module, we then determined the module kind even
   after we previously knew it during the scan. Also, this was checking
   ``os.path.isdir`` which was making it relatively slow and wasting 5%
   compile time on the IO being done. The check got enhanced and most
   often replaced with using the knowledge from the original import scan
   eliminating this time.

-  Already most helper code of Nuitka was included from ``.c`` files,
   but compiled generators and compiled cells codes were not yet done
   like this, making life unnecessarily harder for the compiler and
   linker. This should also allow more optimization for some codes.

-  Cache the plugin decisions about recursion for a module name. When a
   module is imported multiple times plugins were each asked again and
   again, which is not a good thing to do.

-  Avoid usage of ``PyObject_RichCompareBool`` API, as we have our own
   comparison functions that are faster and faster to call without
   crossing of DLL barrier.

-  Python3.8+: Avoid usage of ``PyIndex_Check`` which has become an API
   in 3.8, and was as a result not inlined anymore with a DLL barrier
   was to be crossed, making all kinds of multiplication and
   subscript/index operations slower.

-  Replace ``PyNumber_Index`` API with our own code. As of 3.10 it
   enforces a conversion to ``long`` that for Nuitka is not a good thing
   to do in all places. But also due to DLL barrier it was potentially
   slow to call, and is used a lot, and we can drop the checks that are
   useless for Nuitka.

-  Python3.7+: Avoid the use of ``PyImport_GetModule`` for looking up
   imported modules from ``sys.modules``, rather look it up from
   interpreter internals, also this was using subscript functions, when
   this is always a dictionary.

-  Avoid using ``PyImport_GetModuleDict`` and instead have our own API
   to get this quicker.

-  Faster exception match checks and sub type checks.

   This solves a ``TODO`` about inlining the API function used, so we
   can be faster in a relatively common operation. For every exception
   handler, we had to do one API call there.

-  Faster subtype checks.

   These are common in binary operations on non-identical types, but
   also needed for the exception checks, and object creation through
   class type calls. With our own ``PyType_IsSubType`` replacement these
   faster to use and avoid the API call.

-  Faster Python3 ``int`` value startup initialization.

   On Python 3.9 or higher we can get small int values directly from the
   interpreter, and with 3.11 they are accessible as global values.

   Also we no longer de-duplicate small int values through our cache,
   since there is no use in this, saving a bunch of startup time. And we
   can create the values with our own API replacement, that will work
   during startup already and save API calls as these can be relatively
   slow. And esp. for the small values, this benefits from not having to
   create them.

-  Faster Python3 ``bytes`` value startup initialization.

   On Python 3.10 or higher, we can create these values ourselves
   without an API call, avoiding its overhead.

   Also we no longer de-duplicate small bytes values through our cache,
   because that is already done by the API and our replacement, so this
   was just wasting time.

-  Faster ``slice`` object values with Python 3.10 or higher

   On Python 3.10 or higher, we can create these values ourselves
   without an API call, avoiding its overhead.

   These are important for Python3, because ``a[x:y]`` in the general
   case has to use ``a[slice(x,y)]`` on that version, making this
   somewhat relevant to performance in some cases.

-  Faster ``str`` built-in with API calls

   For common cases, this avoids API calls. We mostly have this such
   that ``print`` style tests do not have this as API calls where we
   strive to remove all API calls for given programs.

-  Faster exception normalization.

   For the common case, we have our own variable of
   ``PyErr_NormalizeException`` that will avoid the API call. It may
   still call the ``PyObject_IsSubclass`` API, for which we only have
   started replacement work, but this is already a step ahead in the
   right direction.

-  Faster object releases

   For Python3.8 or higher when our code released objects, it was doing
   that with an API call, due to a macro change in Python headers. We
   revert that and do it still on our own which avoids the performance
   penalty.

-  Enable Python threading during extension module DLL loading

   We now release the GIL for Python3.8 or higher when loading the DLL,
   following a change in that version.

-  Faster variable handling in trace collection. The code was doing
   checks for variable types, to decide what to do e.g. when control
   flow escapes for a variable. However, this is faster if solved with a
   virtual method in those variable classes, shifting the responsibility
   to inside there.

-  For call codes the need to check the return value was not perfectly
   annotated in all cases. This is now driven by the expression rather
   than passed, and will result in better code generated in some corner
   cases.

****************
 Organisational
****************

-  Release: Make clear we require ``wheel`` and ``setuptools`` to
   install by adding a ``pyproject.toml`` that addresses a warning of
   ``pip``. Part of 1.3.6 release already.

-  Debugging: When plugins evaluate ``when`` conditions that raise,
   output which it was exactly. Part of 1.3.3 already.

-  Anti-Bloat: Added a mnemonic and more clear message for the case of
   unwanted imports being encountered. Also do not warn about IPython
   itself using IPython packages, that must of course be considered
   normal. Now it also lists the module that does the unwanted usage
   immediately. Previously this was not as clear.

-  UI: More clear output for not yet supported Python version. Make it
   more clear in the message, what is the highest supported version, and
   what version is Nuitka and what is Python in this.

-  UI: Make sure data files have normalized paths. Specifically on
   Windows, otherwise a mix of slashes could appear. Part of 1.3.6
   release already.

-  UI: Make it clear that disabling the console harms your debugging
   when we suggest the ``--disable-console`` for GUI packages. Otherwise
   using that, they just deprive themselves of ways to get error
   information.

-  UI: The ordering of scons ``ccache`` report was not enforced. Part of
   1.3.7 release already.

-  Quality: Use proper temporary filename during autoformat, so as to
   avoid flicker in Visual Code, e.g. search results.

-  User Manual: Was still using old option name for
   ``--onefile-tempdir-spec`` that has since been made not OS specific,
   with even the OS specific name being removed.

-  Standalone: Do not include data files scanned with ``site-packages``
   or ``__pycache__`` folders. This should make it easier to use
   ``--include-data-file=./**.qml:.`` when you have a virtualenv living
   in the same folder.

-  Onefile: Added check for compression ability before starting the
   compilation to inform the user immediately.

-  Release: Mark macOS as supported in PyPI categories. This is of
   course true for a long time already.

-  Release: Mark Android as supported in PyPI categories as well. With
   some extra work, it can be used.

-  User Manual: Added section pointing to and explaining compilation
   reports. This has become extremely useful even if still somewhat work
   in progress.

-  User Manual: Added table with included custom reports, at this time
   only the license reports, which is very rough shape and needs
   contributors for good looks and content.

**********
 Cleanups
**********

-  Plugins: Moved parts of the ``pywebview`` plugin that pertain to the
   DLLs and data files to package configuration.

-  Made the user query code a dedicated function, so it can be reused
   and more consistent across its uses in Nuitka. With a default that is
   proposed to a user, and a default that applies if used
   non-interactively. We will switch all prompts to using this.

-  Code generation for module, class and function frames is now unified,
   removing duplication while also becoming more flexible. For
   generators this work has been started, but is not yet completed.

-  Nodes exposing used modules now implement the same virtual method
   providing a list of them.

-  Make sure to pass ``tuple`` values rather than ``list`` values from
   the tree building stage and node optimization creating new nodes.
   This allows us to drop conversions previously done inside of nodes.

*******
 Tests
*******

-  Do not enable deprecated plugins, the warnings about them break
   tests.

-  Ignore Qt binding warnings in tests, some are less supported than
   ``PySide6`` or commercial ``PySide2``.

*********
 Summary
*********

The focus of this release was first a major restructuring of how
children are handled in the node tree. The generated code opens up the
possibility of many more scalability improvements in the coming
releases. The pure iteration speed for the node tree will make compile
times for the Python part even shorter in coming releases. Scalability
will be a continuous focus for some releases.

Then the avoiding of API calls is a huge benefit for many platforms that
are otherwise at a disadvantage. This is also only started. We will aim
at getting more complex programs to do next to none of these, so far
only some tests are working after program start without them, which is
of course big progress. We will progress there with future releases as
well.

Catching up on problems that previous migrations have not discovered is
also a huge step forward to restoring the performance supremacy, that
was not there anymore in extreme cases.

The Yaml package configuration work is showing its fruits. More people
have been able to contribute changes for ``anti-bloat`` or missing
dependencies than ever before.

Some part of the Python 3.11 work have positively influenced things,
e.g. with the frame cleanup. THe focus of the next release cycle shall
be to add support for it. Right now, generator frames need a cleanup to
be finished, to also become better and working with 3.11 at the same
time. Where possible, work to support 3.11 was also conducted as a
cleanup action, or reduction of the technical debts.

All in all, it is fair to say that this release is a big leap forward in
all kinds of ways.
