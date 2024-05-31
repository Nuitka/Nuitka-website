.. post:: Jun 28, 2023
   :tags: Python, Nuitka, compiler, stream

#########################
 Next Nuitka Live Stream
#########################

Tomorrow, Thursday 30.06.2023, there will be the forth live stream of me
coding on Nuitka, and talking and chatting with visitors in the Discord
channel created specifically for this. I will go from 11-14 CEST and
potentially in the evening, maybe 18-20 CEST as well, but it seems I
tend to go overtime.

###########
 Last time
###########

So, with me starting to stream last year, then I went all in on Nuitka
with the commercial offering, and suddenly, there was a lot of things to
do, while at the same time, the 3.11 support was harder than ever before
to add for a new minor version of Python.

So the last four streams are on my Youtube, these are around 4h videos,
always done two on the same day. Lets see how long I last this time.

I honestly forgot where I was last time, but I know that I started a
kind of optimization, where iteration over randomly accessible types,
gets converted to integer lookups, avoiding an iterator creation and
release.

###########
 This time
###########

That unfinished optimization, as far as I recall, with automatically
unlock optimization in terms of standard library parts becoming smaller,
and probably should be on the radar if only because of that.

It may only lack the releases to be converted to something, I will need
to check though.

I have been tagging issues with ``stream`` tag too, so maybe that is
also something to look at.

Not sure yet, what to do. I will definitely start with a quick look at
what new toys there are in Nuitka, esp. the Yaml stuff is very nice.

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
