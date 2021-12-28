State of Nuitka
~~~~~

.. contents::

For quite some time, publicly, very little has happened with my Python compiler
Nuitka. But that doesn't mean, there hasn't been progress. In fact it is
tremendous. I would like to have a post that kind of summarizes, what happened.

The last release, 0.5.1 was more of a maintenance release than making real
changes. It turns out, that the bigger changes got delayed by a feature that I
have described as "C-ish". Let me outline, what this means.

C-ish vs. C++-ish
-----------------

When I started working on Nuitka, the big question was if it is possible to
create a sufficiently compatible compiler. The use of C++11 then, together with
some templates made it easy to cover a wide, wide part of the language, and to
fully integrate with CPython for compatibility.

The main goal was to get it going to work correctly. As time went on, execution
order demanded to do away with variadic templates, raw strings were not all
that perfect at all, and so C++-03 was good enough at one point.

And then, as Nuitka became less and less template based, and shoving more
things into the node tree, and re-formulations, making this where the knowledge
resided. It became more and more obvious that C++ has two problems. One in the
way I used it. One inherent in the language typical implementations:

* C++ exceptions are god damn slow

* Everything should be a in a single statement.

The later was my choice. Initially it made it easy to pass on references and
put the releasing C++ class around every expression as necessary. Identifier
classes were allowing for code generation to avoid taking references where
necessary, and it was not all that bad. Yet limiting.

This led to a couple of issues.

* The order of call arguments release for e.g. ``f(g(h()))`` was not completely
  compatible, with the way how CPython does it. C++ destructors for objects
  living in a single statement didn't give sufficient control, and make the
  order and timing of finalization not compatible.

* The generated C++ code complexity became large. The compilation of the
  generated C++ in some cases was huge. To the point, that e.g. "code too
  complex" was giving by compilers like MSVC for some modules.

* Cases of in-place assignments were discovered, where CPython outperforms
  Nuitka by a large margin. But these don't fit into that style of code
  generation.

So, at some point, the pain had built up. Code generation was already lighter
than in the beginning. For example, initially ``with`` statements had dedicated
code templates to them. This, and many other things, are long gone.

I took a deep dive, and **rewrote** the whole code generation, to be much more
"C-ish" than "C++-ish". A huge undertaking that would take months.

* Where previously, code didn't have to handle return error codes (a C++
  exception was thrown), now everything needed a return value name, and error
  check.

* Where classes were previously conviently made sure things happened at
  function or scope exit, manual handling needed to be added.

* The handling of ``continue``, ``break``, and ``return`` was previously done
  with exceptions being thrown, if they were to pass a ``try``/``finally``
  handler. Now these are done with stacks of exit handlers, where ``goto``
  statements are used to produce the correct behaviour.

Rewriting Code Generation
-------------------------

Redoing code generation, over months, while ultimately, slowly, arriving at a
point where Nuitka would be doing this, it already did before, was kind of
frustrating.

Of course, the performance benefit would be there, but it would not be all that
much, except for exception raising and handling. There it would be
huge. Ultimately for PyStone, a couple of extra percents were gained.

This really was a point, where I felt, that Nuitka will make it or break. And
for a long time, I honestly wasn't so sure, that I pull through. But I did.

Current Situation
-----------------

The current pre-release is release quality. You should try it out, it's great.

* There are many changes to Standalone mode. Due to changes in how constants
  are now created in the modules that uses them, instead of everything
  globally, the parallel compilation now works great. What previously took an
  hour with MSVC (the problem child, gcc was always relatively good), now takes
  minutes only.

* The support for virtualenv's of all kinds seems to work on Windows, Linux,
  and macOS, which all seem to have different kinds of codes.

* The support for macOS is now there. Thanks to a virtual server month donated
  to Jarrad Hope, I was able to iron issues out.

* The final release will also work with standalone binaries created on Fedora
  20 which got hard code rpaths removed on the factory git branch.

And yet, I am not yet releasing. In fact, I would like to ask you to give it a
roll, and integrate test feedback.

Although more tests than ever are executed and pass, (e.g. the Mercurial test
suite is now run each time I make a commit, and fully identically passes or
fails the test suite with the current Mercurial code), there can never be
enough.

The changes I made are the most intense ever, and definitely have potential for
regressions. I am used to providing very high quality releases.

Also, I am working on the Buildbot instances to automate the production of
`performance graphs <https://speedcenter.nuitka.net>`__, which get updated fully
automatically. I am working on updating the downloads page automatically for
each release that gets made.

And generally, I am trying to improve my work flow, to make it easier to push
out releases with less effort. Buildbot should drive the release process more
completely. I am using the git flow to provide hot-fixes, and this should be
even less painful in the future.

Open Points
-----------

With this release, presenting great progress, many things remain in an
unfinished state.

* The support for Python3.4 is not complete. Most things work, but some need
  more work. Specifically the changes to ``__class__`` variable closure taking,
  need another major refactoring, this time on variable handling.

  Currently there are variables, closure variables, temp variables, and then
  temp variable references. The way they work is different. One way they work
  different, prevents a temp variable closure reference to carry a name, in
  that case ``-_class__``, which would be needed for Python3.4, where that is
  suddenly necessary.

  With this done, the SSA code will be even easier to write, as temp variables
  and named variables will finally be fully unified.

* The use of C++ classes is largely reduced now. But a few still remain, namely
  for local variables, closure variables, and temp variables that are explicit
  variables. They still use C++ classes, although changing that seems quite
  possible now, because at least for temporary variables, the class doesn't do
  anything in terms of code anymore.

  Removing these classes may well gain more performance.

* Now that code generation can more easily make a difference, and SSA
  apparently is becoming reliable, it could be used to *know* that values must
  be value and to optimize checks away.

  Currently every variable access checks for "NULL", when it's part of an
  assign trace. Some optimizations exist for parameter variables without
  ``del`` on them, that do not use SSA.

  This could be expanded and made general, allowing for much less code to be
  generated (specifically avoiding error code, and release code for variables
  that cannot give an error).

* The SSA has been found unreliable in some instances, due to bugs that I
  believe I found. We could attempt and forward propagate variable assignments
  to where they are used, eliminating variables, etc.

  This is a place, where a lot of performance can be gained. We really want to
  be there. And "C-ish" now makes this ever more attractive, despite the large
  delay in time it has caused.

* The in-place assignment code for strings, where CPython can be way faster
  than current Nuitka, it bears a risk of getting it wrong. It is therefore
  pushed to a future release.

Other Things
------------

For the website, I am relocating the virtual machine to a dedicated server
rented for an increased price. This will allow to add a few more dynamic
features, as the virtual machine was always too limited in RAM. It's more
expensive, but I feel a better investment of my time.

As mentioned before, I am not going to conferences this year. Enjoy Europython,
and consider having a Lightning talk about Nuitka. I will be there next year
again.

Call for Help
-------------

* Please test the latest release of Nuitka.

* Please consider `making a donation <http://nuitka.net/pages/donations.html>`_
  to support my work on Nuitka. I have continuous monthly costs of it, so it
  would be sweet if it's with all my time spent working on it, at least not a
  financial cost to me.

* Please join the mailing list (since closed), and offer your help with tasks.
  Nuitka can seriously take more people developing, testing, reviewing, and
  quality checking it.

Final Words
-----------

So, there is this "C-ish" release 0.5.2 cooking. You are invited to help. Big,
improvements are coming to Nuitka. Even after this next huge release, very
important work is still open, but hope is to have this complete over the
summer.

| Yours,
| Kay
