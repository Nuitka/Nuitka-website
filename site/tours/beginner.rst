:orphan:

.. meta::
   :description: The Nuitka beginner tour: what the Python compiler is and how to create your first executable.
   :keywords: nuitka,beginner,getting started,first steps,python compiler

######################
 Nuitka Beginner Tour
######################

Dear Python beginner,

you are new to Python, and maybe new to compilers too. This tour shows
you, without much jargon, what Nuitka can do for you and how to get
started. If you get stuck at any point, there is a community of
volunteers that is happy to help.

****************
 What is Nuitka
****************

Nuitka is a compiler for Python programs. Normally, a Python program
needs Python installed to run, and it runs directly from your source
files. Nuitka translates your program into a real executable, like the
programs you download from the internet, that runs on its own.

For you as a beginner, this has two nice effects:

-  Your program becomes faster.

-  You can give your program to other people, and they do not need
   Python at all.

Nuitka supports |SUPPORTED_PYTHONS|.

*************
 First Steps
*************

Install Nuitka:

.. code:: bash

   python -m pip install -U Nuitka

Then check that it works:

.. code:: bash

   python -m nuitka --version

Now take a small program, e.g. ``hello.py``:

.. code:: python

   def main():
       print("Hello World")


   if __name__ == "__main__":
       main()

Compile it:

.. code:: bash

   python -m nuitka --mode=onefile hello.py

You now have a ``hello`` executable (``hello.exe`` on Windows) next to
your source file. Run it, and that is your program, compiled.

.. note::

   The first compilation can take a while, because Nuitka uses a C
   compiler under the hood. The next ones will be much faster.

**************
 Getting Help
**************

-  :doc:`/user-documentation/tutorial-setup-and-build` explains the
   setup in more detail, e.g. how to get a C compiler on Windows.

-  :doc:`/pages/support` lists the chat rooms and the issue tracker. The
   volunteers on the `Discord server <https://discord.gg/nZ9hr9tUck>`_
   help with first steps and questions.

-  :doc:`/user-documentation/common-issue-solutions` covers typical
   problems.

.. include:: ../variables.inc
