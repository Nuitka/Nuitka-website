
At Europython conference, in my presentation, I talked about re-formulations of Python
into simpler Python. It is my intention to turn this into a series of Python quiz
questions that you will hopefully enjoy.

.. admonition:: Update

   Due to comments feedback, I made it more clear that "-O" affects of course both cases,
   and due to work on getting the recent CPython2.7 test suite to work, I noticed, how the
   re-formulation for Quiz Question 2 needed a version dependent solution.

   And I thought this one was easy. :-)

Quiz Question 1
---------------

Say you have the following code:

.. code-block:: python

    assert x == y

How can you achieve the same thing, without using the ``assert`` statement at all. The
behavior is required to be absolutely the same.

The answer is in the next paragraph, so stop reading if you want to find out yourself.

Solution 1
----------

The correct answer is that assertions are the same as a raise exception in a
conditional statement.

.. code-block:: python

   if not x == y:
       raise AssertionError

The thing where this makes a difference, is "-O", which will discard assertions,
but I consider it rarely used. To be really compatible with that, it should be:

.. code-block:: python

   if __debug__ and not x == y:
       raise AssertionError


Quiz Question 2
---------------

But wait, there is slightly more to it. Say you have the following code:

.. code-block:: python

    assert x == y, arg

How can you achieve the same thing, without using the ``assert`` statement at all. The
behavior is required to be absolutely the same.

The answer is in the next paragraph, so stop reading if you want to find out yourself.

Solution 2
----------

This is actually version dependent, due to recent optimizations of CPython.

* For version 2.6 it is as follows:

  The extra value to ``assert``, simply becomes an extra value to raise, which indicates,
  delayed creation of the ``AssertionError`` exception.

  .. code-block:: python

     if not x == y:
         raise AssertionError, arg

* For version 2.7 and higher it is as follows:

  The extra value to ``assert``, simply becomes the argument to creating the ``AssertionError`` exception.

  .. code-block:: python

     if not x == y:
         raise AssertionError( arg )

So, even in the more complex case, you end up with a conditional ``raise``.

The only thing where this makes a difference, is "-O", which will discard assertions,
but I consider it rarely used. To be really compatible with that, it should be:

   .. code-block:: python

       if __debug__ and not x == y:
          raise AssertionError ....

Surprised? Well, yes, there really is nothing to ``assert`` statements. I am using this
for my `Python compiler Nuitka </pages/overview.html>`_ which benefits from having not to
deal with ``assert`` as anything special at all. See also the `respective section in the
Developer Manual </doc/developer-manual.html#the-assert-statement>`_ which explains this
and other things.
