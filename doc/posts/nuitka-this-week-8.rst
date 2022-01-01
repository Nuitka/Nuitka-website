.. post:: 2018/10/02 06:05:00
   :tags: Python, compiler, Nuitka, NTW
   :author: Kay Hayen

#####################
 Nuitka this week #8
#####################

.. contents::

********************************
 Public / Private CI / Workflow
********************************

.. note::

   I wrote this as part of a discussion recently, and I think it makes
   sense to share it here. This is a lot text though, feel free to skip
   forward.

Indeed I have a private repo, where I push and only private CI picks up.
Based on Buildbot, I run many more compilations, basically around the
clock on all of my computers, to find regressions from new optimization
or codegen changes, and well UI changes too.

Public CI offerings like Travis are not aimed at allowing this many
compilations. It will be a while before public cloud infrastructure will
be donated to Nuitka, although I see it happening some time in the
future. This leaves developers with the burden to run tests on their own
hardware, and never enough. Casual contributors will never be able to do
it themselves.

My scope is running the CPython test suites on Windows and Linux. These
are the adapted 26, 27, 32, 33, 34, 35, 36, 37 suites, and also to get
even more errors covered, they are ran with mismatching Python versions,
so a lot of exceptions are raised. Often running the 36 tests with 37
and vice versa will extend the coverage, because of the exceptions being
raise.

On Windows I compile with and without debug mode, x86 and x64, and it's
kind of getting too much. For Linux I have 2 laptops in use, and an ARM
CuBox bought from your donations, there it's working better, esp. due to
``ccache`` being used everywhere, although recent investigations show
room for improvement there as well.

For memory usage I still compile mercurial and observe the memory it
used in addition to comparing the mercurial tests to expected outputs
its test suite gives. It's a sad day when Mercurial tests find changes
in behavior, and luckily that has been rare. Running the Mercurial test
suite gives some confidence in the thing not corrupting data it works
with without knowing.

Caching the CPython outputs of tests to compare against is something I
am going to make operational these days, trying to make things ever
faster. There is no point to re-run tests with Python, just to get at
its output, which will typically not change at all.

But for the time being, ``ccache.exe`` and ``clcache.exe`` seem to have
done wonders for Windows too, but I will want to investigate some more
to avoid unnecessary cache misses.

Workflow
========

As for my workflow with Nuitka, I often tend to let some commits settle
in my private repo only until they become trusted. Other times I will
make bigger changes and put them out to factory immediately, because it
will be hard to split up the changes later, so putting them out makes it
easier.

I am more conservative with factory right after telling people to try
something there. But also I break it on purpose, just trying out
something. I really consider it a private branch for interacting with me
or public CI. I do not recommend to use it, and it's like a permanent
pull request of mine that is not ever going to be finished.

Then on occasions I am making a sorting of all commits on factory and
split it into some things that become hotfixes, some things that become
current pre-release, and other things that will remain in that proving
ground. That is why I typically make hotfix and pre-release at the same
times. The git flow suggests doing that and it's easy, so why not. As a
bonus, develop is then practically stable at nearly all times too, with
hardly any regressions.

I do however normally not take things as hotfixes that are on develop
already, I hate the duplication of commits. Hotfixes must be small and
risk free, and easy to put out, when there is any risk, it definitely
will be on develop. Nuitka stable typically covers nearly all grounds
already. No panic needed to add missing stuff and break others.

Hunting bugs with bisect
========================

For me the git bisect is very important. My private commit history is
basically a total mess and worthless, but on factory I am making very
nice organized commits that I will frequently amend, even for the random
PyLint cleanup. This allows me when e.g. one test suddenly says
"segfault" on Windows to easily find the change that triggers it, look
at C code difference, and spot the bug introduced, then amend the commit
and be done with it.

It's amazing how much time this can save. My goal is to always have a
workable state which is supposed to pass all tests. Obviously I cannot
prove it for every commit, but when I know it to not be the case, I tend
to make rebases. At times I have been tempted and followed up on
backward amending develop and even stable.

I am doing that to be sure to have that bisect ability, but fortunately
it's rare that kind of bug occurs, and I try not to do it.

Experimental Changes
====================

As with recent changes, I sometimes make changes with the
``isExperimental()`` marker, activating breaking changes only gradually.
The C ``bool`` type code generation has been there for months in a
barely useful form, until it became more polished, and always guarded
with a switch, until one day for 0.6 finally I changed it, and made the
necessary fixes retroactively before that switch, to make it work while
that was still in factory.

Then I will remove the experimental code. I feel it's very important and
even ideal to be able to always compare outputs to a fully working
solution. I am willing to postpone some cleanups until later date as a
price, but when then something in my mind tells me again "This cannot
possibly have ever worked"... a command line flag away, I have the
answer to compare, plus, that includes extra changes happened in the
meantime, they don't add noise to diff outputs of generated C code for
example.

Then looking at that diff, I can tell where the unwanted effect is, and
fix all the things, and that way find bugs much faster.

