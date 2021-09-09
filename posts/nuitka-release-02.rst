This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

Good day, this is a major step ahead, improvements everywhere.

***********
 Bug fixes
***********

-  Migrated the Python parser from the deprecated and problematic
   ``compiler`` module to the ``ast`` module which fixes the ``d[a,] =
   b`` parser problem. A pity it was not available at the time I
   started, but the migration was relatively painless now.

-  I found and fixed wrong encoding of binary data into C++ literals.
   Now Nuitka uses C++0x raw strings, and these problems are gone.

-  The decoding of constants was done with the ``marshal`` module, but
   that appears to not deeply care enough about unicode encoding it
   seems. Using ``cPickle`` now, which seems less efficient, but is more
   correct.

-  Another difference is gone: The ``continue`` and ``break`` inside
   loops do no longer prevent the execution of finally blocks inside the
   loop.

****************
 Organizational
****************

-  I now maintain the "README.txt" in org-mode, and intend to use it as
   the issue tracker, but I am still a beginner at that.

   .. admonition:: Update

      Turned out I never master it, and used ReStructured Text instead.

-  There is a public git repository for you to track Nuitka releases.
   Make your changes and then ``git pull --rebase``. If you encounter
   conflicts in things you consider useful, please submit the patches
   and a pull request. When you make your clones of Nuitka public, use
   ``nuitka-unofficial`` or not the name ``Nuitka`` at all.

-  There is a now a mailing list (since closed).

*********************
 Reduced Differences
*********************

-  Did you know you could write ``lambda : (yield something)`` and it
   gives you a lambda that creates a generator that produces that one
   value? Well, now Nuitka has support for lambda generator functions.

-  The ``from __future__ import division`` statement works as expected
   now, leading to some newly passing CPython tests.

-  Same for ``from __future__ import unicode_literals`` statement, these
   work as expected now, removing many differences in the CPython tests
   that use this already.

**************
 New Features
**************

-  The ``Python`` binary provided and ``Nuitka.py`` are now capable of
   accepting parameters for the program executed, in order to make it
   even more of a drop-in replacement to ``python``.

-  Inlining of ``exec`` statements with constant expressions. These are
   now compiled at compile time, not at run time anymore. I observed
   that an increasing number of CPython tests use exec to do things in
   isolation or to avoid warnings, and many more these tests will now be
   more effective. I intend to do the same with eval expressions too,
   probably in a minor release.

*********
 Summary
*********

So give it a whirl. I consider it to be substantially better than
before, and the list of differences to CPython is getting small enough,
plus there is already a fair bit of polish to it. Just watch out that it
needs gcc-4.5 or higher now.
