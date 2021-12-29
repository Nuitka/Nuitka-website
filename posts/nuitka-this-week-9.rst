.. post:: 2018/10/20 06:17:00
   :tags: Python, compiler, Nuitka, NTW
   :author: Kay Hayen

#####################
 Nuitka this week #9
#####################

.. contents::

**************************
 Communication vs. Coding
**************************

My new communication strategy is a full success, engagement with Nuitka
is on an all time high.

But the recent weeks more than ever highlighted why I have to force
myself to do it. I do not like to talk about unfinished stuff. And right
now, there is really a lot of it, almost only it. Also I was ill, and
otherwise busy, so this is now late by a week.

But I am keeping it up, and will give an update, despite the feeling
that it would be better to just finish a few of those things and then
talk about it, but then it will take forever and leave you in the dark.
And that is not what is supposed to be.

Bear in mind, that this is supposed to be a quick, not too polished, and
straight from top of my head, even if really a lot of content. But I
feel that esp. the optimization parts are worth reading.

**********
 Hotfixes
**********

So the 0.6.0 release was a huge success, but it definitely wasn't
perfect, and hotfixes were necessary. The latest one 0.6.0.5 was done
just yesterday and actually contains one for an important
mis-optimization being done, and you ought to update to it from any
prior 0.6.0 release.

There are also a few remaining compatibility issues fixed for 3.7 and
generally using the latest hotfix is always a good idea.

Kind of what one has to expect from a ``0`` release, this one also had
more expose than usual is seems.

**********************************
 Google Summer of Code for Nuitka
**********************************

I need more people to work on Nuitka. One way of doing this could be to
participate in Google Summer of Code under the Python umbrella. To make
that possible, I need you to volunteer as a mentor. So please, please,
do.

I know you will feel not qualified. But I just need a backup that will
help a student around obstacles in case I go missing. Contact me and I
will be very happy.

******************
 Website Overhaul
******************

I updated the website to recent Nikola and dropped the tag cloud that I
was using. Should have cleaner and better looks. Also integrated privacy
aware sharing links, where two clicks are necessary to share a page or
article like this one on Twitter, Facebook, etc.

Also the download page saw some structural updates and polishing. It
should easier to overview now.

******************
 Performance Work
******************

Adding specialized object operations
====================================

The feedback for performance and the work on 0.6.1 are fully ongoing,
and there are many major points that are ongoing. I want to briefly
cover each one of them now, but many of them will only have full effect,
once everything is in place, which each one is very critical.

So, with the type tracing, objects have known types, and short of using
a C type, knowing e.g. that an object is an `int`, and the other one
too, doing `+` for them can take a lot of advantage avoiding unrelated
checks and code paths, even if still using ``PyObject *`` at the end of
the day.

And even we are only knowing it's *not* an ``int``, but say one value is
a ``tuple`` and the other an unknown, that allows to remove checks for
``int`` shortcuts as they can no longer apply. These are tiny
optimizations then, but still worthwhile.

To further this, first the inplace operations for a couple of more or
less randomly selected types, ``list``, ``tuple``, ``int``, ``long``,
``str``, ``unicode``, ``bytes``, and ``float``, have been looked at and
have gotten their own special object based helpers if one or both types
are known to be of that kind.

Finding missing specialized object code generation
==================================================

A report has been added, that will tell when such an operation could
have been used, but was not available. This uncovered where typical
stuff goes non optimized, a nice principle to see what is actually
happening.

So adding ``list`` and ``str`` would now give a warning, although of
course, the optimization phase ought to catch the static raise that is
and never let it get there, so this report also addresses missing
optimization in an earlier phase.

Optimizing plain object operations too
======================================

So the in-place operations were then covered, so this was extended to
mere ``+`` operations too, the ones that are not in-place. Sometimes,
esp. for immutable types, there was already code for that, e.g. ``int``
doesn't really do it, in other cases, ``list`` + ``list`` code for a
quicker concat was added.

And again a report for where it's missing was added and basic coverage
for most of the types. However, in some instances, the optimization
doesn't use the full knowledge yet. But where it does, it will shove off
quite a few cycles.

