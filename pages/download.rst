.. date: 2010/08/18 07:25
.. title: Downloads
.. slug: download

.. contents::

The current release is Nuitka |NUITKA_STABLE_VERSION|, which is a good
replacement of CPython with somewhat better performance. A 312% speed factor for
the PyStone benchmark. The project didn't focus much on the performance side of
things so far, therefore more improvements are expected in the future.

These archives are source and can be used directly, simply start with
``bin/nuitka --help`` and read README.pdf to get started.

Source Archives
---------------

Stable Sources
~~~~~~~~~~~~~~

Stable releases are supported with hot fixes.

* Stable: |NUITKA_STABLE_TAR_GZ|
* Stable: |NUITKA_STABLE_TAR_BZ|
* Stable: |NUITKA_STABLE_ZIP|

Development Sources
~~~~~~~~~~~~~~~~~~~

Develop releases are snapshots of the current development.

* Develop: |NUITKA_UNSTABLE_TAR_GZ|
* Develop: |NUITKA_UNSTABLE_TAR_BZ|
* Develop: |NUITKA_UNSTABLE_ZIP|


Packages
--------

Windows
~~~~~~~

* |WINDOWS_LOGO| Stable MSI Installer:

  .. note::

      The versions of the MSI have a different numbering scheme in their
      filenames, explained in the user manual.

  .. table::

     ==============  =========================  ===========================
     Python Version         MSI 64 Bits                MSI 32 Bits
     ==============  =========================  ===========================
       Python 2.6    Not available as MSI       Not available as MSI
     --------------  -------------------------  ---------------------------
       Python 2.7    |NUITKA_STABLE_MSI_27_64|  |NUITKA_STABLE_MSI_27_32|
     --------------  -------------------------  ---------------------------
       Python 3.3    |NUITKA_STABLE_MSI_33_64|  Not available as MSI
     --------------  -------------------------  ---------------------------
       Python 3.4    |NUITKA_STABLE_MSI_34_64|  Not available as MSI
     --------------  -------------------------  ---------------------------
       Python 3.5    |NUITKA_STABLE_MSI_35_64|  |NUITKA_STABLE_MSI_35_32|
     --------------  -------------------------  ---------------------------
       Python 3.6    |NUITKA_STABLE_MSI_36_64|  |NUITKA_STABLE_MSI_36_32|
     --------------  -------------------------  ---------------------------
       Python 3.7    |NUITKA_STABLE_MSI_37_64|  |NUITKA_STABLE_MSI_37_32|
     ==============  =========================  ===========================


* |WINDOWS_LOGO| Develop MSI Installer:

  .. table::

     ==============  ===========================  ===========================
     Python Version  MSI 64 Bits                  MSI 32 Bits
     ==============  ===========================  ===========================
       Python 2.6    Not available as MSI file    Not available as MSI file
     --------------  ---------------------------  ---------------------------
       Python 2.7    |NUITKA_UNSTABLE_MSI_27_64|  |NUITKA_UNSTABLE_MSI_27_32|
     --------------  ---------------------------  ---------------------------
       Python 3.3    |NUITKA_UNSTABLE_MSI_33_64|  Not available as MSI file
     --------------  ---------------------------  ---------------------------
       Python 3.4    |NUITKA_UNSTABLE_MSI_34_64|  Not available as MSI file
     --------------  ---------------------------  ---------------------------
       Python 3.5    |NUITKA_UNSTABLE_MSI_35_64|  |NUITKA_UNSTABLE_MSI_35_32|
     --------------  ---------------------------  ---------------------------
       Python 3.6    |NUITKA_UNSTABLE_MSI_36_64|  |NUITKA_UNSTABLE_MSI_36_32|
     --------------  ---------------------------  ---------------------------
       Python 3.7    |NUITKA_UNSTABLE_MSI_37_64|  |NUITKA_UNSTABLE_MSI_37_32|
     ==============  ===========================  ===========================


Debian/Ubuntu/Mint
~~~~~~~~~~~~~~~~~~

