.. post:: 2011/08/16 18:21
   :tags: git, Nuitka, Python
   :author: Kay Hayen

####################################
 Nuitka has a new home - nuitka.net
####################################

Hello everybody,

my new vServer is now online, the old site blog redirects to it now, and
planets follow the new site already. The old site is redirecting with
301 error code for some more time, hopefully this will be good enough of
a migration. It felt smooth from here, clearly, and the new site is much
faster of course, because it's not throttled through my poor DSL
upstream.

I also registered it a domain name `"nuitka.net" <https://nuitka.net>`_
for it finally. Originally I wanted to give it a DynDNS name, but I
already have 2, and the third was supposed to cost money, and I didn't
feel like using another service, or cheating them if you consider that
an option, so that was it, I bought the domain name. Clearly it will
also be easier for people to remember.

Moving things over was pretty painless. The Wordpress software has a
pretty good export feature, which only didn't manage the custom menu and
appearance settings. But I guess it's about content anyway, so probably
some way that would work too, but it was easy enough to reproduce that
by hand. I appreciate Wordpress even more now.

Also I did some tuning of the system, to use less memory. Only 512M are
available, and so I run less Apache processes for less requests (memory
leaks), disabled IPv6 (yes, hate me for it), reduced amounts of gettys,
and so on. Nothing I am not familiar with, the ARM machine had 512M as
well, and to me no reason to use the bigger package just because of
that.

The main difference is the faster CPU, I seem to get 3Ghz Intel now,
instead of my 1Ghz ARM, which together with faster internet speed, makes
the site extremely fast.

Now U will dare to make the `gitweb interface
</gitweb/?p=Nuitka.git;a=summary>`_ public as well. The git repository
is already running there.

.. note::

   This is obsolete information, we use Github for this now.

And I took the chance to sanitize the old posts somewhat. Changed the
links to not use the old domain name anymore, and correct some broken
ones too.

Only downside is that I currently haven't got the `"speedcenter"
<https://speedcenter.nuitka.net>`_ up and running again. After losing my
hardware, the old data cannot be compared with new one, and then it
doesn't feel like a priority right now. I seem to be working instead on
XML based regression tests of the optimizer: The output of "--dump-xml"
should be compared for a large quantity of files, to discover
regressions of the optimizer as soon as possible, this will enable me to
make changes and not have to review the C++ as much, to find out if
something is compiled correctly. This way I should detect it when known
good cases degrade, and generally to demonstrate better, what actually
did improve.

|  Yours,
|  Kay Hayen

PS: Oh, you people, who wonder, "but why are you not using
Google/github/gitorious?", my counter question: "Did you read the
agreement?" I did. It basically says (from Google code):

.. code::

   13. INDEMNITY

   You agree to hold harmless and indemnify Google, and its subsidiaries, affiliates, officers, agents, employees, advertisers, licensors, suppliers or partners, (collectively "Google and Partners") from and against any third-party claim arising from or in any way related to your use of Google services, violation of the Terms or any other actions connected with use of Google services, including any liability or expense arising from all claims, losses, damages (actual and consequential), suits, judgments, litigation costs and attorneys' fees, of every kind and nature. In such a case, Google will provide you with written notice of such claim, suit or action.

No thank you, instead I will run my own server, then I get to pay the
attorneys of my discretion - in the admittedly unlikely event that
somebody should sue me, because my Compiler violates some patent, or
whatever.

|  Yours,
|  Kay
