:orphan:

###############################################
 macOS cross Compilation to x86_64 with Nuitka
###############################################

****************************
 The Problem in a Few Words
****************************

Python on macOS runs on 2 arches, x86_64 and arm. From CPython there is
a ``universal`` binary, which can run on either one. On PyPI there are
binary packages, which run on only one of them, and you may also install
packages, which then will not build universal binaries, but ones for
your host architecture. These are not suitable for deployment unless
manually checked and corrected.

************
 Background
************

Then macOS switched the CPU platform, this was done in a way such that
binaries can support both platforms. You can call these "fat" or
universal. Every user has a given architecture and the macOS picks the
part of the binary that works for them.

On some machines, specifically ``x86_64`` machines, it is important that
the CPU is supported. On ``arm64`` there is Rosetta which allows to
emulate the old CPU, so code available only for that CPU can still run,
but the other way around, does not exist.

*********
 Example
*********

So how does this affect you. Well, you might be running a Python
installation, where e.g. the ``cryptography`` package is not actually
working on ``x86_64``.

This is an example of a terrible stack trace given, that is totally
misleading:

.. code::

   ./Mini.dist/Mini.bin
   ModuleNotFoundError: No module named '_cffi_backend'
   thread '<unnamed>' panicked at 'Python API call failed', /Users/runner/.cargo/registry/src/index.crates.io-6f17d22bba15001f/pyo3-0.18.3/src/err/mod.rs:790:5
   note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
   Traceback (most recent call last):
     File "/Users/hayen/repos/Py2C/Mini.dist/Mini.py", line 1, in <module>
     File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
     File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
     File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
     File "/Users/hayen/repos/Py2C/Mini.dist/cryptography/exceptions.py", line 9, in <module cryptography.exceptions>
     File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
     File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
     File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
   pyo3_runtime.PanicException: Python API call failed

*************
 Consequence
*************

When you try to cross compile on macOS, the best is to first make sure
your program runs with ``arch -x86_64 python main.py`` and fix and
issues that come up.

****************
 Recommendation
****************

Sticking with CPython which is best supported and should give best
portability to older macOS, can also be harder. It seems that using
``arch -x86_64 python -m pip install ...`` in a dedicated virtualenv
only used to do the cross compile may allow you easy testing, and
eradicates the issue entirely.

You still get to test your program with Python on both arches, but you
always had to do that. And unfortunately, increasingly it's likely that
newer PyPI packages will just not work properly on ``x86_64``. More and
more, people will stop caring about the old systems and break things
without noticing and notice.
