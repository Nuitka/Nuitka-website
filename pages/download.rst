##################
 Nuitka Downloads
##################

*****************
 General
*****************

Thank you for downloading Nuitka. Please consider becoming a subscriber. Downloads are
available below in various formats.

.. raw:: html

    <style>
        .responsive-google-slides {
            position: relative;
            padding-bottom: 56.25%; /* 16:9 Ratio */
            height: 0;
            overflow: hidden;
        }
        .responsive-google-slides iframe {
            border: 0;
            position: absolute;
            top: 0;
            left: 0;
            width: 100% !important;
            height: 100% !important;
        }
    </style>

    <div class="responsive-google-slides">
        <iframe src="https://docs.google.com/presentation/d/e/2PACX-1vSQ8gKXjTPukmeULWnjqSWWOKzopxEQ-LqfPYbvHE4wEPuYTnj3JmYFc8fm-EriAYgXzEbI-kWwaaQN/embed?rm=minimal&start=true&loop=true&delayms=3000" frameborder="0" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
    </div>

The current release is Nuitka |NUITKA_STABLE_VERSION|, during releases,
it might happen that this information lags behind or that there is a new
release not yet announced.

*****************
 Source Archives
*****************

These archives are source and can be used directly after unpacking, simply start with
``bin/nuitka --help`` and read ``README.pdf`` or ``README.rst`` to get started.

Stable Sources
==============

Stable releases are supported with hot fixes.

-  Stable: |NUITKA_STABLE_TAR_GZ|

-  Stable: |NUITKA_STABLE_TAR_BZ|

-  Stable: |NUITKA_STABLE_ZIP|

Development Sources
===================

Develop releases are snapshots of the current ``develop`` branch in git, usually also relatively stable.

-  Develop: |NUITKA_UNSTABLE_TAR_GZ|

-  Develop: |NUITKA_UNSTABLE_TAR_BZ|

-  Develop: |NUITKA_UNSTABLE_ZIP|

**********
 Packages
**********

Windows
=======

-  |WINDOWS_LOGO| Stable MSI Installer:

   .. note::

      The versions of the MSI have a different numbering scheme in their
      filenames, explained in the user manual.

   +---------------+---------------------------+---------------------------+
   | Python        | MSI 64 Bits               | MSI 32 Bits               |
   | Version       |                           |                           |
   +===============+===========================+===========================+
   | Python 2.6    | Not available as MSI      | Not available as MSI      |
   +---------------+---------------------------+---------------------------+
   | Python 2.7    | |NUITKA_STABLE_MSI_27_64| | |NUITKA_STABLE_MSI_27_32| |
   +---------------+---------------------------+---------------------------+
   | Python 3.3    | |NUITKA_STABLE_MSI_33_64| | Not available as MSI      |
   +---------------+---------------------------+---------------------------+
   | Python 3.4    | |NUITKA_STABLE_MSI_34_64| | Not available as MSI      |
   +---------------+---------------------------+---------------------------+
   | Python 3.5    | |NUITKA_STABLE_MSI_35_64| | |NUITKA_STABLE_MSI_35_32| |
   +---------------+---------------------------+---------------------------+
   | Python 3.6    | |NUITKA_STABLE_MSI_36_64| | |NUITKA_STABLE_MSI_36_32| |
   +---------------+---------------------------+---------------------------+
   | Python 3.7    | |NUITKA_STABLE_MSI_37_64| | |NUITKA_STABLE_MSI_37_32| |
   +---------------+---------------------------+---------------------------+
   | Python 3.8    | |NUITKA_STABLE_MSI_38_64| | |NUITKA_STABLE_MSI_38_32| |
   +---------------+---------------------------+---------------------------+
   | Python 3.9    | |NUITKA_STABLE_MSI_39_64| | |NUITKA_STABLE_MSI_39_32| |
   +---------------+---------------------------+---------------------------+

