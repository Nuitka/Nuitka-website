This is to inform you about the new stable release
of `Nuitka <https://nuitka.net>`_. It is the extremely
compatible Python compiler,  `"download now" </doc/download.html>`_.

I just have just updated Nuitka to version 0.1.1 which is a bug fix
release to 0.1, which corrects many of the small things:

-  Updated the CPython test suite to 2.6.6rc and minimized much of
   existing differences in the course.

-  Compiles standalone executable that includes modules (with --deep
   option), but packages are not yet included successfully.

-  Reference leaks with exceptions are no more.

-  ``sys.exc_info()`` works now mostly as expected (it's not a stack of
   exceptions).

-  More readable generated code, better organisation of C++ template
   code.

-  Restored debug option ``--g++-only``.

The biggest thing probably is the progress with exception tracebacks
objects in exception handlers, which were not there before (always
``None``). Having these in place will make it much more compatible. Also
with manually raised exceptions and assertions, tracebacks will now be
more correct to the line.

On a bad news, I discovered that the ``compiler`` module that I use to
create the AST from Python source code, is not only deprecated, but also
broken. I created the `CPython bug <http://bugs.python.org/issue9656>`__
about it, basically it cannot distinguish some code of the form ``d[1,]
= None`` from ``d[1] = None``. This will require a migration of the
``ast`` module, which should not be too challenging, but will take some
time.

I am aiming at it for a 0.2 release. Generating wrong code (Nuitka sees
``d[1] = None`` in both cases) is a show blocker and needs a solution.

So, yeah. It's better, it's there, but still experimental. You will find
its latest version here. Please try it out and let me know what you
think in the comments section.
