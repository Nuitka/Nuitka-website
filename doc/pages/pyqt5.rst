######################
 Nuitka PyQt5 support
######################

*********************************************
 Support for PyQt5 is relatively problematic
*********************************************

While the ``pyqt5`` plugin of Nuitka enables using it, there are known
bugs with callbacks and threading. You can workaround them, but they
can be very limiting.

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

Otherwise your best bet is to migrate to PyQt6 (which at this time does
not support Qt threading with Nuitka) or PySide6 (recommended) and use
these, as there are no compatibility issues with these.
