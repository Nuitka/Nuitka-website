.. post:: 2023/01/19 15:51:00
   :tags: Python, compiler, Nuitka, package_config
   :author: Kay Hayen

######################################
 Nuitka Package Configuration Kickoff
######################################

The term "kickoff" refers to a series of posts about the Nuitka package
configuration. The details are here on a dedicate page on the web site
only. `Nuitka Package Configuration
<https://nuitka.net/doc/nuitka-package-config.html>`__.

This documentation is still very rough and bare of examples, but the
goal is to make it more complete as package of this series of posts.
When we have an instructive example, we will make a post.

This is an area of Nuitka, where help will be very easy and a wide
variety of people will have the skills and desire to help, but the lack
of documentation, makes it hard or impossible to channel the common
knowledge.

#################
 Problem Package
#################

Each post will feature one package that caused a particular problem. In
this case, we are talking about the package ``tkinterweb``.

Problems are typically encountered in standalone mode only. Missing data
files and DLLs are usually only and issue there, but this one actually
also had a problem with accelerated mode.

#################
 Initial Symptom
#################

The compiled program gave the following error:

.. code::

   ModuleNotFoundError: The files required to run TkinterWeb could not be found. This usually occurs when bundling TkinterWeb into an app without forcing the application maker to include all nessessary files. See https://github.com/Andereoo/TkinterWeb/blob/main/tkinterweb/docs/FAQ.md for more information.

   Error: Traceback (most recent call last):
       File "C:\...\200~1.0\tkinterweb\__init__.py", line 32, in <module tkinterweb>
   ModuleNotFoundError: No module named 'bindings'

.. note::

   The traceback has been redacted, removing user specific part and
   replacing it with ``...``.

The strange looking part of the filename ``200~1.0`` in the traceback is
because Nuitka on Windows is convincing the program that it runs in a
short path. So the errors you get, are not pointing to the name of the
binary inside the dist folder, but to a shorter path, that is however
exactly the same folder. You wouldn't believe how many parts of Python
still don't have long filenames handled properly. Actually Tcl and
TkInter are among them.

#####################
 Step 1 - data files
#####################

So, whenever a Python module fails to import, this can be caused by
missing data files. In Nuitka land, these are not extension modules,
DLLs, bytecode, etc. but everything else, and it has been seen that
these can cause issues. So what to do here. This is easy, Nuitka has
recently gained a command dedicated to this operation, making use of its
internal code to list data files for a package.

Here we go

.. code:: shell

   python3.10 -m nuitka --list-package-data=tkinterweb

Gives output:

.. code::

   Nuitka-Tools:INFO: Checking package directory 'C:\Python310\lib\site-packages\tkinterweb' ..
   C:\Python310\lib\site-packages\tkinterweb
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\combobox-2.3.tm
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\pkgIndex.tcl
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Darwin\64-bit\pkgIndex.tcl
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Linux\32-bit\pkgIndex.tcl
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Linux\64-bit\pkgIndex.tcl
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Windows\32-bit\pkgIndex.tcl
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Windows\64-bit\pkgIndex.tcl

So there are data files, great. Lets just include them, and retry. There
appears to be need for that anyway. Now we could use
``--include-package-data=tkinterweb`` for quickly trying it out, but
since we are in here to make it generally useful, we will start
modification of the Yaml file right away.

.. code:: yaml

   - module-name: 'tkinterweb'
     data-files:
       dirs:
         - 'tkhtml'

So, we retry, and nothing changes. Not enough, but on the other hand, it
was obviously necessary anyway.

####################
 Step 2 - DLL files
####################

The other big trouble maker, and easy to check nowadays, is missing
DLLs. Extension modules can depend on DLLs. When they are linked
against, this not usually and issue, and Nuitka and its plugins
typically resolve all of those perfectly, but often DLLs are loading
manually. Maybe this is what is going on here.

Also recently, Nuitka gained a command to check for DLLs.

Here we go

.. code:: shell

   python3.10 bin/nuitka --list-package-dlls=tkinterweb

Gives output:

.. code::

   Nuitka-Tools:INFO: Checking package directory 'C:\Python310\lib\site-packages\tkinterweb' ..
   C:\Python310\lib\site-packages\tkinterweb
   C:\Python310\lib\site-packages\tkinterweb\tkhtml
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Darwin
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Darwin\64-bit
   tkhtml\Darwin\64-bit\Tkhtml30.dylib
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Linux
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Linux\32-bit
   tkhtml\Linux\32-bit\Tkhtml30.so
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Linux\64-bit
   tkhtml\Linux\64-bit\Tkhtml30.so
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Windows
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Windows\32-bit
   tkhtml\Windows\32-bit\Tkhtml30.dll
   C:\Python310\lib\site-packages\tkinterweb\tkhtml\Windows\64-bit
   tkhtml\Windows\64-bit\Tkhtml30.dll

.. note::

   The output could be not containing folders that have no DLLs
   themselves, but well, such is life, we are going to improve that
   another time.

What this tells us, that in fact there are DLLs, and from the looks of
it, there is no automatic anything in this. This also appears to be one
of those PyPI packages that contain binaries for everything. Rather than
building a wheel per architecture this contains some things, on all
platforms. For a Python installation that is cool, but surely we do not
want to deploy both the 32 and 64 bit DLLs where the compiled binary is
only one of these. Do not even think of different OS, like including
Linux DLLs on Windows.

So, luckily this is easy to handle. We can select for OS and
architecture on Windows for a while already.

.. code:: yaml

   - module-name: 'tkinterweb'
     dlls:
       - from_filenames:
           relative_path: 'tkhtml/Windows/32-bit'
           prefixes:
             - 'Tkhtml'
         when: 'win32 and arch_x86'
       - from_filenames:
           relative_path: 'tkhtml/Windows/64-bit'
           prefixes:
             - 'Tkhtml'
         when: 'win32 and arch_amd64'

.. note::

   Showing this here without the data files section for clarity,
   obviously the DLLs just get added, and Nuitka prevents you from
   having two blocks referencing the same module.

So, including DLLs is fairly easy. If the package directory is not where
the DLL lives, you specify ``relative_path`` which is otherwise
optional. This also influences where it is put in the distribution
folder. Then when specifying the DLL, we do only give the prefix of the
DLL. Choosing here to leave out the ``30`` part of ``Tkhtml30.dll`` just
because it's probably going to make our life easier down the road,
should they update that version number, it would still automatically
work.

Obviously for other platforms than Windows, the DLLs are not included
now, but lets see if this works. And actually at the time of writing,
this is a first. As you can see, on macOS (recognized from "Darwin")
only the ``x86_64`` will work, and maybe we should check that out. For
Linux and 32 bit, this shows what an old package this is.

So far, outside of Windows, we do not provide tags for arches.

.. note::

   This is probably going to change now. At least on macOS this seems
   very much needed. Maybe also time to cleanup ``amd64`` vs ``x86_64``
   which kind of is an inconsistency the technical community has.

Anyway, so more branches will be needed. There is no ``else`` in Nuitka
package configuration. All ``from_filenames`` blocks are applied if the
``when`` matches.

And actually for data files are similar thing should be done, however,
for the time being ``--noinclude-data-file`` can be your friend there.
You can manually exclude them.

But low and behold, the DLLs are included. The data files are. Typically
that is enough, but it **still** does not work.

#######################################
 Step 3 - Check the compilation report
#######################################

So after following the easy steps to take, and still not working. We can
check the compilation report. You should always compile with
``--report=compilation-report.xml`` which produces a very human readable
compilation report, where you can check things easily.

It lists included DLLs and data files, and often also why it is
included, and as of recently it learned to output also modules that were
used by a module, and modules that were attempted to be used, but not
found.

.. note::

   This newly tracked information about failed attempts to use a module
   are the basis of largely enhanced bytecode caching (demoted e.g.
   because too large or standard library) in latest Nuitka.

Nuitka will tell use here about the issue from its perspective. So a
module is not found at runtime, but what happened at compile time. Only
the report can tell.

Lets quote the compilation report snippets.

