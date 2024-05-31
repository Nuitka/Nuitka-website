.. post:: 2023/02/18 12:29:24
   :tags: Python, compiler, Nuitka
   :author: Kay Hayen

#################################
 Python 3.11 and Nuitka Progress
#################################

In my `all in with Nuitka </posts/all-in-with-nuitka.html>`__ post and
my first post `Python 3.11 and Nuitka
</posts/python311-support.html>`__, I promised to give you more updates
on Python 3.11 and in general. So this is where 3.11 is at, and the TLDR
is, experimental support is coming with Nuitka 1.5 release.

*************
 What is now
*************

Currently Nuitka 1.4 contains already some preparations for 3.11
support, but also from the feedback I had read, on how Nuitka has lost
its performance lead over the releases, a huge amount of catching up on
the quality and depth of integration, was put onto the plate, and so
that became a large part of the 1.4 focus.

These preparations mostly addressed frames, unified separate code
generation for them, and since with 3.11 generators frames were far too
buggy, this had to be continued, and interestingly many frame issues
were solved by some great unification right after 1.4 release for 1.5
develop.

And from here, most frame issues got debugged and fixed. This is the
area where 3.11 had the biggest impact on Nuitka internals.

The 1.5 development release now gives this kind of output.

.. code::

   Nuitka:WARNING: The Python version '3.11' is not officially supported by
   Nuitka:WARNING: Nuitka '1.5rc7', but an upcoming release will change that. In
   Nuitka:WARNING: the mean time use Python version '3.10' instead or newer
   Nuitka:WARNING: Nuitka.

Using develop should be good. But I expect to be better with every
pre-release until 1.5 happens. Follow it there if you want.

******************
 What you can do?
******************

Not a lot yet, as a mere mortal, what you can and should do is to
consider becoming a `subscriber of Nuitka commercial
<https://nuitka.net/doc/commercial.html>`__, even if you do not need the
IP protection features it mostly has. All commonly essential packaging
and performance features are entirely free, and I have put incredible
amounts of works in this, and I need to now make a living off it.

Working on 3.11 support, just so tings then continue to work, mostly on
my own deserves financial support. Once a year, for weeks on end, I am
re-implementing features that a much larger collective of developers
came up with.

But don't get me wrong. This may sounds like complaining here. Not at
all. I love these things. I hate to be under some kind of time pressure
though, but it seems that is coming to an end, so it's all good now.

****************
 What was done?
****************

So the "basic" tests of Nuitka are finally passing. That is by itself a
huge step, and the now work on the CPython3.10 test suite, has been
started to be executed with Python 3.11, and fixes are applied.

Doing that, still some bigger issues were still found, e.g. uncompiled
frames as the parent of compiled frames, when inspected, did not
automatically provide a ``f_back``, these now have to created on the
fly. This sort of things, which are not commonly observed by code.

Esp. the usual trouble makers, ``test_generators``, ``test_coroutines``,
and ``test_asyncgen`` (with one test part as an exception) are passing.
Honestly these are always the most scary to me. Debugging coroutines
using asyncgen is a fairly large chunk of my time spent on Nuitka in
recent years.

Compiled frames appear to be not entirely correctly seen for tracebacks
and stacks when uncompiled code looks upward, but that seems negligible
right now.

Up to ``test_inspect`` things appear to be working fine, and there is
some kind of TODO list now, that I maintain on the roadmap document. I
add TODOs there, e.g. because I had to disable attribute optimization
with Python3.11 so that is going to harm performance and should be
revisited before claiming full support.

As for ``inspect`` module, there will be more functions that need monkey
patching, esp. related to frames, e.g. ``getframeinfo`` has no tolerance
for the lack of bytecode in compiled function and their frames.

*************
 The Process
*************

This was largely explained in my previous post. I will just put where we
are now and skip completed steps and avoid repeating it too much.

The current phase is to run the CPython 3.10 test suite compiled with
3.11 and compare its results to running with plain 3.11, and expect it
to be the same. It is normal for CPython 3.10 tests to fail with 3.11,
and this does several things.

