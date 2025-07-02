:orphan:

################################
 Solutions to the Common Issues
################################

We recommend this page if you find **Nuitka** is not working out of the
box for you. There are typical issues encountered and their solutions.

This page can also teach you more about **Nuitka** advanced concepts;
therefore, we recommend reading it for all levels of **Nuitka** users.
It helps a lot to avoid issues and avoid non-optimal results.

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

.. _fork-bombs:

Fork Bombs (Self-execution)
===========================

So after compilation, ``sys.executable`` is the compiled binary. Certain
Python packages like ``multiprocessing``, ``joblib``, or ``loky``
typically expect to run from a full ``Python`` environment with
``sys.executable``. They expect to use the ``-c command`` or ``-m
module_name`` options to be able to launch other code temporarily or
permanently as a service daemon.

However, with **Nuitka**, this executes your program again and puts
these arguments in ``sys.argv`` where you maybe ignore them, and then
you fork yourself again to launch the helper daemons. That leads to
unintentionally repeated forking, potentially resulting in a scenario
called **fork bomb**, where multiple processes spawn recursively,
causing system freeze.

For example, running a program compiled with **Nuitka** may trigger the
following error:

.. code::

   ./hello.dist/hello.bin -l fooL -m fooM -n fooN -o fooO -p
   Error, the program tried to call itself with '-m' argument. Disable with '--no-deployment-flag=self-execution'.

To avoid this issue, ensure your program handles command line parsing
correctly and avoids using unsupported packages that attempt
re-execution. Additionally, you can turn off this specific behavior at
compile time by using the ``--no-deployment-flag=self-execution`` flag.

Misleading Messages
===================

Some Python packages generate misleading error messages when they
encounter import failures. These messages sometimes suggest actions that
may not be the appropriate solution for compiled programs. **Nuitka**
tries to correct them in non-deployment mode. Here is an example where
**Nuitka** changes a message that asks to ``pip install ...`` a package.
That, of course, is not the issue, and instead, **Nuitka** makes the
program point the user to the ``--include-module`` option to use. With
that, the ``imageio`` plugin will work.

.. code:: yaml

   - module-name: 'imageio.core.imopen'
     anti-bloat:
       - replacements_plain:
           '`pip install imageio[{config.install_name}]` to install it': '`--include-module={config.module_name}` with Nuitka to include it'
           'err_type = ImportError': 'err_type = RuntimeError'
         when: 'not deployment'

And much more
=============

The non-deployment mode of **Nuitka** is constantly evolving and adding
more features, for example, something for ``FileNotFoundError`` should
be added; there are plenty of ideas.

Disabling All
=============

Of course, all these helpers are removed at once when using the
``--deployment`` option of **Nuitka**, but remember that you may want to
re-enable it for debugging. To make this easy to toggle, you should use
:ref:`Nuitka Project Options <nuitka-project-options>` and check an
environment variable in them.

.. code:: python

   # nuitka-project-if: os.getenv("DEPLOYMENT") == "yes":
   #  nuitka-project: --deployment

Why should you not disable them all during development?

We recommend selective disabling, as with **PyPI** upgrades and your
code changes, these issues can resurface. The space saved by deployment
mode is minimal, so we advise not to disable them. Instead, review each
feature, and if you know, it won't affect your software or you won't
need it, turn it off.

************************
 Windows Virus Scanners
************************

Some Antivirus Vendors may flag compile binaries using **Nuitka's**
default settings on **Windows** as malware. That happens a lot if you
compile without additional steps. You can avoid this by purchasing the
:doc:`Nuitka Commercial </doc/commercial>` plan and following the
instructions given. You can solve it with those instructions and
support, but there are no guarantees.

******************
 Linux Standalone
******************

For **Linux** standalone, building a binary that works on older
**Linux** versions is challenging. Because on **Linux**, distributors
build **Python** software to link against the concrete system explicitly
**DLLs**. As a consequence, it often does not run on other Linux
flavors.

The solution is to compile your application on the oldest **Linux**
version that you intend to support. However, this process can be
exhausting, involving setup complexities and security considerations
since it exposes source code.

