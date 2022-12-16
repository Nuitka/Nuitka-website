.. post:: 2022/12/10 11:29:24
   :tags: Python, compiler, Nuitka
   :author: Kay Hayen

########################
 Python 3.11 and Nuitka
########################

In my `all in with Nuitka </posts/all-in-with-nuitka.html>`__ post, I promised
to give you an update on the current status of Python 3.11 support and Nuitka,
and this is the report on my busy bee activities there.

*************
 What is now
*************

Current Nuitka 1.2 and likely the coming 1.3 release, will react pretty
hefty to attempts to compile with Python3.11, so this command:

.. code:: bash

   python3.11 -m nuitka tests/basics/Asserts.py

Gives the following output:

.. code::

   Nuitka:WARNING: The version '3.11' is not currently supported. Expect
   Nuitka:WARNING: problems.
   FATAL: The Python version '3.11' is not supported by '1.2.7', but an upcoming release will add it.

******************
 What you can do?
******************

As a mere mortal, what you can and should do is to consider
becoming a `subscriber of Nuitka commercial
<https://nuitka.net/doc/commercial.html>`__, even if you do not
need the IP protection features it mostly has. All essential packaging
and performance features are free, and I have put incredible amounts of
works in this, and I need to now make a living off it.

And working on 3.11 support, just so tings then continue to work, mostly
on my own deserves financial support. Once a year, for weeks on end, I am
re-implementing features that a collective of developers came up with.

Otherwise, unless you are CPython core developer responsible for the changes, I
am afraid, not a lot. Having to know both Nuitka and CPython details is a tall
ask. I might be the only one to do this for a while. I will however strive to
get more people involved each time.

That is not to say this does not happen. Not too long ago, I merged proposed
changes that will help Nuitka with 3.12 compatibility. This would be nice if it
was more frequent, and the fact that it is not, is probably my fault entirely.

***************
 What was done?
***************

In the summer, with release candidates, there was some refactoring done that
aimed at making Nuitka compile, at least with less errors. One of the changes
that was addressed at the time was the reduction of exception state to only a
value.

In Python during an exception, you typically have a exception "type",
"value", and a "traceback". And these used to be sort of independent
objects, which then through a process called "normalization" got
aligned. E.g. when raising an exception, you would simply put a
``ZeroDivisionError`` as a type, and a string as the value, and only on
normalization, which was attempted to be done as late as possible, the
actual exception object was created.

For 3.11 now, in some parts (but not all of course), this got reduced,
and making Nuitka cope with that was a bigger task, and even one that
had then introduced a regression to pre-3.11, i.e. affecting other
versions. I had to make a hotfix because of this for the release that
included these changes. This is of course, due to also cleaning up the
code that was changed, to reduce e.g. duplications that were considered
harmless in the past.

Now, during the 1.3 releases cycle, many more changes have been
addressed. The CPython core is using now "interpreter frames", which are
lightweight non-objects, and does only create a frame when an exception
is needed. Nuitka on the other hand used to cache frame objects, that it
also created only when needed. Adapting the interactions with the frame
stack appears somewhat solved, but actually poses some bugs when dealing
with generators that raise exceptions, and is currently being analysed.

*************
 The Process
*************

When the goal is getting 3.11 supported (or any later Python, this will
repeat forever), in a first step it just doesn't compile on the C level
anymore. First, all kinds of changes need to be addressed that show when
compiling on the C level. Or extra time spent to disable some things to
migrate only later (which I tend to not do), but the unfortunate truth
is, that at that point, running with 3.11 to find out things, is not yet
an option.

Once compiled 3.11 started being executable, it was hard crashing (worst
case) and asserting (good case) like hell. Many assumptions made proved
to be untrue, or things that used to be true, are no more true. That is
pretty normal when you mingle with internal details of course.

Right now reference leaks are being seen with generators, and so are
crashes. This is probably the same issue, where some link between
objects, some reference to an object is taken, and what is most likely,
in other instance, it is lost, which then causes corrupted objects.
These are among the hardest things to debug in Python, often the symptom
only shows later. Many times development in this phase is about adding
assertions. This is where we are now.

The next phase then is to run the CPython 3.10 test suite compiled with
3.11 and compare its results to running with plain 3.11, and expect it
to be the same. It is normal for CPython 3.10 tests to fail with 3.11,
and this does two things.

Either the test passes where it should not, then 3.11 added extra
checks, e.g. making it illegal to provide certain types of inputs that
were legal in the past, or it fails where 3.11 does not, then it
highlights a behavior change or a mistake in the migration. Another case
of course is it crashing. Then some bug in e.g. frame handling or
exception handling might cause that.

During this phase it is esp. initially very hard to assess where we
stand. Often one bug affects many tests with different symptoms. We we
just look for things that are easy to analyse.

In the next phase, the 3.11 test suite is used in the same way. This
will often uncover new features, new behaviors, newly allowed things.
For example Nuitka might reject an input, but that is correct for 3.10,
but not for 3.11 anymore, this this will be added.

This phase has not even started.

One interesting case is new test coverage. Often is has happened in the
past that something was incompatible with 3.10 already, but that has
never been seen. Of course, in this instance, the modification will be
backported, this is often revealed when running the 3.11 tests compiled
with 3.11 and comparing the result with pure 3.10.

And this is also not even started. Once the test suite is adapted for
Nuitka's needs (avoiding random outputs, to make tests comparable e.g.)
this could be started, and would enhance 3.10 compatibility already with
its findings.

**********************
 Intermediate Results
**********************

Once the Python3.11 more or less well passed the 3.10 test suite without
big issues, experimental support for it will be added. The warning from
above will be given, but the error will cease.

But only once the CPython 3.11 test suite is completely passing, it will
be added as supported officially. Again, not all tests have to pass
perfectly for this, cosmetic things are not counted of course.

******
 When
******

Very hard to predict. Supporting existing Nuitka is also a side tracking
thing, that makes it unclear how much time I will have for it. But the
worst things with debugging is that I just never know how much time it
will be. In past releases, the time has varied. I do not know at this
time, what will have to be done for support of 3.11, it clearly is one
of the harder ones. But I am hoping these core changes were the bulk of
the work.

*******************************
 Benefits for older Python too
*******************************

When I noticed that the dictionary implementation had heavily changed,
and Nuitka's "illegal" friendship (accessing internal details of it)
caused it to not compile, step one was to compare current details with
3.10 and find that there are a bunch of things that were added over
time. For example one fast branch that was added to 3.10, Nuitka now has
it too, for 3.6 or higher. So we are also back-porting some speed
improvements.

Also the allocator of 3.11 changed, and as a result, the allocator for
all older Python will be way faster to use, esp. with platforms that use
DLLs.

There are other benefits, e.g. 3.10 is exposing free lists (re-usable
objects without going through allocation) it is using, allowing Nuitka
to accelerate dictionary object creation esp. on Windows, and so on.

*******************
 Expected results
******************

People tend to expect that gains from Nuitka and enhancements of CPython stack
up. The truth of the matter is, no they do not. CPython is applying some tricks
that Nuitka already did. Not using its bytecode will then become less of a
benefit, but that's OK, this is not what Nuitka is about.

We need to get somewhere else entirely anyway, in terms of speed
up. I will be talking about PGO and C types a lot in the coming year, that is
at least the hope. That is where the "all in" part kicks in.

************
 Final Words
************

Look ma, I posted about something that is not complete. I am getting better.
