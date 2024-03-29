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

Other Operating systems will work as well. The portability is expected
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
platform compilation with Nuitka.

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
Importantly, you can execute Nuitka seamlessly without having to
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

Console Window
==============

On Windows, the console is opened by programs by default. You can change
it anytime. Nuitka follows this default behavior, making it primarily
suitable for terminal-based programs or those where output visibility is
essential. There is a difference between **pythonw.exe** and
**python.exe** along those lines. This is replicated in **Nuitka** with
the option ``--disable-console``.

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
good idea to have splash screens. Luckily, with Nuitka, they are easy to
add for **Windows**.

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

By default, Nuitka compiles without ``--deployment`` which leaves a set
of safe guards and helpers on, that are aimed at debugging wrong uses of
Nuitka.

This is a new feature, and implements a bunch of protections and
helpers, that are documented here.

Fork bombs (self-execution)
---------------------------

So after compilation, ``sys.executable`` is the compiled binary. In case
of packages like ``multiprocessing``, ``joblib``, or ``loky`` what these
typically do is to expect to run from a full ``python`` with
``sys.executable`` and then to be able to use its options like ``-c
command`` or ``-m module_name`` and then be able to launch other code
temporarily or permanently as a service daemon.

With Nuitka however, this executes your program again, and puts these
arguments, in ``sys.argv`` where you maybe ignore them, and then you
fork yourself again to launch the helper daemons. Sometimes this ends up
spawning CPU count processes that spawn CPU count processes that... this
is called a fork bomb, and with almost all systems, that freezes them
easily to death.

That is why e.g. this happens with default Nuitka:

.. code::

   ./hello.dist/hello.bin -l fooL -m fooM -n fooN -o fooO -p
   Error, the program tried to call itself with '-m' argument. Disable with '--no-deployment-flag=self-execution'.

Your program may well have its own command line parsing, and not use an
unsupported package that does attempt to re-execute. In this case, you
need at *compile time* to use ``--no-deployment-flag=self-execution``
which disables this specific guard.

Misleading Messages
-------------------

Some packages output what they think is helpful information about what
the reason of a failed import might mean. With compiled programs there
are very often just plain wrong. We try and repair those in
non-deployment mode. Here is an example, where we change a message that
asks to pip install (which is not the issue) to point the user to the
include command that makes an ``imageio`` plugin work.

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
re-enable it. You might want to use Nuitka Project options and an
environment variable to make this conditional.

Should you disable them all?

We believe, disabling should only happen selectively, but with PyPI
upgrades, your code changes, all of these issues can sneak back in. The
space saving of deployment mode is currently negligible, so attempt to
not do it, but review what exists, and if you know that it cannot affect
you, or if it does, you will not need it. Some of the future ones, will
clearly be geared at beginner level usage.

Windows Virus scanners
======================

Binaries compiled on Windows with default settings of Nuitka and no
further actions taken might be recognized by some AV vendors as malware.
This is avoidable, but only in Nuitka commercial there is actual support
and instructions for how to do it, seeing this as a typical commercial
only need. https://nuitka.net/doc/commercial.html

Linux Standalone
================

For Linux standalone it is pretty difficult to build a binary that works
on other Linux versions. This is mainly because on Linux, much software
is built specifically targeted to concrete DLLs. Things like glibc used,
are then encoded into the binary built, and it will not run with an
older glibc, just to give one critical example.

The solution is to build on the oldest OS that you want to see
supported. Picking that and setting it up can be tedious, so can be
login, and keeping it secure, as it's something you put your source code
on.

To aid that, Nuitka commercial has container based builds, that you can
use. This uses dedicated optimized Python builds, targets CentOS 7 and
supports even newest Pythons and very old OSes that way using recent C
compiler chains all turn key solution. The effort needs to be
compensated to support Nuitka development for Linux, there you need to
purchase it https://nuitka.net/doc/commercial.html but even a sponsor
license will be cheaper than doing it yourself.

Program crashes system (fork bombs)
===================================

