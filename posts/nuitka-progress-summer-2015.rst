.. title: Nuitka Progress in Summer 2015
.. slug: nuitka-progress-summer-2015
.. date: 2015/10/05 08:08:54
.. tags: Python,compiler,Nuitka
.. type: text

A long time has passed again without me speaking about what's going on with
Nuitka, and that although definitely a lot has happened. I would contend it's
even *because* so much is going on.

I also am shy to make public postings about unfinished stuff it seems, but it's
long overdue, so much important and great stuff has happened. We are in the
middle of big things with the compiler and there is a lot of great achievement.

.. contents::

SSA (Single State Assignment Form)
==================================

For a long, long time already, each release of Nuitka has worked towards
increasing `"SSA" <http://en.wikipedia.org/wiki/Static_single_assignment_form>`_
usage in Nuitka.

Now it's there. The current pre-release just uses it. There were many things
to consider before enabling it, and always a next thing to be found that was
needed. Often good changes to Nuitka, it was also annoying the hell out of me
at times.

But basically now the forward propagation of variables is in place, with some
limitations that are going to fall later.

So the current release, soon to be replaced, still doesn't optimize this code
as well as possible:

.. code-block:: python

    def f():
        a = 1
        return a

But starting with the next release, the value of ``a`` is forward propagated
(also in way more complex situations), and that's a serious milestone for the
project.

Function Inlining
=================

When submitting my talk to EuroPython 2015, I was putting a lot of pressure
on me by promising to demo that. And I did. It was based on the SSA code that
only now became completely reliable, but otherwise very few few other changes,
and it just worked.

The example I used is this:

.. code-block:: python

    def f():
        def g(x, y):
            return x, y

        x = 2
        y = 1

        x, y = g(x, y) # can be inlined

        return x, y

So, the function ``g`` is forward propagated to a direct call, as are ``x`` and
``y`` into the ``return`` statement after making the in-line, making this:

.. code-block:: python

    def f():
        return 2, 1

Currently function in-lining is not yet activated by default, for this I am
waiting for a release cycle to carry the load of SSA in the wild. As you
probably know I usually tend to be conservative and to not make too many
changes at once.

And as this works for local functions only yet, it's not too important yet
either. This will generally become relevant once we have this working across
modules and their globally defined functions or methods. This will be a while
until Nuitka gets there.

Scalability
===========

Having got Nuitka's memory usage under control, it turned out that there are
files that can trigger Python recursion ``RuntimeError`` exception when using
the ``ast`` module to build the Nuitka internal tree. People really have code
with many thousands of operations to a ``+`` operation.

So, Nuitka here learned to include whole modules as bytecode when it is too
complex as there is no easy way to expand the stack on Windows at least. That
is kind of a limitation of CPython itself I didn't run into so far, and rather
very annoying too.

The scalability of Nuitka also depends much on generated code size. With the
optimization become more clever, less code is generated, and that trend will
continue as more structural optimization are applied.

Compatibility
=============

Very few things are possible here anymore. For the tests, in full compatibility
mode, even more often the less good line number is used.

Also the plug-in work is leading to improved compatibility with Qt plugins of
PySide and PyQt. Or another example is the ``multiprocessing`` module that on
Windows is now supposed to fork compiled code too.

Python 3.5
++++++++++

The next release has experimental support for Python 3.5, with the notable
exception that ``async`` and ``await``, these do not yet work. It passes the
existing test suite for CPython3.4 successfully. Passing here means, to pass or
fail in the same way as does the uncompiled Python. Failures are of course
expected, as details change, and a nice way of having coverage for exception
codes.

The new ``@`` operator is now supported. As the stable release of Python3.5 was
made recently, there is now some pressure on having full support of course.

I am not sure, if you can fully appreciate the catch up game to play here. It
will take a compiled coroutine to support these things properly. And that poses
lots of puzzles to solve. As usual I am binding these to internal cleanups so
it becomes simpler.

In the case of Python3.5, the single function body node type that is used for
generators, class bodies, and function, is bound to be replaced with a base
class and detailing instances, instead of one thing for them all, then with
coroutines added.

Importing Enhancements
++++++++++++++++++++++

A while ago, the import logic was basically re-written with compatibility much
increased. Then quite some issues were fixed. I am not sure, but some of the
fixes have apparently also been regressions at times, with the need for other
fixes now.

So it may have worked for you in the past, but you might have to report new
found issues.

It's mainly the standalone community that encounters these issues, when just one
of these imports doesn't find the correct thing, but picking the wrong one will
of course have seriously bad impacts on compile time analysis too. So once we
do cross module optimization, this must be rock solid.

I think we have gotten a long way there, but we still need to tackle some more
fine details.

