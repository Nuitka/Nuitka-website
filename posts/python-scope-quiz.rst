Quiz Question
-------------

Say you have the following module code:

.. code-block:: python

    a = 1

    class some_class():
        a = a

    def some_function():
        a = a

    some_class()
    some_function()


What is going to happen? Well, think about it, the solution is in the next paragraph.

Solution
--------

The correct answer is that the call "some_function()" is going to give you a
"UnboundLocalError" exception.

This is because it in functions unlike in classes (or modules) do look ahead for assigned
to variable names. Python allocates a slot for local variables of functions and that is a
property that doesn't change - unless you say "global" of course. This slot is used for
every access to the variable name, which forbids you to make it local.

Surprised? I was too! I only learned it while doing my `Python compiler Nuitka
</pages/overview.html>`_ and I made it a separate posting, because it really
surprised me how different function body and class body work.
