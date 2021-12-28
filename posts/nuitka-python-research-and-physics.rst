#####################################
 Nuitka, Python research and Physics
#####################################

Once upon a time ago physics had multiple forces. Each with very
distinct traits. These were the early days. Then as time went on people
started to realize that weak nuclear force and electromagnetic force
were the same sort. That was after discovering that electricity and
magnetism were the same, and that is the pattern. It's called symmetry,
equivalence, and so on.

The `Nuitka </pages/overview.html>`_ project is effectively a Python
research that goes through the same steps. There are e.g. currently
local variables, closure variables (shared from containing function),
module variables, temp holder, temp keeper, and temp variables.

Often when I added one more this was driven by code generation needs or
deficiencies at the time. These are of course way too many, and all are
good at one thing only.

So the main task Nuitka is faced with now to e.g. generalize that "temp
keeper" variables are temporary variables local to one statement only,
surely to be released afterwards, and make that particular feature e.g.
work for all variables across the board. Right now, code generation uses
"cheats" where it puts a C++ block and local declarations for "temp
keeper" variables.

It would be good, if it could be a ``try`` with ``del`` statement on the
"temp keeper variable" in its ``finally`` part and yet, get the same
code generated. Difficult, yes, but not impossible, and definitely what
I am aiming at.

So that is what Nuitka will be dealing with in the next releases. Once
done, maybe there will be a "gravity", i.e. the one thing not yet
harmonized, but for good reasons. Potentially limited due to lack of
understanding, potentially because there is a good reason. And so not
all we be unified or maybe e.g. module variables will be a bit more
special than local variables, although modules are just functions with
variables writable everywhere.

Good stuff is coming, hold on. `Join the project
</doc/user-manual.html#join-nuitka>`_, or support it financially if you
wish.

Nuitka still is too much of a one man show. Should I be asked to name
one single weakness of it - that would be it.
