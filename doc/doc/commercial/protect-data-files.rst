:orphan:

*************************************
 Protect Program Constants Data
*************************************

Your program might be using Qt and QML, or data files loaded. With Nuitka Commercial,
you can product (even before onefile) an executable that contains them and then also
covers it under the regular `constants data protection <protect-constants-data.html>`__
automatically.

Your program uses standard Python mechanisms from ``pkgutil``, ``pkg_resources``,
``importlib.resources`` or ``importlib_resources`` and generally similar packages,
and these load the data as a file or a stream from within the binary without ever
hitting the disk.

All of this is happening with the same code base, i.e. you are not making any
modification (if at all), that is incompatible with Python. Your code will still
run directly. One thing you do have to change though is to not use ``open`` with
paths created from ``__file__``, but the above code is more elegant anyway, as
it does this for you in the normal case, but can easily be hooked by Nuitka.

This means, e.g. rather than this program

.. code::

    PySideQmlPolarchartTest.py
    qmlpolarchart/
        Example-Icon.png
        Example-Icon.svg
        main.qml
        View1.qml
        View2.qml
        View3.qml

you get a file layout just simply like this

.. code::

    PySideQmlPolarchartTest.exe

Due to constant data protection, the contents of the files will be inaccessible to
anything but the program, and this is very much what people want.

In standard Nuitka, you end up with something like this. And note, that onefile mode
is merely a self extracting archive, i.e. these files will be on the customer
disk for inspection:

.. code::

    PySideQmlPolarchartTest.exe
    qmlpolarchart/
        Example-Icon.png
        Example-Icon.svg
        main.qml
        View1.qml
        View2.qml
        View3.qml

.. note::

    For extension modules and DLLs used, this doesn't affect things. This is about
    merely about data files. This is where onefile comes in and hides these from
    the view and need for deployment, but it cannot replace Nuitka commercial and
    its inclusion of data files inside the main binary.

Go `back to Nuitka commercial </doc/commercial.html#protection-vs-reverse-enginneering>`__ overview to
learn about more features or to subscribe to `Nuitka commercial </doc/commercial.html#pricing>`__.