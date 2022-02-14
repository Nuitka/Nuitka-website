.. meta::
   :description: Download the Python compiler Nuitka and make your code faster today.
   :keywords: nuitka,download,redhat,centos,debian,mint,freebsd,openbsd,arch,PyPI,git

##################
 Nuitka Downloads
##################

*********
 General
*********

Thank you for downloading Nuitka. Please consider becoming a Nuitka
commercial subscriber.

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

You may also learn more about `Nuitka Commercial
</doc/commercial.html>`__ offering.

The current release is Nuitka 0.6.19.7. Stable releases are supported
with hot fixes, indicated by the last of the 4 digits.

.. note::

   Stable releases are supposed to work for you. Develop releases are
   snapshots of the current ``develop`` branch in git, usually also
   relatively stable, but also rarely break.

.. note::

   During releases package builds can lag behind for a couple of days.

******
 PyPI
******

There is `Nuitka on PyPI <http://pypi.python.org/pypi/Nuitka/>`_ as
well. So you can install with ``pip`` as follows.

.. note::

   The stable version from PyPI can be installed via pip, and has no
   dependencies on any package, and is a source package, so you will
   have an easy time, even on e.g. Windows to use it.

.. code:: bash

   # Stable version
   python -m pip install -U nuitka

   # Develop version
   pip install -U "https://github.com/Nuitka/Nuitka/archive/develop.zip"

.. note::

   Do this this the python binary, you want to be compiled against.

*********
 Sources
*********

+-----------------------------------------------------------------------------------+-----------------------------------------------------------------------------------+-----------------------------------------------------------------------------------+-----------------------------------------------------------------------------------+
| Branch                                                                            | zip                                                                               | tar.gz                                                                            | tar.bz2                                                                           |
+===================================================================================+===================================================================================+===================================================================================+===================================================================================+
| Stable                                                                            | `Nuitka 0.6.19.7.zip <https://nuitka.net/releases/Nuitka-0.6.19.7.zip>`__         | `Nuitka 0.6.19.7.tar.gz <https://nuitka.net/releases/Nuitka-0.6.19.7.tar.gz>`__   | `Nuitka 0.6.19.7.tar.bz2 <https://nuitka.net/releases/Nuitka-0.6.19.7.tar.bz2>`__ |
+-----------------------------------------------------------------------------------+-----------------------------------------------------------------------------------+-----------------------------------------------------------------------------------+-----------------------------------------------------------------------------------+
| Develop                                                                           | `Nuitka 0.7rc1.zip <https://nuitka.net/releases/Nuitka-0.7rc1.zip>`__             | `Nuitka 0.7rc1.tar.gz <https://nuitka.net/releases/Nuitka-0.7rc1.tar.gz>`__       | `Nuitka 0.7rc1.tar.bz2 <https://nuitka.net/releases/Nuitka-0.7rc1.tar.bz2>`__     |
+-----------------------------------------------------------------------------------+-----------------------------------------------------------------------------------+-----------------------------------------------------------------------------------+-----------------------------------------------------------------------------------+

.. note::

   The source archives can be used directly after unpacking, simply
   start with ``python bin/nuitka --help`` and read ``README.pdf`` or
   ``README.rst`` to get started. Take especially care to read the User
   Manual, such that you don't go on a wrong track.

**********
 Packages
**********

Windows
=======

