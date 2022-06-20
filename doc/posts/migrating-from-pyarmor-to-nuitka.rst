.. post:: 2022/06/20 10:29
   :tags: Python, Windows, compiler, Nuitka, HowTo
   :author: Kay Hayen

##################################
 Migrating from PyArmor to Nuitka
##################################

*********
 Preface
*********

Nuitka, esp. Nuitka commercial has the big advantage over PyArmor, in
that there is simply no bytecode to protect, both Nuitka and Nuitka
commercial generate C code, and ultimately machine code. That is vastly
superior to obfuscation of the bytecode.

To illustrate the point, maybe it's telling that before Nuitka used the
``ast`` module to parse Python code, it re-constructed loops,
conditions, etc. with no issues from bytecode. There is a well
established set of tools that do this probably a lot better, which
Nuitka is putting Python on (almost) equal footing with C code in terms
of protection.

.. important::

   Nuitka commercial also protects your constants data and is
   recommended for anyone who cares about their software getting hacked.

*****************
 Questions Asked
*****************

Therefore, two questions are frequently asked.

:Q:
   Should I use both?

:A:
   No, as Nuitka leaves no bytecode behind, pyarmor has nothing to work
   with that does any actual work. So there is no point.

:Q:
   And how do I migrate from pyarmor to Nuitka?

:A:
   It's easy and should improve your build at the same time.

*******************
 Example Migration
*******************

Below, we see a variation of the build script provided by one user, that
we will discuss how to replace, one by one.

.. code:: bash

   %{{%
       "C:/Users/kayha/AppData/Roaming/Python/Python39/Scripts/pyarmor" pack
       -x " --advanced 2 --bootstrap 2 --enable-suffix"
       -e "
           --add-data 'C:/Users/kayha/AppData/Roaming/Python/Python39/site-packages/eel^;eel'
           --add-binary 'C:/Users/kayha/AppData/Roaming/Python/Python39/site-packages/vosk/libvosk.dll^;vosk'
           --add-binary 'names.txt^;.'
           -c
           --onefile
           --icon "program.ico"
           --hidden-import cryptography
           --hidden-import PIL
           --hidden-import PIL.Image
       "
       --name "Your Application Name"
       main.py
   %}}%

First off, one this that becomes immediately apparent is the hard coding
of Python and package installation paths. That is not needed, Nuitka
will find the things for you. It also prevents you from easily updating
your machine, your Python version, working with a virtualenv (which you
really should do), and these kinds of things.

.. code:: bash

   pyarmor ... --add-data 'C:/Users/kayha/AppData/Roaming/Python/Python39/site-packages/eel^;eel'

For Nuitka. including package data is simply done like this:

.. code:: bash

   --include-package-data=eel

It will find the package ``eel`` that your code will use if you import
things, so e.g. a local package installation will be preferred over the
system one, no problem. It will detect all data-files, i.e. things that
are not DLLs, not Python code, not bytecode, and not extension modules.

What's more, in Nuitka there is an active community of people who
contribute to its package configuration, so in case a package will not
work without the data files, it will be already there by default.

.. note::

   For packages whose data files are not yet there, please raise bugs on
   the GitHub issue tracker, they can be added for everybody.

In this case, the package configuration of Nuitka has this entry:

.. code:: yaml

   - module-name: "eel"
     data-files:
       patterns:
         - "eel.js"

If you encounter this for any package, say even ``your_package``, then
you can just add a similar configuration to a yaml file, and use it with
``--user-package-configuration-file=my_file.yaml`` and similar content,
and it would also work.

.. important::

   For PyPI packages, it would be super sweet if you created a PR out of
   your configuration file there.

There is another example, of a data file in there. That is

.. code:: bash

   pyarmor ... --add-binary 'names.txt^;.'

This data file is not associated with a package. In this case, the more
generic option of Nuitka comes to play.

.. code::

   python -m nuitka ... --include-data-files=names.txt=names.txt'

This is the form of the option with a single file. With pattern, you can
copy all matching files, and there even a variant for a recursive copy
of files in a folder matching a name, that preserves folders.