* |DEBIAN_LOGO| |UBUNTU_LOGO| |MINT_LOGO| Stable: Debian/Ubuntu/Mint repositories

  .. code-block:: sh

     CODENAME=`grep UBUNTU_CODENAME /etc/os-release | cut -d= -f2`
     if ["$CODENAME"] = ""]
     then
        CODENAME=`lsb_release -c -s`
     fi;
     wget -O - http://nuitka.net/deb/archive.key.gpg | apt-key add -
     echo >/etc/apt/sources.list.d/nuitka.list "deb http://nuitka.net/deb/stable/$CODENAME $CODENAME main"
     apt-get update
     apt-get install nuitka

* |DEBIAN_LOGO| |UBUNTU_LOGO| |MINT_LOGO| Develop: Debian/Ubuntu/Mint repositories

  .. code-block:: sh

     CODENAME=`grep UBUNTU_CODENAME /etc/os-release | cut -d= -f2`
     if ["$CODENAME"] = ""]
     then
        CODENAME=`lsb_release -c -s`
     fi;
     wget -O - http://nuitka.net/deb/archive.key.gpg | apt-key add -
     echo >/etc/apt/sources.list.d/nuitka.list "deb http://nuitka.net/deb/develop/$CODENAME $CODENAME main"
     apt-get update
     apt-get install nuitka

  .. note::

     Because Nuitka is part of Debian Stable/Testing/Unstable, a stable version
     is already in the standard repository. This is the only way to access the
     develop version of Nuitka though.

RHEL
~~~~

* |RHEL_LOGO| Stable: RHEL 6.x Packages: |NUITKA_STABLE_RHEL6| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/home:kayhayen.repo>`__

* |RHEL_LOGO| Stable: RHEL 7.x Packages: |NUITKA_STABLE_RHEL7| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/home:kayhayen.repo>`__

* |RHEL_LOGO| Develop: RHEL 6.x Packages: |NUITKA_UNSTABLE_RHEL6| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/home:kayhayen.repo>`__

* |RHEL_LOGO| Develop: RHEL 7.x Packages: |NUITKA_UNSTABLE_RHEL7| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/home:kayhayen.repo>`__

CentOS
~~~~~~

* |CENTOS_LOGO| Stable: CentOS 6.x Packages: |NUITKA_STABLE_CENTOS6| or
  `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/home:kayhayen.repo>`__

* |CENTOS_LOGO| Stable: CentOS 7.x Packages: |NUITKA_STABLE_CENTOS7| or
  `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/home:kayhayen.repo>`__

* |CENTOS_LOGO| Develop: CentOS 6.x Packages: |NUITKA_UNSTABLE_CENTOS6| or
  `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/home:kayhayen.repo>`__

* |CENTOS_LOGO| Develop: CentOS 7.x Packages: |NUITKA_UNSTABLE_CENTOS7| or
  `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/home:kayhayen.repo>`__

Fedora
~~~~~~

* |FEDORA_LOGO| Stable: Fedora 24: |NUITKA_STABLE_F24| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_24/home:kayhayen.repo>`__

* |FEDORA_LOGO| Stable: Fedora 25: |NUITKA_STABLE_F25| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_25/home:kayhayen.repo>`__

* |FEDORA_LOGO| Stable: Fedora 26: |NUITKA_STABLE_F26| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_26/home:kayhayen.repo>`__

* |FEDORA_LOGO| Stable: Fedora 27: |NUITKA_STABLE_F27| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_27/home:kayhayen.repo>`__

* |FEDORA_LOGO| Stable: Fedora 28: |NUITKA_STABLE_F28| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/home:kayhayen.repo>`__

* |FEDORA_LOGO| Stable: Fedora 29: |NUITKA_STABLE_F29| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/home:kayhayen.repo>`__

* |FEDORA_LOGO| Develop: Fedora 24: |NUITKA_UNSTABLE_F24| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_24/home:kayhayen.repo>`__

* |FEDORA_LOGO| Develop: Fedora 25: |NUITKA_UNSTABLE_F25| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_25/home:kayhayen.repo>`__

* |FEDORA_LOGO| Develop: Fedora 26: |NUITKA_UNSTABLE_F26| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_26/home:kayhayen.repo>`__

* |FEDORA_LOGO| Develop: Fedora 27: |NUITKA_UNSTABLE_F27| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_27/home:kayhayen.repo>`__

* |FEDORA_LOGO| Develop: Fedora 28: |NUITKA_UNSTABLE_F28| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/home:kayhayen.repo>`__

* |FEDORA_LOGO| Develop: Fedora 29: |NUITKA_UNSTABLE_F29| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/home:kayhayen.repo>`__