-  |WINDOWS_LOGO| Stable MSI Installer:

   .. note::

      The versions of the MSI have a different numbering scheme in their
      filenames, explained in the User Manual.

      Also, it's recommended to use PyPI and pip based installation on
      Windows, as MSI cannot be used e.g. with ``virtualenv`` and other
      clever dependency management tools.

   +---------------+----------------------------+----------------------------+
   | Python        | MSI 64 Bits                | MSI 32 Bits                |
   | Version       |                            |                            |
   +===============+============================+============================+
   | Python 2.6    | Not available as MSI       | Not available as MSI       |
   +---------------+----------------------------+----------------------------+
   | Python 2.7    | |NUITKA_STABLE_MSI_27_64|  | |NUITKA_STABLE_MSI_27_32|  |
   +---------------+----------------------------+----------------------------+
   | Python 3.3    | |NUITKA_STABLE_MSI_33_64|  | Not available as MSI       |
   +---------------+----------------------------+----------------------------+
   | Python 3.4    | |NUITKA_STABLE_MSI_34_64|  | Not available as MSI       |
   +---------------+----------------------------+----------------------------+
   | Python 3.5    | |NUITKA_STABLE_MSI_35_64|  | |NUITKA_STABLE_MSI_35_32|  |
   +---------------+----------------------------+----------------------------+
   | Python 3.6    | |NUITKA_STABLE_MSI_36_64|  | |NUITKA_STABLE_MSI_36_32|  |
   +---------------+----------------------------+----------------------------+
   | Python 3.7    | |NUITKA_STABLE_MSI_37_64|  | |NUITKA_STABLE_MSI_37_32|  |
   +---------------+----------------------------+----------------------------+
   | Python 3.8    | |NUITKA_STABLE_MSI_38_64|  | |NUITKA_STABLE_MSI_38_32|  |
   +---------------+----------------------------+----------------------------+
   | Python 3.9    | |NUITKA_STABLE_MSI_39_64|  | |NUITKA_STABLE_MSI_39_32|  |
   +---------------+----------------------------+----------------------------+
   | Python 3.10   | |NUITKA_STABLE_MSI_310_64| | |NUITKA_STABLE_MSI_310_32| |
   +---------------+----------------------------+----------------------------+

-  |WINDOWS_LOGO| Develop MSI Installer:

   +--------------+------------------------------+------------------------------+
   | Python       | MSI 64 Bits                  | MSI 32 Bits                  |
   | Version      |                              |                              |
   +==============+==============================+==============================+
   | Python 2.6   | Not available as MSI file    | Not available as MSI file    |
   +--------------+------------------------------+------------------------------+
   | Python 2.7   | |NUITKA_UNSTABLE_MSI_27_64|  | |NUITKA_UNSTABLE_MSI_27_32|  |
   +--------------+------------------------------+------------------------------+
   | Python 3.3   | |NUITKA_UNSTABLE_MSI_33_64|  | Not available as MSI file    |
   +--------------+------------------------------+------------------------------+
   | Python 3.4   | |NUITKA_UNSTABLE_MSI_34_64|  | Not available as MSI file    |
   +--------------+------------------------------+------------------------------+
   | Python 3.5   | |NUITKA_UNSTABLE_MSI_35_64|  | |NUITKA_UNSTABLE_MSI_35_32|  |
   +--------------+------------------------------+------------------------------+
   | Python 3.6   | |NUITKA_UNSTABLE_MSI_36_64|  | |NUITKA_UNSTABLE_MSI_36_32|  |
   +--------------+------------------------------+------------------------------+
   | Python 3.7   | |NUITKA_UNSTABLE_MSI_37_64|  | |NUITKA_UNSTABLE_MSI_37_32|  |
   +--------------+------------------------------+------------------------------+
   | Python 3.8   | |NUITKA_UNSTABLE_MSI_38_64|  | |NUITKA_UNSTABLE_MSI_38_32|  |
   +--------------+------------------------------+------------------------------+
   | Python 3.9   | |NUITKA_UNSTABLE_MSI_39_64|  | |NUITKA_UNSTABLE_MSI_39_32|  |
   +--------------+------------------------------+------------------------------+
   | Python 3.10  | |NUITKA_UNSTABLE_MSI_310_64| | |NUITKA_UNSTABLE_MSI_310_32| |
   +--------------+------------------------------+------------------------------+

Debian/Ubuntu/Mint
==================

-  |DEBIAN_LOGO| |UBUNTU_LOGO| |MINT_LOGO| Stable: Debian/Ubuntu/Mint
   repositories

   .. code:: bash

      CODENAME=`egrep 'UBUNTU_CODENAME|VERSION_CODENAME' /etc/os-release | sort | head -1 | cut -d= -f2`
      if [ -z "$CODENAME" ]
      then
         CODENAME=`lsb_release -c -s`
      fi
      wget -O - https://nuitka.net/deb/archive.key.gpg | sudo apt-key add -
      sudo apt-get install ca-certificates
      sudo echo >/etc/apt/sources.list.d/nuitka.list "deb https://nuitka.net/deb/stable/$CODENAME $CODENAME main"
      sudo apt-get update
      sudo apt-get install nuitka

