.. post:: 2013/12/27 10:48:22
   :tags: Python, compiler, Nuitka, Windows
   :author: Kay Hayen

############################################
 Nuitka Standalone Mode is Work in Progress
############################################

Many of you who turn to my easy to use, highly compatible Python
compiler `Nuitka <https://nuitka.net>`__, do this mostly because they
seek to solve the deployment problem that Python suffers from.

Be this, because you want to use a newer Python2.7 on RHEL5 without
installing anything at all there. Or because Windows is difficult to
tackle otherwise.

For the longest time, Nuitka had not offered anything in this domain,
focusing solely on being an accelerator. Lately, I have taken up the
challenge and polished initial solutions submitted by contributors.

This first showed up in the 0.4.7 release, but turned out relatively
weak. While first examples were working on Linux, it was not working at
all on Windows (anymore). And basically there was a huge lack of tests.

Actually I didn't mean for it to be released with that feature, but as
parts of it seemed to work, I did so. But truth to be sad, that feature
is not nearly as polished in that release as you would like it to.

In current `development releases </doc/download.html>`__, of what is
going to become 0.5.0 really soon now, it's much better already. More
things actually work. But it appears, there will be more ground to
cover, and this is a lot of stuff to sort out.

So, this is mostly about asking you two things. Give that development
release a try and report issues you have with it. And help me.

And have patience. I am developing Nuitka as an accelerator on a "no
known bugs" basis. That means, once I know of a bug, I will fix it. OK,
some issues in fact take longer, but then it really is not important at
all, but difficult at the time. For standalone mode, I can't do it that
way, or I would have to neglect the acceleration parts, which I totally
don't want to do.

Because while you maybe are only interested in a packaging solution,
many others would like to have that orders of magnitude speedup that I
have been aiming for and that feels near now. This is about making
Python a viable language for more uses than it currently is.

So why do it in the first place. For one, I am hoping that it helps
people to not turn away from Python. And second, and more important, I
am hoping that by making it more useful, more people will join me. (Oh,
and thirdly, it's also a nice puzzle to solve. I seem to enjoy that.)

Ultimately both modes will be needed, standalone, and acceleration. And
it seems like I am working to provide both. For standalone, more often,
than seeking to avoid bugs as far as possible, I am going to rely on
your participation.

So join Nuitka. Now. `Download from here </doc/download.html>`__. Join
the mailing list (since closed). And help if you can. And yes you can.
