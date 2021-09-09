This is to inform you about the new stable release of `Nuitka <https://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is the one that completes the Nuitka "sun rise phase".

All of Nuitka is now released under `Apache License 2.0
<http://www.apache.org/licenses/LICENSE-2.0>`__ which is a very liberal
license, and compatible with basically all Free Software licenses there
are. It's only asking to allow integration, of what you send back, and
patent grants for the code.

In the first phase of Nuitka development, I wanted to keep control over
Nuitka, so it wouldn't repeat mistakes of other projects. This is no
longer a concern for me, it's not going to happen anymore.

I would like to thank Debian Legal team, for originally bringing to my
attention, that this license will be better suited, than any copyright
assignment could be.

***********
 Bug fixes
***********

-  The compiled functions could not be used with ``multiprocessing`` or
   ``copy.copy``. `Issue#19 <http://bugs.nuitka.net/issue19>`__. Fixed
   in 0.3.22.1 already.

-  In-place operations for slices with not both bounds specified crashed
   the compiler. `Issue#36 <http://bugs.nuitka.net/issue36>`__. Fixed in
   0.3.22.1 already.

-  Cyclic imports could trigger an endless loop, because module import
   expressions became the parent of the imported module object.
   `Issue#37 <http://bugs.nuitka.net/issue37>`__. Fixed in 0.3.22.2
   already.

-  Modules named ``proc`` or ``func`` could not be compiled to modules
   or embedded due to a collision with identifiers of CPython2.7
   includes. `Issue#38 <http://bugs.nuitka.net/issue38>`__. Fixed in
   0.3.22.2 already.

**************
 New Features
**************

-  The fix for `Issue#19 <http://bugs.nuitka.net/issue19>`__ also makes
   pickling of compiled functions available. As it is the case for
   non-compiled functions in CPython, no code objects are stored, only
   names of module level variables.

****************
 Organizational
****************

-  Using the Apache License 2.0 for all of Nuitka now.

-  Speedcenter has been re-activated, but is not yet having a lot of
   benchmarks yet, subject to change.

   .. admonition:: Update

      We have given up on speedcenter meanwhile, and generate static
      pages with graphs instead.

***********
 New Tests
***********

-  Changed the "CPython26" tests to no longer disable the parts that
   relied on copying of functions to work, as `Issue#19
   <http://bugs.nuitka.net/issue19>`__ is now supported.

-  Extended in-place assignment tests to cover error cases of `Issue#36
   <http://bugs.nuitka.net/issue36>`__.

-  Extended compile library test to also try and compile the path where
   ``numpy`` lives. This is apparently another path, where Debian
   installs some modules, and compiling this would have revealed
   `Issue#36 <http://bugs.nuitka.net/issue36>`__ sooner.

*********
 Summary
*********

The release contains bug fixes, and the huge step of changing `the
license <http://www.apache.org/licenses/LICENSE-2.0>`__. It is made in
preparation to `PyCON EU <https://ep2012.europython.eu>`__.