Lack of type knowledge
======================

To apply these things effectively, optimization and value tracing need
to know types in the first place. I have found two obstacles for that.
One are branch merges. If a branch or both assign to the same type or
original type, well the type is changed. Previously it became "unknown"
which is treated as ``object`` for code generation, and allows nothing
really. But now that is better on develop now, and was actually a
trivial missing thing.

The other area is loops. Loops put values to unknown when entering loop
body, and again when leaving. Essentially making type tracing not
effective where it is needed the most to achieve actual performance.
Also this was limiting the knowledge for all function to one type to not
happening for these kinds of variables that were assigned inside a loop
at all.

Took me a while, but I figured out how to build type tracing for loops
that works. It currently is still unfinished in my private repo, but
passes all tests, I would just like to make it use dedicated interfaces,
and clean it up.

I will most likely have that for 0.6.1 too and that should expand the
cases where types are known in code generation by a fair amount.

The effect of that will be that more often C code generation will
actually see types. Currently e.g. a boolean variable that is assigned
in a loop, cannot use the C target type in code generation. Once loop
code is merged, it will however take advantage there too. And only then
I think adding "C int" as a C type makes sense at all.

Performance regressions vs. CPython
===================================

Then another area is performance regressions. So one thing I did early
on in the 0.6.1 cycle was using the "module var C target type" to get
in-place working for those too. Doing string concatenations on module
variables could be slower by an order of magnitude, as could be other
operations.

I still need to do it for closure variables too. Then Nuitka will do at
least as many of them perfectly as CPython does. It also will be better
at it them, because e.g. it doesn't have to delete from the module
dictionary first, due to it never taking a reference, and same applies
to the cell. Should be faster for that too.

But strings in-place on these if not optimized, it will look very ugly
in terms of worse performance, so 0.6.0 was still pretty bad for some
users. This will however hopefully be addressed in 0.6.1 then.

In-place unicode still being bad
================================

Another field was in-place string add for the already optimized case, it
was still slower than CPython, and I finally found out what causes this.
And that is the using of ``libpython`` where ``PyUnicode_Append`` is far
worse than in the ``python`` binary that you normally use, I have see
that at least for 3.5 and higher CPython. Analysis showed that e.g.
MiniConda had the issue to a much smaller extent, and was being much
faster anyway, but probably just has better ``libpython`` compilation
flags.

So what to do. Ultimately that was to be solved by including a clone of
that function, dubbed ``UNICODE_APPEND`` that behaves the same, and can
even shove off a couple of cycles, by indicating the Python error status
without extra checks, and specializing it for the pure ``unicode +=
unicode`` case that we see most often, same for ``UNICODE_CONCAT`` for
mere ``+``.

Right now the benchmarks to show it do not exist yet. Again something
that typically wants me to delay stuff. But as you can imagine, tracking
down these hard issues, writing that much code to replace the unicode
resizing, is hard enough by itself.

But I hope to convince myself that this will allow to show that for
compiled code, things are going to be faster only now.

Benchmarks Missing
==================

In fact, speedcenter as a whole is currently broken, mostly due to
Nikola changes that I am trying to work around, but it will take more
time apparently and isn't finished as I write this.

Type shapes in optimization
===========================

Another optimization end, is the type shapes of the ``+`` operation
itself. Right now what is being done is that the shape is derived from
the shape of the left argument with the right shape to be considered by
it. These also have reports now, for cases where they are missing. So
saying e.g. that ``int`` + ``float`` results in ``float`` and these
kinds of things, are stuff being encoded there right now.

This is necessary step to e.g. know that ``int`` + ``int`` ->
``int_or_long``, to make effective loop variable optimization.

Without these, and again, that is a lot of code to write, there is no
way to hope for wide spread type knowledge in code generation.

Control flow escape
===================

