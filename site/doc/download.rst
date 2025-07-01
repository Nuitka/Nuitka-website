.. meta::
   :description: Download the Python compiler Nuitka and make your code faster today.
   :keywords: nuitka,download,RedHat,RHEL,CentOS,Debian,Mint,Arch,Fedora,SuSE,FreeBSD,OpenBSD,AIX,PyPI,git,source

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

Nuitka Standard vs Commercial
=============================

The standard edition is what you download here. It lacks features that
commercial users might want for IP protection. Nuitka standard bundles
your code, dependencies and data into a single executable if you want.
It also does acceleration, just running faster in the same environment,
and can produce extension modules as well.

`Get Nuitka Standard </doc/download.html>`_

Nuitka Commercial
=================

The commercial edition additionally protects your code, data and
outputs, so that users of the executable cannot access these. This a
private repository of plugins that you pay to get access to.
Additionally, you can purchase priority support.

`Learn more about Nuitka commercial </doc/commercial.html>`_

The current release is Nuitka |NUITKA_VERSION|. Stable releases are
supported with hot fixes, indicated by the last of the 3 digits.

.. note::

   Stable releases are supposed to work for you. Develop releases are
   snapshots of the current ``develop`` branch in git, usually also
   relatively stable, but also rarely break.

.. note::

   During releases package builds can lag behind for a couple of days.

***************
 Quick Install
***************

**Recommended: Install via PyPI (all platforms)**

.. code:: bash

   python -m pip install -U Nuitka

For the latest development version:

.. code:: bash

   python -m pip install -U "https://github.com/Nuitka/Nuitka/archive/develop.zip"

.. note::

   Use the Python interpreter you want to compile with, that is the
   easiest way. And also invoke as ``python -m nuitka`` with that
   interpreter. It is the easiest and most reliable way.

**Other install options:**

.. dropdown:: Linux (Debian, Ubuntu, Mint, Fedora, CentOS, RHEL, SuSE, Arch)

   **Debian/Ubuntu/Mint**

   -  |DEBIAN_LOGO| |UBUNTU_LOGO| |MINT_LOGO| Stable: Debian/Ubuntu/Mint
      repositories

      .. code:: bash

         CODENAME=`egrep \\'UBUNTU_CODENAME|VERSION_CODENAME\\' /etc/os-release | sort | head -1 | cut -d= -f2`
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

         CODENAME=`egrep \\'UBUNTU_CODENAME|VERSION_CODENAME\\' /etc/os-release | sort | head -1 | cut -d= -f2`
         if [ -z "$CODENAME" ]
         then
            CODENAME=`lsb_release -c -s`
         fi
         wget -O - https://nuitka.net/deb/archive.key.gpg | sudo apt-key add -
         sudo apt-get install ca-certificates
         sudo echo >/etc/apt/sources.list.d/nuitka.list "deb https://nuitka.net/deb/develop/$CODENAME $CODENAME main"
         sudo apt-get update
         sudo apt-get install nuitka

   **RHEL**

   - |RHEL_LOGO| repositories

      .. code:: bash

         # Detect the RHEL version
         eval `grep VERSION_ID= /etc/os-release`

         yum-config-manager --add-repo http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-${VERSION_ID}/home:kayhayen.repo

         # Install only one of these, not both.
         yum install nuitka
         yum install nuitka-unstable

      .. include:: rhel-downloads.inc

   **CentOS**

   - |CENTOS_LOGO| repositories

      .. code:: bash

         # CentOS 6:
         yum-config-manager --add-repo http://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/home:kayhayen.repo
         # CentOS 7
         yum-config-manager --add-repo http://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/home:kayhayen.repo
         # CentOS 8
         yum-config-manager --add-repo http://download.opensuse.org/repositories/home:/kayhayen/CentOS_8/home:kayhayen.repo

         # Install only one of these, not both.
         yum install nuitka
         yum install nuitka-unstable

   .. include:: centos-downloads.inc

   **Fedora**

   - |FEDORA_LOGO| repositories

      .. code:: bash

         # Detect the Fedora version
         eval `grep VERSION_ID= /etc/os-release`

         # Use yum on older versions
         dnf config-manager --add-repo https://download.opensuse.org/repositories/home:/kayhayen/Fedora_${VERSION_ID}/home:kayhayen.repo

         # Install only one of these, not both.
         dnf install nuitka
         dnf install nuitka-unstable

      .. include:: fedora-downloads.inc

   **Suse**

   - |SUSE_LOGO| repositories

      .. code:: bash

         # Detect the OpenSUSE leap version
         eval `grep VERSION_ID= /etc/os-release`

         # Add Nuitka repo
         zypper ar -f https://download.opensuse.org/repositories/home:/kayhayen/Open_${VERSION_ID}/home:kayhayen.repo

         # Install only one of these, not both.
         zypper install nuitka
         zypper install nuitka-unstable

      .. include:: suse-downloads.inc

   **Arch**

      -  |ARCH_LOGO| Stable: Arch Linux, execute \`\`pacman -S nuitka\`\`

   **Gentoo**

      -  |GENTOO_LOGO| Gentoo Linux, execute \`\`emerge -a dev-python/nuitka\`\`

.. dropdown:: macOS

   No installer is available for macOS. Use the source packages, clone from
   git, or use PyPI.

.. dropdown:: Source Code

   .. include:: source-downloads.inc

   .. note::

      The source archives can be used directly after unpacking, simply
      start with ``python bin/nuitka --help``. They do not even have to be installed.

.. dropdown:: GitHub

   -  |GIT_LOGO| Stable: **git clone --branch main
      https://github.com/Nuitka/Nuitka**

   -  |GIT_LOGO| Develop: **git clone --branch develop
      https://github.com/Nuitka/Nuitka**

   Visit https://github.com/Nuitka/Nuitka for the Nuitka repository on
   GitHub.

For commercial support and advanced features, see :doc:`Nuitka
Commercial <commercial>`.

.. _nuitka-standard-license:

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

.. include:: ../variables.inc

.. include:: ../dynamic.inc
