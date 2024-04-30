:orphan:

.. meta::
   :description: User Manual of Nuitka with the details on how to use it
   :keywords: python,compiler,nuitka,manual

####################
 Nuitka User Manual
####################

This page is the recommended first read when you start using **Nuitka**.

This page will teach you more about **Nuitka** fundamentals and is the
recommended first read when you start using **Nuitka**.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

**************
 Requirements
**************

To ensure smooth work of **Nuitka**, make sure to follow the system
requirements that include the following components:

.. contents::
   :depth: 1
   :local:

C Compiler
==========

You need a C compiler with support for **C11** or for older Python only,
a **C++** compiler for **C++03** [#]_.

**For Windows**, use one of the following compilers:

-  `Visual Studio 2022
   <https://www.visualstudio.com/en-us/downloads/download-visual-studio-vs.aspx>`_
   or higher. Use the default English language pack to enable **Nuitka**
   to filter away irrelevant outputs and, therefore, have the best
   results.

   Using ``--msvc=latest`` enforces using this compiler.

-  The **MinGW64** compiler (used with ``--mingw64``) option, must be
   the one Nuitka downloads, and it enforces that because there were
   very frequent breakage with the complete tooling used.

   Nuitka will offer to automatically download it if no usable C
   compiler is found. Using ``--mingw64`` enforces using this compiler.

-  The **Clang-cl** compiler can be used if provided by the **Visual
   Studio** installer or Using ``--clang`` on Windows enforces the one
   from Visual Studio.

-  The **Clang** compiler can be used from from the **MinGW64**
   download.

   Using ``--mingw64 --clang`` enforces using this **Clang**.

**For Linux**, use either the **GCC** from the system or an installed
**clang**.

**For macOS**, use the system **Clang** compiler. Install XCode via
Apple Store to be covered.

**For FreeBSD** on most architectures, use **Clang** or **GCC**, ideally
matching the system compiler.

**For other platforms**, use the **GCC** compiler of at least version
5.1 or higher. Use back-ports such as EPEL or SCL.

.. [#]

   Support for this **C11** is given with **GCC 5.1** or higher and all
   **Clang** versions

   The older **MSVC** compilers don't do it yet. But as a workaround, with
   Python 3.10 or older, the **C++03** language standard is significantly
   enough overlapping with **C11**, such that it is then used instead.

Python
======

|SUPPORTED_PYTHONS| are supported. If a stable Python release isn't
listed here, don't worry; it's being worked on and added as soon as
possible.

.. admonition:: Special cases need 2 Python installations

   In some scenarios, you might need to download an additional Python
   version. To get to know more, read the following statements:

-  If you use **Python 3.4**, additionally install either **Python 2**
   or **Python 3.5+**. You will need it during the compile time because
   **SCons** (which orchestrates the C compilation) does not support
   **Python 3.4**, but **Nuitka** does for some commercial users
   targeting Windows XP.

-  If you use the **Windows** opening system, don't use **Python 2**
   because **clcache** doesn't work with it. Install **Python 3.5+**
   instead. **Nuitka** finds these needed Python versions (for example,
   on **Windows** via registry) and you shouldn't notice it as long as
   they are installed.

-  Other functionality is available when another Python has a certain
   package installed. For example, **Python 2.x** can use onefile
   compression if another Python with the **zstandard** package is
   installed as well.

.. admonition:: Important considerations

   -  **Moving binaries to other machines:** The created binaries can be
      made executable independent of the Python installation, with
      ``--standalone`` and ``--onefile`` options.

   -  **Binary filename suffix:** The created binaries have an ``.exe``
      suffix on Windows. On other platforms, they have either no suffix
      in standalone mode or the ``.bin`` suffix, that you are free to
      remove or change, or specify with the ``-o`` option. The suffix
      for acceleration mode is added to make sure that the original
      script name and the binary name do not ever collide, so we can
      safely overwrite the binary without destroying the source file.

   -  **Module mode filenames:** Python Extension modules cannot be
      renamed without breaking them, the filename and the module name
      have to match, so you must change the source filename to get the
      desired result.

   -  **It has to be a standard Python implementation:** You need a form
      of standard Python implementation, called **CPython**, to execute
      **Nuitka** because it's closely tied to the implementation details
      of it. Ideally, you use the `official Python
      <https://python.org>`__ only.

   -  **Homebrew (for macOS) is supported, but not ideal:** The
      resulting binaries are not as portable and specifically not
      backward portable.

   -  **Anaconda Python is supported:** The Anaconda distribution is
      making special adaptations for some ``conda`` packages that lead
      to errors and might have to be reported as issues, such that
      special treatment can be added.

   -  **Python from Microsoft Store**: Don't download Python from
      **Microsoft Store**, as it doesn't work properly.

   -  **Pyenv on macOS:** It is known that **macOS** **pyenv** does not
      work. Use **Homebrew** instead for self-compiled Python
      installations.

Operating System
================

**Nuitka** supports the following operating systems: **Linux**,
**FreeBSD**, **NetBSD**, **macOS**, and **Windows** (32 bits/64
bits/ARM).

The portability is excellent, therefore other operating systems will
work as well.

However, specific adjustments might be necessary, such as modifying
Nuitka's internal **SCons** usage or providing additional flags. Ensure
that the Python version matches the architecture of the C compiler, or
else you will get cryptic error messages.

Architecture
============

Supported Architectures are **x86**, **x86_64** (**AMD64**), and
**ARM**.

**Nuitka** generally does not use any hardware specifics and produces
portable C code. Therefore, many other architectures work out of the box
as well.

Generally, the architectures that **Debian** or **RHEL** support can be
considered good and tested, too; for example, **RISC-V** won't pose any
issues.

**************
 Installation
**************

For most systems, there will be packages on the `download page
<https://nuitka.net/doc/download.html>`__ of Nuitka. You can also
install it from the source code via the standard ``python setup.py
install`` routine.

Notice for integration with GitHub workflows, there is this
`Nuitka-Action <https://github.com/Nuitka/Nuitka-Action>`__ that you
should use that makes it easy to integrate. You ought to start with a
local compilation to iron out issues, but for deployment to multiple
platforms, **Nuitka-Action** will make that very easy with **Nuitka**.

Read also about the :ref:`Nuitka License <nuitka-standard-license>`.

********************
 Command Line Usage
********************

To use **Nuitka** via the command line, select one of the following ways
to ensure smooth execution.

Recommended way
===============

To execute **Nuitka** in the recommended way, enter the following
command:

.. code:: bash

   <the_right_python> -m nuitka

.. admonition:: Note

   Replace ``<the_right_python>`` with the specific Python interpreter
   executable you want to use. For example, ``python3.9 -m nuitka``.

By executing this command, you can know with certainty which Python
interpreter you are using with Nuitka and your uncompiled program.

Direct way
==========

Alternatively, you can run **Nuitka** directly from a source checkout
(or archive) without altering environment variables. You can execute
**Nuitka** seamlessly without having to manipulate the ``PYTHONPATH``
variable.

Simply execute the ``nuitka`` script directly without changing the
environment. You could add the ``bin`` directory to your ``PATH`` for
convenience, but that is optional; just use a qualified path to execute
it.

Moreover, if you want to execute with the right interpreter, run the
following command:

.. code:: bash

   <the_right_python> bin/nuitka

.. admonition:: Note

   If you encounter the **SyntaxError** message, you most certainly have
   picked the wrong interpreter for the program you are compiling.

Nuitka has a ``--help`` option to display its available functionalities.
To view it, run the following command:

.. code:: bash

   python -m nuitka --help

.. _data-files:

************
 Data Files
************

Data files are all the files of your Python program except for code.
These files might be images, configuration files, or text documents.
**Nuitka** offers several options to handle these data files during the
compilation.

.. _code-is-not-data-files:

Code is not Data Files
======================

.. important::

   Code is not Data Files

   Nuitka does not consider code to be data files and will not include
   DLLs or Python files as data files. Because code files without proper
   treatment will not work on other systems unless you know what you are
   doing.

In the following table, we list code file types.

+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| Suffix     | Rationale                                                                             | Solution                                                                                               |
+============+=======================================================================================+========================================================================================================+
| ``.py``    | Nuitka trims even the stdlib modules to be included. If it doesn't see Python code,   | Use ``--include-module`` on them instead                                                               |
|            | there is no dependencies analyzed, and as a result it will just not work.             |                                                                                                        |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``.pyc``   | Same as ``.py``.                                                                      | Use ``--include-module`` on them from their source code instead.                                       |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``.pyo``   | Same as ``.pyc``.                                                                     | Use ``--include-module`` on them from their source code instead.                                       |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``.pyw``   | Same as ``.py``.                                                                      | For including multiple programs, use multiple ``--main`` arguments instead.                            |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``.pyi``   | These are ignored, because they are code-like and not needed at run time. For the     | Raise an issue if 3rd part software needs it.                                                          |
|            | ``lazy`` package that actually would depend on them, we made a compile time solution  |                                                                                                        |
|            | that removes the need.                                                                |                                                                                                        |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``.pyx``   | These are ignored, because they are Cython source code not used at run time           |                                                                                                        |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``.dll``   | These are ignored, since they **usually** are not data files. For the cases where 3rd | Create Nuitka Package configuration for those, with ``dll`` section for the package that uses them.    |
|            | party packages do use them as data, e.g. ``.NET`` packages, we solve that in package  | For rare cases, a ``data-files`` section with special configuration might be the correct thing to do.  |
|            | configuration for it.                                                                 |                                                                                                        |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``.dylib`` | These are ignored since they are macOS extension modules or DLLs.                     | Need to add configuration with ``dll`` section or ``depends`` that are missing                         |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``.so``    | These are ignored, since they are Linux, BSD, etc. extension modules or DLLs.         | Need to add configuration with ``dll`` section or ``depends`` that are missing                         |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``.exe``   | They are binaries on Windows.                                                         | You can add Nuitka Package configuration to include those as DLLs and mark them as ``executable: yes`` |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``.bin``   | They are binaries to non-Windows, otherwise same as ``.exe``.                         |                                                                                                        |
+------------+---------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+

Package data ``--include-package-data=PACKAGE``
===============================================

Include data files for the given package name. Data files of packages
are not included by default, but package configuration should do it, or
this option can be used. If you find you need to do it for a third-party
package, feel free to let us know through an :ref:`issue report
<github-issue-tracker>` as we strive to make most packages work out of
the box.

DLLs and Python extension modules are not data files and are, by
default, never included by this option. See
:ref:`code-is-not-data-files` for more information about why.

You can use patterns for the filenames as indicated. After a ``:``
optionally, a filename pattern may be specified as well, selecting only
matching files.

Examples:
   -  ``--include-package-data=package_name`` (all files)
   -  ``--include-package-data=package_name=*.txt`` (only certain type)
   -  ``--include-package-data=package_name=some_filename.dat``
      (concrete file)

Data files by file patterns ``--include-data-files``
====================================================

Include data files by filenames in the distribution. Generally do not
use this for package data; see above for that there is
``--include-package-data`` that is easier to use and more likely
correct.

There are several allowed forms.

   -  ``--include-data-files=/path/to/file/some.txt=folder_name/some.txt``
      will copy a single file.

   -  ``--include-data-files=/path/to/file/*.txt=folder_name/some.txt``
      will copy a single file and complain if it's multiple sources, the
      use of a pattern is entirely for convenience here.

   -  ``--include-data-files=/path/to/files/*.txt=folder_name/`` will
      put all matching files into that folder.

   -  For a recursive copy, there is a form with three separated values
      ``--include-data-files=/path/to/scan=folder_name=**/*.txt`` that
      will preserve the directory structure and only copy files
      matching.

.. note::

   You can also use variables here if you use Nuitka project options,
   the most useful being ``{MAIN_DIRECTORY}`` that will allow you refer
   to where the compiled program lives and use relative paths to that.

Data files by directories ``--include-data-dir=DIRECTORY``
==========================================================

Include data files from a complete directory in the distribution. This
is recursive, meaning it includes files from subdirectories as well.

-  Use patterns with ``--include-data-files`` if you want non-recursive
   inclusion.

-  With ``--include-data-dir=/path/some_dir=data/some_dir`` you can
   include a data directory as a whole in the distribution.

-  Use the ``--noinclude-data-files`` to remove files that matched, but
   you want to exclude them. In this fashion, those options work in
   reverse to ``--include-data-files``.

Copy data files near the onefile ``--include-onefile-external-data=PATTERN``
============================================================================

Include the specified data file patterns outside of the onefile binary,
rather than on the inside. It of course only makes sense in case of
``--onefile`` compilation. First files have to be specified as included
somehow, then this refers to target paths, and rather than copying to
the distribution, the path then refers to alongside the onefile
executable produced.

.. _tweaks:

********
 Tweaks
********

This section includes customization options to enhance the appearance
and functionality of compiled binaries.

Icons
=====

The icon tweak allows you to customize the visual appearance of the
resulting executable file. This icon is what users will see when they
look at the file in their file explorer and in the taskbar or dock.

On **Windows**, you can provide a **PNG** file, an icon file, or a
template executable. These create binaries with icons on **Windows** and
may even be combined:

.. code:: bash

   python -m nuitka --onefile --windows-icon-from-ico=your-icon.png program.py
   python -m nuitka --onefile --windows-icon-from-ico=your-icon.ico program.py
   python -m nuitka --onefile --windows-icon-template-exe=your-icon.ico program.py

These create application bundles with icons on **macOS**:

.. code:: bash

   python -m nuitka --macos-create-app-bundle --macos-app-icon=your-icon.png program.py
   python -m nuitka --macos-create-app-bundle --macos-app-icon=your-icon.icns program.py

.. note::

   With **Nuitka**, you don't have to create platform-specific icons
   manually. Instead, it seamlessly converts various formats, such as
   **PNG** and others on the go during the build process.

MacOS Entitlements
==================

Entitlements define the capabilities and permissions that the
application has when running, such as access to audio, camera, or
calendar. Entitlements for a **macOS** application bundle can be added
with the option ``--macos-app-protected-resource`` (**macOS** only).

For example, if you want to request access to a microphone, use the
following option value
``--macos-app-protected-resource="NSMicrophoneUsageDescription:Microphone
access"`` giving the Apple identifier, and a human-readable one.

See the complete list in the `Protected resources
<https://developer.apple.com/documentation/bundleresources/information_property_list/protected_resources>`__
page.

.. note::

   If you have spaces in the entitlement description, make sure to quote
   the argument value. That prevents your shell from interpreting the
   spaces as separate arguments for **Nuitka** and make sure that the
   description is correctly passed through to **Nuitka**.

Windows UAC Configuration
=========================

Request **Windows User Account Control** (**UAC**), to grant admin
rights on execution with ``--windows-uac-admin`` (**Windows** only). By
default, **Nuitka** compiles programs to run without special privileges.

Request **Windows User Account Control** (**UAC**), to enforce prompting
on the remote desktop with ``--windows-uac-uiaccess`` (**Windows**
only). See `Microsoft Documentation
<https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/user-account-control-allow-uiaccess-applications-to-prompt-for-elevation-without-using-the-secure-desktop>`__
on the topic for details about this.

Console Window
==============

On **Windows**, programs can open a console by default. You can change
that with the ``--disable-console`` option. That makes them suitable for
output visibility or easy debugging of program errors, which is
essential.

In Python, there is also a difference between **pythonw.exe** and
**python.exe** along those lines. **Nuitka** replicates that with the
option ``--disable-console``.

**Nuitka** itself recommends this option, especially when using **GUI**
packages like **PySide6** or **wx**, but it may not cover all those
cases. In case you know your program is a console application, use
``--enable-console``, which will get rid of these kinds of outputs from
**Nuitka**.

.. note::

   You cannot use **pythonw.exe** with **Nuitka**, as you won't be able
   to see its output.

Splash screen
=============

Splash screens are helpful when program startup is slow. The startup of
**Nuitka** in **Onefile** is fast, but your program might need more
time. Moreover, you can't be sure how fast the computer used will be, so
it might be a good idea to have splash screens. Luckily, with
**Nuitka**, they are easy to add for **Windows**.

For the splash screen, you need to specify it as a **PNG** file. Make
sure to turn off the splash screen when your program is ready, meaning
it has completed the imports, prepared the window, or connected to the
database. To combine the code with the creation, compile the following
project syntax:

.. code:: python

   # nuitka-project: --onefile
   # nuitka-project: --onefile-windows-splash-screen-image={MAIN_DIRECTORY}/Splash-Screen.png

   # Whatever this is, obviously
   print("Delaying startup by 10s...")
   import time, tempfile, os
   time.sleep(10)

   # Use this code to signal the splash screen removal.
   if "NUITKA_ONEFILE_PARENT" in os.environ:
      splash_filename = os.path.join(
         tempfile.gettempdir(),
         "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"]),
      )

      if os.path.exists(splash_filename):
         os.unlink(splash_filename)

   print("Done... splash should be gone.")
   ...

   # Rest of your program goes here.

