.. post:: May 27, 2022
   :tags: Python, Nuitka, compiler, stream

#########################
 Next Nuitka Live Stream
#########################

In the coming weekend, Saturday 04.06.2022, there will be the next live
streams of me coding on Nuitka, and talking and chatting with visitors
in the Discord channel created specifically for this. I will go from
10-14 CEST and potentially also one in the evening.

###########
 Last time
###########

It's actually been too long for me to remember what I did, but I do know
that it took some time to get it right. It probably was about caching,
but there are usually several topics.

I do however think that I need to use my CI machine with more processing
power rather than my normal desktop, or maybe even both, because the
screen capture, compiling, VS Code, and all, may make the Video
otherwise stutter a bit too much.

###########
 This time
###########

So, streaming is a huge success or Nuitka, however time is also scarce,
and me starting new things, risks the release being bogged down by
stabilization phases that are extended.

Not sure yet, what to do. I think, I want to look at adding the ``int``
as a C type and/or specializing code for mix of ``CLONG`` (C long value)
and ``LONG`` (Python3 ``int`` object) and ``INT`` (Python2 ``int``
object). Right now adding ``1`` goes through a constant object, one that
is prepared, and not time consuming to reference, but still overhead to
use.

#########################
 How to Join Nuitka Live
#########################

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
