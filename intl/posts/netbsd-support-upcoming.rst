.. post:: 2013/04/06 12:58:37
   :tags: Python, Nuitka
   :author: Kay Hayen

#########################
 NetBSD support upcoming
#########################

My first real UNIX ever was a NetBSD. That was now about 22 years ago. I
am still sentimental about it. I had installed it last about 8 years
ago. And I still like it. Back in the days, it was the first UNIX to
encounter for me, running on Amiga hardware, first of a friend, then on
my own.

Recently, there had been support for Nuitka on FreeBSD added. A lot of
people use it on the web, and some want to use Nuitka to improve their
Python performance, so this is kind of relevant.

There were issues resolved, but in the end, something was with Clang on
FreeBSD 8, that I could for the life of it, not resolve remotely. So I
attempted to install it myself. Using "virt-install", these things are a
breeze now. I had already done it with CentOS6 before to test the RPM
repositories of Nuitka. That "virt-install" is a wonderful thing by
itself, making virtualisation somewhat useful. It's only a pity, that I
can't just install other qemu support architectures. I would love to
checkout Nuitka on PowerPC.

.. note::

   If you could check out Nuitka on other Linux architectures than
   x86_64, x86, or arm, that would be great.

This is the report of getting NetBSD supported. It was a quite an
interesting story that I would like to share with you.

Naivly I was assuming, that it would be just for fun, and that Nuitka
will work right away. Little did I know.

On FreeBSD 9 the minimal install medium was chosen, and entered its
ports collection, installed git, cloned Nuitka, and ran the tests,
successfully right away. Now that is unfair, in the Nuitka there were
tons of "Linuxism" already removed. In fact, it had to work, and on the
newest FreeBSD (version 9.1) and then it did. Great!

.. note::

   If you would like to add Nuitka to FreeBSD's ports, please do so. It
   should be really easy now.

On NetBSD, things were unfortunately a little different. I also chose
minimal system. After going through "pkg source" boot strap and git
install, I cloned Nuitka, and then tried to start it. First off, it
couldn't locate "python" at all. I am using ``/usr/bin/env python``
already. But Python2 was on the system. I ended up creating the "python"
link myself. What I should have done according to "#netbsd" is to
install the software, and indeed, ``python2.7 setup.py install`` gives
an installation of Nuitka that is executable.

Next up, you need to know about "Fibers" in Nuitka. These are used for C
co-routines, used to implement Python generators. They have an
interface, that is very close to ``makecontext``/``swapcontext``
routines in C.

For ARM and x86_64 Linux we have optimized code, that switches faster,
but other platforms, including x86 Linux, use the generic
implementation, also because it normally is very fast already.

Now you have to know that since 2001 the interface is deprecated and
shall not be used. And next up, is that on NetBSD, ``makecontext`` gave
a segfault only. So I ran to "#netbsd" and asked.

Now that was a very friendly experience. Of course, I had to give a
rationale for using an obsolete interface. It's not quite obvious, why
threads wouldn't be a better choice. And maybe they are, but they
definitely have more overhead associated, and if they never run at the
same time, why use them.

Ultimately it helped to point out, that for a user of 22 years, an
interface that is only obsolete for 11 years, is not quite as horrifying
as for others.

And they helped me through it. And it turns out, funny thing. For the
context to setup, you are allocating a stack to use for the C routine,
and you "get" the current context, then you make a new one. All the
examples have a certain order of doing it. And my code did it the other
way around. No system but NetBSD noticed.

On FreeBSD and Linux, it didn't matter. But it seems, that the needed
``getcontext`` call was overwriting my stack pointer now with the
current stack. And ``makecontext`` deeply hated that, a lot. It was
preparing that stack to be used, while it was in usage. Doesn't sound
like a good task to give to it, right? My fault truly, because every
example on every man page, on all systems, was doing it differently. But
then they were also all using arrays from the local stack, so quite
obviously that was not real code.

So that was fixed, and all good? No! Next thing was it crashed when
``free`` happened in Python on a compiled frame object, in a later part
of a test that heavily uses generators. Turns out, ``malloc``
information was corrupted. I had to suspect the generic "Fiber" code,
but that took me a while to figure out.

And how could my simple ``malloc`` and ``free`` do that, and make it
happen. When I knew that a context would not longer be used (the
generator has finished, the generator object deleted, etc), I would look
at the context handle stack pointer and free it.

But that pointer changed. Something totally unexpected (by me
obviously), but it also explains the earlier problem. For all systems, I
had used so far, this pointer was not being changed, and remained the
same. So I could ``free`` it from there. It worked fine, but not on
NetBSD. And it wasn't correct anywhere.

It seems NetBSD is doing something clever, since instead of saving the
stack pointer register in a separate area, it saves it to that place
originally specified. It's quite obviously an improvement, in that you
save the pointer.

It's only bad, that now to make up for this savings, I have added the
pointer in a separate field, which won't be changed, so I can free it
again. If one needs it again, and that's not unlikely, you have to
remember it elsewhere. So maybe that idea is not that clever. But it
surely was wrong by me to assume that the provided value would not be
touched.

So, these are 2 bugs it found. The wrong order of calls. And the usage
of a pointer, that may have been changed. This can only help with other
systems, or possibly architectures under Linux.

While this is all description of nasty problems, it's also the report of
the solution, and it was big fun. I would also like to compliment
"#netbsd" for being very helpful and friendly with my porting of Nuitka.
I highly enjoyed doing so. It was a lot of fun. I know that it's
probably on a very tiny amount of people that uses both NetBSD and
Nuitka, but still.

If this Nuitka project were about market share, it wouldn't exist. And I
can work for market share on another day.
