This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is again focusing on optimization, this time very heavily on
the generator performance, which was found to be much slower than CPython
for some cases. Also there is the usual compatibility work and improvements
for Pure C support.

Bug Fixes
---------

- Windows: The 3.5.2 coroutine new protocol implementation was using the wrapper
  from CPython, but it's not part of the ABI on Windows. Have our own instead.
  Fixed in 0.5.23.1 already.

- Windows: Fixed second compilation with MSVC failing. The files renamed to be
  C++ files already existed, crashing the compilation. Fixed in 0.5.23.1
  already.

- Mac OS: Fixed creating extension modules with ``.so`` suffix. This is now
  properly determined by looking at the importer details, leading to correct
  suffix on all platforms. Fixed in 0.5.23.1 already.

- Debian: Don't depend on a C++ compiler primarily anymore, the C compiler from
  GNU or clang will do too. Fixed in 0.5.23.1 already.

- Pure C: Adapted scons compiler detecting to properly consider C11 compilers
  from the environment, and more gracefully report things.

Optimization
------------

- Python2: Generators were saving and restoring exceptions, updating the
  variables ``sys.exc_type`` for every context switch, making it really slow,
  as these are 3 dictionary updates, normally not needed. Now it's only doing
  it if it means a change.

- Sped up creating generators, coroutines and coroutines by attaching the
  closure variable storage directly to the object, using one variable size
  allocation, instead of two, once of which was a standard ``malloc``. This
  makes creating them easier and avoids maintaining the closure pointer
  entirely.

- Using dedicated compiled cell implementation similar to ``PyCellObject`` but
  fully under our control. This allowed for smaller code generated, while still
  giving a slight performance improvement.

- Added free list implementation to cache generator, coroutines, and function
  objects, avoiding the need to create and delete this kind of objects in a
  loop.

- Added support for the built-in ``sum``, making slight optimizations to be much
  faster when iterating over lists and tuples, as well as fast ``long`` sum for
  Python2, and much faster ``bool`` sums too. This is using a prototype version
  of a "qiter" concept.

- Provide type shape for ``xrange`` calls that are not constant too, allowing
  for better optimization related to those.

Tests
-----

- Added workarounds for locks being held by Virus Scanners on Windows to our
  test runner.

- Enhanced constructs that test generator expressions to more clearly show the
  actual construct cost.

- Added construct tests for the ``sum`` built-in on various types of ``int``
  containers, making sure we can do all of those really fast.

Summary
-------

This release improves very heavily on generators in Nuitka. The memory allocator
is used more cleverly, and free lists all around save a lot of interactions with
it. More work lies ahead in this field, as these are not yet as fast as they
should be. However, at least Nuitka should be faster than CPython for these kind
of usages now.

Also, proper pure C in the Scons is relatively important to cover more of the
rarer use cases, where the C compiler is too old.

The most important part is actually how ``sum`` optimization is staging a new
kind of approach for code generation. This could become the standard code for
iterators in loops eventually, making ``for`` loops even faster. This will be
for future releases to expand.
