###########################
 My Europython 2013 report
###########################

Back from Europython 2013 in Florence for a while now. I had a
presentation about my `Python compiler Nuitka </pages/overview.html>`_.
You can watch the Video on Youtube. I believe it's absolutely worth your
time. I was not doing a lot of "why" at all now, only "what", and demo
times, and answering questions:

.. youtube:: BDjXZY_8d58

The talk went really well. I believe one can clearly see that I felt
really good and at ease. The state presented is very good and progress -
there was a lot, so that was great. The `slides
</pr/Nuitka-Presentation-PyCON-EU-2013.pdf>`__ of the talk may also be
interesting.

And it definitely raised a lot of interest.

Last years talk is also there. You can (maybe) see that I was 20kg more
weight then, and also *much* more excited, at least initially.
Background: I was surprised then that Guido van Rossum was attending the
talk, plus I was kind of not in the state of this year, the confidence
that people should believe, that things will work after that, was not
yet there. I knew it, but standing in front of a croud and saying, look
I am attempting what you consider impossible, or even have failed at, is
not easy:

.. youtube:: ZDHkla5rllg

There are also the `slides
</pr/Nuitka-Presentation-PyCON-EU-2012.pdf>`__ of that talk which may
also be interesting, but of course are outdated somewhat now.

************************
 Years make differences
************************

So yeah, the progress happened since 2012 made a difference. Nuitka has
proven things. Let's see what this year does to it. I would hope for
real type inference optimization and portable mode to be there next
year.

Consider that is the a *spare time effort*. Lots of people lauded it for
the out of the box experience, and how it just works. That's right. I
put a lot of focus on stability, correctness, and ease of use. In fact,
since my return, I have mostly worked on the feedback I got in that
domain.

But for the relatively small amount of time I can invest (outside of
holidays), it's make very fast progress.

*************************
 Out of the box thinking
*************************

The feedback during the conference was great. While Nuitka is not yet
seeing a lot of users, and not as many contributions or donations as I
would hope for, but that's kind of expected with my out of the box
thinking there.

Few people at Europython really need a Python compiler. The most
important exception are scientific people, doing number crunching. And I
made some interesting contacts there.

Since my return, I have been receiving a bunch of bug reports. Some of
which were unfortunately regressions of 0.4.4, and these got fixed in
two hotfix releases. Currently 0.4.4.2 is released, and contains a huge
amount of fixes, mostly stuff found by the surge new users.

But I deserved that, having said that I didn't have to do hotfixes for a
while now.

**********
 Florence
**********

Such a lovely place, and so lovely people. It's a tourist place, true,
but it's very open minded. The food is extremely good. And going from
the conference hotel straight over to the river to meet up and have a
few beers was very comfortable for after-conference stuff.

Now that I have been there 2 times, and the conference even 3 times,
it's moving on, to Berlin, which I sort of regret. Knowing the place
somewhat definitely is an advantage by itself.

*******************
 Python Revolution
*******************

One thing that came to my mind during the conference, witnessing the
large amount of non-satisfaction, was that the community is fed up with
the leadership. Questioned about lack of Python3 adoption, a PSF guy in
his presentation said they were 3 years into a 5 years plan, and got
interrupted by laughter.

It may be about time, somebody actually gets up, removes the GIL and has
a Python2.8 that is compatible. Obviously that's much more useful. It
could be a Python3.x with compatibility names of modules, ``print``
statement, and ``dict.iteritems`` added, probably also making some of
the ``unicode`` mess more harmless, and providing ``unicode`` and
``long`` built-in names.

Considering that I have in fact been playing with the idea of forking
CPython top versions, to add things, that would allow Nuitka to work
better with it, that could be a staging ground, where such changes are
nurtured. On the other hand, Nuitka is too irrelevant yet to drive this,
and it would detract me away from it.

*******
 Gains
*******

So Nuitka got a lot more exposure. And one guy watching the talk even
created a really `nice logo </doc/images/Nuitka-Logo-Vertical.png>`_ for
it. I will make it a separate announcement though, and the next release
is going to use it.

And in the aftermath, there were much bug useful reports. And new ideas.
And reinforcement that what I am doing is actually useful to some people
already.

***********
 Donations
***********

My travel to Florence was in part funded by donations. Thanks a lot to
all of you who have given, and who would like to also `make a donation
</pages/donations.html>`_. Should I receive sufficient donations, I
intend to go to FOSDEM 2014 as well.

Going to Berlin will be a bit cheaper this time around, as I can travel
there via train.

************
 Conclusion
************

The Europython 2012 and 2013 both are among the times of my life.
