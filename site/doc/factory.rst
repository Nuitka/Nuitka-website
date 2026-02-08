:orphan:

######################
 Factory Instructions
######################

*******************
 Factory Rationale
*******************

You have probably come here because you want to test a **Nuitka** change
made for you on ``factory`` branch or its **Nuitka Commercial**
counterpart, the ``staging`` branch.

Both the ``main`` and ``develop`` branches of **Nuitka** should always
be working correctly. For experiments in the context of issues and new
features not yet ready for prime time, we use the ``factory`` branch.

The ``staging`` branch of **Nuitka Commercial** is generally only
updated when ``factory`` can be assumed to be relatively good, but also
when commercial users get asked to test corrections, so tread with
caution there as well.

********************************************
 How do you get ``factory`` or ``staging``?
********************************************

|Factory Status|

git
===

.. code:: bash

   # Standard version:
   git clone --branch factory https://github.com/Nuitka/Nuitka.git
   # Commercial version (subscribers only)
   git clone --branch staging https://github.com/Nuitka/Nuitka-commercial.git

Either run ``bin/nuitka`` from the checkout, and it will use the Nuitka
code right next to it, or run ``python setup.py develop`` to create a
``.pth`` file that works like a symlink. That means if you update the
git, Nuitka is automatically updated in your environment, too.

Of course ``python setup.py install`` also works, but copies **Nuitka**
into the environment and needs to be redone for every git update.

pip
===

.. code:: bash

   # With "python" being the version where you want to install Nuitka

   # Standard version with minimal dependencies:
   python -m pip install -U --force-reinstall "https://github.com/Nuitka/Nuitka/archive/factory.zip"
   # Standard version with onefile/app dependencies:
   python -m pip install -U --force-reinstall "Nuitka[app] @ https://github.com/Nuitka/Nuitka/archive/factory.zip"
   # Standard version with all dependencies:
   python -m pip install -U --force-reinstall "Nuitka[all] @ https://github.com/Nuitka/Nuitka/archive/factory.zip"
   # Commercial version with minimal dependencies (subscribers only)
   python -m pip install -U --force-reinstall "https://github.com/Nuitka/Nuitka-commercial/archive/staging.zip"
   # Commercial version with onefile/app dependencies (subscribers only):
   python -m pip install -U --force-reinstall "Nuitka[app] @ https://github.com/Nuitka/Nuitka-commercial/archive/staging.zip"
   # Commercial version with all dependencies (subscribers only):
   python -m pip install -U --force-reinstall "Nuitka[app] @ https://github.com/Nuitka/Nuitka-commercial/archive/staging.zip"

**********************
 When is it released?
**********************

When the ``factory`` branch is stable and about one week old, it's time
to release a new hotfix; we then distribute its contents to ``main`` and
``develop`` branches depending on suitability. They become part of the
hotfix or the new pre-release at that point.

Usually, there is a new hotfix every one or two weeks. But before a new
**Nuitka** release comes out, they might stop for a while, as with the
next release being so close wouldn't matter much.

For invasive fixes that are critical, they can become release triggers,
certainly, if **Nuitka Commercial** customers with priority support are
affected.

**********************************
 Subscribing to Nuitka Commercial
**********************************

You may also learn more about :doc:`Nuitka Commercial </doc/commercial>`
offering.

If you want to have better protection of your IP or just more robust
updates sooner, then you can purchase **Nuitka Commercial**. You, of
course, also reward the responsive support given.

*****************
 Word of Warning
*****************

The ``factory`` branch of **Nuitka** may include all kinds of stupid
mistakes; for example, not being executable with all **Python**
versions, crashing and not working at all.

They also frequently change without notice and nearly always as a ``git
rebase``. So please use it only for the issue at hand or even more than
usual at your own risk.

Once confirmed and found suitable, fixes will typically appear on
``develop`` or ``main`` branch relatively shortly, so try to use those
instead once possible. To keep using ``factory`` is asking for trouble,
and it may have issues you have not noticed yet.

The recommendation about the ``staging`` branch of **Nuitka Commercial**
is slightly less strict, but it's best to treat it the same, even if
with the best efforts to keep it more stable, there will be mistakes.

.. |Factory Status| image:: https://github.com/Nuitka/Nuitka/actions/workflows/testing.yml/badge.svg?branch=factory
   :target: https://github.com/Nuitka/Nuitka/actions/workflows/testing.yml?query=branch%3Afactory
