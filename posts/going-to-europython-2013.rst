.. date: 2013/04/16 09:58:34
.. title: Going to Europython 2013
.. slug: going-to-europython-2013
.. tags: Python,Nuitka,compiler

I am going to the wonderful city of Florence, and `Europython 2013
<https://ep2013.europython.eu/>`_ and make a presentation there. This time, I am
not introducing Nuitka anymore, I did that in 2012, this time, I will try and
dive into static optimization and try to convey the message why I believe it is
possible.

.. contents::


Things to talk about
====================

Status
~~~~~~

Only briefly this time, since I will be able to say that all current Python
versions are fully supported (`surely if you help me with Python3.3 yield from
<nuitka-needs-you-a-call-for-help.html>`_), all major platforms now. One
important milestone has been reached meanwhile, and work on far reaching compile
time optimizations is happening. As this should be quite obvious stuff, I am
going to keep that short.

What I would like to get done until then:

* Win64

  One remaining area of work to achieve Win64 support, which is almost
  complete. I epxect one of the next releases to support it.

* Threading

  And of course there is threading, which was the one real major weakness
  present last time, which appears only short of pronouncing break-through. At
  least one user is using Nuitka with many threads operationally already. I just
  have to re-activate the thread using tests CPython that I disabled. Seems I
  only have to convince myself of it too.

  Since it's not totally a priority right now, one of the next releases will
  support it, likely before the conference.

But as you see. Completion all around is there or at least in sight. Kind of
worked on this nearby.


Last years questions
~~~~~~~~~~~~~~~~~~~~

Builtins
--------

For instance, writing to built-ins, what will/did happen.

Changing builtins can be done in two ways. One is to set the value on the module
level, which is something that has always worked. The other is writing to
``builtins`` module.

This is something that is OK for Nuitka in some cases (``__import__``, ``open``
) and handled by it at run time. And it's not effective in others (``len``,
``str``).

Good news is that we got contributed a "compiled built-ins" code, where we now
will be able to see such writes. Now it's only used to not check every time for
changes, but to know them (pull vs. push). But we will also use it and trigger
``RuntimeError`` exceptions for things we cannot handle when we only learn of it
at run time.

The other element to address is, it of course whole program analysis. When
Nuitka sees the write to ``builtins.str``, it may very well consider it. The
distinction between initial and current builtin values, and the optimization of
it, that will be interesting to cover.

.. note::

   Currently Nuitka does nothing of this, but it will.

Debugger - pdb
--------------

The compiled binaries work the same as the normal Python code. So you will be
able to simply use ``pdb`` on it instead.

Interacting with ``pdb`` is not *totally* out of reach, but kind of pointless
mostly, unless you need to attach to long running operational programs. For now
that use case is not supported though.

Threading
---------

I learned a whole lot about threading. Also thanks to the kind people of
Stackless Python, who explained things to me. I am still amazed at how little I
did know of these things, and still went so far. In my industry, threads are
considered not allowed, and I personally don't like them either, so my
experience was non-existing.

But in the mean time, I managed to come up with ideas that appear to work, and
if I implement the full design, it will even be more efficient than anything.

C++ to Python gaps
~~~~~~~~~~~~~~~~~~

I consider all of these more or less solved.

Well maybe except recently arose issues with MSVC for "function calls". It
appears that compiler highlights a weakness in one of my approaches. Nuitka so
far only changed the order of declaration and call arguments around, which is
kind of transparent.

But MSVC actively takes liberty to calculate function arguments as it sees
fit. The fix for it, is now totally different and should be highly portable and
even compliant to C++.

Performance
~~~~~~~~~~~

There are still slow exceptions. I would like to avoid raising C++ exceptions in
the future, because they are so slow (Python exceptions are much faster).

And diagrams, I would like to have a whole lot more of these. Since I dropped
speedcenter, I am making actual progress there. I hope to have enough to show at
the conference, where the actual strength and weakness currently is.

