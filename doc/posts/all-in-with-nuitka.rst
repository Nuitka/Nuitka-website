.. post:: 2022/12/08 18:27:44
   :tags: Python, compiler, Nuitka, NTW, stream, package_config
   :author: Kay Hayen

####################
 All in with Nuitka
####################

After more than 10 years of working on the Python compiler Nuitka, and
at the age of 50, I have finally decided to take the plunge. My projects
"Nuitka" and "Nuitka commercial" are now my *day job*, and I quit my
work in the Air Traffic Community, after working on `ARTAS
<https://en.wikipedia.org/wiki/ARTAS>`__ (a software to create an Air
Situation Picture from radar and other sensors) for 20 years.

##########
 Why now?
##########

That is very good question. I feel I could have done this a long time
ago, and my heart was torn for a while, and also I prepared this for a
while now. Listing back to interviews from 4 years ago, it seems though
as if it had not been on the radar (pun intended).

So then I launched Nuitka commercial around 1.5 years ago, first as
vapor ware, with early bird customers, and meanwhile it has matured to a
point, where it is the obvious solution to many corporate users, with
big guys picking it up and small business as well. From startups, big
name technology giants, universities, mid sized companies, and from
individuals, I have all kinds of support.

I liked my old job very much, but it was getting old, and I felt like
Nuitka needs me to fulfil my mission. And my wife needed my help with
driving her to work, which was getting the load to high, something had
to give. And it seems nothing related to what is called Nuitka (my wife,
and the compiler share the name) was going to be that.

###################
 What will change?
###################

Already, ever since I launched Nuitka commercial, Nuitka has become way
more of a out of the box experience. It just works, and covers more
packages than ever before, and steps have been taken, to make it
possible to extend this even further with your help. Sure there are
still shortcoming.

But Nuitka has become very polished, and shows this very much that I
also love details and doing things correctly. I have conducted Nuitka
from day one as an attempt to create a software that would be usable to
the enterprise with a million lines of code, that they cannot check for
unsupported language features, so Nuitka is just fully compatible, to a
level of absurdity.

Having conducted Nuitka on a level of where a corporate business can
throw it's code at Nuitka and have it just work, and reliably, this will
only improve now.

Naturally bugs have happened once in a while, but I was always more
careful. You know, like if this was for safety critical software, on
which lives might depend. Hard to not be affected by that stance.

So lets talk about other ways I plan to expand.

##############################
 Nuitka Package Configuration
##############################

Extending Nuitka with tweaks for package has become increasingly
simpler. Many previous plugins, e.g. for ``torch``, ``tensorflow``, and
most recently ``numpy``, and definitely also the Qt binding ones in the
future, have been or will be converted to Yaml configuration applied by
generic plugins that deal with DLLs, data-files, tweaks (called
``anti-bloat``) etc.

Adding stuff there is simple, and as of recently, there is even
documentation for it. This is going to be explained in a series of posts
detailing Nuitka package configuration, under the ``package_config``
tag.

I must say it's so much fun, I love working with it. But the goal is for
this to have you join it, and PRs are indeed starting to come in more
frequently it seems from first glance, but I need to make this more
known.

###########
 Streaming
###########

I have experimented with streaming in the past, and I absolutely love
it. Without my day job, effectively working two jobs at the same time, I
expect to have the time to do more of them in December and then on a
regular basis.

#############
 Python 3.11
#############

There will be a separate post on this issue later this week. I am
scrambling to add support for it and it feels very far already. Many
basic tests already work, but more debugging will be needed. I hope
Nuitka 1.3 will add support for it, at least on the usual experimental
level.

###################
 How you can help?
###################

Please become a `subscriber of Nuitka commercial
<https://nuitka.net/doc/commercial.html>`__, even if you do not
need the IP protection features it mostly has. All essential packaging
and performance features are free, and I have put incredible amounts of
works in this, and I need to now make a living off it.

Right now, I am far from being able to sustain my income from it, and I
am taking a risk with this effort, hoping for support from you.

Nuitka commercial makes creating a Windows Service a blast. It has a
PySide2 that is compatible with Nuitka (I did make PySide6 compatible
myself, and backported it to PySide2), so if you need to stay on old
software. And for IP protection, it is just incredibly important to not
ship bytecode at all, and with Nuitka commercial, it protects your data
and files at runtime too.

I am bad at marketing, but good at software, which is one more reason to
purchase it. You know you love these kinds of people. Was that good
marketing? Also, there are share buttons on this page. Please try them
out and let people know about this.

In future postings, I will make it a regular thing to ask for help with
some of the technical tasks. Stay tuned, there might be something that
you can help with.

######################
 Becoming more active
######################

I am the kind of person that would much rather do good stuff than to
talk about it, like when it finally supports Python 3.11, normal old me
would just mention it maybe on Twitter once, and have it in the
changelog only.

I need to get away from that. I need to resume TWN (This week in Nuitka)
and have all plans to do it. Obviously I can get caught up in things,
and may just always do it later when there is more or better news.
