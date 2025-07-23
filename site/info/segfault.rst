:orphan:

###########
 Segfaults
###########

****************************
 The Problem in a Few Words
****************************

The **Nuitka** compiled programs are not supposed to crash with
segfaults, but occasionally some bugs or unexpected circumstances, as
well as third-party C code can cause this.

************
 Background
************

After compilation, the machine code, when making memory accesses, should
stay within the boundaries of memory owned by the process. When
unexpected situations or corruptions occur, then the OS level protection
steps in and stops a program with ``SIGSEGV`` which you have just hit -
if a compiled program to this page pointed you.

*************
 Consequence
*************

There are no easy workarounds, and this will need debugging of the more
challenging kind, but you can still provide good input that will help us
find it.

****************
 Recommendation
****************

Nuitka has a compilation flag ``--debug`` that you should use to compile
your program when this happens. It generates far worse program code,
with a lot of checks added. This will find where the **Nuitka** created
code finds its assumptions are violated. This should turn the "segfault"
into an "assertion" error on the C level, often catching the error where
it first happens, whereas the segfault happens on usage but not when
data was originally corrupted.

What can happen esp. with gcc compilation is that you get warnings like
the following that abort the build in ``--debug``

.. code::

   module.attr.validators.c: In function 'impl_attr$validators$$$function__43___call__':
   module.attr.validators.c:14164:17: error: variable 'tmp_try_except_1__unhandled_indicator' set but not used [-Werror=unused-but-set-variable]
   14164 |     nuitka_bool tmp_try_except_1__unhandled_indicator = NUITKA_BOOL_UNASSIGNED;
       |                 ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Should this happen, use ``--no-debug-c-warnings`` as that is not
typically the issue you are looking for with larger programs, but rather
a sign of non-optimal code. It could also be an indication of the bug we
are looking for. Recompile with that flag then.

Another thing that can happen at runtime (with Python3.12+) is the
following:

.. code::

   Assertion failed: Py_REFCNT((&_Py_NoneStruct)) == _Py_IMMORTAL_REFCNT, file static_src\CompiledFunctionType.c, line 1330

In that case this is often a case of Nuitka detecting corruption of
immortal values, that Nuitka knows about, but observes that this status
has been corrupted. This can be a Nuitka bug, but more often than not,
extension modules like PySide6 and others cause this. These issues are
more or less harmless, and ignored by other packages it seems. Disable
these checks with ``--no-debug-immortal-assumptions`` and see what else
happens.

It's rare that the above step doesn't find bugs in **Nuitka** if that's
where they are. The crash can also be within an extension modules that
you use in standalone mode. It has been observed that missing data files
and missing implicit dependencies are not observed, and in this case,
the C code, lacking checks, can cause all kinds of errors, and is to
blame. Including data files sometimes the solution. Sometimes adding
missing implicit imports is.

***********
 Reporting
***********

If you have a segfault, always make an issue report since these are not
normal, even if you manage to work around them. With ``--debugger``, you
will get a stack output that will be extremely useful. Please also try
to reduce the test case as much as possible. Often, imports of 3rd-party
code will be enough to produce your issue.
