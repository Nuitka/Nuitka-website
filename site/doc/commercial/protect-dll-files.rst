:orphan:

###################
 Protect DLL Files
###################

Your Python application on Windows relies on Dynamic Link Libraries
(DLLs) or shared libraries for essential functionalities. These
include Python extension modules compiled from C/C++/Rust, or
third-party libraries that your program interfaces with. While these
components are crucial for your application's operation, leaving them as
separate, unprotected files on the end-user's system exposes your
software to attacks.

*****************************
 **Nuitka VM** to the Rescue
*****************************

**Nuitka VM**, through its extension of **Nuitka Commercial** (a
distinct product offering), provides a solution to safeguard critical
components.

By embedding your DLLs and Python extension modules directly into the
main executable and running them within a protected virtual machine
environment, these files become significantly harder to access, modify,
or replace.

This protection ensures that your application runs with the intended
libraries, shielding your intellectual property and maintaining the
integrity and security of your deployed software.

.. note::

   The **Nuitka VM** product is not **Nuitka Commercial** and requires a
   separate product purchase and is currently only Windows.


Go `back to Nuitka commercial
</doc/commercial.html#protection-vs-reverse-engineering>`__ overview to
learn about more features or to subscribe to `Nuitka commercial
</doc/commercial.html#pricing>`__.
