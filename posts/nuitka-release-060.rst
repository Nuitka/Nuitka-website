This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release adds massive improvements for optimization and a couple of
bug fixes.

It also indicates reaching the mile stone of doing actual type inference,
even if only very limited.

And with the new version numbers, lots of UI changes go along. The options
to control recursion into modules have all been renamed, some now have
different defaults, and finally the filenames output have changed.

Bug Fixes
---------

- Python3.5: Fix, the awaiting flag was not removed for exceptions thrown
  into a coroutine, so next time it appeared to be awaiting instead of
  finished.

- Python3: Classes in generators that were using built-in functions crashed
  the compilation with C errors.

- Some regressions for XML outputs from previous changes were fixed.

- Fix, ``hasattr`` was not raising an exception if used with non-string
  attributes.

- For really large compilations, MSVC linker could choke on the input file,
  line length limits, which is now fixed for the inline copy of Scons.

- Standalone: Follow changed hidden dependency of ``PyQt5`` to ``PyQt5.sip``
  for newer versions

- Standalone: Include certificate file using by ``requests`` module in some
  cases as a data file.

New Optimization
----------------

- Enabled C target type ``nuitka_bool`` for variables that are stored with
  boolean shape only, and generate C code for those

- Using C target type ``nuitka_bool`` many more expressions are now handled
  better in conditions.

- Enhanced ``is`` and ``is not`` to be C source type aware, so they can be
  much faster for them.

- Use C target type for ``bool`` built-in giving more efficient code for
  some source values.

- Annotate the ``not`` result to have boolean type shape, allowing for
  more compile time optimization with it.

- Restored previously lost optimization of loop break handling
  ``StopIteration`` which makes loops much faster again.

- Restore lost optimization of subscripts with constant integer values making
  them faster again.

- Optimize in-place operations for cases where left, right, or both sides
  have known type shapes for some values. Initially only a few variants were
  added, but there is more to come.

- When adjacent parts of an f-string become known string constants, join
  them at compile time.

- When there is only one remaining part in an f-string, use that directly
  as the result.

- Optimize empty f-strings directly into empty strings constant during the
  tree building phase.

- Added specialized attribute check for use in re-formulations that doesn't
  expose exceptions.

- Remove locals sync operation in scopes without local variables, e.g. classes
  or modules, making ``exec`` and the like slightly leaner there.

- Remove ``try`` nodes that did only re-raise exceptions.

- The ``del`` of variables is now driven fully by C types and generates more
  compatible code.

- Removed useless double exception exits annotated for expressions of
  conditions and added code that allows conditions to adapt themselves to the
  target shape bool during optimization.

New Features
------------

- Added support for using ``.egg`` files in ``PYTHONPATH``, one of the more
  rare uses, where Nuitka wasn't yet compatible.

- Output binaries in standalone mode with platform suffix, on non-Windows
  that means no suffix. In accelerated mode on non-Windows, use ``.bin`` as a
  suffix to avoid collision with files that have no suffix.

- Windows: It's now possible to use ``clang-cl.exe`` for ``CC`` with Nuitka
  as a third compiler on Windows, but it requires an existing MSVC install
  to be used for resource compilation and linking.

- Windows: Added support for using ``ccache.exe`` and ``clcache.exe``, so that
  object files can now be cached for re-compilation.

- For debug mode, report missing in-place helpers. These kinds of reports are
  to become more universal and are aimed at recognizing missed optimization
  chances in Nuitka. This features is still in its infancy. Subsequent releases
  will add more like these.

Organizational
--------------

- Disabled comments on the web site, we are going to use Twitter instead, once
  the site is migrated to an updated Nikola.

- The static C code is now formatted with ``clang-format`` to make it easier
  for contributors to understand.

- Moved the construct runner to top level binary and use it from there, with
  future changes coming that should make it generally useful outside of Nuitka.

- Enhanced the issue template to tell people how to get the ``develop`` version
  of Nuitka to try it out.

- Added documentation for how use the object caching on Windows to the User
  Manual.

- Removed the included GUI, originally intended for debugging, but XML outputs
  are more powerful anyway, and it had been in disrepair for a long time.

- Removed long deprecated options, e.g. ``--exe`` which has long been the
  default and is no more accepted.

- Renamed options to include plugin files to ``--include-plugin-directory`` and
  ``--include-plugin-files`` for more clarity.

- Renamed options for recursion control to e.g. ``--follow-imports`` to better
  express what they actually do.

- Removed ``--python-version`` support for switching the version during
  compilation. This has only worked for very specific circumstances and has
  been deprecated for a while.

- Removed ``--code-gen-no-statement-lines`` support for not having line
  numbers updated at run time. This has long been hidden and probably would
  never gain all that much, while causing a lot of incompatibilty.

Cleanups
--------

- Moved command line arguments to dedicated module, adding checks was becoming
  too difficult.

- Moved rich comparison helpers to a dedicated C file.

- Dedicated binary and unary node bases for clearer distinction and more
  efficient memory usage of unuary nodes. Unary operations also no longer
  have in-place operation as an issue.

- Major cleanup of variable accesses, split up into multiple phases and all
  including module variables being performed through C types, with no special
  cases anymore.

- Partial cleanups of C type classes with code duplications, there is much
  more to resolve though.

- Windows: The way ``exec`` was performed is discouraged in the ``subprocess``
  documentation, so use a variant that cannot block instead.

- Code proving information about built-in names and values was using not very
  portable constructs, and is now written in a way that PyPy would also like.

Tests
-----

- Avoid using ``2to3`` for basic operators test, removing test of some Python2
  only stuff, that is covered elsewhere.

- Added ability to cache output of CPython when comparing to it. This is to
  allow CI tests to not execute the same code over and over, just to get the
  same value to compare with. This is not enabled yet.

Summary
-------

This release marks a point, from which on performance improvements are likely
in every coming release. The C target types are a major milestone. More C
target types are in the work, e.g. ``void`` is coming for expressions that are
done, but not used, that is scheduled for the next release.

Although there will be a need to also adapt optimization to take full advantage
of it, progress should be quick from here. There is a lot of ground to cover,
with more C types to come, and all of them needing specialized helpers. But
as soon as e.g. ``int``, ``str`` are covered, many more programs are going to
benefiting from this.
