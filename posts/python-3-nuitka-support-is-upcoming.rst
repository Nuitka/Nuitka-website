.. post:: 2013/02/09 08:38:37
   :tags: Python, Nuitka
   :author: Kay Hayen

#######################################
 Python3 support by Nuitka is upcoming
#######################################

This is kind of semi-interesting news for you Python3 lovers. My
`"Python compiler Nuitka" </pages/overview.html>`_ has been supporting
the language somewhat, but in the next release it's going to be
*complete*.

Support for annotations, unicode variable names, keyword only arguments,
starred assignments, exception chaining plus causes, and full support
for new meta classes all have been added. So Python3.2 is covered now
too and passing the test suite on about the same level as with Python2.6
and Python2.7 already.

I readied this while working on optimization, which is also seeing some
progress, that I will report on another day. Plus it's `"available now
on PyPI" <http://pypi.python.org/pypi/Nuitka/>`_ too. At the time of
this writing, there is pre-releases there, but after next release, there
will only stable releases published.

My quick take on the Python3 that I saw:

************************
 Keyword Only Arguments
************************

Now seriously. I didn't miss that. And I am going to hate the extra
effort it causes to implement argument parsing. And when I looked into
default handling, I was just shocked:

.. code:: python

   def f( some_arg = function1(), *, some_key_arg = function2() )

What would you expect the evaluation order to be for defaults? I raised
a CPython `"bug report" <http://bugs.python.org/issue16967>`_ about it.
And I am kind of shocked this could be wrong.

*************
 Annotations
*************

.. code:: python

   def f( arg1 : c_types.c_int, arg2 : c_types.c_int ) -> c_types.c_long
      return arg1+arg2

That looks pretty promising. I had known about that already, and I
guess, whatever "hints" idea, we come up with Nuitka, it should at least
allow this notation. Unfortunately, evaluation order of annotations is
not that great either. I would expected them to come first, but they
come last. Coming last, they kind of come too late to accept do anything
with defaults.

*******************
 Unicode Variables
*******************

Now great. While it's one step closer to "you can't re-enter any
identifier without copy&paste", it is also a whole lot more consistent,
if you come e.g. from German or French and need only a few extra
letters. And there has to be at least one advantage to making everything
unicode, right?

********************
 Exception Chaining
********************

Gotta love that. Exception handlers are often subject to bit rot. They
will themselves contain errors, when they are actually used, hiding the
important thing that happened. No more. That's great.

The exception causes on the other hand, might be useful, but I didn't
see them a lot yet. That's probably because they are too new.

*****************
 Starred Assigns
*****************

I was wondering already, why that didn't work before.

.. code:: python

   a, *b = something()

***********************
 Metaclass __prepare__
***********************

That's great stuff. Wish somebody had thought about meta classes that
way from the outset.

**********
 nonlocal
**********

Yeah, big stuff. I love it. Also being able to write closure variables
is great for consistency.

************
 Conclusion
************

Nothing ground breaking. Nothing that makes me give up on Python2.7 yet,
but a bunch of surprises. And for Nuitka, this also found bugs and
corner cases, where things were not yet properly tested. The Python3
test suite, inspired the finding of some obscure compatibility problems
for sure.

Overall, it's possible to think of Python2 and Python3 as still the same
language with only minor semantic differences. These can then be dealt
with re-formulations into the simpler Python that Nuitka optimization
deals with internally.

I for my part, am still missing the ``print`` statement. But well, now
Python3 finds them when I accidentally check them in. So that's kind of
a feature for as long as I develop in Python2.6/2.7 language.

Now if one of you would help out with Python3.3, that would be great. It
would be about the new dictionary implementation mostly. And maybe
finding a proper re-formulation for "yield from" too.