Reports
=======

For analysis of your program and **Nuitka** packaging, the
:ref:`Compilation Report <compilation-report>` is available. You can
also make custom reports by providing your template or using one
built-in to **Nuitka**. These reports carry all the detailed
information; for example, when a module is imported but not found, you
can see where that happens.

.. note::

   We highly recommend that you provide the Compilation Report when
   reporting issues. This report, with its detailed information, is a
   reliable tool for troubleshooting. It allows you to share precise
   insights into your program's compilation, aiding in swiftly resolving
   any issues that may arise.

Version Information
===================

You can attach copyright and trademark information, company name,
product name, and other elements to your compilation. You will see it in
the version information for the created binary on **Windows** or the
application bundle on **macOS**.

.. note::

   For some version options, you can put any text you choose here, but
   make sure to quote the new lines appropriately for the shell to see
   this is one argument.

Product Name
------------

With the ``--product-name`` option, you specify the product's name to
use in version information. Defaults to the base filename of the created
binary; for example, when compiling ``MySoftware.py``, it becomes
``MySoftware``, but you can override it as you choose.

Product Version
---------------

For **Windows**, there is a distinction between file and product
version, and **Nuitka** will, where applicable, also combine the two
into a single one if you specify both.

Use ``--product-version`` and ``--file-version`` to provide full version
information. It must be up to 4 numbers; for example, ``1.0.0.0``
and``1.0`` will also be accepted. For **Windows** version information,
**Nuitka** adds zeros automatically. Non-numbers are not allowed here.

