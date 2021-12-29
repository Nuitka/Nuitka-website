.. post:: 2019/05/12 11:07:00
   :tags: Python, compiler, Nuitka, NTW
   :author: Kay Hayen

######################
 Nuitka this week #13
######################

.. contents::

**************************
 Communication vs. Coding
**************************

Communication was a lot more, just not these postings. Nuitka has
ventured into important realms.

First, active developers have joined Nuitka. Second, as a consequence of
the later, Nuitka indeed was able to participate with a insanely
powerful offering of 4 mentors.

This meant, that a lot of technical or project management debt hat to be
dealt with, and there was no time to make this kind of posting. This is
probably good news on all fronts, except that I feel they are missing,
and am glad to be able to resume them.

****************************
 Google Summer of Code 2019
****************************

My Experience
=============

This was the most crazy ride and fun. Became the admin of an active
sub-organisation under the PSF umbrella for GSoC 2019. So shortly after
the announcement of the project lists, students flooded in, and starting
working on things right away as early as February.

They were working hard to prove themselves and get to know Nuitka,
asking many questions, with us having lots of email interviews, and even
a lot of video calls, where I personally talked to people about ideas.

This happened simultaneously to more experienced developers joining the
project as well, making very important contributions.

This basically meant, that many days 90%-100% of my Nuitka time was for
communication or working off technical debts I knew there were, or for
preparing things, I want to have with multiple people working on the
code base. This will be detailed in other sections.

Accepted Students
=================

All of this has paid of in that we now have 2 really good students to
work on 2 Nuitka projects over the summer. Let's welcome Batakrishna and
Tommy in separate posts. They will introduce themselves and what they
are going to do shortly, in separate posts.

Lets just say, this is fantastic news. We had so many good applications
and its a shame, but we knew right away, not everybody who deserved it
could be picked. But this is going to be a good chance for us to get to
be open and welcoming to new people.

*******************
 Optimization Work
*******************

Core Stuff
==========

So, the 0.6.3 release (btw. on Windows, be sure to use the 0.6.3.1
hotfix), which was made as a consolidation effort to get the good work
of mostly other people out, didn't contain much optimization work for
the core, as that is still my thing.

However, this changed a lot. An idea that came to my mind for how to do
the massive amounts of specialized helpers needed beyond `+` and `+=`,
with which I had started for prior releases. And that is to use Jinja2
based templates for C, to generate the code.

This was an important idea. Took a while, but soon the manual code for
``+`` was already replaced with generated code, fixing a few bugs by the
way, and from there, the generation was expanded to cover ``*`` as well.

Currently, support for the 3 (!) different kinds of additions
(``TrueDiv`` and ``FloorDir`` as well as Python2 default division,
dubbed ``OldDiv`` in Nuitka was added along with ``-`` .

The reason, ``+`` and ``*`` were done first, is that they have special
treatment for sequences, using ``sq_concat`` and ``sq_repeat``, where
the other operations will be more straightforward, e.g. ``nb_subtract``
(``-``) has a lot types supporting it and that makes those the easy
cases.

I am saving a deeper explanation of 3 things we will need for the next
time. Basically we need optimization of these things at compile time,
and that is getting there, and code to use in the backend, and that is
getting there, and a third thing, that is to use optimization knowledge
to apply the special code as much as possible, and that is not yet fully
there.

Faster Windows Dependencies
===========================

This is going to excite Windows users. After Orsiris de Jong had done a
replacement for dependency walker that is faster, this had remained in
an experimental status, just due to lack of time.

Recently however, I felt there is more time, after GSoC student
selection has happened, and that I could finally work a bit on open
issues like this. And when I wrote a dedicated tool, to analyse
dependences with either technology to compare the results, I found that
dendency walker founds a lot more things.

That was a turn down, but turns out, nothing it finds is stuff that
should not be on the white list. In fact, it's all core Windows things,
and from the ``System32`` folder. That made me question, why we take
anything from there (except maybe ``PythonXY.dll``) at all, and after
that change the performance changed dramatically.

The dependency walker now finishes a file in milliseconds. Actually the
``pefile`` is now slow (surely it ought to be compiled), and takes some
seconds, for a file. That is amazing, and has lead to me to remove the
parallel usage, and since ``pefile`` allows for perfect caching, and is
Free Software, we will probably keep it.

This will address a widespread complaint of many Windows users of the
standalone mode. This is now a relatively unnoticable part of the
overall experience.

Currently I need to finish off some remaining problems with it, before
putting it out in the wild. Getting this into a release will solve many
newcomer issues.

*********************
 Nuitka Organisation
*********************

Esp. for Google Summer of Code, Nuitka has sought and found mentors,
some of which are highly experienced for the task. I will let them
decide and write their own introduction, but I feel really blessed by
them helping me out in my desperate calls for help. Without them,
neither could Nuitka participate, nor could it even overachieve as much
as it does.

Therefore I welcomed Kamran and Vaibhav into the organisation and they
are excited to work the the 2 accepted students, that are also added.

*************
 Plugin Work
*************

On the ``jorj`` branch there is a lot of work from Jorj that aims at
adding support for more of the beasty stuff with hidden dependency and
plugin needs.

He is also working at run time tracing of your program to be translated
to automatic imports of just that. I am going to highlight this later,
once I manage to cherry-pick the release ready parts from it for the
next release.

But this definitely awesome stuff, and going to make Nuitka very easy to
use for some people, even with stranger software.

************
 Opening Up
************

This is also a teaser. But we did so much work for the 0.6.3 release to
make sure information is there, and things are accessible and changeable
by everyone, or even the pre-commit hook that I am very proud of.

But I shall save this for next week, otherwise it will be too much new
information.

*********
 Twitter
*********

I continue to be active there, although often I fall prey to of not
wanting to talk about unfinished things. On Twitter of all things.

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
