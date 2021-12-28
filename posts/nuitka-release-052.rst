This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This is a major release, with huge changes to code generation that
improve performance in a significant way. It is a the result of a long
development period, and therefore contains a huge jump ahead.

##############
 New Features
##############

-  Added experimental support for Python 3.4, which is still work in
   progress.

-  Added support for virtualenv on macOS.

-  Added support for virtualenv on Windows.

-  Added support for macOS X standalone mode.

-  The code generation uses no header files anymore, therefore adding a
   module doesn't invalidate all compiled object files from caches
   anymore.

-  Constants code creation is now distributed, and constants referenced
   in a module are declared locally. This means that changing a module
   doesn't affect the validity of other modules object files from caches
   anymore.

##############
 Optimization
##############

-  C-ish code generation uses less C++ classes and generates more C-like
   code. Explicit temporary objects are now used for statement temporary
   variables.

-  The constants creation code is no more in a single file, but
   distributed across all modules, with only shared values created in a
   single file. This means improved scalability. There are remaining bad
   modules, but more often, standalone mode is now fast.

-  Exception handling no longer uses C++ exception, therefore has become
   much faster.

-  Loops that only break are eliminated.

-  Dead code after loops that do not break is now removed.

-  The ``try``/``finally`` and ``try``/``except`` constructs are now
   eliminated, where that is possible.

-  The ``try``/``finally`` part of the re-formulation for ``print``
   statements is now only done when printing to a file, avoiding useless
   node tree bloat.

-  Tuples and lists are now generated with faster code.

-  Locals and global variables are now access with more direct code.

-  Added support for the anonymous ``code`` type built-in.

-  Added support for ``compile`` built-in.

-  Generators that statically return immediately, e.g. due to
   optimization results, are no longer using frame objects.

-  The complex call helpers use no pseudo frames anymore. Previous code
   generation required to have them, but with C-ish code generation that
   is no more necessary, speeding up those kind of calls.

-  Modules with only code that cannot raise, need not have a frame
   created for them. This avoids useless code size bloat because of
   them. Previously the frame stack entry was mandatory.

###########
 Bug Fixes
###########

-  Windows: The resource files were cached by Scons and re-used, even if
   the input changed. The could lead to corrupted incremental builds.
   Fixed in 0.5.1.1 already.

-  Windows: For functions with too many local variables, the MSVC failed
   with an error "C1026: parser stack overflow, program too complex".
   The rewritten code generation doesn't burden the compiler as much.

-  Compatibility: The timing deletion of nested call arguments was
   different from C++. This shortcoming has been addressed in the
   rewritten code generation.

-  Compatibility: The ``__future__`` flags and ``CO_FREECELL`` were not
   present in frame flags. These were then not always properly inherited
   to ``eval`` and ``exec`` in all cases.

-  Compatibility: Compiled frames for Python3 had ``f_restricted``
   attribute, which is Python2 only. Removed it.

-  Compatibility: The ``SyntaxError`` of having a ``continue`` in a
   finally clause is now properly raised.

-  Python2: The ``exec`` statement with no locals argument provided, was
   preventing list contractions to take closure variables.

-  Python2: Having the ASCII encoding declared in a module wasn't
   working.

-  Standalone: Included the ``idna`` encoding as well.

-  Standalone: For virtualenv, the file ``orig-prefix.txt`` needs to be
   present, now it's copied into the "dist" directory as well. Fixed in
   0.5.1.1 already.

-  Windows: Handle cases, where Python and user program are installed on
   different volumes.

-  Compatibility: Can now finally use ``execfile`` as an expression. One
   of our oldest issues, no 5, is finally fixed after all this time
   thanks to C-ish code generation.

-  Compatibility: The order or call arguments deletion is now finally
   compatible. This too is thanks to C-ish code generation.

-  Compatibility: Code object flags are now more compatible for Python3.

-  Standalone: Removing "rpath" settings of shared libraries and
   extension modules included. This makes standalone binaries more
   robust on Fedora 20.

-  Python2: Wasn't falsely rejecting ``unicode`` strings as values for
   ``int`` and ``long`` variants with base argument provided.

-  Windows: For Python3.2 and 64 bits, global variable accesses could
   give false ``NameError`` exceptions. Fixed in 0.5.1.6 already.

-  Compatibility: Many ``exec`` and ``eval`` details have become more
   correctly, the argument handling is more compatible, and e.g. future
   flags are now passed along properly.

-  Compatibility: Using ``open`` with no arguments is now giving the
   same error.

################
 Organisational
################

-  Replying to email from the `issue tracker <http://bugs.nuitka.net>`__
   works now.

-  Added option name alias ``--xml`` for ``--dump-xml``.

-  Added option name alias ``--python-dbg`` for ``--python-debug``,
   which actually might make it a bit more clear that it is about using
   the CPython debug run time.

-  Remove option ``--dump-tree``, it had been broken for a long time and
   unused in favor of XML dumps.

-  New digital art folder with 3D version of Nuitka logo. Thanks to Juan
   Carlos for creating it.

-  Using "README.rst" instead of "README.txt" to make it look better on
   web pages.

-  More complete whitelisting of missing imports in standard library.
   These should give no warnings anymore.

-  Updated the Nuitka GUI to the latest version, with enhanced features.

-  The builds of releases and update of the `downloads page
   <https://nuitka.net/doc/download.html>`__ is now driven by Buildbot.
   Page will be automatically updated as updated binaries arrive.

##########
 Cleanups
##########

-  Temporary keeper variables and the nodes to handle them are now
   unified with normal temporary variables, greatly simplifying variable
   handling on that level.

-  Less code is coming from templates, more is actually derived from the
   node tree instead.

-  Releasing the references to temporary variables is now always
   explicit in the node tree.

-  The publishing and preservation of exceptions in frames was turned
   into explicit nodes.

-  Exception handling is now done with a single handle that checks with
   branches on the exception. This eliminates exception handler nodes.

-  The ``dir`` built-in with no arguments is now re-formulated to
   ``locals`` or ``globals`` with their ``.keys()`` attribute taken.

-  Dramatic amounts of cleanups to code generation specialities, that
   got done right for the new C-ish code generation.

###########
 New Tests
###########

-  Warnings from MSVC are now error exits for ``--debug`` mode too,
   expanding the coverage of these tests.

-  The outputs with ``python-dbg`` can now also be compared, allowing to
   expand test coverage for reference counts.

-  Many of the basic tests are now executable with Python3 directly.
   This allows for easier debug.

-  The library compilation test is now also executed with Python3.

#########
 Summary
#########

This release would deserve more than a minor number increase. The C-ish
code generation, is a huge body of work. In many ways, it lays ground to
taking benefit of SSA results, that previously would not have been
possible. In other ways, it's incomplete in not yet taking full
advantage yet.

The release contains so many improvements, that are not yet fully
realized, but as a compiler, it also reflects a stable and improved
state.

The important changes are about making SSA even more viable. Many of the
problematic cases, e.g. exception handlers, have been stream lined. A
whole class of variables, temporary keepers, has been eliminated. This
is big news in this domain.

For the standalone users, there are lots of refinements. There is esp. a
lot of work to create code that doesn't show scalability issues. While
some remain, the most important problems have been dealt with. Others
are still in the pipeline.

More work will be needed to take full advantage. This has been explained
in a `separate post <https://nuitka.net/posts/state-of-nuitka.html>`__
in greater detail.
