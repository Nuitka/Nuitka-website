.. post:: 2011/10/08 21:24
   :tags: Nuitka, Python, compiler, conference
   :author: Kay Hayen

###########################
 PyCON DE 2011 - My Report
###########################

The PyCON DE 2011 is just over, sprints are still happening over the
weekend, but my wife wouldn't allow me to stay away for that long, so
it's not for me this time. Maybe next time.

Right now I feel very happy and excited that I went there. What a
**great** experience this was.

It was the first German PyCON and clearly it was overdue as it was now
the merger of many already grown up communities. A huge number of talks
over 3 days in 3 parallel tracks, with 3 keynotes, was an outstanding
program. And very well run. Strict time management, every detail was
well prepared.

I can only admire the professional preparation and setup. I wanted to
say thank you deeply. I didn't consider it possible to be this good.
Clearly not a first time.

I enjoyed the talks, most often in the technical track, but other tracks
would have been very interesting too. The parallelism was making me do
hard decisions.

******
 Food
******

The food was great too. I esp. liked the Asian day, but there was also
Italian and French, and what many liked very much is that there was a
Vegan food offer too. I do not live vegan style, but I appreciate good
food and the vegan food often is that.

**************
 Social Event
**************

The social event was a visit to a "Variete" (music hall, French origin),
where I am sure, there will be images posted, I currently `found this
one
<https://secure.flickr.com/photos/onyame/6222954609/in/pool-1775853@N21/>`_
, that my wife will find interesting too.

*********
 Leipzig
*********

The quality of the organization team, the city "Leipzig", where we also
got to have a guided city tour of fantastic enthusiasms, was very high.
I knew Leipzig from earlier visits and liked it before, but this time it
seemed everybody was even friendlier.

******
 Site
******

The convention place "Kubus" was very well chosen, absolutely ideal.
It's got good equipment, and that large room setup, where you can make a
split with movable walls, and have 3 big screens. The acoustics were
pretty damn good there.

*********************
 My own Presentation
*********************

As to my own presentation, it was well received, although I sort of
regret that I agreed to have only 30m instead of original plan of 60m. I
had so much to say.

I ended up with getting my manifesto part out, but that one pretty well.
And it's OK I guess, because nobody really listens that long anyway. And
my major points came across that way.

That focus on my Nuitka "manifesto" was probably a good idea. The talk
will be available online as a video, I will link it then. The `PDF that
I presented only a small part of
</pr/Nuitka-Presentation-PyCON-DE-2011.pdf>`_, is linked here. I believe
it went pretty well.

I will use that content from the PDF in updated documentation (currently
ongoing in PDF is work to use REST and document a lot more). The
presentation was created with "rst2pdf", which I find is a fantastic
tool.

**********
 Contacts
**********

Cython / lxml
=============

Then contacts!

Early on I already made contacts with interesting people, e.g. with
Dr.Stefan Behnel, author of lxml and core Cython developer. I him
offered a beer for using his software in the best of Free Software
traditions. He doesn't drink these, but a large mango juice counts too
or so I assume.

We also talked about Cython and Nuitka, and the common history we had as
well. For some time, I attempted to change Cython, but that failed to
get the developers support at the time. Not wanting to deviate from
PyRex clearly isn't the state anymore, but that was then.

We also had a evening session of showing each other the good and bad
parts, comparing was quite fun. And it was quite interesting to the both
of us. I believe we made friends and will only benefit another.

We discussed my goals, and I think we came to the conclusion that they
are in fact different enough from Cythons. Although I go away with the
sense, that of course Stefan believes, it would be better if I joined
Cython. Naturally.

But that's not going to happen. I think i have a cleaner and better
implementation now, closer to my goals with a realistic chance to
succeed. To me it would be a step back to fix language parsing issues
and incompatibilities of Cython, with the danger that my goals will not
be shared.

As an example of these things, I would mention function call errors,
where e.g. Cython gives different and sometimes worse error messages
than CPython, and I designed the code so that it does things in that
same order than CPython does.

It do not want to give different error messages, and who knows, somebody
may check for the exception text and expect CPython output. In this
case, I will rather accept a worse performance, than an incompatibility.

Eliminating function parameter parsing for the whole program as far as
possible is going to be more worthwhile anyway.

But in my mind, Cython is something I can and do recommend. For as long
as I am not able to declare Nuitka "useful" yet. That statement may come
within a year though. In my mind, in many fields Nuitka is already
superior.

PyHasse
=======

Another interesting contact I made, was with the author of PyHasse. It's
Rainer Bruggemann, who is a really nice and witty guy. He introduced me
to how he applies graph theory to multi-parameter optimization problems.

We agreed that we will try and work together on this project. Hopefully
it will come to pass. One thing I personally wanted, was to get into
contact with people who understand or are part of the scientific
community.

I can see what NumPy is. But I may never know myself what it really is,
unless I find proxies, and make these kind of contacts. The same thing
is true of Django, or e.g. Mercurial. I am positive though that with
time, and such conferences, my knowledge of these will only grow.

We said that we will try and see how far we can go. In the worst case,
Nuitka will not yet be useful, but I will have a clearer image what is
needed.

Debian
======

I saw the presentation from Jan Dittberner and met him later too, asking
him questions, and generally discussing Debian packaging of Nuitka. He
encouraged me to contact the Debian Python Team, and so I will.

I used the chance to make contact with a Debian guy, who made a
presentation on how to package Python modules for Debian. He gave me
hints on how to solve that "find files near me" issue that plagues
Nuitka just as much as other software. Really kind and helpful guy and
clearly I admire Debian Developers, keep up the good work.

General
=======

I also made contacts with lots of other people. Python is diverse and it
was fun to get to know, many people with similar and entirely different
backgrounds.

The mood was extremely constructive. Nuitka was well received, but
that's not why I say it. There is that general sense of respect around
that German community, you can feel how pretty much everybody is well
established and doesn't have to disprove the others.

**********
 Keynotes
**********

One keynotes speaker had a part about how trolling and hate is bad for a
community, but that's not the German Python community.

Another keynote speaker (Paul Everitt) had a part about how Zope, which
was kind of his project, failed in many ways. He seemed to be quite
disappointed about that, which triggered me to point out, that he should
start his story with Apache, and not see the "failure to integrate" as a
failure.

If there had not been Apache failing, there wouldn't have been Zope, and
then not Django, etc. that's kind of normal and actually good. He agreed
and pointed out how Apache was created from another project that had
failed to integrate people.

You either fork a projects code, or ideas. The fork still should credit
and appreciate the predecessor/origin.

In my mind, Cython failed to integrate me. Which triggered me to come up
with Nuitka, and as I will point out over time (there ought to be
postings and there probably will be), some better approaches.

So not integrating me is not necessarily a failure. If it were not for
Cython, there would not be Nuitka. The original projects will regret the
fork/remake, but they probably shouldn't. Competition is good.

******************
 Lets repeat that
******************

I believe the PyCON DE 2011 was a huge success. I will most likely go
again to update people on Nuitka. It's already clear there will be a
PyCON DE 2012 I understand. And I am aiming for a slot at PyCON EU 2012
next year too. I wanted to go in 2011, but need to not put it in my
early booked holiday again.

But you know what Murphy says about that.

|  Yours,
|  Kay Hayen
