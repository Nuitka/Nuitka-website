.. title: Nuitka this week #7
.. slug: nuitka-this-week-7
.. date: 2018/09/22 11:05:00
.. tags: Python,compiler,Nuitka,NTW
.. type: text

.. contents::


Nuitka Design Philosophy
========================

.. note::

  I wrote this as part of a discussion recently, and I think it makes sense to
  share my take on Nuitka and design. This is a lot text though, feel free to
  skip forward.

The issue with Nuitka and design mainly for me is that the requirements for many
parts were and are largely unknown to me, until I actually start to do it.

My goto generators approach worked out as originally designed, and that felt
really cool for once, but the whole "C type" thing was a total unknown to me,
until it all magically took form.

But rather I know it will evolve further if I go from "bool" (complete and
coming for 0.6.0) via "void" (should be complete already, but enabling will
happen only for 0.6.1 likely) to "int", not sure how long that will take.

I really think Nuitka, unlike other software that I have designed, is more of
a prototype project that gradually turns more and more into the real thing.

I have literally spent *years* to inject proper design in steps into the
optimization phase, what I call SSA, value tracing, and it is very much there
now. I am probably going to spend similar amounts of time, to execute on
applying type inference results to the code generation.

So I turned that into something working with code strings to something working
with variable declaration objects knowing their type for the goto generators,
aiming at C types generally. All the while carrying the full weight of passing
every compatibility test there is.

Then e.g. suddenly cleaning up module variables to no longer have their special
branch, but a pseudo C type, that makes them like everything else. Great. But
when I first introduced the new thing, I postponed that, because I could sooner
apply its benefits to some things and get experience from it.

While doing partial solutions, the design sometimes horribly degrades, but only
until some features can carry the full weight, and/or have been explored to have
their final form.

Making a whole Nuitka design upfront and then executing it, would instead give
a very high probability of failing in the real world. I am therefore applying
the more agile approach, where I make things work first. And then continue to
work while I clean it up.

For every feature I added, I actively go out, and change the thing, that made
it hard or even fail. Always. I think Nuitka is largely developed by cleanups
and refactoring. Goto generators were a fine example of that, solving many of
the issues by injecting variable declarations objects into code generation,
made it easy to indicate storage (heap or object or stack) right there.

That is not to say that Nuitka didn't have the typical compiler design. Like
parsing inputs, optimizing a tree internally, producing outputs. But that grand
top level design only tells you the obvious things really and is stolen anyway
from knowing similar projects like gcc.

There always were of course obvious designs for Nuitka, but that really never
was what anybody would consider to make a Python compiler hard. But for actual
compatibility of CPython, so many details were going to require examination
with no solutions known ahead of time.

I guess, I am an extreme programmer, or agile, or however they call it these
days. At least for Nuitka. In my professional life, I have designed software
for ATC on the drawing board, then in paper, and then in code, the design just
worked, and got operational right after completion, which is rare I can tell
you.

But maybe that is what keeps me exciting about Nuitka. How I need to go beyond
my abilities and stable ground to achieve it.

But the complexity of Nuitka is so dramatically higher than anything I ever
did. It is doing a complicated, i.e. detail rich work, and then it also is
doing hard jobs where many things have to play together. And the wish to have
something working before it is completed, if it ever is, makes things very
different from projects I typically did.

So the first version of Nuitka already had a use, and when I publicly showed
it first, was capable of handling most complex programs, and the desire was to
evolve gradually.

I think I have desribed this elsewhere, but for large parts of the well or bad
designed solutions of Nuitka, there is reliable ways of demonstrating it works
correctly. Far better than I have ever encountered. i believe it's the main
reason I managed to get this off the ground is that. Having a test "oracle" is
what makes Nuitka special, i.e. comparing to existing implementations.

Like a calculator can be tested comparing it to one of the many already perfect
ones out there. That again makes Nuitka relatively easy despite the many
details to get right, there is often an easy way to tell correct from wrong.

So for me, Nuitka is on the design level, something that goes through many
iterations, discovery, prototyping, and is actually really exciting in that.

Compilers typically are boring. But for Nuitka that is totally not the case,
because Python is not made for it. Well, that*s technically untrue, lets say
not for optimizing compilers, not for type inference, etc.

UI rework
=========

Following up on discussion on the mailing list, the user interface of Nuitka
will become more clear with ``--include-*`` options and ``--[no]follow-import*``
options that better express what is going to happen.

Also the default for following with extension modules is now precisely what
you say, as going beyond what you intend to deliver makes no sense in the
normal case.

Goto Generators
===============

Now release as 0.5.33 and there has been little regressions so far, but
the one found is only in the pre-release of 0.6.0 so use that instead if
you encounter a C compilation error.

Benchmarks
==========

The performance regressions fixed for 0.6.0 impact ``pystone`` by a lot,
loops were slower, so were subscripts with constant integer indexes. It
is a pity these were introduced in previous releases during refactorings
without noticing.

We should strive to have benchmarks with trends. Right now Nuitka speedcenter
cannot do it. Focus shoud definitely go to this. Like I said, after 0.6.0
release, this will be a priority, to make them more useful.

Twitter
=======

I continue to be active there. I just put out a poll about the comment
system, and disabling Disqus comments I will focus on Twitter for web site
comments too now.

`Follow @kayhayen <https://twitter.com/kayhayen?ref_src=twsrc%5Etfw>`_

And lets not forget, having followers make me happy. So do re-tweets.

Help Wanted
===========

If you are interested, I am tagging issues
`help wanted <https://github.com/kayhayen/Nuitka/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22>`_
and there is a bunch, and very likely at least one *you* can help with.

Nuitka definitely needs more people to work on it.

Egg files in PYTHONPATH
=======================

This is a relatively old issue that now got addressed. Basically these should
be loaded from for compilation. Nuitka now unpacks them to a cache folder so
it can read source code from them, so this apparently rare use case works now,
yet again improving compatibility.

Will be there for 0.6.0 release.

Certifi
=======

Seems request module sometimes uses that. Nuitka now includes that data file
starting with 0.6.0 release.

Compatibility with pkg_resources
================================

It seems that getting "distributions" and taking versions from there, is really
a thing, and Nuitka fails pkg_resources requirement checks in standalone mode
at least, and that is of course sad.

I am currently researching how to fix that, not sure yet how to do it. But some
forms of Python installs are apparently very affected by it. I try looking into
its data gathering, maybe compiled modules can be registered there too. It seems
to be based on file system scans of its own makings, but there is always a
monkey patch possible to make it better.

Plans
=====

Still working on the 0.6.0 release, cleaning up open ends only. Release tests
seem to be pretty good looking. The UI changes and stuff are a good time to be
done now, but delay things, and there is a bunch of small things that are low
hanging fruits while I wait for test results.

But since it fixes so many performance things, it really ought to be out any
day now.

Also the in-place operations stuff, I added it to 0.6.0 too, just because it
feels very nice, and improves some operations by a lot too. Initially I had
made a cut for 0.6.1 already, but that is no more.

Donations
=========

If you want to help, but cannot spend the time, please consider to donate
to Nuitka, and go here:

`Donate to Nuitka <http://nuitka.net/pages/donations.html>`_

