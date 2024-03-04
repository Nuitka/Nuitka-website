:orphan:

################################
 Build failure in C with Nuitka
################################

****************************
 The Problem in a few Words
****************************

Nuitka is using a "Backend C" compiler to create program code, be it
extension modules, accelerated binaries, standalone or onefile. During
this phase a compilation error occurred.

************
 Background
************

When generating the C code things can go wrong, and when the C compiler
looks at generated, correct code, things can also go wrong. You seem to
have encountered this now.

Nuitka has requirements for the C part of the compilation, namely a
supported C compiler.

*************
 Consequence
*************

There are no easy workarounds, the result is that Nuitka will not
produce a result and complains about this. You need to follow the
recommendations below.

****************
 Recommendation
****************

Make sure to only use a supported C compiler. Nuitka is not ready to
just use any of them, esp. not on Windows, but also quite generally.
Check the respective section in :doc:`/doc/user-manual` out.

But when you have C compiler errors, they can come from lack of disc
space, from lack of memory, or other external factors.

It is e.g. believed solved that network drives do not work. Chinese
characters in build paths and modules are believed to be dealt with
correctly. However, this can occur. Make sure you are not having those,
and if that helps, make sure to report the issue, such that it can be
solved.

More often that not though, the problem is caused by using the wrong C
compiler. If you please, you are in fact using one, make sure to report
it.

***********
 Reporting
***********

However, sometimes specific code constructs after optimization by Nuitka
can trigger warnings and errors that have not yet been seen and warrant
a correction in Nuitka. If that is the case, make sure to isolate the
code in a minimal reproducer.
