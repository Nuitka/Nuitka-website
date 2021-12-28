####################################
 Nuitka needs you - a call for help
####################################

.. admonition:: Update 3

   And the first point has been done too, Python3.3 is now fully
   supported, including ``yield from`` syntax.

.. admonition:: Update 2

   The third point, Windows 64 support has been done as well. Turns out,
   that I do in fact own only Win64 systems, and with MSVC support in
   place, only a few portability fixes were needed.

   Help with the other point, "re-formulation of yield", would still be
   more than welcome, and no signs of progress there yet. So stop
   thinking "you could", enter telling people "you did" mode.

.. admonition:: Update

   The second point, Fibers implementation for Windows, has been done.
   Thanks for the help you people provide. The next release will contain
   it.

Hello everybody,

the Python compiler Nuitka has come an ever longer way, and currently I
have quite a bunch of issues, that I believe could well need your help.
These are all issues of some important and significance, yet self
contained jobs that you may enjoy.

.. note::

   You can check the page `What is Nuitka? </pages/overview.html>`_ for
   clarification of what it is now and what it wants to be.

-  Python 3.3 - reformulation of ``yield from`` needed.

   As you can see, covering all the CPython 2.6, 2.7, and 3.2 language
   features is already something. Also CPython 3.3 is now working on a
   basic level. Other projects are far, far away from that.

   Many language constructs, such as the ``with`` statement are
   re-formulated into other constructs. This makes it possible to work
   with a simple core for optimization, and to reduce the complexity a
   lot. For the ``with`` statement case, it's changed to
   ``try``/``finally`` and ``try``/``except`` statements, together with
   a few temporary variables. Check the Nuitka source of it:

   `ReformulationWithStatements.py
   <http://www.nuitka.net/gitweb/?p=Nuitka.git;a=blob;f=nuitka/tree/ReformulationWithStatements.py;h=2a2d5821e5a511201454e5ae8a7c979d48f04c4a;hb=HEAD>`_

   There is also `descriptions of all these re-formulations in the
   developer manual
   </doc/developer-manual.html#language-conversions-to-make-things-simpler>`_
   so you can see how this is done.

   Now check `PEP 380 <http://www.python.org/dev/peps/pep-0380/>`_ for
   the details of it, and your task would be to come up with a
   re-formulation of ``yield from`` statements to the semantically
   equivalent.

   The benefit is, you are working on a totally self-contained level.
   The re-formulation only needs to use ``ast`` node information, and
   turn that into Nuitka nodes. The problem will be fully solved this
   way.

   And once we have this, we can pronounce CPython3.3 as fully
   supported. So if you would like to see this happen, please join.

-  Windows - MSVC support needs low level code help

   .. admonition:: update

      This is now done.

   The support for MSVC is already mostly there. If you execute the
   environment setting script, and use Nuitka under Windows, it will
   work. The only problem is that for the generator functions, Nuitka is
   using a concept called "Fiber", which is basically just switching C
   stacks, so called co-routines.

   It works great for Linux and UNIX. For Windows, Fibers are currently
   using threads, which wouldn't be as much of a performance problem,
   because they are very lightweight, it is slightly wasteful only.

   But, the bad thing, is with these threads switching and C++
   exceptions used to represent Python exceptions, no combination of
   MSVC options seems to carry the day and keep the exception in the
   current thread. They are caught in the wrong thread, and make
   generators misbehave, crash.

   This is the *only* thing that holds back proper MSVC support at this
   time, and it has been like this for a while. With MinGW, the issue
   does not exist, but MinGW is a stranger to many, and MSVC will be
   more efficient code generation, so we would like to have that.

   So what it takes is somebody familiar with Windows and its ABI, esp.
   register usage to write code that swaps the registers around, so we
   can have multiple C stacks without threads for it too. This may
   involve messing around with exception jump back pointers as well.

   It needs somebody who can handle this and does it for Nuitka, and
   then it would be well supported. It may involve writing some
   assembler code. The job is also very well contained, but also
   requires very specific knowledge, so please join me here. If you
   think you can do this, do it.

-  Windows 64 bit

   I have no access to Win64. I bought many Windows versions, but not
   the Win64 variants so far. I understand that there are CPython builds
   for it, and probably a MinGW matching it, as well as a matching newer
   MSVC, that may work better for C++ exceptions than the one CPython
   2.x is tied to.

   Doing that, you would mostly only have to play around with
   `SingleExe.scons
   <http://www.nuitka.net/gitweb/?p=Nuitka.git;a=blob;f=nuitka/build/SingleExe.scons;h=f32dd2f61293ee6dca3b5b828b30769ea4d00902;hb=HEAD>`_,
   which abstracts the details of it all. One issue you will encounter
   is that Scons needs a Python2, and other small things. This is mostly
   only about porting Nuitka, and could be done by anybody with access
   to Win64 and willing to fiddle around a bit.

So these are 3 different ways you can help Nuitka. Creating the Python
compiler is a huge effort. And if you help it, we will sooner arrive at
its goals. Join the Nuitka mailing list (since closed) or `contact me
<mailto:kay.hayen@gmail.com>`_ directly if you choose to help with any
of these issues.

Wait, actually there is another way you can help. Please spread this
news to people that you believe might be willing to help. And allow me
to plug this, I am doing Nuitka in my spare time. If you feel, you
cannot help, but still would like to support it, you can still `make
donations </pages/donations.html>`_ to allow me to travel to conferences
and spend more time on it myself.

Anyway, it would be great if these 3 things got sorted out. Come and
join me for this grand vision of the Python compiler.

|  Yours,
|  Kay