-  |WINDOWS_LOGO| Develop MSI Installer:

   +--------------+-----------------------------+-----------------------------+
   | Python       | MSI 64 Bits                 | MSI 32 Bits                 |
   | Version      |                             |                             |
   +==============+=============================+=============================+
   | Python 2.6   | Not available as MSI file   | Not available as MSI file   |
   +--------------+-----------------------------+-----------------------------+
   | Python 2.7   | |NUITKA_UNSTABLE_MSI_27_64| | |NUITKA_UNSTABLE_MSI_27_32| |
   +--------------+-----------------------------+-----------------------------+
   | Python 3.3   | |NUITKA_UNSTABLE_MSI_33_64| | Not available as MSI file   |
   +--------------+-----------------------------+-----------------------------+
   | Python 3.4   | |NUITKA_UNSTABLE_MSI_34_64| | Not available as MSI file   |
   +--------------+-----------------------------+-----------------------------+
   | Python 3.5   | |NUITKA_UNSTABLE_MSI_35_64| | |NUITKA_UNSTABLE_MSI_35_32| |
   +--------------+-----------------------------+-----------------------------+
   | Python 3.6   | |NUITKA_UNSTABLE_MSI_36_64| | |NUITKA_UNSTABLE_MSI_36_32| |
   +--------------+-----------------------------+-----------------------------+
   | Python 3.7   | |NUITKA_UNSTABLE_MSI_37_64| | |NUITKA_UNSTABLE_MSI_37_32| |
   +--------------+-----------------------------+-----------------------------+
   | Python 3.8   | |NUITKA_UNSTABLE_MSI_38_64| | |NUITKA_UNSTABLE_MSI_38_32| |
   +--------------+-----------------------------+-----------------------------+
   | Python 3.9   | |NUITKA_UNSTABLE_MSI_39_64| | |NUITKA_UNSTABLE_MSI_39_32| |
   +--------------+-----------------------------+-----------------------------+

Debian/Ubuntu/Mint
==================

-  |DEBIAN_LOGO| |UBUNTU_LOGO| |MINT_LOGO| Stable: Debian/Ubuntu/Mint
   repositories

   .. code:: bash

      CODENAME=`egrep 'UBUNTU_CODENAME|VERSION_CODENAME' /etc/os-release | cut -d= -f2`
      if [ -z "$CODENAME" ]
      then
         CODENAME=`lsb_release -c -s`
      fi
      wget -O - http://nuitka.net/deb/archive.key.gpg | apt-key add -
      echo >/etc/apt/sources.list.d/nuitka.list "deb http://nuitka.net/deb/stable/$CODENAME $CODENAME main"
      apt-get update
      apt-get install nuitka

-  |DEBIAN_LOGO| |UBUNTU_LOGO| |MINT_LOGO| Develop: Debian/Ubuntu/Mint
   repositories

   .. code:: bash

      CODENAME=`egrep 'UBUNTU_CODENAME|VERSION_CODENAME' /etc/os-release | cut -d= -f2`
      if [ -z "$CODENAME" ]
      then
         CODENAME=`lsb_release -c -s`
      fi
      wget -O - http://nuitka.net/deb/archive.key.gpg | apt-key add -
      echo >/etc/apt/sources.list.d/nuitka.list "deb http://nuitka.net/deb/develop/$CODENAME $CODENAME main"
      apt-get update
      apt-get install nuitka

   .. note::

      Because Nuitka is part of Debian Stable/Testing/Unstable, a stable
      version is already in the standard repository. This is the only
      way to access the develop version of Nuitka though.

RHEL
====

-  |RHEL_LOGO| Stable: RHEL 6.x Packages: |NUITKA_STABLE_RHEL6| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/home:kayhayen.repo>`__

-  |RHEL_LOGO| Stable: RHEL 7.x Packages: |NUITKA_STABLE_RHEL7| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/home:kayhayen.repo>`__

