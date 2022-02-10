.. post:: 2010/11/23 16:11
   :tags: Nuitka, Python, compiler
   :author: Kay Hayen

####################################
 Nuitka needs you - a call for help
####################################

Hello everybody,

.. admonition:: Update

   Python3 support was added, and has reached 3.3 in the mean time. The
   doctests are extracted by a script indeed. But exception stack
   correctness is an ongoing struggle.

my Python compiler Nuitka has come a long way, and currently I have
little to no time to spend on it, due to day job reasons, so it's going
to mostly stagnate for about 2 weeks from my side. But that's coming to
an end, and still I would like to expand what we currently have, with
your help.

Note: You can check the page `What is Nuitka? </pages/overview.html>`_
for clarification of what it is now and what it wants to be.

As you will see, covering all the CPython 2.6 and 2.7 language features
is already something. Other projects are far, far away from that. But
going ahead, I want to secure that base. And this is where there are
several domains where you can help:

-  Python 3.1 or higher

   I did some early testing. The C/API changed in many ways, and my
   current working state has a couple of fixes for it. I would like
   somebody else to devote some time to fixing this up. Please contact
   me if you can help here, esp. if you are competent in the C/API
   changes of Python 3.1. Even if the CPython 3.1 doesn't matter as much
   to me, I believe the extended coverage from the new tests in its test
   suite would be useful. The improved state is not yet released. I
   would make an release to the person(s) that want to work on it.

-  Doctests support

   I have started to extract the doctests from the CPython 2.6 test
   suite. There is a script that does it, and you basically only need to
   expand it with more of the same. No big issue there, but it could
   find issues with Nuitka that we would like to know. Of course, it
   should also be expanded to CPython 2.7 test suite and ultimately also
   CPython 3.1

-  Exception correctness

   I noted some issues with the stacks when developing with the CPython
   2.7 tests, or now failing 2.6 tests, after some merge work. But what
   would be needed would be tests to cover all the situations, where
   exceptions could be raised, and stack traces should ideally be
   identical for all. This is mostly only accuracy work and the CPython
   test suite is bad at covering it.

All these areas would be significant help, and do not necessarily or at
all require any Nuitka inside knowledge. You should also subscribe the
mailing list (since closed) if you consider helping, so we can discuss
things in the open.

If you choose to help me, before going even further into optimization,
in all likelihood it's only going to make things more solid. The more
tests we have, the less wrong paths we can take. This is why I am asking
for things, which all point into that direction.

Thanks in advance, Kay Hayen
