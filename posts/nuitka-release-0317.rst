.. post:: 2012/01/09 07:59
   :tags: compiler, Nuitka, Python
   :author: Kay Hayen

#######################
 Nuitka Release 0.3.17
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This is to inform you about the new stable release of Nuitka. This time
there are a few bug fixes, lots of very important organisational work,
and yet again improved compatibility and cleanups. Also huge is the
advance in making ``--deep`` go away and making the recursion of Nuitka
controllable, which means a lot for scalability of projects that use a
lot of packages that use other packages, because now you can choose
which ones to embed and which ones one.

The release cycle had a focus on improving the quality of the test
scripts, the packaging, and generally to prepare the work on "type
inference" in a new feature branch.

I have also continued to work towards CPython3.2 compatibility, and this
version, while not there, supports Python3 with a large subset of the
basic tests programs running fine (of course via ``2to3`` conversion)
without trouble. There is still work to do, exceptions don't seem to
work fully yet, parameter parsing seems to have changed, etc. but it
seems that CPython3.2 is going to work one day.

And there has been a lot of effort, to address the Debian packaging to
be cleaner and more complete, addressing issues that prevented it from
entering the Debian repository.

***********
 Bug fixes
***********

-  Fixed the handling of modules and packages of the same name, but with
   different casing. Problem showed under Windows only. Released as
   0.3.16a hot fix already.

-  Fixed an error where the command line length of Windows was exceeded
   when many modules were embedded, Christopher Tott provided a fix for
   it. Released as 0.3.16a hot fix already.

-  Fix, avoid to introduce new variables for where built-in exception
   references are sufficient. Released as 0.3.16b hot fix already.

-  Fix, add the missing ``staticmethod`` decorator to ``__new__``
   methods before resolving the scopes of variables, this avoids the use
   of that variable before it was assigned a scope. Released as 0.3.16b
   hot fix already.

**************
 New Features
**************

-  Enhanced compatibility again, provide enough ``co_varnames`` in the
   code objects, so that slicing them up to ``code_object.co_argcount``
   will work. They are needed by ``inspect`` module and might be used by
   some decorators as well.

-  New options to control the recursion:

   ``--recurse-none`` (do not warn about not-done recursions)
   ``--recurse-all`` (recurse to all otherwise warned modules)
   ``--recurse-to`` (confirm to recurse to those modules)
   ``--recurse-not-to`` (confirm to not recurse to those modules)

**************
 Optimization
**************

-  The optimization of constant conditional expressions was not done
   yet. Added this missing constant propagation case.

-  Eliminate near empty statement sequences (only contain a pass
   statement) in more places, giving a cleaner node structure for many
   constructs.

-  Use the pickle "protocol 2" on CPython2 except for ``unicode``
   strings where it does not work well. It gives a more compressed and
   binary representation, that is generally more efficient to un-stream
   as well. Also use the cPickle protocol, the use of ``pickle`` was not
   really necessary anymore.

****************
 Organisational
****************

-  Added a `Developer Manual
   <https://nuitka.net/doc/developer-manual.html>`__ to the release.
   It's incomplete, but it details some of the existing stuff, coding
   rules, plans for "type inference", etc.

-  Improved the ``--help`` output to use ``metavar`` where applicable.
   This makes it more readable for some options.

-  Instead of error message, give help output when no module or program
   file name was given. This makes Nuitka help out more convenient.

-  Consistently use ``#!/usr/bin/env python`` for all scripts, this was
   previously only done for some of them.

-  Ported the PyLint check script to Python as well, enhancing it on the
   way to check the exit code, and to only output changes things, as
   well as making the output of warnings for ``TODO`` items optional.

-  All scripts used for testing, PyLint checking, etc. now work with
   Python3 as well. Most useful on Arch Linux, where it's also already
   the default for ``Python``.

-  The help output of Nuitka was polished a lot more. It is now more
   readable and uses option groups to combine related options together.

-  Make the tests run without any dependence on ``PATH`` to contain the
   executables of Nuitka. This makes it easier to use.

-  Add license texts to 3rd party file that were missing them, apply
   ``licensecheck`` results to cleanup Nuitka. Also removed own
   copyright statement from in-line copy of Scons, it had been added by
   accident only.

-  Release the tests that I own as well as the Debian packaging I
   created under "Apache License 2.0" which is very liberal, meaning
   every project will be able to use it.

