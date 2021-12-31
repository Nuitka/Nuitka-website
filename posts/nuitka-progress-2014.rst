.. post:: 2015/03/02 07:08:54
   :tags: Python, compiler, Nuitka
   :author: Kay Hayen

######################
 Nuitka progress 2014
######################

Again, not much has happened publicly to Nuitka, except for some
releases, so it's time to make a kind of status post, about the really
exciting news there is, also looking back at 2014 for Nuitka, and
forward of course.

I meant to post this basically since last year, but never got around to
it, therefore the 2014 in the title.

.. contents::

************************************
 SSA (Single State Assignment Form)
************************************

For a long, long time already, each release of Nuitka has worked towards
enabling `"SSA"
<http://en.wikipedia.org/wiki/Static_single_assignment_form>`_ usage in
Nuitka. There is a component called "constraint collection", which is
tasked with driving the optimization, and collecting variable traces.

Based on these traces, optimizations can be made. Having SSA or not, is
(to me) the difference between Nuitka as a compiler, and Nuitka as an
optimizing compiler.

The news is, SSA has carried the day, and is used throughout code
generation for some time now, and gave minor improvements. It has been
applied to the temporary and local variable values.

And currently, work is on the way to expand it to module and shared
variables, which can get invalidated quite easily, as soon as unknown
code is executed. An issue there is to identify all those spots
reliably.

And this spring, we are finally going to see the big jump that is
happening, once Nuitka starts to use that information to propagate
things.

Still, right now, this code assigns to a local variable, then reads from
it to return. But not much longer.

.. code:: python

   def f():
       a = 1
       return a

This is going to instantly give gains, and more importantly, will enable
analysis, that leads to avoiding e.g. the creation of function objects
for local functions, being able to in-line, etc.

**************************
 Improved Code Generation
**************************

Previously, under the title "C-ish", Nuitka moved away from C++ based
code generation to less C++ based code generated, and more C-ish code.
This trend continues, and has lead to removing more code generation
improvements.

The important change recently was to remove the usage of the blocking
holdouts, the C++ classes used for local variables are closure taking,
and release, and move those to be done manually.

This enabled special code generation for in-place operations, which are
the most significant improvements of the upcoming release. These were
held back on, as with C++ destructors doing the release, it's
practically impossible to deal with values suddenly becoming illegal.
Transfer of object ownership needs to be more fluid than could be
presented to C++ objects.

Currently, this allows to speed up string in-place operations, which
very importantly then, can avoid to ``memcpy`` large values potentially.
And this is about catching up to CPython in this regard. After that, we
will likely be able to expand it to cases where CPython could never do
it, e.g. also ``int`` objects

*************
 Scalability
*************

The scalability of Nuitka depends much on generated code size. With it
being less stupid, the generated code is now not only faster, but
definitely smaller, and with more optimization, it will only become more
practical.

Removing the many C++ classes already gave the backend compiler an
easier time. But we need to do more, to e.g. have generic parameter
parsing, instead of specialized per function, and module exclusive
constants should not be pre-created, but in the module body, when they
are used.

***************
 Compatibility
***************

There is not a whole lot to gain in the compatibility domain anymore.
Nothing important certainly. But there are these minor things.

Cells for Closure
=================

However, since we now use ``PyCell`` objects for closure, we could start
and provide a real ``__closure__`` value, that could even be writable.
We could start supporting that easily.

Local Variable Storage
======================

Currently, local variables use stack storage. Were we to use function
object or frame object attached storage, we could provide frame locals
that actually work. This may be as simple as to put those in an array on
the stack and use the pointer to it.

Suddenly locals would become writable. I am not saying this is useful,
just that it's possible to do this.

*************
 Performance
*************

Graphs and Benchmarks
=====================

The work on automated performance graphs has made progress, and they are
supposed to show up on `Nuitka Speedcenter
<https://speedcenter.nuitka.net>`_ each time, ``master``, ``develop`` or
``factory`` git branches change.

There currently is no structure to these graphs. There is no
explanations or comments, and there is no trend indicators. All of which
makes it basically useless to everybody except me. And even harder for
me than necessary.

