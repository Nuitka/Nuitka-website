
The TL;DR ...
=============

Nuitka is a Python compiler written in Python.

It's fully compatible with Python2 (2.6, 2.7) and Python3 (3.3 .. 3.9).

You feed it your Python app, it does a lot of clever things, and spits out an
executable or extension module.

Free license (Apache).

Okay I'm hooked! Tell me more!
==============================

Now
---

Right now Nuitka is a good replacement for the Python interpreter and compiles
**every** construct that all relevant CPython versions, and even irrelevant ones,
like 2.6 and 3.3 offer. It translates the Python into a C program that then is
linked against ``libpython`` to execute in the same way as CPython does, in a very
compatible way.

It is somewhat faster than CPython already, but currently it doesn't make all
the optimizations possible, but a 312% factor on pystone is a good start (number
is from version 0.6.0 and Python 2.7), and many times this is not generally
achieved yet.

Future
------

In the future, Nuitka will be able to use type inference and guessing by doing
whole program analysis and then applying the results to perform as many
calculations as possible. It will do this - where possible - without accessing
``libpython`` but in C with its native data types.

It will also be possible to integrate ``ctypes`` based bindings without the normal
speed penalty (the compiled program will call the C library directly without the
use of ``ctypes`` run time).

And finally you will be able to use a ``hints`` module to tell Nuitka about type
information that it cannot guess.

Now vs. Future or The Plan
--------------------------

It's a road with milestones.

1. Feature parity with Python, understand all the language construct and behave
   absolutely compatible.

2. Create the most efficient native code from this. This means to be fast with
   the basic Python object handling.

3. Then do constant propagation, determine as many values and useful constraints
   as possible at compile time and create more efficient code.

4. Type inference, detect and
   special case the handling of strings, integers, lists in the program

5. Add interfacing to C code, so Nuitka can turn a ``ctypes`` binding into an
   efficient binding as written with C.

6. Add hints module with a useful Python implementation that the compiler can
   use to learn about types from the programmer.

Where is it now?
----------------

Well milestone 1, feature parity has been reached for Python 2.6, 2.7, and
3.x up to 3.9 was mastered. There is no way, this could be any better, but
with every new Python release, there is a lot of new things to add.

With milestone 2, it is considered reached. Nuitka is more than 2 times faster
than CPython because of this. While this is certainly not going to give the
anywhere near the biggest gains possible, these are solid improvements that can
only help the goal to be as fast as possible. Even in final Nuitka, not all
objects will always be correctly type inferenced and then the quality of
milestone 2 will be able to *still* be faster than CPython.

Aiming at milestone 3, the constant folding and propagation is in place. Some
control flow optimization are applied too. But this only at a start. It will
give the big gains when types are inferred.

For milestone 4, first steps have been undertaken to achieve "type
inference". The results are encouraging, but will need a lot more work, before
they can be made the default approach.

And milestone 5+6 are not even started. So way to go until we hit the "future".

In the meantime you will find its `latest version here </pages/download.html>`_.
