.. post:: 2024/01/12
   :tags: Python, compiler, Nuitka, NTW
   :author: Kay Hayen

######################
 Nuitka this week #14
######################

.. contents::

**************************
 Communication vs. Coding
**************************

After GSoC 2019, it seems I dropped off with communication about Nuitka
quite a lot, e.g. I stopped "Nuitka This Week". The reasons are
multi-facetted. I think part of the reason is that I was getting busy,
part of it clearly also was Corona. But also a more dreadful change in
my private life, where the real life Nuitka, my wife, became ill for a
long time. Effectively it's only become really better mid last year.

I think, this caused me to go full into code for Nuitka, and to launch
Nuitka commercial, but generally to become more quiet. I have already
relaxed this for a bit, e.g. about Python 3.11, I made a bunch of
postings.

So this one is a bit general to start off, but I also provide fairly
recent details about what I worked on for 2.0 as well.

**************************
 Nuitka has evolved a lot
**************************

From a usability standpoint, ever since I went `all in with Nuitka
</posts/all-in-with-nuitka.html>`__, but also before, the out of the box
experience of Nuitka has become ever better. And even 2.0 will take it
noticeable further. It's the premier choice for Python deployment if you
want efficiency. Its onefile mode is pretty great already and is
continuously getting better.

It's fair to say that Nuitka was great in 2019. I think in 2023 it
became almost amazing for deployment. This is in large part due to
working on the Yaml configuration and these things. In 2024 I hope to
get it really smooth.

I actually made posts about the Yaml stuff, and I will resume the series
shortly, basically it allows people to help improve the deployment side
of Nuitka, e.g. missing DLLs and data files, hacks needed, etc. for
packages, and it's quickly becoming better and more complete.

***********
 Community
***********

On the Discord server, I have been in touch with users of Nuitka a lot
more. You are welcome to join us on the `Discord server for Nuitka
community <https://discord.gg/nZ9hr9tUck>`__ where you can hang out with
the developers and ask questions. It's not intended as an interactive
manual. You are supposed to read the docs for yourself first.

I am also now occasionally on the Python Discord server. Mostly when I
get summoned to answer questions that my community thinks make sense,
and have been awarded the community role there, which is pretty nice. I
seem to make new connections there.

*******************
 Optimization Work
*******************

I think, it's in vain to explain what I did for performance in all that
time. Mostly, some technical debts for Python3 were collected, extending
to advantage in in speed of Nuitka over pure Python again. The advantage
compared on Python2 was not as present, and still is not, on Python3,
but for 3.10 it's pretty good.

The major breakthroughs have not happened. But I will be talking about
the plans, these sure are exciting. Lots of things are in place, some
are not, but I hope to get there.

********************
 Current Evolutions
********************

So many things on my mind right now, for one, I guess, 4 plugin changes
that I have yet to document in new postings. Two are visible here in
this code.

.. code:: yaml

   - module-name: 'toga.platform' # checksum: 4db91cac
     variables:
       setup_code: 'import toga.platform'
       declarations:
         'toga_backend_module_name': 'toga.platform.get_platform_factory().__name__'
     anti-bloat:
       - change_function:
           'get_platform_factory': "'importlib.import_module(%r)' % get_variable('toga_backend_module_name')"

First, the checksum. Nuitka is going to warn you about checking your
user yaml files for correctness in the future. Since it often finds
structural problems, very much needed, since yaml is whitespace
sensitive, and you never know what it is: a list, a dict, etc. but the
schema we created, can tell.

Second, ``variables`` are a new section, and in fact so new, they are
not even documented. They can be used to query values from code at
compile time. In this case we are using it to get at the backend to use,
so we can tell it at runtime. Otherwise, it's hidden to Nuitka, and
could e.g. still be subject to a changed decision from environment
variables, something we typically do not want.

For the third and fourth thing, we need another example. Torch can use a
JIT to speed up some things, with a compilation very similar to what
Nuitka does. That however needs a compiler and the source code on the
target platform. Not an easy ask for all kinds of deployments. A new
feature makes this easier than before.

.. code:: yaml

   - module-name: 'torch' # checksum: 84315db6
     parameters:
       - 'name': 'disable-jit'
         'values': 'value in ("yes", "no")'
     options:
       checks:
         - description: "Torch JIT is disabled by default, make a choice explicit with '--module-parameter=torch-disable-jit=yes|no'"
           support_info: 'parameter'
           when: 'standalone and get_parameter("disable-jit", None) is None'
     import-hacks:
       - force-environment-variables:
           'PYTORCH_JIT': '0'
         when: 'get_parameter("disable-jit", "no" if standalone else "yes") == "yes"'

So, what this does, is to make Nuitka accept parameters. The options
part is designed to complain when the default value is used in
standalone mode, kind of making the user acknowledge that it's the
intended value. For accelerated mode, we do not disable the JIT, since
we can expect to be in the same environment with source code intact.

With ``get_parameter`` you get the option value, and can be conditional
on it in the ``when`` block. That is the 3rd new thing.

The fourth new thing, is the forcing of environment variables. We have
so far done this, including in plugins like ``tk-inter`` manually with
post-load-code. The above is the same, effectively doing
``os.environ["PYTORCH_JIT"] = "0"`` if the JIT is to be disabled.

These changes are designed to avoid having to do plugins again.
Historically for ``toga`` support, we should have created a new plugin,
but now it's not necessary anymore, since the Yaml mechanism can cover
retrieval of compile time values from modules. And for ``torch`` and the
JIT, a plugin would have been needed to provide the command line control
for that decision.

This increased power of the Yaml will make it even less often the case
that a plugin must be written. But of course docs will have to be added
and maybe more places will need to work with variables to make that true
even more often. More on that in the future.

*********
 Teasers
*********

Future TWN will speak about Nuitka-Python (our own Python fork with
incredible capabilities), about Nuitka-Watch (our way of making sure
Nuitka works with PyPI packages and hot-fixes to not regress), about
compilation reports as a new feature, Windows AV stuff, onefile
improvements, and so on and so on. I got interesting stuff for many
weeks. Limiting myself for now or I will never publish this.

**********************
 Twitter and Mastodon
**********************

I should be more active there, although often I fail due to not wanting
to talk about unfinished things, so actually I do not post there as
much.

-  `Follow @kayhayen on Twitter
   <https://twitter.com/kayhayen?ref_src=twsrc%5Etfw>`_

-  `Follow @kayhayen on Mastodon <https://fosstodon.org/@kayhayen>`_

And lets not forget, having followers make me happy. So do re-tweets.
Esp. those, please do them.

*************
 Help Wanted
*************

If you are interested, I am tagging issues `help wanted
<https://github.com/kayhayen/Nuitka/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22>`_
and there is a bunch, and very likely at least one *you* can help with.

Nuitka definitely needs more people to work on it.
