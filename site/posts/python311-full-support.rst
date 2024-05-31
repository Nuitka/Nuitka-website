.. post:: 2023/08/01
   :tags: Python, compiler, Nuitka
   :author: Kay Hayen

#####################################
 Python 3.11 and Nuitka full support
#####################################

I kind of noticed, that I never really updated this post series to its
conclusion. Python 3.11 is now fully supported by Nuitka, that is the
TLDR. This has been the case since 1.6, and the 1.7 release improved on
it, and 1.8 well is around the corner, so it's about time to state it
now in dedicated form.

So, this post is kind of too late. My excuse is that well, there are
very exciting improvements in kind of all areas of Nuitka, and esp. even
recently, with long standing fixes for some memory leaks in 1.7 hot
fixes. These are usually very intense, adding new packages and fixing
old bugs usually, since there are usually very few regressions in
Nuitka.

*****************
 Lessons Learned
*****************

On thing I want to do better when 3.12 comes, is to be prepared for the
core changes, so work on 3.12 support has already started with the first
alpha, with Nuitka having a few commits (but not yet enough) to make it
work for basic compilation.

It will be more of a priority to follow CPython closer. It seems core
changes are becoming more involved, and it's better to not fall behind
too much. The delay in supporting 3.11 must have hurt Nuitka, since
bleeding edge users are also those reporting some import issues long
before commercial users of Nuitka even considering the environment.

So, well, maybe what I will be aiming at for a new Nuitka release 1.8
e.g. is to support the current pre-release of CPython. But I also want
to make releases more time based, i.e. not delay new features, and
sometimes important improvements longer than necessary. We shall see how
it goes.
