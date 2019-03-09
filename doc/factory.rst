
Factory Rationale
=================

Both the ``master`` and ``develop`` branch are supposed to be working
for people at all times. For experiments in the context of issues and
generally features not yet ready for prime time, there is factory.

You have probably come here, because you were asked to checkout a
change made for you on ``factory``.

How to get
==========

git
---

.. code-block:: sh

   git clone --branch factory http://git.nuitka.net/Nuitka.git

pip
---

.. code-block:: sh

   pip install -U "http://nuitka.net/gitweb/?p=Nuitka.git;a=snapshot;h=refs/heads/factory;sf=tgz"

Word of Warning
===============

The factory may include all kinds of stupid mistakes, e.g. not being executable
with all versions, crashing, not working at all. So please use it only for the
issue at hand or even more than usually on your own risk. Once confirmed, fixes
will normally appear in either hotfixes or pre-releases shortly.
