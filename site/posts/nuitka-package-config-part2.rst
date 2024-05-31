.. post:: 2023/02/13 09:01:00
   :tags: Python, compiler, Nuitka, package_config
   :author: Kay Hayen

#####################################
 Nuitka Package Configuration Part 2
#####################################

This is the second part of a post series under the tag `package_config
<https://nuitka.net/blog/tag/package_config.html>`__ that explains the
Nuitka package configuration in more detail. To recap, Nuitka package
configuration is the way Nuitka learns about hidden dependencies, needed
DLLs, data files, and just generally avoids bloat in the compilation.
The details are here on a dedicate page on the web site in `Nuitka
Package Configuration
<https://nuitka.net/doc/nuitka-package-config.html>`__ but reading on
will be just fine.

#################
 Problem Package
#################

Each post will feature one package that caused a particular problem. In
this case, we are talking about the package ``customtkinter``.

Problems are typically encountered in standalone mode only. Missing data
files are typical issue there, and in this case, we already had a
solution, but turns out, only working on Windows for a weird reason. We
are going to look at that in some detail, and will see a workaround
applied with the ``anti-bloat`` engine doing code modification on the
fly.

#################
 Initial Symptom
#################

The initial symptom reported was like this, on the Nuitka Discord server
and much to my surprise, against the then current 1.4.4 release of
Nuitka.

.. code::

   Traceback (most recent call last):
   File "/tmp/onefile_32802_1675869955_205649/customtkinter/windows/widgets/theme/__init__.py", line 5, in <module customtkinter.windows.widgets.theme>
   File "/tmp/onefile_32802_1675869955_205649/customtkinter/windows/widgets/theme/theme_manager.py", line 18, in load_theme
   FileNotFoundError: [Errno 2] No such file or directory: '/tmp/onefile_32802_1675869955_205649/customtkinter/windows/widgets/theme/../../../assets/themes/blue.json'

One thing to say here is that if you have this kind of issues, using
onefile is definitely too early. The recommendation is to use onefile
only after standalone works, because it is easier to debug.

###################
 Step 1 - Analysis
###################

So first thing, I did was to normalize the path, so I can see if
something funny is going on, with that.

.. code::

   >>> import os
   >>> os.path.normpath("/tmp/onefile_32802_1675869955_205649/customtkinter/windows/widgets/theme/../../../assets/themes/blue.json")
   '/tmp/onefile_32802_1675869955_205649/customtkinter/assets/themes/blue.json'

So this matches existing data files. Originally we had worked off this
on Windows,

.. code::

   python3.10 -m nuitka --list-package-data=customtkinter
   Nuitka-Tools:INFO: Checking package directory 'C:\Python310_64\lib\site-packages\customtkinter' ..
   C:\Python310_64\lib\site-packages\customtkinter
   C:\Python310_64\lib\site-packages\customtkinter\assets\fonts\CustomTkinter_shapes_font.otf
   C:\Python310_64\lib\site-packages\customtkinter\assets\fonts\Roboto\Roboto-Medium.ttf
   C:\Python310_64\lib\site-packages\customtkinter\assets\fonts\Roboto\Roboto-Regular.ttf
   C:\Python310_64\lib\site-packages\customtkinter\assets\icons\CustomTkinter_icon_Windows.ico
   C:\Python310_64\lib\site-packages\customtkinter\assets\themes\blue.json
   C:\Python310_64\lib\site-packages\customtkinter\assets\themes\dark-blue.json
   C:\Python310_64\lib\site-packages\customtkinter\assets\themes\green.json

Which confirms the data file, and had lead to adding configuration to
include these data files.

.. code:: yaml

   - module-name: 'customtkinter'
     data-files:
       dirs:
         - 'assets'

This is the most simple for including data files. Because there are no
needs to limit by file type, and not even a wish to know what file types
might get added in the future. We add the folder and are good.

Since the original report was on Windows, it was tested there and
assumed to be good on all platforms.

####################
 Step 2 - Debugging
####################

So, the data files are indeed included, which was confirmed by asking to
compile in standalone and to provide the listing. However, at run time
they were not found.