Since I am getting closer to pronouncing Nuitka useful. I surely believe, I need
to answer the performance question in larger detail. And of course, I need now a
better idea, what impact measures have.

But as this is a lot of work, I doubt that I will be all that perfect by then,
my goal is to have a comparison with Shedskin. No matter how unfair it is
(Shedskin does only a small subset of Python), it's the most useful comparison
in my eyes, as where Shedskin makes static type analysis, Nuitka also should do
it, only hampered by guards at maximum.

Demos
~~~~~

The talk with start out with demonstration of Nuitka, something simple first,
and then Mercurial as a more complex example, and then its test suite.

And I will show portable binaries. It seems to work quite nicely. Generally I
expect to start out with demos, and explain from there, instead of having a demo
only at the end.

If it all works out, this time, they will be prepared with ``recordmydesktop``
so I can publish them separately too.

Future Work
~~~~~~~~~~~

Generally the talk will be more directed at the future, although this is kind of
a dark area now. That's its nature I guess.

SSA
---

The talk will also be largely built SSA (static single assignment) and how it
applies to Python. What everybody means, when they say "Python is too dynamic
(to be statically compiled)" is that Python values may escape to unknown code
that changes them very often.

I will have to talk about that, and how get out of that trap, basically guards,
much like PyPy does it too. Escaped values and strange code are only one option
of things to occur. Having code for both cases, sounds possible. I will talk
about how to decide, which branches we shall have and which not.

Compiled Modules
----------------

And I believe with "compiled modules" potentially already in place, we can
achieve very cheap guards in most cases. I can at least explain, why guards can
be relatively cheap, where we need them.

I am kind of bugged by that idea. It kind of means to revisit an older
milestone, but now an idea has surfaced, that I previously didn't have, and that
I am very curious to learn the benefit of. Very quick *and* safe module
variabls, are very tempting to have, and definitely make a difference for the
Nuitka design.

Compiled Locals
---------------

Who knows, we might even have a "compiled locals" as well, which as a side
effect, also allows total interactivity with the most absurd codes. So far, each
local variable is a C++ object, and as this is compiled, and very fast.

But the frame locals is not in sync with it. Were it a special object, it could
try and interact with these when control escapes to code that we don't know if
it might use it.

Whole Program Analysis
----------------------

Big words. Can Nuitka avoid module objects entirely. Can it inline functions,
specialize them according to the only types used (think including
``os.path.dirname`` in the binary, but with the constraint that it only need to
work on string objects as input, because the program is known to use it any
different.

Perspective
===========

Last time, I spent a lot of time on justification, "why a new project?", "why
not work with the others?", what goals do I have that others do not. Giving
examples of how code generation works. Generally to give people an idea of the
project.

With this out of the way, I can now focus on inclusion, and success.

Funding
=======

And, well yes, this time I may not have to pay for it all by myself. Last time I
spent close to 1000 Euros for the trip (ticket to enter, hotel, flight, food),
because I am `accepting donations </pages/donations.html>`_ for this specific
reason.

For a strange reason, I devote substantial amounts of time to the project, only
to put it under the most liberal license. It's probably fair to allow people to
`make donations </pages/donations.html>`_ if they feel they want to further the
project, but don't know how. Or if they just consider it too important for me to
loose interest. That kind of feels unlikely though. Too much fun.

Final Picture
=============

And lets have an image I made during Europython 2012 in the city of Florence. It
shows what a vibrant place this town is.

.. image:: images/europython-2012-07-img6319.jpg

Florence is a place full of kind people. The mood not only of the conference,
but the whole city is very open minded and helpful. It was very easy to get
adopted by strangers to their party.

Final Words
===========

I am looking forward to meeting the friends I made there last time, and new
friends. I kind of a great time there last time, one of these "times of my
life". Even if the reception was not always as warm as I had deserved. I
remember laughing a lot, learning a lot. And making unique experiences.
