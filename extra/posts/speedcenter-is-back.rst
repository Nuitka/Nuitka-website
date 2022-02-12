.. post:: 2012/06/30 16:39
   :tags: compiler, Nuitka, Nikola, Python, benchmark
   :author: Kay Hayen

############################
 Nuitka Speedcenter is back
############################

Once a long time ago, I was benchmarking Nuitka more often. Check `"What
is Nuitka?" </pages/overview.html>`_ in case you don't know what it
is.

*********
 Problem
*********

And I was considering the use of codespeed, and had some data online.
But ultimately, it got discontinued. This has 3 reasons:

-  Moved the website to a dedicated machine, which broke the previous
   install.

-  Controlling which data is used for display was hard and not
   satisfactory.

   #. For example, I didn't want to have to commit and push, just to let
      the benchmarks run.

   #. And I wanted to be able to re-run benchmarks with newer compiler,
      even newer Python, but old Nuitka. Using g++ 4.6 over g++ 4.5
      should not impact the data.

   #. It turned out to be a nightmare to migrate to newer codespeed
      versions. I found myself starting from empty database - over and
      over.

   #. Many things were not supported.

      For example, I would want to collect all PyBench results, but only
      publish those who are expressive. That seemed difficult to
      achieve.

-  Benchmarks of Nuitka are not yet useful

   #. Nuitka was not yet doing type inference

   #. Most of the work was aimed at correctness, and effectively was
      often degrading performance even if only temporary. Seeing it
      wouldn't have been too motivating.

**********
 Solution
**********

I have simply created a small wrapper:

#. Small script to run benchmarks and collect data.

   It checks out Nuitka in all versions in a playground, and then runs
   defined benchmarks, with valgrind, etc. taking exe sizes, etc.

#. Data is stored in local sqlite databases.

   I have a database per machine, i.e. a distributed repository, where I
   collect information. That works for me, and will allow me to compare
   different kinds of machines.

   The advantage is that I have no risk of data loss anymore, and no
   issues and difficulty with poor interfaces to replace existing data.

#. Data is merged on one machine, and then pushed.

   That allows me to inspect the changes before publishing them. It
   allows me to play with local commits, branches, with information that
   will go away. I can then push when I choose to.

That integrates better with my work flow. It allows me to retro-fit
benchmarks results on the machine and to be tool independent.

In principle, I could publish the data in other forms as well, and I
likely will. Making tables of e.g. PyBench results seems like one
application. Recently, I have worked with Nikola, and could also imagine
to integrate Codespeed graph functionality (which is apparently all I
want) to there.

|  Yours,
|  Kay
