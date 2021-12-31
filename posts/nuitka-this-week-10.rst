.. post:: 2018/11/21 06:06:00
   :tags: Python, compiler, Nuitka, NTW
   :author: Kay Hayen

######################
 Nuitka this week #10
######################

.. contents::

**************************
 Communication vs. Coding
**************************

Recently it was a bit more tough to make that decision. First, there was
much going privately, with me ill, then child ill, and ill again, and
myself, and that made me have a much harder time to communicate about
incomplete things.

Even now, I am torn between fixing issues for 0.6.1 and doing this, but
I know that it will take at least one week, so I am missing the point,
if I wait for it more.

Bear in mind, that this is supposed to be a quick, not too polished, and
straight from top of my head, even if really a lot of content. But I
feel that esp. the optimization parts are worth reading.

**********
 Hotfixes
**********

There has been another hotfix, 0.6.0.6 and there ought to be one
0.6.0.7, at least on factory there is a bunch of stuff for it, but I
didn't actually do it yet. I was wandering between there will be a
release anyway, and the feeling that some of the material may cause
regressions, so I might skip on that really.

So for the most fixes, I suspect, develop is going to be the way until
next week.

**********************************
 Google Summer of Code for Nuitka
**********************************

Nobody has stepped up, which means it will not happen unfortunately.
This would be your last chance to step up. I know you will feel not
qualified. But I just need a backup that will help a student around
obstacles in case I go missing. Contact me and I will be very happy.

********************
 Pythran and Nuitka
********************

As suggested by @wuoulf (Wolf Vollprecht) we had a meeting at the side
of the PyCon DE 2018 conference in Karlsruhe, abusing the C++ regular
table as a forum for that, which was a very nice experience.

First of all, Wolf is so much more knowledgeable about AnaConda and
could point out to me, very important stuff, not the least, that
AnaConda contains its own compiler, which I have successfully used
since, to first add easier installation instructions for Windows, and
second, to successfully statically link with LTO on Linux amd64. Both of
which are important for me.

But for Pythran which is limited Python, specialized to translate Numpy
API to C++, we showed each other, Nuitka and Pythran details, and
somehow in my mind a plan formed how Nuitka could use the Pythran tricks
long term, and mid term, how it could include a plugin that will allow
to integrate with Pythran compilation.

This was a huge success.

******************
 Performance Work
******************

Adding specialized object operations
====================================

See last week, this has seen more completion. Both `+` and `+=` are more
or less covered for the selected subset. The CPython test suites were
initially not finding uses, but with more and more optimization phase
improvements, it challenges code generation with missing ones, and then
I added them more and more.

Controlflow Descriptions
========================

Shapes were added for the `+` and `<` operation so far, but didn't
influence anything else really but code generation, but of course they
should also impact optimization phase.

So the query for type shape has been enhanced to return not only a type
shape saying that `int+float -> float`, but also now an object that
describes impact on control flow of the program. This can then say e.g.
that this doesn't execute arbitrary code, and that it does not modify
input values, things used in the code generation to avoid error checks,
and in the optimization to not have to mark things as unknown.

Preparations for comparison operations
======================================

So optimization now also has proper type shape functions for the `<` and
the warnings when they fail to know what to do for concrete types. This
allows to actually remove checks, but so far this wasn't exposed for
neither `+` or for `<`. Doing this eliminates the exception check for
the operation part, where previously it was done if anything in the
expression could raise.

Specializing the rich comparisons helper codes is the next step, but so
far I didn't quite get to it yet, but it has been started.

Comparison Conditions
=====================

Preparing `<` optimization for the loop, I noticed that `not` was
optimized for `in` to become `not in`, and also `is` to become `is not`,
etc. but for comparisons, where we can not the result is of bool shape,
we can now also switch `not <` to `>=` and `not =` to `!=` of course.

And since our reformulation of `while a < b` ends up having a statement
like `if not a < b: break` as part of its re-formulation, that is again
one step closer to optimizing my example loop.

Local variable escaping
=======================

Much to my shock, I noticed that the code which is responsible to handle
escaping control flow (i.e. unknown code is executed), was not only
doing what it was supposed to do, i.e. mark closure variables as
unknown, but more or less did it for all local variables with Python3.

Fixing that allows for a lot more optimization obviously, and makes my
test find missing ones, and even bugs in existing ones, that were
previously hidden. A good thing to notice this regression (was better
once), now that I am looking at concrete examples.

One noticeable sign was that more of my tests failed with warnings about
missing code helpers. And another that in my while loop with `int`
increase, it now seems as if Python3 is good. For Python2, the "int or
long" shape will need dedicated helpers. That is because `ìnt + int`
becomes either `int` or `long` there, where Python3 only has `long` but
renamed it `int`.

Benchmarks Missing
==================

Speedcenter got repaired, but I need to add the loop examples I am using
as test cases before next release, so I can show what Nuitka 0.6.1 will
have achieved or at least have improved somewhat already.

But currently these examples only serve as input for general
improvements that then take a lot of time, and don't have immediate
impact on their own.

Still would be good to see where Nuitka is standing after each one.

****************
 Static Linking
****************

So static linking works now, provided it's not a `pyenv` crappy
`libpython.a` but one that can actually work. I got this to work on
Linux and using the Conda CC, even LTO will work with it. Interestingly
then linking is noticely slow, and I bet `ccache` and the likes won't
help with that.

I am interested to see what this means for performance impact. But it
will allow to address issues, where embedded CPython run time is plain
slower than the one that lives in the python binary. For acceleration
this is great news.

**********
 Conda CC
**********

Using Conda CC by default as a fallback in `--mingw` mode on Windows is
something that was easy to add. So when no other `gcc` is found, and
MSVC is not tried in this mode, and the right directory is added to
`PATH` automatically, with Anaconda, things should now be smoother. It
has also its own `libpython.a`, not sure yet if it's a static link
library, that would be fantastic, but unlike standard MinGW64 we do not
have to roll our own at least.

I will try with `--lto` eventually though and see what it does. But I
think static linking on Windows is not supported by CPython, but I am
not entirely sure of that.

****************************
 Annotations Future Feature
****************************

Found a 3.7 feature that is not covered by the test suite, the
`__future__` flag `annotations` wasn't working as expected. In this,
strings are to be used for `__annotations__` where they show up (many
are ignored simply) and that requires an `unparse` function, going from
parsed ast (presumably it's still syntax checked) back to the string,
but that was only very hard to get at, and with evil hackery.

For 3.8 a bug fix is promised that will give us the string immediately,
but for now my hack must suffice.

***********
 MSI files
***********

Following the 3.7.1 release, there are MSI files again, as the
regression of 3.7.0 to build them has been fixed in that release. The
MSI files will work with 3.7.0 also, just the building was broken.

*********
 Overall
*********

So 0.6.1 is in still in full swing in terms of optimization. I think I
need to make a release soon, simply because there is too much
unreleased, but useful stuff already.

I might have to postpone my goal of C int performance for one example
loop until next release. No harm in that. There already are plenty of
performance improvements across the board.

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

`Donate to Nuitka </pages/donations.html>`_