At least it's updated to latest Nikola, and uses PyGal for the graphics
now, so it's easier to expand. The plan here, is to integrate with
special pages from a Wiki, making it easy to provide comments.

************
 Standalone
************

The standalone mode of Nuitka is pretty good, and as usual it continued
to improve only.

The major improvements came from handling case collisions between
modules and packages. One can have ``Module.py`` and
``module/__init__.py`` and they both are expected to be different, even
on Windows, where filenames are case insensitive.

So, giving up on ``implib`` and similar, we finally have our own code to
scan in a compatible way the file system, and make these determinations,
whereas library code exposing functionality, doesn't handling all things
in really the proper way.

*************
 Other Stuff
*************

Funding
=======

Nuitka receives some, bit not quite enough `donations
</pages/donations.html>`_. There is no support from
organizations like e.g. the PSF, and it seems I better not hold my
breath for it. I will travel to Europython 2015, and would ask you to
support me with that, it's going to be expensive.

In 2014, with donations, I bought a "Cubox i4-Pro", which is an ARM
based machine with 4 cores, and 2GB RAM. Works from flash, and with the
eSATA disk attached, it works nice for continuous integration, which
helps me a lot to deliver extremely high quality releases. It's pretty
nice, except that when using all 4 cores, it gets too hot. So "systemd"
to the rescue and just limited the Buildbot slave's service to use 3
cores of CPU maximum and now it runs stable.

Also with donations I bought a Terrabyte SSD, which I use on the desktop
to speed up hosting the virtual machines, and my work in general.

And probably more important, the host of "nuitka.net" became a real
machine with real hardware last year, and lots more RAM, so I can spare
myself of optimizing e.g. MySQL for low memory usage. The monthly fee of
that is substantial, but supported from your donations. Thanks a lot!

Collaborators
=============

Things are coming along nicely. When I started out, I was fully aware
that the project is something that I can do on my own if necessary, and
that has not changed. Things are going slower than necessary though, but
that's probably very typical.

But you can join and should do so now, just `follow this link
</doc/user-manual.html#join-nuitka>`_ or become part of
the mailing list (since closed) and help me there with request I make,
e.g. review posts of mine, test out things, pick up small jobs, answer
questions of newcomers, you know the drill probably.

Nuitka is about to make break through progress. And you can be a part of
it. Now.

********
 Future
********

So, there is multiple things going on:

-  More "C-ish" code generation

   The next release is going to be more "C-ish" than before, and we can
   start to actually migrate to really "C" language. You can help out if
   you want to, this is fairly standard cleanups. Just pop up on the
   mailing list and say so.

   This prong of action is coming to a logical end. The "C-ish" project,
   while not planned from the outset, turns out to be a full success.
   Initially, I would not have started Nuitka, should I have faced the
   full complexity of code generation that there is now. So it was good
   to start with "C++", but it's a better Nuitka now.

-  More SSA usage

   The previous releases consolidated on SSA. A few missing
   optimizations were found, because SSA didn't realize things, which
   were then highlighted by code generation being too good, e.g. not
   using exception variables.

   We seem to have an SSA that can be fully trusted now, and while it
   can be substantially improved (e.g. the ``try/finally`` removes all
   knowledge, although it only needs to do a partial removing of
   knowledge for the finally block, not for afterwards at all), it will
   already allow for many nice things to happen.

   Once we take it to that next level, Nuitka will be able to speed up
   some things by much more than the factor it basically has provided
   for 2 years now, and it's probably going to happen before summer, or
   so I hope.

-  Value propagation

   Starting out with simple cases, Nuitka will forward propagate
   variable values, and start to eliminate variable usages entirely,
   where they are not needed.

   That will make many things much more compact, and faster at run time.
   We will then try and build "gates" for statements that they cannot
   pass, so we can e.g. optimize constant things outside of loops, that
   kind of thing.

When these 3 things come to term, Nuitka will make a huge step ahead. I
look forward to demoing function call in-lining, or at least avoiding
the argument parsing at EuroPython 2015, making direct calls, which will
be way faster than normal calls.

From then on, a boatload of work remains. The infrastructure in place,
still there is going to be plenty of work to optimize more and more
things conretely.

Let me know, if you are willing to help. I really need that help to make
things happen faster.
