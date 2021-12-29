.. post:: 2014/10/02 07:08:54
   :tags: Python, compiler, Nuitka
   :author: Kay Hayen

###################
 Nuitka shaping up
###################

Not much has happened publicly to Nuitka, so it's time to make a kind of
status post, about the exciting news there is.

.. contents::

************************************
 SSA (Single State Assignment Form)
************************************

For a long, long time already, each release of Nuitka has worked towards
enabling `"SSA"
<http://en.wikipedia.org/wiki/Static_single_assignment_form>`_ usage in
Nuitka. There is a component called "constraint collection", which is
tasked with driving the optimization, and collecting variable traces.

Based on these traces, optimizations could be made. Having SSA or not,
is (to me) the difference between Nuitka as a compiler, and Nuitka as an
optimizing compiler.

The news is, SSA is shaping up, and will be used in the next release.
Not yet to drive variable based optimization (reserved for a release
after it), but to aid the code generation to avoid useless checks.

**************************
 Improved Code Generation
**************************

Previously, under the title "C-ish", Nuitka moved away from C++ based
code generation to less C++ based code generated, and more C-ish code.
This trend continues, and has lead to removing even more code cleanups.

The more important change is from the SSA derived knowledge. Now Nuitka
knows that a variable must be assigned, cannot be assigned, may be
assigned, based on its SSA traces.

Lets check out an example:

.. code:: python

   def f():
       a = 1
       return a

Nevermind, that *obviously* the variable ``a`` can be removed, and this
could be transformed to statically return ``1``. That is the next step
(and easy if SSA is working properly), now we are looking at what
changed now.

This is code as generated now, with current 0.5.5pre5:

.. code:: c++

   tmp_assign_source_1 = const_int_pos_1;
   assert( var_a.object == NULL );
   var_a.object = INCREASE_REFCOUNT( tmp_assign_source_1 );

   tmp_return_value = var_a.object;

   Py_INCREF( tmp_return_value );
   goto function_return_exit;

There are some things, wrong with it still. For one, ``var_a`` is still
a C++ object, which we directly access. But the good thing is, we can
assert that it starts out uninitialized, before we overwrite it. The
stable release as of now, 0.5.4, generates code like this:

.. code:: c++

   tmp_assign_source_1 = const_int_pos_1;
   if (var_a.object == NULL)
   {
       var_a.object = INCREASE_REFCOUNT( tmp_assign_source_1 );
   }
   else
   {
       PyObject *old = var_a.object;
       var_a.object = INCREASE_REFCOUNT( tmp_assign_source_1 );
       Py_DECREF( old );
   }
   static PyFrameObject *cache_frame_function = NULL;
   MAKE_OR_REUSE_FRAME( cache_frame_function, codeobj_4e03e5698a52dd694c5c263550d71551, module___main__ );
   PyFrameObject *frame_function = cache_frame_function;

   // Push the new frame as the currently active one.
   pushFrameStack( frame_function );

   // Mark the frame object as in use, ref count 1 will be up for reuse.
   Py_INCREF( frame_function );
   assert( Py_REFCNT( frame_function ) == 2 ); // Frame stack

   // Framed code:
   tmp_return_value = var_a.object;

   if ( tmp_return_value == NULL )
   {

       exception_type = INCREASE_REFCOUNT( PyExc_UnboundLocalError );
       exception_value = UNSTREAM_STRING( &constant_bin[ 0 ], 47, 0 );
       exception_tb = NULL;

       frame_function->f_lineno = 4;
       goto frame_exception_exit_1;
   }

   Py_INCREF( tmp_return_value );
   goto frame_return_exit_1;

As you can see, the assignment to ``var_a.object`` was checking if it
were ``NULL``, and if were not (which we now statically know), would
release the old value. Next up, before returning, the value of
``var_a.object`` needed to be checked, if it were ``NULL``, in which
case, we would need to create a Python exception, and in order to do so,
we need to create a frame object, that even if cached, consumes time,
and code size.

So, that is the major change to code generation. The SSA information is
now used in it, and doing so, has found a bunch of issues, in how it is
built, in e.g. nested branches, that kind of stuff.

