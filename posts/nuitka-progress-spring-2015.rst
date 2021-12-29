.. post:: 2015/04/30 16:08:54
   :tags: Python, compiler, Nuitka
   :author: Kay Hayen

################################
 Nuitka Progress in Spring 2015
################################

It's absolutely time to speak about what's going on with Nuitka, there
have been a few releases, and big things are going to happen now. The
ones I have always talked of, it's happening now.

I absolutely prefer to talk of things when they are completed, that is
why I am shy to make these kinds of postings, but this time, I think
it's warranted. The next couple of releases are going to be very
different.

.. contents::

************************************
 SSA (Single State Assignment Form)
************************************

For a long, long time already, each release of Nuitka has worked towards
increasing `"SSA"
<http://en.wikipedia.org/wiki/Static_single_assignment_form>`_ usage in
Nuitka.

The component that works on this, is now called "trace collection", and
does the major driving part for optimization. It collects "variable
traces" and puts them together into "global" forms as well.

Based on these traces, optimizations can be made. Having SSA or not, is
(to me) the difference between Nuitka as a mere compiler, and Nuitka as
an optimizing compiler.

The major news is that factory versions of Nuitka now do this in serious
ways, propagating values forward, and we also are close to eliminating
dead assignments, some of which become dead by being having been forward
propagated.

So we can now finally see that big step, jump really, happening, and
Nuitka does now do some pretty good static optimization, at least
locally.

Still, right now, this trivial code assigns to a local variable, then
reads from it to return. But not for much longer.

.. code:: python

   def f():
       a = 1
       return a

This is going to instantly give performance gains, and more importantly,
will enable analysis, that leads to avoiding e.g. the creation of
function objects for local functions, becoming able to in-line, etc.

This is major excitement to me. And I cannot wait to have the releases
that do this.

*************
 Scalability
*************

The focus has also been lately, to reduce Nuitka's own memory usage. It
has gone down by a large factor, often by avoiding cyclic dependencies
in the data structures, that the garbage collector of Python failed to
deal with properly.

The scalability of Nuitka also depends much on generated code size. With
the optimization become more clever, less code needs to be generated,
and that will help a lot. On some platforms, MSVC most notably, it can
be really slow, but it's noteworthy that Nuitka works not just with 2008
edition, but with the latest MSVC, which appears to be better.

***************
 Compatibility
***************

There was not a whole lot to gain in the compatibility domain anymore.
Nothing important certainly. But there are import changes.

Python 3.5
==========

The next release has changes to compile and run the Python3.4 test suite
successfully. Passing here means, to pass/fail in the same way as does
the uncompiled Python. Failures are of course expected, and a nice way
of having coverage for exception codes.

The new ``@`` operator is not supported yet. I will wait with that for
things to stabilize. It's currently only an alpha release.

However, Nuitka has probably never been this close to supporting a new
Python version at release time. And since 3.4 was such a heavy drain,
and still not perfectly handled (``super`` still works like it's 3.3
e.g.), I wanted to know what is coming a bit sooner.

Cells for Closure
=================

We now provide a ``__closure__`` value for compiled functions too. These
are not writable in Python, so it's only a view. Having moved storage
into the compiled function object, that was easy.

Importing Enhancements
======================

The the past couple of releases, the import logic was basically
re-written with compatibility much increased. The handling of file case
during import, multiple occurrences in the path, and absolute import
future flags for relative imports has been added.

It's mainly the standalone community that will have issues, when just
one of these imports doesn't find the correct thing, but picking the
wrong one will of course have seriously bad impacts on compile time
analysis too. So once we do cross module optimization, this must be rock
solid.

I think we have gotten there, tackling these finer details now too.

*************
 Performance
*************

Graphs and Benchmarks
=====================

Nuitka, users don't know what to expect regarding the speed of their
code after compilation through Nuitka, neither now nor after type
inference (possibly hard to guess). Nuitka does a bunch of optimizations
for some constructs pretty heavily, but weak at others. But how much
does that affect real code?