-  |RHEL_LOGO| Develop: RHEL 6.x Packages: |NUITKA_UNSTABLE_RHEL6| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/home:kayhayen.repo>`__

-  |RHEL_LOGO| Develop: RHEL 7.x Packages: |NUITKA_UNSTABLE_RHEL7| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/home:kayhayen.repo>`__

CentOS
======

-  |CENTOS_LOGO| Stable: CentOS 6.x Packages: |NUITKA_STABLE_CENTOS6| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/home:kayhayen.repo>`__

-  |CENTOS_LOGO| Stable: CentOS 7.x Packages: |NUITKA_STABLE_CENTOS7| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/home:kayhayen.repo>`__

-  |CENTOS_LOGO| Stable: CentOS 8.x Packages: |NUITKA_STABLE_CENTOS8| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_8/home:kayhayen.repo>`__

-  |CENTOS_LOGO| Develop: CentOS 6.x Packages: |NUITKA_UNSTABLE_CENTOS6|
   or `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/home:kayhayen.repo>`__

-  |CENTOS_LOGO| Develop: CentOS 7.x Packages: |NUITKA_UNSTABLE_CENTOS7|
   or `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/home:kayhayen.repo>`__

-  |CENTOS_LOGO| Develop: CentOS 8.x Packages: |NUITKA_UNSTABLE_CENTOS8|
   or `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_8/home:kayhayen.repo>`__

Fedora
======

-  |FEDORA_LOGO| Stable: Fedora 24: |NUITKA_STABLE_F24| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_24/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Stable: Fedora 25: |NUITKA_STABLE_F25| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_25/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Stable: Fedora 26: |NUITKA_STABLE_F26| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_26/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Stable: Fedora 27: |NUITKA_STABLE_F27| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_27/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Stable: Fedora 28: |NUITKA_STABLE_F28| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Stable: Fedora 29: |NUITKA_STABLE_F29| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Stable: Fedora 30: |NUITKA_STABLE_F30| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_30/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Stable: Fedora 31: |NUITKA_STABLE_F31| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_31/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Stable: Fedora 32: |NUITKA_STABLE_F32| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_32/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Stable: Fedora 33: |NUITKA_STABLE_F33| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_33/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Stable: Fedora 34: |NUITKA_STABLE_F34| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_34/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 24: |NUITKA_UNSTABLE_F24| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_24/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 25: |NUITKA_UNSTABLE_F25| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_25/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 26: |NUITKA_UNSTABLE_F26| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_26/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 27: |NUITKA_UNSTABLE_F27| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_27/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 28: |NUITKA_UNSTABLE_F28| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 29: |NUITKA_UNSTABLE_F29| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 30: |NUITKA_UNSTABLE_F30| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_30/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 31: |NUITKA_UNSTABLE_F31| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_31/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 32: |NUITKA_UNSTABLE_F32| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_32/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 33: |NUITKA_UNSTABLE_F33| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_33/home:kayhayen.repo>`__

-  |FEDORA_LOGO| Develop: Fedora 34: |NUITKA_UNSTABLE_F34| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_34/home:kayhayen.repo>`__

Suse
====

-  |SLE_LOGO| Stable: SLE 15: |NUITKA_STABLE_SLE150| or `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/SLE_15/home:kayhayen.repo>`__

-  |SUSE_LOGO| Stable: openSUSE 13.1: |NUITKA_STABLE_SUSE131| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.1/home:kayhayen.repo>`__

-  |SUSE_LOGO| Stable: openSUSE 13.2: |NUITKA_STABLE_SUSE132| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.2/home:kayhayen.repo>`__

-  |SUSE_LOGO| Stable: openSUSE 15.0: |NUITKA_STABLE_SUSE150| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/home:kayhayen.repo>`__

-  |SUSE_LOGO| Stable: openSUSE 15.1: |NUITKA_STABLE_SUSE151| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.1/home:kayhayen.repo>`__

-  |SUSE_LOGO| Stable: openSUSE 15.2: |NUITKA_STABLE_SUSE152| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.2/home:kayhayen.repo>`__

