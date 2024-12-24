:orphan:

#############
 Performance
#############

This page gives an overview, of what to currently expect in terms of
performance from Nuitka.

*****************
 Pystone Results
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