Suse
~~~~

* |SLE_LOGO| Stable: SLE 15: |NUITKA_STABLE_SLE150| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/SLE_15/home:kayhayen.repo>`__

* |SUSE_LOGO| Stable: openSUSE 13.1: |NUITKA_STABLE_SUSE131| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.1/home:kayhayen.repo>`__

* |SUSE_LOGO| Stable: openSUSE 13.2: |NUITKA_STABLE_SUSE132| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.2/home:kayhayen.repo>`__

* |SUSE_LOGO| Stable: openSUSE 42.1: |NUITKA_STABLE_SUSE421| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.1/home:kayhayen.repo>`__

* |SUSE_LOGO| Stable: openSUSE 42.2: |NUITKA_STABLE_SUSE422| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.2/home:kayhayen.repo>`__

* |SUSE_LOGO| Stable: openSUSE 42.3: |NUITKA_STABLE_SUSE423| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.3/home:kayhayen.repo>`__

* |SUSE_LOGO| Stable: openSUSE 15.0: |NUITKA_STABLE_SUSE150| or `repository file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/home:kayhayen.repo>`__

* |SLE_LOGO| Develop: SLE 15: |NUITKA_UNSTABLE_SLE150| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/SLE_15/home:kayhayen.repo>`__

* |SUSE_LOGO| Develop: openSUSE 13.1: |NUITKA_UNSTABLE_SUSE131| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.1/home:kayhayen.repo>`__

* |SUSE_LOGO| Develop: openSUSE 13.2: |NUITKA_UNSTABLE_SUSE132| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.2/home:kayhayen.repo>`__

* |SUSE_LOGO| Develop: openSUSE 42.1: |NUITKA_UNSTABLE_SUSE421| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.1/home:kayhayen.repo>`__

* |SUSE_LOGO| Develop: openSUSE 42.2: |NUITKA_UNSTABLE_SUSE422| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.2/home:kayhayen.repo>`__

* |SUSE_LOGO| Develop: openSUSE 42.3: |NUITKA_UNSTABLE_SUSE423| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.3/home:kayhayen.repo>`__

* |SUSE_LOGO| Develop: openSUSE 15.0: |NUITKA_UNSTABLE_SUSE150| or `repository
  file
  <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/home:kayhayen.repo>`__

Arch
~~~~

* |ARCH_LOGO| Stable: Arch Linux, execute ``pacman -S nuitka``

* |ARCH_LOGO| Develop: Arch Linux `Nuitka from git develop
  <https://aur.archlinux.org/packages/nuitka-git/>`_

macOS
~~~~~

No installer is available for macOS. Use the source packages, clone from git, or
use PyPI.

PyPI / pip
----------

There is `Nuitka on PyPI <http://pypi.python.org/pypi/Nuitka/>`_ as well. So
you can install with ``pip`` as follows.

Stable
~~~~~~

The stable version from PyPI can be installed like this:

  .. code-block:: sh

      pip install -U nuitka

Develop
~~~~~~~

The develop version can be fetched from the Official git repo of Nuitka like
this:

  .. code-block:: sh

      pip install -U 'http://nuitka.net/gitweb/?p=Nuitka.git;a=snapshot;h=refs/heads/develop;sf=tgz'

git
---

Official
~~~~~~~~

* |GIT_LOGO| Stable: **git clone http://git.nuitka.net/Nuitka.git**
* |GIT_LOGO| Develop: **git clone --branch develop
  http://git.nuitka.net/Nuitka.git**

Then do your own modifications, and do git ``pull --rebase`` each time there is
a new release. To reduce your differences, feel free to send me pull requests or
the patches you create with ``git format-patch <commit-id>`` and I will likely
merge it.

Github
~~~~~~

Visit https://github.com/kayhayen/Nuitka for a mirror of the Nuitka repository
on Github. Because issue tracking also lives there, PRs there are most logical
way of interaction.


Gitlab
~~~~~~

Visit https://gitlab.com/kayhayen/Nuitka for a mirror of the Nuitka
repository on Gitlab.

Bitbucket
~~~~~~~~~

Visit https://bitbucket.org/kayhayen/nuitka for a mirror of the Nuitka
repository on Bitbucket.