Something missing there, is to also make it known that ``+`` unlike it
currently is now, should not in all cases lead to "control flow escape"
with the consequence of removing all stuff, and expecting an exception
possible, but instead to let the ``int`` type also make known that ``+
int`` ont it not only gives an ``int_or_long`` result shape, but also
while doing so, that it will never raise an exception (bare
``MemoryError``), and therefore allow more optimization to happen and
less and therefore faster code generated.

Until this is done, what is actually going to happen is that while the
``+`` result is known, Nuitka will assume control flow escape.

And speaking of that, I think this puts too many variables to a too
unknown state. You can to distrust all values, but not the types in this
case, so that could be better, but right now it is not. Something else
to look into.

Overall
=======

So 0.6.1 is in full swing in terms of optimization. All these ends need
a completion, and then I can expect to use advantage of things in a
loop, and ultimately to generate C performance code for one example of
loop. esp. if we add a C ``int`` target type, which currently isn't yet
started, because I think it would barely be used yet.

But we are getting there and I wouldn't even say we are making small
steps, this is all just work to be completed, nothing fundamental about
it. But it may take more than one release for sure.

Mind you, there is not only ``+``, there is also ``-``, ``*``, ``%``,
and many more operators, all of them will require work. Granted, loop
variables tend to use ``+`` more often, but any un-optimized operation
will immediately loose a lot of type knowledge.

**********************
 Improved Annotations
**********************

There are two kinds of annotations, ones for classes and modules, which
actually are stored in a ``__annotations__`` variable, and everything
else is mostly just ignored.

So Nuitka got the criterion wrong, and did one thing for functions, and
the other for everything else. So that annotations in generators,
coroutines and asyncgen ended up with wrong, crashing, and slower code,
due to it updating the module ``__annotations__``, so that one is
important too if you have to do those.

****************
 Release or not
****************

To release or not. There is at least one bug about star imports that
affects numpy that is solved in develop, and wasn't back ported, and I
was thinking it only applies to develop, but in fact does to stable. It
makes me want to release even before all these optimization things
happen and are polished, and I might well decide to go with that.

Maybe I only add the closure in-place stuff and the polish the loop SSA
stuff, and then call it a release. It already will solve a lot of
performance issues that exist right now, while staging the ground for
more.

*************************
 Standalone Improvements
*************************

Standalone work is also improving. Using pyi files got more apt, and a
few things were added, all of which make sense to be used by people.

But I also have a backlog of issues there however. I will schedule one
sprint for those I guess, where I focus on these. I am neglecting those
somewhat recently.

******************
 Caching Examined
******************

For the static code, I now noticed that it's compiled for each target
name, due to the build directory being part of the object file for
debug. For gcc 8 there is an option to allow pointing at the original
static C file location, and then ``ccache`` is more effective, because
object files will be the same.

That's actually pretty bad, as most of my machines are on ``gcc-6`` and
makes me think that ``libnuitka.a`` is really more of an requirement
than ever. I might take some time to get this sorted out.

******************************
 Python3 deprecation warnings
******************************

So Nuitka supports the ``no_warnings`` Python flag, and for a long time
I have been annoyed at how it was not working for Python3 in some cases.
The code was manually settign filters, but these would get overridden by
CPython test suites testing warnings. And the code said that there is no
CPython C-API to control it, which is just plain wrong.

So I changed that and it became possible to remove lots of
``ignore_stderr`` annotations in CPython test suites, and more
importantly, I can stop adding them for when running older/newer CPython
version with a suite.

*********
 Twitter
*********

I continue to be very active there.

`Follow @kayhayen <https://twitter.com/kayhayen?ref_src=twsrc%5Etfw>`_

And lets not forget, having followers make me happy. So do re-tweets.

Adding Twitter more prominently to the web site is something that is
also going to happen.

*************
 Help Wanted
*************

If you are interested, I am tagging issues `help wanted
<https://github.com/kayhayen/Nuitka/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22>`_
and there is a bunch, and very likely at least one *you* can help with.

Nuitka definitely needs more people to work on it.

***********
 Donations
***********

If you want to help, but cannot spend the time, please consider to
donate to Nuitka, and go here:

`Donate to Nuitka <http://nuitka.net/pages/donations.html>`_
