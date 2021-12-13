############################
 Nuitka the Python Compiler
############################

Nuitka is a Python compiler written in Python.

It is fully compatible with Python2 (2.6, 2.7) and Python3 (3.3 - 3.9).

You feed Nuitka your Python app, it does a lot of clever things, and
spits out an executable or extension module.

Nuitka is distributed under the Apache license.

********************************
 Okay I'm hooked! Tell me more!
********************************

Now
===

Right now Nuitka is a good replacement for the Python interpreter. It
compiles **every** language construct in all relevant CPython versions,
and even the irrelevant ones like 2.6 and 3.3. It translates Python into
a C program that then is linked against libpython to execute exactly
like CPython. It is extremely compatible.

Nuitka is already slightly faster than CPython, but there is work to be
done to include as many C optimizations as possible. We currently get a
335% speedup in pystone, which is a good start. (source: Nuitka version
0.6.17 with Debian Python 2.7)

Future
======

In the future Nuitka will be able to use type inferencing based on whole
program analysis. It will apply that information in order to perform as
many calculations as possible in C, using C native types, without
accessing ``libpython``.

Nuitka will also be able to integrate ``ctypes`` bindings, but without
the usual speed penalty. The compiled program can call the C library
directly, avoiding run-time overhead.

And finally, you will be able to use a ``hints`` module to inform Nuitka
about type information.

Now vs. Future, or, The Plan
============================

These are the milestones and priorities for Nuitka's development.

#. Total feature parity with Python. Understand all language constructs,
   and behave exactly like CPython.

#. Create the most efficient native C code possible. The goal is to make
   basic Python object handling as fast as possible.

#. Implement constant propagation. Determine as many values and useful
   constraints as possible at compile time, and create extremely
   efficient code for the compiler.

#. Make intelligent type inferences. Detect and use special case
   handling for strings, integers, and lists in the compiled program.

#. Add interfacing with C code to allow Nuitka to turn Python ``ctypes``
   bindings into efficient C bindings.

#. Provide a hints module with a useful Python implementation so the
   compiler can learn about intended types directly from the programmer.

Where are we now?
=================

Milestone 1, feature parity, has been achieved for Python 2.6, 2.7, and
3.3 up to 3.9. This part of Nuitka is already mature, but every new
Python release has lots of new features to add!

Milestone 2 is always a work in progress, but it has been quite
successful. Nuitka can already produce code that is more than 2 times
faster than CPython. These gains are nowhere near the best gains
possible, but they are solid improvements and will improve further.

Milestone 3, constant folding and propagation, is already in place, and
some control flow optimizations are also applied - but this is just the
start. Constant folding will see big gains as the type inferencing
matures and more variables are opened up to become constants.

For milestone 4 the first steps are in place achieve type inferencing.
The results are encouraging, but it will need a lot more work before
this can be made the default approach. Remember that this is still
Python, Nuitka cannot be guaranteed to perfectly guess type information.

We have yet to start on milestones 5 and 6. There is still quite a way
to go until we hit the "future".

In the meantime you can find its `latest version here
</pages/download.html>`_.

.. toctree::
   :caption: Manuals
   :hidden:

   User Manual <user-manual>
   Developer Manual <developer-manual>

.. toctree::
   :caption: Commercial Users
   :hidden:

   commercial

.. toctree::
   :caption: Changelog
   :hidden:

   Changelog
   Roadmap <roadmap>

.. toctree::
   :caption: Downloads
   :hidden:

   Downloads <download>

.. toctree::
   :caption: API doc
   :hidden:

   api-doc

.. toctree::
   :caption: Credits
   :hidden:

   Credits

.. toctree::
   :caption: Impressum
   :hidden:

   Impressum

.. .. toctree::
..    :caption: Factory Instructions
..    :hidden:

..    factory
