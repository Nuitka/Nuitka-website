:orphan:

################################
 Solutions to the Common Issues
################################

This page is the recommended read if you find **Nuitka** is not working
out of the box for you. There are typical issues encountered and their
solutions.

This page can also teach you more about **Nuitka** advanced concepts and
is a recommended read for all levels of **Nuitka** users.

.. contents:: Table of Contents
   :depth: 1
   :local:
   :class: page-toc

*****************
 Deployment Mode
*****************

The non-deployment mode of **Nuitka** intends to assist you at the
runtime of the compiled program. It aims to give you better error
information and to catch typical user errors.

By default, **Nuitka** is set to compile in non-deployment mode, which
can be deactivated using the ``--deployment`` option. In this mode,
Nuitka activates a range of safety guards and helpers to identify and
resolve any incorrect usage of **Nuitka**.

If you want to disable all these helpers, read more in the `Disabling
All`_ section. Following is the list of currently implemented helpers
you can also deactivate individually by name, and you might have to.

Fork Bombs (Self-execution)
===========================

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
===================

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
=============

The deployment mode is relatively new and has constantly more features
added, for example, something for ``FileNotFoundError`` should be coming
soon.

Disabling All
=============

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

************************
 Windows Virus Scanners
************************

If you compile binaries using **Nuitka's** default settings on
**Windows** without additional steps, some antivirus vendors may flag
them as malware. You can avoid this by purchasing the `Nuitka Commercial
<https://nuitka.net/doc/commercial.html>`_ plan. In this case, you will
get instructions and support on that matter.

******************
 Linux Standalone
******************

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

*************************************
 Program Crashes System (Fork Bombs)
*************************************

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

   if "NUITKA_LAUNCH_TOKEN" in os.environ:
      sys.exit("Error, launch token must not be present or else fork bomb suspected.")
   os.environ["NUITKA_LAUNCH_TOKEN"] = "1"

This code checks for the presence of the environment variable
``NUITKA_LAUNCH_TOKEN`` and if found, the program exits with an error
message. Otherwise, it sets the ``NUITKA_LAUNCH_TOKEN`` in the
environment, so afterwards, the potential fork bomb can be discovered.

**Nuitka** tries to handle fork bombs without the deployment option,
finding ``-c`` and ``-m`` options. However, the detection may not be
perfect or not work well with a package (anymore).

*********************************
 Memory issues and compiler bugs
*********************************

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
=============================

There is a dedicated option ``--low-memory`` which influences decisions
of Nuitka, such that it avoids high usage of memory during compilation
at the cost of increased compile time.

Avoid 32 bit C compiler/assembler memory limits
===============================================

Do not use a 32 bit compiler, but a 64 bit one. If you are using Python
with 32 bits on Windows, you most definitely ought to use MSVC as the C
compiler, and not MinGW64. The MSVC is a cross-compiler, and can use
more memory than gcc on that platform. If you are not on Windows, that
is not an option, of course. Also, using the 64 bit Python will work.

Use a minimal virtualenv
========================

When you compile from a living installation, that may well have many
optional dependencies of your software installed. Some software will
then have imports on these, and Nuitka will compile them as well. Not
only may these be just the troublemakers, they also require more memory,
so get rid of that. Of course, you do have to check that your program
has all the needed dependencies before you attempt to compile, or else
the compiled program will equally not run.

Use LTO compilation or not
==========================

With ``--lto=yes`` or ``--lto=no`` you can switch the C compilation to
only produce bytecode, and not assembler code and machine code directly,
but make a whole program optimization at the end. This will change the
memory usage pretty dramatically, and if your error is coming from the
assembler, using LTO will most definitely avoid that.

Switch the C compiler to clang
==============================

People have reported that programs that fail to compile with gcc due to
its bugs or memory usage work fine with clang on Linux. On Windows, this
could still be an option, but it needs to be implemented first for the
automatic downloaded gcc, that would contain it. Since MSVC is known to
be more memory effective anyway, you should go there, and if you want to
use Clang, there is support for the one contained in MSVC.

Add a larger swap file to your embedded Linux
=============================================

On systems with not enough RAM, you need to use swap space. Running out
of it is possibly a cause, and adding more swap space, or one at all,
might solve the issue, but beware that it will make things extremely
slow when the compilers swap back and forth, so consider the next tip
first or on top of it.

Limit the amount of compilation jobs
====================================

With the ``--jobs`` option of Nuitka, it will not start many C compiler
instances at once, each competing for the scarce resource of RAM. By
picking a value of one, only one C compiler instance will be running,
and on an 8 core system, that reduces the amount of memory by factor 8,
so that's a natural choice right there.

**********************
 Dynamic ``sys.path``
**********************

If your script modifies ``sys.path``, for example inserts directories
with source code relative to it, Nuitka will not be able to see those.
However, if you set the ``PYTHONPATH`` to the resulting value, it will
be able to compile it and find the used modules from these paths as
well.

****************************
 Manual Python File Loading
****************************

A very frequent pattern with private code is that it scans plugin
directories of some kind, and for example uses ``os.listdir``, then
considers Python filenames, and then opens a file and does ``exec`` on
them. This approach works for Python code, but for compiled code, you
should use this much cleaner approach, that works for pure Python code
and is a lot less vulnerable.

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

**********************************
 Missing data files in standalone
**********************************

If your program fails to find data file, it can cause all kinds of
different behavior, for example a package might complain it is not the
right version because a ``VERSION`` file check defaulted to an unknown.
The absence of icon files or help texts, may raise strange errors.

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

*********************************
 Missing DLLs/EXEs in standalone
*********************************

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

********************************
 Dependency creep in standalone
********************************

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
occur. Use it for example like this ``--noinclude-pytest-mode=nofollow
--noinclude-setuptools-mode=nofollow`` and for example also
``--noinclude-custom-mode=setuptools:error`` to get the compiler to
error out for a specific package. Make sure to check its help output. It
can take for each module of your choice, for example forcing also that
for example ``PyQt5`` is considered uninstalled for standalone mode.

It's also driven by a configuration file, ``anti-bloat.yml`` that you
can contribute to, removing typical bloat from packages. Please don't
hesitate to enhance it and make PRs towards Nuitka with it.

***************************
 Standalone: Finding files
***************************

The standard code that normally works, also works, you should refer to
``os.path.dirname(__file__)`` or use all the packages like ``pkgutil``,
``pkg_resources``, ``importlib.resources`` to locate data files near the
standalone binary.

.. important::

   What you should **not** do, is use the current directory
   ``os.getcwd``, or assume that this is the script directory, for
   example with paths like ``data/``.

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

************************
 Onefile: Finding files
************************

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

*************************************************
 Windows Programs without console give no errors
*************************************************

For debugging purposes, remove ``--disable-console`` or use the options
``--force-stdout-spec`` and ``--force-stderr-spec`` with paths as
documented for ``--onefile-tempdir-spec`` above. These can be relative
to the program or absolute, so you can see the outputs given.

***********************************
 Deep copying uncompiled functions
***********************************

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

********************************************************
 Modules: Extension modules are not executable directly
********************************************************

A package can be compiled with Nuitka, no problem, but when it comes to
executing it, ``python -m compiled_module`` is not going to work and
give the error ``No code object available for AssertsTest`` because the
compiled module is not source code, and Python will not just load it.
The closest would be ``python -c "import compile_module"`` and you might
have to call the main function yourself.

To support this, the CPython ``runpy`` and/or ``ExtensionFileLoader``
would need improving such that Nuitka could supply its compiled module
object for Python to use.
