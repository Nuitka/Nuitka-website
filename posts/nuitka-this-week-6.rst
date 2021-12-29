.. post:: 2018/09/12 12:05:00
   :tags: Python, compiler, Nuitka, NTW
   :author: Kay Hayen

#####################
 Nuitka this week #6
#####################

.. contents::

*********
 Holiday
*********

In my 2 weeks holiday, I indeed focused on a really big thing, and got
more done that I had hoped for. For C types, ``nuitka_bool``, which is a
tri-state boolean with true, false and unassigned, can be used for some
variables, and executes some operations without going through objects
anymore.

bool
====

Condition codes are no longer special. They all need a boolean value
from the expression used as a condition, and there was a special paths
for some popular expressions for conditions, but of course not all. That
is now a universal thing, conditional statement/expressions will now
simply ask to provide a temp variable of value ``nuitka_bool`` and then
code generation handles it.

For where it is used, code gets a lot lighter, and of course faster,
although I didn't measure it yet. Going to ``Py_True``/``Py_False`` and
comparing with it, wasn't that optimal, and it's nice this is now so
much cleaner as a side effect of that C bool work.

This seems to be so good, that actually it's the default for this to be
used in 0.6.0, and that itself is a major break through. Not so much for
actual performance, but for structure. Other C types are going to follow
soon and will give massive performance gains.

void
====

And what was really good, is that not only did I get ``bool`` to work
almost perfectly, I also started work on the ``void`` C target type and
finished that after my return from holiday last weekend, which lead to
new optimization that I am putting in the 0.5.33 release that is coming
soon, even before the ``void`` code generation is out.

The ``void`` C type cannot read values back, and unused values should
not be used, so this gives errors for cases where that becomes obvious.

.. code:: python

   a or b

Consider this expression. The ``or`` expression, that one is going to
producing a value, which is then released, but not used otherwise. New
optimzation creates a conditional statement out of it, which takes ``a``
as the condition and if not true, then evaluates ``b`` but ignores it.

.. code:: python

   if not a:
       b

The ``void`` evaluation of ``b`` can then do further optimization for
it.

Void code generation can therefore highlight missed opportunities for
this kid of optimization, and found a couple of these. That is why I was
going for it, and I feel it pays off. Code generation checking
optimization here, is a really nice synergy between the two.

Plus I got all the tests to work with it, and solved the missing
optimizations it found very easily. And instead of allocating an object
now, not assigning is often creating more obvious code. And that too
allowed me to find a couple of bugs by C compiler warnings.

Obviously I will want to run a compile all the world test before making
it the default, which is why this will probably become part of 0.6.1 to
be the default.

module_var
==========

Previously variable codes were making a hard distinction for module
variables and make them use their own helper codes. Now this is
encapsulated in a normal C type class like ``nuitka_bool``, or the one
for ``PyObject *`` variables, and integrates smoothly, and even got
better. A sign things are going smooth.

*****************
 Goto Generators
*****************

Still not released. I delayed it after my holiday, and due to the heap
generator change, after stabilizing the C types work, I want to first
finish a ``tests/library/compile_python_module.py resume`` run, which
will for a Anaconda3 compile all the code found in there.

Right now it's still doing that, and even found a few bugs. The heap
storage can still cause issues, as can changes to cloning nodes, which
happens for ``try`` nodes and their ``finally`` blocks.

This should finish these days. I looked at performance numbers and found
that ``develop`` is indeed only faster, and ``factory`` due to even more
optimization will be yet faster, and often noteworthy.

************
 Benchmarks
************

The Speedcenter of Nuitka is what I use right now, but it's only showing
the state of 3 branches and compared to CPython, not as much historical
information. Also the organization of tests is poor. At least there is
tags for what improved.

After release of Nuitka 0.6.0 I will show more numbers, and I will start
to focus on making it easier to understand. Therefore no link right now,
google if you are so keen. ;-)

*********
 Twitter
*********

During the holiday sprint, and even after, I am going to Tweet a lot
about what is going on for Nuitka. So follow me on twitter if you like,
I will post important stuff as it happens there:

`Follow @kayhayen <https://twitter.com/kayhayen?ref_src=twsrc%5Etfw>`_

And lets not forget, having followers make me happy. So do re-tweets.

**************************
 Poll on Executable Names
**************************

So I put e.g. poll up on Twitter, which is now over. But it made me
implement a new scheme, due to `popular consensus
<https://twitter.com/KayHayen/status/1037591355319640065>`_

**********
 Hotfixes
**********

Even more hotfixes. I even did 2 during my holiday, however packages
built only later.

Threaded imports on 3.4 or higher of modules were not using the locking
they should use. Multiprocessing on Windows with Python3 had even more
problems, and the ``--include-package`` and ``--include-module`` were
present, but not working.

That last one was actually very strange. I had added a new option group
for them, but not added it to the parser. Result: Option works. Just
does not show up in help output. Really?

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

Working down the release backlog. Things should be out. I am already
working on what should become 0.6.1, but it's not yet 0.5.33 released.
Not a big deal, but 0.6.0 has 2 really important fixes for performance
regressions that have happened in the past. One is for loops, making
that faster is probably like the most important one. The other for
constant indexing, probably also very important. Very much measurable in
pystone at least.

In the mean time, I am preparing to get ``int`` working as a target C
type, so e.g. comparisons of such values could be done in pure C, or
relatively pure C.

Also, I noticed that e.g. in-place operations can be way more optimized
and did stuff for 0.6.1 already in this domain. That is unrelated to C
type work, but kind of follows a similar route maybe. How to compare
mixed types we know of, or one type only. That kind of things needs
ideas and experiments.

Having ``int`` supported should help getting some functions to C speeds,
or at least much closer to it. That will make noticeable effects in many
of the benchmarks. More C types will then follow one by one.

***********
 Donations
***********

If you want to help, but cannot spend the time, please consider to
donate to Nuitka, and go here:

`Donate to Nuitka <http://nuitka.net/pages/donations.html>`_