-  |DEBIAN_LOGO| |UBUNTU_LOGO| |MINT_LOGO| Develop: Debian/Ubuntu/Mint
   repositories

   .. code:: bash

      CODENAME=`egrep 'UBUNTU_CODENAME|VERSION_CODENAME' /etc/os-release | cut -d= -f2`
      if [ -z "$CODENAME" ]
      then
         CODENAME=`lsb_release -c -s`
      fi
      wget -O - https://nuitka.net/deb/archive.key.gpg | sudo apt-key add -
      sudo apt-get install ca-certificates
      sudo echo >/etc/apt/sources.list.d/nuitka.list "deb https://nuitka.net/deb/develop/$CODENAME $CODENAME main"
      sudo apt-get update
      sudo apt-get install nuitka

   .. note::

      Because Nuitka is part of Debian Stable/Testing/Unstable, a stable
      version is already in the standard repository. This is the only
      way to access the develop version of Nuitka though.

RHEL
====

|RHEL_LOGO| repositories

.. code:: bash

   # Detect the RHEL version
   eval `grep VERSION_ID= /etc/os-release`

   yum-config-manager --add-repo http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-${VERSION_ID}/home:kayhayen.repo

   # Install either the these, but not both
   yum install nuitka
   yum install nuitka-unstable

+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| RHEL Version                                                                                                     | RPM Repository                                                                                                   | Stable                                                                                                           | Develop                                                                                                          |
+==================================================================================================================+==================================================================================================================+==================================================================================================================+==================================================================================================================+
| RHEL 8                                                                                                           | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-8/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                                  | Nuitka 0.6.20rc6                                                                                                 |
+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| RHEL 7                                                                                                           | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                                  | Nuitka 0.6.20rc6                                                                                                 |
+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| RHEL 6                                                                                                           | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                                  | Nuitka 0.6.20rc4                                                                                                 |
+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------+

CentOS
======

|CENTOS_LOGO| repositories

.. code:: bash

   # CentOS 6:
   yum-config-manager --add-repo http://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/home:kayhayen.repo
   # CentOS 7
   yum-config-manager --add-repo http://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/home:kayhayen.repo
   # CentOS 8
   yum-config-manager --add-repo http://download.opensuse.org/repositories/home:/kayhayen/CentOS_8/home:kayhayen.repo

   # Install either the these, but not both
   yum install nuitka
   yum install nuitka-unstable

+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| CentOS Version                                                                                                     | RPM Repository                                                                                                     | Stable                                                                                                             | Develop                                                                                                            |
+====================================================================================================================+====================================================================================================================+====================================================================================================================+====================================================================================================================+
| CentOS 8                                                                                                           | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_8/home:kayhayen.repo>`__        | Nuitka 0.6.19.7                                                                                                    | Nuitka 0.6.20rc6                                                                                                   |
+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| CentOS 7                                                                                                           | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/home:kayhayen.repo>`__        | Nuitka 0.6.19.7                                                                                                    | Nuitka 0.6.20rc6                                                                                                   |
+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| CentOS 6                                                                                                           | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                                    | Nuitka 0.6.20rc4                                                                                                   |
+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+

Fedora
======

|FEDORA_LOGO| repositories

.. code:: bash

   # Detect the Fedora version
   eval `grep VERSION_ID= /etc/os-release`

   # Use yum on older versions
   dnf config-manager --add-repo https://download.opensuse.org/repositories/home:/kayhayen/Fedora_${VERSION_ID}/home:kayhayen.repo

   # Install either the these, but not both
   dnf install nuitka
   dnf install nuitka-unstable

+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Fedora Version                                                                                               | RPM Repository                                                                                               | Stable                                                                                                       | Develop                                                                                                      |
+==============================================================================================================+==============================================================================================================+==============================================================================================================+==============================================================================================================+
| Fedora 35                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_35/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                              | Nuitka 0.6.20rc6                                                                                             |
+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Fedora 34                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_34/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                              | Nuitka 0.6.20rc6                                                                                             |
+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Fedora 33                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_33/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                              | Nuitka 0.6.20rc6                                                                                             |
+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Fedora 32                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_32/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                              | Nuitka 0.6.20rc6                                                                                             |
+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Fedora 31                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_31/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                              | Nuitka 0.6.20rc6                                                                                             |
+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Fedora 30                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_30/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                              | Nuitka 0.6.20rc6                                                                                             |
+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Fedora 29                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                              | Nuitka 0.6.20rc6                                                                                             |
+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Fedora 28                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                              | Nuitka 0.6.20rc6                                                                                             |
+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+

Suse
====

|SUSE_LOGO| repositories

