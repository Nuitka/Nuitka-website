#####################
 Letting go of C++11
#####################

This post is about Nuitka the Python compiler started out using C++0x
which is now C++11, and then chose to stop it.

******************
 In the Beginning
******************

Very early on, when I considered how to generate code from the node
tree, in a way, that mistakes should practically be impossible to make,
I made the fundamental decision, that every Python expression, which
produces temporary variables, should become an expression in the
generated code too.

.. note::

   That is my choice, I think it keeps code generation more simple, and
   easier to understand. There may come a separate post about how that
   played out.

That decision meant some trouble. Certain things were not easy, but
generally, it was achievable for g++ relatively quickly, and then lots
of helper functions would be needed. Think of ``MAKE_TUPLE`` and
``MAKE_DICT``, but also other stuff needed that. Calling a Python
built-in with variable number of parameters e.g. could be implemented
that way easily.

Other nice things were ``enum`` classes, and generally good stuff. It
was really quick to get Nuitka code generation off the ground this way.

..
   note:

   And it made the project slightly more interesting, and feel bleeding edge. If you
   follow the project, you know that decision are naturally very conservative, and this
   one was not.

*****************
 Reality Strikes
*****************

But then, as time went on, I found that the order of evaluation was
becoming an issue. It became apparent that for more and more things, I
needed to reverse it, so it works. Porting to ARM, it then became clear,
that it needs to be the other way around for that platform. And checking
out clang, which is also a C++11 compiler, I noticed, this one yet uses
a different one.

So, for normal functions, I found a solution that involves the
pre-processor to reverse or not, *both* function definition and call
sites, and then it is already correct.

This of course, doesn't work for C++11 variadic functions. So, there
came a point, where I had to realize, that each of its uses was more or
less causing evaluation order bugs. So that most of their uses were
already removed. And so I basically knew they couldn't stay that way.

****************
 Other Features
****************

Also, things I initially assumed, e.g. that lambda functions of C++11
may prove useful, or even "auto", didn't turn out to be true. There
seemingly is a wealth of new features, besides variadic templates that I
didn't see how Nuitka would benefit from it at all.

************
 New Wishes
************

Then, at Europython, I realized, that Android is still stuck with
g++-4.4 and as such, that an important target platform will be
unavailable to me. This platform will become even more important, as I
intend to buy an device now.

***********
 Biting it
***********

So what I did, was to remove all variadic functions and instead generate
code for them as necessary. I just need to trace the used argument
counts, and then provide those, simple enough.

Also, other things like deleted copy constructors, and so on, I had to
give up on these a bit.

This change was probably suited to remove subtle evaluation order
problems, although I don't recall seeing them.

*************
 The Present
*************

The current stable release still requires C++11, but the next release
will work on g++-4.4 and compiles fine with MSVC from Visual Studio
2008, although at this time, there is still the issue of generators not
working yet, but I believe that ought to be solvable.

The new requirement is only C++03, which means, there is a good chance
that supporting Android will become feasible. I know there is interest
from App developers, because there, even the relatively unimportant 2x
speedup, that Nuitka might give for some code, may matter.

************
 Conclusion
************

So that is a detour, I have taken, expanding the base of Nuitka even
further. I felt, this was important enough to write down the history
part of it.