We recommend purchasing :doc:`Nuitka Commercial </doc/commercial>` plan
to overcome this issue without extra effort. **Nuitka Commercial** has
container-based builds that you can use. This container uses dedicated
optimized Python builds, targeting **CentOS 7** and supporting even the
newest Pythons and old operating systems. This solution streamlines the
process by integrating recent C compiler chains.

*************************************
 Program Crashes System (Fork Bombs)
*************************************

A fork bomb is a program that spawns recursively, causing a system lock
and ultimately crashing it in short order. That happens since
``sys.executable`` for a compiled program is not the Python interpreter
it usually is, and packages that try to do multiprocessing in a better
way relaunch themselves. That starts the process all over again unless
taken care of.

**Nuitka** handles it for all packages known to do that; for example,
``joblib``. However, you may encounter a situation where the detection
of this fails. To turn off this protection, read about the
:ref:`fork-bombs` option.

To debug fork bombs, use the ``--experimental=debug-self-forking``
option to check program fork behavior. To minimize risks associated with
fork bombs, put the following code snippet at the very beginning of your
program.

.. code:: python

   import os, sys

   if "NUITKA_LAUNCH_TOKEN" in os.environ:
      sys.exit("Error, launch token must not be present or else fork bomb suspected.")
   os.environ["NUITKA_LAUNCH_TOKEN"] = "1"

This code checks for the presence of the environment variable
``NUITKA_LAUNCH_TOKEN`` and the program reacts with an error exit.
Otherwise, it sets the ``NUITKA_LAUNCH_TOKEN`` in the environment, so
afterward, the potential fork bomb is detected, should the program
re-execute itself.

**Nuitka** handles fork bombs without the deployment option if it finds
``-c`` and ``-m`` options, as typically used with the Python interpreter
to execute code. However, the detection may need improvement to work
well, with a new package (or a previously working package in a newer
version).

*********************************
 Memory issues and compiler bugs
*********************************

Sometimes, the C compilers will crash with unspecific errors. It may be
saying they cannot allocate memory, that some assembly input was
truncated, or other similar error messages. All of these can be caused
by using more memory than is available.

These are example error messages that are a sure sign of memory being
too low; there is no end to them.

.. code::

   # gcc
   fatal error: error writing to -: Invalid argument
   Killed signal terminated program
   {standard input}: Assembler messages:
   {standard input}: Warning: end of file not at end of a line; newline inserted
   # MSVC
   fatal error C1002: compiler is out of heap space in pass 2
   fatal error C1001: Internal compiler error

There are several approaches you can explore here.

Ask Nuitka to use less memory
=============================

There is a dedicated option ``--low-memory`` which influences decisions
of **Nuitka**, such that it avoids high usage of memory during
compilation at the cost of increased compile time.

Avoid 32-bit C compiler/assembler memory limits
===============================================

Do not use a 32-bit compiler, but a 64-bit one. If you use Python with
32 bits on **Windows**, you should use **MSVC** as the C compiler, not
MinGW64. The **MSVC** is a cross-compiler and can use more memory than
**MinGW64** on that platform. Also, using the 64-bit Python will work.

Use a minimal virtualenv
========================

When you compile from an installation used for many packages and
programs, you may have many optional dependencies of your software
installed. Some software will then have imports on these, and **Nuitka**
will compile them as well. Not only may these be just the troublemakers,
but they also require more memory, so get rid of that. Of course, you do
have to check that your program has all the needed dependencies before
you attempt to compile, or else the compiled program will equally not
run.

Use LTO compilation or not
==========================

Link time optimization (**LTO**) is a technique modern compilers allow
for. With ``--lto=yes`` or ``--lto=no``, you can switch the C
compilation to only produce bytecode, and not assembler code and machine
code directly, but make a whole program optimization at the end.

Using **LTO** will change memory usage dramatically, and if your error
is coming from the assembler, using LTO will most likely avoid that. On
the other hand, **LTO** does much more work during linking and can
itself be the cause of the memory shortage.

There is no clear answer to whether ** LTO ** or not is better for
memory usage, but you can attempt switching.

Switch the C compiler to Clang
==============================