A fork bomb is a program that starts itself over and over. This can
easily happen, since ``sys.executable`` for compiled programs is not a
Python interpreter, and packages that try to do multiprocessing in a
better way, often relaunch themselves through this, and Nuitka needs and
does have handling for these with known packages. However, you may
encounter a situation where the detection of this fails. See deployment
option above that is needed to disable this protection.

When this fork bomb happens easily all memory, all CPU of the system
that is available to the user is being used, and even the most powerful
build system will go down in flames sometimes needing a hard reboot.

For fork bombs, we can use ``--experimental=debug-self-forking`` and see
what it does, and we have a trick, that prevents fork bombs from having
any actual success in their bombing. Put this at the start of your
program.

.. code:: python

   import os, sys

   if "NUITKA_LAUNCH_TOKEN" not in os.environ:
      sys.exit("Error, need launch token or else fork bomb suspected.")
   else:
      del os.environ["NUITKA_LAUNCH_TOKEN"]

Actually Nuitka is trying to get ahold of them without the deployment
option already, finding "-c" and "-m" options, but it may not be perfect
or not work well with a package (anymore).

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

******
 Tips
******

Nuitka Options in the code
==========================

One clean way of providing options to Nuitka, that you will always use
for your program, is to put them into the main file you compile. There
is even support for conditional options, and options using pre-defined
variables, this is an example:

.. code:: python

   # Compilation mode, support OS-specific options
   # nuitka-project-if: {OS} in ("Windows", "Linux", "Darwin", "FreeBSD"):
   #    nuitka-project: --onefile
   # nuitka-project-else:
   #    nuitka-project: --standalone

   # The PySide2 plugin covers qt-plugins
   # nuitka-project: --enable-plugin=pyside2
   # nuitka-project: --include-qt-plugins=qml

The comments must be at the start of lines, and indentation inside of
them is to be used, to end a conditional block, much like in Python.
There are currently no other keywords than the used ones demonstrated
above.

You can put arbitrary Python expressions there, and if you wanted to
e.g. access a version information of a package, you could simply use
``__import__("module_name").__version__`` if that would be required to
e.g. enable or disable certain Nuitka settings. The only thing Nuitka
does that makes this not Python expressions, is expanding ``{variable}``
for a pre-defined set of variables:

Table with supported variables:

+------------------+--------------------------------+------------------------------------------+
| Variable         | What this Expands to           | Example                                  |
+==================+================================+==========================================+
| {OS}             | Name of the OS used            | Linux, Windows, Darwin, FreeBSD, OpenBSD |
+------------------+--------------------------------+------------------------------------------+
| {Version}        | Version of Nuitka              | e.g. (1, 6, 0)                           |
+------------------+--------------------------------+------------------------------------------+
| {Commercial}     | Version of Nuitka Commercial   | e.g. (2, 1, 0)                           |
+------------------+--------------------------------+------------------------------------------+
| {Arch}           | Architecture used              | x86_64, arm64, etc.                      |
+------------------+--------------------------------+------------------------------------------+
| {MAIN_DIRECTORY} | Directory of the compiled file | some_dir/maybe_relative                  |
+------------------+--------------------------------+------------------------------------------+
| {Flavor}         | Variant of Python              | e.g. Debian Python, Anaconda Python      |
+------------------+--------------------------------+------------------------------------------+

The use of ``{MAIN_DIRECTORY}`` is recommended when you want to specify
a filename relative to the main script, e.g. for use in data file
options or user package configuration yaml files,

.. code:: python

   # nuitka-project: --include-data-files={MAIN_DIRECTORY}/my_icon.png=my_icon.png
   # nuitka-project: --user-package-configuration-file={MAIN_DIRECTORY}/user.nuitka-package.config.yml

Python command line flags
=========================

For passing things like ``-O`` or ``-S`` to Python, to your compiled
program, there is a command line option name ``--python-flag=`` which
makes Nuitka emulate these options.

The most important ones are supported, more can certainly be added.

Caching compilation results
===========================

