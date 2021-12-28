#####################
 Nuitka this week #4
#####################

.. contents::

*****************
 Goto Generators
*****************

This continues `TWN #3 <./nuitka-this-week-3.html#goto-generators>`_
where I explained what is all about.

Good news is, at the time Python2 generators were largely working with
the new ways, in the mean time not only did all of the Python 2.7 test
suite pass with goto generators, also did the Python 3.4 test suite,
i.e. also the ``yield from`` is working with it.

The way it was done is to set ``m_yieldfrom`` in generators, and then to
enter a state, where the code will only be resumed, when that
sub-generator that currently it is yielding from, is finished. That
makes it very much like normal yield. In fact, code generation is hardly
different there.

Since the whole purpose is to get rid of ``make/get/setcontext``, the
next stop is coroutines. They have ``async for``, ``async with`` and
``await`` but at the end of the day, the implementation comes down to
``yield from`` really with only a lot of sugar applied.

Right now, I am debugging "goto coroutines". It's hard to tell when it
will be finished, and then ``asyncgen`` will be waiting still.

This is easily the largest change in a long time, esp. due to the heap
storage changes that I already discussed. One this is finished, I expect
to turn towards C types with relative ease.

************
 Tox Plugin
************

Anthony Shaw took on Tox and Nuitka and created a plugin that allows
using Nuitka. I am still wrapping my head around these things. It's only
a proof of concept yet. I will give it more coverage in the future.

*********
 Twitter
*********

Follow me on twitter if you like, I will:

`Follow @kayhayen <https://twitter.com/kayhayen?ref_src=twsrc%5Etfw>`_

**********
 Hotfixes
**********

So there have even more hotfixes. One addresses memory leaks found with
the ``yield from`` while I was adding tests. Usually if I encounter an
old issue that has a small fix, that is what I do, push out a hotfix
using the git flow model. Also nested namespace packages for Python3,
those are the ones without a ``__init__.py`` were not working after the
original directory was removed, and that got fixed.

And right now, I have hotfixes for frames ``close`` method, which
apparently was never updated to work properly for ``coroutines`` and
``asyncgen``. That is going to be in the next hotfix.

*******
 Plans
*******

So the heap storage seems pretty complete now, and goto generators are
on the final stretch. As always, things feel right around the corner.
But it's unclear how much longer I will have to debug. I am pretty sure
the bare work of doing asyncgen is going to be low. Debugging that too
then, that is the hard part.

A new release seems justified, but I kind of do not want to make it
without that major new code used. Because apparently during the
debugging, I tend to find issues that need hotfixes, so I will wait for
the goto generator work to finish.
