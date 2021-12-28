#####################
 Nuitka this week #2
#####################

.. contents::

**********************
 New Series Rationale
**********************

As discussed last week in `TWN #1 <./nuitka-this-week-1.html>`_ this is
a new series that I am using to highlight things that are going on,
newly found issues, hotfixes, all the things Nuitka.

************
 Python 3.7
************

I made the first release with official 3.7 support, huge milestone in
terms of catching up. Generic classes posed a few puzzles, and need more
refinements for error handling, but good code works now.

The class creation got a bit more complex, yet again, which will make it
even hard to know the exact base classes to be used. But eventually we
will manage to overcome this and statically optimize that.

**************************
 MSI 3.7 files for Nuitka
**************************

Building the MSI files for Nuitka ran into a 3.7.0 regression of CPython
failing to build them, that I reported and seems to be valid bug of
theirs.

So they will be missing for some longer time. Actually I wasn't so sure
if they are all that useful, or working as expected for the runners, but
with the ``-m nuitka`` mode of execution, that ought to be a non-issue.
so it would be nice to keep them for those who use them for deployment
internally.

**************
 Planned Mode
**************

I have a change here. This is going to be a draft post until I publish
it, so I might the link, or mention it on the list, but I do not think I
will wait for feedback, where there is not going to be all that much.

So I am shooting this off the web site.

*****************
 Goto Generators
*****************

This is an exciting field of work, that I have been busy with this week.
I will briefly describe the issue at hand.

So generators in Python are more generally called coroutines in other
places, and basically that is code shaking hands, executing resuming in
one, handing back a piece of data back and forth.

In Python, the way of doing this is ``yield`` and more recently ``yield
from`` as a convienant way for of doing it in a loop in Python3. I still
recall the days when that was a statement. Then communication was one
way only. Actually when I was still privately doing Nuitka based on then
Python 2.5 and was then puzzled for Python 2.6, when I learned in Nuitka
about it becoming an expression.

The way this is implemented in Python, is that execution of a frame is
simply suspended, and another frame stack bytecode is activated. This
switching is of course very fast potentially, the state is already fully
preserved on the stack of the virtual machine, which is owned by the
frame. For Nuitka, when it still was C++, it wasn't going to be possible
to interrupt execution without preserving the stack. So what I did was
very similar, and I started to use ``makecontext/setcontext`` to
implement what I call fibers.

Basically that is C level stack switching, but with a huge issue. Python
does not grow stacks, but can need a lot of stack space below. Therefore
1MB or even 2MB per generator was allocated, to be able to make deep
function calls if needed.

So using a lot of generators on 32 bits could easily hit a 2GB limit.
And now with Python3.5 coroutines people use more and more of them, and
hit memory issues.

So, goto generators, now that C is possible, are an entirely new
solution. With it, Nuitka will use one stack only. Generator code will
become re-entrant, store values between entries on the heap, and
continue execution at goto destinations dispatched by a switch according
to last exit of the generator.

So I am now making changes to cleanup the way variable declarations and
accesses for the C variables are being made. More on that next week
though. For now I am very exited about the many cleanups that stem from
it. The code generation used to have many special bells and whistles,
and they were generalized into one thing now, making for cleaner and
easier to understand Nuitka code.

*********************
 Python3 Enumerators
*********************

On interesting thing, is that an incompatibility related to ``__new__``
will go away now.

The automatic ``staticmethod`` that we had to hack into it, because the
Python core will do it for uncompiled functions only, had to be done
while declaring the class. So it was visible and causing issues with at
least the Python enum module, which wants to call your ``__new__``
manually. Because why would it not?!

But turns out, for Python3 the ``staticmethod`` is not needed anymore.
So this is now only done for Python2, where it is needed, and things
work smoothly with this kind of code now too. This is currently in my
factory testing and will probably become part of a hotfix if it turns
out good.

**********
 Hotfixes
**********

Immediately after the release, some rarely run test, where I compiled
all the code on my machine, found 2 older bugs, obscure ones arguably,
that I made into a hotfix, also because the test runner was having a
regression with 3.7, which prevented some package builds. So that was
0.5.32.1 release.

And then I received a bug report about ``await`` where a self test of
Nuitka fails and reports an optimization error. Very nice, the new
exceptions that automatically dump involved nodes as XML made it
immediately clear from the report, what is going on, even without having
to reproduce anything. I bundled a 3.7 improvement for error cases in
class creation with it. So that was the 0.5.32.2 release.

*******
 Plans
*******

Finishing goto generators is my top priority, but I am also going over
minor issues with the 3.7 test suite, fixing test cases there, and as
with e.g. the enum issue, even known issues this now finds.

Until next week.