Some **Nuitka** users have reported that programs that fail to compile
with **GCC** due to its bugs or memory usage work fine with **Clang** on
Linux. On **Windows**, since **MSVC** is known to be more memory
effective, you should go there first. But adding the option ``--clang``
to your compilation may help you.

Add a larger swap file to your embedded **Linux**
=================================================

On systems with not enough RAM, you need to use swap space. Running out
of it is possibly a cause, and adding more swap space, or one at all,
might solve the issue, but beware that it will make things extremely
slow when the compilers swap back and forth, so consider the following
tip first or on top of it.

Refer to your systems instructions on how to add swap space to a
**Linux** installation.

Limit the number of compilation jobs
====================================

With the ``--jobs`` option of **Nuitka**, it will not start many C
compiler instances at once, each competing for the scarce resource of
RAM. For example, picking a value of ``1`` on an eight-core system
reduces the amount of memory by a factor up to 8.

.. note::

   The ``--low-memory`` option implies ``--jobs=1`` already.

*********************************
 Dynamic ``sys.path`` at runtime
*********************************

If your program (or some used modules) modify ``sys.path`` at runtime,
for example, inserting directories with source code relative to it,
**Nuitka** will not be able to see those. However, if you set the
``PYTHONPATH`` to the resulting value, **Nuitka** will be able to locate
the modules used from there as well.

****************************
 Manual Python File Loading
****************************

A widespread pattern with private code is that it scans plugin
directories of some kind, and for example, uses ``os.listdir``, then
considers Python filenames, and then opens a file and does ``exec`` on
them.

This approach only works for Python source code but for compiled code,
you should use this much cleaner approach that works for pure Python
code and is a lot less vulnerable.

.. code:: python

   # Using a package name to locate the plugins. Also, a good approach
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

If your program fails to find a data file, it can cause different
problematic behavior; for example, a package might complain that it is
not the correct version because a ``VERSION`` read from the file usually
was not found, and instead, it uses a default value. The absence of
files containing, for example, icons may cause visual issues only or
databases, or texts missing in a file, which may also raise all kinds of
strange errors.

Often, the error handling code paths for files that are not present are
even buggy and will reveal programming errors like unbound local
variables. Please look carefully at these exceptions, considering this
can be the cause. If your program works fails ``--mode=standalone`` and
works only with ``--follow-imports``, data files are likely the cause.

The most common error indicating file absence is, of course, an uncaught
``FileNotFoundError`` with a filename. You should figure out what the
Python package is that is missing files and then use
``--include-package-data`` (preferably), or
``--include-data-dir``/``--include-data-files`` to include them.

You can read all about data files in :ref:`data-files`; there are much
more detail to learn than is covered here.

*********************************
 Missing DLLs/EXEs in standalone
*********************************

**Nuitka** has plugins and configurations to deal with copying **DLLs**
needed by some packages. It covers **NumPy**, **SciPy**, **Tkinter**,
and practically all popular packages.

The **DLLs** need special treatment to be able to run on other systems,
merely copying them is not working and will give strange errors at
runtime.

Sometimes, newer versions of packages, such as **NumPy**, can be
unsupported. In this situation, you will have to raise an issue so we
can also add support for it.

If you want to manually add a DLL or an EXE because it is your project
only, you must use user Yaml files to describe their location.

The reference for the syntax to use with examples is in the :doc:`Nuitka
Package Configuration </user-documentation/nuitka-package-config>` page.

.. _anti-bloat:

********************************
 Dependency creep in standalone
********************************

Some packages are a single import, but to **Nuitka** means that more
than a thousand packages (literally) are included as its dependency. One
example is **IPython**, which does want to plug and use just about
everything you can imagine. Multiple frameworks for syntax highlighting
everything imaginable take time.

Nuitka will have to learn effective caching to deal with this in the
future. Presently, you will have to deal with substantial compilation
times for these.

A major weapon in fighting dependency creep should be applied, namely
the ``anti-bloat`` plugin, which offers interesting abilities that can
be put to use and block unneeded imports, giving an error for where they
occur. Use it for example like this ``--noinclude-pytest-mode=nofollow
--noinclude-setuptools-mode=nofollow`` and, for example, also
``--noinclude-custom-mode=setuptools:error`` to get the compiler to
error out for a specific package. Make sure to check its help output. It
can take for each module of your choice, for example, forcing also that
for example ``PyQt5`` is considered uninstalled for standalone mode.

