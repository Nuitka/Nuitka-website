:orphan:

#############################
 Debian packages with Nuitka
#############################

****************************
 The Problem in a Few Words
****************************

Python from Debian packages is not generally suitable for use on any
other OS, because they are changed such, that they work only on Debian.
Instead create a virtualenv and use a virtualenv with PyPI packages or
Anaconda instead. These are designed to be used on all Linux OSes.

************
 Background
************

Debian and distributions based on it, e.g. Ubuntu and Mint, are
widespread and popular among Linux users, because it's very easy to
install, you get a maintained.

As part of the their goals, Debian wants to remove duplication between
packages, have packages in standard places, and generally clean up
things. As a result, data files are moved to ``/etc``, used DLLs are in
``/usr/lib``, and to make that possible, patches are applied during
packaging to the source.

*********
 Example
*********

This is the change, that Debian does to certifi. The code is changed,
such that a data file is found not near the Python code, like most
Python packages do it, using ``importlib.resources`` but rather a hard
coded path is used.

.. code::

   --- /opt/python3100/lib/python3.10/site-packages/certifi/core.py
   +++ /usr/lib/python3/dist-packages/certifi/core.py
   @@ -8,6 +8,8 @@
   """
   import os

   +DEBIAN_CA_CERTS_PATH = '/etc/ssl/certs/ca-certificates.crt'
   +
   try:
       from importlib.resources import path as get_path, read_text

   @@ -33,8 +35,7 @@
               # We also have to hold onto the actual context manager, because
               # it will do the cleanup whenever it gets garbage collected, so
               # we will also store that at the global level as well.
   -            _CACERT_CTX = get_path("certifi", "cacert.pem")
   -            _CACERT_PATH = str(_CACERT_CTX.__enter__())
   +            _CACERT_PATH = DEBIAN_CA_CERTS_PATH

           return _CACERT_PATH

   @@ -51,10 +52,9 @@
       # If we don't have importlib.resources, then we will just do the old logic
       # of assuming we're on the filesystem and munge the path directly.
       def where():
   -        f = os.path.dirname(__file__)
   -
   -        return os.path.join(f, "cacert.pem")
   +        return DEBIAN_CA_CERTS_PATH


   def contents():
   -    return read_text("certifi", "cacert.pem", encoding="ascii")
   +    with open(where(), "r", encoding="ascii") as data:
   +        return data.read()

*************
 Consequence
*************

Using Debian for standalone to port things to other OSes, means, that
some of the packages will not find the data files. Nuitka would have to
undo the effect of all these patches, making the code portable again.
That is of course not viable.

****************
 Recommendation
****************

For being portable on Linux, generally it is recommended to use a
portable Python distribution.

One way is to use packages from PyPI over system Debian packages, but
still with the Debian python. Nuitka will generally work well with
these, even if in some cases, the latest version may not yet be
supported right after its release. This however leaves you with the
problem, that newest Debian Python will not run on older Linux systems,
so you need to also solve that by building on old Debian, in a chroot,
docker container, pbuilder, etc.

The harder way is to use Anaconda over Debian Python. The advantage
there is that similar to Debian, this has a set of supported packages,
and even though they are usually a bit older, chances are that the
version used there is also already well supported by Nuitka. And
Anaconda will run on older Linux no problem, and therefore standalone
distributions created with it will as well.