.. code:: bash

   # Detect the OpenSUSE leap version
   eval `grep VERSION_ID= /etc/os-release`

   # Add Nuitka repo
   zypper ar -f https://download.opensuse.org/repositories/home:/kayhayen/Open_${VERSION_ID}/home:kayhayen.repo

   # Install either the these, but not both
   zypper install nuitka
   zypper install nuitka-unstable

+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| SUSE Version                                                                                                          | RPM Repository                                                                                                        | Stable                                                                                                                | Develop                                                                                                               |
+=======================================================================================================================+=======================================================================================================================+=======================================================================================================================+=======================================================================================================================+
| SLE 15                                                                                                                | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/SLE_15/home:kayhayen.repo>`__             | Nuitka 0.6.19.7                                                                                                       | Nuitka 0.6.20rc6                                                                                                      |
+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| openSUSE Leap 15.0                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                                       | Nuitka 0.6.20rc6                                                                                                      |
+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| openSUSE Leap 15.1                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.1/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                                       | Nuitka 0.6.20rc6                                                                                                      |
+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| openSUSE Leap 15.2                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.2/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                                       | Nuitka 0.6.20rc6                                                                                                      |
+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| openSUSE Leap 15.3                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.3/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                                       | Nuitka 0.6.20rc6                                                                                                      |
+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| openSUSE Leap 15.4                                                                                                    | `repository file <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.4/home:kayhayen.repo>`__ | Nuitka 0.6.19.7                                                                                                       | Nuitka 0.6.20rc6                                                                                                      |
+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+

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

********
 Github
********

-  |GIT_LOGO| Stable: **git clone https://github.com/Nuitka/Nuitka**

-  |GIT_LOGO| Develop: **git clone --branch develop
   https://github.com/Nuitka/Nuitka**

Visit https://github.com/Nuitka/Nuitka for the Nuitka repository on
Github.

.. |NUITKA_UNSTABLE_MSI_27_32| replace::

   `Nuitka 0.7.0rc1 Python2.7 32 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win32.py27.msi>`__

.. |NUITKA_UNSTABLE_MSI_27_64| replace::

   `Nuitka 0.7.0rc1 Python2.7 64 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win-amd64.py27.msi>`__

.. |NUITKA_UNSTABLE_MSI_33_32| replace::

   `Nuitka 0.5.29rc5 Python3.3 32 bit MSI <https://nuitka.net/releases/Nuitka-5.0.2950.win32.py33.msi>`__

.. |NUITKA_UNSTABLE_MSI_33_64| replace::

   `Nuitka 0.7.0rc1 Python3.3 64 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win-amd64.py33.msi>`__

.. |NUITKA_UNSTABLE_MSI_34_32| replace::

   `Nuitka 0.5.26rc4 Python3.4 32 bit MSI <https://nuitka.net/releases/Nuitka-5.0.2640.win32.py34.msi>`__

.. |NUITKA_UNSTABLE_MSI_34_64| replace::

   `Nuitka 0.7.0rc1 Python3.4 64 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win-amd64.py34.msi>`__

.. |NUITKA_UNSTABLE_MSI_35_32| replace::

   `Nuitka 0.7.0rc1 Python3.5 32 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win32.py35.msi>`__

.. |NUITKA_UNSTABLE_MSI_35_64| replace::

   `Nuitka 0.7.0rc1 Python3.5 64 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win-amd64.py35.msi>`__

.. |NUITKA_UNSTABLE_MSI_36_32| replace::

   `Nuitka 0.7.0rc1 Python3.6 32 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win32.py36.msi>`__

.. |NUITKA_UNSTABLE_MSI_36_64| replace::

   `Nuitka 0.7.0rc1 Python3.6 64 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win-amd64.py36.msi>`__

.. |NUITKA_UNSTABLE_MSI_37_32| replace::

   `Nuitka 0.7.0rc1 Python3.7 32 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win32.py37.msi>`__

.. |NUITKA_UNSTABLE_MSI_37_64| replace::

   `Nuitka 0.7.0rc1 Python3.7 64 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win-amd64.py37.msi>`__

.. |NUITKA_UNSTABLE_MSI_38_32| replace::

   `Nuitka 0.7.0rc1 Python3.8 32 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win32.py38.msi>`__

.. |NUITKA_UNSTABLE_MSI_38_64| replace::

   `Nuitka 0.7.0rc1 Python3.8 64 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win-amd64.py38.msi>`__

.. |NUITKA_UNSTABLE_MSI_39_32| replace::

   `Nuitka 0.7.0rc1 Python3.9 32 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win32.py39.msi>`__