-  |SLE_LOGO| Develop: SLE 15: |NUITKA_UNSTABLE_SLE150| or `repository
   file
   <http://download.opensuse.org/repositories/home:/kayhayen/SLE_15/home:kayhayen.repo>`__

-  |SUSE_LOGO| Develop: openSUSE 13.1: |NUITKA_UNSTABLE_SUSE131| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.1/home:kayhayen.repo>`__

-  |SUSE_LOGO| Develop: openSUSE 13.2: |NUITKA_UNSTABLE_SUSE132| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.2/home:kayhayen.repo>`__

-  |SUSE_LOGO| Develop: openSUSE 15.0: |NUITKA_UNSTABLE_SUSE150| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/home:kayhayen.repo>`__

-  |SUSE_LOGO| Develop: openSUSE 15.1: |NUITKA_UNSTABLE_SUSE151| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.1/home:kayhayen.repo>`__

-  |SUSE_LOGO| Develop: openSUSE 15.2: |NUITKA_UNSTABLE_SUSE152| or
   `repository file
   <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.2/home:kayhayen.repo>`__

Arch
====

-  |ARCH_LOGO| Stable: Arch Linux, execute ``pacman -S nuitka``

-  |ARCH_LOGO| Develop: Arch Linux `Nuitka from git develop
   <https://aur.archlinux.org/packages/nuitka-git/>`_

Gentoo
======

-  |GENTOO_LOGO| Gentoo Linux, execute ``emerge -a dev-python/nuitka``

macOS
=====

No installer is available for macOS. Use the source packages, clone from
git, or use PyPI.

************
 PyPI / pip
************

There is `Nuitka on PyPI <http://pypi.python.org/pypi/Nuitka/>`_ as
well. So you can install with ``pip`` as follows.

Stable
======

The stable version from PyPI can be installed like this:

.. code:: bash

   pip install -U nuitka

Develop
=======

The develop version can be fetched from the Official git repo of Nuitka
like this:

.. code:: bash

   pip install -U "https://github.com/Nuitka/Nuitka/archive/develop.zip"

********
 Github
********

-  |GIT_LOGO| Stable: **git clone https://github.com/Nuitka/Nuitka**

-  |GIT_LOGO| Develop: **git clone --branch develop
   https://github.com/Nuitka/Nuitka**

Visit https://github.com/Nuitka/Nuitka for the Nuitka repository on
Github.

.. |NUITKA_STABLE_VERSION| replace::

   0.6.18

.. |NUITKA_STABLE_TAR_GZ| replace::

   `Nuitka 0.6.18 (0.6 MB tar.gz) <https://nuitka.net/releases/Nuitka-0.6.18.tar.gz>`__

.. |NUITKA_STABLE_TAR_BZ| replace::

   `Nuitka 0.6.18 (0.5 MB tar.bz2) <https://nuitka.net/releases/Nuitka-0.6.18.tar.bz2>`__

.. |NUITKA_STABLE_ZIP| replace::

   `Nuitka 0.6.18 (1.1 MB zip) <https://nuitka.net/releases/Nuitka-0.6.18.zip>`__

.. |NUITKA_UNSTABLE_TAR_GZ| replace::

   `Nuitka 0.6.19rc1 (0.6 MB tar.gz) <https://nuitka.net/releases/Nuitka-0.6.19rc1.tar.gz>`__

.. |NUITKA_UNSTABLE_TAR_BZ| replace::

   `Nuitka 0.6.19rc1 (0.5 MB tar.bz2) <https://nuitka.net/releases/Nuitka-0.6.19rc1.tar.bz2>`__

.. |NUITKA_UNSTABLE_ZIP| replace::

   `Nuitka 0.6.19rc1 (1.2 MB zip) <https://nuitka.net/releases/Nuitka-0.6.19rc1.zip>`__