Performance
===========

Graphs and Benchmarks
+++++++++++++++++++++

I also presented this weak point to EuroPython 2015 and my plan on how to
resolve it. And low and behold, turns out the PyPy people had already developed
a tool that will be usable for the task and to present to the conference.

So basically I was capable of doing kind of a prototype of comparative benchmark
during EuroPython 2015 already. I will need to complete this. My plan was to get
code names of functions sorted out in a better way, to more easily match the
Nuitka C function names with Python functions in an automatic way. That matching
is the hard part.

So that is already progressing, but I could need help with that definitely.

Nuitka really has to catch up with benchmarks generally.. The work on automated
performance graphs has made more progress, and they are supposed to show up on
`Nuitka Speedcenter <http://speedcenter.nuitka.net>`__ each time, ``master``,
``develop``, or ``factory`` git branches change.

.. note::

   There currently is no structure to these graphs. There is no explanations or
   comments, and there is no trend indicators. All of which makes it basically
   useless to everybody except me. And even harder for me than necessary.


As a glimpse of what is possible with in-lined functions, look at this:

`Lambda call construct case <http://speedcenter.nuitka.net/constructs/construct-calllambdaexpressiondirectly.html>`__

But we also need to put real programs and use cases to test. This may need
your help. Let me know if you want to. It takes work on taking the data, and
merging them into one view, linking it with the source code ideally. That will
be the tool you can just use on your own code.

Standalone
==========

The standalone mode of Nuitka was pretty good, and continued to improve further,
now largely with the help of plug-ins.

I now know that PyGTK is an issue and will need a plug-in to work. Once the
plug-in interface is public, I hope for more outside contributions here.

Other Stuff
===========

Funding
+++++++

Nuitka receives the occasional `donation <http://nuitka.net/pages/donations.html>`_
and those make me very happy. As there is no support from organization like the
PSF, I am all on my own there.

This year I traveled to Europython 2015, I needed a new desktop computer after
burning the old one through with CI tests, the website has running costs, and
so on. That is pretty hefty money. It would be sweet if aside of my free time
it wouldn't also cost me money.

EuroPython 2015
+++++++++++++++

This was a blast. Meeting people who knew Nuitka but not me was a regular
occurrence. And many people well appreciate my work. It felt much different
than the years before.

I was able to present Nuitka's function in-lining indeed there, and this high
goal that I set myself, quite impressed people. My talk went very well, I am
going to post a link separately in another post.

Also I made many new contacts, largely with the scientific community. I hope to
find work with data scientists in the coming years. More amd more it looks like
my day job should be closer to Nuitka and my expertise in Python.

Collaborators
+++++++++++++

Nuitka is making break through progress. And you can be a part of it. Now.

You can join and should do so now, just `follow this link
<http://nuitka.net/doc/user-manual.html#join-nuitka>`_ or become part of the
mailing list (since closed) and help me there with request I make, e.g. review
posts of mine, test out things, pick up small jobs, answer questions of
newcomers, you know the drill probably.

Future
======

So, there is multiple things going on:

* Function in-lining

  For locally declared functions, it should become possible to avoid their
  creation, and make direct calls instead of ones that use function objects
  and expensive parameter handling.

* Nested frames

  One result of in-lining will be nested frames still present for exceptions
  to be properly annotated, or ``locals`` giving different sets of locals and
  so on.

  Some cleanup of these will be needed for code generation and SSA to be able
  to attach variables to some sort of container, and for a function to be able
  to reference different sets of these.

* Type Inference

  With SSA in place, we really can start to recognize types, and treat things
  that work something assigned from ``[]`` different, and with code special to
  these.

  That's going to be a lot of work. For ``float`` and ``list`` there are very
  important use cases, where the code can be much better.

* Shape Analyisis

  My plan for types, is not to use them, but the more general shapes, things
  that will be more prevalent than actual type information in a program. In
  fact the precise knowledge will be rare, but more often, we will just have
  a set of operations performed on a variable, and be able to guess from there.

* Python 3.5 new features

  The coroutines are a new type, and currently it's unclear how deep this is
  tied into the core of things, i.e. if a compile coroutine can be a premier
  citizen immediately, or if that needs more work. I hope it just takes for
  the code object to have the proper flag. But there could be stupid type
  checks, we shall see.

* Plug-ins

  Something I wish I could have shown at EuroPython was plug-ins to Nuitka. It
  is recently becoming more complete, and some demo plug-ins for say Qt plugins,
  or multiprocessing, are starting to work. The API will need work and of course
  documentation. Hope is for this to expand Nuitka's reach and appeal to get
  more contributors.

Let me know, if you are willing to help. I really need that help to make things
happen faster. Nuitka will become more and more important only.
