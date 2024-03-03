#######################
 Untruths about Nuitka
#######################

These are things that used to be true, but are not more. The
documentation often doesn't reflect that and should be changed.

***************************************************************
 Older MSVC can no longer with used with Python 3.11 or higher
***************************************************************

Because the Python upstream changed their code to newer C code, they now
require the MSVC 2022 to compile 3.11 and Nuitka follows suite, since it
also compiles that code in part.

Previously Nuitka has asked people to use MSVC 2022, but that is no
longer a request, but can become a requirement. Commercial users
however, often use older MSVC compilers, because they want to target
older Windows, but there Python 3.11 and compiled programs with that
won't run anyway.

*************************************
 Python 3.3 is not supported anymore
*************************************

Nuitka never supported 3.0 and 3.1, it at some point stopped supporting
3.2 which it once had, and 3.3 stood for a long time, but has been
removed a while ago, but the documentations and even code still mentions
it occasionally.
