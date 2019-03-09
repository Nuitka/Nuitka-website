
This page attempts to given an overview over the performance history of
Nuitka. It aims to list benchmark results. It's probably also quite bad at it.

.. note::

   This is not comparing Nuitka to CPython yet. It's going to be added, stay
   tuned.

PyStone Valgrind Ticks
======================

Running the "pystone" benchmark for 50000 passes, and measuring the amount of
ticks with Valgrind. It doesn't matter what "pystones" are output, instead the
whole benchmark is measured.

The idea of using Valgrind is to get reliable results, without any system
perturbation. It gives good measurements and makes even tiny effects visible. On
purpose, the ticks for initialization are not counted, i.e. the tick counter
starts only when the main module is entered, not when the compiled types and
constant values are prepared.

Of course, "pystone" code exercises not a whole lot of Python features, esp. no
modern ones at all. Still it's a nice indicator. It will benefit most from quick
module variable access, quick instance attribute access and function call
performance, etc.

.. image:: images/pystone-nuitka.svg
   :target: images/pystone-nuitka.svg

.. include:: pages/tables/pystone-nuitka.inc

PyStone Binary Size
===================

The size of the created binary is also an interesting figure of course. While we
are very willing to trade performance for executable size, there should be some
gain. More code may also mean worse cache performance.

This is a by-product of the above PyStone valgrind based test. It's a pretty
automatic result, and an interesting indicator for generated code complexity.

.. image:: images/pystone-binary-nuitka.svg
   :target: images/pystone-binary-nuitka.svg

.. include:: pages/tables/pystone-binary-nuitka.inc

PyStone Peak Memory Usage
=========================

The peak ``malloc`` memory of the resulting binary. While we are willing to
trace memory usage over performance, often higher memory usage leads to lower
performance, because e.g. two objects that could be shared are now
duplicated. Reducing memory usage means to share more objects and consequently
better performance.

This is a by-product of the above PyStone valgrind based test. It's a pretty
automatic result, and an interesting indicator for memory leaks or avoided
objects.

.. image:: images/pystone-memory-nuitka.svg
   :target: images/pystone-memory-nuitka.svg

.. include:: pages/tables/pystone-memory-nuitka.inc
