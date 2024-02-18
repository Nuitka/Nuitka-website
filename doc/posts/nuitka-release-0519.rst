.. post:: 2016/02/02 09:04
   :tags: compiler, Python, Nuitka
   :author: Kay Hayen

#######################
 Nuitka Release 0.5.19
#######################

This is to inform you about the new stable release of `Nuitka
<https://nuitka.net>`__. It is the extremely compatible Python compiler,
`"download now" </doc/download.html>`_.

This release brings optimization improvements for dictionary using code.
This is now lowering subscripts to dictionary accesses where possible
and adds new code generation for known dictionary values. Besides this
there is the usual range of bug fixes.

***********
 Bug Fixes
***********

-  Fix, attribute assignments or deletions where the assigned value or
   the attribute source was statically raising crashed the compiler.

-  Fix, the order of evaluation during optimization was considered in
   the wrong order for attribute assignments source and value.

-  Windows: Fix, when ``g++`` is the path, it was not used
   automatically, but now it is.

-  Windows: Detect the 32 bits variant of MinGW64 too.

-  Python3.4: The finalize of compiled generators could corrupt
   reference counts for shared generator objects. Fixed in 0.5.18.1
   already.

-  Python3.5: The finalize of compiled coroutines could corrupt
   reference counts for shared generator objects.

**************
 Optimization
**************

-  When a variable is known to have dictionary shape (assigned from a
   constant value, result of ``dict`` built-in, or a general dictionary
   creation), or the branch merge thereof, we lower subscripts from
   expecting mapping nodes to dictionary specific nodes. These generate
   more efficient code, and some are then known to not raise an
   exception.

   .. code:: python

      def someFunction(a, b):
          value = {a: b}
          value["c"] = 1
          return value

   The above function is not yet fully optimized (dictionary key/value
   tracing is not yet finished), however it at least knows that no
   exception can raise from assigning ``value["c"]`` anymore and creates
   more efficient code for the typical ``result = {}`` functions.

-  The use of "logical" sharing during optimization has been replaced
   with checks for actual sharing. So closure variables that were
   written to in dead code no longer inhibit optimization of the then no
   more shared local variable.

-  Global variable traces are now faster to decide definite writes
   without need to check traces for this each time.

**********
 Cleanups
**********

-  No more using "logical sharing" allowed to remove that function
   entirely.

-  Using "technical sharing" less often for decisions during
   optimization and instead rely more often on proper variable registry.

-  Connected variables with their global variable trace statically avoid
   the need to check in variable registry for it.

-  Removed old and mostly unused "assume unclear locals" indications, we
   use global variable traces for this now.

*********
 Summary
*********

This release aimed at dictionary tracing. As a first step, the value
assign is now traced to have a dictionary shape, and this this then used
to lower the operations which used to be normal subscript operations to
mapping, but now can be more specific.

Making use of the dictionary values knowledge, tracing keys and values
is not yet inside the scope, but expected to follow. We got the first
signs of type inference here, but to really take advantage, more
specific shape tracing will be needed.
