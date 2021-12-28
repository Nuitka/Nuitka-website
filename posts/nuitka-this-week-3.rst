.. title: Nuitka this week #3
.. slug: nuitka-this-week-3
.. date: 2018/08/11 11:58:00
.. tags: Python,compiler,Nuitka,NTW
.. type: text

.. contents::

New Series Rationale
====================

This is working out well so far. I think driving more attention at the things
that are going on can only be good. Also to explain will always help. It also
kind of motivates me a bit.

Twitter
=======

Also as part of my communications offensive, I am using my Twitter account
more regularly. I used to highlight important fixes, or occasionally releases
of some importance there. I will continue to do only important stuff there,
but with more regularity.

And I noticed in the past, even when I do not post, followers makes me
happy. So here you go:

`Follow @kayhayen <https://twitter.com/kayhayen?ref_src=twsrc%5Etfw>`_

Goto Generators
===============

This continues `TWN #2 <./nuitka-this-week-2.html#goto-generators>`_ where
I promised to speak more of it, and this is the main focus of my work on
Nuitka right now.

Brief summary, context switches were how this was initially implemented. The
main reason being that for C++ there never was going to be a way to save and
restore state in the middle of an expression that involves constructors and
destructors.

Fast forward some years, and C-ish entered the picture. No objects are used
anymore, and Nuitka is purely C11 now, which has convenience of C++, but no
objects. Instead ``goto`` is used a lot already. So every time an exception
occurs, a ``goto`` is done, every time a branch is done, a loop exit or
continue, you get it, another ``goto``.

But so far, all Python level variables of a frame live on that C stack still,
and the context switch is done with functions that swap stack. That is fast,
but the imporant drawback is that it takes more memory. How deep of a stack
will we need? And we can use really many, if you imagine a pool of 1000
coroutines, that quickly become impossible to deal with.

So, the new way of doing this basically goes like this:

.. code-block:: python

    def g():
        yield 1
        yield 2

This was some far becoming something along this lines:

.. code-block:: c

   PyObject *impl_g( NuitkaGenerator *generator )
   {
        YIELD( const_int_1 );
        YIELD( const_int_2 );

        PyErr_SetException( StopIteration );
        return NULL;
   }

The ``YIELD`` in there was basically doing the switching of the stacks and
for the C code, it looked like a normal function call.

In the new approach, this is done:

.. code-block:: c

   PyObject *impl_g( NuitkaGenerator *generator )
   {
        switch( generator->m_resume_point )
        {
             case 1: goto resume_1;
             case 2: goto resume_2;
        }

        generator->m_yielded = const_int_1;
        generator->resume_point = 1
        return NULL;
        resume_1:

        generator->m_yielded = const_int_2;
        generator->resume_point = 2
        return NULL;
        resume_2:

        PyErr_SetException( StopIteration );
        return NULL;
   }

As you can see, the function has an initial dispatcher. Resume point 0 means
we are starting at the top. Then every ``yield`` results in a function return
with an updated resume point.

I experimented with this actually a long time ago, and experimental code was
the result that remained in Nuitka. The problem left to solve was to store the
variables that would normally live on the stack, in a heap storage. That is
what I am currently working on.

This leads me to "heap storage", which is what I am currently working on and
will report on next week. Once that is there, goto generators can work, and
will become the norm. Until then, I am refactoring a lot to get accesses to
variable go through proper objects that know their storage locations and
types.

Hotfixes
========

So there have been 2 more hotfixes. One was to make the ``enum`` and ``__new__``
compatibility available that I talked about last week in
`TWN #2 <./nuitka-this-week-2.html#python3-enumerators>` coupled with a
new minor things.

And then another one, actually important, where Python3 ``__annotations__`` by
default was the empty dictionary, but then could be modified, corrupting the
Nuitka internally used one severely.

Right now I have on factory another fix for nested namespace packages in
Python3 and that might become another hotfix soon.

As you know, I am following the git flow model, where it's easy to push out
small fixes, and just those, on top of the last release. I tend to decide
based on importance. However, I feel that with the important fixes in the
hotfixes now, it's probably time to make a full release, to be sure everybody
gets those.

Plans
=====

Finishing heap storage is my top priority right now and I hope to complete
the refactorings necessary in the coming week. I will also talk about how
it also enables C types work next week.

Until next week then!
