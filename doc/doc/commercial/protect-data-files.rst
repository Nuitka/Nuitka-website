:orphan:

####################
 Protect Data Files
####################

Your program might be using Qt and QML, or other kinds of data file
loaded. With Nuitka Commercial, you can produce an executable that
contains them and then also covers it under the regular `constants data
protection <protect-constants-data.html>`__ automatically.

Due to constant data protection, the contents of the files will be
inaccessible to anything but the program, and this is very much what
people want.

Your program continues to use standard Python mechanisms from ``open``,
``pkgutil``, ``pkg_resources``, ``importlib.resources`` or
``importlib_resources`` and generally all similar packages, and these
load the data as a file or a stream from within the binary without ever
hitting the disk.

All of this is happening with your original code base, i.e. you are not
making any modification, that is incompatible with Python. This is one
of the major goals. Your code will still run directly in Python during
development, and during deployment, the files are embedded by merely
adding a Nuitka commercial option.

**********
 Examples
**********

We are going to look at the various APIs in detail, and show part of
what is working. Generally embedding aims at requiring no modification
of your program. Read through all the examples, as each one is going to
tell you something new.

Qt resources
============

This means, e.g. rather than this program

.. code::

   PySideQmlPolarchartTest.py
   qmlpolarchart/
       Example-Icon.svg
       main.qml
       View1.qml
       View2.qml
       View3.qml

you get a file layout just simply like this (DLLs and PyQt extensions
not shown) that doesn't contain your QML files, not the icon file.

.. code::

   PySideQmlPolarchartTest.exe

The code can do simply this, and refer to the icon file relative to
where the code lives which will work with standard Python, standard
Nuitka, and for embedding with Nuitka commercial.

.. code:: python

   icon_filename = os.path.join(
       os.path.dirname(__file__), "qmlpolarchart/Example-Icon.svg"
   )
   app.setWindowIcon(QIcon(icon_filename))

For Nuitka commercial, the options to include the data file and to then
embed it are as follows:

.. code:: bash

   python -m nuitka ... --include-data-dir=qmlpolarchart=qmlpolarchart \
                        --embed-data-files-qt-resource-pattern=qmlpolarchart/**

The general rule is to first include your data files with the standard
Nuitka means, in this case, we use a data directory. Generally e.g.
``--include-package-data`` can be a better choice too, as you avoid file
paths entirely. After that, embedding options work on target paths. And
with the ``/**`` part of the patterns (could also use ``qmlpolarchart``)
we ask it to include all these files as embedded. This being a pattern
allows you to include only a subset

In standard Nuitka, you end up with something like this. And note, that
onefile mode is merely a self extracting archive, i.e. these files will
be on the customer disk for inspection:

.. code::

   PySideQmlPolarchartTest.exe
   qmlpolarchart/
       Example-Icon.png
       Example-Icon.svg
       main.qml
       View1.qml
       View2.qml
       View3.qml

.. note::

   For extension modules and DLLs used, this doesn't affect things. This
   is about merely about data files. This is where ``--onefile`` comes
   in and hides these from the view and need for deployment, but it
   cannot replace Nuitka commercial and its inclusion of data files
   inside the main binary.

**********************************************************
 Using ``open``, ``os.listdir``, ``os.path.isfile``, etc.
**********************************************************

As you can see from below code, the traditional Python file handling
just works, and we took large efforts to get standard ``open`` to work
seamlessly. It is not the easiest way to use data files, but a very
common usage in third party packages and the idea of Nuitka commercial
is to make work, what worked before, see below for the more modern
approaches.

.. code:: python

   # Standard open works with binary and text mode, encoding, etc.
   print(
      "Contents of data file 1 (as binary):",
      open(
         os.path.join(os.path.dirname(__file__), "data_file1.txt"),
         "rb"
      ).read(),
   )
   print(
      "Contents of data file 1 (as text):",
      open(
         os.path.join(os.path.dirname(__file__), "data_file1.txt"),
         "r"
      ).read(),
   )

   # Works also for functions that cannot not be statically optimized.
   def dynamicFunction(filename):
      print(
         "Contents of dynamic data file (as binary):",
         repr(open(filename, "rb").read()),
      )

      print(
         "Contents of dynamic data file (as text):",
         repr(open(filename, "r").read()),
      )

   dynamicFunction(os.path.join(os.path.dirname(__file__), "data_file3.txt"))

   print("Using with and open data file 4 gives (as binary):")

   # The "with" statement works too.
   with open(
      os.path.join(os.path.dirname(__file__), "data_file4.txt"), "rb"
   ) as binary_stream:
      print("Line 1:", repr(binary_stream.readline()))
      print("Line 2:", repr(binary_stream.readline()))

   with open(
      os.path.join(os.path.dirname(__file__), "data_file4.txt"), "r"
   ) as text_stream:
      print("Line 1:", repr(text_stream.readline()))
      print("Line 2:", repr(text_stream.readline()))

   print("Checking with 'os.path.isdir' for contained and not contained directories:")

   # The "os.path.isdir" works, "os.path.isfile", and "os.path.exists" too.
   print(
      "isdir on templates:",
       os.path.isdir(os.path.join(os.path.dirname(__file__), "templates")))
   )
   print(
      "isfile on data_file4.txt:",
      os.path.isfile(os.path.join(os.path.dirname(__file__), "data_file4.txt")),
   )
   print(
      "exists on 'templates' dir:",
      os.path.exists(os.path.join(os.path.dirname(__file__), "templates")),
   )
   print(
      "exists on 'data_file4.txt':",
      os.path.exists(os.path.join(os.path.dirname(__file__), "data_file4.txt")),
   )

   # Listing the embedded data files with os.listdir works too.
   print(
      "os.listdir of package dir gives:",
      os.listdir(os.path.join(os.path.dirname(__file__))),
   )

********************
 Use of ``pkgutil``
********************

The ``pkgutil.get_data`` was the first way for standard library of
accessing data file content from packages in a fashion that does not
require to use ``__file__``. However, it's limited in getting the data.

.. code:: python

   import pkgutil
   print(
      "Contents of data file 1:",
      repr(pkgutil.get_data(__package__, "data_file1.txt")
   )

**************************
 Use of ``pkg_resources``
**************************

The ``pkg_resources`` was one of the first to offer ways of accessing
data files from packages in a fashion that does not require to use
``__file__``. It has since become less popular and was never part of
standard Python, but extremely wide spread and is still in use.

.. code:: python

   import pkg_resources

   # This shows using pkg_resources to get a string.
   print(
      "Contents of data file 1:",
      repr(pkg_resources.resource_string(__package__, "data_file1.txt")),
   )

   # This shows using pkg_resources to get a stream, which then can be used
   # like a file. Here we read it right away, but it could be passed elsewhere
   # of course.

   print(
      "Stream of data file 1 gives:",
      repr(pkg_resources.resource_stream(__package__, "data_file1.txt").read()),
   )

***********************************************************************
 Use of ``importlib.resources`` and ``importlib_resources (backport)``
***********************************************************************

The most recent addition to standard library is also available as a
backport and both are supported by Nuitka commercial file embedding.

.. code:: python

   # Could use importlib_resources as well for older Python versions.
   import importlib.resources

   # Can read as str or bytes:
   print(
      "Contents of data file 1 (as binary):",
      repr(importlib.resources.read_binary(__package__, "data_file1.txt")),
   )
   print(
      "Contents of data file 1 (as text):",
      repr(importlib.resources.read_text(__package__, "data_file1.txt")),
   )

   # Can get binary or text streams:
   print(
      "Stream of data file 1 gives (as binary):",
      repr(importlib.resources.open_binary(__package__, "data_file1.txt").read()),
   )

   print(
      "Stream of data file 1 gives (as text):",
      repr(importlib.resources.open_text(__package__, "data_file1.txt").read()),
   )

**************
 Using Jinja2
**************

Jinja does a few special things with files, and Nuitka commercial
however supports it as well, without changes. We iterate here over
various approaches seen, that all work. File system loaders and package
loaders are all fine.

.. code:: python

   # Old school string paths
   loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
   env = jinja2.Environment(
      loader=loader,
   )
   template = env.get_template("templates/data_file5.txt")
   print("Template loaded via old school file system strings:", template)

   # New school "pathlib" paths work too.
   from pathlib import Path
   loader = jinja2.FileSystemLoader(
       Path(os.path.dirname(os.path.abspath(__file__))) / "templates"
   )
   env = jinja2.Environment(
       loader=loader,
   )
   template = env.get_template("templates/data_file5.txt")
   print("Template loaded via pathlib use paths gave template:", template)

   # Package loaders work of course too.
   loader = jinja2.PackageLoader("data_inclusion", "templates")
   env = jinja2.Environment(
      loader=loader,
   )
   template = env.get_template("templates/data_file5.txt")
   print("Template loaded via package loader:", template)

Go `back to Nuitka commercial
</doc/commercial.html#protection-vs-reverse-engineering>`__ overview to
learn about more features or to subscribe to `Nuitka commercial
</doc/commercial.html#pricing>`__.
