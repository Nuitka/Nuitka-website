.. post:: 2011/12/01 20:24
   :tags: compiler, Nuitka, Python
   :author: Kay Hayen

#######################
 Nuitka Release 0.3.15
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`_. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This is to inform you about the new stable release of Nuitka. This time
again many organisational improvements, some bug fixes, much improved
compatibility and cleanups.

This release cycle had a focus on packaging Nuitka for easier
consumption, i.e. automatic packaging, making automatic uploads,
improvement documentation, and generally cleaning things up, so that
Nuitka becomes more compatible and ultimately capable to run the "hg"
test suite. It's not there yet, but this is a huge jump for usability of
Nuitka and its compatibility, again.

Then lots of changes that make Nuitka approach Python3 support, the
generated C++ for at least one large example is compiling with this new
release. It won't link, but there will be later releases.

And there is a lot of cleanup going on, geared towards compatibility
with line numbers in the frame object.

***********
 Bug fixes
***********

-  The main module was using ``__main__`` in tracebacks, but it must be
   ``<module>``. Released as 0.3.14a hot fix already.

-  Workaround for "execfile cannot be used as an expression". It wasn't
   possible to use ``execfile`` in an expression, only as a statement.

   But then there is crazy enough code in e.g. mercurial that uses it in
   a lambda function, which made the issue more prominent. The fix now
   allows it to be an expression, except on the class level, which
   wasn't seen yet.

-  The in-line copy of Scons was not complete enough to work for
   "Windows" or with ``--windows-target`` for cross compile. Fixed.

-  Cached frames didn't release the "back" frame, therefore holding
   variables of these longer than CPython does, which could cause
   ordering problems. Fixed for increased compatibility.

-  Handle "yield outside of function" syntax error in compiled source
   correctly. This one was giving a Nuitka backtrace, now it gives a
   ``SyntaxError`` as it needs to.

-  Made syntax/indentation error output absolutely identical to CPython.

-  Using the frame objects ``f_lineno`` may fix endless amounts bugs
   related to traceback line numbers.

**************
 New Features
**************

-  Guesses the location of the MinGW compiler under Windows to default
   install location, so it need not be added to ``PATH`` environment
   variable. Removes the need to modify ``PATH`` environment just for
   Nuitka to find it.

-  Added support for "lambda generators". You don't want to know what it
   is. Lets just say, it was the last absurd language feature out there,
   plus that didn't work. It now works perfect.

****************
 Organisational
****************

-  You can now download a Windows installer and a Debian package that
   works on Debian Testing, current Ubuntu and Mint Linux.

-  New release scripts give us the ability to have hot fix releases as
   download packages immediately. That means the "git flow" makes even
   more beneficial to the users.

-  Including the generated "README.pdf" in the distribution archives, so
   it can be read instead of "README.txt". The text file is fairly
   readable, due to the use of ReStructured Text, but the PDF is even
   nicer to read, due to e.g. syntax highlighting of the examples.

-  Renamed the main binaries to ``nuitka`` and ``nuitka-python``, so
   that there is no dependency on case sensitive file systems.

-  For Windows there are batch files ``nuitka.bat`` and
   ``nuitka-python.bat`` to make Nuitka directly executable without
   finding the ``Python.exe``, which the batch files can tell from their
   own location.

-  There are now man pages of ``nuitka`` and ``nuitka-python`` with
   examples for the most common use cases. They are of course included
   in the Debian package.

-  Don't strip the binary when executing it to analyse compiled binary
   with ``valgrind``. It will give better information that way, without
   changing the code.

**************
 Optimization
**************

-  Implemented ``swapcontext`` alike (``swapFiber``) for x64 to achieve
   8 times speedup for Generators. It doesn't do useless syscalls to
   preserve signal masks. Now Nuitka is faster at frame switching than
   CPython on x64, which is already good by design.

**********
 Cleanups
**********

-  Using the frame objects to store current line of execution avoids the
   need to store it away in helper code at all. It ought to also help a
   lot with threading support, and makes Nuitka even more compatible,
   because now line numbers will be correct even outside tracebacks, but
   for mere stack frame dumps.

-  Moved the ``for_return`` detection from code generation to tree
   building where it belongs. Yield statements used as return statements
   need slightly different code for Python2.6 difference. That solved an
   old ``TODO``.

-  Much Python3 portability work. Sometimes even improving existing
   code, the Python compiler code had picked up a few points, where the
   latest Nuitka didn't work with Python3 anymore, when put to actual
   compile.

   The test covered only syntax, but e.g. meta classes need different
   code in CPython3, and that's now supported. Also helper code was made
   portable in more places, but not yet fully. This will need more work.

-  Cleaned up uses of debug defines, so they are now more consistent and
   in one place.

-  Some more PyLint cleanups.

***********
 New Tests
***********

-  The tests are now executed by Python scripts and cover ``stderr``
   output too. Before we only checked ``stdout``. This unveiled a bunch
   of issues Nuitka had, but went unnoticed so far, and triggered e.g.
   the frame line number improvements.

-  Separate syntax tests.

-  The scripts to run the tests now are all in pure Python. This means,
   no more MinGW shell is needed to execute the tests.

*********
 Summary
*********

The Debian package, Windows installer, etc. are now automatically
updated and uploaded. From here on, there can be such packages for the
hot fix releases too.

The exception tracebacks are now correct by design, and better covered.

The generator performance work showed that the approach taken by Nuitka
is in fact fast. It was fast on ARM already, but it's nice to see that
it's now also fast on x64. Programs using generators will be affected a
lot by this.

Overall, this release brings Nuitka closer to usability. Better binary
names, man pages, improved documentation, issue tracker, etc. all there
now. I am in fact now looking for a sponsor for the Debian package to
upload it into Debian directly.

.. admonition:: Update

   The upload to Debian happened for 0.3.18 and was done by Yaroslav
   Halchenko.

What's missing is more "hg" completeness. The frame release issue helped
it, but ``inspect.getargs()`` doesn't work yet, and is a topic for a
future release. Won't be easy, as ``func_defaults`` will be an invasive
change too.