There may well be no significant gain at all for many people, while
there is a number for PyStone that suggests higher. The current and
future versions possibly do speed up but the point is that you cannot
tell if it is even worth for someone to try.

Nuitka really has to catch up here. The work on automated performance
graphs has some made progress, and they are supposed to show up on
`Nuitka Speedcenter <https://speedcenter.nuitka.net>`__ each time,
``master``, ``develop`` or ``factory`` git branches change.

.. note::

   There currently is no structure to these graphs. There is no
   explanations or comments, and there is no trend indicators. All of
   which makes it basically useless to everybody except me. And even
   harder for me than necessary.

However, as a glimpse of what will happen when we in-line functions,
take a look at the case, where we already eliminate parameter parsing
only, and make tremendous speedups:

`Lambda call construct case
<https://speedcenter.nuitka.net/constructs/construct-calllambdaexpressiondirectly.html>`__

Right now (the graph gets automatic updates with each change), what you
should see, is that ``develop`` branch is 20 times faster than CPython
for that very specific bit of code. That is where we want to be, except
that with actually in-line, this will of course be even better.

It's artificial, but once we can forward propagate local function
creations, it will apply there too. The puzzle completes.

But we also need to put real programs and use cases to test. This may
need your help. Let me know if you want to.

************
 Standalone
************

The standalone mode of Nuitka is pretty good, and as usual it continued
to improve only.

Nothing all that important going on there, except the work on a plug-in
framework, which is under development, and being used to handle e.g.
PyQt plug-ins, or known issues with certain packages.

The importing improvements already mentioned, have now allowed to cover
many more libraries successfully than before.

*************
 Other Stuff
*************

Debian Stable
=============

Nuitka is now part of Debian stable, aka Jessie. Debian and Python are
the two things closest to my heart in the tech field. You can imagine
that being an upstream worthy of inclusion into Debian stable is an
import milestone to Nuitka for me.

Funding
=======

Nuitka receives the occasional `donation
<http://nuitka.net/pages/donations.html>`_ and those make me very happy.
As there is no support from organization like the PSF, I am all on my
own there.

This year I likely will travel to Europython 2015, and would ask you to
support me with that, it's going to be expensive.

EuroPython 2015
===============

I have plans to present Nuitka's function in-lining there, real stuff,
on a fully and functional compiler that works as a drop-in replacement.

Not 100% sure if I can make it by the time, but things look good.
Actually so far I felt ahead of the plan, but as you know, this can
easily change at any point. But Nuitka stands on very stable grounds
code wise.

Collaborators
=============

Things are coming along nicely. When I started out, I was fully aware
that the project is something that I can do on my own if necessary, and
that has not changed. Things are going slower than necessary though, but
that's probably very typical.

But you can join and should do so now, just `follow this link
<http://nuitka.net/doc/user-manual.html#join-nuitka>`_ or become part of
the mailing list (since closed) and help me there with request I make,
e.g. review posts of mine, test out things, pick up small jobs, answer
questions of newcomers, you know the drill probably.

Nuitka is about to make break through progress. And you can be a part of
it. Now.

********
 Future
********

So, there is multiple things going on:

-  More SSA usage

   The next releases are going to be all about getting this done.

   Once we take it to that next level, Nuitka will be able to speed up
   some things by much more than the factor it basically has provided
   for 2 years now, and it's probably going to happen long before
   EuroPython 2015.

-  Function in-lining

   For locally declared functions, it should become possible to avoid
   their creation, and make direct calls instead of ones that use
   function objects and expensive parameter handling.

   The next step there of course is to not only bind the arguments to
   the function signature, but then also to in-line and potentially
   specialize the function code. It's my goal to have that at EuroPython
   2015 in a form ready to show off.

When these 2 things come to term, Nuitka will have made really huge
steps ahead and laid the ground for success.

From then on, a boatload of work remains. The infrastructure in place,
still there is going to be plenty of work to optimize more and more
things conretely, and to e.g. do type inference, and generate different
codes for booleans, ints or float values.

Let me know, if you are willing to help. I really need that help to make
things happen faster. Nuitka will become more and more important only.
