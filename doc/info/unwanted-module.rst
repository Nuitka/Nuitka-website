:orphan:

##################
 Unwanted Modules
##################

****************************
 The Problem in a Few Words
****************************

Some specific modules have a lot of dependencies, which then become part
of the compilation. That will make compile time much longer and
distribution size much bigger than necessary. The time increases might
be due to an explosion in module count. DLLs from unwanted modules can
also cause an increase in size.

Nuitka wants you to be aware of the issue so you are not disappointed by
too long of a compile-time or too large of a distribution size.

************
 Background
************

**Nuitka** gives this warning for some modules only. The worst offender
currently is ``IPython`` which will use just about every syntax
highlighting, language parsing, rendering, and more frameworks, leading
to a compilation that takes a very long time. However, many packages
import ``IPython`` and offers ways to integrate with it.

Another example is ``Numba``. **Nuitka** does not support its JIT in
standalone mode of **Nuitka**, but still pull in the dependencies that
themselves require huge DLLs, while they are not going to be usable
anyway.

Nuitka follows imports when you say so, and in standalone mode
specifically, it is the default to do so. You can exclude specific
packages or modules manually by inhibiting them with
``--nofollow-import-to=module_name``, but that may not work, in which
case, ``anti-bloat`` work is needed to eradicate this kind of imports.
For common packages, these exist.

You appear to have come across code that is not yet dealt with.

.. note::

   Checkout the `Nuitka Package Configuration
   <https://nuitka.net/doc/nuitka-package-config.html>`__. page to find
   out how to help with ``anti-bloat`` additions. There are plenty of
   examples; if you need help, feel free to ask.

*********
 Example
*********

Here is an example output where we import ``unittest`` to demonstrate the
issue.

.. code::

   Nuitka-Plugins:WARNING: anti-bloat: Undesirable import of 'unittest' at 'Mini.py:1' encountered. It may slow down compilation.
   Nuitka-Plugins:WARNING:     Complex topic! More information can be found at https://nuitka.net/info/unwanted-module.html

For ``unittest`` **Nuitka** gives the warning, because it appears you are
including test code in your compilation, which is never a good thing. Often
it has extra dependencies, and it can be a lot of code too.

Maybe you forced the inclusion of a whole package, which will also pull in
its tests, and you should exclude those then. Perhaps you mixed test code
and application code, and it's normal for you. You can turn off the
warning for specific ones with options like
``--noinclude-unittest-mode=allow`` that exists for each of these
warnings. Naturally, you are subject to all the disadvantages
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
