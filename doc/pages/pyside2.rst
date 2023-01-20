:orphan:

########################
 Nuitka PySide2 support
########################

***********************************************
 Support with baseline PySide2 is only partial
***********************************************

While the ``pyside2`` plugin of Nuitka can workaround some issues PySide
5.15.2.1 has to support compiled methods as callbacks, these are far
from complete. Some programs work, but many do have problems, esp. in
reacting to events.

For this the PySide2 wheels provided by Nuitka commercial contain a
backport of the PySide6 changes made to support compiled code perfectly.
The support of PySide6 is much better, but unfortunately not perfect.
However, all current known bugs with PySide6 do not affect PySide2 as
accessible in Nuitka commercial.

For older PySide2 and just generally, the recommended solution is to use
the wheels as provided by Nuitka commercial. There is no way these
patches will be backported and as a result, we have that backported
patch that will not get released in any other way. This is very
understandable, now that Qt6 is out.

*******************************
 Solution in Nuitka Commercial
*******************************

The patched PySide2 source code and binary wheels for some platforms are
available as part of the the `Nuitka Commercial
</doc/commercial.html>`__ offering.

*************
 Alternative
*************

Otherwise your best bet is to migrate to PySide6 which has excellent
support for Nuitka. Also PyQt6 would work, but PyQt5 unfortunately is
very poorly supported.
