######################
 Nuitka PyQt5 support
######################

*********************************************
 Support for PyQt5 is relatively problematic
*********************************************

While the ``pyqt5`` plugin of Nuitka enables using it, there are known
bugs with callbacks and threading.

can workaround some issues PySide 5.15.2.1 has to support compiled
methods as callbacks, these are far from complete. Some programs work,
but many do have problems, esp. in reacting to events.

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

********************************************
 Solution in Nuitka Commercial with PySide2
********************************************

The patched PySide2 source code and binary wheels for some platforms are
available as part of the the `Nuitka Commercial
</doc/commercial.html>`__ offering. The PySide2 and PyQt5 are most
similar and might be the easiest way out.

*************
 Alternative
*************

Otherwise your best bet is to migrate to PyQt6 or PySide6 (recommended)
and use these, there are no compatibility issues with these.
