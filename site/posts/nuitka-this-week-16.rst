.. post:: 2025/02/15
   :tags: Python, compiler, Nuitka, NTW
   :author: Kay Hayen

######################
 Nuitka this week #16
######################

Hey Nuitka users! This started out as an idea of a weekly update, but
that hasn't happened, and so we will switch it over to just writing up
when something interesting happens and then push it out relatively
immediately when it happens.

***********************************************************************************
 Nuitka Onefile Gets More Flexible: ``--onefile-cache-mode`` and ``{PROGRAM_DIR}``
***********************************************************************************

We've got a couple of exciting updates to Nuitka's onefile mode that
give you more control and flexibility in how you deploy your
applications. These enhancements stem from real-world needs and
demonstrate Nuitka's commitment to providing powerful and adaptable
solutions.

Taking Control of Onefile Unpacking: ``--onefile-cache-mode``
=============================================================

Onefile mode is fantastic for creating single-file executables, but the
management of the unpacking directory where the application expands has
sometimes been a bit... opaque. Previously, Nuitka would decide whether
to clean up this directory based on whether the path used
runtime-dependent variables. This made sense in theory, but in practice,
it could lead to unexpected behavior and made debugging onefile issues
harder.

Now, you have complete control! The new ``--onefile-cache-mode`` option
lets you explicitly specify what happens to the unpacking directory:

-  ``--onefile-cache-mode=auto``: This is the default behavior. Nuitka
   will remove the unpacking directory unless runtime-dependent values
   were used in the path specification. This is the same behavior as
   previous versions.

-  ``--onefile-cache-mode=cached``: The unpacking directory is *not*
   removed and becomes a persistent, cached directory. This is useful
   for debugging, inspecting the unpacked files, or if you have a use
   case that benefits from persistent caching of the unpacked data. The
   files will remain available for subsequent runs.

-  ``--onefile-cache-mode=temporary``: The unpacking directory *is*
   removed after the program exits.

This gives you the power to choose the behavior that best suits your
needs. No more guessing!

Relative Paths with ``{PROGRAM_DIR}``
=====================================

Another common request, particularly from users deploying applications
in more restricted environments, was the ability to specify the onefile
unpacking directory *relative* to the executable itself. Previously, you
were limited to absolute paths or paths relative to the user's temporary
directory space.

We've introduced a new variable, ``{PROGRAM_DIR}``, that you can use in
the ``--onefile-tempdir-spec`` option. This variable is dynamically
replaced at runtime with the full path to the directory containing the
onefile executable.

For example:

.. code::

   nuitka --onefile --onefile-tempdir-spec="{PROGRAM_DIR}/.myapp_data" my_program.py

This would create a directory named ``.myapp_data`` *inside* the same
directory as the ``my_program.exe`` (or ``my_program`` on Linux/macOS)
and unpack the application there. This is perfect for creating truly
self-contained applications where all data and temporary files reside
alongside the executable.

Nuitka Commercial and Open Source
=================================

These features, like many enhancements to Nuitka, originated from a
request by a Nuitka commercial customer. This highlights the close
relationship between the commercial offerings and the open-source core.
While commercial support helps drive development and ensures the
long-term sustainability of Nuitka, the vast majority of features are
made freely available to all users.

Give it a Try!
==============

This change will be in 2.7 and is currently

We encourage you to try out these new features and let us know what you
think! As always, bug reports, feature requests, and contributions are
welcome on `GitHub <https://github.com/Nuitka/Nuitka/issues>`__.
