######################
 Factory Instructions
######################

*******************
 Factory Rationale
*******************

Both the ``master`` and ``develop`` branch are supposed to be working
for people at all times. For experiments in the context of issues and
generally features not yet ready for prime time, there we have the
factory branch.

You have probably come here, because you were asked to checkout a change
made for you on ``factory``.

************************
 How to get ``factory``
************************

|Factory Status|

git
===

.. code:: bash

   git clone --branch factory https://github.com/Nuitka/Nuitka.git

pip
===

.. code:: bash

   pip install -U --force-reinstall "https://github.com/Nuitka/Nuitka/archive/factory.zip"

*****************
 Word of Warning
*****************

This personal branch may include all kinds of stupid mistakes, e.g. not
being executable with all versions, crashing, not working at all. They
also frequently change without notice. So please use it only for the
issue at hand or even more than usually on your own risk.

Once confirmed and found good, fixes will normally appear on develop
branch relatively shortly, try to use those instead from then on, and
wait for the change to appear there.

.. |Factory Status| image:: https://github.com/Nuitka/Nuitka/actions/workflows/testing.yml/badge.svg?branch=factory
   :target: https://github.com/Nuitka/Nuitka/actions/workflows/testing.yml?query=branch%3Afactory