Even better, if I decide to make a cleanup action as part of making a
change more viable to execute, then I get to execute it on stable
grounds, covered by the full test suite. I can complete that cleanup,
e.g. using variable identifier objects instead of mere strings was
needed to make "heap generators" more workable. But I was able to put
that one to active before "heap generators" was ever fully workable, and
complete it, and actually reap some of its benefits already.

Hardware
========

Obviously this takes a lot of hardware and CPU to be able to compile
this much Python code on a regular basis. And I really wish I could add
one of the new AMD Threadripper 2 to the mix. Anybody donating one to
me? Yes I know, I am only dreaming. But it would really help the cause.

*******************
 Milestone Release
*******************

So the 0.6 is out, and already a hotfix that addresses mostly use cases
of people that didn't work. More people seemed to have tried out 0.6.0
and as a result 0.6.0.1 is going to cover a few corner cases. So far I
have not encountered a single regression of 0.6.0, but instead it
contained ones for 0.5.33 which did have one that was not easy to fix.

So that went really smooth.

***********
 UI rework
***********

The UI needs more work still. Specifically that packages do not
automatically include all stuff below them and have to be specified by
file path instead of by name, is really annoying to me.

But I had delayed 0.6 for some UI work, and the quirks are to remain
some. I will work on these things eventually.

************
 Benchmarks
************

So I updated the website to state that PyStone is now 312% faster, from
a number that was very old. I since then ran it with an updated version
for Python3, and it's much less there. That is pretty sad.

I will be looking into that for 0.6.1 release, or I will have to update
the wording to provide 2 numbers there, because it seems for Python3
performance with Nuitka it might be misleading.

Something with unicode strings and in-place operations is driving me
crazy. Nuitka is apparently slower for that, and I can't point where
that is happening exactly. It seems internally unicode objects are maybe
put into a different state from some operations, which then making
in-place extending in realloc fail more often, but I cannot know yet.

********************
 Inplace Operations
********************

So more work has been put into those, adding more specialization, and
esp. also applying them for module variables as well. CPython can do
that, and actually is giving itself a hard time about it, and Nuitka
should be doing this much clever with its more static knowledge.

But I cannot tell you how much scratching my head was wasted debugging
that. I was totally stupid about how I approached that, looking from the
final solution, it was always easy. Just not for me apparently.

***************
 New use cases
***************

Talked about those above. So the top level ``logging`` module of your
own was working fine in accelerated mode, but for standalone it failed
and used the one from standard library instead. That kind of shadowing
happened because Nuitka was going from module objects to their names and
back to objects, which are bad in case of duplicates. That is fixed for
develop, and one of those risk cases, where it cannot be a hotfix
because it touched too much.

Then pure Python3 packages need not have ``__init__.py`` and so far that
was best working for sub-packages, but after 0.6.0.1 hotfix, now it will
also work for the main module you compile to be that empty.

*******************
 Tcl/Tk Standalone
*******************

So instructions have been provided how to properly make that work for
Python standalone on Windows. I have yet to live up to my promise and
make Nuitka automatically include the necessary files. I hope to do it
for 0.6.1 though.

******************
 Caching Examined
******************

So I am looking at ccache on Linux right now, and found e.g. that it was
reporting that ``gcc --version`` was called a lot at startup of Scons
and then ``g++ --version`` once. The later is particularly stupid,
because we are not going to use g++ normally, except if gcc is really
old and does not support C11. So in case a good one was found, lets
disable that version query and not do it.

And for the gcc version output, monkey patching scons to a version of
getting that output that caches the result, removes those unnecessary
forks.

So ``ccache`` is being called less frequently, and actually these
``--version`` outputs appears to actually take measurable time. It's not
dramatic, but ``ccache`` was apparently getting locks, and that's worth
avoiding by itself.

That said, the goal is for ``ccache`` and ``clcache`` to make them both
report their effectiveness of cache usage after the end of a test suite
run. That way I am hoping to notice and be able to know, if caching is
used to its full effect.

*********
 Twitter
*********

I continue to be very active there. I put out a poll about the comment
system, and disabling Disqus comments as a result, I will focus on
Twitter for web site comments too now.

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

*******
 Plans
*******

Working on the 0.6.1 release, attacking more in-place add operations as
a first goal, and now turning to binary operations, I am trying to shape
how using different helper functions to different object types looks
like. And to gain performance without C types. But ultimately the same
issue will arise there, what to do with mixed input types.

My desire is for in-place operations to fully catch up with CPython, as
these can easily loose a lot of performance. Closure variables and their
cells are another target to pick on, and I feel they ought to be next
after module ones are now working, because also their solution ought to
be very similar. Then showing that depending on target storage, local,
closure, or module, is then faster in all cases would be a goal for the
0.6.1 release.

This feels not too far away, but we will see. I am considering next
weekend for release.

***********
 Donations
***********

If you want to help, but cannot spend the time, please consider to
donate to Nuitka, and go here:

`Donate to Nuitka </pages/donations.html>`_