The removal of local variables as C++ classes, and them managed as
temporary variables, is going to happen in a future release, reducing
code complexity further. Were ``a`` a temporary variable, already, the
``Py_INCREF`` which implies a later ``Py_DECREF`` on the constant ``1``
could be totally avoided.

*************
 Scalability
*************

The scalability of Nuitka hinges much of generated code size. With it
being less stupid, the generated code is now not only faster, but
definitely smaller, and with more optimization, it will only become more
practical.

***************
 Compatibility
***************

Python2 exec statements
=======================

A recent change in CPython 2.7.8+ which is supposed to become 2.7.9 one
day, highlighted an issue with ``exec`` statements in Nuitka. These were
considered to be fully compatible, but apparently are not totally.

.. code:: python

   def f():
       exec a in b, c
       exec (a, b, c)

The above two are supposed to be identical. So far this was rectified at
run time of CPython, but apparently the parser is now tasked with it, so
Nuitka now sees ``exec a in b, c`` for both lines. Which is good.

However, as it stands, Nuitka handles ``exec`` in ``locals()`` the same
as ``exec`` in ``None`` for plain functions (OK to classes and modules),
which is totally a bug.

I have been working on an enhanced re-formulation (it needs to be
tracked if the value was ``None``, and then the sync back to locals from
the provided dictionary ought to be done. But the change breaks
``execfile`` in classes, which was implemented piggy-backing on
``exec``, and now requires locals to be a dictionary, and immediately
written to.

Anyway, consider ``exec`` as well working already. The non-working cases
are really corner cases, obviously nobody came across so far.

Python3 classes
===============

Incidentally, that ``execfile`` issue will be solved as soon as a bug is
fixed, that was exposed by new abilities of Python3 metaclasses. They
were first observed in Python3.4 enum classes.

.. code:: python

   class MyEnum(enum):
       red = 1
       blue = 2
       red = 3  # error

Currently, Nuitka is delaying the building of the dictionary (absent
``execfile`` built-in), and that is not allowed, in fact, immediate
writes to the mapping giving by ``__prepare__`` of the metaclass will be
required, in which case, the ``enum`` class can raise an error for the
second assignment to ``red``.

So that area now hinges on code generation to learn different local
variable codes for classes, centered around the notion of using the
locals dictionary immediately.

Python3.4
=========

The next release is no longer warning you if you use Python3.4, as many
of the remaining problems have been sorted out. Many small things were
found, and in some cases these highlighted general Python3 problems.

Nuitka for Python3 is not yet all that much in the focus in terms of
performance, but correctness will have become much better, with most
prominently, exception context being now correct most often.

The main focus of Nuitka is Python2, but to Nuitka the incompatibility
of Python3 is largely not all that much an issue. The re-formulations to
lower level operations for just about everything means that for the
largest part there is not much trouble in supporting a mostly only
slightly different version of Python.

The gain is mostly in that new tests are added in new releases, and
these sometimes find things that affect Nuitka in all versions, or at
least some others. And this could be a mere reference leak.

Consider this:

.. code:: python

   try:
       raise (TypeError, ValueError)
   except TypeError:
       pass

So, that is working with Python2, but comes from a Python3 test. Python2
is supposed to unwrap the tuple and take the first argument and raise
that. It didn't do that so far. Granted, obscure feature, but still an
incompatibility. For Python3, a ``TypeError`` should be raised
complaining that ``tuple`` is not derived from ``BaseException``.

Turned out, that also, in that case, a reference leak occurs, in that
the wrong exception was not released, and therefore memory leaked.
Should that happen a lot during a programs live, it will potentially
become an issue, as it keeps frames on the traceback also alive.

So this lead to a compatibility fix and a reference leak fix. And it was
found by the Python3.4 suite, checking that exception objects are
properly released, and that the proper kind of exception is raised in
the no longer supported case.

*************
 Performance
*************

Graphs and Benchmarks
=====================

I had been working on automated performance graphs, and they are
supposed to show up on `Nuitka Speedcenter
<https://speedcenter.nuitka.net>`_ already, but currently it's broken
and outdated.

Sad state of affairs. Reasons include that I found it too ugly to
publish unless updated to latest Nikola, for which I didn't take the
time. I intend to fix it, potentially before the release though.

Incremental Assignments
=======================

Consider the following code:

.. code:: python

   a += "bbb"

If ``a`` is a ``str``, and if (and only if), it's the only reference
being held, then CPython, reuses the object, instead of creating a new
object and copying ``a`` over. Well, Nuitka doesn't do this. This is
despite the problem being known for quite some time.

With SSA in place, and "C-ish" code generation complete, this will be
solved, but I am not going to solve this before.

************
 Standalone
************

The standalone mode of Nuitka is pretty good, and in the pre-release it
was again improved. For instance, virtualenv and standalone should work
now, and more modules are supported.

However, there are known issues with ``win32com`` and a few other
packages, which need to be debugged. Mostly these are modules doing
nasty things that make Nuitka not automatically detect imports.

This has as usual only so much priority from me. I am working on this on
some occasions, as kind of interesting puzzles to solve. Most of the
time, it just works though, with ``wxpython`` being the most notable
exception. I am going to work on that though.

The standalone compilation exhibits scalability problems of Nuitka the
most, and while it has been getting better, the recent and future
improvements will lead to smaller code, which in turn means not only
smaller executables, but also faster compilation. Again, ``wxpython`` is
a major offender there, due to its many constants, global variables,
etc. in the bindings, while Qt, PySide, and GTK are apparently already
good.

*************
 Other Stuff
*************

Funding
=======

Nuitka doesn't receive enough `donations
<http://nuitka.net/pages/donations.html>`_. There is no support from
organizations like e.g. the PSF, which recently backed several projects
by doubling donations given to them.

I remember talking to a PSF board member during Europython 2013 about
this, and the reaction was fully in line with the Europython 2012
feedback towards me from the dictator. They wouldn't help Nuitka in any
way before it is successful.

I have never officially applied for help with funding though with them.
I am going to choose to take pride in that, I suppose.

Collaborators
=============

My quest to find collaborators to Nuitka is largely failing. Aside from
the standalone mode, there have been too little contributions. Hope is
that it will change in the future, once the significant speed gains
arrive. And it might be my fault for not asking for help more, and to
arrange myself with that state of things.

Not being endorsed by the Python establishment is clearly limiting the
visibility of the project.

Anyway, things are coming along nicely. When I started out, I was fully
aware that the project is something that I can do on my own if
necessary, and that has not changed. Things are going slower than
necessary though, but that's probably very typical.

But you can join now, just `follow this link
<http://nuitka.net/doc/user-manual.html#join-nuitka>`_ or become part of
the mailing list (since closed) and help me there with request I make,
e.g. review posts of mine, test out things, pick up small jobs, answer
questions of newcomers, you know the drill probably.

********
 Future
********

So, there is multiple things going on:

-  More "C-ish" code generation

   The next release is going to be more "C-ish" than before, generating
   less complex code than before, and removes the previous
   optimizations, which were a lot of code, to e.g. detect parameter
   variables without ``del`` statements.

   This prong of action will have to continue, as it unblocks further
   changes that lead to more compatibility and correctness.

-  More SSA usage

   The next release did and will find bugs in the SSA tracing of Nuitka.
   It is on purpose only using it, to add ``assert`` statements to
   things it now no longer does. These will trigger in tests or cause
   crashes, which then can be fixed.

   We better know that SSA is flawless in its tracking, before we use it
   to make optimizations, which then have no chance to assert anything
   at all anymore.

   Once we take it to that next level, Nuitka will be able to speed up
   some things by more than the factor it basically has provided for 2
   years now, and it's probably going to happen this year.

-  More compatibility

   The new ``exec`` code makes the dictionary synchronization explicit,
   and e.g. now it is optimized away to even check for its need, if we
   are in a module or a class, or if it can be known.

   That means faster ``exec``, but more importantly, a better understood
   ``exec``, with improved ability to do ``SSA`` traces for them. Being
   able to in-line them, or to know the limit of their impact, as it
   will help to know more invariants for that code.

When these 3 things come to term, Nuitka will be a huge, huge step ahead
towards being truly a static optimizing compiler (so far it is mostly
only peep hole optimization, and byte code avoidance). I still think of
this as happening this year.
