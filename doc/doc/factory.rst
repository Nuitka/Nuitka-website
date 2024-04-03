:orphan:

######################
 Factory Instructions
######################

*******************
 Factory Rationale
*******************

You have probably come here, because you were asked to checkout a change
made for you on ``factory`` or its commercial counterpart ``staging``
branch.

Both the ``main`` and ``develop`` branch are supposed to be working for
people at all times. For experiments in the context of issues and
generally features not yet ready for prime time, there we have the
factory branch. The staging branch is generally only updated when
factory is assumed to be relatively good, but tread with caution there
as well.

****************************************
 How to get ``factory`` or ``staging``.
****************************************

|Factory Status|

git
===

.. code:: bash

   # Standard version:
   git clone --branch factory https://github.com/Nuitka/Nuitka.git
   # Commercial version (subscribers only)
   git clone --branch staging https://github.com/Nuitka/Nuitka-commercial.git

Either just run ``bin/nuitka`` from the checkout, and it will use the
install local to it, or run ``python setup.py develop`` which will
create a ``.pth`` file that is kind of like a symlink, i.e. if you
update the git, Nuitka is automatically updated in your environment too.
Of course ``python setup.py install`` does that, but actually copies it
into the environment.

pip
===

.. code:: bash

   # With "python" being the one where you want to install Nuitka into.

   # Standard version:
   python -m pip install -U --force-reinstall "https://github.com/Nuitka/Nuitka/archive/factory.zip"
   # Commercial version (subscribers only)
   python -m pip install -U --force-reinstall "https://github.com/Nuitka/Nuitka-commercial/archive/staging.zip"

**********************
 When it is released?
**********************

Factory only contents gets distributed to ``main`` and ``develop`` when
the time has come to make a new hotfix. Usually there is one every one
or two weeks, but before a new release comes out, they often stop for a
while, with the new release being so close it wouldn't matter much.

Fixes that are not invasive go to a hotfix branch on GitHub first, you
can use that branch if you want. Fixes that are invasive go to develop
at roughly the same time a hotfix is releases, there is usually a day
between that for package builds to be completed.

For invasive fixes that are critical, they might be release triggers,
certainly if Nuitka commercial priority customers are affected.

**********************************
 Subscribing to Nuitka Commercial
**********************************

You may also learn more about `Nuitka Commercial
</doc/commercial.html>`__ offering.

You might want to have better protection of your IP or just more robust
updates sooner, then you can go and purchase Nuitka commercial. You of
course also support the responsive support given.

*****************
 Word of Warning
*****************

The factory branch may include all kinds of stupid mistakes, e.g. not
being executable with all versions, crashing, not working at all. They
also frequently change without notice, and nearly always as a rebase. So
please use it only for the issue at hand or even more than usually on
your own risk.

Once confirmed and found good, fixes will normally appear on develop or
main branch relatively shortly, try to use those instead from then on,
and wait for the change to appear there. To keep using factory is asking
for trouble, and it may have issues you didn't notice.

My recommendation about staging is slightly less strict, but honestly I
recommend to treat it the same even if it is attempted to be kept
stable, there is no way this actually succeeds all the time.

.. |Factory Status| image:: https://github.com/Nuitka/Nuitka/actions/workflows/testing.yml/badge.svg?branch=factory
   :target: https://github.com/Nuitka/Nuitka/actions/workflows/testing.yml?query=branch%3Afactory
