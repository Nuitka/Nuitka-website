.. post:: Jan 30, 2022
   :tags: Python, Nuitka, compiler, stream

#########################
 Next Nuitka Live Stream
#########################

Today, Sunday 30.01.2022, there will be the third live stream of me
coding on Nuitka, and talking and chatting with visitors in the Discord
channel created specifically for this. I will go from 9-12 CEST and from
18 CEST until probably at least 20 CEST, but it seems I tend to go
overtime.

###########
 Last time
###########

So the last two streams are on my Youtube, these are around 4h videos,
done on the same day.

In the second stream I was working on Onefile compression for all Python
versions, by making the location of another Python that for Scons we
sort of did already, reusable. So now, you can run Nuitka with Python2.6
and compile your legacy code, while with say 3.6 also installed on the
same system, you do the ``zstandard`` compression. That will be used for
other things in the future as well. This is going to be part of the next
release and currently on develop.

In the first stream, I also did a little bit of performance plans, but
mostly only showing people what I have there in stock, not actually went
there and I started work on a ``upx`` plugin, such that DLLs for
standalone are compressed with that. That also required a bit of plugin
interface changes and research. This one works mostly, but will need
more live. Also I think I looked at reducing what is included with the
follow standard library option, getting very minimal distributions out
of it.

###########
 This time
###########

All around, this last stream, was a huge success. I was a bit under the
weather last weekend, but we go on now.

Not sure yet, what to do. I might be debugging issues I have with 2.6
and a recent optimization, that prevents factory branch from becoming
the next pre-release, I might be looking at macOS still. And I might be
looking at the caching of bytecode demoted modules, that is kind of
ready to be used, but is not currently, which is a pity. And of course,
the Python PGO may get a closer look, such that e.g. it works for
standalone mode.

#############
 How to Join
#############

There is a `dedicated page on the web site </pages/Streaming.html>`_
which has the details. Spoiler, it's free and I have no plans for
anything that involves a subscription of any kind. Of course, talking of
subscription, do also checkout the `Nuitka commercial
</doc/commercial.html>`_ offering. That is a subscription with adds that
protect your IP even more than regular Nuitka.

#########
 Join me
#########

Come and join me there. `Instructions </pages/Streaming.html>`_ here.
You know you want to do it. I know I want you to do to it!

|  Yours,
|  Kay
