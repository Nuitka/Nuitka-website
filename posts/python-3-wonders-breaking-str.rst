That just killed some hope inside of me, breaking code that uses ``str``
ought to be forbidden.

.. admonition:: Update

   Turns out, this only a bug, and not intentional. And the bug is only
   in the doc string, so it's being fixed, and there is no inconsistency
   then any more.

Python 3:

.. code::

   Python 3.2.3 (default, Jun 25 2012, 23:10:56)
   [GCC 4.7.1] on linux2
   Type "help", "copyright", "credits" or "license" for more information.
   >>> print( str.__doc__ )
   str(string[, encoding[, errors]]) -> str

   Create a new string object from the given encoded string.
   encoding defaults to the current default string encoding.
   errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.
   >>> str( string = "a" )
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: 'string' is an invalid keyword argument for this function

Python 2:

.. code::

   Python 2.7.3 (default, Jul 13 2012, 17:48:29)
   [GCC 4.7.1] on linux2
   Type "help", "copyright", "credits" or "license" for more information.
   >>> print str.__doc__
   str(object) -> string

   Return a nice string representation of the object.
   If the argument is a string, the return value is the same object.
   >>> str( object = "a" )
   'a'

I do understand that it's in fact just the old ``unicode`` built-in. In
fact, I made it work like that for Nuitka just now. But there is a
difference, for Python2, it was well behaved.

Python 2:

.. code::

   >>> print unicode.__doc__
   unicode(string [, encoding[, errors]]) -> object

   Create a new Unicode object from the given encoded string.
   encoding defaults to the current default string encoding.
   errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.
   >>> unicode( string = "a" )
   u'a'

Is Python3 supposed to be more clean or what? I think it is not
happening.

|  Yours,
|  Kay Hayen