The C compiler, when invoked with the same input files, will take a long
time and much CPU to compile over and over. Make sure you are having
``ccache`` installed and configured when using gcc (even on Windows). It
will make repeated compilations much faster, even if things are not yet
not perfect, i.e. changes to the program can cause many C files to
change, requiring a new compilation instead of using the cached result.

On Windows, with gcc Nuitka supports using ``ccache.exe`` which it will
offer to download from an official source and it automatically. This is
the recommended way of using it on Windows, as other versions can e.g.
hang.

Nuitka will pick up ``ccache`` if it's found in system ``PATH``, and it
will also be possible to provide if by setting ``NUITKA_CCACHE_BINARY``
to the full path of the binary, this is for use in CI systems where
things might be non-standard.

For the MSVC compilers and ClangCL setups, using the ``clcache`` is
automatic and included in Nuitka.

On macOS and Intel, there is an automatic download of a ``ccache``
binary from our site, for arm64 arches, it's recommended to use this
setup, which installs Homebrew and ccache in there. Nuitka picks that
one up automatically if it on that kind of machine. You need and should
not use Homebrew with Nuitka otherwise, it's not the best for standalone
deployments, but we can take ``ccache`` from there.

.. code:: bash

   export HOMEBREW_INSTALL_FROM_API=1
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
   eval $(/opt/homebrew/bin/brew shellenv)
   brew install ccache

Control where Caches live
=========================

The storage for cache results of all kinds, downloads, cached
compilation results from C and Nuitka, is done in a platform dependent
directory as determined by the ``appdirs`` package. However, you can
override it with setting the environment variable ``NUITKA_CACHE_DIR``
to a base directory. This is for use in environments where the home
directory is not persisted, but other paths are.

There is also per cache control of these caches, here is a table of
environment variables that you can set before starting the compilation,
to make Nuitka store some of these caches in an entirely separate space.

+------------------+-----------------------------------+----------------------------------------+
| Cache name       | Environment Variable              | Data Put there                         |
+==================+===================================+========================================+
| downloads        | NUITKA_CACHE_DIR_DOWNLOADS        | Downloads made, e.g. dependency walker |
+------------------+-----------------------------------+----------------------------------------+
| ccache           | NUITKA_CACHE_DIR_CCACHE           | Object files created by gcc            |
+------------------+-----------------------------------+----------------------------------------+
| clcache          | NUITKA_CACHE_DIR_CLCACHE          | Object files created by MSVC           |
+------------------+-----------------------------------+----------------------------------------+
| bytecode         | NUITKA_CACHE_DIR_BYTECODE         | Bytecode of demoted modules            |
+------------------+-----------------------------------+----------------------------------------+
| dll-dependencies | NUITKA_CACHE_DIR_DLL_DEPENDENCIES | DLL dependencies                       |
+------------------+-----------------------------------+----------------------------------------+

Runners
=======

Avoid running the ``nuitka`` binary, doing ``python -m nuitka`` will
make a 100% sure you are using what you think you are. Using the wrong
Python will make it give you ``SyntaxError`` for good code or
``ImportError`` for installed modules. That is happening, when you run
Nuitka with Python2 on Python3 code and vice versa. By explicitly
calling the same Python interpreter binary, you avoid that issue
entirely.

Fastest C Compilers
===================

The fastest binaries of ``pystone.exe`` on Windows with 64 bits Python
proved to be significantly faster with MinGW64, roughly 20% better
score. So it is recommended for use over MSVC. Using ``clang-cl.exe`` of
Clang7 was faster than MSVC, but still significantly slower than
MinGW64, and it will be harder to use, so it is not recommended.

On Linux, for ``pystone.bin``, the binary produced by ``clang6`` was
faster than ``gcc-6.3``, but not by a significant margin. Since gcc is
more often already installed, that is recommended to use for now.

Differences in C compilation times have not yet been examined.

Unexpected Slowdowns
====================

Using the Python DLL, like standard CPython does, can lead to unexpected
slowdowns, e.g. in uncompiled code that works with Unicode strings. This
is because calling to the DLL rather than residing in the DLL causes
overhead, and this even happens to the DLL with itself, being slower,
than a Python all contained in one binary.