File Description
----------------

You can also describe the created binary for use in the version
information with the option ``--file-description``, by default on
**Windows**, because it's mandatory in version information **Nuitka**
uses the binary filename, so for example, ``MySoftware.py`` becomes
``MySoftware.exe``, but it's better for you to provide one.

Copyright
---------

You can specify legal copyright information to display in the version
information with the ``--copyright`` option.

Trademarks
----------

You can specify legal trademark information to display in the version
information with the ``--trademark`` option.

.. _compilation-report:

********************
 Compilation Report
********************

When you use ``--report=compilation-report.xml`` Nuitka will create an
XML file with detailed information about the compilation and packaging
process. This is growing in completeness with every release and exposes
module usage attempts, timings of the compilation, plugin influences,
data file paths, DLLs, and reasons why things are included or not.

At this time, the report contains absolute paths in some places, with
your private information. The goal is to make this blended out by
default because we also want to become able to compare compilation
reports from different setups, for example with updated packages, and
see the changes to Nuitka. The report is, however, recommended for your
bug reporting.

Also, another form is available, where the report is free form and
according to a Jinja2 template of yours and one that is included in
Nuitka. The same information used to produce the XML file is accessible.
However, right now, this is not yet documented, but we plan to add a
table with the data. For a reader of the source code who is familiar
with Jinja2, however, it will be easy to do it.

If you have a template, you can use it like this
``--report-template=your_template.rst.j2:your_report.rst`` and of
course, the usage of restructured text, is only an example. You can use
Markdown, your own XML, or whatever you see fit. Nuitka will just expand
the template with the compilation report data.

Currently, the following reports are included in Nuitka. You just use
the name as a filename, and Nuitka will pick that one instead.

+---------------+--------------+--------------------------------------------------------+
| Report Name   | Status       | Purpose                                                |
+===============+==============+========================================================+
| LicenseReport | experimental | Distributions used in a compilation with license texts |
+---------------+--------------+--------------------------------------------------------+

.. note::

   The community can and should contribute more report types and help
   enhancing the existing ones for good looks.

***************************
 Unsupported functionality
***************************

The ``co_code`` attribute of code objects
=========================================

The code objects are empty for compiled functions. There is no bytecode
with Nuitka's compiled function objects, so there is no way to provide
it.

PDB
===

There is no tracing of compiled functions to attach a debugger to.

.. include:: ../variables.inc
