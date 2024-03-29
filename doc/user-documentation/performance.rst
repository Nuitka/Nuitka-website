#############
 Performance
#############

This chapter gives an overview, of what to currently expect in terms of
performance from Nuitka. It's a work in progress and is updated as we
go. The current focus for performance measurements is Python 2.7, but
3.x is going to follow later.

*****************
 pystone results
*****************

The results are the top value from this kind of output, running pystone
1000 times and taking the minimal value. The idea is that the fastest
run is most meaningful, and eliminates usage spikes.

.. code:: bash

   echo "Uncompiled Python2"
   for i in {1..100}; do BENCH=1 python2 tests/benchmarks/pystone.py ; done | sort -rn | head -n 1
   python2 -m nuitka --lto=yes --pgo tests/benchmarks/pystone.py
   echo "Compiled Python2"
   for i in {1..100}; do BENCH=1 ./pystone.bin ; done | sort -n | head -rn 1

   echo "Uncompiled Python3"
   for i in {1..100}; do BENCH=1 python3 tests/benchmarks/pystone3.py ; done | sort -rn | head -n 1
   python3 -m nuitka --lto=yes --pgo tests/benchmarks/pystone3.py
   echo "Compiled Python3"
   for i in {1..100}; do BENCH=1 ./pystone3.bin ; done | sort -rn | head -n 1

+-------------------+-------------------+----------------------+---------------------+
| Python            | Uncompiled        | Compiled LTO         | Compiled PGO        |
+===================+===================+======================+=====================+
| Debian Python 2.7 | 137497.87 (1.000) | 460995.20 (3.353)    | 503681.91 (3.663)   |
+-------------------+-------------------+----------------------+---------------------+
| Nuitka Python 2.7 | 144074.78 (1.048) | 479271.51 (3.486)    | 511247.44 (3.718)   |
+-------------------+-------------------+----------------------+---------------------+

***********************
 Report issues or bugs
***********************

Should you encounter any issues, bugs, or ideas, please visit the
`Nuitka bug tracker <https://github.com/Nuitka/Nuitka/issues>`__ and
report them.

Best practices for reporting bugs:

-  Please always include the following information in your report, for
   the underlying Python version. You can easily copy&paste this into
   your report. It does contain more information than you think. Do not
   write something manually. You may always add, of course,

   .. code:: bash

      python -m nuitka --version

-  Try to make your example minimal. That is, try to remove code that
   does not contribute to the issue as much as possible. Ideally, come
   up with a small reproducing program that illustrates the issue, using
   ``print`` with different results when the program runs compiled or
   native.

-  If the problem occurs spuriously (i.e. not each time), try to set the
   environment variable ``PYTHONHASHSEED`` to ``0``, disabling hash
   randomization. If that makes the problem go away, try increasing in
   steps of 1 to a hash seed value that makes it happen every time,
   include it in your report.

-  Do not include the created code in your report. Given proper input,
   it's redundant, and it's not likely that I will look at it without
   the ability to change the Python or Nuitka source and re-run it.

-  Do not send screenshots of text, that is bad and lazy. Instead,
   capture text outputs from the console.
