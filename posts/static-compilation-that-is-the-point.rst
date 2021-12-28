########################################
 Static Compilation - That is the point
########################################

In a recent post, Stefan Behnel questioned the point of static
compilation and suggests that in order to be useful, a static compiler
**needs** to add something on top.

This is going to be a rebuttal.

**************************
 Compatibility, I mean it
**************************

First of all, let me start out, by saying that Nuitka is intended to be
the fully optimizing compiler of Python. The optimizing part is not yet
true. Right now, it's probably a correct compiler of Python. Correct in
the sense that it's compatible to CPython as far as possible.

As examples of what I mean with compatibility:

-  Nuitka will hold references to local variables of frames, when an
   exception is raised, and will release them only once the next
   exception is raised.

-  Nuitka will give the same error messages for all kinds of errors. For
   example, the parameter parsing of functions will be the same.

-  Nuitka provides all language constructs no matter how absurd or
   unused they are.

*************************
 Compatibility != Slower
*************************

While generally Nuitka will have a hard time to be faster *and*
compatible to CPython, I don't have much concern about that. Using
guards between optimistic, and less optimistic variants of code, there
is no doubt in my head, that for programs, lots of code will only need
very minimal type annotation and still receive respectable speedups.

Of course, at this point, this is only speculation. But I somehow gather
that the sentiment is that incompatible and fast *need* to go along. I
totally dispute that.

*********************
 Language Extensions
*********************

Now, the "in addition" stuff, that Stefan is talking about. I don't see
the point at all. It is quite obvious that everything you can say with
``cdef`` syntax, could also be said with a more Pythonic syntax. And if
it were missing, it could be added. And where it's a semantic change, it
should be frowned upon.

For the Nuitka project, I never considered an own parser of Python. No
matter how easy it would be, to roll your own, and I understand that
Cython did that, it's always going to be wrong and it's work. Work that
has no point. The CPython implementation exhibits and maintains the
module ``ast`` that works just fine.

For Python, if this were so really useful, such language extensions
should be added to Python itself. If there were missing meaningful
things, I contend they would best be added there, not in a fork of it.
Note how ``ctypes`` and ``cffi`` **have** been added. When I created
bindings for Ada code (C exports) to Python, it was so easy to do that
in pure Python with ctypes. I so much enjoyed that.

So, slow bindings are in my view really easy to create with plain Python
now. Somebody ought to make a ".h" to ``ctypes``/``cffi`` declarations
converter, once they are really faster to use (possibly due to Nuitka).
For Nuitka it should be possible to accelerate these into direct calls
and accesses. At which point, mixing generated C code and C include
statements, will just be what it is, a source of bugs that Nuitka won't
have.

.. note::

   Further down, I will give examples of why I think that ``cdef`` is
   inferior to plain Python, even from a practical point of view.

****************************
 Lack of Interpreter is bad
****************************

Static compilation vs. interpretation as a discussion has little merits
to me. I find it totally obvious that you don't need static compilation,
but 2 other things:

#. You may need interpretation.
#. And may need speed.

To me static code analysis and compilation are means to achieve that
speed, but not intended to remove interpretation, e.g. plugins need to
still work, no matter how deep the go.

For Cython syntax there is no interpreter, is there? That makes it loose
an important point. So it has to have another reason for using it, and
that would be speed and probably convenience. Now suppose Nuitka takes
over with these benefits, what would it be left with? Right. Nothing. At
all. Well, of course legacy users.

The orinal sin fall of PyRex - that is now Cython - is nothing that
Nuitka should repeat.

************
 No Lock-in
************

The Cython language is so underspecified, I doubt anybody could make a
compatible implementation. Should you choose to use it, you will become
locked in. That means, if Cython breaks or won't work to begin with, you
are stuck.

That situation I totally despise. It seems an unnecessary risk to take.
Not only, if your program does not work, you can't just try another
compiler. You also will never really know, if it's either your fault or
Cython's fault until you do know, whose fault it is. Find yourself
playing with removing, adding, or re-phrasing ``cdef`` statements, until
things work.

Common. I would rather use PyPy or anything else, that can be checked
with CPython. Should I ever encounter a bug with it, I can try CPython,
and narrow down with it. Or I can try Jython, IronPython, or low and
behold, Nuitka.

I think, this totally makes it obvious, that static compilation of a
non-Python language has no point to people with Python code.

What I will always admit, is that Cython is (currently) the best way to
create fast bindings, because Nuitka is not ready yet. But from my point
of view, Cython has no point long term if a viable replacement that is
Pythonic exists.

*************************
 Python alone is a point
*************************

So, if you leave out static compilation vs. interpretation and JIT
compilation, what would be the difference between PyPy and Nuitka? Well,
obviously PyPy people are a lot cooler and cleverer. Their design is
really inspiring and impressive. My design and whole approach to Nuitka
is totally boring in comparison.

