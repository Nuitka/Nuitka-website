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

The current release is Nuitka |NUITKA_VERSION|. Stable releases are
supported with hot fixes, indicated by the last of the 4 digits.

.. note::

   Stable releases are supposed to work for you. Develop releases are
   snapshots of the current ``develop`` branch in git, usually also
   relatively stable, but also rarely break.

.. note::

   During releases package builds can lag behind for a couple of days.

*********
 License
*********

**Nuitka** is licensed under the `Apache License, Version 2.0
<http://www.apache.org/licenses/LICENSE-2.0>`_; you may not use it
except in compliance with the License. Unless required by applicable law
or agreed to in writing, software distributed under the License is
distributed on an **"as is" basis, without warranties or conditions of
any kind**, either express or implied. See the License for the specific
language governing permissions and limitations under the License.

******
 PyPI
******

There is `Nuitka on PyPI <http://pypi.python.org/pypi/Nuitka/>`__ as
well. So you can install with ``pip`` as follows.

.. note::

   The stable version from PyPI can be installed via pip, and has no
   dependencies on any package, and is a source package, so you will
   have an easy time, even on e.g. Windows to use it.

.. code:: bash

   # Stable version
   python -m pip install -U nuitka

   # Develop version
   python -m pip install -U "https://github.com/Nuitka/Nuitka/archive/develop.zip"

.. note::

   Do this this the python binary, you want to be compiled against.

*********
 Sources
*********

.. include:: source-downloads.inc

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

The MSI installers are discontinued as Python has deprecated their
support for them, as well as Windows 10 making it harder to users to
install them. Using the PyPI installation is recommended on Windows.

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

.. include:: rhel-downloads.inc

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

.. include:: centos-downloads.inc

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

.. include:: fedora-downloads.inc

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

.. include:: suse-downloads.inc

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

-  |GIT_LOGO| Stable: **git clone --branch main
   https://github.com/Nuitka/Nuitka**

-  |GIT_LOGO| Develop: **git clone --branch develop
   https://github.com/Nuitka/Nuitka**

Visit https://github.com/Nuitka/Nuitka for the Nuitka repository on
Github.

.. include:: ../variables.inc

.. include:: ../dynamic.inc
