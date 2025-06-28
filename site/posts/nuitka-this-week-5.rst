.. post:: 2018/08/24 12:55:00
   :tags: Python, compiler, Nuitka, NTW
   :author: Kay Hayen

#####################
 Nuitka this week #5
#####################

.. contents::

*****************
 Goto Generators
*****************

Finished. Done. Finally.

Benchmarking was exciting. One program benchmark I had run in the past,
was twice as fast than before, showing that the new implementation is
indeed much faster, which is fantastic news.

Creating generator expressions and using them both got substantially
faster and that is great.

It took me a fair amount of time to debug coroutines and asyncgen based
on the new goto implementation. But the result is really good, and a
fair amount of old bugs have been fixed. There always had been a
segfault with asyncgen test that now has been eradicated.

One major observation is now, with only one C stack, debugging got a lot
easier before, where context switches left much of the program state not
reachable.

************
 Benchmarks
************

Posted this one Twitter already:

`Nuitka Speedcenter Builtin sum with generator
<https://speedcenter.nuitka.net/constructs/construct-builtinsumwithgenerator.html>`_

That one construct test has been a problem child, where Nuitka was
slower than CPython 2.x, and very little faster than 3.x, and now with
goto generators finally has become consistently faster.

I will explain what you see there in the next issue. The short version
is that there is code, in which for one run, one line is used, and in
another the other line is used, and then the "construct" is measure that
way, by making the delta of the two. That construct performance is then
compared between Python and Nuitka.

So if e.g. Nuitka is already better at looping, that won't influence the
number of making that ``sum`` call with a generator expression.

The alternative line uses the generator expression, to make sure the
construction time is not counted. To measure that, there is another
construct test, that just creates it.

`Nuitka Speedcenter Generator Expression Creation
<https://speedcenter.nuitka.net/constructs/construct-generatorexpressioncreation.html>`_

This one shows that stable Nuitka was already faster at creating them,
but that the develop version got even faster again. As creating
generator objects became more lightweight, that is also news.

There are constructs for many parts of Python, to shed a light on how
Nuitka fares for that particular one.

*********
 Holiday
*********

In my 2 weeks holiday, I will try and focus on the next big thing, C
types, something also started in the past, and where recent changes as
part of the heap storage, should make it really a lot easier to get it
finished. In fact I don't know right now, why my ``bool`` experimental
work shouldn't just prove to be workable.

I am not going to post a TWN issue next week, mostly because my home
servers won't be running, and the static site is rendered on one of
them. Of course that would be movable, but I won't bother.

I am going to post a lot on Twitter though.

********************
 Static Compilation
********************

There is a GitHub issue where I describe how pyenv on macOS ought to be
possible to use, and indeed, a brave soul has confirmed and even
provided the concrete commands. All it takes now is somebody to fit this
into the existing caching mechanism of Nuitka and to make sure the
static library is properly patched to work with these commands.

Now is anyone of you going to create the code that will solve it for
good?

*********
 Twitter
*********

Follow me on twitter if you like, I will post important stuff as it
happens there:

`Follow @kayhayen <https://twitter.com/kayhayen?ref_src=twsrc%5Etfw>`_

And lets not forget, having followers make me happy. So do re-tweets.

**********
 Hotfixes
**********

And there have been yet again more hotfixes. Some are about coroutine
and asyncgen corruptions for closes of frames. Multiprocessing plugin on
Windows will work in all cases now.

Noteworthy was that the "0.5.32.6" was having a git merge problem on the
cherry-pick that git didn't tell me about, leading to crashes. That made
it necessary to push an update right after. I was confused that I didn't
get a conflict, because there was one. But I am to blame for not
checking the actual diff.

*************
 Bug Tracker
*************

The next release will make GitHub the official tracker for Nuitka
issues. I am working down the issues on the old tracker. The web site
already pointed users there for a while, and I was set on this for some
time, but yesterday I focused on taking action.

Basically what won me over is the easier templating of issues and pull
requests that would have been possible with Roundup, but never happened.
Also the OpenID integration that bugs.python.org has, never became
available to me in a ready usable form.

***************
 Issue Backlog
***************

Finishing goto "generators allowed" for around 10 issues to be closed
alone, and I went over things, and checked out some stale issues, to see
if they are dealt with, or pinging authors. I spent like half a day on
this, bring down the issue count by a lot. Tedious work, but must be
done too.

Also my inbox got a fair amount of cleanup, lots of issues pile up
there, and from time to time, I do this, to get things straight. I
raised issues for 2 things, that I won't be doing immediately.

But actually as issues go, there really very little problematic stuff
open right now, and nothing important really. I would almost call it
issue clean.

*************
 Help Wanted
*************

If you are interested, I am tagging issues `help wanted
<https://github.com/kayhayen/Nuitka/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22>`_
and there is a bunch, and very like one you can help with.

Nuitka definitely needs more people to work on it.

*******
 Plans
*******

The goto generator work could be released, but I want to make the
compile all the world test before I do so. It is running right now, but
I will not complete before I leave. Also I do not want to get regression
reports in my holiday, and goto generators along with heap storage, mean
there could be some.

I am going to work on C types now. There is a few closing down actions
on what I observed doing goto generators. There are a few easy ways to
get even slightly better performance, definitely smaller code out of
generators. Not sure if I go there first, or for the C types work
directly. I often like to get these kind of observations dealt with more
immediately, but I don't want to spend too much quality time on it.

***********
 Donations
***********

As I have been asked this, yes, you can donate to Nuitka if you wish to
further its development. Go here:

`Donate to Nuitka </pages/donations.html>`_
