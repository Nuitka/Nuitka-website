:orphan:

################################
 Build failure in C with Nuitka
################################

****************************
 The Problem in a Few Words
****************************

Nuitka uses a "Backend C" compiler to create program code. That applies
to all outputs: extension modules, accelerated binaries, standalone, or
onefile. During this final phase, a compilation error occurred.

************
 Background
************

When generating the C code, things can go wrong, and when the C compiler
looks at generated, correct code, things can also go wrong. You seem to
have encountered this now.

Nuitka has requirements for the C part of the compilation, namely a
supported C compiler.

*************
 Consequence
*************

There are no easy workarounds, and the result is that Nuitka will not
produce a result and complains about this. You need to follow the
recommendations below.

****************
 Recommendation
****************

Make sure only to use a supported C compiler. Most often, the problem is
caused by using the wrong C compiler, so check :ref:`C Compiler
<nuitka-requirements>` out.

But when then you still have C compiler errors, they can also come from
lack of disc space, from lack of system memory or other external
factors.

It assumed that network drives do work. "Chinese" characters in build
paths and module names are believed to be handled correctly. However,
this can occur. Make sure you avoid having those, and if that helps,
make sure to report the issue so we can improve it.

***********
 Reporting
***********

However, sometimes specific code constructs after optimization by Nuitka
can trigger warnings and errors that have not yet been seen and warrant
a correction in Nuitka. If that is the case, isolate the code in a
minimal reproducer.
