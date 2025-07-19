:orphan:

##########################################
 Python.h header file not found by Nuitka
##########################################

****************************
 The Problem in a Few Words
****************************

Nuitka uses a "Backend C" compiler to create program code. That applies
to all outputs: extension modules, accelerated binaries, standalone, or
onefile. During this final phase, for the Python build from C code, the
``Python.h`` file was not found.

************
 Background
************

This file is used to be able to create C code that integrates with
Python, which is what Nuitka does. It is absolutely required.

*************
 Consequence
*************

If you are using a system Python, execute the command from this table,
it may require root rights.

Commands to install Python.h

+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| Distribution Family    | Python Version   | Example Command                                                                                          |
+========================+==================+==========================================================================================================+
| Debian / Ubuntu / Mint | Python 3.x       | ``sudo apt-get install python3-dev`` (or e.g. ``python3.11-dev`` for a specific version)                 |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| Debian / Ubuntu / Mint | Python 2.7       | ``sudo apt-get install python-dev``                                                                      |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| RHEL / CentOS / Fedora | Python 3.x       | ``sudo dnf install python3-devel`` (use ``yum`` on older systems like CentOS 7)                          |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| RHEL / CentOS / Fedora | Python 2.7       | ``sudo dnf install python-devel`` (use ``yum`` on older systems like CentOS 7)                           |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| SUSE / openSUSE        | Python 3.x       | ``sudo zypper install python3-devel``                                                                    |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| SUSE / openSUSE        | Python 2.7       | ``sudo zypper install python-devel``                                                                     |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| Alpine Linux           | Python 3.x       | ``sudo apk add python3-dev``                                                                             |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| Alpine Linux           | Python 2.7       | ``sudo apk add python2-dev``                                                                             |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| Arch Linux             | Python 3.x       | ``sudo pacman -S python`` (headers are included)                                                         |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| Termux (Android)       | Python 3.x       | ``pkg install python``                                                                                   |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| Termux (Android)       | Python 2.7       | ``pkg install python2``                                                                                  |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
| Anaconda               | Python 2.x / 3.x | Development headers are included with the ``python`` package. (e.g., ``conda create -n my_env python``)  |
+------------------------+------------------+----------------------------------------------------------------------------------------------------------+