.. |NUITKA_STABLE_VERSION| replace::
   0.6.2

.. |NUITKA_STABLE_TAR_GZ| replace::
   `Nuitka 0.6.2 (0.6 MB tar.gz) <http://nuitka.net/releases/Nuitka-0.6.2.tar.gz>`__

.. |NUITKA_STABLE_TAR_BZ| replace::
   `Nuitka 0.6.2 (0.5 MB tar.bz2) <http://nuitka.net/releases/Nuitka-0.6.2.tar.bz2>`__

.. |NUITKA_STABLE_ZIP| replace::
   `Nuitka 0.6.2 (1.1 MB zip) <http://nuitka.net/releases/Nuitka-0.6.2.zip>`__

.. |NUITKA_UNSTABLE_TAR_GZ| replace::
   `Nuitka 0.6.3rc3 (0.6 MB tar.gz) <http://nuitka.net/releases/Nuitka-0.6.3rc3.tar.gz>`__

.. |NUITKA_UNSTABLE_TAR_BZ| replace::
   `Nuitka 0.6.3rc3 (0.5 MB tar.bz2) <http://nuitka.net/releases/Nuitka-0.6.3rc3.tar.bz2>`__

.. |NUITKA_UNSTABLE_ZIP| replace::
   `Nuitka 0.6.3rc3 (1.2 MB zip) <http://nuitka.net/releases/Nuitka-0.6.3rc3.zip>`__

.. |NUITKA_STABLE_WININST| replace::
   `Nuitka 0.6.2 (1.2 MB exe) <http://nuitka.net/releases/Nuitka-0.6.2.win32.exe>`__

.. |NUITKA_UNSTABLE_MSI_27_32| replace::
   `Nuitka 0.6.3rc3 Python2.7 32 bit MSI <http://nuitka.net/releases/Nuitka-6.0.330.win32.py27.msi>`__

.. |NUITKA_UNSTABLE_MSI_27_64| replace::
   `Nuitka 0.6.3rc3 Python2.7 64 bit MSI <http://nuitka.net/releases/Nuitka-6.0.330.win-amd64.py27.msi>`__

.. |NUITKA_UNSTABLE_MSI_33_32| replace::
   `Nuitka 0.5.29rc5 Python3.3 32 bit MSI <http://nuitka.net/releases/Nuitka-5.0.2950.win32.py33.msi>`__

.. |NUITKA_UNSTABLE_MSI_33_64| replace::
   `Nuitka 0.6.3rc3 Python3.3 64 bit MSI <http://nuitka.net/releases/Nuitka-6.0.330.win-amd64.py33.msi>`__

.. |NUITKA_UNSTABLE_MSI_34_32| replace::
   `Nuitka 0.5.26rc4 Python3.4 32 bit MSI <http://nuitka.net/releases/Nuitka-5.0.2640.win32.py34.msi>`__

.. |NUITKA_UNSTABLE_MSI_34_64| replace::
   `Nuitka 0.6.3rc3 Python3.4 64 bit MSI <http://nuitka.net/releases/Nuitka-6.0.330.win-amd64.py34.msi>`__

.. |NUITKA_UNSTABLE_MSI_35_32| replace::
   `Nuitka 0.6.3rc3 Python3.5 32 bit MSI <http://nuitka.net/releases/Nuitka-6.0.330.win32.py35.msi>`__

.. |NUITKA_UNSTABLE_MSI_35_64| replace::
   `Nuitka 0.6.3rc3 Python3.5 64 bit MSI <http://nuitka.net/releases/Nuitka-6.0.330.win-amd64.py35.msi>`__

.. |NUITKA_UNSTABLE_MSI_36_32| replace::
   `Nuitka 0.6.3rc3 Python3.6 32 bit MSI <http://nuitka.net/releases/Nuitka-6.0.330.win32.py36.msi>`__

.. |NUITKA_UNSTABLE_MSI_36_64| replace::
   `Nuitka 0.6.3rc3 Python3.6 64 bit MSI <http://nuitka.net/releases/Nuitka-6.0.330.win-amd64.py36.msi>`__

.. |NUITKA_UNSTABLE_MSI_37_32| replace::
   `Nuitka 0.6.3rc3 Python3.7 32 bit MSI <http://nuitka.net/releases/Nuitka-6.0.330.win32.py37.msi>`__

