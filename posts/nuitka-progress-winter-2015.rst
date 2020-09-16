.. title: Nuitka Progress in 2015
.. slug: nuitka-progress-winter-2015
.. date: 2016/01/29 08:08:54
.. tags: Python,compiler,Nuitka
.. type: text

For quite a bit, there have been no status posts, not for lack of news, but a
lot has happened indeed. I just seem to post a *lot* more to the mailing list
than I do here. Especially about unfinished stuff, which is essentially for a
project like Nuitka everything that's going on.

Like I previously said, I am shy to make public postings about unfinished stuff
and that's going to continue. But I am breaking it, to keep you up to date with
where Nuitka has been going lately.

And with release focuses, I have been making some actual changes that I think
are worth talking about.

.. contents::

SSA (Single State Assignment Form)
==================================

The SSA using release has been made last summer. Recent releases have lifted
more and more restrictions on where and now it is applied and made sure the
internal status is consistent and true. And that trend is going to continue
even more.

For shared variables (closure variables and module variables), Nuitka is still
too conservative to make optimization. Code does annotate value escapes, but
it's not yet trusting it. The next releases will focus on lifting that kind of
restriction, and for quality of result, that will mean making a huge jump ahead
once that works, so module variables used locally a lot will become even faster
to use then and subject to static optimization too.

Function Inlining
=================

When doing my talk to EuroPython 2015, I was demoing it that, and indeed, what
a break through. The circumstances under which it is done are still far too
limited though. Essentially that ability is there, but will not normally be
noticeable yet due to other optimization, e.g. functions are most often module
variables and not local to the using function.

More code generation improvements will be needed to be able to inline functions
that might raise an exception. Also the "cost" of inlining a function is also
very much an unsolved issue. It will become the focus again, once the SSA use
as indicated above expands to module variables, as then inlining other things
than local functions will be possible too.

So there is a lot of things to do for this to really make a difference to your
programs. But it's still great to have that part solved so far.

Scalability
===========

Parameter Parsing
+++++++++++++++++

Recent releases have replaced some of the oldest code of Nuitka, the one that
generated special argument parsing for each function individually, now replaced
with generic code, that surprisingly is often even faster, although quick entry
points were tough to beat.

That gives the C backend compiler a much easier time. Previously 3 C functions
were created per Python level function, two of which could get really big with
many arguments, and these are no more.

Variable Error Messages
+++++++++++++++++++++++

Something similar was going on with variable error messages. Each had their
exception value pre-computed and created at module load time. Most of these
are of course unused. This has been replaced with code that generates it on
the fly, resulting in a lot less constants code.

Code Objects
++++++++++++

And another thing was to look after code objects, of which there often were two
for each Python level function. The one used or the frame during run time and
the one used in the function object, differered often, sometimes by small things
like flags or local variable names.

That of course was just the result of not passing that along, but created cached
objects with hopefully the same options, but that not being true.

Resolving that, and sharing the code object used for creation and then the frame
is gives less complex C code too.

Optimization
++++++++++++

The scalability of Nuitka also depends much on generated code size. With the
optimization become more clever, less code is generated, and that trend will
continue as more structural optimization are applied.

Every time e.g. an exception is identified to not happen, this removes the
corresponding error exits from the C code, which then makes it easier for the
C compiler. Also more specialized code as we now have or dictionaries, is often
less complex to it.

Compatibility
=============

Important things have happened here. Full compatibility mode is planned to not
be the default anymore in upcoming releases, but that will only mean to not be
stupid compatible, but to e.g. have more complete error messages than CPython,
more correct line numbers, or for version differences, the best Python version
behaviour.

++++++++++

The stable release has full support for Python 3.5, including the new ``async``
and ``await`` functions. So recent releases can pronounce it as fully supported
which was quite a feat.

I am not sure, if you can fully appreciate the catch up game needed to play
here. CPython clearly implements a lot of features, that I have to emulate
too. That's going to repeat for every major release.

The good news is that the function type of Nuitka is now specialized to the
generators and classes, and that was a massive cleanup of its core that was
due anyway. The generators have no more their own function creation stuff
and that has been helpful with a lot of other stuff.

Another focus driven from Python3, is to get ahead with type shape tracing
and type inference of dictionary, and value tracing. To fully support Python3
classes, we need to work on something that is a dictionary a-like, and that
will only ever be efficient if we have that. Good news is that the next release
is making progress there too.

Performance
===========

Graphs and Benchmarks
+++++++++++++++++++++

I also presented this weak point to EuroPython 2015 and my plan on how to
resolve it. Unfortunately, nothing really happened here. My plan is still to
use what the PyPy people have developed as vmprof.

So that is not progressing, and I could need help with that definitely. Get in
contact if you think you can.

Standalone
==========

The standalone mode of Nuitka was pretty good, and continued to improve further,
but I don't care much.

Other Stuff
===========

EuroPython 2015
+++++++++++++++

This was a blast. Meeting people who knew Nuitka but not me was a regular
occurrence. And many people well appreciate my work. It felt much different
than the years before.

