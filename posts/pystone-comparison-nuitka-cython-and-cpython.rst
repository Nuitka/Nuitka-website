.. post:: 2013/03/04 08:57:10
   :tags: Nuitka, Python
   :author: Kay Hayen

################################################
 PyStone Comparison Nuitka, Cython, and CPython
################################################

As you all know, Nuitka (see `"what is Nuitka?" </pages/overview.html>`_
) has recently completed a milestone. Always short on time, I am not
doing a whole lot of benchmarking yet, and focus on development. But
here is an interesting submission from Dave Kierans (CTO of `iPowow! Ltd
<http://ipowow.com>`_):

.. code::

   ➜  ~  python pystone.py 1000000
   Pystone(1.1) time for 1000000 passes = 10.2972
   This machine benchmarks at 97113.5 pystones/second
   ➜  ~  cython --embed pystone.py;gcc pystone.c -I/usr/include/python2.6 -L /usr/lib/ -lpython2.6 -o ./pystone.cython;./pystone.cython 1000000
   Pystone(1.1) time for 1000000 passes = 8.20789
   This machine benchmarks at 121834 pystones/second
   ➜  ~  nuitka-python pystone.py 1000000
   Pystone(1.1) time for 1000000 passes = 4.06196
   This machine benchmarks at 246187 pystones/second

This is nice result for Nuitka, even if we all *know* that pystone is
not a really good benchmark at all, and that its results definitely do
not translate to other software. It definitely makes me feel good. With
the 0.4.x series kicked off, it will be exciting to see, where these
numbers can indeed go, once Nuitka actually applies standard compiler
techniques.
