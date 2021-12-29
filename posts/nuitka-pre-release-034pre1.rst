.. post:: 2010/12/06 23:27
   :tags: compiler, git, Nuitka, Python
   :author: Kay Hayen

##############################
 Nuitka Pre-Release 0.3.4pre1
##############################

This pre-release of Nuitka has a focus on re-organizing the Nuitka
generated source code. Please see the page `"What is Nuitka?"
</pages/overview.html>`_ for clarification of what it is now and what it
wants to be.

For a long time, Nuitka has generated a single C++ file, even when
embedding many modules into one. And it has always showed that the GNU
g++ compiler clearly has exponential compile time behavior when
translating these into the executable.

This is no more the case. So this pre-release is mainly about making the
``--deep`` feature useful. Before the release, I may look into
optimizations for speed again. Right now time is very short due to day
job reasons, so this pre-release is also about allowing people to use
the improvements that I have made and get some feedback about it.

***********
 Bug fixes
***********

-  None at all. Although I am sure that there may be regressions on the
   options side. The tests of CPython 2.7 all pass still, but you may
   find some breakage.

**********
 Cleanups
**********

-  Static helpers source code has been moved to ".hpp" and ".cpp" files,
   instead of being in ".py" files.

-  Generated generated code for each module is now a separate file.

-  Constants etc. go to their own file (although not named sensible yet)

**************
 New Features
**************

-  Uses Scons to make the build.

***********
 New Tests
***********

-  I have added ExtremClosure from the Python quiz. I feel it was not
   covered by existing tests yet.

****************
 Organizational
****************

-  There is now a new environment variable "NUITKA_SCONS" which should
   point to the directory with the Scons file for Nuitka.

-  The ``create-environment.sh`` can now be sourced (if you are in the
   top level directory of Nuitka) or be used with eval. In either case
   it also reports what it does.

*********
 Numbers
*********

None at this time. It likely didn't change much at all. And I am not yet
using the link time optimization feature of the g++ compiler, so
potentially it should be worse than before at max.

This release will be inside the "git" repository only. Check out `latest
version here <../pages/download.html>`_ to get it.

|  Yours,
|  Kay Hayen