.. |NUITKA_STABLE_WININST| replace::

   `Nuitka 0.6.18 (1.2 MB exe) <https://nuitka.net/releases/Nuitka-0.6.18.win32.exe>`__

.. |NUITKA_UNSTABLE_MSI_27_32| replace::

   `Nuitka 0.6.19rc1 Python2.7 32 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win32.py27.msi>`__

.. |NUITKA_UNSTABLE_MSI_27_64| replace::

   `Nuitka 0.6.19rc1 Python2.7 64 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win-amd64.py27.msi>`__

.. |NUITKA_UNSTABLE_MSI_33_32| replace::

   `Nuitka 0.5.29rc5 Python3.3 32 bit MSI <https://nuitka.net/releases/Nuitka-5.0.2950.win32.py33.msi>`__

.. |NUITKA_UNSTABLE_MSI_33_64| replace::

   `Nuitka 0.6.19rc1 Python3.3 64 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win-amd64.py33.msi>`__

.. |NUITKA_UNSTABLE_MSI_34_32| replace::

   `Nuitka 0.5.26rc4 Python3.4 32 bit MSI <https://nuitka.net/releases/Nuitka-5.0.2640.win32.py34.msi>`__

.. |NUITKA_UNSTABLE_MSI_34_64| replace::

   `Nuitka 0.6.19rc1 Python3.4 64 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win-amd64.py34.msi>`__

.. |NUITKA_UNSTABLE_MSI_35_32| replace::

   `Nuitka 0.6.19rc1 Python3.5 32 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win32.py35.msi>`__

.. |NUITKA_UNSTABLE_MSI_35_64| replace::

   `Nuitka 0.6.19rc1 Python3.5 64 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win-amd64.py35.msi>`__

.. |NUITKA_UNSTABLE_MSI_36_32| replace::

   `Nuitka 0.6.19rc1 Python3.6 32 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win32.py36.msi>`__

.. |NUITKA_UNSTABLE_MSI_36_64| replace::

   `Nuitka 0.6.19rc1 Python3.6 64 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win-amd64.py36.msi>`__

.. |NUITKA_UNSTABLE_MSI_37_32| replace::

   `Nuitka 0.6.19rc1 Python3.7 32 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win32.py37.msi>`__

.. |NUITKA_UNSTABLE_MSI_37_64| replace::

   `Nuitka 0.6.19rc1 Python3.7 64 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win-amd64.py37.msi>`__

.. |NUITKA_UNSTABLE_MSI_38_32| replace::

   `Nuitka 0.6.19rc1 Python3.8 32 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win32.py38.msi>`__

.. |NUITKA_UNSTABLE_MSI_38_64| replace::

   `Nuitka 0.6.19rc1 Python3.8 64 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win-amd64.py38.msi>`__

.. |NUITKA_UNSTABLE_MSI_39_32| replace::

   `Nuitka 0.6.19rc1 Python3.9 32 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win32.py39.msi>`__

.. |NUITKA_UNSTABLE_MSI_39_64| replace::

   `Nuitka 0.6.19rc1 Python3.9 64 bit MSI <https://nuitka.net/releases/Nuitka-6.0.1910.win-amd64.py39.msi>`__

.. |NUITKA_STABLE_MSI_27_32| replace::

   `Nuitka 0.6.18.0 Python2.7 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win32.py27.msi>`__

.. |NUITKA_STABLE_MSI_27_64| replace::

   `Nuitka 0.6.18.0 Python2.7 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win-amd64.py27.msi>`__

.. |NUITKA_STABLE_MSI_33_32| replace::

   `Nuitka 0.5.28.1 Python3.3 32 bit MSI <https://nuitka.net/releases/Nuitka-5.1.281.win32.py33.msi>`__

.. |NUITKA_STABLE_MSI_33_64| replace::

   `Nuitka 0.6.18.0 Python3.3 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win-amd64.py33.msi>`__

