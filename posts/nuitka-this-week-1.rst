Nuitka this week #1
~~~~~

.. contents::

New Series Rationale
====================

I think I tend to prefer coding over communication too much. I think I
need to make more transparent what I am doing. Also things, will be
getting exciting continuously for a while now.

I used to status report posts, many years ago, every 3 months or so, and that
was nice for me also to get an idea of what changed, but I stopped. What
did not happen, was to successfully engage other people to contribute.

This time I am getting more intense. I will aim to do roughly weekly or
bi-weekly reports, where I highlight things that are going on, newly found
issues, hotfixes, all the things Nuitka.

Planned Mode
============

I will do it this fashion. I will write a post to the mailing list, right
about wednesday every week or so. I need to pick a day. I am working from
home that day, saving me commute time. I will invest that time into this.

The writing will not be too high quality at times. Bare with me there. Then I
will check feedback from the list, if any. Hope is for it to point out the
things where I am not correct, missing, or even engage right away.

Topics are going to be random, albeit repeating. I will try and make links
to previous issues where applicable. Therefore also the TOC, which makes for
link targets in the pages.


Locals Dict
===========

When I am speaking of locals dict, I am talking of class scopes (and functions
with ``exec`` statements). These started to use actual dictionary a while ago,
which was a severe setback to optimization.

Right now, so for this week, after a first prototype was making the replacement
of local dict assignment and references for Python2, and kind of worked through
my buildbots, flawlessly, I immediately noticed that it would require some
refactoring to not depend on the locals scopes to be only in one of the
trace collections. Thinking of future inlining, maybe part of a locals scope
was going to be in multiple functions, that ought to not be affected.

Therefore I made a global registry of locals scopes, and working on those, I
checked its variables, if they can be forward propagated, and do this not per
module, but after all the modules have been done. This is kind of a setback for
the idea of module specific optimization (cacheable later on) vs. program
optimization, but since that is not yet a thing, it can remain this
way for now.

Once I did that, I was interested to see the effect, but to my horror,
I noticed, that memory was not released for the locals dict nodes. It
was way too involved with cyclic dependencies, which are bad. So that was
problematic of course. Compilation to keep nodes in memory for both tracing
the usage as a locals dict and temporary variables, wasn't going to help
scaling at all.

Solution is finalization

Nodes need Finalization
=======================

So replaced nodes reference a parent, and then the locals scope references
variables, and trace collections referencing variables, which reference
locals scopes, and accesses referencing traces, and so on. The garbage collector
can handle some of this, but seems I was getting past that.

For a solution, I started to add a finalize method, which released the links
for locals scopes, when they are fully propagated, on the next run.

Adding a finalize to all nodes, ought to make sure, memory is released
soon, and might even find bugs, as nodes become unusable after they
are supposedly unused. Obviously, there will currently be cases, where
nodes becomes unused, but they are not finalized yet. Also, often this is
more manual, because part of the node is to be released, but one child is
re-used. That is messy.

Impact on Memory Usage
======================

The result was a bit disappointing. Yes, memory usage of mercurial compilation
went back again, but mostly to what it had been. Some classes are now having
their locals dict forward propagated, but the effect is not always a single
dictionary making yet. Right now, function definitions, are not forward at
all propagated. This is a task I want to take on before next release though,
but maybe not, there is other things too. But I am assuming that will make
most class dictionaries created without using any variables at all anymore,
which should make it really lean.

Type Hints Question
===================

Then, asking about type hints, I got the usual question about Nuitka going to
use it. And my stance is unchanged. They are just hints, not reliable. Need to
behave the same if users do it wrong. Suggested to create decorated which make
type hints enforced. But I expect nobody takes this on though. I need to make
it a Github issue of Nuitka, although technically it is pure CPython work and
ought to be done independently. Right now Nuitka is not yet there anyway yet,
to take full advantage.

Python 3.7
==========

Then, for Python 3.7, I have long gotten the 3.6 test suite to pass. I raised 2
bugs with CPython, one of which lead to update of a failing test. Nuitka had
with large delay, caught of with what ``del __annotations__`` was doing in a
class. Only with the recent work for proper locals dict code generation, we
could enforce a name to be local, and have proper code generation, that allows
for it to be unset.

This was of course a bit of work. But the optimization behind was always kind
of necessary to get right. But now, that I got this, think of my amazement
when for 3.7 they reverted to the old behavior, where annotiatons then corrupt
the module annotations

The other bug is a reference counting bug, where Nuitka tests were failing with
CPython 3.7, and turns out, there is a bug in the dictionary implementation of
3.7, but it only corrupts counts reported, not actual objects, so it's harmless,
but means for 3.7.0 the reference count tests are disabled.

Working through the 3.7 suite, I am cherry picking commits, that e.g. allow the
``repr`` of compiled functions to contain ``<compiled_function ...>`` and the
like. Nothing huge yet. There is now a subscript of type, and foremost the async
syntax became way more liberal, so it is more complex for Nuitka to make out if
it is a coroutine due to something happening inside a generator declared inside
of it. Also ``cr_origin`` was added to coroutines, but that is mostly it.

Coroutine Compatibility
=======================

A bigger thing was that I debugged coroutines and their interaction with
uncompiled and compiled coroutines awaiting one another, and turns out, there
was a lot to improve.

The next release will be much better compatible with ``asyncio`` module and
its futures, esp with exceptions to cancel tasks passed along. That required to
clone a lot of CPython generator code, due to how ugly they mess with bytecode
instruction pointers in ``yield from`` on an uncompiled coroutine, as they don't
work with ``send`` method unlike everything else has to.

PyLint Troubles
===============

For PyLint, the 2.0.0 release found new things, but unfortunately for 2.0.1
there is a lot of regressions that I had to report. I fixed the versions of
first PyLint, and now also Astroid, so Travis cannot suddenly start to fail
due to a PyLint release finding new warnings.

Currently, if you make a PR on Github, a PyLint update will break it. And also
the cron job on Travis that checks master.

As somebody pointed out, I am now using `requires.io
<https://requires.io/github/kayhayen/Nuitka/requirements/?branch=factory>`
to check for Nuitka dependencies. But since 1.9.2 is still needed for Python2,
that kind of is bound to give alarms for now.

TODO solving
============

I have a habit of doing off tasks, when I am with my notebook in some place,
and don't know what to work on. So I have some 2 hours recently like this,
and used it to look at ``TODO`` and resolve them.

I did  a bunch of cleanups for static code helpers. There was one in my mind
about calling a function with a single argument. That fast call required a
local array with one element to put the arg into. That makes using code ugly.

Issues Encountered
==================

So the ``enum`` module of Python3 hates compiled classes and their
``staticmethod`` around ``__new__``. Since it manually unwraps ``__new__`` and
then calls it itself, it then finds that a ``staticmethod`` object cannot be
called. It's purpose is to sit in the class dictionary to give a descriptor
that removes the ``self`` arg from the call.

I am contemplating submitting an upstream patch for CPython here. The hard
coded check for ``PyFunction`` on the ``__new__`` value is hard to emulate.

So I am putting the ``staticmethod`` into the dictionary passed already. But
the undecorated function should be there for full compatibility.

If I were to make compiled function type that is both a staticmethod alike and
a function, maybe I can work around it. But it's ugly and a burden. But it
would need no change. And maybe there is more core wanting to call ``__new__``
manually

Plans
=====

I intend to make a release, probably this weekend. It might not contain full
3.7 compatibility yet, although I am aiming at that.

Then I want to turn to "goto generators", a scalability improvement of
generators and coroutines that I will talk about next week then.

Until next week.
