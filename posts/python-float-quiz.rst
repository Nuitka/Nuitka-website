###############
 Quiz Question
###############

Say you have the following code:

.. code:: python

   assert type(s) is str
   x = float(s)
   if x != x:
       print "Bad bad float!"

What value of "s" and then "x" can make the code complain? Do you see
the really bad side of it?

The answer is in the next paragraph, so stop reading if you want to find
out yourself.

##########
 Solution
##########

The correct answer is that there is one float that is not equal to
itself and that is float("nan"). Which I find terrible. It is so bad, it
spoils set, dict, and everything there is. Any container that has it
inside is no longer equal to itself.

Surprised? I was too! I only learned it while doing my `Python compiler
Nuitka </pages/overview.html>`_ and I made it a separate posting,
because it really surprised me how this could possibly happen. A builtin
type that breaks fundamental assumptions like "x == x".