I was able to present Nuitka's function in-lining indeed there, and this high
goal that I set myself, quite impressed people.

Also I made many new contacts, largely with the scientific community. I hope to
find work with data scientists in the coming years. More amd more it looks like
my day job should be closer to Nuitka and my expertise in Python.

Funding
+++++++

Nuitka receives the occasional `donation <http://nuitka.net/pages/donations.html>`_
and those make me very happy. As there is no support from organization like the
PSF, I am all on my own there.

This year I want to travel to Europython 2016. It would be sweet if aside of my
free time it wouldn't also cost me money. So please consider donating some
more, as these kind of events are really helpul to Nuitka.

Collaborators
+++++++++++++

Nuitka is making more and more break through progress. And you can be a part of
it. Now.

You can join and should do so now, just `follow this link
<http://nuitka.net/doc/user-manual.html#join-nuitka>`_ or become part of the
mailing list (since closed) and help me there with request I make, e.g. review
posts of mine, test out things, pick up small jobs, answer questions of
newcomers, you know the drill probably.

Videos
++++++

There is a Youtube channel of mine with `all the videos of Nuitka so far
<https://www.youtube.com/playlist?list=PLKO58t9ADuF6o_Dcmve1DXpUkUEEVvDux>`_
and I have been preparing myself with proper equipment to make Videos of Nuitka,
but so far nothing has come out of that.

I do however really want to change that. Let's see if it happens.

Twitter
+++++++

I have started to use `my Twitter account <https://twitter.com/kayhayen>`_ on
occasions. You are welcome to follow me there. I will highlight interesting
stuff there.

Future
======

So, there is multiple things going on:

* Type Inference

  With SSA in place, Nuitka starts to recognize types, and treat things
  that work something assigned from ``{}`` or ``dict`` built-in with special
  nodes and code.

  That's going to be a lot of work. For ``float`` and ``list`` there are very
  important use cases, where the code can be much better. But ``dict`` is the
  hardest case, and to get the structure of shape tracing right, we are going
  there first.

* Shape Analyisis

  The plan for types, is not to use them, but the more general shapes, things
  that will be more prevalent than actual type information in a program. In
  fact the precise knowledge will be rare, but more often, we will just have
  a set of operations performed on a variable, and be able to guess from there.

  Shape analysis will begin though with concrete types like ``dict``. The reason
  is that some re-formulations like Python3 classes should not use locals, but
  dictionary accesses throughout for full compatibility. Tracing that correctly
  to be effectively the same code quality will allow to make that change.

* Plug-ins

  Something I wish I could have shown at EuroPython was plug-ins to Nuitka. It
  has become more complete, and some demo plug-ins for say Qt plugins or
  multiprocessing, are starting to work, but it's not progressing recently. The
  API will need work and of course documentation. Hope is for this to expand
  Nuitka's reach and appeal to get more contributors.

  It would be sweet, if there were any takers, aiming to complete these things.

* Nested frames

  One result of in-lining will be nested frames still present for exceptions
  to be properly annotated, or ``locals`` giving different sets of locals and
  so on.

  Some cleanup of these will be needed for code generation and SSA to be able
  to attach variables to some sort of container, and for a function to be able
  to reference different sets of these.

Let me know, if you are willing to help. I really need that help to make things
happen faster. Nuitka will become more and more important only. And with your
help, things will be there sooner.

Release Focus
=============

One thing I have started recently, is to make changes to Nuitka focused to just
one goal, and to only deal with the rare bug in other fields, but not much else
at all. So instead of across the board improvements in just about everything, I
have e.g. in the last release added type inference for dictionaries and special
nodes and their code generation for dictionary operations.

This progresses Nuitka in one field. And the next release then e.g. will only
focus on making the performance comparison tool, and not continue much in other
fields.

That way, more "flow" is possible and more visible progress too. As an example
of this, these are the focuses of last releases.

- Full Python 3.5 on a clean base with generators redone so that coroutines
  fit in nicely.
- Scalability of C compilation with argument parsing redone
- Next release soon: Shape analysis of subscript usages and optimization to
  exact dictionaries
- Next release thereafter: Comparison benchmarking (vmprof, resolving C level
  function identifiers easier)

Other focuses will also happen, but that's too far ahead. Mostly like some
usability improvements will be the focus of a release some day. Focus is for
things that are too complex to attack as a side project, and therefore never
happen although surely possible.

Digging into Python3.5 coroutines and their semantics was hard enough, and the
structural changes needed to integrate them properly with not too much special
casing, but rather removing existing special cases (generator functions) was
just too much work to ever happen while also doing other stuff.

Summary
=======

So I am very excited about Nuitka. It feels like the puzzle is coming together
finally, with type inference becoming a real thing. And should dictionaries be
sorted out, the real important types, say ``float`` for scientific use cases,
or ``int``, ``list`` for others, will be easy to make.

With this, and then harder import association (knowing what other modules are),
and module level SSA tracing that can be trusted, we can finally expect Nuitka
to be generally fast and deserve to be called a compiler.

That will take a while, but it's likely to happen in 2016. Let's see if I will
get the funding to go to EuroPython 2016, that would be great.
