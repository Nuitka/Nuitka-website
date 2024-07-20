.. post:: 2024/01/24
   :tags: Python, compiler, Nuitka, package_config
   :author: Kay Hayen

#####################################
 Nuitka Package Configuration Part 3
#####################################

This is the third part of a post series under the tag `package_config
<https://nuitka.net/blog/tag/package_config.html>`__ that explains the
Nuitka Package Configuration in more detail. To recap, Nuitka package
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
this case, we are talking about the package ``toga``.

Problems like with this package are typically encountered in standalone
mode only, but they also affect accelerated mode, since it doesn't
compile all the things desired in that case. Some packages, and in this
instance look at what OS they are running on, environment variables,
etc. and then in a relatively static fashion, but one that Nuitka cannot
see through, loads a what it calls "backend" module.

We are going to look at that in some detail, and will see a workaround
applied with the ``anti-bloat`` engine doing code modification on the
fly that make the choice determined at compile time, and visible to
Nuitka is this way.

#################
 Initial Symptom
#################

The initial symptom reported was that ``toga`` did suffer from broken
version lookups and therefor did not work, and we encountered even two
things, that prevented it, one was about the version number. It was
trying to do ``int`` after resolving the version of toga by itself to
``None``.

.. code::

   Traceback (most recent call last):
     File "C:\py\dist\toga1.py", line 1, in <module>
     File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
     File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
     File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
     File "C:\py\dist\toga\__init__.py", line 1, in <module toga>
     File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
     File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
     File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
     File "C:\py\dist\toga\app.py", line 20, in <module toga.app>
     File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
     File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
     File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
     File "C:\py\dist\toga\widgets\base.py", line 7, in <module toga.widgets.base>
     File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
     File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
     File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
     File "C:\py\dist\travertino\__init__.py", line 4, in <module travertino>
     File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
     File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
     File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
     File "C:\py\dist\setuptools_scm\__init__.py", line 7, in <module setuptools_scm>
     File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
     File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
     File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
     File "C:\py\dist\setuptools_scm\_config.py", line 15, in <module setuptools_scm._config>
     File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
     File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
     File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
     File "C:\py\dist\setuptools_scm\_integration\pyproject_reading.py", line 8, in <module setuptools_scm._integration.pyproject_reading>
     File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
     File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
     File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
     File "C:\py\dist\setuptools_scm\_integration\setuptools.py", line 62, in <module setuptools_scm._integration.setuptools>
     File "C:\py\dist\setuptools_scm\_integration\setuptools.py", line 29, in _warn_on_old_setuptools
   ValueError: invalid literal for int() with base 10: 'unknown'

So, this is clearly something that we consider bloat in the first place,
to runtime lookup your own version number. The use of ``setuptools_scm``
is implying the use of setuptools, for which the version cannot be
determined, and that's crashing.

#######################################
 Step 1 - Analysis of initial crashing
#######################################

So first thing, we did was to repair ``setuptools``, to know its
version. It is doing it a bit different, because it cannot use itself.
Our compile time optimization failed there, but also would be overkill.
We never came across this, since we avoid ``setuptools`` very hard
normally, but it's not good to be incompatible.

.. code:: yaml

   - module-name: 'setuptools.version'
     anti-bloat:
       - description: 'workaround for metadata version of setuptools'
         replacements:
           "pkg_resources.get_distribution('setuptools').version": "repr(__import__('setuptools.version').version.__version__)"

We do not have to include all metadata for ``setuptools`` here, just to
get that one item, so we chose to make a simple string replacement here,
that just looks the value up at compile time and puts it into the source
code automatically. That removes the
``pkg_resources.get_distribution()`` call entirely.

With that, ``setuptools_scm`` was not crashing anymore. That's good. But
we don't really want it to be included, since it's good for dynamically
detecting the version from git, and what not, but including the
framework for building C extensions, not a good idea in the general
case. Nuitka therefore said this:

.. code::

   Nuitka-Plugins:WARNING: anti-bloat: Undesirable import of 'setuptools_scm' (intending to
   Nuitka-Plugins:WARNING: avoid 'setuptools') in 'toga' (at
   Nuitka-Plugins:WARNING: 'c:\3\Lib\site-packages\toga\__init__.py:99') encountered. It may
   Nuitka-Plugins:WARNING: slow down compilation.
   Nuitka-Plugins:WARNING:     Complex topic! More information can be found at
   Nuitka-Plugins:WARNING: https://nuitka.net/info/unwanted-module.html

So that's informing the user to take action. And in the case of optional
imports, i.e. ones where using code will handle the ``ImportError`` just
fine and work without it, we can use do this.

.. code:: yaml

   - module-name: 'toga'
     anti-bloat:
       - description: 'remove setuptools usage'
         no-auto-follow:
           'setuptools_scm': ''
         when: 'not use_setuptools'

He we say, no **not** automatically follow ``setuptools_scm`` reports,
**unless** there is other code that still does it. In that way, the
import still happens if some other part of the code imports the module,
but only then. We no longer enforce the non-usage of a module here, we
just make that decision based on other uses being present.

With this the bloat warning, and the inclusion of ``setuptools_scm``
into the compilation is removed, and you always want to make as small as
possible and remove those packages that do not contribute anything but
overhead, aka bloat.

The next thing discovered was that ``toga`` needs the ``toga-core``
distribution to version check. For that, we use the common solution, and
tell that we want to include the metadata of it, for when ``toga`` is
part of a compilation.

.. code:: yaml

   - module-name: 'toga'
     data-files:
       include-metadata:
         - 'toga-core'

So that moved the entire issue of version looks to resolved.

#####################################
 Step 2 - Dynamic Backend dependency
#####################################

Now on to the backend issue. What remained was a need for including the
platform specific backend. One that can even be overridden by an
environment variable. For full compatibility, we invented something new.
Typically what we would have done is to create a toga plugin for the
following snippet.

.. code:: yaml

   - module-name: 'toga.platform'
     variables:
       setup_code: 'import toga.platform'
       declarations:
         'toga_backend_module_name': 'toga.platform.get_platform_factory().__name__'
     anti-bloat:
       - change_function:
           'get_platform_factory': "'importlib.import_module(%r)' % get_variable('toga_backend_module_name')"

There is a whole new thing here, a new feature that was added
specifically for this to be easy to do. And with the backend selection
being complex and partially dynamic code, we didn't want to hard code
that. So we added support for ``variables`` and their use in Nuitka
Package Configuration.

The first block ``variables`` defines a mapping of expressions in
``declarations`` that will be evaluated at compile time given the setup
code under ``setup_code``.

This then allows us to have a variable with the name of the backend that
``toga`` decides to use. We then change the very complex function
``get_platform_factory`` that we used used, for compilation, to be
replacement that Nuitka will be able to statically optimize and see the
backend as a dependency and use it directly at run time, which is what
we want.

###############
 Final remarks
###############

I am hoping you will find this very helpful information and will join
the effort to make packaging for Python work out of the box. Adding
support for ``toga`` was a bit more complex, but with the new tool, once
identified to be that kind of backend issue, it might have become a lot
more easy.

Lessons learned. We should cover packages that we routinely remove from
compilation, like setuptools, but e.g. also IPython. This will have to
added, such that ``setuptools_scm`` cannot cloud the vision to actual
issues.