.. |NUITKA_STABLE_MSI_34_32| replace::

   `Nuitka 0.5.25.0 Python3.4 32 bit MSI <https://nuitka.net/releases/Nuitka-5.1.250.win32.py34.msi>`__

.. |NUITKA_STABLE_MSI_34_64| replace::

   `Nuitka 0.6.18.0 Python3.4 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win-amd64.py34.msi>`__

.. |NUITKA_STABLE_MSI_35_32| replace::

   `Nuitka 0.6.18.0 Python3.5 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win32.py35.msi>`__

.. |NUITKA_STABLE_MSI_35_64| replace::

   `Nuitka 0.6.18.0 Python3.5 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win-amd64.py35.msi>`__

.. |NUITKA_STABLE_MSI_36_32| replace::

   `Nuitka 0.6.18.0 Python3.6 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win32.py36.msi>`__

.. |NUITKA_STABLE_MSI_36_64| replace::

   `Nuitka 0.6.18.0 Python3.6 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win-amd64.py36.msi>`__

.. |NUITKA_STABLE_MSI_37_32| replace::

   `Nuitka 0.6.18.0 Python3.7 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win32.py37.msi>`__

.. |NUITKA_STABLE_MSI_37_64| replace::

   `Nuitka 0.6.18.0 Python3.7 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win-amd64.py37.msi>`__

.. |NUITKA_STABLE_MSI_38_32| replace::

   `Nuitka 0.6.18.0 Python3.8 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win32.py38.msi>`__

.. |NUITKA_STABLE_MSI_38_64| replace::

   `Nuitka 0.6.18.0 Python3.8 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win-amd64.py38.msi>`__

.. |NUITKA_STABLE_MSI_39_32| replace::

   `Nuitka 0.6.18.0 Python3.9 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win32.py39.msi>`__

.. |NUITKA_STABLE_MSI_39_64| replace::

   `Nuitka 0.6.18.0 Python3.9 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.180.win-amd64.py39.msi>`__

.. |NUITKA_STABLE_CENTOS6| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_CENTOS7| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_CENTOS8| replace::

   `Nuitka 0.6.18-7.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_8/noarch/nuitka-0.6.18-7.1.noarch.rpm>`__

.. |NUITKA_STABLE_RHEL6| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_RHEL7| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_F24| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_24/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_F25| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_25/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_F26| replace::

   `Nuitka 0.6.17.7 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_26/noarch/nuitka-0.6.17.7-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_F27| replace::

   `Nuitka 0.6.17.7 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_27/noarch/nuitka-0.6.17.7-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_F28| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_F29| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_F30| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_30/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_F31| replace::

   `Nuitka 0.6.18-7.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_31/noarch/nuitka-0.6.18-7.1.noarch.rpm>`__

.. |NUITKA_STABLE_F32| replace::

   `Nuitka 0.6.18-7.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_32/noarch/nuitka-0.6.18-7.1.noarch.rpm>`__

.. |NUITKA_STABLE_F33| replace::

   `Nuitka 0.6.18-7.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_33/noarch/nuitka-0.6.18-7.1.noarch.rpm>`__

.. |NUITKA_STABLE_F34| replace::

   `Nuitka 0.6.18-7.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_34/noarch/nuitka-0.6.18-7.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE131| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.1/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE132| replace::

   `Nuitka 0.6.18-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.2/noarch/nuitka-0.6.18-6.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE150| replace::

   `Nuitka 0.6.18-lp150.6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/noarch/nuitka-0.6.18-lp150.6.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE151| replace::

   `Nuitka 0.6.18-lp151.6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.1/noarch/nuitka-0.6.18-lp151.6.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE152| replace::

   `Nuitka 0.6.18-lp152.6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.2/noarch/nuitka-0.6.18-lp152.6.1.noarch.rpm>`__