.. code:: xml

   <module name="__main__" kind="PythonMainModule" reason="Root module">
     <optimization-time pass="1" time="0.25" />
     <optimization-time pass="2" time="0.01" />
     <module_usages>
       <module_usage name="tkinterweb" finding="absolute" line="1" />
       <module_usage name="tkinter" finding="absolute" line="4" />
       <module_usage name="Tkinter" finding="not-found" line="6" />
     </module_usages>
   </module>

This is the main module. Even without giving you the source code, you
can see that the example code does import tkinterweb and tkinter. And
due to this being probably very old code, the Python2/Python3 module
name difference is present, so it imports the Python3 name successfully,
but not the Python2 name.

How do we know this is a bug or not? The reality is, we do by context
knowledge, there is not a single best way to decide if an import that is
not found represents an issue in the compilation or not. But this looks
good. I am showing it to you for educational purpose mostly.

Now lets find the module that raised the ``ModuleNotFoundError``
exception.

.. code:: xml

   <module name="tkinterweb" kind="CompiledPythonPackage" reason="Instructed by user to follow to all non-standard library modules.">
     <plugin-influence name="dll-files" influence="condition-used" condition="win32 and arch_x86" tags_used="win32,arch_x86" result="false" />
     <plugin-influence name="dll-files" influence="condition-used" condition="win32 and arch_amd64" tags_used="win32,arch_amd64" result="true" />
     <optimization-time pass="1" time="0.07" />
     <optimization-time pass="2" time="0.03" />
     <module_usages>
       <module_usage name="os" finding="absolute" line="1" />
       <module_usage name="sys" finding="built-in" line="1" />
       <module_usage name="sys" finding="built-in" line="27" />
       <module_usage name="os" finding="absolute" line="27" />
       <module_usage name="ntpath" finding="absolute" line="28" />
       <module_usage name="bindings" finding="not-found" line="31" />
       <module_usage name="htmlwidgets" finding="not-found" line="32" />
       <module_usage name="utilities" finding="not-found" line="33" />
       <module_usage name="traceback" finding="absolute" line="35" />
       <module_usage name="sys" finding="built-in" line="41" />
       <module_usage name="tkinter" finding="absolute" line="44" />
       <module_usage name="tkinter" finding="absolute" line="45" />
       <module_usage name="tkinter.messagebox" finding="relative" line="45" />
       <module_usage name="Tkinter" finding="not-found" line="47" />
       <module_usage name="tkMessageBox" finding="not-found" line="48" />
       <module_usage name="tkinter" finding="absolute" line="67" />
       <module_usage name="Tkinter" finding="not-found" line="69" />
     </module_usages>
   </module>

At the top, you can see the ``plugin-influence``. This is where the
plugin records that it influenced. It records what conditions were
checked, and the result. Actually further down, we got this.

.. code:: xml

   <included_dll name="Tkhtml30.dll" dest_path="tkinterweb\tkhtml\Windows\64-bit\Tkhtml30.dll" source_path="C:\Python310_64\lib\site-packages\tkinterweb\tkhtml/Windows/64-bit\Tkhtml30.dll" package="tkinterweb" ignored="no" reason="Yaml config of 'tkinterweb'" />

But that is now why we are here. You can also see the imports being
done. They are given with line numbers and the one we care about is this
snippet.

.. code:: xml

   <module_usage name="bindings" finding="not-found" line="31" />

So Nuitka didn't find it at compile time. And a quick check with Python
on the prompt would reveal that this name is not importable. So now we
switch to the source code of the trouble making module. There is no tool
for that yet, typically just do this manually:

.. code::

   >>> import tkinterweb
   >>> tkinterweb
   <module 'tkinterweb' from 'C:\\Python310\\lib\\site-packages\\tkinterweb\\__init__.py'>

This is a clickable link in my Visual Code terminal, and after I click
it and go to the line, what we see is:

.. code:: python

   import sys, os
   sys.path.append(os.path.dirname(os.path.realpath(__file__)))

   try:
       from bindings import TkinterWeb
       from htmlwidgets import HtmlFrame, HtmlLabel
       from utilities import Notebook
   except (ImportError, ModuleNotFoundError):
       # Useless code goes here.
       ...