.. |NUITKA_UNSTABLE_MSI_37_64| replace::
   `Nuitka 0.6.3rc3 Python3.7 64 bit MSI <http://nuitka.net/releases/Nuitka-6.0.330.win-amd64.py37.msi>`__

.. |NUITKA_STABLE_MSI_27_32| replace::
   `Nuitka 0.6.2.0 Python2.7 32 bit MSI <http://nuitka.net/releases/Nuitka-6.1.20.win32.py27.msi>`__

.. |NUITKA_STABLE_MSI_27_64| replace::
   `Nuitka 0.6.2.0 Python2.7 64 bit MSI <http://nuitka.net/releases/Nuitka-6.1.20.win-amd64.py27.msi>`__

.. |NUITKA_STABLE_MSI_33_32| replace::
   `Nuitka 0.5.28.1 Python3.3 32 bit MSI <http://nuitka.net/releases/Nuitka-5.1.281.win32.py33.msi>`__

.. |NUITKA_STABLE_MSI_33_64| replace::
   `Nuitka 0.6.2.0 Python3.3 64 bit MSI <http://nuitka.net/releases/Nuitka-6.1.20.win-amd64.py33.msi>`__

.. |NUITKA_STABLE_MSI_34_32| replace::
   `Nuitka 0.5.25.0 Python3.4 32 bit MSI <http://nuitka.net/releases/Nuitka-5.1.250.win32.py34.msi>`__

.. |NUITKA_STABLE_MSI_34_64| replace::
   `Nuitka 0.6.2.0 Python3.4 64 bit MSI <http://nuitka.net/releases/Nuitka-6.1.20.win-amd64.py34.msi>`__

.. |NUITKA_STABLE_MSI_35_32| replace::
   `Nuitka 0.6.2.0 Python3.5 32 bit MSI <http://nuitka.net/releases/Nuitka-6.1.20.win32.py35.msi>`__

.. |NUITKA_STABLE_MSI_35_64| replace::
   `Nuitka 0.6.2.0 Python3.5 64 bit MSI <http://nuitka.net/releases/Nuitka-6.1.20.win-amd64.py35.msi>`__

.. |NUITKA_STABLE_MSI_36_32| replace::
   `Nuitka 0.6.2.0 Python3.6 32 bit MSI <http://nuitka.net/releases/Nuitka-6.1.20.win32.py36.msi>`__

.. |NUITKA_STABLE_MSI_36_64| replace::
   `Nuitka 0.6.2.0 Python3.6 64 bit MSI <http://nuitka.net/releases/Nuitka-6.1.20.win-amd64.py36.msi>`__

.. |NUITKA_STABLE_MSI_37_32| replace::
   `Nuitka 0.6.2.0 Python3.7 32 bit MSI <http://nuitka.net/releases/Nuitka-6.1.20.win32.py37.msi>`__

.. |NUITKA_STABLE_MSI_37_64| replace::
   `Nuitka 0.6.2.0 Python3.7 64 bit MSI <http://nuitka.net/releases/Nuitka-6.1.20.win-amd64.py37.msi>`__

.. |NUITKA_STABLE_CENTOS6| replace::
   `Nuitka 0.6.2 RPM <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/noarch/nuitka-0.6.2-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_CENTOS7| replace::
   `Nuitka 0.6.2 RPM <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/noarch/nuitka-0.6.2-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_RHEL6| replace::
   `Nuitka 0.6.2 RPM <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/noarch/nuitka-0.6.2-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_RHEL7| replace::
   `Nuitka 0.6.2 RPM <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/noarch/nuitka-0.6.2-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_F24| replace::
   `Nuitka 0.6.1.1 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_24/noarch/nuitka-0.6.1.1-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_F25| replace::
   `Nuitka 0.6.1.1 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_25/noarch/nuitka-0.6.1.1-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_F26| replace::
   `Nuitka 0.6.1.1 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_26/noarch/nuitka-0.6.1.1-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_F27| replace::
   `Nuitka 0.6.1.1 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_27/noarch/nuitka-0.6.1.1-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_F28| replace::
   `Nuitka 0.6.1.1 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/noarch/nuitka-0.6.1.1-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_F29| replace::
   `Nuitka 0.6.1.1 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/noarch/nuitka-0.6.1.1-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE131| replace::
   `Nuitka 0.6.2 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.1/noarch/nuitka-0.6.2-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE132| replace::
   `Nuitka 0.6.2 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.2/noarch/nuitka-0.6.2-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE421| replace::
   `Nuitka 0.6.2 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.1/noarch/nuitka-0.6.2-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE422| replace::
   `Nuitka 0.6.2 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.2/noarch/nuitka-0.6.2-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE423| replace::
   `Nuitka 0.6.2 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.3/noarch/nuitka-0.6.2-5.1.noarch.rpm>`__

