:orphan:

.. meta::
   :description: User Manual of Nuitka with the details on how to use it
   :keywords: python,compiler,nuitka,manual

####################
 Nuitka User Manual
####################

This page is the recommended first read when you start using **Nuitka**.
On this page, you will learn more about **Nuitka** fundamentals, such as
license type, use cases, requirements, and credits. This page is the
recommended first read when you start using **Nuitka**. On this page,
you will learn more about **Nuitka** fundamentals, such as requirements,
installation guidelines, and tips.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

**************
 Requirements
**************

To ensure smooth work of **Nuitka**, make sure to follow system
requirements, that include the following components:

.. contents::
   :depth: 1
   :local:

C Compiler
==========

You need a C compiler with support for **C11** or alternatively a
**C++** compiler for **C++03** [#]_.

**For Windows**, use one of the following compilers:

-  The **MinGW64 C11** compiler must be based on **gcc 11.2** or higher.
   It will be automatically downloaded if no usable C compiler is found,
   which is the recommended way of installing it, as Nuitka will also
   upgrade it for you.

-  `Visual Studio 2022
   <https://www.visualstudio.com/en-us/downloads/download-visual-studio-vs.aspx>`_
   or higher. Use the default English language pack to enable **Nuitka**
   to filter away irrelevant outputs and, therefore, have the best
   results.

-  The **Clang-cl** compiler can be used if provided by the **Visual
   Studio** installer.

**For macOS**, use the **Clang** compiler. It's also compatible with
most **FreeBSD** architectures.

**For other platforms**, use the **GCC** compiler of at least version
5.1, and below that the **G++** compiler of at least version 4.4 as an
alternative.

.. [#]

   Support for this **C11** is given with **gcc 5.x** or higher or any
   **clang** version.

   The older **MSVC** compilers don't do it yet. But as a workaround, with
   Python 3.10 or older, the C++03 language standard is significantly
   overlapping with C11, it is then used instead.

Python
======

|SUPPORTED_PYTHONS| are supported. If a stable Python release isn't
listed here, don't worry; it's being worked on and will be added soon.

.. important::

   You might need to download an additional Python version. To get to
   know more, read the following statements:

-  If you use **Python 3.4**, additionally install **Python 2** or
   **Python 3.5+**. You will need it during the compile time because
   **SCons** (which orchestrates the C compilation) does not support
   **Python 3.4**.

-  If you use the **Windows** opening system, don’t use **Python 2**
   because **clcache** doesn’t work with it. Install **Python 3.5+**
   instead. **Nuitka** finds these needed Python versions (for example,
   on **Windows** via registry) and you shouldn’t notice it as long as
   they are installed.

-  Other functionality is available when another Python has a certain
   package installed. For example, **Python 2.x** can use onefile
   compression if another Python with the **zstandard** package is
   installed.

.. admonition:: Important considerations

   -  **Moving binaries to other machines:** The created binaries can be
      made executable independent of the Python installation, with
      ``--standalone`` and ``--onefile`` options.

   -  **Binary filename suffix:** The created binaries have an ``.exe``
      suffix on Windows. On other platforms they have no suffix for
      standalone mode, or ``.bin`` suffix, that you are free to remove
      or change, or specify with the ``-o`` option. The suffix for
      acceleration mode is added just to be sure that the original
      script name and the binary name do not ever collide, so we can
      safely overwrite the binary without destroying the original source
      file.

   -  **It has to be standard Python implementation**: You need the
      standard Python implementation, called **CPython**, to execute
      **Nuitka** because it's closely tied to implementation details of
      it. You can also use **Homebrew** (for macOS) or **Anaconda
      Python**.

   -  **Python from Microsoft Store**: Don’t download Python from
      **Microsoft Store**, as it doesn’t work properly.

   -  **Pyenv on macOS:** It is known that **macOS** **pyenv** does not
      work. Use **Homebrew** instead for self-compiled Python
      installations. Note that standalone mode will be worse on these
      platforms and not be as backward compatible with older **macOS**
      versions.

Operating System
================

**Nuitka** supports the following operating systems: **Linux**,
**FreeBSD**, **NetBSD**, **macOS**, and **Windows** (32 bits/64
bits/ARM).

Other operating systems will work as well. The portability is expected
to be generally good. However, specific adjustments might be necessary,
such as modifying Nuitka's internal **SCons** usage or providing
additional flags. Ensure that the Python version matches the
architecture of the C compiler, or else you will get cryptic error
messages.

Architecture
============

Supported Architectures are **x86**, **x86_64** (**AMD64**), and
**ARM**.

Other architectures are expected to also work out of the box, as
**Nuitka** is generally not using any hardware specifics. These are just
the ones tested and known to be good. Generally, the architectures that
**Debian** supports can be considered good and tested, too.

**************
 Installation
**************

For most systems, there will be packages on the `download page
<https://nuitka.net/doc/download.html>`__ of Nuitka. But you can also
install it from source code as described above, but also like any other
Python program it can be installed via the normal ``python setup.py
install`` routine.

Notice for integration with GitHub workflows there is this
`Nuitka-Action <https://github.com/Nuitka/Nuitka-Action>`__ that you
should use that makes it really easy to integrate. You ought to start
with a local compilation though, but this will be easiest for cross
platform compilation with **Nuitka**.

Read also about `Nuitka license
<https://nuitka.net/doc/download.html>`_.

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

By executing this command, you can be absolutely certain which Python
interpreter you are using, so it is easier to match with what Nuitka
has.

Direct way
==========

Alternatively, you can run **Nuitka** directly from a source checkout or
archive, without any need for altering environment variables.
Importantly, you can execute **Nuitka** seamlessly without having to
manipulate the ``PYTHONPATH`` variable. You just execute the ``nuitka``
and ``nuitka-run`` scripts directly without any changes to the
environment. You may want to add the ``bin`` directory to your ``PATH``
for your convenience, but that step is optional.

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

************
 Data Files
************

Data files are all the files of your Python program except for code.
These files might be images, configuration files, or text documents.
**Nuitka** offers several options to handle these data files during the
compilation.

----

``--include-package-data=PACKAGE``
==================================

Include data files for the given package name. Dynamic-link libraries
and extension modules are not data files and never included like this.
Can use patterns the filenames as indicated below. Data files of
packages are not included by default, but package configuration can do
it. This will only include non-DLL, non-extension modules, i.e. actual
data files. After a ``:`` optionally a filename pattern can be given as
well, selecting only matching files.

Examples:
   -  ``--include-package-data=package_name`` (all files)
   -  ``--include-package-data=package_name=*.txt`` (only certain type)
   -  ``--include-package-data=package_name=some_filename.dat``
      (concrete file)

Default empty.

----

``--include-data-files=DESC``
=============================

Include data files by filenames in the distribution.

There are many allowed forms.
   -  ``--include-data-files=/path/to/file/.txt=folder_name/some.txt``
      will copy a single file and complain if it's multiple.

   -  ``--include-data-files=/path/to/files/.txt=folder_name/`` will put
      all matching files into that folder.

   -  For recursive copy there is a form with 3 values
      ``--include-data-files=/path/to/scan=folder_name=**/*.txt`` that
      will preserve directory structure.

Default empty.

----

``--include-data-dir=DIRECTORY``
================================

Include data files from complete directory in the distribution. This is
recursive, meaning it includes files from subdirectories as well.

-  Use patterns with ``--include-data-files`` if you want non-recursive
   inclusion. For example,
   ``--include-data-dir=/path/some_dir=data/some_dir`` illustrates how
   to include a directory and its contents in the distribution.

-  Use ``--noinclude-data-files`` to remove all non-code files.

Default empty.

----

``--include-onefile-external-data=PATTERN``
===========================================

Include the specified data file patterns outside of the onefile binary,
rather than on the inside. Makes only sense in case of ``--onefile``
compilation. First files have to be specified as included somehow, then
this refers to target paths.

Default empty.

----

``--list-package-data=LIST_PACKAGE_DATA``
=========================================

Output the data files found for a given package name.

Default not done.

----

.. _tweaks:

********
 Tweaks
********

This section includes customization options to enhance the appearance
and functionality of compiled binaries.

Icons
=====

The icon tweaks allow you to customize the visual appearance of the
resulting executable file. This icon is what users will see when they
look at the file on their computer or in their file explorer.

On **Windows**, you can provide **PNG** file, an icon file, or a
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
   **PNG** and others, on the go during the build process.

MacOS Entitlements
==================

Entitlements define the capabilities and permissions that the
application has when running, such as access to audio, camera, or
calendar. Entitlements for a **macOS** application bundle can be added
with the following option:

.. code:: bash

   --macos-app-protected-resource

For example, if you want to request access to a microphone, run the
following command:

.. code:: bash

   --macos-app-protected-resource=NSMicrophoneUsageDescription:Microphone access

See the full list in the `Protected resources
<https://developer.apple.com/documentation/bundleresources/information_property_list/protected_resources>`_
page.

.. note::

   If you have spaces in the entitlement description, make sure to quote
   it. This prevents your shell from interpreting the spaces as separate
   arguments for **Nuitka** and ensures that the description is
   correctly passed through to **Nuitka**.

Windows UAC Configuration
=========================

``--windows-uac-admin``

Request **Windows User Account Control** (**UAC**), to grant admin
rights on execution. (**Windows** only). By default, this option is
turned off.

----

``--windows-uac-uiaccess``

Request **Windows User Account Control** (**UAC**), to enforce running
from a few folders only, remote desktop access. (**Windows** only). By
default, this option is turned off.

----

Console Window
==============

On Windows, the console is opened by programs by default. You can change
it anytime. **Nuitka** follows this default behavior, making it
primarily suitable for terminal-based programs or those where output
visibility is essential. There is a difference between **pythonw.exe**
and **python.exe** along those lines. This is replicated in **Nuitka**
with the option ``--disable-console``.

**Nuitka** recommends this option, especially when using **GUI**
packages like **PySide6** or **wx**. In case, you know your program is
console application, use ``--enable-console`` which will get rid of
these kinds of outputs from **Nuitka**.

.. note::

   Avoid using **pythonw.exe** with **Nuitka**, as you won't see its
   output.

Splash screen
=============

Splash screens are useful when program startup is slow. **Onefile**
startup itself is fast, but your program might need more time. Moreover,
you can't be sure how fast the computer used will be, so it might be a
good idea to have splash screens. Luckily, with **Nuitka**, they are
easy to add for **Windows**.

For the splash screen, you need to specify it as a **PNG** file. Make
sure to disable the splash screen when your program is ready, meaning it
has completed the imports, prepared the window, or connected to the
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

For analysis of your program and **Nuitka** packaging, there is the
`Compilation Report`_ available. You can also make custom reports by
providing your template, with a few of them built-in to **Nuitka**.
These reports carry all the detail information, for example, when a
module was attempted to be imported, but not found, you can see where
that happens. For bug reporting, it's very much recommended to provide
the report.

Version Information
===================

You can attach copyright and trademark information, company name,
product name, and other elements to your compilation. You will see it in
the version information for the created binary on **Windows** or the
application bundle on **macOS**.

********************************
 Solutions to the Common Issues
********************************

Deployment Mode
===============

By default, **Nuitka** compiles without the ``--deployment`` flag,
keeping a set of safety guards and helpers active to troubleshoot any
misuses of **Nuitka**. You can learn more about this feature and its
benefits in the paragraphs below.

If you want to disable all these helpers, read more in the `Disabling
All`_ section.

Fork Bombs (Self-execution)
---------------------------

So after compilation, ``sys.executable`` is the compiled binary. Certain
Python packages like ``multiprocessing``, ``joblib``, or ``loky``
typically expect to run from a full ``Python`` environment with
``sys.executable``. They expect to use the ``-c command`` or ``-m
module_name`` options to be able to launch other code temporarily or
permanently as a service daemon.

However, with **Nuitka**, this executes your program again, and puts
these arguments in ``sys.argv`` where you maybe ignore them, and then
you fork yourself again to launch the helper daemons. This can lead to
unintentional forking, potentially resulting in a **fork bomb** scenario
where multiple processes spawn recursively, causing system freeze.

For example, running a Nuitka-compiled program may trigger the following
error:

.. code::

   ./hello.dist/hello.bin -l fooL -m fooM -n fooN -o fooO -p
   Error, the program tried to call itself with '-m' argument. Disable with '--no-deployment-flag=self-execution'.

To avoid this issue, ensure your program handles command line parsing
correctly and avoids using unsupported packages that attempt
re-execution. Additionally, you can disable this specific behavior at
compile time by using the ``--no-deployment-flag=self-execution`` flag.

Misleading Messages
-------------------

Some Python packages generate misleading error messages when they
encounter import failures. These messages may suggest actions, which may
not be the appropriate solution in the context of compiled programs.
**Nuitka** tries to correct them in non-deployment mode. Here is an
example, where **Nuitka** changes a message that asks to pip install
(which is not the issue) to point the user to the include command that
makes an ``imageio`` plugin work.

.. code:: yaml

   - module-name: 'imageio.core.imopen'
     anti-bloat:
       - replacements_plain:
           '`pip install imageio[{config.install_name}]` to install it': '`--include-module={config.module_name}` with Nuitka to include it'
           'err_type = ImportError': 'err_type = RuntimeError'
         when: 'not deployment'

And much more
-------------

The deployment mode is relatively new and has constantly more features
added, e.g. something for ``FileNotFoundError`` should be coming soon.

Disabling All
-------------

All these helpers can of course be disabled at once with
``--deployment`` but keep in mind that for debugging, you may want to
re-enable it. You might want to use **Nuitka Project** options and an
environment variable to make this conditional.

Should you disable them all?

We recommend selective disabling, but with **PyPI** upgrades and your
code changes, these issues can resurface. The space saved by deployment
mode is minimal, so we advise not to disable them. Instead, review each
feature, and if you know that it won't affect you, or you won't need it,
then disable it. Some upcoming features will be geared at beginner-level
usage.

Windows Virus Scanners
======================

If you compile binaries using **Nuitka's** default settings on
**Windows** without additional steps, some antivirus vendors may flag
them as malware. You can avoid this by purchasing the `Nuitka Commercial
<https://nuitka.net/doc/commercial.html>`_ plan. In this case, you will
get instructions and support on that matter.

Linux Standalone
================

For **Linux** standalone it's difficult to build a binary that works on
other **Linux** versions. This is mainly because on Linux, much software
is built specifically targeted to concrete dynamic-link libraries.

The solution is to compile your application on the oldest **Linux**
version you intend to support. However, this process can be exhausting,
involving setup complexities and security considerations since it
involves exposing your source code.

We recommend purchasing `Nuitka Commercial
<https://nuitka.net/doc/commercial.html>`_ plan, to overcome this issue
without extra efforts. **Nuitka Commercial** has container-based builds,
that you can use. This uses dedicated optimized Python builds, targeting
**CentOS 7** and supporting even newest Pythons and very old operating
systems. This solution streamlines the process by integrating recent C
compiler chains.

Program Crashes System (Fork Bombs)
===================================

A fork bomb is a program that spawn recursively, causing system crash.
This can happen, since ``sys.executable`` for compiled programs is not a
Python interpreter, and packages that try to do multiprocessing in a
better way, often relaunch themselves. **Nuitka** handles it with known
packages. However, you may encounter a situation where the detection of
this fails. To disable this protection, read about `Fork Bombs
(Self-execution)`_ option.

To handle fork bombs, use the ``--experimental=debug-self-forking``
option to check fork bombs behavior. To minimize risks associated with
fork bombs, put the following code snippet at the beginning of your
program.

.. code:: python

   import os, sys

   if "NUITKA_LAUNCH_TOKEN" not in os.environ:
      sys.exit("Error, need launch token or else fork bomb suspected.")
   else:
      del os.environ["NUITKA_LAUNCH_TOKEN"]

This code checks for the presence of a specific environment variable
**(NUITKA_LAUNCH_TOKEN)**. If it's not found, the program exits with an
error message. Otherwise, it removes the **NUITKA_LAUNCH_TOKEN** from
the environment, neutralizing any potential fork bomb threat.

**Nuitka** tries to handle fork bombs without the deployment option,
finding **"-c"** and **"-m"** options. However, the detection may not be
perfect or not work well with a package (anymore).

Memory issues and compiler bugs
===============================

In some cases, the C compilers will crash saying they cannot allocate
memory or that some input was truncated, or similar error messages,
clearly from it. These are example error messages, that are a sure sign
of too low memory, there is no end to them.

.. code::

   # gcc
   fatal error: error writing to -: Invalid argument
   Killed signal terminated program
   # MSVC
   fatal error C1002: compiler is out of heap space in pass 2
   fatal error C1001: Internal compiler error

There are several options you can explore here.

Ask Nuitka to use less memory
-----------------------------

There is a dedicated option ``--low-memory`` which influences decisions
of Nuitka, such that it avoids high usage of memory during compilation
at the cost of increased compile time.

Avoid 32 bit C compiler/assembler memory limits
-----------------------------------------------

Do not use a 32 bit compiler, but a 64 bit one. If you are using Python
with 32 bits on Windows, you most definitely ought to use MSVC as the C
compiler, and not MinGW64. The MSVC is a cross-compiler, and can use
more memory than gcc on that platform. If you are not on Windows, that
is not an option, of course. Also, using the 64 bit Python will work.

Use a minimal virtualenv
------------------------

When you compile from a living installation, that may well have many
optional dependencies of your software installed. Some software will
then have imports on these, and Nuitka will compile them as well. Not
only may these be just the troublemakers, they also require more memory,
so get rid of that. Of course, you do have to check that your program
has all the needed dependencies before you attempt to compile, or else
the compiled program will equally not run.

Use LTO compilation or not
--------------------------

With ``--lto=yes`` or ``--lto=no`` you can switch the C compilation to
only produce bytecode, and not assembler code and machine code directly,
but make a whole program optimization at the end. This will change the
memory usage pretty dramatically, and if your error is coming from the
assembler, using LTO will most definitely avoid that.

Switch the C compiler to clang
------------------------------

People have reported that programs that fail to compile with gcc due to
its bugs or memory usage work fine with clang on Linux. On Windows, this
could still be an option, but it needs to be implemented first for the
automatic downloaded gcc, that would contain it. Since MSVC is known to
be more memory effective anyway, you should go there, and if you want to
use Clang, there is support for the one contained in MSVC.

Add a larger swap file to your embedded Linux
---------------------------------------------

On systems with not enough RAM, you need to use swap space. Running out
of it is possibly a cause, and adding more swap space, or one at all,
might solve the issue, but beware that it will make things extremely
slow when the compilers swap back and forth, so consider the next tip
first or on top of it.

Limit the amount of compilation jobs
------------------------------------

With the ``--jobs`` option of Nuitka, it will not start many C compiler
instances at once, each competing for the scarce resource of RAM. By
picking a value of one, only one C compiler instance will be running,
and on an 8 core system, that reduces the amount of memory by factor 8,
so that's a natural choice right there.

Dynamic ``sys.path``
====================

If your script modifies ``sys.path``, e.g. inserts directories with
source code relative to it, Nuitka will not be able to see those.
However, if you set the ``PYTHONPATH`` to the resulting value, it will
be able to compile it and find the used modules from these paths as
well.

Manual Python File Loading
==========================

A very frequent pattern with private code is that it scans plugin
directories of some kind, and e.g. uses ``os.listdir``, then considers
Python filenames, and then opens a file and does ``exec`` on them. This
approach works for Python code, but for compiled code, you should use
this much cleaner approach, that works for pure Python code and is a lot
less vulnerable.

.. code:: python

   # Using a package name, to locate the plugins. This is also a sane
   # way to organize them into a directory.
   scan_path = scan_package.__path__

   for item in pkgutil.iter_modules(scan_path):
      importlib.import_module(scan_package.__name__ + "." + item.name)

      # You may want to do it recursively, but we don't do this here in
      # this example. If you'd like to, handle that in this kind of branch.
      if item.ispkg:
         ...

Missing data files in standalone
================================

If your program fails to find data file, it can cause all kinds of
different behavior, e.g. a package might complain it is not the right
version because a ``VERSION`` file check defaulted to an unknown. The
absence of icon files or help texts, may raise strange errors.

Often the error paths for files not being present are even buggy and
will reveal programming errors like unbound local variables. Please look
carefully at these exceptions, keeping in mind that this can be the
cause. If your program works without standalone, chances are data files
might be the cause.

The most common error indicating file absence is of course an uncaught
``FileNotFoundError`` with a filename. You should figure out what
package is missing files and then use ``--include-package-data``
(preferably), or ``--include-data-dir``/``--include-data-files`` to
include them.

Missing DLLs/EXEs in standalone
===============================

Nuitka has plugins that deal with copying DLLs. For NumPy, SciPy,
Tkinter, etc.

These need special treatment to be able to run on other systems.
Manually copying them is not enough and will give strange errors.
Sometimes newer version of packages, esp. NumPy can be unsupported. In
this case, you will have to raise an issue, and use the older one.

If you want to manually add a DLL or an EXE because it is your project
only, you will have to use user Yaml files describing where they can be
found. This is described in detail with examples in the `Nuitka Package
Configuration <https://nuitka.net/doc/nuitka-package-config.html>`__
page.

Dependency creep in standalone
==============================

Some packages are a single import, but to Nuitka mean that more than a
thousand packages (literally) are to be included. The prime example of
Pandas, which does want to plug and use just about everything you can
imagine. Multiple frameworks for syntax highlighting everything
imaginable take time.

Nuitka will have to learn effective caching to deal with this in the
future. Presently, you will have to deal with huge compilation times for
these.

A major weapon in fighting dependency creep should be applied, namely
the ``anti-bloat`` plugin, which offers interesting abilities, that can
be put to use and block unneeded imports, giving an error for where they
occur. Use it e.g. like this ``--noinclude-pytest-mode=nofollow
--noinclude-setuptools-mode=nofollow`` and e.g. also
``--noinclude-custom-mode=setuptools:error`` to get the compiler to
error out for a specific package. Make sure to check its help output. It
can take for each module of your choice, e.g. forcing also that e.g.
``PyQt5`` is considered uninstalled for standalone mode.

It's also driven by a configuration file, ``anti-bloat.yml`` that you
can contribute to, removing typical bloat from packages. Please don't
hesitate to enhance it and make PRs towards Nuitka with it.

Standalone: Finding files
=========================

The standard code that normally works, also works, you should refer to
``os.path.dirname(__file__)`` or use all the packages like ``pkgutil``,
``pkg_resources``, ``importlib.resources`` to locate data files near the
standalone binary.

.. important::

   What you should **not** do, is use the current directory
   ``os.getcwd``, or assume that this is the script directory, e.g. with
   paths like ``data/``.

   If you did that, it was never good code. Links, to a program,
   launching from another directory, etc. will all fail in bad ways. Do
   not make assumptions about the directory your program is started
   from.

In case you mean to refer to the location of the ``.dist`` folder for
files that are to reside near the binary, there is
``__compiled__.containing_dir`` that also abstracts all differences with
``--macos-create-app-bundle`` and the ``.app`` folder a having more
nested structure.

.. code:: python

   # This will find a file *near* your app or dist folder
   try:
      open(os.path.join(__compiled__.containing_dir, "user-provided-file.txt"))
   except NameError:
      open(os.path.join(os.path.dirname(sys.argv[0]), "user-provided-file.txt"))

.. _onefile-finding-files:

Onefile: Finding files
======================

There is a difference between ``sys.argv[0]`` and ``__file__`` of the
main module for the onefile mode, that is caused by using a bootstrap to
a temporary location. The first one will be the original executable
path, whereas the second one will be the temporary or permanent path the
bootstrap executable unpacks to. Data files will be in the later
location, your original environment files will be in the former
location.

Given 2 files, one which you expect to be near your executable, and one
which you expect to be inside the onefile binary, access them like this.

.. code:: python

   # This will find a file *near* your onefile.exe
   open(os.path.join(os.path.dirname(sys.argv[0]), "user-provided-file.txt"))
   # This will find a file *inside* your onefile.exe
   open(os.path.join(os.path.dirname(__file__), "user-provided-file.txt"))

   # This will find a file *near* your onefile binary and work for standalone too
   try:
      open(os.path.join(__compiled__.containing_dir, "user-provided-file.txt"))
   except NameError:
      open(os.path.join(os.path.dirname(sys.argv[0]), "user-provided-file.txt"))

Windows Programs without console give no errors
===============================================

For debugging purposes, remove ``--disable-console`` or use the options
``--force-stdout-spec`` and ``--force-stderr-spec`` with paths as
documented for ``--onefile-tempdir-spec`` above. These can be relative
to the program or absolute, so you can see the outputs given.

Deep copying uncompiled functions
=================================

Sometimes people use this kind of code, which for packages on PyPI, we
deal with by doing source code patches on the fly. If this is in your
own code, here is what you can do:

.. code:: python

   def binder(func, name):
      result = types.FunctionType(func.__code__, func.__globals__, name=func.__name__, argdefs=func.__defaults__, closure=func.__closure__)
      result = functools.update_wrapper(result, func)
      result.__kwdefaults__ = func.__kwdefaults__
      result.__name__ = name
      return result

Compiled functions cannot be used to create uncompiled ones from, so the
above code will not work. However, there is a dedicated ``clone``
method, that is specific to them, so use this instead.

.. code:: python

   def binder(func, name):
      try:
         result = func.clone()
      except AttributeError:
         result = types.FunctionType(func.__code__, func.__globals__, name=func.__name__, argdefs=func.__defaults__, closure=func.__closure__)
         result = functools.update_wrapper(result, func)
         result.__kwdefaults__ = func.__kwdefaults__

      result.__name__ = name
      return result

Modules: Extension modules are not executable directly
======================================================

A package can be compiled with Nuitka, no problem, but when it comes to
executing it, ``python -m compiled_module`` is not going to work and
give the error ``No code object available for AssertsTest`` because the
compiled module is not source code, and Python will not just load it.
The closest would be ``python -c "import compile_module"`` and you might
have to call the main function yourself.

To support this, the CPython ``runpy`` and/or ``ExtensionFileLoader``
would need improving such that Nuitka could supply its compiled module
object for Python to use.

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
reports from different setups, e.g. with updated packages, and see the
changes to Nuitka. The report is, however, recommended for your bug
reporting.

Also, another form is available, where the report is free form and
according to a Jinja2 template of yours, and one that is included in
Nuitka. The same information as used to produce the XML file is
accessible. However, right now, this is not yet documented, but we plan
to add a table with the data. For a reader of the source code that is
familiar with Jinja2, however, it will be easy to do it now already.

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

The code objects are empty for native compiled functions. There is no
bytecode with Nuitka's compiled function objects, so there is no way to
provide it.

PDB
===

There is no tracing of compiled functions to attach a debugger to.

.. include:: ../variables.inc