.. code:: bash

   python -m nuitka ... --include-data-files=.=.=**/*.txt

The above would also copy the file from the current directory, to top
level in the distribution folder, but that then would also find files
that are in subdirectories.

As you can see, these are very powerful options for picking up data
files, and the main take away is, that while you can work with paths,
you don't have to and probably shouldn't.

The next item is this:

.. code:: bash

   pyarmor ... --add-binary 'C:/Users/kayha/AppData/Roaming/Python/Python39/site-packages/vosk/libvosk.dll^;vosk'

For DLLs, Nuitka has special love. This is because depending on the
platform, DLLs need special treatment to be portable. They get checks
and automatic modifications that are indispensable to be complete, e.g.
to include other DLLs used by one DLL are detected by dependency
analysis. Skipping that can cause all kinds of errors.

For the example, if Nuitka didn't contain this already, what you could
do is to provide this as a user yaml file, which if course, you can do
for your own code as well. There is two approaches, in one filenames are
scanned, if the are DLLs, that match given prefixes, or in another more
complex case, code can be executed, that provides DLL file names.

So this is what we got here.

.. code:: yaml

   - module-name: "vosk"
     dlls:
       - from_filenames:
           prefixes:
             - "libvosk"

And for reference, if you wanted to use code instead, that's also
possible and works by compile time execution of said code.

.. code:: yaml

   - module-name: "shapely.geos"
     dlls:
       - dest_path: "shapely"
         by_code:
           setup_code: "import shapely.geos"
           dll_filename_code: "shapely.geos._lgeos._name"

In this, the setup code does preparatory work, most likely importing
modules. You can have multiple statements, by using ``;`` to separate
them. And then there is an expression, to be evaluated (this is using
``eval`` at the end of the day) and that's the DLL filename. Works for
modules that have complex rules for their DLL filename, but a runtime
variable that is accessible with the filename.

So, this is very flexible. At this time, there is no option to include
package DLLs or DLLs by filename. The above approach does have to be
used. Mostly in hope of making it easy to integrate them into Nuitka via
PR.

.. note::

   The main goal of Nuitka to have that out of the box experience of it
   working. That's what we strive for, but options are going to come as
   well.

The ``--onefile`` option is named the same. Nuitka has a standalone
option as well, and lets you have it as a result from the onefile build
as well, so in case of missing data files, it is easier to play around
without having a full rebuild.

The ``--icon`` option of Nuitka is platform specific, and for ``.ico``
files, you can use ``--windows-icon-from-ico``, but e.g. for Windows,
there is also an option to use a template executable and Nuitka copies
it from there. And something that is not yet well documented, but
deserves to, is that you do not have to create an icon file yourself,
but Nuitka will gladly use your existing ``.png`` file, and convert to
an icon itself. The same holds true for other platforms, e.g. macOS,
where its ``.icns`` format is created automatically from the same PNG.

So, rather than using this:

.. code:: bash

   pyarmor ... --icon program.ico

.. code:: bash

   python -m nuitka ... --windows-icon-from-ico=program.ico

   # You may find this works even better.
   python -m nuitka ... --windows-icon-from-ico=program.png

Also with Nuitka, there is much more version information available for
your control, there is ``--windows-product-name`` and
``--windows-product-version`` to name a few, but there is much more for
cleanly looking executables.

.. code:: bash

   pyarmor ... --hidden-import PIL.Image

This is another example, of something that is already solved by default
in Nuitka. All image format plugins are added automatically. But if they
were not, you would say

.. code:: bash

   python -m nuitka ... --include-package=PIL.Image

This will tell Nuitka to include everything below a certain package,
even if it appears unused. There is always a catch here, that it might
be too much, so if this happens with PyPI packages, it is probably best
to report the issue and have Nuitka adapted.

Here is an example, of how this could also be achieved in Yaml:

.. code:: yaml

   module-name: "phonenumbers.data"
     implicit-imports:
       depends:
         - ".region_*"

That is a real example, taken from Nuikta package configuration, and one
that is vastly superior to the command line option. Here as you see, it
will scan for sub-packages that match a pattern, and include only those.
In this way, no unused code from the package gets included.