But from a practical standpoint, is there any difference? What is the
difference between Jython and PyPy? The target VM it is. PyPy's or
Java's. And performance it is, of course.

So, with Python implementations all being similar, and just differing in
targets, and performances, do they all have no point? I believe taken to
the logical conclusion, that is what Stefan suggests. I of course think
that PyPy, Nuitka, and Jython have have as much of a point, as CPython
does.

*****************************
 Type Annotations done right
*****************************

And just for fun. This is making up a use cases of type annotations:

.. code:: python

   plong = long if python_version < 3 else int


   @hints.signature(plong, plong)
   def some_function(a):
       return a ** 2

Notice how ``plong`` depends on an expression, that may become known
during compile time or not. Should that turn out to be not possible,
Nuitka can always generate code for both branches and branch when
called.

Or more complex and useful like this:

.. code:: python

   def guess_signature(func):
       types = [None]

       emit = types.append
       for arg in inspect.getargnames(func):
           if arg == "l":
               emit(list)
           elif arg == "f":
               emit(float)
           elif arg == "i":
               emit(int)
           else:
               hints.warning("Unknown type %s" % arg)
               emit(None)

       return hints.signature(*types)


   def many_hints(func):
       # Won't raise exception.
       hints.doesnot_raise(func)

       # Signature to be inferred by conventions
       guess_signature(func)(func)

       # No side effects
       hints.pure(func)


   @many_hints
   def some_func1(f):
       return f + 2.0


   @many_hints
   def some_func2(i):
       return i + 2


   @many_hints
   def some_func3(l):
       return i + [2]

This is just a rough sketch, but hopefully you get the idea. Do this
with Cython, can you?

The hints can be put into decorators, which may be discovered as
inlinable, which then see more inlines. For this to work best, the loop
over the compile time constant code object, needs to be unrolled, but
that appears quite possible.

The signatures can therefore be done fully automatic. One could use
prefix notation to indicate types.

Another way would put fixed types for certain variable names. In Nuitka
code, "node", "code", "context", etc. have always the same types. I
suspect many programs are the same, and it would be sweet, if you could
plug something in and check such types throughout all of the package.

And then, what do you do then? Well, you can inspect these hints at run
time as well, they work with CPython as well (though they won't make
things faster, only will that find errors in your program), they will
even work with PyPy, or at least not harm it. It will nicely JIT them
away I suppose.

Your IDE will like the code. syntax highlighting, auto indent will work.
With every Python IDE. PyLint will find the bugs I made in that code up
there. And Nuitka will compile it and benefit from the hints.

My point here really is, that ``cdef`` is not flexible, not standard,
not portable. It should die. It totally is anti-Pythonic to me.

***********
 Elsewhere
***********

In Java land, people compile to machine code as well. They probably also
- like stupid me - didn't understand that static compilation would have
no point. Why do they do it? Why am I using compiled binaries done with
their compiler then?

And why didn't they take the chance to introduce ubercool ``cdef``
a-likes while doing it? They probably just didn't know better, did they?

No seriously. A compiler is just a compiler. It takes a source code in a
language and turns it into a package to execute. That may be a required
or an optional step. I prefer optional for development turn around. It
should try and make code execute as fast as it can. But it should not
change the language. With Cython I have to compile. With Nuitka I could.

In fact, I would be hard pressed to find another example of a compiler
that extends the interpreted language compiled, just so there is a point
in having it.

************
 Conclusion
************

Nuitka has a point. On top of that I enjoy doing it. It's great to have
the time to do this thing in the correct way.

So far, things worked out pretty well. My earlier experimentations with
type inference had shown some promise. The "value friends" thing, and
the whole plan, appears relatively sound, but likely is in need of an
update. I will work on it in december. Up to now, and even right now I
worked on re-formulations, that should have made it possible to get more
release ready effects from this.

When I say correct way, I mean this. When I noticed that type inference
was harder than it should be, I could take the time and re-architecture
things so that it will be simpler. To me that is fun. This being my
spare time allows me to do things this efficiently. That's not an
excuse, it's a fact that explains my approach. It doesn't mean it makes
less sense, not at all.

As for language compatibility, there is more progress with Python3. I am
currently changing the ``class`` re-formulations for Python2 and Python3
(they need totally different ones due to ``metaclass`` changes) and then
"test_desc.py" should pass with it too, which will be a huge achievement
in that domain. I will do a post on that later.

Then infrastructure, should complete the valgrind based benchmark
automatism. Numbers will become more important from now on. It starts to
make sense to observe them. This is not entirely as fun. But with
improving numbers, it will be good to show off.

And of course, I am going to document some more. The testing strategy of
Nuitka is worth a look, because it's totally different from everything
else people normally do.

Anyway. I am not a big fan of controversy. I respect Cython for all it
achieved. I do want to go where it fails to achieve. I should not have
to justify that, it's actually quite obvious, isn't it?

|  Yours,
|  Kay
