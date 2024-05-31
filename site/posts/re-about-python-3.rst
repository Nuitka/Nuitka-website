.. post:: 2013/12/30 20:56:32
   :tags: Python
   :author: Kay Hayen

####################
 Re: About Python 3
####################

In `Alex Gaynor's post
<http://alexgaynor.net/2013/dec/30/about-python-3/>`__ there is just
about everything right. I still want to add my take on it.

Python3 is a fork of the Python community, that has left the user base
largely behind. After developing features very conservatively for a long
time (``from __future__ import division`` and stuff), where features
were first available but not active by default, that whole "Python 3000"
thing came up.

Misguided, after having maintained CPython on a level of excellence for
such a long time, there was a sense of "finally we get to make free
choices". I can understand that. And having witnessed Gnome 2.0.0, and
KDE 4.0.0, I even start to believe that there is some kind of underlying
law. Something that makes people want to start over.

That "5 years plan" Alex mentioned has failed, and everybody knows that
without solving the GIL within the next 5 years, i.e. another
incompatible Python change, it will likely become obsolete.

In terms of Python2.8, call it that way. Or have a 3.5 that has
``print`` statement, and then all kinds of incompatible changes to
Python3 to make it behave sane ``bytes(7)`` needs to do what ``str(7)``
once it. That would be about ``from __past__ import ....`` I suppose.

I also had another idea, having a "python2" built-in module that carries
a CPython2 interpreter and proxy objects for instances, where they talk
to another with incompatible types (new ``bytes``/``unicode`` to old
``str``).

Due to my work on that `Python compiler </pages/overview.html>`__ that
should have existed 20 years ago, I am familiar enough, to actually be
able and create that kind of CPython2/CPython3 hybrid.

But the main problems with all of that are:

#. CPython is developed by volunteers, and as such, they are neither
   obliged to do what we need, nor will they bend to any amount of
   posting. We need to get our acts together or it's not happening, and
   we are people who care about Python relevancy.

   There may not be nearly enough overlap of people capable and caring.
   And that would be a tremendous amount of work. Highly speculative, in
   the sense, that it may not see fruits.

#. And then, when you got that sorted out, expect a hostile reaction
   from the core developers and/or PSF. Whatever it is, that you
   develop, you won't be able to call it Python 2.8, as they are going
   to hate it.

#. And finally, as a course of action, that may even bring the complete
   downfall of Python as a community. The controversy associated is not
   for everybody, and we don't need a libreoffice/openoffice situation
   in Python, do we.

It's a pity, because clearly, for Nuitka there would be a bunch of
patches, that I would like to make, that would make my life far easier,
and even interpreted Python faster.
