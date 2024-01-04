:orphan:

##################
 Unwanted Modules
##################

****************************
 The Problem in a few Words
****************************

Some specific modules can cause a lot of dependencies to be pulled in,
and will make compile time and distribution size relatively large. This
might be an explosion in modules count, or it might be DLLs being
included in standalone mode, that should not have to it.

Nuitka wants you to be aware of this, so you are not disappointed from
endless compile time or too large distribution size.

************
 Background
************

This warning is given for ever more modules. The worst offender is e.g.
``IPython`` which will use just about every syntax highlighting,
language parsing, rendering, and what not framework, leading to
compilations that require very long times.

Another end of the spectrum are packages like ``Numba`` that are not
supported for JIT in standalone mode of Nuitka, but still pull in the
dependencies that themselves require huge DLLs, while they are not going
to be usable anyway.

Nuitka follows imports when you say so, and in standalone mode
specifically it is the default to do so. You can exclude specific
packages or modules manually by inhibiting them with
``--nofollow-import-to=module_name``, but that may not work, in which
case, ``anti-bloat`` work is needed to eradicate this kind of imports.
For common packages these exist. You appear to have come across code
that is not yet dealt with.

.. note::

   Checkout the `Nuitka Package Configuration
   <https://nuitka.net/doc/nuitka-package-config.html>`__. page to find
   out how to help with ``anti-bloat`` additions. There are plenty of
   examples, and if you need help, feel free to ask.

*********
 Example
*********

This is an artificial example where we import unittest.

.. code::

   Nuitka-Plugins:WARNING: anti-bloat: Undesirable import of 'unittest' at 'Mini.py:1' encountered. It may slow down compilation.
   Nuitka-Plugins:WARNING:     Complex topic! More information can be found at https://nuitka.net/info/unwanted-module.html

For ``unittest`` the warning is given, because it appears you are
including test code in your compilation, which is never a good thing.
Maybe you forced inclusion of a whole package, which will also pull in
its tests, and you should exclude those then. Maybe you mixed test code
and application code, and it's normal for you. You can disable the
warning for specific ones with options like
``--noinclude-unittest-mode=allow`` that exist for every of these
warnings. Naturally then you are subject to all the disadvantages
mentioned.

*************
 Consequence
*************

While you can ignore these warnings, it's best to at least attempt to
disable the following into the named module. Otherwise the warning can
be disabled or ignored, it is not an error of any kind, just a strong
pointer to get this resolved.

****************
 Recommendation
****************

For best results, you should compile with
``--noinclude-default-mode=error`` and help to get your compilation
error free by removing the problematic imports from 3rd party software
with ``anti-bloat`` contributions.

Alternatively for popular packages, report the issue, and we might do it
for you, but there are guides on how to do this, and ideally you
contribute yourself.

If you do not care, you can add ``--noinclude-unittest-mode=allow`` or
whatever options is triggering this.

If you really do not care, and do not want to see the message you can
disable the mnemonic with ``--nowarn-mnemonic=unwanted-module`` and
carry on, the warning will no longer show itself, but the impact of
including too much in your compilation will persist and new instances
will not be reported.
