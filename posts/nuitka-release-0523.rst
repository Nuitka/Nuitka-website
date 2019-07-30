This is to inform you about the new stable release of `Nuitka <http://nuitka.net>`_. It is the extremely compatible Python compiler. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for an overview.

This release is focusing on optimization, the most significant part for the
users being enhanced scalability due to memory usage, but also break through
structural improvements for static analysis of iterators and the debut of
type shapes and value shapes, giving way to "shape tracing".

Bug Fixes
---------

- Fix support Python 3.5.2 coroutine changes. The checks got added for
  improved mode for older 3.5.x, the new protocol is only supported when
  run with that version or higher.

- Fix, was falsely optimizing away unused iterations for non-iterable compile
  time constants.

  .. code-block:: python

    iter(1) # needs to raise.

- Python3: Fix, ``eval`` must not attempt to ``strip`` memoryviews. The was
  preventing it from working with that type.

- Fix, calling ``type`` without any arguments was crashing the compiler. Also
  the exception raised for anything but 1 or 3 arguments was claiming that only
  3 arguments were allowed, which is not the compatible thing.

- Python3.5: Fix, follow enhanced error checking for complex call handling of
  star arguments.

- Compatibility: The ``from x import x, y`` re-formulation was doing two
  ``__import__`` calls instead of re-using the module value.

Optimization
------------

- Uses only about 66% of the memory compared to last release, which is
  very important step for scalability independent of re-loading. This
  was achieved by making sure to break loop traces and their reference
  cycle when they become unused.

- Properly detect the ``len`` of multiplications at compile time from
  newly introduces value shapes, so that this is e.g. statically optimized.

  .. code-block:: python

    print(len("*" * 10000000000))

- Due to newly introduced type shapes, ``len`` and ``iter`` now properly
  detect more often if values will raise or not, and warn about detected
  raises.

  .. code-block:: python

     iter(len((something)) # Will always raise

- Due to newly introduced "iterator tracing", we can now properly detect if
  the length of an unpacking matches its source or not. This allows to remove
  the check of the generic re-formulations of unpackings at compile time.

  .. code-block:: python

     a, b = b, a    # Will never raise due to unpacking
     a, b = b, a, c # Will always raise, 3 items cannot unpack to 2

- Added support for optimization of the ``xrange`` built-in for Python2.

- Python2: Added support for ``xrange`` iterable constant values, pre-building
  those constants ahead of time.

- Python3: Added support and ``range`` iterable constant values, pre-building
  those constants ahead of time. This brings optimization support for Python3
  ranges to what was available for Python2 already.

- Avoid having a special node variange for ``range`` with no arguments, but
  create the exception raising node directly.

- Specialized constant value nodes are using less generic implementations to
  query e.g. their length or iteration capabilities, which should speed up
  many checks on them.

- Added support for the ``format`` built-in.

- Python3: Added support for the ``ascii`` built-in.

Organizational
--------------

- The movement to pure C got the final big push. All C++ only idoms of C++ were
  removed, and everything works with C11 compilers. A C++03 compiler can be
  used as a fallback, in case of MSVC or too old gcc for instance.

- Using pure C, MinGW64 6x is now working properly. The latest version had
  problems with ``hypot`` related changes in the C++ standard library. Using
  C11 solves that.

- This release also prepares Python 3.6 support, it includes full language
  support on the level of CPython 3.6.0b1.

- The CPython 3.6 test suite was run with Python 3.5 to ensure bug level
  compatibility, and had a few findings of incompatibilities.

Cleanups
--------

- The last holdouts of classes in Nuitka were removed, and many idioms of C++
  were stopped using.

- Moved range related helper functions to a dedicated include file.

- Using ``str is not bytes`` to detect Python3 ``str`` handling or
  actual ``bytes`` type existence.

- Trace collections were using a mix-in that was merged with the base
  class that every user of it was having.

Tests
-----

- Added more static optimization tests, a lot more has become feasible to
  decide at run time, and is now done. These are to detect regressions in
  that domain.

- The CPython 3.6 test suite is now also run with CPython 3.5 which found
  some incompatibilities.

Summary
-------

This release marks a huge step forward. We are having the structure for type
inference now. This will expand in coming releases to cover more cases, and
there are many low hanging fruits for optimization. Specialized codes for
variable versions of certain known shapes seems feasible now.

Then there is also the move towards pure C. This will make the backend
compilation lighter, but due to using C11, we will not suffer any loss of
convenience compared to "C-ish". The plan is to use continue to use C++ for
compilation for compilers not capable of supporting C11.

The amount of static analysis done in Nuitka is now going to quickly expand,
with more and more constructs predicted to raise errors or simplified. This
will be an ongoing activity, as many types of expressions need to be enhanced,
and only one missing will not let it optimize as well.

Also, it seems about time to add dedicated code for specific types to be as
fast as C code. This opens up vast possibilities for acceleration and will
lead us to zero overhead C bindings eventually. But initially the drive is
towards enhanced ``import`` analysis, to become able to know the precide module
expected to be imported, and derive type information from this.

The coming work will attack to start whole program optimization, as well as
enhanced local value shape analysis, as well specialized type code generation,
which will make Nuitka improve speed.