Test failures of 3.11 with 3.10 code actually give new test coverage. It
has happened in previous new Python releases, that only then it became
apparent that there were slight incompatibilities in exceptions, etc.

Also now a test may passes where it should not, i.e. 3.11 changed
behavior and now Nuitka still follows 3.10 behavior. So maybe a new
check is done or something like that, and Nuitka needs a version guarded
change that also makes it behave the same with 3.11 version. But of
course, when using 3.10 it has to retain the older behavior still.

The other thing, is when Python 3.11 passes, but Nuitka is not.
Typically then Nuitka has some sort of change missing to the internal
codes, often only a changed error message, exception type, etc. but
sometimes this can be also a bigger thing.

During this phase it is hard to know where we stand. I do not really
want to do repeated analysis. So e.g. when the exception for using a
non-context manager in a ``with`` statement fails, I am not really
interested to see how many other tests are failing because of that or
other things. I am going to fix that first *and only then* I will look
what the next failure is.

Since I will get to fix *all* the things, anyway, I tend to address most
of the issues I find immediately and delay further executing of the test
suite. Only when I understand the issue clearly enough and see that it
will take a lot of time for a corner case, then I will add fixing it to
the roadmap.

This I am doing e.g. with the single test part failure in
``test_asyncgen``, because I suspect, that some change in 3.11 has
happened, or that I will revisit the topic in the 3.11 test suite, which
often has more dedicated tests to highlight changes. The one not good
with Nuitka right now does not look important, nor easy to analyze.

In the next phase, the 3.11 test suite is used in the same way. Then we
will get to support new features, new behaviors, newly allowed things,
and achieve super compatibility with 3.11 as we always do for every
CPython release. All the while doing this, the CPython3.10 test suite
will be executed with 3.11 by my internal CI, immediately reporting when
things change for the worse.

This phase has not even started however. But probably results of it will
be in 1.6 I would assume now.

**********************
 Intermediate Results
**********************

Once the Python 3.11 more or less well passed the 3.10 test suite
without big issues, experimental support for it will be proclaimed and
1.5 shall be released. The warning from above will be given, but the
error that 1.4 gave you will cease, and come back for 3.12 probably.

******
 When
******

Very hard to predict. It *feels* close now. Supporting existing Nuitka
is also a side tracking thing, that makes it unclear how much time I
will have for it.

And the worst things with debugging is that I just never know how much
time it will be. I have spent almost a day staring at debugging traces
for the coroutine code, before these worked finally. And during that
time it didn't feel like progressing at all.

I think, look back at Python changes since 2.6, which was the first
thing Nuitka supported, and still does btw, 3.5 and coroutines, 3.6 and
asyncgen, and then 3.10 and ``match`` statements, the 3.11 release will
probably have been the hardest.

*******************************
 Benefits for older Python too
*******************************

I mentioned stuff before, that I will not repeat only new stuff. So the
frame changes caused me to solve most of the issues by doing cleanups
and refactoring that allowed for enhancements present in 1.4 and coming
to 1.5 some more, covering generators as well.

Most likely, attribute lookups will gain the same JIT approach the
Python 3.11 allows for now, and maybe that will be possible to backport
to old Python as well. Not sure yet. For now, they are actually worse
than with 3.10, while CPython made them faster. Not quite good for
benchmarking at this time.

******************
 Expected results
******************

I need to repeat this. People tend to expect that gains from Nuitka and
enhancements of CPython stack up. The truth of the matter is, no they do
not. CPython is now applying some tricks that Nuitka already did, some a
decade ago. Not using its bytecode will then become less of a benefit,
but that's OK, this is not what Nuitka is about.

We need to get somewhere else entirely anyway, in terms of speed up. I
will be talking about PGO and C types a lot in the coming year, that is
at least the hope. The boost of 1.4 will only be the start. Once 3.11
support is sorted out, ``int`` will be getting dedicated code too,
that's where things will become interesting.

*************
 Final Words
*************

Look ma, I posted about something that is not complete. The temptation
to just wait until I finish it was so huge. But I resisted successfully.
