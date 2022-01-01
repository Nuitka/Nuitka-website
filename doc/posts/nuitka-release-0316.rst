.. post:: 2011/12/18 17:24
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.3.16
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This time there are many bug fixes, some important scalability work, and
again improved compatibility and cleanups.

The release cycle had a focus on fixing the bug reports I received. I
have also continued to look at CPython3 compatibility, and this is the
first version to support Python3 somewhat, at least some of the basic
tests programs run (of course via ``2to3`` conversion) without trouble.
I don't know when, but it seems that it's going to work one day.

Also there has an effort to make the Debian packaging cleaner,
addressing all kinds of small issues that prevented it from entering the
Debian repository. It's still not there, but it's making progress.

***********
 Bug fixes
***********

-  Fixed a packaging problem for Linux and x64 platform, the new
   ``swapFiber.S`` file for the fiber management was not included.
   Released as 0.3.15a hot fix already.

-  Fixed an error where optimization was performed on removed
   unreachable code, which lead to an error. Released as 0.3.15b hot fix
   already.

-  Fixed an issue with ``__import__`` and recursion not happening in any
   case, because when it did, it failed due to not being ported to new
   internal APIs. Released as 0.3.15c hot fix already.

-  Fixed ``eval()`` and ``locals()`` to be supported in generator
   expressions and contractions too. Released as 0.3.15d hot fix
   already.

-  Fixed the Windows batch files ``nuitka.bat`` and
   ``nuitka-python.bat`` to not output the ``rem`` statements with the
   copyright header. Released as 0.3.15d hot fix already.

-  Fixed re-raise with ``raise``, but without a current exception set.
   Released as 0.3.15e hot fix already.

-  Fixed ``vars()`` call on the module level, needs to be treated as
   ``globals()``. Released as 0.3.15e hot fix already.

-  Fix handling of broken new lines in source files. Read the source
   code in "universal line ending mode". Released as 0.3.15f hot fix
   already.

-  Fixed handling of constant module attribute ``__name__`` being
   replaced. Don't replace local variables of the same name too.
   Released as 0.3.15g hot fix already.

-  Fixed assigning to ``True``, ``False`` or ``None``. There was this
   old ``TODO``, and some code has compatibility craft that does it.
   Released as 0.3.15g hot fix already.

-  Fix constant dictionaries not always being recognized as shared.
   Released as 0.3.15g hot fix already.

-  Fix generator function objects to not require a return frame to
   exist. In finalize cleanup it may not.

-  Fixed non-execution of cleanup codes that e.g. flush ``sys.stdout``,
   by adding ``Py_Finalize()``.

-  Fix ``throw()`` method of generator expression objects to not check
   arguments properly.

-  Fix missing fallback to subscript operations for slicing with
   non-indexable objects.

-  Fix, in-place subscript operations could fail to apply the update, if
   the intermediate object was e.g. a list and the handle just not
   changed by the operation, but e.g. the length did.

-  Fix, the future spec was not properly preserving the future division
   flag.

**************
 Optimization
**************

-  The optimization scales now much better, because per-module
   optimization only require the module to be reconsidered, but not all
   modules all the time. With many modules recursed into, this makes a
   huge difference in compilation time.

-  The creation of dictionaries from constants is now also optimized.

**************
 New Features
**************

-  As a new feature functions now have the ``func_defaults`` and
   ``__defaults__`` attribute. It works only well for non-nested
   parameters and is not yet fully integrated into the parameter
   parsing. This improves the compatibility somewhat already though.

-  The names ``True``, ``False`` and ``None`` are now converted to
   constants only when they are read-only module variables.

-  The ``PYTHONPATH`` variable is now cleared when immediately executing
   a compiled binary unless ``--execute-with-pythonpath`` is given, in
   which case it is preserved. This allows to make sure that a binary is
   in fact containing everything required.

****************
 Organisational
****************

-  The help output of Nuitka was polished a lot more. It is now more
   readable and uses option groups to combine related options together.

-  The in-line copy of Scons is not checked with PyLint anymore. We of
   course don't care.

-  Program tests are no longer executed in the program directory, so
   failed module inclusions become immediately obvious.

-  The basic tests can now be run with ``PYTHON=python3.2`` and use
   ``2to3`` conversion in that case.

**********
 Cleanups
**********

-  Moved ``tags`` to a separate module, make optimization emit only
   documented tags, checked against the list of allowed ones.

-  The Debian package has seen lots of improvements, to make it "lintian
   clean", even in pedantic mode. The homepage of Nuitka is listed, a
   watch file can check for new releases, the git repository and the
   gitweb are referenced, etc.

-  Use ``os.path.join`` in more of the test code to achieve more Windows
   portability for them.

-  Some more PyLint cleanups.

***********
 New Tests
***********

-  There is now a ``Crasher`` test, for tests that crashed Nuitka
   previously.

-  Added a program test where the imported module does a ``sys.exit()``
   and make sure it really doesn't continue after the ``SystemExit``
   exception that creates.

-  Cover the type of ``__builtins__`` in the main program and in
   imported modules in tests too. It's funny and differs between module
   and dict in CPython2.

-  Cover a final ``print`` statement without newline in the test. Must
   still receive a newline, which only happens when ``Py_Finalize()`` is
   called.

-  Added test with functions that makes a ``raise`` without an exception
   set.

-  Cover the calling of ``vars()`` on module level too.

-  Cover the use of eval in contractions and generator expressions too.

-  Cover ``func_defaults`` and ``__default__`` attributes for a function
   too.

-  Added test function with two ``raise`` in an exception handler, so
   that one becomes dead code and removed without the crash.

*********
 Summary
*********

The "git flow" was really great in this release cycle. There were many
hot fix releases being made, so that the bugs could be addressed
immediately without requiring the overhead of a full release. I believe
that this makes Nuitka clearly one of the best supported projects.

This quick turn-around also encourages people to report more bugs, which
is only good. And the structure is there to hold it. Of course, the many
bug fixes meant that there is not as much new development, but that is
not the priority, correctness is.

The work on Python3 is a bit strange. I don't need Python3 at all. I
also believe it is that evil project to remove cruft from the Python
core and make developers of all relevant Python software, add
compatibility cruft to their software instead. Yet, I can't really stop
to work on it. It has that appeal of small fixups here and there, and
then something else works too.

Python3 work is like when I was first struggling with Nuitka to pass the
CPython2 unit tests for a first time. It's fun. And then it finds real
actual bugs that apply to CPython2 too. Not doing ``Py_Finalize`` (but
having to), the slice operations shortcomings, the bug of subscript
in-place, and so on. There is likely more things hidden, and the earlier
Python3 is supported, the more benefit from increased test covered.

What's missing is more "hg" completeness. I think only the ``raise``
without exception set and the ``func_defaults`` issue were going into
its direction, but it won't be enough yet.
