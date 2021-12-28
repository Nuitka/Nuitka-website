#########################
 Try Finally Python Quiz
#########################

When working on my Python compiler Nuitka, I often come across
ridiculous language details of the Python language, and turn these into
quizzes, for which I finally added a `dedicated quiz tag
</categories/quiz.html>`__.

Anyway, who can predict, what these will do to you:

.. code:: python

   def f():
       try:
           return 1
       finally:
           return 2

Will it return ``1`` or ``2`` ?

.. code:: python

   def f():
       try:
           1 / 0
       finally:
           return 2

Will this raise an ``ZeroDivisionError`` or return ``2`` ?

.. code:: python

   def f():
       while 1:
           try:
               continue
           finally:
               break

Is this an endless loop or does it return?

.. code:: python

   def f():
       while 1:
           try:
               break
           finally:
               continue

What about that? This one holds an inconsistency.

No solutions yet this time.
