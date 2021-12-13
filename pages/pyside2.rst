###############################################
 Support with baseline PySide2 is only partial
###############################################

While PySide 5.15.2 has some patches to support compiled methods as
callbacks, these are far from complete. Some programs work, but many do
have problems in reacting to events.

Therefore upstream support for PySide6 was developed and will be
available in the 6.1 release once made. We will maintain the integration
of Nuitka such that it should be perfect.

But for older PySide2, there is no way these patches will be backported
and as a result, we have a backported patch that will not get released.
This is very understandable, now that Qt6 is out.

################################
 Available in Nuitka Commercial
################################

The patched PySide2 source code and binary wheels for some platforms are
available as part of the the `Nuitka Commercial
</doc/commercial.html>`__ offering.

#############
 Alternative
#############

Otherwise your best bet is to migrate to PySide 6.0 yet, and compile the
``dev`` branch from source and use that instead.