.. |NUITKA_UNSTABLE_MSI_39_64| replace::

   `Nuitka 0.7.0rc1 Python3.9 64 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win-amd64.py39.msi>`__

.. |NUITKA_UNSTABLE_MSI_310_32| replace::

   `Nuitka 0.7.0rc1 Python3.0 32 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win32.py310.msi>`__

.. |NUITKA_UNSTABLE_MSI_310_64| replace::

   `Nuitka 0.7.0rc1 Python3.0 64 bit MSI <https://nuitka.net/releases/Nuitka-7.0.10.win-amd64.py310.msi>`__

.. |NUITKA_STABLE_MSI_27_32| replace::

   `Nuitka 0.6.19.7 Python2.7 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win32.py27.msi>`__

.. |NUITKA_STABLE_MSI_27_64| replace::

   `Nuitka 0.6.19.7 Python2.7 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win-amd64.py27.msi>`__

.. |NUITKA_STABLE_MSI_33_32| replace::

   `Nuitka 0.5.28.1 Python3.3 32 bit MSI <https://nuitka.net/releases/Nuitka-5.1.281.win32.py33.msi>`__

.. |NUITKA_STABLE_MSI_33_64| replace::

   `Nuitka 0.6.19.7 Python3.3 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win-amd64.py33.msi>`__

.. |NUITKA_STABLE_MSI_34_32| replace::

   `Nuitka 0.5.25.0 Python3.4 32 bit MSI <https://nuitka.net/releases/Nuitka-5.1.250.win32.py34.msi>`__

.. |NUITKA_STABLE_MSI_34_64| replace::

   `Nuitka 0.6.19.7 Python3.4 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win-amd64.py34.msi>`__

.. |NUITKA_STABLE_MSI_35_32| replace::

   `Nuitka 0.6.19.7 Python3.5 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win32.py35.msi>`__

.. |NUITKA_STABLE_MSI_35_64| replace::

   `Nuitka 0.6.19.7 Python3.5 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win-amd64.py35.msi>`__

.. |NUITKA_STABLE_MSI_36_32| replace::

   `Nuitka 0.6.19.7 Python3.6 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win32.py36.msi>`__

.. |NUITKA_STABLE_MSI_36_64| replace::

   `Nuitka 0.6.19.7 Python3.6 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win-amd64.py36.msi>`__

.. |NUITKA_STABLE_MSI_37_32| replace::

   `Nuitka 0.6.19.7 Python3.7 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win32.py37.msi>`__

.. |NUITKA_STABLE_MSI_37_64| replace::

   `Nuitka 0.6.19.7 Python3.7 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win-amd64.py37.msi>`__

.. |NUITKA_STABLE_MSI_38_32| replace::

   `Nuitka 0.6.19.7 Python3.8 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win32.py38.msi>`__

.. |NUITKA_STABLE_MSI_38_64| replace::

   `Nuitka 0.6.19.7 Python3.8 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win-amd64.py38.msi>`__

.. |NUITKA_STABLE_MSI_39_32| replace::

   `Nuitka 0.6.19.7 Python3.9 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win32.py39.msi>`__

.. |NUITKA_STABLE_MSI_39_64| replace::

   `Nuitka 0.6.19.7 Python3.9 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win-amd64.py39.msi>`__

.. |NUITKA_STABLE_MSI_310_32| replace::

   `Nuitka 0.6.19.7 Python3.0 32 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win32.py310.msi>`__

.. |NUITKA_STABLE_MSI_310_64| replace::

   `Nuitka 0.6.19.7 Python3.0 64 bit MSI <https://nuitka.net/releases/Nuitka-6.1.197.win-amd64.py310.msi>`__

.. |DEBIAN_LOGO| image:: ../../images/debian.png

.. |UBUNTU_LOGO| image:: ../../images/ubuntu.png

.. |MINT_LOGO| image:: ../../images/mint.png

.. |CENTOS_LOGO| image:: ../../images/centos.png

.. |RHEL_LOGO| image:: ../../images/rhel.png

.. |FEDORA_LOGO| image:: ../../images/fedora.png

.. |SUSE_LOGO| image:: ../../images/opensuse.png

.. |WINDOWS_LOGO| image:: ../../images/windows.jpg

.. |ARCH_LOGO| image:: ../../images/arch.jpg

.. |GENTOO_LOGO| image:: ../../images/gentoo-signet.png

.. |GIT_LOGO| image:: ../../images/git.jpg
