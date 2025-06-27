.. meta::
   :description: Download the Python compiler Nuitka and make your code faster today.
   :keywords: nuitka,download,redhat,centos,debian,mint,freebsd,openbsd,arch,PyPI,git

##################
 Nuitka Downloads
##################

***************
 Quick Install
***************

Nuitka is a Python compiler that makes your code faster and easier to
distribute.

**Recommended: Install via PyPI (all platforms)**

.. code:: bash

   python -m pip install -U nuitka

For the latest development version:

.. code:: bash

   python -m pip install -U "https://github.com/Nuitka/Nuitka/archive/develop.zip"

.. note::

   Use the Python interpreter you want to compile with, that is the
   easiest way. And also invoke as ``python -m nuitka`` with that
   interpreter. It is the easiest and most reliable way.

**Other install options:**

.. dropdown:: Linux Packages (Debian, Ubuntu, Fedora, etc.)

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

   |RHEL_LOGO| repositories

   .. code:: bash

      # Detect the RHEL version
      eval `grep VERSION_ID= /etc/os-release`

      yum-config-manager --add-repo http://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-${VERSION_ID}/home:kayhayen.repo

      # Install only one of these, not both.
      yum install nuitka
      yum install nuitka-unstable

   .. include:: rhel-downloads.inc

   **CentOS**

   |CENTOS_LOGO| repositories

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

   |FEDORA_LOGO| repositories

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

   |SUSE_LOGO| repositories

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

   -  |ARCH_LOGO| Develop: Arch Linux `Nuitka from git develop
      <https://aur.archlinux.org/packages/nuitka-git/>`_

   **Gentoo**

   -  |GENTOO_LOGO| Gentoo Linux, execute \`\`emerge -a dev-python/nuitka\`\`

   **macOS**

   No installer is available for macOS. Use the source packages, clone from
   git, or use PyPI.

.. dropdown:: Source Code

   .. include:: source-downloads.inc

   .. note::

      The source archives can be used directly after unpacking, simply
      start with \`\`python bin/nuitka --help\`\` and read \`\`README.pdf\`\` or
      \`\`README.rst\`\` to get started. Take especially care to read the User
      Manual, such that you don\\'t go on a wrong track.

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