.. |NUITKA_STABLE_SLE150| replace::

   `Nuitka 0.6.18-bp150.6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/SLE_15/noarch/nuitka-0.6.18-bp150.6.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_CENTOS6| replace::

   `Nuitka 0.6.18rc8-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/noarch/nuitka-unstable-0.6.18rc8-6.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_CENTOS7| replace::

   `Nuitka 0.6.18rc9-9.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/noarch/nuitka-unstable-0.6.18rc9-9.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_CENTOS8| replace::

   `Nuitka 0.6.18rc9-9.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_8/noarch/nuitka-unstable-0.6.19rc1-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_RHEL6| replace::

   `Nuitka 0.6.18rc8-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/noarch/nuitka-unstable-0.6.18rc8-6.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_RHEL7| replace::

   `Nuitka 0.6.18rc8-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/noarch/nuitka-unstable-0.6.18rc9-8.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F24| replace::

   `Nuitka 0.6.18rc9-8.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_24/noarch/nuitka-unstable-0.6.18rc9-8.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F25| replace::

   `Nuitka 0.6.18rc8-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_25/noarch/nuitka-unstable-0.6.18rc8-6.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F26| replace::

   `Nuitka 0.6.18rc8-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_26/noarch/nuitka-unstable-0.6.18rc8-6.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F27| replace::

   `Nuitka 0.6.18rc8-6.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_27/noarch/nuitka-unstable-0.6.18rc8-6.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F28| replace::

   `Nuitka 0.6.18rc9-8.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/noarch/nuitka-unstable-0.6.18rc9-8.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F29| replace::

   `Nuitka 0.6.18rc9-8.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/noarch/nuitka-unstable-0.6.18rc9-8.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F30| replace::

   `Nuitka 0.6.9rc1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_30/noarch/nuitka-unstable-0.6.9rc1-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F31| replace::

   `Nuitka 0.6.7rc2 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_31/noarch/nuitka-unstable-0.6.7rc2-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F32| replace::

   `Nuitka 0.6.19rc1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_32/noarch/nuitka-unstable-0.6.19rc1-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F33| replace::

   `Nuitka 0.6.19rc1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_33/noarch/nuitka-unstable-0.6.19rc1-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F34| replace::

   `Nuitka 0.6.19rc1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_34/noarch/nuitka-unstable-0.6.19rc1-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE131| replace::

   `Nuitka 0.6.18rc9-9.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.1/noarch/nuitka-unstable-0.6.18rc9-9.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE132| replace::

   `Nuitka 0.6.18rc9-9.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.2/noarch/nuitka-unstable-0.6.18rc9-9.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE150| replace::

   `Nuitka 0.6.18rc9-lp150.8.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/noarch/nuitka-unstable-0.6.18rc9-lp150.8.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE151| replace::

   `Nuitka 0.6.18rc9-lp151.8.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.1/noarch/nuitka-unstable-0.6.18rc9-lp151.8.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE152| replace::

   `Nuitka 0.6.18rc9-lp152.8.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.2/noarch/nuitka-unstable-0.6.18rc9-lp152.8.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SLE150| replace::

   `Nuitka 0.6.18rc9-bp150.8.1 RPM <https://download.opensuse.org/repositories/home:/kayhayen/SLE_15/noarch/nuitka-unstable-0.6.18rc9-bp150.8.1.noarch.rpm>`__

.. |DEBIAN_LOGO| image:: images/debian.png

.. |UBUNTU_LOGO| image:: images/ubuntu.png

.. |MINT_LOGO| image:: images/mint.png

.. |CENTOS_LOGO| image:: images/centos.png

.. |RHEL_LOGO| image:: images/rhel.png

.. |FEDORA_LOGO| image:: images/fedora.png

.. |SUSE_LOGO| image:: images/opensuse.png

.. |SLE_LOGO| image:: images/opensuse.png

.. |WINDOWS_LOGO| image:: /images/windows.jpg

.. |ARCH_LOGO| image:: images/arch.jpg

.. |GENTOO_LOGO| image:: images/gentoo-signet.png

.. |GIT_LOGO| image:: images/git.jpg