This is where the platform differences come in, somewhat to my surprise,
on Windows the
``customtkinter/windows/widgets/theme/../../../assets/themes/blue.json``
part of the path works, even though there is no ``windows`` directory.
Since compiled code is contained in the executable, packages in
standalone may not have a directory associated.

So while ``__file__`` is set to that virtual directory, it does not
exist. And usually that is all good, and directories get created of
course when package data gets added. That is e.g. why ``customtkinter``
and then of course ``customtkinter/assets`` exist. But
``customtkinter/windows`` does not.

The platform difference, that I was not aware of that only on Windows,
will a path being opened get normalized before being used.

.. code::

   >>> os.name
   'nt'
   >>> os.path.exists("README.rst")
   True
   >>> os.path.exists("doesnotexist")
   False
   >>> os.path.exists("doesnotexist\\..\\README.rst")

But neither on Linux nor macOS this is going to be possible. So that was
the problem. Checkout their code, this is what is used:

.. code:: python

   with open(os.path.join(script_directory, "../../../assets", "themes", f"{theme_name_or_path}.json"), "r") as f:
       cls.theme = json.load(f)

This could have used ``pkg_resources`` or ``importlib.resources`` or
many of the methods that Nuitka supports out of the box. But actually
``open`` and being ``__file__`` relative is supposed to be fine.

So this does not work.

##############################
 Step 2 - Devising a solution
##############################

So, there are actually a couple of ways to resolve this. One would be to
just provide the empty directories that non-Windows is checking to
exist. These would then have to be deployed. There is actually support
for that in Nuitka package configuration.

And we have examples of that in our existing configuration, e.g. for
``Crypto.Util._raw_api``.

.. code:: yaml

   - module-name: 'customtkinter.windows.widgets.theme.theme_manager'
     data-files:
       empty_dirs:
         - '.'

This is for code that insists on the package directory, but honestly,
while it is easy enough, I don't quite like this solution. The empty
directory requires a dummy file, and ultimately it that is all that is
used for is rather ugly.

So, what else we can do? Well, we can modify the code of course too. We
have the ``anti-bloat`` engine and it is capable of achieving reduction
of bloat. What if the we used it to modify the code to do a
``os.path.normpath`` and that is actually what we ended up doing. The
most simple form of anti-bloat does plain string replacements. Here it
is used.

.. code:: yaml

   - module-name: 'customtkinter.windows.widgets.theme.theme_manager'
     anti-bloat:
       - description: 'workaround for file path on Linux'
         replacements_plain:
           'script_directory, "../../../assets"': 'os.path.normpath(os.path.join(script_directory, "../../../assets"))'
         # Not necessary on Windows
         when: 'not win32'

The effect can be easily seen with the ``--show-source-changes option``
which outputs for modules the changes applied. Notice that we do not do
it on Windows, because there it is not needed. The ``when`` clause
allows us to specify such conditions.

.. code:: diff

   customtkinter.windows.widgets.theme.theme_manager:
   --- original
   +++ modified

   @@ -15,7 +15,7 @@

            script_directory = os.path.dirname(os.path.abspath(__file__))

            if theme_name_or_path in cls._built_in_themes:
   -            with open(os.path.join(script_directory, "../../../assets", "themes", f"{theme_name_or_path}.json"), "r") as f:
   +            with open(os.path.join(os.path.normpath(os.path.join(script_directory, "../../../assets")), "themes", f"{theme_name_or_path}.json"), "r") as f:

The ``normpath`` is limited to where it is needed, to keep the replaced
expression minimal. And in this way, the problem is solved for in a
pretty non-invasive way.

Source modification is of course always something that can break if the
code changes, and should normally be avoided. But it appears this should
be a very robust one.

###############
 Final remarks
###############

I am hoping you will find this very helpful information and will join
the effort to make packaging for Python work out of the box. Adding
support for ``customtkinter`` seems trivial at first, and for Windows in
fact is was.

Lessons learned. Data files working need to be confirmed on either Linux
or macOS too, esp. in case of these relative paths.

We will have to have a repository of test cases for this kind of small
programs, where you can help by checking for new version to still
produce the same compilation report. Then it would be fairly easy to get
the coverage on all platforms and in case of updated packages on PyPI.