.. |NUITKA_STABLE_SUSE150| replace::
   `Nuitka 0.6.2-lp150.5.1 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/noarch/nuitka-0.6.2-lp150.5.1.noarch.rpm>`__

.. |NUITKA_STABLE_SLE150| replace::
   `Nuitka 0.6.2 RPM <http://download.opensuse.org/repositories/home:/kayhayen/SLE_15/noarch/nuitka-0.6.2-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_CENTOS6| replace::
   `Nuitka 0.6.3rc3 RPM <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/noarch/nuitka-unstable-0.6.3rc3-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_CENTOS7| replace::
   `Nuitka 0.6.3rc3 RPM <http://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/noarch/nuitka-unstable-0.6.3rc3-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_RHEL6| replace::
   `Nuitka 0.6.3rc3 RPM <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/noarch/nuitka-unstable-0.6.3rc3-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_RHEL7| replace::
   `Nuitka 0.6.3rc3 RPM <http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/noarch/nuitka-unstable-0.6.3rc3-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F24| replace::
   `Nuitka 0.6.2rc5 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_24/noarch/nuitka-unstable-0.6.2rc5-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F25| replace::
   `Nuitka 0.6.2rc5 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_25/noarch/nuitka-unstable-0.6.2rc5-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F26| replace::
   `Nuitka 0.6.2rc5 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_26/noarch/nuitka-unstable-0.6.2rc5-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F27| replace::
   `Nuitka 0.6.2rc5 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_27/noarch/nuitka-unstable-0.6.2rc5-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F28| replace::
   `Nuitka 0.6.2rc5 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/noarch/nuitka-unstable-0.6.2rc5-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_F29| replace::
   `Nuitka 0.6.2rc5 RPM <http://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/noarch/nuitka-unstable-0.6.2rc5-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE131| replace::
   `Nuitka 0.6.3rc3 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.1/noarch/nuitka-unstable-0.6.3rc3-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE132| replace::
   `Nuitka 0.6.3rc3 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.2/noarch/nuitka-unstable-0.6.3rc3-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE421| replace::
   `Nuitka 0.6.3rc3 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.1/noarch/nuitka-unstable-0.6.3rc3-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE422| replace::
   `Nuitka 0.6.3rc3 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.2/noarch/nuitka-unstable-0.6.3rc3-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE423| replace::
   `Nuitka 0.6.3rc3 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_42.3/noarch/nuitka-unstable-0.6.3rc3-5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SUSE150| replace::
   `Nuitka 0.6.3rc3-lp150.5.1 RPM <http://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/noarch/nuitka-unstable-0.6.3rc3-lp150.5.1.noarch.rpm>`__

.. |NUITKA_UNSTABLE_SLE150| replace::
   `Nuitka 0.6.3rc3 RPM <http://download.opensuse.org/repositories/home:/kayhayen/SLE_15/noarch/nuitka-unstable-0.6.3rc3-5.1.noarch.rpm>`__

.. |DEBIAN_LOGO| image:: images/debian.png

.. |UBUNTU_LOGO| image:: images/ubuntu.png

.. |CENTOS_LOGO| image:: images/centos.png

.. |RHEL_LOGO| image:: images/rhel.png

.. |FEDORA_LOGO| image:: images/fedora.png

.. |SUSE_LOGO| image:: images/opensuse.png

.. |SLE_LOGO| image:: images/opensuse.png

.. |WINDOWS_LOGO| image:: images/windows.jpg

.. |ARCH_LOGO| image:: images/arch.jpg

.. |MINT_LOGO| image:: images/mint.png

.. |GIT_LOGO| image:: images/git.jpg
