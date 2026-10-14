:orphan:

################################################
 Nuitka is older than the latest stable release
################################################

****************************
 The Problem in a Few Words
****************************

The Nuitka version used for your compilation is older than the latest
stable release available on PyPI. Most stable releases are hotfixes that
resolve bugs, so remaining on an older version means you keep bugs that
are already known and already fixed. By default, Nuitka checks for a
newer release once a week and informs you when one exists.

************
 Background
************

Nuitka issues a stable release on a regular basis. After a release such
as ``4.3``, hotfix releases like ``4.3.1``, ``4.3.2`` and so on are made
to resolve bugs reported by users. These are usually not about new
features, but corrections for bugs that you may well be hitting, which
makes staying up to date particularly valuable.

Versions between stable releases are typically release candidates. A
release candidate such as ``4.3rc9`` is considered older than the final
``4.3`` release, since it is not final. So even when you run a recent
release candidate, you can see this message once the final release is
out.

The latest stable version is obtained from PyPI. Because this requires
network access, the result is cached for a week, and when the network is
unavailable, previously cached information is used instead. This check
can be controlled with the ``--update-check`` option or the
``NUITKA_UPDATE_CHECK`` environment variable.

*********
 Example
*********

.. code::

   Nuitka:WARNING: Nuitka '4.3rc9' is older than the latest stable release '4.3'.
   Nuitka:WARNING:     Complex topic! More information can be found at
   Nuitka:WARNING: https://nuitka.net/info/outdated-nuitka-version.html

*************
 Consequence
*************

The most important consequence is that bug fixes from the hotfix
releases you skipped are not in effect for you. Problems you encounter
may be exactly those that were already fixed in a release you did not
install, and issues you report may already have been resolved. Beyond
that, you may also be missing support for newer Python versions and
newly added features.

Because of this, "it works after an upgrade" is by far the most common
reason that a reported problem turns out not to be reproducible.

****************
 Recommendation
****************

Upgrade Nuitka to the latest stable release, and in particular, do not
skip the hotfix releases. Depending on how you installed it, one of the
following should work:

.. code:: bash

   pip install --upgrade nuitka

.. code:: bash

   python -m pip install --upgrade nuitka

If you installed Nuitka with a system package manager, use that instead.

If you cannot upgrade for a good reason, you can make Nuitka stay quiet
about this with the ``--update-check=never`` option or by setting the
``NUITKA_UPDATE_CHECK`` environment variable to ``never``. Use
``--update-check=error`` to make outdated versions abort the compilation
instead.