What strikes immediately is that Visual Code agrees, and displays the
imported names a color used for modules that it couldn't resolve. And
actually the first like on top there is revealing rather rare code. This
package is extending the global import path with its package contents.
In this way, what would be ``tkinterweb.bindings`` is available as
``bindings`` **after** the module has been imported at runtime.

Expanding the ``PYTHONPATH`` is therefore our next step. Since I am
using bash, I can prefix the call to Nuitka with
``PYTHONPATH='C:\\Python310_64\\lib\\site-packages\\tkinterweb'`` and
low and behold, it works with this. Compilation takes longer and
includes more modules, and the initial message is gone.

So, how to resolve this. Nuitka has gained a feature dedicated to this.
It will be nice if this was automatically resolved at compile time,
which is well could, note has been taken that there is value in tracking
expanding ``sys.path`` at compile time.

There is another section called ``import-hacks`` and it too recently
gained a new feature dedicated to this.

.. code:: yaml

   - module-name: 'tkinterweb'
     import-hacks:
       - global-sys-path:
           # This package forces itself into "sys.path" and expects absolute
           # imports to be available.
           - ''

We can here provide a list of relative paths, that are added when a
package is imported to the search path of Nuitka. With this we can drop
the ``PYTHONPATH`` which while being a nice workaround, required using
absolute paths of the install, never easy to handle.

With this it now works fully automatically. One issue remains. The
compiled program does not need the ``sys.path`` trick at runtime. And
for isolation purposes, ``sys.path`` ought to be empty, so what we do we
do with this here?

###########################
 Step 4 - Cleanup the code
###########################

In order to get rid of that code, we can use the ``anti-bloat``
mechanism. It is very powerful and can do all sorts of things, but today
we got a simple task for it.

This is the troubling line.

.. code:: python

   sys.path.append(os.path.dirname(os.path.realpath(__file__)))

There are many ways to change this, it's always good be at less invasive
as possible, so we do not want to append. We could prefix that line with
``if False:``, but that typically only works well for single liners.
What we can do rather generally is something like this:

.. code:: python

   sys.path.append(os.path.dirname(os.path.realpath(__file__)))
   # -> we want this instead:
   (os.path.dirname(os.path.realpath(__file__)))

Notice that just not calling will be good enough and extremely likely
robust against all kinds of formatting changes, multiple lines, etc. and
probably also very applicable should be encounter similar ones.

So this can be expressed with the following yaml snippet.

.. code:: yaml

   - module-name: 'tkinterweb'
     anti-bloat:
       - description: 'remove "sys.path" hack'
         replacements_plain:
           'sys.path.append': ''

And to know what effect it had and to see the wonders if anti-bloat in
general, you can use ``--show-source-changes`` and output the diffs done
on module source changes.

.. code::

   --- original
   +++ modified

   @@ -25,7 +25,7 @@

    """

    import sys, os
   -sys.path.append(os.path.dirname(os.path.realpath(__file__)))
   +(os.path.dirname(os.path.realpath(__file__)))

    try:
        from bindings import TkinterWeb

So, now this is perfect. Just need to add more OS specific branches,
maybe also for the data files include more selectively, then this is
perfect.

###############
 Final remarks
###############

I am hoping you will find this very helpful information and will join
the effort to make packaging for Python work out of the box. Adding
support for ``tkinterweb`` was a little more complex than your typical
package. The OS specific DLLs in different places are relatively
unusual, although it has been seen before and will be gain.

This is a simpler example, that is way less complex, with all defaults
just working.

.. code:: yaml

   - module-name: 'lightgbm.libpath'
     dlls:
       - from_filenames:
           prefixes:
             - 'lib_lightgbm'

Please review the guidelines for contributing, and esp. make sure to
install the commit hook as described, or run
``bin/autoformat-nuitka-source --yaml`` at least, so the CI will not
complain about formatting and we will have consistent files.

The last hot fixes of 1.3 already have user provided packaging
enhancements that add dependencies and anti-bloat. We might discuss
those in the next installment.
