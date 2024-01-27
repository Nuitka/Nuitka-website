.. post:: 2023/03/13 13:05:25
   :tags: Python, compiler, Nuitka
   :author: Kay Hayen

#############################################
 Python 3.11 and Nuitka experimental support
#############################################

In my `all in with Nuitka </posts/all-in-with-nuitka.html>`__ post and
my first post `Python 3.11 and Nuitka </posts/python311-support.html>`__
and then progress post `Python 3.11 and Nuitka Progress
</posts/python311-progress.html>`__ , I promised to give you more updates
on Python 3.11 and in general.

So this is where 3.11 is at, and the TLDR is, experimental support has
arrives with Nuitka 1.5 release, follow develop branch for best support,
and 1.6 is expected to support new 3.11 features.

*************
 What is now
*************

The 1.5 release passes the CPython3.10 test suite practically as good as
with Python3.11 as with Python3.10, with only a handful of tests failing
and these do not seem significant, and it is expected to be resolved
later when making the CPython3.11 test suite working.

The 1.5 release now gives this kind of output.

.. code::

   Nuitka:WARNING: The Python version '3.11' is not officially supported by Nuitka '1.5', but an
   Nuitka:WARNING: upcoming release will change that. In the mean time use Python version '3.10'
   Nuitka:WARNING: instead or newer Nuitka.

Using develop should always be relatively good, it doesn't often have
regressions, but Python3.11 improvements will accumulate there until 1.6
release happens. Follow it there if you want. However, checking those
standalone cases that can be done, as many packages are not available
for 3.11 yet, I have not found a single issue.

******************
 What you can do?
******************

Try your software with Nuitka and Python3.11 now. Very likely your code
base is not using 3.11 specific features, or is it? If it is, of course
you may have to wait until develop catches up with new features and
changes in behavior.

In case you are wondering, how I can invest this much time into doing
all of what I do, consider becoming a `subscriber of Nuitka commercial
<https://nuitka.net/doc/commercial.html>`__, even if you do not need the
IP protection features it mostly has. All commonly essential packaging
and performance features are entirely free, and I have put incredible
amounts of works in this, and I need to now make a living off it, while
I do not plan to make Nuitka annoying or unusable for non-commercial
non-subscribers at all.

****************
 What was done?
****************

Getting all of the test suite to work, is a big thing already. Also a
bunch of performance degradations have been addressed. However right
now, attribute lookups and updates e.g. are not as well optimized, and
that despite and of course *because* Python 3.11 changed the core a lot
in this area.

*************
 The Process
*************

This was largely explained in my previous posts. I will just put where
we are now and skip completed steps and avoid repeating it too much.

In the next phase, during 1.6 development the 3.11 test suite is used in
the same way as the 3.10 test suite. Then we will get to support new
features, new behaviors, newly allowed things, and achieve super
compatibility with 3.11 as we always do for every CPython release. All
the while doing this, the CPython3.10 test suite will be executed with
3.11 by my internal CI, immediately reporting when things change for the
worse.

This phase is starting today actually.

******
 When
******

It is very hard to predict what will be encountered in the test suite.
It didn't look like many things are there, but e.g. exception groups
might be an invasive feature, otherwise I am not aware of too many
things at this point. It sure *feels* close now.

These new features will be relatively unimportant to the masses of users
who didn't immediately change their code to use 3.11 only features.

The worst things with debugging is that I just never know how much time
it will be. Often things are very quick to add to Nuitka, and sometimes
they hurt a lot or cause regressions for other Python versions by
mistake.

*******************************
 Benefits for older Python too
*******************************

I mentioned stuff before, that I will not repeat only new stuff.

Most likely, attribute lookups will lead to adding the same JIT approach
the Python 3.11 allows for now, and maybe that will be possible to
backport to old Python as well. Not sure yet. For now, they are actually
worse than with 3.10, while CPython made them faster.

******************
 Expected results
******************

Not quite good for benchmarking at this time. From the comparisons I
did, the compiled code of 3.10 and 3.11 seemed equally fast, allowing
CPython to catch up. When Nuitka takes advantage of the core changes to
dict and attributes more closely, hope is that will change.

So in a sense, using 3.11 with Nuitka over 3.10 actually doesn't have
much of a point yet.

I need to repeat this. People tend to expect that gains from Nuitka and
enhancements of CPython stack up. The truth of the matter is, no they do
not. CPython is now applying some tricks that Nuitka already did, some a
decade ago. Not using its bytecode will then become less of a benefit,
but that's OK, this is not what Nuitka is about.

We need to get somewhere else entirely anyway, in terms of speed up. I
will be talking about PGO and C types a lot in the coming year, that is
at least the hope. The boost of 1.4 and 1.5 was only be the start. Once
3.11 support is sorted out, ``int`` will be getting dedicated code too,
that's where things will become interesting.

*************
 Final Words
*************

So, this post is kind of too late. My excuse is that due to having
Corona, I did kind of close down on some of the things, and actually
started to do optimization that will lead towards more scalable class
code. This is also already in 1.5 and important.

But now that I feel better, I actually forced myself to post this. I am
getting better at this. Now back and starting the CPython3.11 test
suite, I will get back to you once I have some progress with that.
Unfortunately adding the suite is probably also a couple of days work,
just technically before I encounter interesting stuff.
