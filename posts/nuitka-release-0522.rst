This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is mostly an intermediate release on the way to the large goal
of having per module compilation that is cacheable and requires far less memory
for large programs. This is currently in progress, but required many changes
that are in this release, more will be needed.

It also contains a bunch of bug fixes and enhancements that are worth to
be released, and the next changes are going to be more invasive.

Bug Fixes
---------

- Compatibility: Classes with decorated ``__new__`` functions could miss
  out on the ``staticmethod`` decorator that is implicit. It's now applied
  always, unless of course it's already done manually. This corrects an
  issue found with Pandas. Fixed in 0.5.22.1 already.

- Standalone: For at least Python 3.4 or higher, it could happen that the
  locale needed was not importable. Fixed in 0.5.22.1 already.

- Compatibility: Do not falsely assume that ``not`` expressions cannot raise
  on boolean expressions, since those arguments might raise during creation.
  This could lead to wrong optimization. Fixed in 0.5.22.2 already.

- Standalone: Do not include system specific C libraries in the distribution
  created. This would lead to problems for some configurations on Linux in
  cases the glibc is no longer compatible with newer or older kernels.
  Fixed in 0.5.22.2 already.

- The ``--recurse-directory`` option didn't check with decision mechanisms
  for module inclusion, making it impossible to avoid some things.

Optimization
------------

- Introduced specialized constant classes for empty dictionaries and other
  special constants, e.g. "True" and "False", so that they can have more
  hard coded properties and save memory by sharing constant values.

- The "technical" sharing of a variable is only consider for variables that
  had some sharing going in the first place, speeing things up quite a bit
  for that still critical check.

- Memory savings coming from enhanced trace storage are already visible at
  about 1%. That is not as much as the reloading will mean, but still helpful
  to use less overall.


Cleanups
--------

- The global variable registry was removed. It was in the way of unloading
  and reloading modules easily. Instead variables are now attached to their
  owner and referenced by other users. When they are released, these variables
  are released.

- Global variable traces were removed. Instead each variable has a list of the
  traces attached to it. For non-shared variables, this allows to sooner tell
  attributes of those variables, allowing for sooner optimization of them.

- No longer trace all initial users of a variable, just merely if there were
  such and if it constitutes sharing syntactically too. Not only does this
  save memory, it avoids useless references of the variable to functions that
  stop using it due to optimization.

- Create constant nodes via a factory function to avoid non-special instances
  where variants exist that would be faster to use.

- Moved the C string functions to a proper ``nuitka.utils.CStrings`` package
  as we use it for better code names of functions and modules.

- Made ``functions`` and explicit child node of modules, which makes their
  use more generic, esp. for re-loading modules.

- Have a dedicated function for building frame nodes, making it easier to see
  where they are created.

Summary
-------

This release is the result of a couple of months work, and somewhat means that
proper re-loading of cached results is becoming in sight. The reloading of
modules still fails for some things, and more changes will be needed, but with
that out of the way, Nuitka's footprint is about to drop and making it then
absolutely scalable. Something considered very important before starting to
trace more information about values.

This next thing big ought to be one thing that structurally holds Nuitka back
from generating C level performance code with say integer operations.