A configuration file drives it, ``standard.nuitka-package.config.yml``
that you can contribute to, removing typical bloat from packages. Please
join us in enhancing it and making PRs towards **Nuitka** for more and
more packages to compile without severe bloat.

***************************
 Standalone: Finding files
***************************

The standard code that normally works also works; you should refer to
``os.path.dirname(__file__)`` or use all the packages like ``pkgutil``,
``pkg_resources``, ``importlib.resources`` to locate data files near the
standalone binary.

.. important::

   What you should **not** do is use the current directory
   ``os.getcwd``, or assume that ``.`` is the script directory for
   example with paths like ``data/``.

   If you did that, it was never good code. Links to a program,
   launching it from another directory, or code changing the current
   directory will all cause failures. Do not make assumptions about the
   directory from which your program starts.

.. admonition:: Tip

   Want to catch these errors before compiling?

   Using the terminal, create a sub-directory, move one directory up,
   and then run your program like this ``python ../main.py`` and correct
   all the errors you will encounter compared to ``python main.py``.

   It goes a long way to not having issues after compilation in
   standalone mode to do this, but make sure to refer to
   ``os.path.dirname(__file__)`` for files to be part of your compiled
   program installation, and for files that are to reside next to the
   compiled program use ``os.path.dirname(sys.argv[0])``.

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
main module for the onefile mode, which is caused by using a bootstrap
to a temporary location. The first will be the original executable path,
whereas the second will be the temporary or permanent path the bootstrap
executable unpacks to. Data files will be in the later location; your
original environment files will be in the former location.

Given two files, one which you expect to be near your executable and one
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
 Windows Programs with no console give no errors
*************************************************

For debugging purposes, remove ``--windows-console-mode=disable`` or use
the options ``--force-stdout-spec`` and ``--force-stderr-spec`` with
paths as documented for ``--onefile-tempdir-spec`` above. These can be
program relative, absolute paths, or temp directories.

.. admonition:: Example

   You may, for example, use
   ``--force-stdout-spec={PROGRAM_BASE}.out.txt`` and
   ``--force-stderr-spec={PROGRAM_BASE}.err.txt`` and use :ref:`Nuitka
   Project Options <nuitka-project-options>` to enable them with
   environment variables in your compilation.

   .. code:: python

      # nuitka-project-if: os.getenv("DEBUG") == "yes":
      #  nuitka-project: --force-stdout-spec={PROGRAM_BASE}.out.txt
      #  nuitka-project: --force-stderr-spec={PROGRAM_BASE}.err.txt

Use these options to capture the errors and outputs and check them; they
will contain **Python** tracebacks and, generally, the information you
would use to debug your program.

***********************************
 Deep copying uncompiled functions
***********************************

Sometimes, people use this kind of code, which we deal with for packages
on PyPI by doing source code patches on the fly. If this is in your
code, here is what you can do:

.. code:: python

   def binder(func, name):
      result = types.FunctionType(func.__code__, func.__globals__, name=func.__name__, argdefs=func.__defaults__, closure=func.__closure__)
      result = functools.update_wrapper(result, func)
      result.__kwdefaults__ = func.__kwdefaults__
      result.__name__ = name
      return result

Code cannot use compiled functions to create uncompiled ones from them,
so the above code will not work. However, there is a dedicated ``clone``
method that is specific to them, so use this instead.

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

You can compile modules and packages with **Nuitka**, no problem, but
when it comes to executing it, ``python -m compiled_module`` is not
going to work and give the error ``No code object available for
<module_name>``.

Because the compiled module is not source code, and **Python** will not
just load it with the ``-m`` implementation. The closest to it is
``python -c "import compile_module"`` and you might have to call the
main function yourself.

To support this, the **Python** ``runpy`` and/or ``ExtensionFileLoader``
would need improving such that **Nuitka** could supply its compiled
module object for Python to use.
