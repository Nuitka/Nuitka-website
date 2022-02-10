.. post:: 2014/06/18 07:46:50
   :tags: Python, quiz
   :author: Kay Hayen

##########################
 Yup, another Python Quiz
##########################

Using the following source code as a test happily in my `Python compiler
Nuitka </pages/overview.html>`__ for some years now.

.. code:: python

   # Testing dict optimization with all constants for compatibility.
   print(
       "Dictionary entirely from constant args",
       dict(q="Guido", w="van", e="Rossum", r="invented", t="Python", y=""),
   )

***************
 Quiz Question
***************

Lately, when adding Python 3.4 support, this and other code changed. So
lets do this manually:

.. code:: bash

   PYTHONHASHSEED=0 python3.3

.. code::

   Python 3.3.5 (default, Mar 22 2014, 13:24:53)
   [GCC 4.8.2] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> dict(
   ...                q='Guido',
   ...                w='van',
   ...                e='Rossum',
   ...                r='invented',
   ...                t='Python',
   ...                y=''
   ...             )
   {'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van', 'y': ''}
   >>> {'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van', 'y': ''}
   {'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van', 'y': ''}
   >>> {'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van', 'y': ''}
   {'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van', 'y': ''}
   >>> {'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van', 'y': ''}
   {'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van', 'y': ''}

See, the dictionary is stable, once it gets reordered, due to hash
values, but then it stays fixed. Which is pretty OK, and using a fixed
hash value, it's deterministic. Random hashing is not good for
comparison testing, so I disable it for tests.

Now things get interesting, repeat with 3.4:

.. code:: bash

   PYTHONHASHSEED=0 python3.4

.. code::

   Python 3.4.1rc1 (default, May  5 2014, 14:28:34)
   [GCC 4.8.2] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> dict(
   ...                q='Guido',
   ...                w='van',
   ...                e='Rossum',
   ...                r='invented',
   ...                t='Python',
   ...                y=''
   ...             )
   {'y': '', 'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van'}
   >>> {'y': '', 'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van'}
   {'r': 'invented', 'q': 'Guido', 'y': '', 'e': 'Rossum', 't': 'Python', 'w': 'van'}
   >>> {'y': '', 'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van'}
   {'r': 'invented', 'q': 'Guido', 'y': '', 'e': 'Rossum', 't': 'Python', 'w': 'van'}
   >>> {'y': '', 'q': 'Guido', 'r': 'invented', 'e': 'Rossum', 't': 'Python', 'w': 'van'}
   {'r': 'invented', 'q': 'Guido', 'y': '', 'e': 'Rossum', 't': 'Python', 'w': 'van'}

   Nuitka builds this as the argument dictionary, before it is
   passed to dict. Since it's all compile time constants, we can do that, right, and
   we can use the result instead. So see this:

Look at how the result of "dict" is not reproducing itself, when used as
a constant. I am only feeding the ``dict`` result to the interpreter,
and it changes.

So the quizz this time is, why does this happen. What change in
CPython3.4 makes this occur. Obviously it has to do with dictionary
sizes.

**********
 Solution
**********

I had a theory, but I couldn't confirm it looking at all of CPython
sources "ceval.c" and "dictobject.c" differences between the two
versions.

I am suspecting a difference between presized and non-presized
dictionaries, or that change to dictionary grow. When ``dict`` is being
called, the amount of keys is know though, as well as when building the
constant. So this ought to not play any role.

Hm, actually. I don't know the solution yet. :-)