So if feasible, aim at static linking, which is currently only possible
with Anaconda Python on non-Windows, Debian Python2, self compiled
Pythons (do not activate ``--enable-shared``, not needed), and installs
created with ``pyenv``.

.. note::

   On Anaconda, you may need to execute ``conda install
   libpython-static``

Standalone executables and dependencies
=======================================

The process of making standalone executables for Windows traditionally
involves using an external dependency walker to copy necessary libraries
along with the compiled executables to the distribution folder.

There are plenty of ways to find that something is missing. Do not
manually copy things into the folder, esp. not DLLs, as that's not going
to work. Instead, make bug reports to get these handled by Nuitka
properly.

Windows errors with resources
=============================

On Windows, the Windows Defender tool and the Windows Indexing Service
both scan the freshly created binaries, while Nuitka wants to work with
it, e.g. adding more resources, and then preventing operations randomly
due to holding locks. Make sure to exclude your compilation stage from
these services.

Windows standalone program redistribution
=========================================

Whether compiling with MingW or MSVC, the standalone programs have
external dependencies to Visual C Runtime libraries. Nuitka tries to
ship those dependent DLLs by copying them from your system.

Beginning with Microsoft Windows 10, Microsoft ships ``ucrt.dll``
(Universal C Runtime libraries) which handles calls to
``api-ms-crt-*.dll``.

With earlier Windows platforms (and wine/ReactOS), you should consider
installing Visual C runtime libraries before executing a Nuitka
standalone compiled program.

Depending on the used C compiler, you'll need the following redist
versions on the target machines. However, notice that compilation using
the 14.3 based version is always recommended, working and best
supported, unless you want to target Windows 7.

+------------------+-------------+----------+
| Visual C version | Redist Year | CPython  |
+==================+=============+==========+
| 14.3             | 2022        | 3.11     |
+------------------+-------------+----------+
| 14.2             | 2019        | 3.5-3.10 |
+------------------+-------------+----------+
| 14.1             | 2017        | 3.5-3.8  |
+------------------+-------------+----------+
| 14.0             | 2015        | 3.5-3.8  |
+------------------+-------------+----------+
| 10.0             | 2010        | 3.4      |
+------------------+-------------+----------+
| 9.0              | 2008        | 2.6, 2.7 |
+------------------+-------------+----------+

When using MingGW64 as downloaded by Nuitka, you'll need the following
redist versions:

+----------------------------+-------------+---------------------+
| MingGW64 version           | Redist Year | CPython             |
+============================+=============+=====================+
| WinLibs automatic download | 2015        | 2.6, 2.7, 3.4- 3.11 |
+----------------------------+-------------+---------------------+

Once the corresponding runtime libraries are installed on the target
system, you may remove all ``api-ms-crt-*.dll`` files from your Nuitka
compiled dist folder.

Detecting Nuitka at run time
============================

Nuitka does *not* ``sys.frozen`` unlike other tools because it usually
triggers inferior code for no reason. For Nuitka, we have the module
attribute ``__compiled__`` to test if a specific module was compiled,
and the function attribute ``__compiled__`` to test if a specific
function was compiled.

Providing extra Options to Nuitka C compilation
===============================================

Nuitka will apply values from the environment variables ``CCFLAGS``,
``LDFLAGS`` during the compilation on top of what it determines to be
necessary. Beware, of course, that is this is only useful if you know
what you are doing, so should this pose issues, raise them only with
perfect information.

Producing a 32 bit binary on a 64 bit Windows system
====================================================

Nuitka will automatically target the architecture of the Python you are
using. If this is 64 bit, it will create a 64 bit binary, if it is 32
bit, it will create a 32 bit binary. You have the option to select the
bits when you download the Python. In the output of ``python -m nuitka
--version`` there is a line for the architecture. It's ``Arch: x86_64``
for 64 bits, and just ``Arch: x86`` for 32 bits.

The C compiler will be picked to match that more or less automatically.
If you specify it explicitly, and it mismatches, you will get a warning
about the mismatch and informed that your compiler choice was rejected.

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
