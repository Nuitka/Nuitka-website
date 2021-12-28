While writing `Nuitka </pages/overview.html>`_ I get to see an absurd
amount of CPython code. For a while now, it's also CPython3.2 that I
look at. Checking out ``__future__`` handling, I was surprised the other
day though, this really works:

.. code:: python

   # Python 3.2.3 (default, Jun 25 2012, 23:10:56)
   # [GCC 4.7.1] on linux2
   >>> from __future__ import barry_as_FLUFL
   >>> 1 <> 2
   True
   >>> 1 != 2
     File "<stdin>", line 1
       1 != 2
          ^
   SyntaxError: invalid syntax

It's new in CPython3, and this the code that makes it possible, from the
Python parser:

.. code:: c++

   if (type == NOTEQUAL) {
       if (!(ps->p_flags & CO_FUTURE_BARRY_AS_BDFL) &&
                       strcmp(str, "!=")) {
           PyObject_FREE(str);
           err_ret->error = E_SYNTAX;
           break;
       }
       else if ((ps->p_flags & CO_FUTURE_BARRY_AS_BDFL) &&
                       strcmp(str, "<>")) {
           PyObject_FREE(str);
           err_ret->text = "with Barry as BDFL, use '<>' "
                           "instead of '!='";
           err_ret->error = E_SYNTAX;
           break;
       }
   }

Now who would think bad of that, would you? The fun aspect is, that
Nuitka will easily supports it. By re-using the Python parser, it works
out of the box, I only needed to add the flag value.

For fun, I tried to add a test that confirms - and then notice:

   -  It doesn't really work for CPython3.2 already.
   -  The flag is only used for ``eval`` and ``exec`` and not on the
      same level, so it's only inherited.
   -  And "2to3" kindly removes that flag silently. It probably should
      raise an error.

So yeah, oddities in Python3!
