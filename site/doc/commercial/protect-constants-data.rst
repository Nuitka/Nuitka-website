:orphan:

################################
 Protect Program Constants Data
################################

Let's look at how **Nuitka Commercial** protects sensitive data embedded
in your source code. This example will highlight a common vulnerability
in standard Python applications and demonstrate how **Nuitka
Commercial** provides a solution that protects this information.

Here is a simple Python script with a hard-coded secret:

.. code:: bash

   cat important-data-demo.py

.. literalinclude:: important-data-demo.py
   :language: python

When a secret, like an API key, is stored as a string constant directly
in your source code, it is not protected. (Protecting data from separate
`data files <protect-data-files.html>`__ is covered in another section.)
Let's see what happens when we compile this Python file to bytecode:

.. code:: bash

   python -m compileall important-data-demo.py
   # produces e.g. __pycache__/important-data-demo.cpython-39.pyc, depending on Python version

   strings __pycache__/important-data-demo.cpython-39.pyc

.. code::

   SuperSecret
   important-data-demo.py
   getKey
   __main__N)
   __name__
   printr
   <module>

As you can see, the ``.pyc`` file exposes not only program identifiers
like function and argument names, but also the ``SuperSecret`` string
itself. While the ``strings`` command provides a quick look, more
sophisticated tools can easily decode the bytecode and retrieve the
original data as a clean Python object. This clearly shows that standard
Python bytecode offers no real protection for your embedded secrets.

This is where **Nuitka Commercial** comes to the rescue.

.. code:: bash

   # The data-hiding plugin uses whitebox encryption to protect the constant data.
   python -m nuitka --enable-plugin=data-hiding important-data-demo.py
   # produces e.g. important-data.exe, depending on platform

   # No outputs from these
   strings important-data.exe | grep SuperSecret
   strings important-data.exe | grep getKey

With **Nuitka Commercial's** ``data-hiding`` plugin, the result is
completely different. The ``strings`` command finds nothing. The secret
is no longer present in plain text in the file. This plugin, available
with a **Nuitka Commercial** subscription, provides a unique and
powerful level of protection by encrypting your constant data, making it
inaccessible to trivial reverse engineering attempts.

Go `back to Nuitka commercial
</doc/commercial.html#protection-vs-reverse-engineering>`__ overview to
learn about more features or to subscribe to `Nuitka commercial
</doc/commercial.html#pricing>`__.
