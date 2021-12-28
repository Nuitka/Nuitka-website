######################
 Nuitka this week #12
######################

.. contents::

**************************
 Communication vs. Coding
**************************

Over the holiday season I sort of neglected these postings, but there
are other fields, where I have put my focus, but I think these postings
are now going to resume.

A quick update in a while in an eternally fluent situation, and not too
polished.

*******************
 Optimization Work
*******************

So, the 0.6.2 optimization work has been not a lot yet. I started some
work on ``int``/``long`` C type and it looked good.

*******************
 Week of Bugfixing
*******************

So I did this, and it turned out rather long. I continued fixing things
and finishing up open things to the point that it now is clean. I hate
to be falling behind. I am touching on a few more interesting topics.

************************
 Python flag -O and -OO
************************

Nuitka was supporting `-O` but doing what should only the done for `-OO`
which I only learned of now. So this is going to be supported both now.

*********************
 Virtualenv vs. venv
*********************

Accelerated binaries were not running with full ``sys.path`` in the
virtualenv, because ``site`` module uses ``sys.prefix`` and that was not
propagated,but it now is.

**********************************
 Google Summer of Code for Nuitka
**********************************

So the GSoC 2019 page is shaping up, the pull request to list Nuitka on
the PSF project pages has been merged. More tweaking will be needed to
get into perfect shape, and that has been my main communication time
effort.

Finally somebody had stepped up for mentor, which means a lot to me. Now
we need to see if students are willing to pick us.

And because I publish this too late. Already a bunch of stundents are
showing interest and are hacking on Nuitka, which keeps me even more
busy, and makes me extremely happy.

*********************
 Nuitka Organisation
*********************

The Nuitka organisation on Github was introduced for my a while ago, and
I had transferred the ownership of the Nuitka repository to there.
Having moved the issue tracking to there, I was going more all in on it.

Recently more people have submitted PRs and with incredible quality and
willingness to support it even after merge of their PR. No dry by
contribution, but people looking to actually improve Nuitka together
with me.

Therefore I welcome Orsiris and Jorj on board and am really happy about
it.

**********************************
 Windows Dependencies from pefile
**********************************

So Orsiris de Jong implemented a replacement for the dependency walker
based code to scan DLLs for Windows standalone using the `pefile`
module, which is likely way better at this. For starters it's
experimental in the next release, but I expect it to soon become the
default.

****************
 Tkinter Plugin
****************

And Jorj X. McKie implemented a Windows Tkinter plug-in that deals with
copying of the TCL installation and integrating it with Nuitka
standalone for distribution.

That is very nice and seems to affect a lot of people using that GUI
style it seems.

**************
 Numpy Plugin
**************

And Jorj X. McKie also implemented a NumPy plug-in that deals with the
various acceleration methods there are, e.g. MKL, Blas, I have no idea.
It copies the needed DLLs along and makes sure that `numpy` stays fast
in standalone mode.

*********
 Twitter
*********

I continue to be very active there.

`Follow @kayhayen <https://twitter.com/kayhayen?ref_src=twsrc%5Etfw>`_

And lets not forget, having followers make me happy. So do re-tweets.

Adding Twitter more prominently to the web site is something that is
also going to happen.

*************
 Help Wanted
*************

If you are interested, I am tagging issues `help wanted
<https://github.com/kayhayen/Nuitka/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22>`_
and there is a bunch, and very likely at least one *you* can help with.

Nuitka definitely needs more people to work on it.

***********
 Donations
***********

If you want to help, but cannot spend the time, please consider to
donate to Nuitka, and go here:

`Donate to Nuitka <http://nuitka.net/pages/donations.html>`_
