.. title: Nuitka this week #11
.. slug: nuitka-this-week-11
.. date: 2018/12/10 07:09:00
.. tags: Python,compiler,Nuitka,NTW
.. type: text

.. contents::

Communication vs. Coding
========================

I continue to force myself to report more publicly, and it feels good. This
time things are in a stablizing period, and I feel I have a consistent
message.

Bear in mind, that this is supposed to be a quick, not too polished, and
straight from top of my head, even if really a lot of content. But I feel
that esp. the optimization parts are worth reading.

Optimization Work
=================

So, the 0.6.1 optimization work has been a lot. And it's containing
improvements on every level. I think I will detail the levels in another section.

Levels of Optimization
----------------------

First level is of course node level optimization. Here 0.6.1 adds many things,
from better handling of closure variables not all as unknown every time control
flow escapes, to some operations ``+`` and comparisons on known built-in type
shapes to now be able to statically tell that they do not raise. The opposite
(does definitely raise) is prepared, but not yet used.

This allows for type shapes to be longer known. Now ``a+b+c`` can be known, but
previously only ``a+b`` was sort of known, and little used information.

The next level is picking the C target type. Here seeing more operations and
understanding more variables allows to more often pick the `C bool` or `C void`
types over the `PyObject *` C type. For 0.6.1 I have observed that esp. more
indicator variables make it to that stage, generating way more efficient C code
(for that indicator variable) for those  in many instances, esp. with loops,
as these no longer loose type shape information as badly as they did.

The, another level is when it is treated as an object, but known to be `int`,
there are way more helpers used for `+`/`+=` and a whole new set of them
for comparisons, that in these cases of full or partial type knowledge operate
faster.

And even if e.g. only one type is known, this still allows to not make a lot
of tests about it, and to avoid attempted shortcuts that cannot work. For 0.6.1
the `+` and `+=` are pretty well covered for these, but some variants are not
yet tuned to take all type knowledge advantage.

These will be also the building block, once the C type layer picks types like
"C int or PyObject * known to be int" with indicator flags which values are
currently valid to use, then these specialized calls still make sense.

The most attrative level, "C int" has not been reached for 0.6.1 but for my
loop example and Python3, I can say that now would be a nice time to start it,
as type shape knowledge is all there. This was totally not the case for 0.6.0,
but it seems that this step will have to be postponed to another release, maybe
0.6.2, maybe even later.

Week of Bugfixing
=================

But something that bothers me is seeing the issue tracker pile up on actionable
items, where I just have not taken action.  So as announced on Twitter already,
I am having and continue to have bug fixing time. I am acting on issues that
are relatively old and easy to act on, or where I have no hope of this
happening by anybody else anymore.

I have listed some interesting examples below. But basically these are small,
relatively unimportant, yet somewhat import for some use cases things.

Exec on Filehandles
===================

So when doing exec on a filehandle, Nuitka was at runtime reading the source,
then compiling it, but forgetting about the filename. This makes things like
`inspect.getsource()` fail on functions from there, and ugly tracebacks not
pointing to the filename. This was one of the things which I had understood,
but not did the actual work yet.

pkgutil.iter_modules
====================

And another one, which seemed just not done, but turned out to be rather
complex, this one needs to populate a ``sys.path_importer_cache`` for imported
modules, and then to report the child modules. There was no object to carry that
information, so now instances of the meta path based importer are associated
for every import.

Turns out for Python3, my simplistic type building calling `type` manually here
does not work, as ``__init__`` and ``iter_modules`` do not become anything but
static methods ever. Needs a real type.

Plus, I had to disable it for now, because mixed packages, like the one we do
with ``multiprocessing" where only part is compiled (the one required) and part
is pure Python from disk still, stopped to work. The ``iter_modules`` it seems
will have to cover that case too.

So no luck, postponing this until next week of bug fixes. Frustrating a bit,
but such is life.

When to release
---------------

There are still some issues that I want to get to. Specicially the OpenGL
plugins which has been research ever since, and nobody stepped up, but it's
rather trivial. And the Tcl/Tk for Windows. People have provided sufficient
instructions for a plugin that I am going to write this week.

Once I feel the issue tracker is clean, I will release. As a matter of
experience, it is then going to grow a lot again.

Google Summer of Code for Nuitka
================================

Finally somebody has stepped up, which means a lot to me. Now to the actual
work!

Twitter
=======

I continue to be very active there.

`Follow @kayhayen <https://twitter.com/kayhayen?ref_src=twsrc%5Etfw>`_

And lets not forget, having followers make me happy. So do re-tweets.

Adding Twitter more prominently to the web site is something that is also
going to happen.

Help Wanted
===========

If you are interested, I am tagging issues
`help wanted <https://github.com/kayhayen/Nuitka/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22>`_
and there is a bunch, and very likely at least one *you* can help with.

Nuitka definitely needs more people to work on it.

Donations
=========

If you want to help, but cannot spend the time, please consider to donate
to Nuitka, and go here:

`Donate to Nuitka <http://nuitka.net/pages/donations.html>`_

