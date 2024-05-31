:orphan:

##############################
 Windows Services with Nuitka
##############################

In your code, you do not do anything special. If you have previously
used something like ``win32service``, remove this. Nuitka handles all
interaction with the system for you.

.. code:: python

   try:
       while True:
           # Do your service work here as you would normally do it,
           # of course trying to not busy loop.
           ...
           time.sleep(1)

   except KeyboardInterrupt:
       # Service is being stopped, e.g. shutdown, manual
       # you have a little time for cleanups until getting hard killed.
       ...

The plugin enables the creation of Windows Service executables, which
you can do manually like this:

.. code:: bash

   sc.exe \\myserver create NewService binpath= c:\some_path\NewServ.exe

.. note::

   The created binary also has a hidden parameter ``install`` that will
   delete the existing service (for updates) and create it automatically
   with the binary path set correctly, and therefore it will be
   relatively easy. Extra arguments passed after install become
   arguments passed to the service at run time.

   Every other configuration of the service could be added, but it would
   take work and somebody to fund my time this. For now, this is mainly
   intended for simple use cases and internal automatic testing of the
   plugin.

.. note::

   There are options to force the output of the service to standard
   output and standard error into specified files. For debugging, you
   can specify e.g. ``--windows-force-stdout-spec='%PROGRAM%.out.txt'``
   and ``--windows-force-stderr-spec='%PROGRAM%.err.txt'``. Refer to the
   User Manual of Nuitka for allowed special monikers. Of course,
   absolute paths are allowed too.

The plugin is enabled with ``--enable-plugin=windows-service`` and has a
required parameter ``--windows-service-name`` which will be used as the
service name.

Combine this with ``--windows-company-name`` and ideally all related
options to provide a proper version resource.

.. note::

   The created binary does not run directly anymore, but *only* when
   launched as a Windows service.

Go `back to Nuitka commercial
</doc/commercial.html#special-needs-commercial-only-use-cases>`__
overview to learn about more features or to subscribe to `Nuitka
commercial </doc/commercial.html#pricing>`__.
