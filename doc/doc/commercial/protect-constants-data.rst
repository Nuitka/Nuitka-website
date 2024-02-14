:orphan:

################################
 Protect Program Constants Data
################################

Consider this example information, to learn what this is about. Only Nuitka
commercial offers the full protection, and this illustrates the issue
with standard Python the best.

.. code:: bash

   cat important-data-demo.py

.. literalinclude:: important-data-demo.py
   :language: python

Key is contained in the source code (separate file is dealt with in
another part), and literally unprotected due to that. Lets turn it to
bytecode:

.. code:: bash

   python -m compileall important-data-demo.py
   # produces e.g. __pycache__/important-data-demo.cpython-39.py, depending on Python version

   strings __pycache__/important-data-demo.cpython-39.pyc

.. code::

   SuperSecret
   important-data-demo.py
   getKey
   __main__N)
   __name__
   printr
   <module>

So not only are all program identified, argument names, also the string
value that is our secret contained in the ``.pyc`` file. There are
better ways to decode a bytecode file, that will give the data in clear
form as a Python object, but at this point it should be clear, the
bytecode object offers no protection for your data there. Nuitka
Commercial to the rescue.

.. code:: bash

   # The data-hiding plugin uses whitebox encryption to protect the constant data.
   python -m nuitka --enable-plugin=data-hiding important-data-demo.py
   # produces e.g. important-data.bin, depending on platform

   # No output
   strings important-data.bin | grep SuperSecret

For Nuitka commercial, the output is empty. Without that plugin, the
string will be found. The plugin is part of the Nuitka Commercial
subscription and unique in this level of protection.

Go `back to Nuitka commercial
</doc/commercial.html#protection-vs-reverse-engineering>`__ overview to
learn about more features or to subscribe to `Nuitka commercial
</doc/commercial.html#pricing>`__.
