:orphan:

###########
 Donations
###########

Should you feel that you cannot help Nuitka directly, but still want to
support, please consider `making a donation
<https://nuitka.net/pages/donations.html>`__ and help this way.

#############
 Join Nuitka
#############

You are more than welcome to join Nuitka development and help to
complete the project in all minor and major ways.

The development of Nuitka occurs in git. We currently have these 3
branches:

-  ``main``

   This branch contains the stable release, to which only hotfixes for
   bugs will be done. It is supposed to work at all times and is
   supported.

-  ``develop``

   This branch contains the ongoing development. It may at times contain
   little regressions, but also new features. On this branch, the
   integration work is done, whereas new features might be developed on
   feature branches.

-  ``factory``

   This branch contains unfinished and incomplete work. It is very
   frequently subject to ``git rebase`` and the public staging ground,
   where my work for develop branch lives first. It is intended for
   testing only, and it's recommended to base any of your own
   development on. When updating it, you will very often get merge
   conflicts. Simply resolve those by doing ``git fetch && git reset
   --hard origin/factory`` and switch to the latest version.

.. note::

   The `Developer Manual
   <https://nuitka.net/doc/developer-manual.html>`__ explains the coding
   rules, branching model used, with feature branches and hotfix
   releases, the Nuitka design and much more. Consider reading it to
   become a contributor. This document is intended for Nuitka users.
