.. meta::
   :description: Download the Python compiler Nuitka and make your code faster today.
   :keywords: nuitka,download,RedHat,RHEL,CentOS,Debian,Mint,Arch,Fedora,SuSE,FreeBSD,OpenBSD,AIX,PyPI,git,source

##################
 Nuitka Downloads
##################
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

      -  |ARCH_LOGO| Stable: Arch Linux, execute \`\`pacman -S nuitka\`\` or use from AUR https://aur.archlinux.org/packages/nuitka

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
