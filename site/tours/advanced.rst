:orphan:

.. meta::
   :description: The Nuitka advanced tour: how the Python compiler works inside, its optimizations, and plugin development.
   :keywords: nuitka,advanced,optimization,type inference,plugins,package configuration

######################
 Nuitka Advanced Tour
######################

Dear Python expert,

you know Python well, and you want to know what Nuitka is really doing,
and how to get the most out of it. This tour gives you the short
version, with pointers to the deep documentation.

******************
 How Nuitka works
******************

Nuitka is a source to source compiler. It translates your Python program
into optimized C code, which is then compiled by your system's C
compiler and linked against ``libpython``, so the resulting binary
behaves exactly like CPython.

On top of the translation, Nuitka applies a growing set of
optimizations, including:

-  Constant folding and propagation.

-  Control flow optimizations.

-  Type inference that replaces Python objects with native C types where
   it is provably safe. This is work in progress, with more coming in
   future releases.

-  ``anti-bloat`` work, which replaces slow or unnecessary modules, e.g.
   ``mock`` or test helpers, with fast dummy implementations. This is on
   by default.

The result is usually a noticeable speedup over CPython, without
changing the semantics of your program.

***********************
 Controlling the Build
***********************

You can compile whole programs rather than single files:

.. code:: bash

   python -m nuitka --follow-imports program.py

For non-trivial projects, put the build configuration in
``nuitka-project:`` comment directives at the top of your main program,
so that options, data files, and plugin settings are versioned with the
source. See :doc:`/user-documentation/user-manual` for the syntax.

Nuitka has a plugin system to support packages that need special
handling, e.g. GUI toolkits. Plugins are automatically activated when
Nuitka detects that their target package is used.

********************
 Performance Tuning
********************

-  Use ``--lto=yes`` for link time optimizations.

-  Compile the whole program with ``--follow-imports``.

-  Read :doc:`/user-documentation/performance` for what to expect and
   what to measure.

******************
 Extending Nuitka
******************

-  The package configuration system can describe dependencies, data
   files, and ``anti-bloat`` rules for packages, see
   :doc:`/user-documentation/nuitka-package-config`.

-  Plugins can be written for your own packages.

-  :doc:`/doc/developer-manual` explains the internals for contributors.

.. include:: ../variables.inc
