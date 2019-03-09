.. title: Support for portable (standalone) programs
.. slug: support-for-portable-standalone-programs
.. date: 2013/04/07 13:52:44
.. tags: Python,Nuitka,compiler,Windows

This post is about a feature often requested, but so far not available feature of
Nuitka. Please see the page `"What is Nuitka?" </pages/overview.html>`_ for clarification
of what it is now and what it wants to be.

In forums, and in Google, people are looking at a Python compiler, also as a way of
deployment. It should offer what `py2exe <http://www.py2exe.org/>`_ does, allow
installation independent of Python.

Well, for a long time it didn't. But thanks to recent contributions, it's upcoming for the
next release, Nuitka 0.4.3, and it's in the current pre-releases.

It works by adding ``--portable`` to the command line. So this should work for you:

.. code-block:: bash

   nuitka-python --recurse-all --portable your-program.py

Right now, it will create a folder "_python" with DLLs, and "_python.zip" with standard
library modules used along to the "your-program.exe". Copy these to another machine,
without a Python installation, and it will (should) work. Making that statement fully true
may need refinements, as some DLL dependencies might not be defined yet.

.. note::

   We may improve it in the future to meld everything into one executable for even easier
   deployment.

You are more than welcome to experiment with it. To do so, download Nuitka from the `download page </pages/download.html>`_ and give it a roll.

.. note::

   Of course, Nuitka is not about replacing "py2exe" primarily, it's only a side effect of
   what we do. Our major goal is of course to accelerate Python, but surely nobody minds
   achieving the two things at the same time.

And while the post is labeled "Windows", this feature also works for Linux at least too. It's just that the lack of Python installations on client systems is far more widespread on this platform.

To me, as this is from a contributor, it's another sign of Nuitka gaining adoption for
real usage. My personal "py2exe" experience is practically not existing, I have never used
it. And I will only merge the improvements into the Nuitka project as provided by
others. My focus for the time to come is of course the compile time and run time
optimization.
