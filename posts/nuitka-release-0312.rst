This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This is to inform you about the new release of Nuitka many bug fixes,
and substantial improvements especially in the organisational area.
There is a new `User Manual <https://nuitka.net/doc/user-manual.html>`__
(`PDF <https://nuitka.net/doc/user-manual.pdf>`__), with much improved
content, a ``sys.meta_path`` based import mechanism for ``--deep`` mode,
git flow goodness.

This release is generally also the result of working towards compilation
of a real programs (Mercurial) and to get things work more nicely on
Windows by default. Thanks go to Liu Zhenhai for helping me with this
goal.

Due to the use of the "git flow", most of the bugs listed here were
already fixed in on the stable release before this release. And there
were many of these.

###########
 Bug fixes
###########

-  The order of evaluation for base classes and class dictionaries was
   not enforced.

   Apparently nothing in the CPython test suite did that, I only noticed
   during debugging that Nuitka gave a different error than CPython did,
   for a class that had an undefined base class, because both class body
   and base classes were giving an error. Fixed in 0.3.11a already.

-  Method objects didn't hold a reference to the used class.

   The effect was only noticed when ``--python-debug`` was used, i.e.
   the debug version of Python linked, because then the garbage
   collector makes searches. Fixed in 0.3.11b already.

-  Set ``sys.executable`` on Linux as well. On Debian it is otherwise
   ``/usr/bin/python`` which might be a different version of Python
   entirely. Fixed in 0.3.11c already.

-  Embedded modules inside a package could hide package variables of the
   same name. Learned during PyCON DE about this corner case. Fixed in
   0.3.11d already.

-  Packages could be duplicated internally. This had no effect on
   generated code other than appearing twice in the list if frozen
   modules. Fixed in 0.3.11d already.

-  When embedding modules from outside current directory, the look-up
   failed. The embedding only ever worked for the compile itself and
   programs test cases, because they are all in the current directory
   then. Fixed in 0.3.11e already.

-  The check for ARM target broke Windows support in the Scons file.
   Fixed in 0.3.11f already.

-  The star import from external modules failed with an error in
   ``--deep`` mode. Fixed in 0.3.11g already.

-  Modules with a parent package could cause a problem under some
   circumstances. Fixed in 0.3.11h already.

-  One call variant, with both list and dict star arguments and keyword
   arguments, but no positional parameters, didn't have the required C++
   helper function implemented. Fixed in 0.3.11h already.

-  The detection of the CPU core count was broken on my hexacore at
   least. Gave 36 instead of 6, which is a problem for large programs.
   Fixed in 0.3.11h already.

-  The in-line copy of Scons didn't really work on Windows, which was
   sad, because we added it to simplify installation on Windows
   precisely because of this.

-  Cleaning up the build directory from old sources and object files
   wasn't portable to Windows and therefore wasn't effective there.

-  From imports where part of the imported were found modules and parts
   were not, didn't work. Solved by the feature branch
   ``meta_path_import`` that was merged for this release.

-  Newer MinGW gave warnings about the default visibility not being
   possible to apply to class members. Fixed by not setting this default
   visibility anymore on Windows.

-  The ``sys.executable`` gave warnings on Windows because of
   backslashes in the path. Using a raw string to prevent such problems.

-  The standard library path was hard coded. Changed to run time
   detection.

##########
 Cleanups
##########

-  Version checks on Python runtime now use a new define
   ``PYTHON_VERSION`` that makes it easier. I don't like
   ``PY_VERSION_HEX``, because it is so unreadable. Makes some of the
   checks a lot more safe.

-  The ``sys.meta_path`` based import from the ``meta_path_import``
   feature branch allowed the cleanup the way importing is done. It's a
   lot less code now.

-  Removed some unused code. We will aim at making Nuitka the tool to
   detect dead code really.

-  Moved ``nuitka.Nodes`` to ``nuitka.nodes.Nodes``, that is what the
   package is intended for, the split will come later.

###########
 New Tests
###########

-  New tests for import variants that previously didn't work: Mixed
   imports. Imports from a package one level up. Modules hidden by a
   package variable, etc.

-  Added test of function call variant that had no test previously. Only
   found it when compiling "hg". Amazing how nothing in my tests,
   CPython tests, etc. used it.

-  Added test to cover the partial success of import statements.

-  Added test to cover evaluation order of class definitions.

################
 Organisational
################

-  Migrated the "README.txt" from org-mode to ReStructured Text, which
   allows for a more readable document, and to generate a nice `User
   Manual <https://nuitka.net/doc/user-manual.html>`__ in PDF form.

-  The amount of information in "README.txt" was increased, with many
   more subjects are now covered, e.g. "git flow" and how to join Nuitka
   development. It's also impressive to see what code blocks and syntax
   highlighting can do for readability.

-  The Nuitka git repository has seen multiple hot fixes.

   These allowed to publish bug fixes immediately after they were made,
   and avoided the need for a new release just to get these out. This
   really saves me a lot of time too, because I can postpone releasing
   the new version until it makes sense because of other things.

-  Then there was a feature branch ``meta_path_import`` that lived until
   being merged to ``develop`` to improve the import code, which is now
   released on ``master`` as stable. Getting that feature right took a
   while.

-  And there is the feature branch ``minimize_CPython26_tests_diff``
   which has some success already in documenting the required changes to
   the "CPython26" test suite and in reducing the amount of differences,
   while doing it. We have a frame stack working there, albeit in too
   ugly code form.

-  The release archives are now built using ``setuptools``. You can now
   also download a zip file, which is probably more Windows friendly.
   The intention is to work on that to make ``setup.py`` produce a
   Nuitka install that won't rely on any environment variables at all.
   Right now ``setup.py`` won't even allow any other options than
   ``sdist`` to be given.

-  Ported "compile_itself.sh" to "compile_itself.py", i.e. ported it to
   Python. This way, we can execute it easily on Windows too, where it
   currently still fails. Replacing ``diff``, ``rm -rf``, etc. is a
   challenge, but it reduces the dependency on MSYS tools on Windows.

-  The compilation of standard library is disabled by default, but
   ``site`` or ``dist`` packages are now embedded. To include even
   standard library, there is a ``--really-deep`` option that has to be
   given in addition to ``--deep``, which forces this.

#########
 Summary
#########

Again, huge progress. The improved import mechanism is very beautiful.
It appears that little is missing to compile real world programs like
"hg" with Nuitka. The next release cycle will focus on that and continue
to improve the Windows support which appears to have some issues.