-  Don't require copyright assignment for contributions anymore, instead
   only "Apache License 2.0", the future Nuitka license, so that the
   code won't be a problem when changing the license of all of Nuitka to
   that license.

-  Give contributors listed in the `User Manual
   <https://nuitka.net/doc/user-manual.html>`__ an exception to the GPL
   terms until Nuitka is licensed under "Apache License 2.0" as well.

-  Added an ``--experimental`` option which can be used to control
   experimental features, like the one currently being added on branch
   ``feature/ctypes_annotation``, where "type inference" is currently
   only activated when that option is given. For this stable release, it
   does nothing.

-  Check the static C++ files of Nuitka with ``cppcheck`` as well.
   Didn't find anything.

-  Arch Linux packages have been contributed, these are linked for
   download, but the stable package may lag behind a bit.

**********
 Cleanups
**********

-  Changed ``not`` boolean operation to become a normal operator.
   Changed ``and`` and ``or`` boolean operators to a new base class, and
   making their interface more similar to that of operations.

-  Added cumulative ``tags`` to node classes for use in checks. Use it
   annotate which node kinds to visit in e.g. per scope finalization
   steps. That avoids kinds and class checks.

-  Enhanced the "visitor" interface to provide more kinds of callbacks,
   enhanced the way "each scope" visiting is achieved by generalizing is
   as "child has not tag 'closure_taker'" and that for every "node that
   has tag 'closure_taker'".

-  Moved ``SyntaxHighlighting`` module to ``nuitka.gui`` package where
   it belongs.

-  More white listing work for imports. As recursion is now the default,
   and leads to warnings for non-existent modules, the CPython tests
   gave a lot of good candidates for import errors that were white
   listed.

-  Consistently use ``nuitka`` in test scripts, as there isn't a
   ``Nuitka.py`` on all platforms. The later is scheduled for removal.

-  Some more PyLint cleanups.

***********
 New Tests
***********

-  Make sure the basic tests pass with CPython or else fail the test.
   This is to prevent false positives, where a test passes, but only
   because it fails in CPython early on and then does so with Nuitka
   too. For the syntax tests we make sure they fail.

-  The basic tests can now be run with ``PYTHON=python3.2`` and use
   ``2to3`` conversion in that case. Also the currently not passing
   tests are not run, so the passing tests continue to do so, with this
   run from the release test script ``check-release``.

-  Include the syntax tests in release tests as well.

-  Changed many existing tests so that they can run under CPython3 too.
   Of course this is via ``2to3`` conversion.

-  Don't fail if the CPython test suites are not there.

   Currently they remain largely unpublished, and as such are mostly
   only available to me (exception,
   ``feature/minimize_CPython26_tests_diff`` branch references the
   CPython2.6 tests repository, but that remains work in progress).

-  For the compile itself test: Make the presence of the Scons in-line
   copy optional, the Debian package doesn't contain it.

-  Also make it more portable, so it runs under Windows too, and allow
   to choose the Python version to test. Check this test with both
   CPython2.6 and CPython2.7 not only the default Python.

-  Before releasing, test that the created Debian package builds fine in
   a minimal Debian ``unstable`` chroot, and passes all the tests
   included in the package (``basics``, ``syntax``, ``programs``,
   ``reflected``). Also many other Debian packaging improvements.

*********
 Summary
*********

The "git flow" was used again in this release cycle and proved to be
useful not only for hot fix, but also for creating the branch
``feature/ctypes_annotation`` and rebasing it often while things are
still flowing.

The few hot fixes didn't require a new release, but the many
organisational improvements and the new features did warrant the new
release, because of e.g. the much better test handling in this release
and the improved recursion control.

The work on Python3 support has slowed down a bit. I mostly only added
some bits for compatibility, but generally it has slowed down. I wanted
to make sure it doesn't regress by accident, so running with CPython3.2
is now part of the normal release tests.

What's still missing is more "hg" completeness. Only the ``co_varnames``
work for ``inspect`` was going in that direction, and this has slowed
down. It was more important to make Nuitka's recursion more accessible
with the new options, so that was done first.

And of course, the real excitement is the "type inference" work. It will
give a huge boost to Nuitka, and I am happy that it seems to go well.
With this in place, new benchmarks may make sense. I am working on
getting it off the ground, so other people can work on it too. My idea
of ``ctypes`` native calls may become true sooner than expected. To
support that, I would like to add more tools to make sure we discover
changes earlier on, checking the XML representations of tests to
discover improvements and regressions more clearly.
